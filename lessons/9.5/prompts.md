# Lesson 9.5 prompts and commands

Everything typed in the lesson, in order. Lines that start with `!` run in the terminal from inside Claude Code
(shell mode: your own shell command, not a request to Claude). Lines that start with `/` are Claude Code commands.
Every request runs in auto mode. Only the H3 download (part 5) needs IB Gateway, logged in to the paper account.

## 1. Build the factory

```text
/clear
```

```text
Time to turn the research loop into a factory. Set up three researcher subagents in .claude/agents/, one per strategy family: breakout and momentum, mean reversion, and time-of-day effects. Each one takes one journal idea from its family, follows our loop (spec, code with tests, the judge, a strategy card, the journal row), never touches the judge or the holdout, and stops after its budget. Then write research/leaderboard.py: it reads the audit log and the cards, ranks every strategy the judge has scored, drops exact duplicates and any strategy whose daily returns correlate above 0.7 with a better one, and writes research/leaderboard.md. Run it on what we have now, add a --parallel option to research_batch.sh so the families run side by side with one total time budget, do a dry run, and commit.
```

In the video this took about 9 minutes. Claude wrote `research/leaderboard.py` (384 lines, then a plainer duplicate
check) and 10 tests, ran it on the lab's earlier work (14 runs read, 1 duplicate and 6 look-alikes dropped, 7 on the
board, none passing all 8 rules), wrote `research/LOOP.md`, `research/families.txt` and the three agents, rebuilt
`scripts/research_batch.sh` around one lane per family, checked both dry runs and that `claude -p --agent <name>` loads
an agent, and committed (331 tests). The judge guard from Lesson 9.4 blocked three of its commands along the way (a
combined read that printed the judge with `sed`, a `git add` of the ledger files, and a here-doc that named locked files);
each time Claude switched to an allowed tool.

## 2. Launch a run

```text
/clear
```

```text
Launch the factory run: research_batch.sh with the three families in parallel, a 3-hour total budget, at most 40 turns per idea, full mode, logs as usual. Start it in the background so it keeps going when this session ends, show me the first ideas starting, and tell me what you expect to find when it's done.
```

The command Claude ran (yours may differ in the log name):

```bash
setsid nohup scripts/research_batch.sh --parallel --budget-minutes 180 --max-turns 40 > research/batch_logs/_run_$(date +%Y%m%d_%H%M).out 2>&1 &
```

`setsid nohup ... &` detaches the run from the terminal, so closing Claude Code does not stop it. We ran it for three
hours during the day; the same command runs overnight with a longer `--budget-minutes`. In the video every idea finished
in about 5 minutes. Our commit hook (Lesson 3.6) fired at the end of the turn because the lanes had files open; Claude
left them alone, since each lane commits its own files.

## 3. Review the run honestly

```text
/clear
```

```text
The factory run has finished. Show me what it did: the leaderboard, every new card, how many trials it added to the ledger, how long and how many turns each idea took, and anything that broke. Then give me an honest review: is anything here worth paper trading in the next module, or did we mostly learn what doesn't work?
```

In the video: six ideas in about 5 minutes, zero judge runs, zero trials added. Five ideas stopped at the cheap check
(no effect, loses before costs, too few days, or a diagnostic only); idea C was built and tested but blocked on its
`STRATEGIES` entry. The Cost column in the run table is Claude Code's API-price estimate for each `claude -p` session. On
a subscription nothing is billed per run; it counts toward your plan's usage.

## 4. Close idea C: a patch you apply

Same session.

```text
Yes to H3, as soon as the Gateway is logged in later today. First, give idea C its closure: put the vwap_trend STRATEGIES entry in a patch file I can review and apply myself. Once I've applied it, run the judge on it, update the card and the journal, and commit.
```

Read the patch, then apply and commit it yourself:

```text
! cat research/patches/0002-judge-vwap-trend-strategies-entry.patch
! git apply research/patches/0002-judge-vwap-trend-strategies-entry.patch && git add judge/scorecard.py && git commit -m "judge: add the vwap_trend STRATEGIES entry (reviewed patch 0002)"
```

Then tell Claude it's applied (in the video Claude picked it up from the shell-mode output and ran the judge at once).
The first judge run crashed inside the new strategy (too few bars for its stop distance at the start of a walk-forward
window); Claude added a warm-up guard and a test that fails without it. The rerun: FAIL, 4 of 8. The guard blocked
Claude from committing the ledger rows, so that commit is yours:

```text
! git add research/trials.csv research/audit_log.jsonl && git commit -m "research: ledger and audit rows for the vwap_trend runs" && git push
```

## 5. Pre-register the out-of-sample test (H3)

Needs IB Gateway logged in to the paper account. Best with the market closed.

```text
/clear
```

```text
The Gateway is logged in and the market is closed, so it is time for H3 from research/journal.md. Step 1 only for now: write the frozen ORB settings and the exact test (symbols, the 2019-10 to 2024-09 span, costs, what we report) into the H3 row and a pre-registered card BEFORE any data exists, and commit that. Step 2: give me the exact backfill command to run in my other terminal (client ID 5, paper port) and how long IB's limits will make it take. Do not run the backfill or any backtest yourself.
```

In a second terminal, in the Lab folder (about 1.5 to 2 hours; if it stops, run it again and it resumes):

```bash
uv run -m data_pipeline --symbols QQQ SPY --bar-sizes 5min --backfill-years 7.1
```

Use the client ID your Lab reserves for downloads (5 in the video) and the paper port.

## 6. Move the old bars out, then the one run

After the download, a fresh session:

```text
/clear
```

```text
The H3 backfill has finished in my other terminal. Read the H3 card in research/cards and do step 3 only: quality-check the new QQQ and SPY bars (duplicates, gaps, sessions per year, half days), then move every bar before 2024-10-21 out of data/cache into data/oos so no other research command can read them, gitignore it, and prove the cache is back to exactly what it was before. Do not run any backtest yet.
```

```text
Step 4. Write the H3 script exactly as the card freezes it, reading only data/oos, and commit it before running anything. Then run it exactly once. Fill in the Results section with every number the card lists, mention the March 2020 zero-volume bars, and give the verdict strictly by the pre-registered rules. No re-runs and no tweaks, whatever the result. Commit the card.
```

Change `2024-10-21` to the first date of your own research cache. In the video: FAIL by the pre-registered rules. QQQ:
901 trades, net -$155, Sharpe 0.03, Monte Carlo 5th-percentile drawdown -31.0%, 3 of 6 years up. SPY: Sharpe -0.03.

The last question in the video looks ahead to Module 10, where the Lab runs this strategy on a paper engine:

```text
Our paper engine runs this same ORB every day. Given this FAIL, what should we do with it? Answer in a few lines, add your recommendation to the research journal and commit it, but do not change the engine.
```

## Pause and try

1. Send request 1 and read `research/LOOP.md` and one agent file before you trust them.
2. Launch a short run (`--budget-minutes 30` is enough to see it work) and review it with request 3.
3. Pick your best idea and pre-register one test on data it has never seen, before you download that data.

You're done when the run leaves a card for every idea, the leaderboard is rebuilt, and your test card is committed
before its data arrives.
