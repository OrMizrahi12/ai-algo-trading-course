# Rejects and messages from the lesson

Every refusal in the lesson was real, and each one teaches something about how IB handles orders.

| Code / message | Where | What it means | What we did |
|---|---|---|---|
| 354 Requested market data is not subscribed ... Delayed market data is available | Gateway, while getting the SPY reference price | No live data subscription; delayed quotes are available (as in Lesson 4.3) | Nothing: the script fell back to delayed data |
| tif defaulted to DAY | Gateway, the first run | IB filled in the order's time in force for us | The script sets `tif="DAY"` explicitly |
| 161 Cancel attempted when order is not in a cancellable state | Gateway, the follow-up run | A cancel reached IB for an order that was no longer cancellable (already filled or cancelled) | Harmless here |
| 10311 (direct routing) | Gateway, flatten_all, closing SPY | The position reports its fill venue (ARCA). Reusing it for the closing order is direct routing, which IB rejects | Stocks now always close through SMART |
| 10318 (fractional units) | Gateway, flatten_all, closing EUR | IDEALPRO does not accept fractional currency units | Forex now closes in whole units; 0.68 EUR stays |
| 10168 Requested market data is not subscribed. Delayed market data is not enabled. | TWS, getting the SPY quote | TWS gave the API no SPY quotes. TWS showed delayed quotes on screen, but they did not reach the API | Claude stopped instead of guessing a price; we gave it the close of the last 5-minute historical bar |
| Order Precautions dialog: "Would you like to deactivate these precautions for all API Orders?" | TWS | TWS's safety checks for API orders (price percentage, total value limit, size limit and more). An API order waits on this dialog until someone answers | We answered **No** and kept the checks |
| 354 (TWS): "submit an order without having market data for this instrument ... Precautionary Settings" | TWS, both limit buys | TWS's no-market-data precaution rejected the orders: order 11 (763.55) and order 12 (764.55) Cancelled, nothing filled, the sell skipped | Nothing: the setting is yours to decide |

## Reading TWS's Orders panel

- An API order appears in the Activity > Orders panel as soon as TWS receives it.
- A **Transmit** button on a row means the order is in TWS but not yet sent to IB.
- A red mark on the left means the order is no longer working (here: cancelled).
- Orders you typed by hand in TWS belong to client 0; orders from `orders.py` carry its client ID (5 on TWS).

## The precaution is a choice

TWS can bypass the Order Precautions for API orders (Global Configuration > API > Precautions), and it can stop
asking about orders without market data. On a paper account that's a legitimate choice for testing, but make it
knowingly: these checks are the last line of defense against a buggy script that sends an order far too big, or far
from the market. In the lesson, Claude noticed the setting, explained it, and said: "That setting is yours, so I
haven't tried to get around it."

## Sources

- TWS API, order precautions: https://www.interactivebrokers.com/docs/tws-api/doc/tws-settings/order-precautions
- TWS API, order placement considerations (rejections to handle in code):
  https://www.interactivebrokers.com/docs/tws-api/doc/orders/place-order/order-placement-considerations
- TWS API, client ID 0 and the master client ID:
  https://www.interactivebrokers.com/docs/tws-api/doc/order-management/client-id-0-and-the-master-client-id
- TWS API, delayed market data: https://www.interactivebrokers.com/docs/tws-api/doc/md/delayed-data
