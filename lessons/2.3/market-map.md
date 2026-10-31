# The map of markets

Lesson 2.3 · values as seen in TWS on a paper account on October 22, 2026. They change: check your own TWS.

## Seven kinds of markets

| Market | What you own | Where it trades | Hours (New York time) | Size and leverage | Our paper account |
|---|---|---|---|---|---|
| **Stock** | A small share of one company | Exchanges (Nasdaq, NYSE and others); one company can also list abroad | Regular 9:30-16:00; pre-market from 4:00; after-hours to 20:00 | One share; buying on margin is possible (lesson 2.6) | Yes: free history and 15-minute delayed quotes. **This course trades these.** |
| **ETF** (exchange-traded fund) | A share of a fund that holds a basket (DIA: the 30 Dow Jones stocks; SPY: the S&P 500) | Exchanges, exactly like a stock (TWS lists DIA as type "Stock") | Same as stocks | One share | Yes, same as stocks. **This course trades these.** |
| **Bond** | A loan to a company or a government that pays interest | Mostly between dealers, over the counter | Varies | Face value, often 1,000 per bond | Shown in the chooser (corporate bonds); not used in this course |
| **Forex pair** | One currency priced in another (EUR.USD = how many dollars one euro costs) | Between banks and dealers, no central exchange | Around the clock from Sunday ~17:00 to Friday ~17:00 | Large contract sizes, high leverage | No data on our paper account (the rows show n/a) |
| **Futures contract** | An agreement to buy or sell later at a price fixed today | Futures exchanges (MES: the CME) | Nearly 24 hours, with a daily one-hour break | A multiplier (MES: 5 dollars per index point) and an expiry; high leverage | MES showed delayed prices; not traded in this course |
| **Option** | The right, not the duty, to buy (call) or sell (put) at a strike price before expiry | Options exchanges | Mostly the regular session of its stock or ETF | One contract covers 100 shares; it loses value as expiry approaches, other things equal | Delayed prices shown; not traded in this course |
| **Crypto** | Digital coins such as bitcoin | Crypto venues (in TWS through providers); funds and futures wrap it too | 24 hours a day, 7 days a week | Varies | Greyed out: no crypto permission on our account |

## What we read in TWS

**The instrument chooser** (type a symbol in an empty watchlist row, press Enter): every product with that name.
For AMD: Stock, Options, Warrants, Structured Products, CFD on Nasdaq; the same company in Toronto, Mexico, Germany and
Switzerland; the company's corporate bonds.

**A stock's Description** (AAPL): Security type Stocks · Currency USD · Exchange SMART (Interactive Brokers' router;
primary exchange Nasdaq) · Market data: delayed, up to 15 minutes · Regular session 09:30-16:00 · Total available hours
04:00-20:00 (US/Eastern) · Overnight trading available · Margin requirement 16.50 % initial · Shortable.

**A futures contract's Description** (MES, December 2026): Security type FUT · Contract month DEC26, expires
December 18, 2026 · Multiplier 5 · Exchange CME · Settlement: cash · Minimum tick 0.25 (= 1.25 USD per contract) ·
Regular 08:30-16:00, total 17:00 (the day before) to 16:00, US/Central time · Initial margin about 3,510 USD per contract.

**The size of one MES contract:** index near 7,734 points x 5 USD = about 38,670 USD of exposure, held with about
3,510 USD of margin: roughly 11 to 1 leverage. Every point is 5 USD, up or down.

**The size of one option:** the SPY 766 call (29 days to expiry) asked 13.90; one contract covers 100 shares, so
about 1,390 USD.

## All the hours on one clock (New York time)

| Session | New York time | UTC in October (summer time) |
|---|---|---|
| US stocks, pre-market | 04:00-09:30 | 08:00-13:30 |
| US stocks, regular session | 09:30-16:00 | 13:30-20:00 |
| US stocks, after-hours | 16:00-20:00 | 20:00-00:00 |
| Micro E-mini (MES) futures | 18:00-17:00 next day, one-hour break | 22:00-21:00 |
| Forex, Asia (Tokyo), roughly | 19:00-04:00 | 23:00-08:00 |
| Forex, London, roughly | 03:00-12:00 | 07:00-16:00 |
| Forex, New York, roughly | 08:00-17:00 | 12:00-21:00 |
| Crypto | always | always |

When the clocks change in New York (early November and mid-March), every UTC time in this table moves by an hour.
Forex session times are approximate; sources differ by an hour.

## Why this course trades US stocks and ETFs

1. **Liquidity**: big stocks and funds like SPY trade millions of shares a day, with spreads of a cent or two.
2. **One session a day**: 9:30 to 16:00, a clear open and a clear close.
3. **The data we already have**: free history and 15-minute delayed quotes on the paper account. Forex, crypto and
   real-time data would need extra permissions or paid subscriptions.
4. **The simplest contracts**: one share, no expiry, no multiplier.

Educational content, not financial advice.
