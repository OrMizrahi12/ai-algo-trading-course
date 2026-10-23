# Lesson 5.3 prompts and commands

Everything typed in the lesson, in order. Lines that start with `!` run in the terminal from inside Claude Code
(shell mode). Lines that start with `/` are Claude Code commands.

## 1. From idea to spec

```text
/clear
```

```text
I have a strategy idea in plain English: on SPY 5-minute bars, after the first 15 minutes, buy when the close crosses back above VWAP while the 20-bar EMA is above VWAP. Put the stop under the recent swing low or 1.5 ATR, take profit at 2R, and be flat before the close. Turn it into a strategy spec. First write strategies/specs/TEMPLATE.yaml that covers market, timeframe, session, entry, exit, stop (fixed, ATR, trailing, time), take profit, sizing and filters, with a short comment on every field. Then fill strategies/specs/spy_vwap_reclaim.yaml. Before you write it, ask me about anything ambiguous and give me options.
```

Claude answers with a question picker (one tab per question; Enter selects, Tab or the arrow keys move between
tabs, then a review screen and **Submit answers**). The answers chosen in the video:

| Question | Answer chosen |
|---|---|
| Cross rule: what counts as the close crossing back above VWAP? | 1. Prior bar below, this bar above (Recommended) |
| Stop rule: how should the stop combine the swing low and 1.5 ATR? | 3. Swing low, capped at 1.5 ATR |
| Entry fill: at what price do we assume the buy fills? | 1. Next bar's open (Recommended) |
| Flat and limits: when must we be flat, how many trades per day? | 1. Exit at 15:55 ET bar, max 1 trade/day (Recommended) |

Your questions may be worded differently, or there may be more or fewer of them. Answer what you really mean.

Open the spec in VS Code:

```text
! code -g strategies/specs/spy_vwap_reclaim.yaml
```

## 2. One interface, coded from the spec (plan mode)

```text
/clear
```

Then press **Shift+Tab** until the footer says **plan mode on**.

```text
Design one Strategy interface that our backtester (module 6) and the live paper trader (later) will both use, so a strategy is written once. Then implement spy_vwap_reclaim from its spec, and tests with small hand-made bar sequences: an entry, the stop, the target, the time exit, and the filter that blocks the first 15 minutes. No backtester yet.
```

Read the plan, then choose **1. Yes, and use auto mode**.

## 3. Keep everything on main

In the video Claude committed on a new branch. For a solo lab:

```text
This is a solo lab, so keep everything on main: merge strategy-interface into main, push, delete the branch, and show me the test results once more.
```

Open the interface in VS Code:

```text
! code -g strategies/base.py
```

Run the tests yourself at any time:

```text
! uv run pytest
```

## Pause and try

Write a spec for an idea of your own (it can be completely different: another ETF or stock, another entry, another
stop). Use request 1 with your idea in place of ours, and let Claude interview you before it writes the file. Then, in plan
mode, ask Claude to implement your spec behind the existing `Strategy` interface in `strategies/base.py` (the
interface is already there, so it should not design a new one), with tests on small hand-made bar sequences.

You're done when every rule in your spec is a number or a time, every guess is marked as an assumption, and your
tests pass.
