# Lesson 5.2 prompts

The requests typed in the lesson, in order, ready to copy. Type them at Claude Code's prompt inside your
`trading-lab` folder. Each part starts with `/clear`, so Claude begins with a fresh session. No IB connection is
needed: everything runs on the cached SPY bars from Lesson 5.1.

## Part 1: pandas for traders

```text
/clear
```

```text
Teach me the pandas a trader needs, using our real SPY 5-minute bars from the data cache. Write notebooks/pandas_tour.py as a short, well-commented tour: load the bars, show the first rows and the columns, convert the time to New York, pick one trading day, compute bar returns, then resample to 15-minute and daily bars and prove the daily high equals the highest 5-minute high. Run it and walk me through the output.
```

To read the file in VS Code from inside Claude Code (the `!` runs a shell command):

```text
!code -n . notebooks/pandas_tour.py
```

Then, about the line that does the resampling (line 78 in the lesson's file; yours may differ):

```text
Explain line 78 of notebooks/pandas_tour.py like I am new to pandas: what resample and agg do, and why we must not just average the prices.
```

## Part 2: indicators from scratch

```text
/clear
```

```text
Now write indicators.py with SMA, EMA, RSI using Wilder's smoothing, ATR, Bollinger Bands and a VWAP that resets every session, all from scratch with pandas, no look-ahead. Then add tests that compare each one with TA-Lib on our SPY bars (VWAP has no TA-Lib version: test it by hand on a tiny example). Run the tests, show me a small table of the last values side by side, and commit.
```

To open the file in the VS Code window that's already open:

```text
!code -g indicators.py
```

## Part 3: a chart you can explore

```text
/clear
```

```text
Make an interactive candlestick chart of the latest full SPY session: 5-minute candles, the session VWAP and a 20-bar EMA, volume underneath, and a small marker wherever the close crosses above or below VWAP. Save it as reports/spy_session.html and tell me the path. These markers are just an illustration, not a strategy.
```

## Your turn (pause and try)

Pause the video and, with Claude:

1. Add one more indicator to the chart: Bollinger Bands, or RSI in its own panel.
2. Ask Claude to explain one line you don't understand yet.

You're done when the chart opens, and you can say what every line on it means.
