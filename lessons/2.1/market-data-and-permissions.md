# Market data and permissions: the exact steps

All of these settings live in your IBKR **account settings** on the website (the account portal, called Client
Portal in IBKR's guides): log in at interactivebrokers.com → **Log In**, then open the **user menu** (the
head-and-shoulders icon, top right) → **Settings**. IBKR renames menu items from time to time; if a name differs,
use the search box in the portal or IBKR's help pages. Do these in your **live** account login: the paper account
takes its permissions and market data from it.

**This course uses only the free data every account gets**: the price history and delayed quotes (about 15
minutes behind). Sections 1 and 2 are all you need. The "Optional" part below is for later, if you ever want
real-time data or forex; nothing in this course needs it, and nothing here costs you anything unless you choose to
subscribe.

Facts and prices below were read on IBKR's official pages on 2026-10-21. **Prices may change**: check
interactivebrokers.com/en/pricing/market-data-pricing.php before you subscribe to anything.

## 1. Market data subscriber status: non-professional

1. **Settings** → **Market Data Subscriptions** (in the trading platform / user settings section).
2. Click the gear next to **Market Data Subscriber Status**.
3. Choose **Non-Professional** if it is true for you, and agree to the terms shown.

A non-professional subscriber is a private person (not a company or trust) who is not registered or qualified with a
securities or commodities regulator or exchange, is not an investment adviser, and does not perform such functions
for a bank or another organization. Anyone who does meet those criteria is a professional subscriber, and pays far
more for data. Answer honestly. IBKR may ask you to fill in a short non-professional questionnaire; the answer
arrives in the portal's message center.

## 2. Market Data API Acknowledgement

The course's Python code receives prices through the API. IBKR asks you to sign an acknowledgement once:

1. **Settings** → **Market Data Subscriptions**.
2. Find the **Market Data API Acknowledgement** box and click its gear.
3. Under "Would you like to enable this functionality", choose **Yes**, continue, then review and sign the form.
4. Log out of TWS (and IB Gateway, later) and log back in.

## Optional (not needed for this course)

### A. Real-time data in the paper account

The paper account has no subscriptions of its own. Without sharing, it shows delayed data where available, which is
what this course uses. If you ever pay for real-time data on your live account and want it in paper too:

1. **Settings** → **Account Configuration** → **Paper Trading Account**.
2. Set "share real-time market data subscriptions with the paper trading account" to **Yes**, pick your live
   username, and save.
3. Allow time for it to take effect (often the next day), then log out of TWS and back in on the Paper Trading tab.

One live user shares with one paper account, and while data is shared the live and paper sessions can't both use it
at the same time. In TWS, delayed prices sit on a **dark olive background** (as in the lesson); real-time prices
have a plain dark background.

### B. Forex

In the lesson, EUR.USD showed "**No market data permissions for IDEALPRO CASH**". IDEALPRO is IBKR's forex venue;
CASH is IBKR's name for spot currency pairs. Forex needs its own trading permission (**Settings** → **Trading** →
**Trading Permissions** → **Forex**, then IBKR's approval) and its own data. This course trades US stocks and ETFs,
not forex, so you can skip this.

### C. What real-time US data costs

This course uses none of these. They are here so you know what real-time data would cost if you ever want it.

| Data | Price (non-professional, per month, 2026-10-21) | What you get |
|---|---|---|
| Free delayed data | Free | Delayed quotes, where available (what this course uses) |
| Free US streaming (Cboe One + IEX) | Free on the live account | Real-time quotes for US-listed stocks and ETFs from those two venues only (non-consolidated) |
| Snapshot quotes | 100 free per month | One-off real-time quotes at order entry |
| US Securities Snapshot and Futures Value Bundle | about USD 10.00 (waived in a month with at least USD 30 in commissions) | The base US bundle; snapshots cost USD 0.01 each |
| US Equity and Options Add-On Streaming Bundle | USD 4.50 (requires the bundle above) | Consolidated real-time streaming from all US exchanges |

Through the API, IBKR states that live (real-time) data generally needs a paid subscription and a minimum account
equity (USD 500 on 2026-10-21). Subscriptions are billed per calendar month and are not pro-rated. To subscribe:
**Settings** → **Market Data Subscriptions** → **Configure** → North America → tick the bundles → continue and sign.

## Checklist

- [ ] Subscriber status: non-professional (if it is true for you)
- [ ] Market Data API Acknowledgement signed
- [ ] Logged out of TWS and back in on the Paper Trading tab after the changes
- [ ] (Optional, not needed for this course) real-time data, sharing it with paper, forex
