# Reading the chart

`trading-lab/reports/spy_session.py` draws the latest full SPY session (78 five-minute bars) from the cache into
`reports/spy_session.html`. In the lesson that was Tuesday, October 20, 2026.

## What's on it

| On the chart | What it is |
|---|---|
| Teal and red candles | One 5-minute bar each: teal when the close is above the open (up bar), red when below |
| Blue line | The session VWAP: the average price paid so far that day, weighted by volume |
| Amber line | The 20-bar EMA of the close |
| Triangles | The close crossing VWAP: up triangles below the bar for a cross above, down triangles above the bar for a cross below |
| Bottom panel | Volume, colored like the candle |
| Time axis | New York time, 9:30 to 16:00 |
| Title | "illustration only, not a strategy" |

The markers show how to draw signals on a chart. They are not a reason to trade. On the lesson's session the script
found six crossings up and six down.

## Hover, zoom, reset

- **Hover** over a candle: one box shows everything for that bar (the chart uses a unified hover).
- **Drag** a box over a stretch of time to zoom in.
- **Double-click** to zoom back out.

The 11:15 bar from the lesson:

| Field | Value |
|---|---|
| Open | 768.92 |
| High | 770.08 |
| Low | 768.73 |
| Close | 769.86 |
| VWAP | 769.0804 |
| EMA 20 | 769.8482 |
| Marker | Close crosses above VWAP, 11:15, close 769.86 |

## The two lines at the open

Zoom into the first ninety minutes and compare the lines:

- **VWAP starts fresh at 9:30.** It resets every session, so its first value is the first bar's typical price, and it
  follows the price closely early in the day.
- **The EMA arrives already moving.** The script computes it across earlier days, so at the open it still carries
  the previous day's bars. That was a deliberate choice: the EMA is "warm" at the open instead of starting empty.

Same chart, two very different memories.

## Why the HTML file isn't in Git

The file carries the whole plotting library inside it (about 4.8 MB), so it opens offline, without a server. The
lesson keeps `reports/*.html` out of Git: only the code that makes the chart is committed, and anyone can rebuild it
with `uv run -m reports.spy_session`.
