# Student kit: Lesson 9.2, Don't stop until: /goal

Module 9: The strategy factory: goal-driven research loops · AI Algorithmic Trading with Claude Code and Interactive Brokers

"Find me a profitable strategy" sounds like a goal, but nothing can check it. In this lesson Claude turns a vague wish
into a measurable goal for journal idea H2 (replace the opening range breakout's 1R profit target with a time-based
exit): who decides (the judge alone), what counts as done (a PASS or a FAIL, defined in advance), the budget (five judge
runs, fixed up front), what to record after each attempt, and a never-change list. It saves the goal to
`research/goals/h2_exit.md` and commits it. Then `/goal` runs it unattended: Claude adds the optional `max_hold_bars`
setting with tests, runs the baseline and three time exits through the judge, and stops with a clean FAIL. The goal
indicator stays active, so we ask Claude to check the condition item by item against the files and the git log, and
then close the goal ourselves with `/goal clear`.

## What's in this kit

| File | What it is |
|---|---|
| `prompts.md` | The request, the `/goal` command and the check typed in the lesson, the commands to reproduce the runs, and the pause-and-try exercise |
| `cheat-sheet.md` | The words, the four parts of a measurable goal, how `/goal` works, H2's results, and the check before you close a goal |
| `trading-lab/research/goals/h2_exit.md` | The goal file Claude wrote: the question, who decides, the allowed changes, the attempts fixed in advance, what "done" means (PASS or FAIL), what to record after every attempt, and the never-change list |
| `trading-lab/research/cards/h2_time_exit_orb.md` | The strategy card for H2: how the judge treats the new setting, all four scorecards verbatim with their exact commands, the verdict (FAIL), the plain reading, the next step and notes |
| `trading-lab/research/journal.md` | The research journal from Lesson 9.1 with the H2 row filled in (FAIL), the suggested order and a new log line |
| `trading-lab/strategies/opening_range_breakout.py` | The breakout strategy with the new optional `max_hold_bars` (a time exit; `None` by default, so old runs are unchanged) |
| `trading-lab/tests/test_strategy_opening_range_breakout.py` | The breakout's tests, with the new time-exit tests (it fires at `max_hold_bars` and never by default; a run without it is identical to the old one; a 6-bar hold sells 30 minutes after the entry fill) |
| `trading-lab/judge/scorecard.py` | The judge from Lesson 8.4 with `max_hold_bars` added to the breakout's entry in `STRATEGIES` (settings and ranges only, no rule logic) |

Nothing else in the Lab changed; no new dependency.

## Before you start

- The Trading Lab with the opening range breakout (Lesson 7.4), the judge `judge/scorecard.py` with
  `judge/standards.yaml` (Lesson 8.4), and the research journal `research/journal.md` (Lesson 9.1).
- Two years of QQQ 5-minute bars in the cache (`data/cache/`). No IB connection is needed.
- A Claude Code version that has the `/goal` command (type `/goal` and look for "Set a goal Claude checks before
  stopping" in the menu).
- Time: writing the goal took about 30 seconds on our computer; the `/goal` run took about 7 minutes, most of it four
  judge runs of about 75 to 80 seconds each.

## Try it yourself

1. In your `trading-lab` folder, start `claude`, `/clear`, and send the goal-writing request in `prompts.md`. Read the
   goal file before you run it: does it name the judge, the definition of done, the budget and the never-change list?
2. `/clear`, and run `/goal` with a condition that points at your goal file and ends with a turn budget.
3. When Claude stops, look at the status line. If the goal still shows as active, ask Claude to check the condition
   item by item against the files and the git log, then close it with `/goal clear`.

You're done when your goal file names the judge, the definition of done, the budget and the never-change list, and your
card and journal row show a verdict. Pass or fail, both count. Your numbers, wording and Claude's replies will differ
from the video; the behaviour is what matters.

## Good to know

- The budget is part of the condition ("Stop after 30 turns"), and the attempts are fixed in the goal file before any
  run. A goal without a budget can run until your usage runs out.
- The trial count for the time exits is 329: the 326 breakout runs the Lab had already tried (from
  `reports/luck_vs_skill.py`) plus the 3 new settings. Rule 7 (the Deflated Sharpe) gets stricter the more settings were
  tried, so a smaller number would make passing too easy.
- Rule 3 (walk-forward) came out at 0.41 in all four runs, the baseline included. Adding `max_hold_bars` to the
  judge's `STRATEGIES` entry lets the walk-forward tune it itself, so rule 3 could not tell the runs apart. Letting the
  judge hold a setting fixed would be a rule change; Claude flagged it for a decision instead of making it. Even so, on
  Sharpe after costs every time exit (1.12, 1.29, 0.88) lost to the 1R target (1.77).
- When Claude finished, the `/goal` indicator still showed "active" (likely because two background shells were still
  running: the check waits for background work). Claude checked the condition from the files and the
  git log (not from its own summary), reported one process deviation (attempts 1 to 3 were committed together, not
  one by one), and we closed the goal with `/goal clear`.

## Safety

Paper trading only. Educational content, not financial advice. H2 failed the judge, and no result here is a
recommendation or a promise of profit. Nothing in this lesson connects to a broker or places an order.
