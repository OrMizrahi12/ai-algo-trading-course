# Student kit: Lesson 7.3, The gap scanner

Module 7: Day-trading strategies · AI Algorithmic Trading with Claude Code and Interactive Brokers

Stocks that open far from yesterday's close, on heavy volume, are where many day traders look first. In this lesson you
asked the IB Gateway which scanner codes can find gaps, then had Claude build a gap scanner into the Trading Lab: IB's
two gap scans nominate the candidates, and our own 5-minute bars from the Gateway measure the real gap, the gap in ATRs,
relative volume, price and dollar volume. It ran on the paper connection in the middle of a trading day and wrote a
dated watchlist (94 stocks measured, 60 passed). Claude also explained what the 15-minute data delay means for every
column. Finally, you checked the top name on a chart, and turned the chart script into a small reusable tool.

## What's in this kit

| File | What it is |
|---|---|
| `prompts.md` | Every request typed in the lesson, the commands, and the pause-and-try exercise |
| `cheat-sheet.md` | Gap, gap in ATRs, relative volume and dollar volume; IB's scan codes; the filters; what the delay means |
| `trading-lab/scanner.py` | The scanner file, with the new gap scanner (IB client ID 4, read-only, paper checks) |
| `trading-lab/tests/test_gap_scanner.py` | Offline tests with a fake IB and hand-made bars (14 tests, no Gateway needed) |
| `trading-lab/reports/gap_chart.py` | Study chart of one stock's 5-minute bars with a dashed line at the previous close (IB client ID 9) |
| `trading-lab/tests/test_gap_chart.py` | Offline tests for the chart tool's pure parts (4 tests) |

The scanner reuses `market_data.py` (host, port, delayed data and the 55-requests-per-10-minutes history throttle from
Lesson 4.3) and `indicators.py` (ATR). The lesson also updated `AGENTS.md`: the client ID list and one line each for the
scanner and the chart tool. The watchlist CSV itself is not in this kit: run the scanner to make your own.

## Before you start

- The Trading Lab as of **Lesson 7.2**, with `market_data.py`, `indicators.py` and the scanner from Lesson 4.3.
- IB Gateway running and logged in to your **paper** account (port 4002), API enabled. Free delayed data is enough.
- The gap scanner is most useful on a trading day while the market is open. Outside market hours there is no "today"
  for it to measure, and it says so.
- The chart tool works any time for a past trading day, because it only reads history.

## Try it yourself

1. In your `trading-lab` folder, start `claude`, `/clear`, and send the first request in `prompts.md`. Read which scan
   codes your account can use, and the caveats.
2. `/clear`, and send the build request while the market is open. Let Claude work through the tests and the first real
   run. A full scan of about 100 candidates takes roughly 10 minutes because of IB's history pacing limit.
3. Read the delay section of Claude's answer, then pick a name from your list and chart it with the chart requests.

You're done when the tests pass, `watchlists/gap_scan_<date>.csv` exists, and you can explain why the gap numbers hold
up with delayed data while price and relative volume don't. Your names, numbers and Claude's replies will differ from
the video; the behaviour is what matters.

## Good to know

- IB's scanner is a nominator, not a measurer: it returns symbols and ranks, not the gap itself. With delayed data IB
  also says the scan results aren't precise (message 492), and each scan returns at most 50 rows.
- Claude added a market-cap floor of $300 million to the scan to save history requests. It wasn't in the request, and
  Claude reported it. Change `SCAN_MIN_MARKET_CAP_M` if you disagree.
- IB code 162 is used for pacing errors and for harmless notices. The scanner only treats it as pacing when the text
  says so.
- If you have more programs connected to the Gateway, every one needs its own client ID. The lab's list is in `AGENTS.md`.

## Safety

Paper trading only. Educational content, not financial advice. The stocks in the video are that day's examples of what
the scanner found: they are not tips or recommendations, and a watchlist says nothing about what a stock does next.
Everything in this lesson is read-only; nothing places an order.
