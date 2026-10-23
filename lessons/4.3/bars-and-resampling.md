# Bars, small and big

## What a bar is

A **bar** is one slice of time with four prices and a volume:

- **Open**: the first price in the slice.
- **High**: the highest price.
- **Low**: the lowest price.
- **Close**: the last price.
- **Volume**: how much traded in the slice.

## Asking IB for bars

`market_data.py` asks for the last day of 5-minute bars with `reqHistoricalData`:

```python
bars = ib.reqHistoricalData(
    contract,
    endDateTime="",        # empty = now
    durationStr="1 D",
    barSizeSetting="5 mins",
    whatToShow="TRADES",   # stocks: built from trades
    useRTH=True,           # regular trading hours only
    formatDate=2,          # timestamps in UTC
)
```

- **TRADES** builds bars from real trades, so they have a volume. That's the usual choice for stocks.
- **MIDPOINT** builds bars from the middle of bid and ask. Forex needs it: IB has no traded volume for forex, and
  TRADES isn't offered for it.
- **useRTH=True** keeps only regular trading hours (no pre-market or after-hours).
- The times are in **UTC**. The New York open, 9:30 in the morning, is **13:30 UTC** in the lesson (October, US
  daylight saving time; it's 14:30 UTC in winter).

**5-second real-time bars** (`reqRealTimeBars`) are a different request: IB streams them only to accounts with a
real-time subscription, so on our free paper data the request was refused (error 420).

## Small bars into big ones

A bigger bar is built from the smaller bars in its time window:

| Field | Rule |
|---|---|
| Open | the **first** open |
| High | the **highest** high |
| Low | the **lowest** low |
| Close | the **last** close |
| Volume | the **sum** of the volumes |

In pandas this is one call (`resample_bars` in `market_data.py`):

```python
df.resample("15min").agg(
    {"open": "first", "high": "max", "low": "min", "close": "last", "volume": "sum"}
).dropna(subset=["open"])
```

Change `"15min"` to `"1min"` or `"5min"` and nothing else changes. The `dropna` drops empty windows (for example the
time when the market is closed).

## The lesson's first 15-minute bar, by hand

Apple, 21 October 2026, three 5-minute bars (UTC):

| 5-min start | Open | High | Low | Close | Volume |
|---|---|---|---|---|---|
| 13:30 | **339.28** | 340.34 | **338.83** | 339.30 | 1,290,807 |
| 13:35 | 339.30 | 340.18 | 339.08 | 340.15 | 420,633 |
| 13:40 | 340.09 | **341.19** | 340.02 | **340.12** | 707,938 |

The 13:30 15-minute bar:

- Open **339.28**: the first open (13:30).
- High **341.19**: the highest of the three highs (13:40).
- Low **338.83**: the lowest of the three lows (13:30).
- Close **340.12**: the last close (13:40).
- Volume **2,419,378** = 1,290,807 + 420,633 + 707,938.

## Watch the last bar

If the market is still open when you pull the data, the last bigger bar holds only the small bars that exist so far.
In the lesson the last 15-minute bar (19:15) held only one 5-minute bar. Don't treat a bar like that as a full bar.

## When the request is refused

The step that builds bigger bars never got real 5-second bars (error 420), so Claude tested it with made-up bars
first and said so: 13 made-up 5-second bars gave one full 1-minute bar from the first 12, and the 13th started the
next minute. Then it ran the same function on the real Apple 5-minute bars: 70 bars became 24 bars of 15 minutes.
Your counts will differ with the day and the time you run it.

## Sources

- TWS API, historical bars (bar sizes, whatToShow, TRADES not offered for forex):
  https://www.interactivebrokers.com/docs/tws-api/doc/md/historical-bars
- TWS API, 5-second real-time bars: https://www.interactivebrokers.com/docs/tws-api/doc/md/5-second-bars
- pandas `DataFrame.resample`: https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.resample.html

Checked on 2026-10-20.
