# Lesson 9.2 prompts and commands

Everything typed in the lesson, in order. Lines that start with `!` run in the terminal from inside Claude Code
(shell mode). Lines that start with `/` are Claude Code commands. Every request runs in auto mode. Nothing here needs an
IB connection: the backtests use the cached bars.

## 1. Write a measurable goal

```text
/clear
```

```text
I want to use /goal for research, and 'find me a profitable strategy' is too vague. Help me write a measurable goal for journal idea H2, a time-based exit for the opening range breakout on QQQ. Who decides pass or fail, what counts as done, the most attempts allowed, what you must record after each attempt, and what you are never allowed to change. Keep it short enough to paste into /goal, save it to research/goals/h2_exit.md and commit.
```

In the video, Claude read the H2 row of the journal and the judge setup, wrote `research/goals/h2_exit.md` (about 30
lines) and committed it straight to `main`. About 30 seconds.

## 2. Run the goal

```text
/clear
```

```text
/goal Follow research/goals/h2_exit.md exactly. Done when research/cards/h2_time_exit_orb.md records attempts 0 to 3 (4 is optional) with all 8 judge rules each, the H2 row in research/journal.md says PASS or FAIL as that file defines it, nothing on its never-change list was changed, and everything is committed and pushed. Stop after 30 turns.
```

Claude Code answers "Goal set", and the status line shows `/goal active` with a running time. In the video, Claude
added the optional `max_hold_bars` setting with tests (183 pass), ran attempt 0 (the 1R baseline) and attempts 1 to 3
(holds of 6, 12 and 24 bars) through the judge, found the goal file's FAIL condition met, skipped the optional
attempt 4, wrote the card and the journal row, and pushed. About 7 minutes, with no input.

Reproduce the four runs yourself (about 80 seconds each):

```text
! uv run -m judge.scorecard opening_range_breakout --symbol QQQ --set range_minutes=15 --set target_r=1.0 --trials 326
! uv run -m judge.scorecard opening_range_breakout --symbol QQQ --set range_minutes=15 --set max_hold_bars=6 --trials 329
! uv run -m judge.scorecard opening_range_breakout --symbol QQQ --set range_minutes=15 --set max_hold_bars=12 --trials 329
! uv run -m judge.scorecard opening_range_breakout --symbol QQQ --set range_minutes=15 --set max_hold_bars=24 --trials 329
```

And the tests:

```text
! uv run pytest -q
```

## 3. Check the goal, then close it

See the goal's state:

```text
/goal
```

In the video it still showed "Goal active, running 9m" after Claude had finished, so we pressed Esc and asked for
evidence:

```text
The goal is still active. Check its condition item by item against the files and the git log, and tell me whether it is met.
```

Claude answered with a table (condition, evidence, met), one process deviation, and "I checked this from the files and
git log, not from my earlier summary". Then we closed the goal:

```text
/goal clear
```

## Pause and try

1. Pick one untested idea from your own `research/journal.md`. Ask Claude to write a measurable goal for it, like
   request 1: who decides, what counts as done, the most attempts, what to record, and what may never change.
2. Read the goal file before you run it. Is "done" something a program can check? Is there a budget?
3. Run it with `/goal`, ending the condition with a turn budget. When Claude stops, check the condition against the
   files and the git log yourself (or ask Claude to), then `/goal clear`.

You're done when your goal file names the judge, the definition of done, the budget and the never-change list, and your
card and journal row show a verdict. Pass or fail, both count. Your numbers will differ from the video, and that's fine.
This is paper research, not a strategy to trade.

## Try next (optional)

- Write a goal whose condition you can check with one command (for example the judge's exit code), and compare how
  quickly Claude can tell it is done.
- Make the budget smaller (fewer attempts, fewer turns) and see how Claude plans around it.
- Read the H2 card's section "How the judge treats the new setting". Write down what you would decide about holding a
  setting fixed during walk-forward, and why. Don't change the judge yet.
