# Student kit: Lesson 5.2, Python for traders, with Claude

Module 5: Data and strategy foundations · AI Algorithmic Trading with Claude Code and Interactive Brokers

In this lesson Claude wrote three pieces of Python for the Trading Lab, all on the free SPY history we cached in
Lesson 5.1, and we read every one of them. First a commented pandas tour: load the bars, convert UTC to New York
time, pick one day, compute returns, resample 5-minute bars into 15-minute and daily bars, and prove the resampling
right. Then six indicators written from scratch and tested against TA-Lib. Last, an interactive Plotly chart of one
SPY session with VWAP, a 20-bar EMA, volume and VWAP-cross markers.

## What's in this kit

| File | What it is |
|---|---|
| `prompts.md` | The four requests typed in the lesson, ready to copy, plus the pause-and-try exercise |
| `pandas-cheat-sheet.md` | Every pandas step from the tour, one line each, with the resampling rule and the 9:30 bucket worked by hand |
| `indicator-formulas.md` | SMA, EMA, Wilder's smoothing, RSI, true range and ATR, Bollinger Bands and session VWAP, in plain words and formulas, with the lesson's ours-vs-TA-Lib table |
| `reading-the-chart.md` | What each line and marker on the chart means, the 11:15 bar from the lesson, and why VWAP and the EMA look so different at the open |
| `trading-lab/notebooks/pandas_tour.py` | The pandas tour, as Claude wrote it (113 lines) |
| `trading-lab/indicators.py` | The six indicators, from scratch (114 lines) |
| `trading-lab/tests/test_indicators.py` | The tests: each indicator against TA-Lib, VWAP by hand, and the look-ahead check |
| `trading-lab/reports/spy_session.py` | The chart script (and an empty `reports/__init__.py`, so it runs as a module) |

## Before you start

- You need the Trading Lab and the data cache from Lesson 5.1 (`data/cache/SPY_5min.parquet`). This lesson needs no
  connection to IB: everything runs on the cached history.
- Add the libraries the lesson added, from your `trading-lab` folder:

  ```bash
  uv add plotly          # the chart
  uv add --dev ta-lib    # only for the tests: the referee, not part of the Lab's own code
  ```

  The tests also need `pytest` (from Module 3). Recent TA-Lib versions ship ready-made packages, so no separate C
  library install is needed on common systems.
- The chart's HTML file is about 4.8 MB, because it carries the plotting library inside it so it works offline. Add
  `reports/*.html` to your `.gitignore`, as the lesson did: commit the code that makes the chart, not the chart.

## Run it

```bash
uv run notebooks/pandas_tour.py      # the pandas tour, printed section by section
uv run pytest tests/test_indicators.py   # the indicator tests
uv run -m reports.spy_session        # writes reports/spy_session.html (run it as a module, with -m)
```

Then open `reports/spy_session.html` in your browser: hover a candle, drag a box to zoom, double-click to zoom out.

`uv run reports/spy_session.py` fails with "No module named indicators": running a script by its path puts the
`reports` folder on Python's import path, not the project root. That is the exact error Claude hit and fixed in the
lesson.

## Try it yourself

1. With Claude, add one more indicator to the chart: Bollinger Bands, or RSI in its own panel.
2. Ask Claude to explain one line of the code you don't understand yet.

You're done when the chart opens, and you can say what every line on it means. Your bars, dates and Claude's wording
will differ from the video; the method is what matters.

## Good to know

- The chart's markers show how to draw signals on a chart. They are an illustration, not a strategy, and not a
  reason to trade.
- Indicator readings (like RSI above 70) are descriptions of past prices, not signals or advice.
- Paper (simulated) account and free historical data only. Educational content, not financial advice.
- Library versions and outputs were current at the time of recording (October 2026).
