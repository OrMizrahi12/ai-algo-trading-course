# Lesson 7.2 prompts and commands

Everything typed in the lesson, in order. Lines that start with `!` run in the terminal from inside Claude Code
(shell mode). Lines that start with `/` are Claude Code commands. Both requests run in auto mode. Nothing here needs an
IB connection.

## 1. Two reversion strategies, at three cost levels

```text
/clear
```

```text
Add two intraday mean-reversion strategies on our Strategy interface, with a spec and tests each. One: buy when the close is below the lower 20-bar Bollinger band and the 2-bar RSI is under 10; exit at the middle band. Two: buy when the price is more than 2 ATR below VWAP; exit back at VWAP. Both long only, a 2 ATR stop, flat before the close. Backtest both on SPY and QQQ with zero costs, our usual costs and double costs, and give me one table. Ask me first if anything is ambiguous.
```

Claude reads the existing strategy code first, then asks one question, about the exits:

- **Signal exit (recommended)**: when a bar closes at or above the middle band (or VWAP), sell at the next bar's open as
  a market order. It uses the level as it is when the bar closes, and market sells pay slippage. This is the one we chose.
- **Fixed limit target**: at entry, set a take-profit at the middle band (or VWAP) value on the signal bar. The level is
  frozen, and it fills inside the bar at the target price with no slippage.
- **Run both**: both exit styles, which doubles the table to 24 rows.

Then it writes both strategies, their specs and tests, runs the whole test suite (131 tests in the video, 20 of them
new), runs the 12 backtests, and commits. Run them yourself any time:

```text
! uv run pytest -q
! uv run -m backtests.reversion_comparison
```

## 2. When does mean reversion stop working?

```text
/clear
```

```text
When does mean reversion stop working? Split the trades of both reversion strategies by day type: trend days, the third of days with the biggest move from open to close, versus all other days. Use our usual costs. Show results and stop-outs for each, save a chart to reports/ and open it, and explain what you find.
```

Claude writes `reports/reversion_by_day_type.py`, runs it, opens the chart in your browser, explains the table, and
commits the script. Run it yourself:

```text
! uv run -m reports.reversion_by_day_type
```

## Pause and try

1. Build both strategies with the first request, and answer Claude's question about the exits.
2. Read the cost table: which strategy is closest to break-even before costs, and what do costs do to it?
3. Split the trades by day type with the second request, and read the caveats.

You're done when both strategies pass their tests, your table has all three cost levels, and you can explain why the
trend-day split is hindsight. Your numbers will differ from the video, and that's fine.

## Try next (optional)

- Run the same comparison with the fixed limit target instead of the signal exit, and compare the cost rows.
- Ask Claude for an early-day filter that uses only what is known by 10:30 (the first hour's range, or the gap at the
  open), and test whether it keeps any of the "other days" edge. Claude suggested this and did not start it.
