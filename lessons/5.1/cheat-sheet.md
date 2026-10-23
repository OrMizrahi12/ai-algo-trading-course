# Lesson 5.1 cheat sheet: the data pipeline

## Words

| Word | Meaning |
|---|---|
| Bar | One candle: open, high, low, close and volume for a fixed period (here 5 minutes or 1 minute) |
| Chunk | One historical request. The downloader asks for the newest chunk, then steps backwards with `endDateTime` |
| Pacing | IB's speed limit for historical data. Asking too fast gets a pacing error instead of bars |
| Parquet | A compact file format for tables. Fast to read, and it keeps column types and time zones |
| Incremental update | Download only the bars newer than what the cache already has |
| Forming bar | The bar of the current, unfinished period. It changes until the period ends, so it is never stored |
| UTC | Coordinated Universal Time: one clock with no daylight saving jumps |
| RTH | Regular trading hours: 9:30 to 16:00 New York time for US stocks (`useRTH=True`) |
| Survivorship bias | Testing only on companies that still exist makes past results look better than they were |

## IB's pacing limits for historical data

From IBKR's TWS API documentation (checked 2026-10-20):

- No identical request within 15 seconds.
- No 6 or more requests for the same contract, exchange and tick type within 2 seconds.
- No more than 60 requests in any 10-minute period.

IBKR lists these under small bars (30 seconds or less); the Lab applies the same limits to every historical request,
to stay safe.

The Lab's `Throttle` (from `market_data.py`, Lesson 4.3) keeps a 5-request safety margin (55 per 10 minutes) and holds
a repeated request for 15 seconds. The downloader also waits half a second between requests and backs off 15, 30, 60
and 120 seconds after a pacing error before it gives up.

IB is not a bulk data vendor: it works well for a few symbols and months of 1- to 5-minute bars, if you keep a cache.

## How the downloader works

1. Read the last bar in the cache file. No file yet: seed 30 calendar days (5-minute) or 3 trading days (1-minute).
2. Ask IB for the newest chunk (1 week of 5-minute bars, or 1 day of 1-minute bars), then step backwards until the
   start is covered.
3. Treat a request that times out (60 s, no reply) or a dropped data farm (codes 2103, 2105, 2110, 2157) as a failure:
   retry, then stop. An empty answer is only trusted as "no bars" (a weekend or holiday) when IB said nothing wrong.
4. Drop the bar that is still forming, merge with the cache (newest copy wins), sort, and write the file atomically.
   If anything fails, nothing is written, so a failed run can't leave a hole.

## Bars per regular session (US stocks)

| Bar size | Bars per full day | Example from the lesson |
|---|---|---|
| 5 minutes | 78 (6.5 hours x 12) | 21 full sessions x 78 + 75 bars so far today = 1,713 |
| 1 minute | 390 | 2 full days x 390 + 374 so far today = 1,154 |

Early-close days (for example the day after Thanksgiving) have fewer bars. The quality report uses the NYSE calendar
from `exchange_calendars`, so it knows them.

## UTC and New York time

| Season | 9:30 open in New York | Same moment in UTC |
|---|---|---|
| Summer (daylight saving, UTC-4) | 09:30 | 13:30 |
| Winter (standard time, UTC-5) | 09:30 | 14:30 |

Store UTC; convert to New York time only for display and for session logic. On New York's wall clock one hour repeats
when daylight saving ends (01:30 happens twice) and one hour is skipped in spring, which creates false duplicates and
gaps. UTC never jumps.

In pandas: `df.index.tz_convert("America/New_York")` shows New York time; the cache index stays UTC.

## The quality checks

| Check | What it catches |
|---|---|
| Duplicate timestamps | The same bar stored twice |
| Zero or negative prices | Broken rows |
| High below low, close outside high-low | Impossible bars |
| Zero-volume bars | Bars with no trades in a liquid stock (suspicious) |
| Bars outside session hours | Extended-hours bars in a regular-hours file |
| Gaps inside sessions | Missing bars between the open and the close |
| NYSE days missing entirely | Whole trading days that never arrived |
| Bars on non-trading days | Bars on weekends or holidays |

A gap at the very end of today usually means the cache is stale (delayed data, or a run before the close). Run the
download again.

## Survivorship bias, tested

IB returned `Error 200: No security definition has been found for the request` for Lehman Brothers (LEH), Enron
(ENRNQ), SVB Financial (SIVB), Bed Bath & Beyond (BBBY) and Sears Holdings (SHLDQ). The control, AAPL, was found with
251 daily bars. IB acts as if delisted companies never existed, so a backtest on IB history only sees the survivors.
Treat its results as an upper bound. Fixing that needs a separate data source with delisted stocks.

## Commands

| Command | What it does |
|---|---|
| `uv run -m data_pipeline` | Update every cache file (needs IB Gateway paper on port 4002) |
| `uv run -m data_pipeline --dry-run` | Show what each file would fetch, without connecting |
| `uv run -m data_pipeline --quality` | Check the cached files (offline) |
| `uv run -m data_pipeline --symbols SPY --bar-sizes 1min` | Only some symbols or bar sizes |
| `uv run pytest -q` | The offline tests, with a fake IB |

Read the cache in Python:

```python
import pandas as pd
bars = pd.read_parquet("data/cache/AAPL_5min.parquet")
print(bars.tail())
print(bars.index.tz_convert("America/New_York")[-1])
```
