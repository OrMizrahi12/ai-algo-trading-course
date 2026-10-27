# Lesson 7.3 prompts and commands

Everything typed in the lesson, in order. Lines that start with `/` are Claude Code commands; lines that start with `!`
run in the terminal from inside Claude Code (shell mode). Every request runs in auto mode, with IB Gateway logged in to
the paper account (port 4002).

## 1. Ask the Gateway first

```text
/clear
```

```text
Before we build anything: which IB scanner codes and filters can find today's gappers on US stocks? Ask the Gateway for its scanner parameters, look for the gap-related scan codes and filters, and tell me which ones our paper account can really use with delayed data. Paper only, read-only connection.
```

Claude downloads the scanner parameters (one large XML file), searches it for gap codes and filters, runs a few small
read-only scans, and answers with a table. In the video: two gap codes (`HIGH_OPEN_GAP`, `LOW_OPEN_GAP`), the filters
`openGapPercAbove` / `openGapPercBelow`, IB message 492 on every scan, and leveraged ETFs mixed into the results.

## 2. Build the gap scanner (while the market is open)

```text
/clear
```

```text
The US market is open right now. Build a gap scanner for the open in scanner.py: use IB's HIGH_OPEN_GAP and LOW_OPEN_GAP scans for candidates (US stocks only, no ETFs), then our own daily history from the Gateway to compute the real gap %, the gap in daily ATRs, relative volume by time of day, price and average dollar volume. Filters: price above 5 dollars, at least 20 million dollars average daily dollar volume, a gap of at least 2% or 1 ATR. Rank by relative volume, save today's list to watchlists/ with the date, and show it as a table. Tests on fake data, paper only, read-only connection. Then run it for real and tell me what the 15-minute delay means for this list.
```

In the video, Claude wrote the scanner and 14 offline tests, fixed its own test data (too little fake volume to pass
the $20M filter), fixed a false "pacing" alarm (IB code 162 was a harmless notice), added a $300M market-cap prefilter
so the scan needs fewer history requests, committed, and let the full scan run in the background. Run them yourself:

```text
! uv run pytest -q tests/test_gap_scanner.py
! uv run scanner.py
```

## 3. Check the top name on a chart

```text
/clear
```

```text
From our gap watchlist of 2026-10-22, take the top name by relative volume and make a quick Plotly chart of its 5-minute bars for that whole session, pulled from the Gateway history, with a dashed line at the previous day close so the gap is easy to see. Save it as an HTML file in the lab and open it in Chrome. This is a study chart, not a tip, so keep the title neutral.
```

Use your own watchlist's date. Claude reads the CSV, pulls the bars, writes the chart and checks the gap it measured
against the watchlist's number.

## 4. Make it a tool

```text
It opened in Chrome, thanks. Yes, move the script into the lab as a small reusable tool that takes the symbol and the date, add a test, and commit it.
```

In the video, the first attempt was blocked by the live-port hook from Module 3 (a test named a live port to check that
the tool refuses it). Claude rewrote the test with a made-up port and committed.

```text
One catch: our desk project uses client ID 8 for its heartbeat, 20 for its MCP server, and 30 for the Nautilus test. Two programs with the same ID cannot be connected at once. Pick a free ID for the chart tool, note all of these in AGENTS.md, run the tests, commit and push.
```

The desk project comes later in the course. If you don't have it yet, ask for a free ID that isn't in `AGENTS.md`.

```text
Run the tool once for TTMI on 2026-10-22 and open it.
```

Or run it yourself, with any symbol and trading day:

```text
! uv run -m reports.gap_chart TTMI 2026-10-22 --open
```

## Pause and try

In your watchlist (or the table in the video), find the stock with the biggest gap in ATRs. Is it first on the list? If
not, why not? (Answer: the list is ranked by relative volume, not by gap size.)

## Try next (optional)

- Ask Claude to add a `--rank gap_atr` option, and compare the two lists for the same day.
- Run the scanner twice, an hour apart, on the same day. Which columns change, and which stay the same?
- Chart the stock with the biggest gap up on your list, and look at whether the gap was filled during the day.
