# Order types, with the lesson's numbers

Everything `orders.py` sent in the lesson, one share of SPY at a time, on the paper account. Prices are from
21 October 2026, about 15 minutes before the close, and came from delayed data (about 15 minutes old).

## The paper guard comes first

```python
PAPER_PORTS = {7497, 4002}          # TWS paper, Gateway paper
...
accounts = ib.managedAccounts()
if not accounts or not all(a.startswith("DU") for a in accounts):
    ib.disconnect()
    raise RuntimeError(f"Refusing to trade: accounts {accounts} are not all DU paper accounts")
```

Paper accounts start with **DU**. With Read-Only API off, this check is what keeps a script from ever trading a live
account by mistake.

## What-if order

A test order: IB answers with the margin and commission the order *would* need, and places nothing.
`ib.whatIfOrder(contract, order)` returns an `OrderState`.

- Lesson (Gateway): one share of SPY would add about **$85** of initial margin (the cash set aside for the
  position) and cost about **$1.00** in commission.
- Lesson (TWS): initial margin change **+84.14**, commission about **1.00 USD**.

## Market order

Buy or sell now, at the best price available. `MarketOrder("BUY", 1)`.

- Lesson: filled **1 share at $772.98**, commission **$1.00**.

## Limit order

Buy or sell only at your price or better. A buy limit below the market waits until the price comes down to it.
`LimitOrder("BUY", 1, price)`.

- Lesson: a buy limit 5% below the market, at **$734.13**, rested, and the script cancelled it with
  `ib.cancelOrder(order)`.

## Bracket order

An entry with a take-profit and a stop-loss attached. The exits only become active when the entry fills, and once one
exit fills IB cancels the other.

- `ib.bracketOrder("BUY", 1, entry, takeProfitPrice=..., stopLossPrice=...)` returns three orders. The two exits
  carry `parentId` = the entry's order ID.
- **transmit**: every order goes to IB as soon as you place it, unless `transmit=False`. The entry and the
  take-profit are placed with `transmit=False`; the stop-loss goes last with `transmit=True`, which releases all three
  together. Without that, the entry could fill before its stop-loss exists.
- Lesson: buy limit **$772.67** (a little under the market, so it waited), take-profit **$780.40**, stop-loss
  **$764.94**, order IDs 15 to 17.

## Trailing stop

A stop that follows the price up by a fixed distance or percent, and never moves down. The first version of
`orders.py` placed one for the share we held:

```python
trail = Order(action="SELL", orderType="TRAIL", totalQuantity=1, trailingPercent=1.0, tif="DAY")
```

- Lesson: a 1% trailing stop, order 18. Claude then pointed out that the trailing stop and the bracket's exits both
  cover the same share, so the next request cancelled it and used an OCA group instead.

## OCA group (one-cancels-all)

Several orders in one named group: when one fills, IB cancels the others. `ib.oneCancelsAll(orders, group, ocaType)`
sets `ocaGroup` and `ocaType` on each order.

| ocaType | Meaning |
|---|---|
| 1 | Cancel the other orders, with block (used in the lesson) |
| 2 | Reduce the other orders' size, with block |
| 3 | Reduce the other orders' size, without block |

- Lesson: a limit sell at **$780.72** and a stop sell at **$765.26** for the one share, same `ocaGroup`,
  `ocaType=1`. Step 5 of the main run now uses this group instead of the trailing stop.

## Time in force (tif)

How long an order stays alive. `DAY` orders expire at the end of the trading day. In the first run IB answered that
the time in force had defaulted to DAY; the script now sets `tif="DAY"` on every order, on purpose.

## Cash quantity (forex)

For forex you can say how much money to spend instead of how many units to buy: `order.cashQty = 20000` with a
quantity of 0. The API supports cash-quantity orders only for forex and crypto.

- Lesson: buy EURUSD with **20,000 USD** on IDEALPRO, IB's forex venue: filled **17,804.68 EUR at 1.1233**,
  commission **$2.00**. The amount isn't round because cashQty converts dollars into euros. (IB briefly showed
  PendingCancel and "remaining 3,560" before the final Filled status.)
- This course trades US stocks and ETFs; the forex order is only a contrast.

## Marketable limit

A limit order priced through the market (a buy limit above the ask, a sell limit below the bid). It fills right away
like a market order, but never worse than its limit. The TWS stage used buy limits at the reference price **+0.50**.

## Flatten

Cancel every open order and close every position. `flatten_all()`:

1. `ib.reqGlobalCancel()` cancels every open order of the account.
2. For each position, a market order the other way: sell what you hold, buy back what you're short.
3. Stocks are routed through **SMART**, forex closes in **whole units** (see `rejects-and-messages.md`).

- Lesson, after the fix: SPY sold at **$773.16**, EUR sold 17,804 at **1.12325**, open orders empty. **0.68 EUR**
  stayed: too small to close on IDEALPRO, worth pennies.

## Sources

- TWS API, the Order object (orderType, auxPrice, trailingPercent, parentId, ocaGroup, ocaType, transmit, tif):
  https://www.interactivebrokers.com/docs/tws-api/ref/order
- IBKR, bracket orders: https://www.interactivebrokers.com/docs/general/order-types/complex-orders/bracket-orders
- IBKR, one-cancels-all (OCA): https://www.interactivebrokers.com/docs/general/order-types/complex-orders/one-cancels-all
- TWS API, what-if orders: https://www.interactivebrokers.com/docs/tws-api/doc/orders/test-order-impact-what-if
- IBKR, forex cash quantity orders: https://www.interactivebrokers.com/docs/general/order-types/basic-orders/forex-cash-quantity-order
