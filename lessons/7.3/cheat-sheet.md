# Lesson 7.3 cheat sheet: the gap scanner

## The words

| Term | Meaning | In `scanner.py` |
|---|---|---|
| Gap | The jump between yesterday's close and today's open (news overnight, earnings, upgrades) | |
| Gap % | (today's open / yesterday's close - 1) x 100 | `gap_pct` |
| Gap in ATRs | (open - previous close) / ATR. ATR (average true range) = a normal day's travel, 14 daily bars | `gap_atr` |
| Relative volume | Shares traded so far today / the average traded by the same time of day over the last 20 sessions | `rel_vol` |
| Dollar volume | Price x shares traded per day; we use the 20-session average | `avg_dollar_vol` |
| Stock in play | Traders' name for a big gap on heavy relative volume | |
| Scanner | IB's built-in stock screener: returns symbols and ranks | `gap_candidates` |
| Watchlist | A list of candidates to study. Not a signal to buy or sell | `watchlists/gap_scan_YYYY-MM-DD.csv` |

Example: a stock closes at $100 and opens at $90. Gap % = -10%. If its ATR is $2.50, the gap is -4 ATRs.

## IB scan codes for gaps (as Claude found them in the Gateway's scanner parameters)

| Code | What it ranks |
|---|---|
| `HIGH_OPEN_GAP` | Biggest close-to-open gainers (gapped up) |
| `LOW_OPEN_GAP` | Biggest close-to-open losers (gapped down) |
| `TOP_PERC_GAIN` / `TOP_PERC_LOSE` | Change since yesterday's close. Looks similar, but it is not a gap |
| `TOP_OPEN_PERC_GAIN` / `TOP_OPEN_PERC_LOSE` | Change since today's open |
| Filters `openGapPercAbove` / `openGapPercBelow` | Gap size filters (in the video, they seemed to change nothing) |

Location `STK.US.MAJOR` = major US exchanges. `stockTypeFilter="CORP"` = corporate stocks only (no ETFs).
`marketCapAbove` is in **millions** of dollars.

## The scanner's pipeline

1. Candidates: both gap scans, up to 50 rows each, price above $5, market cap at least $300M, corporate stocks only.
2. Measure: one read-only history request per candidate, about a month of regular-hours 5-minute bars.
3. Filter: price above $5, average dollar volume at least $20M a day, gap at least 2% **or** at least 1 ATR.
4. Rank by relative volume, highest first. Save `watchlists/gap_scan_YYYY-MM-DD.csv` and print the table.

IB allows about 60 history requests per 10 minutes; the lab's throttle stays at 55. About 100 candidates take roughly
10 minutes.

## What the 15-minute delay means (Claude's answer in the video)

| Column | With free delayed data |
|---|---|
| Gap %, gap in ATRs | Hold up: the open is a fixed print from 9:30, and the previous close doesn't change |
| Price | A snapshot 15 to 25 minutes old (the delay, plus the bar that is still forming) |
| Relative volume | Also stale, and very noisy early in the day (only one or two bars) |
| At the open | Nothing to measure until about 9:45 New York time: good for study and watchlists, not for timing entries |
| IB's candidate list | Approximate (message 492) and capped at 50 rows per scan, so some gappers never become candidates |
| Ranking | Stocks are measured one after another, so the first and last can be up to 10 minutes apart |

A real-time market data subscription removes the delay; the lesson uses free delayed data on purpose.

## Things Claude reported itself

- An extra filter you didn't ask for: the $300M market-cap prefilter.
- IB's volume for these bars may be lower than the whole market's, so dollar volume is probably understated. Claude
  said it didn't check that.
- Which stocks were skipped, and why.
- Safety: read-only connection, paper port 4002, account checked to start with DU.

## That day's top 10 (2026-10-22, scan at 13:19 New York, ranked by relative volume)

These are examples of what the scanner found that day, not tips. They say nothing about what happened next.

| # | Symbol | Scan | Gap % | Gap in ATRs | Rel vol |
|---|---|---|---|---|---|
| 1 | HXL | down | -12.78 | -4.83 | 16.6x |
| 2 | TTMI | down | -18.03 | -2.16 | 9.0x |
| 3 | SNA | down | -10.56 | -7.20 | 8.8x |
| 4 | CRS | down | -10.26 | -2.96 | 8.3x |
| 5 | GGG | down | -10.67 | -6.45 | 7.7x |
| 6 | FPS | down | -14.39 | -1.95 | 7.4x |
| 7 | RCUS | down | -8.84 | -1.00 | 6.6x |
| 8 | PG | up | +3.33 | +2.00 | 5.2x |
| 9 | COHU | down | -7.31 | -1.03 | 5.1x |
| 10 | CSX | up | +3.68 | +2.48 | 5.0x |

SNA has the biggest gap in ATRs but is third: the list is ranked by relative volume, not gap size.

## Client IDs in the lab

Every program connected to the Gateway at the same time needs its own client ID. The scanner uses 4, the chart tool 9.
The full list is in `AGENTS.md`; IDs 8, 20 and 30 are kept for the desk project later in the course.
