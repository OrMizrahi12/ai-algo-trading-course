# TWS or IB Gateway?

Both come from Interactive Brokers (IBKR), and both serve the same API (the door programs use). IBKR's API
documentation says that, from the point of view of an API program, the two are identical, and that the Gateway uses
about 40% fewer resources.

| | Trader Workstation (TWS) | IB Gateway |
|---|---|---|
| What you see | The full trading screen: charts, watchlists, order tickets | A login window and a small status window |
| Good for | Looking: charts, manual checks, what your program just did | Running code: programs connect and trade through it |
| Resources | More (it draws everything) | About 40% fewer |
| API settings | Global Configuration → API → Settings | Configure → Settings → API → Settings |
| Socket clients | A box you must tick ("Enable ActiveX and Socket Clients") | Always on |

In this course, our programs talk to the **Gateway**. TWS stays useful for looking at the market and checking what
the programs did.

## The four ports

A socket port is a numbered door on your computer. A program connects to the port of the app it wants to talk to.

| | Paper (simulated) | Live (real money) |
|---|---|---|
| TWS | **7497** | 7496 |
| IB Gateway | **4002** | 4001 |

This course only ever uses the paper ports. Our code connects to **4002**.

## One session per username

An IBKR username can be logged in in only one place at a time. If TWS is open with your paper username and you log
in to the Gateway with the same username, IBKR shows "Existing session detected" and asks whether to disconnect the
other session.
