# Pacing and the scanner

## Pacing limits

**Pacing** means IB slows down, rejects or disconnects programs that ask too fast. These are IB's documented limits
(checked 2026-10-20). They match what Claude listed in the lesson, with one correction for the scanner (below).

**Historical data** (`reqHistoricalData`, and real-time 5-second bars):

- The same request can't repeat within **15 seconds**.
- No more than **6 requests** for the same contract, exchange and data type within **2 seconds**.
- No more than about **60 requests in any 10 minutes**.
- BID_ASK requests count twice.

**Market data lines and messages:**

- A market data line is one live subscription (a quote stream, or a set of real-time bars). Everyone gets **100
  lines at once** by default; more come with higher commissions or equity.
- The whole API accepts about **50 messages per second** with 100 lines (lines divided by 2).

## The throttle in `market_data.py`

- `Throttle.wait(ib, key)` runs before every historical request. It sleeps only as long as needed: 15 seconds before
  repeating the same request, and until the 10-minute window has room. Its cap is **55** requests instead of 60, a
  safety margin.
- `check_line_room(ib)` runs before every new market data line and raises an error before the 100-line default would
  be passed.
- Claude tested the throttle offline with a fake connection, so nothing touched IB: a repeated request waited 15.0 s,
  and a full window waited 600.0 s.
- The "6 requests in 2 seconds" rule has no check of its own; at our request rate, the 15-second gap and the 10-minute
  cap keep us well under it.

## The market scanner

A **scanner** is IB's own search. It runs on IB's servers and returns the instruments that match a rule.
`scanner.py` asks for:

- scan code **TOP_PERC_GAIN**: today's biggest percentage gainers,
- location **STK.US.MAJOR**: stocks on the major US exchanges,
- price above **USD 5** and volume above **1 million** shares,
- the top **10** rows: rank, symbol and exchange.

What to know when you read the result:

- The scanner returns contracts only, not prices. Ask for quotes separately.
- Every row said **SMART**: that's IB's order routing, not the listing exchange.
- Warning **492**: without real-time data, the price and volume filters are imprecise, so some rows may not truly pass
  them.
- **Correction**: on screen Claude said "at most 50 scanner subscriptions at once". IB's documentation says at most
  **10 active scanner subscriptions** at a time, with up to **50 results** each.

The symbols in the lesson were that day's examples of what a scanner returns. They are **not tips and not
recommendations**: the day's biggest gainers are often the riskiest stocks on the board.

## Sources

- TWS API, historical data limitations (the pacing rules):
  https://www.interactivebrokers.com/docs/tws-api/doc/md/introduction
- TWS API, pacing limitations (requests per second): https://www.interactivebrokers.com/docs/tws-api/doc/pacing-limitations/introduction
- TWS API, market scanner (50 results per scan, 10 active scans):
  https://www.interactivebrokers.com/docs/tws-api/doc/market-scanner/introduction
- IBKR, how market data lines are allocated:
  https://www.interactivebrokers.com/docs/general/market-data-subscriptions/market-data-lines/how-market-data-is-allocated

Checked on 2026-10-20.
