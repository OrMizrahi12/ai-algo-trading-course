# Market data basics

What the lesson showed about contracts, quotes and IB's answers, on one page.

## Contracts

A **contract** is how IB names what you trade: a symbol, a type, an exchange and a currency. Qualifying a contract
asks IB to fill in the rest, including its **conId**, IB's unique number for one instrument.

| Contract | In `ib_async` | conId | Primary exchange |
|---|---|---|---|
| Apple stock | `Stock("AAPL", "SMART", "USD")` | 265598 | NASDAQ |
| SPY ETF | `Stock("SPY", "SMART", "USD")` | 756733 | ARCA |
| EUR/USD | `Forex("EURUSD")` (venue IDEALPRO) | 12087792 | none |

- `SMART` is IB's order routing: IB picks where to send the order. It is not the listing exchange.
- The primary exchange is where the instrument mainly trades. Forex has none, because it isn't listed anywhere. Its
  venue is **IDEALPRO**, IB's forex market.

## The four market data types

You choose the type with `ib.reqMarketDataType(n)` before you ask for quotes.

| Type | Name | What you get |
|---|---|---|
| 1 | Live | Real-time prices. Through the API they need a paid subscription. |
| 2 | Frozen | The last price IB saw, for when the market is closed (live data). |
| 3 | Delayed | Free, 15 to 20 minutes behind. |
| 4 | Delayed frozen | The last delayed price, for when the market is closed. |

A **snapshot** asks for one reading of the quote instead of a continuous stream. In a quote:

- **Bid**: the best price a buyer offers.
- **Ask**: the best price a seller wants.
- **Last**: the most recent trade.
- **Close**: the previous session's closing price.

## IB's messages from the lesson

| Code | Kind | Seen when | What it means |
|---|---|---|---|
| 354 | Error | Live quotes for AAPL and SPY | Requested market data is not subscribed. The end of the message adds that delayed data is available. |
| 10089 | Error | EUR/USD quotes, live and delayed | The data needs an additional subscription for the API. |
| 10167 | Notice | Delayed quotes for AAPL and SPY | Displaying delayed market data. Not a failure. |
| 300 | Error | After a snapshot | Can't find the request ID: the cancel arrived after IB had already ended the snapshot. Harmless. |
| 162 | Error | EUR/USD historical bars | Historical data service: no market data permissions for IDEALPRO. |
| 420 | Error | SPY 5-second real-time bars | No permission for this data: real-time bars need a real-time subscription. |
| 492 | Warning | The scanner | Without real-time data, the scanner's price and volume filters are imprecise. |
| 2104, 2106, 2107, 2158, 2119 | Status | Connecting | The data farms (IB's data servers) are connected. Not errors. |

`NaN` in a quote means "not a number": no data arrived for that field.

## What our paper account gets

In the lesson, with no paid subscriptions:

- **US stocks and ETFs**: delayed quotes (about 15 minutes behind) and historical bars. Free, and fine for learning
  and testing, but not for judging a trade at the current price.
- **Live quotes**: refused (error 354). Live data through the API is a paid add-on.
- **5-second real-time bars**: refused (error 420).
- **Forex**: nothing in either mode (errors 10089 and 162). It needs a separate data permission.

Your own account may answer differently. A paper account normally shares the market data subscriptions of the live
account it belongs to (one paper account per live user); without shared subscriptions it gets delayed data.

## What live data costs

To receive market data through the API, IBKR asks for a funded IBKR Pro account (not a demo), at least **USD 500** of
equity plus the cost of the subscriptions, and the subscriptions themselves (chosen in the Client Portal, with the
API acknowledgement). Subscriptions are billed monthly and are not pro-rated.

US stock data, non-professional prices per month (IBKR's pricing page, checked 2026-10-20):

| Subscription | Per month | Notes |
|---|---|---|
| US Securities Snapshot and Futures Value Bundle | USD 10.00 | Waived in a month with at least USD 30 of commissions |
| US Equity and Options Add-On Streaming Bundle | USD 4.50 | Needs the bundle above; streaming quotes for US stocks |
| NYSE (Network A/CTA) L1, a la carte | USD 1.50 | |
| Regional exchanges (Network B) L1, a la carte | USD 1.50 | |
| NASDAQ (Network C/UTP) L1, a la carte | USD 1.50 | |

The usual minimum for live US stock data through the API is the first two rows: about **USD 14.50 a month**, plus the
USD 500 equity. This course works with the free, delayed data. Prices change: check IBKR's page before you subscribe.

## Sources

- IBKR market data subscriptions and requirements:
  https://www.interactivebrokers.com/docs/general/market-data-subscriptions/market-data-requirements
- Sharing market data with a paper account:
  https://www.interactivebrokers.com/docs/general/market-data-subscriptions/market-data-users/market-data-sharing
- TWS API, delayed data and the market data types: https://www.interactivebrokers.com/docs/tws-api/doc/md/delayed-data
- IBKR market data pricing: https://www.interactivebrokers.com/en/pricing/research-news-marketdata.php

Checked on 2026-10-20.
