# Student kit: Lesson 6.3, Metrics and reports

Module 6: The backtest engine · AI Algorithmic Trading with Claude Code and Interactive Brokers

In Lesson 6.2 we inspected trades and found one held over a half-day close. In this lesson you asked Claude to fix
it: the strategy now measures its last-entry and flatten times from each day's real NYSE close, read from the
exchange calendar, with two tests built on the day after Thanksgiving (2025-11-28, a 13:00 close). Then Claude added a
metrics module (net profit, CAGR, Sharpe, Sortino, max drawdown, profit factor, expectancy, win rate, average R,
exposure and trade count, each with one plain sentence) and a self-contained HTML report with an equity curve, a
drawdown chart, a monthly returns table and the full trade list. You opened it in the browser and read it.

## What's in this kit

| File | What it is |
|---|---|
| `prompts.md` | Both requests typed in the lesson, the commands, and the pause-and-try exercise |
| `cheat-sheet.md` | Every metric in one sentence, why Sharpe needs care, the half-day fix, the lesson's numbers |
| `trading-lab/strategies/spy_vwap_reclaim.py` | The strategy, now with `last_entry_minutes_before_close` and `flatten_minutes_before_close`, measured from the real NYSE close (`exchange_calendars`) |
| `trading-lab/strategies/specs/spy_vwap_reclaim.yaml` | The spec, with comments saying the times are measured from the real close |
| `trading-lab/tests/test_strategy_spy_vwap_reclaim.py` | The strategy tests, including the two new half-day tests |
| `trading-lab/backtests/metrics.py` | `compute_metrics(trades, equity, start_equity)` and `METRICS` (label, format and plain sentence for each number) |
| `trading-lab/tests/test_metrics.py` | Seven offline tests on hand-made equity curves and trades |
| `trading-lab/reports/spy_vwap_reclaim.py` | Builds `reports/spy_vwap_reclaim.html` from a fresh backtest |

The engine (`backtests/engine.py`) is unchanged since Lesson 6.2.

## Before you start

- The Trading Lab from **Lesson 6.2**: `backtests/engine.py`, `strategies/spy_vwap_reclaim.py` and its tests, and the
  two years of SPY 5-minute bars in the cache from **Lesson 6.1**.
- `exchange_calendars` (added to the lab in Lesson 5.1 for the quality check) and `plotly` (Lesson 5.2's chart).
- No IB connection is needed: everything in this lesson runs offline, from the cache.

## Try it yourself

1. In your `trading-lab` folder, start `claude`, `/clear`, and send the first request in `prompts.md`.
2. Check the before/after table: the overnight exit should be gone.
3. `/clear`, send the second request, and open the HTML file it gives you in your browser.

You're done when your report opens in the browser with the metric cards, both charts, the monthly table and the trade
list. Your numbers, wording and Claude's replies will differ from the video; the behaviour is what matters.

## Good to know

- `reports/*.html` is ignored by Git: the report is rebuilt from the code with `uv run -m reports.spy_vwap_reclaim`
  (about a minute). The file is about 5 MB because the Plotly chart library is embedded, so it opens offline.
- Claude checked the HTML's text but did not open it in a browser. Opening it and looking is your part of the job.
- In the lesson, Claude's comment in the spec YAML says the half-day last entry is 13:30. The code and the tests use
  12:30 (30 minutes before the 13:00 close). Comments can be wrong; tests are what prove the behaviour.

## Safety

Paper trading only. Educational content, not financial advice. The `spy_vwap_reclaim` rule is a teaching example and it
loses money in this test: no result in this lesson is a promise, a recommendation, or a strategy to trade. Nothing in
this lesson connects to a broker or places an order.
