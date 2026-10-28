"""Cleanup for red team (3): sell the 1 SPY share the direct script bought. PAPER ONLY (port 4002, client ID 99, DU* account).

Sells at most what is held (never more than 1), so it can never open a short.
"""

import sys

from ib_async import IB, MarketOrder, Stock

HOST, PORT, CLIENT_ID = "127.0.0.1", 4002, 99

ib = IB()
ib.connect(HOST, PORT, clientId=CLIENT_ID, timeout=10)
try:
    accounts = ib.managedAccounts()
    if not accounts or not all(a.startswith("DU") for a in accounts):
        sys.exit(f"ABORT: not a paper account {accounts}; nothing sent")

    held = int(sum(p.position for p in ib.positions() if p.contract.symbol == "SPY"))
    print("SPY held:", held)
    if held < 1:
        sys.exit("nothing to sell")

    contract = Stock("SPY", "SMART", "USD")
    ib.qualifyContracts(contract)
    order = MarketOrder("SELL", min(held, 1))
    order.orderRef = "redteam:direct:SPY:cleanup"
    trade = ib.placeOrder(contract, order)
    for _ in range(20):
        ib.sleep(1)
        if trade.isDone():
            break
    print("status:", trade.orderStatus.status, "filled:", trade.orderStatus.filled,
          "avg fill price:", trade.orderStatus.avgFillPrice)
finally:
    ib.disconnect()
