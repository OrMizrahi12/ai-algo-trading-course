# Student kit: Lesson 7.1, ETF breakouts and trend

Module 7: Day-trading strategies · AI Algorithmic Trading with Claude Code and Interactive Brokers

First lesson of Module 7. Before writing any strategy, you asked Claude to measure the shape of a trading day on two
years of SPY and QQQ 5-minute bars: when prices move and when volume is high. Then, in plan mode, Claude planned and
built two textbook trend strategies on the Lab's Strategy interface, each with a spec and tests: a Donchian breakout
and an EMA trend rule. It backtested both on SPY and QQQ, all day and with no midday entries: 7 of 8 runs lost money
or roughly broke even. A puzzle in the table (a profit with a negative average R) led to the engine's no-leverage
position cap; R is now measured against a fixed 1% of equity. And the only winning row turned out to rest on one
trade, on April 9, 2025.

## What's in this kit

| File | What it is |
|---|---|
| `prompts.md` | Every request typed in the lesson, the two plan-mode answers, the commands, and the pause-and-try exercise |
| `cheat-sheet.md` | The words, the time-of-day table, both strategies' rules, the eight runs, the R puzzle and the April 9 outlier |
| `trading-lab/reports/intraday_profile.py` | The time-of-day profile chart (average absolute move and volume per 5-minute slot) |
| `trading-lab/strategies/donchian_breakout.py`, `ema_trend.py` | The two strategies on the Strategy interface |
| `trading-lab/strategies/session_clock.py` | Shared helper: flatten and last-entry times from the real NYSE close, and the optional no-entry window |
| `trading-lab/strategies/specs/donchian_breakout.yaml`, `ema_trend.yaml` | Their specs, assumptions included |
| `trading-lab/tests/helpers.py`, `test_strategy_donchian_breakout.py`, `test_strategy_ema_trend.py` | Hand-made bar builders and the strategy tests |
| `trading-lab/backtests/trend_comparison.py` | Runs the 8 combinations and prints one table |
| `trading-lab/backtests/engine.py`, `backtests/metrics.py` | The engine and metrics after commit `6ca7131` (R against a fixed 1% of equity, new `stop_risk` column, cap kept) |
| `trading-lab/tests/test_engine.py`, `test_engine_known_answer.py` | Engine tests, updated for the new R, plus a capped-stop test |

## Before you start

- The Trading Lab from **Lesson 6.4**: the engine, the metrics module, the Strategy interface and `spy_vwap_reclaim`.
- Two years of SPY **and** QQQ 5-minute bars in `data/cache/` (Lesson 5.1's data pipeline).
- `plotly` for the chart and `ta-lib` (both already in the Lab). No IB connection is needed.

## Try it yourself

1. In your `trading-lab` folder, start `claude`, `/clear`, and send request 1 in `prompts.md`. Open the chart.
2. `/clear`, switch to plan mode, send request 2, answer the two questions, read the plan and approve it.
3. When the table arrives, ask how much of the best row comes from its single best trade.

You're done when you know how much of a result rests on its best trade. Your numbers, wording and Claude's replies
will differ from the video; the method is what matters.

## Good to know

- `reports/*.html` is ignored by Git: rebuild the chart with `uv run -m reports.intraday_profile`.
- The cached bars are adjusted for dividends, so their prices sit a little below the prices quoted in the news for the
  same day (for example, SPY's close on April 9, 2025 is 543.37 in the data).
- What happened on April 9, 2025 came from Claude's own recall, and Claude said so; the 5-minute bars match the timing.
  Check news facts against a source before you rely on them (see the lesson notes).
- Claude skipped the plan's hand check at first and admitted it. Asking for it found the R problem and the outlier.

## Safety

Paper trading only. Educational content, not financial advice. Both strategies are textbook teaching examples and they
lose money in this test: no result in this lesson is a promise, a recommendation, or a strategy to trade. Nothing in
this lesson connects to a broker or places an order. Leverage was deliberately left off.
