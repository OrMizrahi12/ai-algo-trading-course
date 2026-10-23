# Pandas for traders: cheat sheet

Every step of the lesson's tour (`trading-lab/notebooks/pandas_tour.py`), one line each. `bars` is the table of SPY
5-minute bars from the Lesson 5.1 cache.

## The words

- **pandas**: Python's library for tables.
- **DataFrame**: a pandas table. Here, one row per bar.
- **Index**: the row labels. Here, each bar's start time.
- **Column**: one field of every row: `open`, `high`, `low`, `close`, `volume`, `average`, `barCount`.
- **NaN**: "not a number", pandas' marker for a missing or not-yet-defined value.

## The columns of a bar

| Column | Meaning |
|---|---|
| `open` | the first price in the five minutes |
| `high` | the highest price |
| `low` | the lowest price |
| `close` | the last price |
| `volume` | shares traded |
| `average` | the volume-weighted average price of that one bar |
| `barCount` | the number of trades in the bar |

## The steps

| Step | Code | What it does |
|---|---|---|
| Load | `bars = pd.read_parquet(CACHE)` | Reads the cache file into a DataFrame, indexed by bar start time |
| Look | `bars.head()`, `bars.dtypes`, `len(bars)` | First rows, column types, number of rows |
| Time range | `bars.index.min()`, `bars.index.max()` | First and last bar time |
| Time zone | `bars.index = bars.index.tz_convert("America/New_York")` | Relabels UTC times as New York times: same instant, new clock, daylight saving handled |
| One day | `bars.loc["2026-10-21"]` | Every row on that calendar day |
| Returns | `bars["ret"] = bars["close"].pct_change()` | Each bar's move from the previous close, as a fraction (0.001 = 0.1%) |
| Volatility | `day["ret"].std()` | Standard deviation of returns: the typical size of a move |
| Biggest moves | `day["ret"].max()`, `day["ret"].idxmax()` | The biggest return, and the time of that bar |
| Bigger bars | `bars[list(OHLCV)].resample("15min").agg(OHLCV).dropna()` | 5-minute bars into 15-minute bars (see below) |
| Daily bars | `bars[list(OHLCV)].resample("1D").agg(OHLCV).dropna()` | The same rule, one bar per New York day |
| Per-day max | `bars.groupby(bars.index.date)["high"].max()` | The highest 5-minute high of each day, computed directly |

Compute returns on the whole file first, then slice the day. That way the day's first bar has a real previous close
(yesterday's last bar), and its return includes the overnight gap.

## The resampling rule

```python
OHLCV = {"open": "first", "high": "max", "low": "min", "close": "last", "volume": "sum"}
bars15 = bars[list(OHLCV)].resample("15min").agg(OHLCV).dropna()
```

Read it left to right:

1. `bars[list(OHLCV)]` keeps the five columns named in the dictionary.
2. `.resample("15min")` puts the rows into 15-minute buckets: the 9:30, 9:35 and 9:40 bars land in the 9:30 bucket.
3. `.agg(OHLCV)` squashes each bucket into one row, column by column: first open, highest high, lowest low, last
   close, summed volume.
4. `.dropna()` removes the empty buckets: nights and weekends, when nothing traded.

## Why you can't average the prices

The real 9:30 bucket on October 21, 2026, from the lesson:

| 5-minute bar | high |
|---|---|
| 9:30 | 771.23 |
| 9:35 | 770.98 |
| 9:40 | 771.17 |

- The 15-minute high is the biggest one, **771.23**. The average (about 771.13) is a price the market never reached.
- The low works the same way: the single lowest price, 769.73.
- Only the first bar's open and the last bar's close count.
- Volume is a count of shares: add it up. Averaging it would make it three times too small.
- Averaged bars look calmer than the market really was, so anything built on them, like a stop-loss placed just
  below a low, would sit in the wrong place.

## The tour's numbers (October 2026 data)

- 1,713 bars, from September 22 to October 21, 2026, over 22 trading days.
- The cache stores UTC: the first bar of a day reads 13:30 UTC, which is 9:30 in New York (the opening bell).
- October 21 has 75 bars, not 78 (6.5 hours × 12), because the cache stops at the 15:40 bar; that day's close is
  really the 15:40 bar's close.
- 75 five-minute bars became 25 fifteen-minute bars.
- A typical five-minute move that day was about 0.06% (standard deviation of returns).
- The proof: on all 22 days, the daily high equals the highest 5-minute high, and the daily low the lowest 5-minute
  low.

Your numbers will differ: they depend on the dates in your cache.
