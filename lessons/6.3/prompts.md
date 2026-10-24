# Lesson 6.3 prompts and commands

Everything typed in the lesson, in order. Lines that start with `!` run in the terminal from inside Claude Code
(shell mode). Lines that start with `/` are Claude Code commands. Both requests run in auto mode. Nothing here needs
an IB connection.

## 1. Fix the half-day close

```text
/clear
```

```text
Last time we found a trade held over a half-day close. Fix the strategy so its last-entry and flatten times are measured from the real NYSE close of each day, using the exchange calendar, add a test with the day after Thanksgiving, re-run the backtest and show me before and after.
```

Claude runs the current backtest first and saves it as the "before", finds the trade (entered 12:55 New York time on
2025-11-28, sold at Monday's open), changes the strategy, adds two tests for that day and re-runs. Check its work
yourself any time:

```text
! uv run pytest -q
! uv run -m backtests.engine
```

A good habit from the lesson: a new test should fail on the old code and pass on the new one. A test that passes
either way proves nothing.

## 2. Metrics and an HTML report

```text
/clear
```

```text
Add backtests/metrics.py with net profit, CAGR, Sharpe and Sortino from daily returns, max drawdown, profit factor, expectancy, win rate, average R, exposure and trade count, each explained in one plain sentence. Then make an HTML report for the spy_vwap_reclaim run: the metrics at the top, an equity curve, a drawdown chart, a monthly returns table and the trade list. Save it as reports/spy_vwap_reclaim.html and give me the path.
```

Rebuild the report and run the metric tests yourself:

```text
! uv run pytest tests/test_metrics.py -q
! uv run -m reports.spy_vwap_reclaim
```

## 3. Open the report

Open Chrome (or any browser), open a new tab, and paste the full path Claude gave you, for example
`file:///home/<your user>/trading-lab/reports/spy_vwap_reclaim.html` (on Windows the path starts with a drive letter,
such as `file:///C:/Users/<you>/trading-lab/reports/spy_vwap_reclaim.html`). Zoom in with Ctrl and + if the text is
small. Hover over the equity curve and the drawdown chart to see the date and value of any point.

## Pause and try

1. Fix the half-day close with the first request, and read the before/after table.
2. Build the metrics and the report with the second request, and open the report in your browser.

You're done when your report opens with the metric cards, both charts, the monthly table and the trade list. Your
numbers will differ from the video, and that's fine.

## Try next (optional)

- Ask Claude to add a second report for the vectorized EMA rule from Lesson 6.1, using the same `compute_metrics`.
- Sort the trade list by R and look at the worst five trades. Do any of them look like another bug?
