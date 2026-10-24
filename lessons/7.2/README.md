# Student kit: Lesson 7.2, Intraday mean reversion

Module 7: Day-trading strategies · AI Algorithmic Trading with Claude Code and Interactive Brokers

Lesson 7.1 bet that an intraday move keeps going. This lesson makes the opposite bet: mean reversion buys a price that
has stretched far below its normal level inside the session, and expects it to snap back. You had Claude add two
reversion strategies to the Trading Lab, each with a spec and tests: `bollinger_rsi_reversion` (a close below the lower
20-bar Bollinger band with a 2-bar RSI under 10, exit at the middle band) and `vwap_stretch_reversion` (a close more
than 2 ATR below VWAP, exit back at VWAP). Both are long only, with a 2 ATR stop, flat before the close. Claude
backtested them on SPY and QQQ at zero, usual and double costs: 11 of the 12 runs lose money, and the only positive
one (Bollinger on QQQ) needs zero costs. Then you asked when mean reversion stops working, and split the trades by day
type: all four strategy and symbol combinations lose on trend days and win on the other days, with the honest catch
that trend days were picked with hindsight.

## What's in this kit

| File | What it is |
|---|---|
| `prompts.md` | The two requests typed in the lesson, Claude's one question, the commands, and the pause-and-try exercise |
| `cheat-sheet.md` | The three indicators in one line each, the full cost table, the day-type table, and Claude's caveats |
| `trading-lab/strategies/bollinger_rsi_reversion.py` | The Bollinger + 2-bar RSI reversion strategy, written from its spec |
| `trading-lab/strategies/vwap_stretch_reversion.py` | The VWAP stretch reversion strategy, written from its spec |
| `trading-lab/strategies/specs/bollinger_rsi_reversion.yaml` | Its spec, with every assumption Claude added in the notes |
| `trading-lab/strategies/specs/vwap_stretch_reversion.yaml` | Its spec, with every assumption Claude added in the notes |
| `trading-lab/tests/test_strategy_bollinger_rsi_reversion.py` | Offline tests on tiny hand-made bar sequences (10 tests) |
| `trading-lab/tests/test_strategy_vwap_stretch_reversion.py` | Offline tests on tiny hand-made bar sequences (10 tests) |
| `trading-lab/backtests/reversion_comparison.py` | 2 strategies x 2 symbols x 3 cost levels = 12 backtests, printed as one table |
| `trading-lab/reports/reversion_by_day_type.py` | Splits every trade by day type (trend days vs other days) and writes a three-panel chart |

The engine (`backtests/engine.py`), the metrics and the indicators are unchanged since Lesson 7.1. The lesson also added
the new files to the layout section of `AGENTS.md`.

## Before you start

- The Trading Lab from **Lesson 7.1**: the engine with its `CostModel`, the session clock, `indicators.py` (Bollinger,
  RSI, ATR, VWAP) and the existing trend strategies, which Claude reads first to copy the house style.
- Two years of SPY and QQQ 5-minute bars in the cache (`data/cache/SPY_5min.parquet` and `QQQ_5min.parquet`).
- No IB connection is needed: everything in this lesson runs offline, from the cache.

## Try it yourself

1. In your `trading-lab` folder, start `claude`, `/clear`, and send the first request in `prompts.md`. Claude asks
   about the exits before it builds; pick the option you understand, and write down why.
2. Read the cost table before Claude's reading of it. Which rows change between zero, usual and double costs, and which
   numbers stay the same?
3. `/clear`, send the second request, and look at the chart: red bars are trend days, blue bars every other day.

You're done when both strategies pass their tests, your table has all three cost levels, and you can say in one
sentence why the trend-day split is hindsight. Your numbers, wording and Claude's replies will differ from the video;
the behaviour is what matters.

## Good to know

- Mean reversion makes many small trades (about 650 to 740 in two years per strategy and symbol here), so the spread,
  commission and slippage are paid on every one of them. That is why the cost levels move the results so much.
- The comparison run takes several minutes (`uv run -m backtests.reversion_comparison`); the day-type report takes a
  few minutes too (`uv run -m reports.reversion_by_day_type`). The chart is written to `reports/` and is gitignored.
- A trend day here is one of the third of sessions with the biggest move from the open to the close. You only know
  that after the close, so the split shows where the edge goes, not a filter you could trade. A usable filter needs
  information you have early in the day.

## Safety

Paper trading only. Educational content, not financial advice. Both strategies are teaching examples and both lose money
after costs in this test: no result in this lesson is a promise, a recommendation, or a strategy to trade. Nothing in
this lesson connects to a broker or places an order.
