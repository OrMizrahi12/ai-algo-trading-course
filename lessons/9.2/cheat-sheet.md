# Lesson 9.2 cheat sheet: Don't stop until: /goal

## The words

| Word | Meaning |
|---|---|
| **Goal condition** | The sentence you give `/goal`. It is checked after every turn; while it isn't met, Claude keeps working |
| **Measurable** | Provable from evidence (the judge's PASS/FAIL lines, a file, the git log), not from anyone's opinion |
| **Budget** | The most attempts or turns a goal may use, so it always ends ("Stop after 30 turns"; "at most 5 scorecard runs") |
| **Judge** | `judge/scorecard.py` with the 8 rules in `judge/standards.yaml` (Lesson 8.4). The only one who decides PASS or FAIL |
| **Never-change list** | What the goal may not touch: the judge's rules, the engine and costs, sizing, the data, the entry logic, the grid of values, and the settings after seeing a result |
| **Trial count** | How many settings were tried in all (`--trials`). The Deflated Sharpe rule gets stricter as it grows; never lower it |

## A vague wish vs. a measurable goal

| | "Find me a profitable strategy" | The H2 goal file |
|---|---|---|
| Who decides? | Nobody says | `uv run -m judge.scorecard` alone: the printed PASS/FAIL lines and the exit code |
| What counts as done? | Whenever it feels done | PASS: one hold length passes all 8 rules and a neighbouring value passes rule 2. FAIL: all attempts used, or all three values fail rule 2 or rule 3. A failure is a valid finish |
| Budget? | None | 5 judge runs, fixed up front: baseline, 6/12/24 bars, optional SPY |
| What must be recorded? | Nothing | After each attempt: command, settings, trial count, all 8 rules, trade count, one sentence, a commit |
| What may never change? | Anything | The judge, engine, costs, sizing, data, entry logic, the grid, the settings after a result |

## How /goal works

1. `/goal <condition>`: Claude Code answers "Goal set", and the status line shows `/goal active`.
2. Claude works. After every turn, a separate, smaller model checks the condition against the conversation. Not met:
   Claude starts another turn without waiting for you. Met: the goal clears itself.
3. The checker doesn't read files or run commands, so write a condition that Claude's own output can prove (the judge's
   printed lines, a `git status`, a file it shows).
4. Put the budget inside the condition ("Stop after 30 turns"), so the goal always ends.
5. `/goal` alone shows the goal (state, running time, the condition); `/goal clear` closes it; Esc dismisses the panel.
6. The check waits while background work (shells, subagents) is still running. In the lesson, "2 shells still running"
   is the likely reason the goal stayed active after Claude finished.

## H2 through the goal (QQQ 5-minute bars, 15-minute range, 2024-10-21 to 2026-10-21)

| Attempt | Exit | Trials | Sharpe after costs | Rule 3 (walk-forward) | Net profit | Rules passed |
|---|---|---|---|---|---|---|
| 0 | 1R target (baseline) | 326 | 1.77 | 0.41 FAIL | $24,671 | 6 of 8 |
| 1 | 6-bar hold | 329 | 1.12 | 0.41 FAIL | $9,258 | 6 of 8 |
| 2 | 12-bar hold | 329 | 1.29 | 0.41 FAIL | $13,413 | 6 of 8 |
| 3 | 24-bar hold | 329 | 0.88 | 0.41 FAIL | $10,453 | 5 of 8 |

- **Verdict: FAIL.** All three time exits fail rule 3, a stated FAIL condition. Attempt 4 (SPY) was optional and skipped.
- The time exit is worse than the 1R target on Sharpe, net profit and Deflated Sharpe.
- Rule 3 can't separate the runs: the walk-forward tunes `max_hold_bars` itself and ignores the command-line value.
  Holding a setting fixed during walk-forward would be a rule change; it needs a decision, not a quiet edit.
- Next step on the card: stop H2. Other hold lengths on the same data would be fishing.

## Before you close a goal

The indicator can still say "active" after the work is done. Check the condition item by item against evidence:

| Condition | Evidence Claude used |
|---|---|
| Card records attempts 0 to 3 | The card has a section per attempt, each with its exact command |
| All 8 rules for each attempt | 32 rule lines = 4 attempts x 8 |
| Journal row says PASS or FAIL | Row reads "FAIL (2026-10-22)" |
| Never-change list untouched | `git diff 0247c5e HEAD` shows no changes to `judge/standards.yaml`, `backtests/` or `data/` |
| Trial counts | 326 for attempt 0, 329 for attempts 1 to 3 |
| Committed and pushed | Clean working tree; `main` and `origin/main` at the same commit |

Report deviations honestly (here: attempts 1 to 3 were committed together, not one by one), then `/goal clear`.
