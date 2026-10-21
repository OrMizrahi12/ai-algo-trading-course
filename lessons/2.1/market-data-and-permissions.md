# Market data and permissions: the exact steps

All of these settings live in your IBKR **account settings** on the website (the account portal, called Client
Portal in IBKR's guides): log in at interactivebrokers.com → **Log In**, then open the **user menu** (the
head-and-shoulders icon, top right) → **Settings**. IBKR renames menu items from time to time; if a name differs,
use the search box in the portal or IBKR's help pages. Do these in your **live** account login: the paper account
takes its permissions and market data from it.

Facts and prices below were read on IBKR's official pages on 2026-10-21. **Prices may change**: check
interactivebrokers.com/en/pricing/market-data-pricing.php before you subscribe.

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

## 3. Share market data with your paper account

The paper account has no subscriptions of its own. It uses your live account's market data **only if you share it**;
without sharing, it gets delayed data where available.

1. **Settings** → **Account Configuration** → **Paper Trading Account**.
2. Set "share real-time market data subscriptions with the paper trading account" to **Yes** and pick your live
   username, then save.
3. Allow time for it to take effect (often the next day), then log out of TWS and log back in on the Paper Trading tab.

Good to know: one live user shares with one paper account. While data is shared, the live and the paper session
can't both use it at the same time; if both are open at once, they must run on the same computer.

How to see it in TWS: delayed prices sit on a **dark olive background** (that's what our watchlist showed in the
lesson). Real-time prices have a plain dark background.

## 4. The Forex trading permission

In the lesson, EUR.USD showed "**No market data permissions for IDEALPRO CASH**". IDEALPRO is IBKR's forex venue;
CASH is IBKR's name for spot currency pairs. That message means the account has no Forex trading permission yet.
Forex quotes themselves are free at IBKR ("IBKR Currencies", fee waived), but the account needs the permission.

1. **Settings** → (Account Settings) **Trading** → **Trading Permissions**.
2. Find **Forex** (shown as Cash Forex / Currency) and click **Add** or **Request**.
3. Pick the region(s) you want, continue, and read and sign the risk disclosures that follow.
4. Wait for approval (IBKR says requests are typically handled within about 48 business hours). The paper account
   inherits the permission from the live account.
5. Log out of TWS and log back in. EUR.USD should now show a quote.

## 5. What the data costs (US stocks)

| Data | Price (non-professional, per month, 2026-10-21) | What you get |
|---|---|---|
| Free US streaming (Cboe One + IEX) | Free | Real-time quotes for US-listed stocks and ETFs from those two venues only (non-consolidated) |
| Free delayed data | Free | Delayed quotes on other products, where available |
| Snapshot quotes | 100 free per month | One-off real-time quotes at order entry |
| US Securities Snapshot and Futures Value Bundle | about USD 10.00 (waived in a month with at least USD 30 in commissions) | The base US bundle; snapshots cost USD 0.01 each |
| US Equity and Options Add-On Streaming Bundle | USD 4.50 (requires the bundle above) | Consolidated real-time streaming from all US exchanges |
| IBKR Currencies (IDEALPRO forex) | Fee waived | Forex quotes (needs the Forex trading permission) |

Our course account uses the two paid US bundles. You can start without them: the free US streaming data is enough for
the market lessons in TWS. For data through the API, IBKR states that a paid subscription is generally required for
live data and that the account must meet a minimum equity (USD 500 on 2026-10-21) in addition to the subscription
cost; we cover what the API needs in module 4.

To subscribe: **Settings** → **Market Data Subscriptions** → **Configure** (or the gear) → choose your region (North
America) → tick the bundles → continue and sign. Subscriptions are billed per calendar month and are not pro-rated.

## Checklist

- [ ] Subscriber status: non-professional (if it is true for you)
- [ ] Market Data API Acknowledgement signed
- [ ] Market data shared with the paper account
- [ ] Forex trading permission requested and approved
- [ ] (Optional) US bundles subscribed
- [ ] Logged out of TWS and back in on the Paper Trading tab after the changes
