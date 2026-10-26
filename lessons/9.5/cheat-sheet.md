# Lesson 9.5 cheat sheet: The factory at scale

## The words

| Word | Meaning |
|---|---|
| **Strategy family** | Strategies that share one idea about the market. In the Lab: breakout and momentum (price leaves a range and keeps going), mean reversion (price stretches away from normal and snaps back), time of day (the clock is the signal) |
| **Subagent** | A separate Claude worker with its own instructions and its own context. Here: a file in `.claude/agents/`, started by the batch script with `claude -p --agent <name>` |
| **Lane** | One family's queue of ideas in a `--parallel` run. Lanes run side by side under one shared time budget |
| **Budget** | Where an agent must stop: the turn limit, 8 judge runs, 1 new strategy, or the idea's own stop condition, whichever comes first |
| **Cheap check** | A quick pandas measurement on the research cache before any strategy is written. If the number says there is nothing there, the idea stops with a card, and no trial is spent |
| **Correlated strategies** | Two strategies whose daily returns rise and fall on the same days. Correlation 1 = they move together every day, 0 = unrelated. Keeping both doubles the risk, not the edge |
| **Leaderboard** | `research/leaderboard.md`: every run the judge has scored, ranked by rules passed, then Deflated Sharpe, then Sharpe, without exact duplicates and without runs correlated above 0.7 with a better one |
| **Pre-registration** | Writing the settings, the test and the PASS / FAIL rules down, and committing them, before the data exists. Then the result can't be argued with |
| **Out-of-sample** | Data the settings were never picked on. Here: 2019-10 to 2024-09, five years older than the research cache |

## The factory, file by file

| File | What it does |
|---|---|
| `research/LOOP.md` | The one procedure every researcher follows: pick the idea, pre-register the card, cheap check first, spec, code with tests, the judge, the card (with the whole scorecard pasted), the journal row, a commit by explicit path. Plus the budget, the locked files, the shared-checkout git rules and the lessons from earlier ideas |
| `.claude/agents/researcher-breakout-momentum.md`, `researcher-mean-reversion.md`, `researcher-time-of-day.md` | One agent per family: what that family's ideas look like, its traps, its stop condition. Each one says "read `research/LOOP.md` and follow it exactly" |
| `research/families.txt` | Which journal idea belongs to which family (`H3 breakout-momentum`, `G mean-reversion`, `A time-of-day` ...). An idea without a line is skipped by `--parallel` |
| `research/leaderboard.py` | Reads the audit log and the scorecards pasted into the cards, drops duplicates, ranks, rebuilds each run's daily returns once on the research cache, and drops look-alikes (`--threshold`, default 0.7) |
| `scripts/research_batch.sh --parallel` | One lane per family, one shared `--budget-minutes`, `--max-turns` per idea, `--dry-run` to see the plan, `--only <id>` to run one idea. It commits the ledger files between ideas (the agents can't) and rebuilds the leaderboard at the end. Exit code 75 = a usage limit stopped it; rerun later and it carries on |

## Locks that still apply (Lesson 9.4)

- Agents can't edit the judge, so they can't register a new strategy. They leave the exact `STRATEGIES` entry in
  `research/requests/<id>_strategies_entry.md` and mark the idea `blocked: needs STRATEGIES entry`. You add it, by hand
  or by applying a patch you've read.
- Agents can't `git add` `research/trials.csv` or `research/audit_log.jsonl`. The batch script commits them; outside a
  batch, you do.
- The holdout stays locked: the guard even blocked an `ls` of `data/holdout/` in this lesson.

## Reading a factory run

1. **Count the trials.** A run that never reached the judge added none. Cheap "no"s are free.
2. **Read every card**, not just the leaderboard. The reasons matter: no effect, loses before costs, too few trades,
   a diagnostic only, blocked.
3. **Distrust the top of the board.** Ask what data it was judged on (here: data that's now the holdout), whether rows
   are the same idea in two forms (correlation 0.77 to 0.84), and how short the sample is (18 months).
4. **Check what broke**: shared checkout, stale lock files, a wrong title, and limits of the engine (long only, 200 bars).
5. **Decide the next test**, not a trade. Paper trading is a test, not an endorsement.

## A pre-registered test, step by step

1. Card first: the question, the frozen settings, the span, the symbols, what gets reported, the PASS / PARTIAL / FAIL
   rules and your own expectation. Commit it. "Results" stays empty.
2. Download the data only after that commit.
3. Keep the new data out of everything else (here: moved to `data/oos/`, gitignored, with proof that the research cache
   is unchanged).
4. Write the script exactly as the card says and commit it before its first run.
5. Run it once. No reruns, no tweaks. Fill in the results and give the verdict by the rules.

## The numbers in the video

| What | Result |
|---|---|
| Factory run | 6 ideas, about 5 minutes, 0 judge runs, 0 trials added |
| Leaderboard | 7 runs, none passes all 8 rules; best: opening range breakout QQQ 15 min / 1R, 6 of 8, Sharpe 1.77 (judged on data that includes the holdout) |
| Idea C (VWAP trend) | FAIL, 4 of 8: 995 trades, Sharpe 0.29, costs take 72% of the profit, loses at 2x costs |
| H3 (QQQ 2019-10 to 2024-09) | FAIL: 901 trades, net -$155, Sharpe 0.03, Monte Carlo 5th-percentile drawdown -31.0%, 3 of 6 years up; SPY Sharpe -0.03; with zero costs about 0.35 |

Your numbers will differ. None of this is a strategy to trade.
