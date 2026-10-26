# Student kit: Lesson 9.5, The factory at scale

Module 9: The strategy factory: goal-driven research loops · AI Algorithmic Trading with Claude Code and Interactive Brokers

In Lesson 9.3 one loop worked through the journal one idea at a time. In this lesson it becomes a factory:

1. **Three researcher subagents**, one per strategy family (breakout and momentum, mean reversion, time of day), all
   following one written procedure, `research/LOOP.md`, under a budget (8 judge runs and 1 new strategy per idea).
2. **A leaderboard** that ranks every judged run and drops exact duplicates and look-alikes (daily returns correlated
   above 0.7 with a better run).
3. **A parallel batch run** in the background, then an honest review: six ideas in about five minutes, zero judge runs,
   nothing to paper trade. Idea C is closed through a patch you read and apply yourself: FAIL, 4 of 8.
4. **One pre-registered test** of the best result on five years it had never seen (H3), written down and committed
   before the data was downloaded, run exactly once: FAIL, Sharpe 0.03 on QQQ.

The factory's value is fast, cheap, honest "no"s, each one written down.

## What's in this kit

| File | What it is |
|---|---|
| `prompts.md` | The requests typed in the lesson, the shell-mode commands to review and apply the patch and commit the ledger, the download command, and the pause-and-try exercise |
| `cheat-sheet.md` | The words, the factory file by file, the locks that still apply, how to read a factory run, a pre-registered test step by step, the numbers in the video |
| `trading-lab/research/LOOP.md` | The shared research procedure, the budget, the locked files, the shared-checkout git rules and the lessons from earlier ideas |
| `trading-lab/.claude/agents/researcher-breakout-momentum.md`, `researcher-mean-reversion.md`, `researcher-time-of-day.md` | The three researcher subagents |
| `trading-lab/research/families.txt` | Which journal idea belongs to which family. Edit it to match your own journal |
| `trading-lab/research/leaderboard.py`, `tests/test_leaderboard.py` | The leaderboard (`uv run -m research.leaderboard`, about a minute) and its tests |
| `trading-lab/research/leaderboard.md` | The board as it was in the lesson (7 runs, none passing all 8 rules). Yours is rebuilt from your own audit log and cards |
| `trading-lab/scripts/research_batch.sh` | The batch script with `--parallel` (one lane per family, one shared `--budget-minutes`) |
| `trading-lab/strategies/vwap_trend.py`, `strategies/specs/vwap_trend.yaml`, `tests/test_strategy_vwap_trend.py` | Idea C's strategy as the agent wrote it, with the warm-up guard added after the first judge run crashed |
| `trading-lab/research/requests/C_strategies_entry.md`, `research/patches/0002-judge-vwap-trend-strategies-entry.patch` | The agent's request and the patch for the locked judge, to read and apply yourself |
| `trading-lab/research/cards/C_vwap_trend.md` | Idea C's card with the judge's verdict (FAIL, 4 of 8) |
| `trading-lab/research/cards/h3_orb_unseen_years.md`, `backtests/h3_unseen_years.py` | The pre-registered H3 card (with the results filled in afterwards) and the script that ran it once |

Also add these lines to the Lab's `.gitignore` (Claude did in the lesson):

```text
# Leaderboard daily-return cache (research/leaderboard.py)
research/leaderboard_cache/
# Out-of-sample bars for H3, read only by backtests/h3_unseen_years.py
data/oos/
```

Claude also added entries for `research/LOOP.md`, the agents, `scripts/research_batch.sh` and the leaderboard to
`AGENTS.md`. No new dependency.

## Before you start

- The Trading Lab with the judge (Lesson 8.4), the research journal and cards (Lesson 9.1), the batch script
  (Lesson 9.3), the judge guard, the holdout, the trial ledger and the audit log (Lesson 9.4), and the commit hook
  (Lesson 3.6).
- QQQ and SPY 5-minute bars in `data/cache/` (Lesson 5.1); about 18 months after the holdout split.
- Claude Code in the terminal, signed in with your subscription, in auto mode.
- For H3 only: IB Gateway logged in to the **paper** account, and about two hours for the download.
- Time on our computer: about 9 minutes to build the factory, about 5 minutes for the run, about 1 minute for the
  review, about 8 minutes to close idea C, 2 minutes to pre-register H3, then the download, about 1 minute to move the
  old bars out and about 7 minutes for the one run.

## Try it yourself

1. `/clear`, then send request 1 in `prompts.md`. Read `research/LOOP.md` and one agent file before you trust them.
2. Edit `research/families.txt` to match your journal, then launch a short run (request 2, a smaller
   `--budget-minutes` is fine) and review it with request 3.
3. If an idea ends blocked, read its request and the patch, then apply it yourself (part 4).
4. Pick your best idea and pre-register one test on data it has never seen, before you download that data (parts 5
   and 6).

You're done when the run leaves a card for every idea, the leaderboard is rebuilt, and your test card is committed
before its data arrives. Your ideas, numbers and Claude's replies will differ from the video; the process is what
matters.

## Good to know

- Most ideas stop at the cheap check. That's the loop working: a "no" from a pandas measurement costs no judge run and
  no trial.
- The lanes share one checkout. Agents commit only their own paths, and our commit hook (which looks at the whole tree)
  may complain while another lane still has files open. Separate worktrees would be cleaner but need their own data
  cache and a ledger merge.
- An agent that writes a new strategy can't judge it: the judge is locked. Read its request, apply the entry yourself,
  then rerun the idea (`scripts/research_batch.sh --only <id>`) or ask Claude to run the judge.
- The Cost column in a run summary is Claude Code's API-price estimate for each `claude -p` session. On a subscription
  nothing is billed per run; the runs count toward your plan's usage. If a usage limit stops a run, the script exits
  with code 75; run it again later and it carries on.
- Leaderboard rows judged before the holdout split saw data that's now the holdout; the board flags them. Rows that are
  the same idea in two forms (correlation up to 0.84 here) are one piece of evidence, not two.
- An old done marker can make the batch skip an idea (H3 in the video). Delete the marker or use `--only <id>`.
- The H3 download writes into `data/cache/`, which the judge, the optimizers and the leaderboard read whole. Move the
  old bars out (`data/oos/`) before anything else runs, and check the row counts.
- A FAIL is a result. Don't tune the strategy on the years it failed on: that would turn them into a tuning set. A
  variant is a new journal row and counts as a trial.

## Safety

Paper trading only. Educational content, not financial advice. The download connects read-only to IB Gateway on the
paper account; nothing in this lesson places an order. Every strategy in the lesson failed the judge or its
out-of-sample test; nothing here is a recommendation or a promise of profit.
