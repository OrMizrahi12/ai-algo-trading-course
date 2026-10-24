# Lesson 6.2 prompts and commands

Everything typed in the lesson, in order. Lines that start with `!` run in the terminal from inside Claude Code
(shell mode). Lines that start with `/` are Claude Code commands.

## 1. Ask for a plan

```text
/clear
```

Press **Shift+Tab** until the footer says `plan mode on`. In plan mode Claude reads and plans, but changes nothing.

```text
Build an event-driven backtest engine in backtests/engine.py that runs any strategy written to our Strategy interface, bar by bar. Rules: fill entries at the next bar's open; check stops and targets inside each bar; if one bar touches both, assume the stop; if price gaps through the stop, fill at the open. Model commission, spread and slippage, and size each trade so a stop-out costs 1% of equity. Add tests for those rules, then run spy_vwap_reclaim on our two years of SPY bars and summarize the results.
```

Read the plan from the top before you approve it. In the lesson the answer was **1. Yes, and use auto mode**.

## 2. Run it yourself

All offline, from the cache:

```text
! uv run pytest tests/test_engine.py -q
! uv run pytest -q
! uv run -m backtests.engine
```

The last one runs `spy_vwap_reclaim` on SPY 5-minute bars with $100,000 and 1% risk per trade, and prints the stats and
the first five trades. It takes under a minute.

## 3. Straight to main

In the lesson, the Stop hook asked for a commit and Claude put it on a new branch. In a solo lab we want `main`:

```text
Merge backtests-engine into main, push, and delete the branch. Then add a line to CLAUDE.md so you remember it in every session: in this solo lab, always commit straight to main.
```

## 4. One trade, bar by bar

In the same session:

```text
Show me one real winning trade and one real losing trade from that run, bar by bar: the signal bar, the entry fill, the stop and the target, each bar's high and low while the trade was open, and where and why it exited, with the costs. Keep it short.
```

## Pause and try

1. Plan the engine in plan mode with the first request, read the plan, and approve it.
2. Run the tests and the engine.
3. Trace one winning and one losing trade with the last request.

You're done when your tests pass, your engine prints its results, and you can follow one trade from signal to exit,
bar by bar. Your numbers will differ from the video, and that's fine.

## Try next (optional)

- Change one cost in `CostModel` (for example 2¢ of slippage) and run the engine again: how much of the result is costs?
- Ask Claude to trace the −5.2R half-day trade of 2025-11-28 bar by bar, and explain why it was held overnight.
