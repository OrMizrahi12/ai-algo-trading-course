"""Red team (3): buy 1 SPY share straight through ib_async, skipping the MCP server, the hook and the lab's Broker.

PAPER ONLY: connects to 127.0.0.1:4002 (the IB paper Gateway) with client ID 99, and aborts before sending anything if
the account is not a paper account (IB paper account numbers start with "DU").
A market order = buy at whatever price is available right now. Prices are delayed data, but the order is real (paper).
"""

import sys

from ib_async import IB, MarketOrder, Stock

HOST, PORT, CLIENT_ID = "127.0.0.1", 4002, 99
FILL_TIMEOUT_S = 20

ib = IB()
ib.connect(HOST, PORT, clientId=CLIENT_ID, timeout=10)
try:
    accounts = ib.managedAccounts()
    print("accounts:", accounts)
    if not accounts or not all(a.startswith("DU") for a in accounts):
        sys.exit(f"ABORT: not a paper account {accounts}; nothing sent")

    contract = Stock("SPY", "SMART", "USD")
    ib.qualifyContracts(contract)
    order = MarketOrder("BUY", 1)
    order.orderRef = "redteam:direct:SPY"
    trade = ib.placeOrder(contract, order)
    print("order sent, no stop, no target, no risk check")

    for _ in range(FILL_TIMEOUT_S):
        ib.sleep(1)
        if trade.isDone():
            break

    print("status:", trade.orderStatus.status, "filled:", trade.orderStatus.filled,
          "avg fill price:", trade.orderStatus.avgFillPrice)
    for fill in trade.fills:
        print("fill:", fill.execution.shares, "@", fill.execution.price, "at", fill.time)

    if not trade.isDone():
        ib.cancelOrder(order)
        ib.sleep(1)
        print("not filled in", FILL_TIMEOUT_S, "s; cancelled. status:", trade.orderStatus.status)
finally:
    ib.disconnect()
