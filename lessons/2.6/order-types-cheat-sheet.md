# Order types cheat sheet

Lesson 2.6 · TWS, Mosaic layout, **paper** account, free delayed data. Every step below is what TWS showed in the
lesson. Dialogs can change between TWS versions: if one looks different, look for the same words nearby.

## Building any order (the Order Entry panel, top left)

1. Pick the symbol (type it, then pick the stock from the list).
2. Click **Buy** (the panel turns blue) or **Sell** (it turns red).
3. Set the quantity, the order **type**, the price field(s) the type needs, and the time in force (**TIF**).
4. **Submit** opens a confirmation. Read it: side, quantity, type, prices, estimated commission, and on the right what
   changes in your account (margin, position). Then **Transmit** (or **Override and Transmit** when TWS shows a
   warning, such as "no live market data" on free delayed data).
5. The order appears in **Orders** (the Activity panel). Working orders also show as lines on the chart.

## The order types

| Type (TWS code) | What it says | Prices you set | The catch |
|---|---|---|---|
| Market (MKT) | Fill me now, at the best price available | none | You don't choose the price. On delayed data the fill can be far from the quote you see |
| Limit (LMT) | Fill me only at this price or better | limit price | It may never fill. A buy limit below the market waits for the price to come down |
| Stop (STP) | When the price trades at the stop, become a market order | stop price | Once triggered it's a market order: in a fast move the fill can be worse than the stop |
| Stop-limit (STP LMT) | When the price reaches the stop, become a limit order | stop price + limit price | In a fast drop the price can jump past the limit, and then it doesn't fill at all |
| Trailing stop (TRAIL) | A stop that follows the price up by a fixed amount, and never moves down (for a sell) | trailing amount | It fires on any pullback of that size, noise included |
| Bracket | An entry plus two exits: a profit taker (limit) and a stop loss (stop) | entry, target, stop | The two exits are an OCA group: only one of them can fill |

## Time in force

- **DAY**: anything not filled expires at the close.
- **GTC** (good till cancelled): survives the close. TWS still gave it an automatic cancel date (in the lesson, about
  five months ahead), so GTC is not forever. Read the date in the dialog TWS shows after Transmit.

## Working with orders in the Orders list

- **Change a price:** click the price in the order's row and type the new one. The row turns orange with a yellow
  **U**: the change is on your screen only. Click the **U** to send it. Until then the broker holds the old price.
- **Cancel:** the **Cancel** button on the row. The status icon turns pink (cancel requested), then the row greys out.
- **Bracket rows** are numbered as a family: 1 for the parent, 1.1 for the profit taker, 1.2 for the stop loss.
  Cancelling the parent cancels all three.

## The bracket, step by step (lesson: Apple, 10 shares)

1. **Buy**, quantity, type **LMT**, limit price (lesson: 344.00, below the market at about 345.70).
2. Open the advanced part of the panel. Under *Attach Stop Loss, Profit Taker, Bracket*, tick **Bracket**.
3. Two child orders appear with prices filled in. Set the **profit taker** (a limit sell above the entry, lesson 348)
   and the **stop loss** (a stop sell below it, lesson 341).
4. **Submit**: the confirmation lists all three orders. Both children carry the same **OCA group** number. OCA means
   *one cancels all*: if one exit fills, the other is cancelled.
5. **Transmit**. TWS previews each child order. It may then ask about its *Price Management Algo*; in the lesson we chose
   **Use on this order**, so nothing is saved for later.

## Positions, fills and the account

- **Portfolio:** your positions, average price (fill plus commission spread over the shares), and **Realized** P&L.
- **Trades tab** (Activity panel): the activity log, one line per fill, with price and commission.
- **Account > Account Window:** Net Liquidation (what the account is worth if you closed everything), Cash, margin
  requirements, Excess Liquidity, **Buying Power**.
- **Close a position:** right-click the row in the portfolio > **Close**. TWS fills in the opposite order (for a short of
  10: buy 10); choose the type, check the confirmation, Transmit.
- **Account > Trade > Close All Positions** closes everything at once (greyed out when you hold nothing).

## Short selling

- **Sell** shares you don't own. The confirmation shows the position going from 0 to minus the quantity, and the margin
  going up: a short needs margin.
- Cash goes up by the sale's proceeds, but that money isn't yours to keep: you owe the shares.
- To close it, buy the shares back. A short **loses when the price rises**. With real money, a short can also pay a fee
  to borrow the shares, which for some stocks gets expensive.

## Before you go: the honest bits

- Paper fills are simulated: a live account fills differently, and the paper server can be slow.
- Delayed data is about 15 minutes old; fills come at the real price of the moment.
- Buying power is what the account lets you buy, not what you should risk.
