# Lesson 4.2 cheat sheet: the first connection

## Where your code connects

| | Paper (this course) | Live (never in this course) |
|---|---|---|
| IB Gateway | `127.0.0.1`, port **4002** | port 4001 |
| TWS | `127.0.0.1`, port **7497** | port 7496 |

- **Read-Only API** on (Lesson 4.1), and `readonly=True` in `connect_test.py`: the session can read data but can't
  place orders.
- Paper account numbers start with **DU**. Both scripts stop unless every account starts with `DU`.
- **One login at a time**: one IBKR username can be logged in in one place. TWS and the Gateway with the same paper
  username knock each other out ("EXISTING SESSION DETECTED"). Use one of them.

## The account summary, in plain words

| Value | What it means |
|---|---|
| Net liquidation | What the account would be worth if everything were sold right now |
| Total cash | Cash in the account |
| Buying power | How much you could buy, including margin (borrowed money); much larger than your cash |
| Positions | What you hold; an empty list on a fresh paper account |

On the lesson's account, net liquidation was cash plus about $1,770 of accrued interest (earned, not paid out yet).

## Client IDs

- Every connection to the Gateway gives a **client ID**, a number that names that program. Each ID is its own seat.
- Two programs connected at the same time with the **same** ID: the newcomer is rejected with error **326**
  ("Unable to connect as the client id is already in use"). The first connection keeps working.
- With `ib_async` the newcomer only sees a `TimeoutError`. If a connect ever times out, look for an old program still
  holding that client ID.
- Different IDs (7 and 8 in the lesson) connect side by side. The Gateway's window shows a tab per client ID.
- In the Lab: `connect_test.py` uses client ID 1, `ibapi_hello.py` uses 2.

## Real errors, or just information?

| Message | What it is | Meaning |
|---|---|---|
| 2104 | Information | Market data farm connection is OK |
| 2107 | Information | Historical data farm is idle; it wakes up when you ask for history (normal, yellow in the Gateway) |
| 2158 | Information | Sec-def (contract lookup) server connection is OK |
| 326 | Real error | Client ID already in use; the connection fails |
| `ConnectionRefusedError` (111) | Real error | Nothing is listening on that port: wrong port, or the Gateway is closed or logged out |

Codes 2100 to 2199 are warnings: status notes about IBKR's data connections, not failures. Filter on the code, not on
the fact that an error event fired.

## The Stop hook fix

Claude Code sends a Stop hook `stop_hook_active: true` when Claude is already continuing because a Stop hook sent it
back. The fixed `require_commit.py` returns 0 (let Claude stop) in that case:

```python
# Already blocked once this turn: let Claude stop so the hook can't loop forever.
if payload.get("stop_hook_active"):
    return 0
```

It still blocks the first stop while there's uncommitted work, so it still enforces a commit; it just can't loop.

## `ib_async` or `ibapi`

| | `ib_async` (what the Lab uses) | `ibapi` (IBKR's official client) |
|---|---|---|
| Made by | A community project | IBKR, in the TWS API download |
| Where from | `uv add ib-async` (PyPI) | Only IBKR's download page; the PyPI copy is from 2020 |
| How it reads | Step by step: connect, ask, get the answer | Callbacks: you subclass `EWrapper` (answers) and `EClient` (requests), and run a reader loop in a thread |
| In the lesson | `connect_test.py`, 39 lines | `ibapi_hello.py`, 52 lines |

- A **callback** is a function you never call yourself: the library calls it for you when an answer arrives
  (`managedAccounts`, `nextValidId`, `accountSummary`, `accountSummaryEnd`, `error`).
- Wait for **`nextValidId`** before sending requests: it means the connection is ready.
- Don't call `disconnect()` from inside a callback: in the lesson that crashed `app.run()`. Run the reader loop in a
  thread and disconnect from the main thread.

## Links

- TWS API download (IBKR): https://www.interactivebrokers.com/docs/tws-api/doc/download-the-tws-api/introduction
- Establishing an API connection (IBKR): https://www.interactivebrokers.com/docs/tws-api/doc/connectivity/establishing-an-api-connection
- ib_async: https://github.com/ib-api-reloaded/ib_async
- Claude Code hooks (`stop_hook_active`): https://code.claude.com/docs/en/hooks
