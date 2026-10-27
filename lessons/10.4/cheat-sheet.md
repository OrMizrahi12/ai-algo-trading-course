# Lesson 10.4 cheat sheet: Journal and dashboard

## The words

| Word | Meaning |
|---|---|
| **Trade journal** | The permanent record of what happened, trade by trade: every signal, order and fill, with its commission. In the Lab: `data/live/journal.sqlite3` (kept out of Git) |
| **SQLite** | A database that is one file on disk, with no server. Python has it built in (`import sqlite3`) |
| **Equity curve** | The account's value over time. The journal keeps one snapshot per account per New York day |
| **Drift** | The gap between what the backtest says should have happened and what really did: prices, timing, costs |
| **Entry ref** | The `orderRef` the engine puts on an entry's orders, for example `live:proof_entry:SPY:2026-10-22:0930`. It ties the buy, the sell and their fills together |
| **Idempotent** | Safe to run twice: a second import adds nothing, because rows are keyed by IB's own ids |

## One writer, many readers

- **The engine writes.** `Runner` records each signal and syncs orders and fills from IB after every poll. A failed
  journal write is logged and trading goes on.
- **Everything else only reads:** your queries, the drift check, the dashboard. The dashboard opens the file read-only
  (`mode=ro`), never through the engine's `Journal` class (which creates tables), and never selects the account column.
- **The import** (`uv run -m live.journal_import`) is read-only toward IB (client ID 7) and copies today's orders, fills
  and a snapshot into the journal. IB lists only the current day's executions, so run it that day.

## The tables (`live/journal.py`)

| Table | One row per | Worth knowing |
|---|---|---|
| `signals` | strategy decision | what was done (bought, sold, skipped, not filled, dry run) and how late the bar was seen |
| `orders` | IB order (its `perm_id`) | IB reports a finished order with quantity 0, so quantity and average price come from its fills |
| `fills` | execution (its `exec_id`) | `commission` stays empty until IB's report arrives, never a made-up 0 |
| `snapshots` | account per New York day | the first and the latest net liquidation |
| `entry_pnl` (a view) | entry ref | bought, sold, gross, commission, net, status. Fills with no `live:` ref are grouped as `(not ours)` |

## Queries

```bash
uv run python - <<'PY'
import sqlite3
db = sqlite3.connect("file:data/live/journal.sqlite3?mode=ro", uri=True)
for row in db.execute("SELECT time_et, side, shares, price, commission, entry_ref FROM fills ORDER BY time_utc"):
    print(row)
for row in db.execute("SELECT entry_ref, bought, sold, gross_pnl, commission, net_pnl, status FROM entry_pnl ORDER BY day, entry_ref"):
    print(row)
PY
```

If the `sqlite3` command-line tool is installed, `sqlite3 -readonly data/live/journal.sqlite3` runs the same SQL.

## What the journal showed on our computer (one day, paper)

| | Model (`CostModel`) | Real (IB) |
|---|---|---|
| Commission, one share, one side | 1¢ | $1.00 (IB's minimum per order) |
| Proof round trip, total cost | 5¢ | $2.04 |
| First kill switch demo, total cost | 5¢ | $2.12 |
| Sells | no fee | about 1.6¢ more (looks like a sell-side regulatory fee; IB doesn't itemise it) |
| Each new bar seen | at once | 10.5 to 11 minutes after it closed (free delayed data) |

The three one-share engine trades moved a few cents either way and each lost about $2 net. The 11-share manual trade made
+$5.58 gross, paid $4.17 commission and kept +$1.41: commission took about 75% of the gross.

## What it means for testing

- A cost is a **fixed fee plus a per-share part**. At a small size the fixed part dominates; a per-share-only model
  understates it (about 11 times for a 10-share trade, about 100 times for one share).
- **Gross profit alone says nothing.** The average gain per trade has to clearly beat the real round-trip cost.
- **Measure, don't assume.** Check your backtest's costs against what IB really charged, with the minimum per order.
- **The plan doesn't move.** A test that is already written down (here H3) runs with the costs it was registered with.
  The finding goes into the research journal as a new idea to test afterwards (`idea-m.md`).
- **Four trades prove nothing about any strategy.** They were plumbing tests.

## The dashboard (`dashboard/`, Lab commit ce492b2)

| File | What it does |
|---|---|
| `dashboard/data.py` | Reads the journal read-only: equity per day, open positions, closed trades (gross, commission, net), stats |
| `dashboard/server.py` | Standard-library web server on 127.0.0.1 only; refuses any Host header that isn't localhost and any write request |
| `dashboard/index.html` | The page: stats, the equity curve, open positions, trades newest first. Refreshes every 30 s |
| `dashboard/__main__.py` | `uv run -m dashboard [--port 8765] [--db PATH]` |
| `tests/test_dashboard.py` | The P&L maths, a fake account ID never reaching any output, the file can't be written, other hosts refused |

It is its own process, with no IB connection and no client ID, so it can run while the engine trades.
