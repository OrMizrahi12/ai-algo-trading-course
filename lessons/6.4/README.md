# Student kit: Lesson 6.4, Trust, but verify the engine

Module 6: The backtest engine · AI Algorithmic Trading with Claude Code and Interactive Brokers

In Lessons 6.2 and 6.3 the engine said `spy_vwap_reclaim` lost 2.54% over two years. In this lesson you checked that
the engine's arithmetic can be trusted, twice. First with a known-answer test: twelve hand-made SPY bars and two trades,
every fill, cost and share count worked out by hand before the engine ran, down to a final equity of $100,256.00.
Then with a cross-check: the same strategy, rewritten from its spec, run in an independent library (backtesting.py
0.6.6) on the same 38,976 bars, compared trade by trade until all 252 trades matched to the cent, with every difference
explained. Last, you asked for a map of the mature engines and when you would outgrow your own.

## What's in this kit

| File | What it is |
|---|---|
| `prompts.md` | The three requests typed in the lesson, the commands, and the pause-and-try exercise |
| `cheat-sheet.md` | The hand-worked table, the cross-check results, every difference and its cause, and the map of engines |
| `trading-lab/tests/test_engine_known_answer.py` | The known-answer test: 12 bars, two trades, the hand calculation in its docstring, three tests |
| `trading-lab/backtests/crosscheck_backtestingpy.py` | The cross-check: the strategy rewritten from its YAML spec with TA-Lib indicators, run in backtesting.py with zero costs and with costs, compared with our engine |

The engine (`backtests/engine.py`) and the strategy are unchanged since Lesson 6.3. The lesson also added
`backtesting` as a development dependency (`uv add --dev backtesting`, one line in `pyproject.toml` plus `uv.lock`).

## Before you start

- The Trading Lab from **Lesson 6.3**: `backtests/engine.py`, `strategies/spy_vwap_reclaim.py` and its spec, and the
  two years of SPY 5-minute bars in the cache from **Lesson 6.1**.
- TA-Lib for Python (`ta-lib`, already in the lab's development dependencies).
- No IB connection is needed: everything in this lesson runs offline, from the cache. The third request uses the web.

## Try it yourself

1. In your `trading-lab` folder, start `claude`, `/clear`, and send the first request in `prompts.md`. Before you read
   Claude's table, try trade 1 yourself with the numbers in `cheat-sheet.md`.
2. `/clear`, send the second request, and read Claude's list of differences. Each one should have a cause.
3. `/clear`, send the third request, and open the official links it gives you.

You're done when your known-answer test passes, and your cross-check matches trade for trade, or every difference has a
reason. Your numbers, wording and Claude's replies will differ from the video; the behaviour is what matters.

## Good to know

- A known-answer test does not say the strategy is any good. It says the engine's arithmetic is right for these bars and
  these rules, and it stays in the test suite, so a later change that breaks the arithmetic fails right away.
- The cross-check run takes a minute or two (`uv run -m backtests.crosscheck_backtestingpy`).
- Agreement is not the same as right: both engines share the 100% position cap, so the cross-check cannot tell you
  that the cap, not the 1% risk rule, sets almost every position size.
- Versions move fast. The versions in the cheat sheet were current at the time of recording (October 2026).

## Safety

Paper trading only. Educational content, not financial advice. The `spy_vwap_reclaim` rule is a teaching example and it
loses money in this test: no result in this lesson is a promise, a recommendation, or a strategy to trade. Nothing in
this lesson connects to a broker or places an order.
