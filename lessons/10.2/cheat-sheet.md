# Lesson 10.2 cheat sheet: Order management that survives

## The words

| Word | Meaning |
|---|---|
| **Bracket** | One entry order (the parent) plus two children: a stop below and a target above. The children are one-cancels-other (OCA): when one fills, IB cancels the other. The parent is held back (`transmit=False`) until the last child is sent, so nothing can fill without its stop |
| **Order reference (`orderRef`)** | A text label IB stores with every order and execution. Ours: `live:<strategy>:<symbol>:<session date>:<signal bar HHMM>`, for example `live:opening_range_breakout:QQQ:2026-10-22:0945` |
| **Idempotent** | Doing it twice has the same effect as doing it once. Before sending, the engine looks for the ref; if it is already there, nothing is sent |
| **Partial fill** | Only part of the order filled. The stop and target are resized to the shares that actually filled |
| **Reject** | IB refuses the order, with a code and a reason (error 110: the price is not a multiple of the tick) |
| **Pre-trade risk check** | Limits checked before an order leaves the program, outside the strategy |
| **Kill switch** | One command that writes a STOP file, cancels our orders, sells our positions and keeps the engine from starting |
| **permId** | IB's permanent order ID. It stays the same across sessions; an order from an earlier session shows `orderId` 0 |

## What survives a restart

1. The runner writes its intent (`pending_entry`, `sent_refs`) to `state.json` **before** the first order goes out.
2. The bracket is sent; all three orders carry the ref.
3. If the runner dies now, the next start runs reconcile, which asks IB what happened:

| What IB did while we were down | What reconcile does |
|---|---|
| The buy is still working | Waits, then cancels what is left |
| Filled | Takes over the position, with the average price and the order IDs |
| Stopped out, or never filled | Holds nothing (a stop-out is logged, but not written to `trades.jsonl`) |
| Filled in part | Replaces children that are too big with ones sized to what filled |
| IB has the ref, the state file doesn't | Halts, so a person can look |

## The limits (`live/risk_limits.yaml`)

| Limit | In the lesson |
|---|---|
| `max_shares`, `max_position_value` per symbol | SPY and QQQ: 10 shares or $8,000 (about 0.8% of the ~$1M paper account) |
| `max_trades_per_day` | 4 (distinct entry refs bought or resting today) |
| `daily_loss_limit` | $500 under the day's first net-liquidation reading |
| A symbol not listed | Can't be bought at all |

- Checked in `Broker.place`, the only way to place an order, before every order leaves the program.
- `Executor.size` clamps to the limits first, so a signal gets a smaller order instead of a refusal.
- Only buys can be refused. Sells and cancels always go out, so a limit can never block a stop or the kill switch
  (and also can't stop an accidental short sale).
- The end-of-session flatten from Lesson 10.1 stays: flat 10 minutes before the close.

## The commands

| Command | What it does |
|---|---|
| `uv run -m live.proof` | One-share bracket on SPY, then sells it and checks flat. Run it again the same day: 0 orders sent |
| `uv run -m live.proof --keep --name <name>` | Opens 1 SPY with its stop and target and leaves it (a new name = a new ref) |
| `uv run -m live.kill` | STOP file first, cancel every order whose ref starts with `live:`, sell our positions, report flat. Safe to run twice |
| `uv run -m live.kill --clear` | Removes the STOP file before the next paper session |
| `uv run -m live.probe reject` | Makes IB refuse a 1-share buy (a half-cent price far under the market): error 110, logged once, no retry |
| `uv run -m live ... --port 7497` | The runner through another paper port (for the relay drill). Only paper ports are accepted |

Exit codes: the runner exits 3 when it refuses to start because STOP exists; a proof that a limit refused exits 2.

## What happens when it goes wrong

| Failure | How it's handled | Shown on |
|---|---|---|
| Same entry sent twice (restart, retry) | Ref checked in open orders, today's executions and the state file; a hit sends nothing | Paper (proof run twice) |
| Runner dies between send and fill | Intent on disk first; reconcile adopts what IB did | Fake IB only |
| Partial entry fill | Children resized; after a restart, too-big children replaced | Fake IB only |
| Oversized order | Clamped by the limits; a refusal is logged and the signal skipped | Fake IB; the STOP refusal on paper |
| Need to stop everything | `live.kill`: flat, buys refused, runner won't start | Paper, by hand |
| IB refuses an order | Detected from IB's error on the order (ib_async reports 110 as Cancelled, not Inactive); logged once with code and reason, never retried, runner halts; a refused exit puts the stop back | Paper (`live.probe reject`) |
| Connection drop | Up to 6 reconnect tries 10 s apart, then the same reconcile as at start: carry on if clean, halt otherwise | Paper (a short and a long outage) |

Not shown on the real Gateway: a drop while holding a position, a drop in the middle of an order, a real partial fill,
and a Gateway restart (which may surface as a different error than a cut relay).

## Three rules

1. Never retry a reject blindly.
2. Never assume a fill.
3. After any doubt, IB is the source of truth: reconcile before trading again.

## The numbers in the video

- A1: 484 tests (`358beb4`, about 15 minutes); proof run 1: bought 1 SPY at 762.32, sold at 762.30, 4 orders, flat;
  run 2: 0 orders; quiet console in about 3 minutes (`8fb3bbd`, 134 live tests).
- C1: 523 tests (`b268b49`, about 9 minutes); by hand: bought 1 SPY at 761.59, stop 746.80, target 777.28; kill switch:
  flat; runner exit code 3; buy refused while STOP exists.
- B1: 540 tests (`2680378`), error 110 on paper (`282c121`), the reconnect fix (`1965ac6`, 192 live tests); outage A:
  3 failed attempts, back, reconcile OK; outage B: 6 failed attempts, HALT, clean exit.

Prices are delayed paper prices from October 2026. The reference price in the proof is the latest 5-minute bar, which
runs 15-20 minutes late with delayed data and may still be filling in (Lesson 16.1 makes the engine decide only on
settled bars).
