# Student kit: Lesson 7.4, Opening range and VWAP

Module 7: Day-trading strategies · AI Algorithmic Trading with Claude Code and Interactive Brokers

The opening range breakout (ORB) is one of the best-known day-trading setups, with famous published numbers behind it.
In this lesson you had Claude research what published and independent tests say, then send it back to read the two
papers themselves: Claude corrected its own first summary (leverage, short selling, almost no costs, and a weak base
result behind the "stocks in play" headline). Then you had Claude add an `opening_range_breakout` strategy to the
Trading Lab, with a spec, tests and a VWAP variant, and backtest it eight ways on QQQ and SPY with our usual costs, long
only and no leverage. The best row (QQQ, 15-minute range) made +$15,263 in two years, the VWAP filter changed nothing,
and when asked whether that row is safe to trade, Claude said no, and listed what it would check first.

## What's in this kit

| File | What it is |
|---|---|
| `prompts.md` | The four requests typed in the lesson, the commands, and the pause-and-try exercise |
| `cheat-sheet.md` | The ORB rules, our 8-row results table, the papers' rules side by side, why our numbers differ, and the checklist |
| `trading-lab/strategies/opening_range_breakout.py` | The opening range breakout strategy (5 or 15-minute range, optional above-VWAP filter), written from its spec |
| `trading-lab/strategies/specs/opening_range_breakout.yaml` | Its spec, with every assumption Claude added in the notes |
| `trading-lab/tests/test_strategy_opening_range_breakout.py` | Offline tests on tiny hand-made bar sequences (20 tests) |
| `trading-lab/backtests/orb_comparison.py` | 2 symbols x 2 range lengths x 2 variants = 8 backtests, printed as one table |

The engine (`backtests/engine.py`), the metrics and the indicators are unchanged since Lesson 7.2. The lesson also added
the new files to the layout section of `AGENTS.md`.

## Before you start

- The Trading Lab as of **Lesson 7.2** (nothing from Lesson 7.3's gap scanner is needed here): the engine with its `CostModel`, the session clock, `indicators.py` (with VWAP)
  and the existing strategies, which Claude reads first to copy the house style.
- Two years of SPY and QQQ 5-minute bars in the cache (`data/cache/SPY_5min.parquet` and `QQQ_5min.parquet`).
- No IB connection is needed. The research requests use Claude's web search and fetch tools.

## Try it yourself

1. In your `trading-lab` folder, start `claude`, `/clear`, and send the research request in `prompts.md`. Then send the
   follow-up that makes Claude read the papers themselves, and compare the two answers.
2. `/clear`, send the build request, and read the results table before Claude's explanation. Which rows are identical,
   and why?
3. Ask whether the best row is safe to trade, and read the checklist.

You're done when your strategy passes its tests, your table has all eight rows, and you can give two reasons why the
best row isn't a winner yet. Your numbers, wording and Claude's replies will differ from the video; the behaviour is
what matters.

## Good to know

- Published results are claims under their authors' assumptions: up to 4x leverage, long and short, almost no costs,
  and (in 2024) a daily pick of "stocks in play". Our engine charges spread and slippage, never uses leverage, and our
  strategies are long only, so the numbers are not comparable one to one.
- The replications Claude found are GitHub repos and blogs, not peer reviewed, and it read only their summaries.
- The comparison takes a few minutes (`uv run -m backtests.orb_comparison`).
- The best of eight backtests is not a winner. Module 8 covers the checks: other parameters, higher costs, concentration,
  confidence intervals, out-of-sample data and a benchmark.

## Safety

Paper trading only. Educational content, not financial advice. The opening range breakout here is a teaching example: no
result in this lesson is a promise, a recommendation, or a strategy to trade. Nothing in this lesson connects to a broker
or places an order.
