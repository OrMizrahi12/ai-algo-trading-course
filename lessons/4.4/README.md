# Student kit: Lesson 4.4, Orders through the API

Module 4: IB Gateway and the API · AI Algorithmic Trading with Claude Code and Interactive Brokers

In this lesson we switched off Read-Only API in IB Gateway, so our programs can place orders on the paper account.
Claude wrote `orders.py` for the Trading Lab: a script that refuses anything but a paper account, then places a
what-if test, a market buy, a limit buy that it cancels, a bracket and a trailing stop, all on one share of SPY. We
replaced the overlapping trailing stop with an OCA group, tried one forex order, and added `flatten_all()`, which
cancels every open order and closes every position. Its first run met two real rejects, both fixed. Last, we sent
orders from the same script to TWS and watched them arrive, and meet TWS's no-market-data precaution.

## What's in this kit

| File | What it is |
|---|---|
| `prompts.md` | The four requests typed in the lesson, ready to copy, plus the pause-and-try exercise |
| `order-types.md` | What-if, market, limit, bracket (`parentId` and `transmit`), trailing stop, OCA, time in force, cash quantity, marketable limits and flattening, with the lesson's real numbers |
| `rejects-and-messages.md` | Every IB and TWS message from the lesson (354, 10168, 161, 10311, 10318, the Order Precautions dialog) and what to do about each |
| `trading-lab/orders.py` | The script at the end of the lesson: the paper guard, the five-step SPY run with OCA exits, `followup`, `flatten` and the TWS stage |

## Before you start

- You need the Trading Lab from Module 3 and IB Gateway from Lesson 4.1, logged in to your **paper** account, API
  socket port **4002**.
- In the Gateway: **Configure > Settings > API > Settings**, untick **Read-Only API**, then OK. Do this only on your
  paper login. With Read-Only off, any program connected to the Gateway can place orders.
- `orders.py` refuses to run unless the port is a paper port (4002 or 7497) and every account starts with **DU**
  (the prefix of paper accounts). Keep that check in every script that can trade.
- Client IDs: `orders.py` uses **4** with the Gateway and **5** with TWS. Pick IDs your other scripts don't use at
  the same time.
- The TWS stage needs `pandas` (`uv add pandas` if your project doesn't have it yet).
- Run the order steps while the US market is open (9:30 to 16:00 New York time). Outside those hours a market order
  waits for the next session, and day orders expire at the close.

## Run it

From your `trading-lab` folder, with the Gateway running (or TWS paper for the last line):

```bash
uv run orders.py            # the five-step SPY run: what-if, market buy, limit + cancel, bracket, OCA exits
uv run orders.py followup   # cancel trailing stops, OCA exits, the EURUSD cashQty order, then flatten_all()
uv run orders.py flatten    # only flatten_all(): cancel every open order, close every position, print what's left
uv run orders.py tws        # against TWS paper (port 7497, client ID 5)
```

Every one of these places real orders on your paper account. Check the open orders and positions it prints at the
end: after `flatten` both should be empty.

## Try it yourself

1. Untick Read-Only API in your paper Gateway.
2. Ask Claude for `orders.py` with the what-if, market, limit, bracket and OCA steps and a flatten-all function
   (the prompts are in `prompts.md`; change them freely).
3. Run it during market hours, then run the flatten step.

You're done when the open orders and positions print empty at the end. Your prices, fills, order IDs and Claude's
wording will differ from the video; the method is what matters.

## Good to know

- In the lesson, the trailing stop from the first run was later cancelled and replaced by the OCA exits, so the
  final `orders.py` no longer places a trailing stop. `order-types.md` shows the trailing stop line from the first
  version.
- The EURUSD order is only a contrast: orders for other markets go through the API the same way. This course trades
  US stocks and ETFs.
- On TWS, the API orders were cancelled by TWS's "no market data" precaution, and nothing filled. Claude did not try
  to get around the setting: that choice is yours. The engine we build later talks to the Gateway, where these orders
  went through.
- A tiny forex remainder (0.68 EUR in the lesson) can't be closed on IDEALPRO, which doesn't take fractional units.
  On a paper account it can stay.
- Paper (simulated) account only. Educational content, not financial advice.
- Menus, versions, prices and limits were current at the time of recording (October 2026).
