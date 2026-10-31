# Student kit: Lesson 2.3, The map of markets, in TWS

Module 2: Markets from zero, on a real trading platform · AI Algorithmic Trading with Claude Code and Interactive Brokers

In this lesson you walk the map of markets in Trader Workstation (TWS) on the paper account: a stock and its other
listings, an ETF that trades like a stock, a micro futures contract with its expiry and multiplier, crypto that our
account can't trade, forex rows with no data, and an option chain of calls and puts. Then you read two contract spec
sheets (a stock and a futures contract), put every market's trading hours on one clock, and turn on the extended hours
on a 5-minute chart. The course trades US stocks and ETFs from here on; the rest of the map is context.

## What's in this kit

| File | What it is |
|---|---|
| `market-map.md` | The seven kinds of markets on one page: what you own, where it trades, hours, size and leverage, and what our paper account can do with each |
| `tws-walkthrough.md` | The lesson's steps in TWS, click by click, so you can repeat them on your own paper account |

## Try it yourself

1. In TWS, logged in to your **paper** account, click an empty row of a watchlist, type a symbol (for example `AMD`)
   and press Enter. Read the list: the stock, its options, its other listings.
2. Right-click a stock and open its **Description**. Note the exchange, the currency, the regular session and the total
   available hours. Do the same for an ETF (for example `DIA` or `SPY`).
3. On a 5-minute chart, open **Edit > Chart Parameters**, tick **Show data outside of regular trading hours** and click
   OK. Find the 9:30 open.
4. You're done when you can name every market on the map, its hours, and what our paper account can and can't trade.

## Remember

- Everything in this course runs on a **paper (simulated) account**. Nothing here is bought, enabled or subscribed.
- Your paper account number is private. Don't post it in screenshots or forums.
- Prices, margins, listings and menus change. What your own TWS shows today wins over this kit.
- This is educational content, not financial advice. Futures, options and crypto are shown for context; this course
  doesn't trade them.

Next lesson: 2.4, Trading styles on real charts.
