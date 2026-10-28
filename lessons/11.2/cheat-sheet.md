# Lesson 11.2 cheat sheet: the agent loop

## Words

| Word | Meaning |
|---|---|
| Snapshot | Everything Claude needs for one decision, in one file (`data/desk/snapshots/<bar>.json`) |
| Decision contract | The exact JSON shape Claude's answer must have, enforced by `--json-schema` |
| Validator | Checks the answer is well formed and sane before anything else sees it; never repairs it |
| Risk seatbelt | Hard limits in code that Claude can't change (STOP file, risk limits, entry window, flatten, no overnight, paper guard) |
| Time budget | How long one bar may take before the decision is too old to use (120 s) |
| R | The money lost if the stop is hit: 1R = 1% of the account's net liquidation (total value) |
| Flatten | Selling the whole position, here 10 minutes before the close |
| Dry run | The whole loop for one bar, with no orders sent (`--once --dry-run`) |

## The loop, on every closed 5-minute bar

1. **Heartbeat** (`desk/heartbeat.py`): polls the lab's bar feed. Every bar newer than the last one handled gets exactly
   one model call; several bars at once are handled in order, none is skipped.
2. **Snapshot** (`desk/snapshot.py`): the last 100 five-minute, 60 fifteen-minute and 30 daily bars with indicators (EMA,
   RSI, ATR, Bollinger bands, VWAP), positions, open orders, the account, today's fills, the risk limits, the session
   block (bar age, minutes to the close, the flatten time) and the last journal entries. Facts only: no signal and no
   recommendation computed by Python.
3. **Claude** (`desk/model.py`): `claude -p` in the desk folder, the snapshot on stdin, the desk's
   `desk/instructions.md` as the system prompt, no tools (it can only answer).
4. **Validator** (`desk/decision.py`): the contract below.
5. **Gates and seatbelts** (`desk/gates.py`, `desk/seatbelts.py`): in order the STOP file, the rules for each action, the
   lab's risk limits. Python may refuse an unsafe decision; it never makes one.
6. **Executor** (`desk/execute.py`): only through the lab's order manager, on paper (a bracket: entry + stop + target).
7. **Journal** (`desk/journal.py`): one JSON line per bar in `data/desk/journal.jsonl`, even for a wait.

## The decision contract

```json
{"action": "buy | sell | close | wait", "size_r": 0, "stop": null, "target": null, "reason": "..."}
```

- Exactly these five keys, nothing else (`additionalProperties: false`).
- `size_r` from 0 to 2; above 0 for `buy` and `sell`.
- `stop` and `target`: a price or `null`. A `buy` needs a stop below the last close; a target, if any, above it.
- `reason`: not empty, at most 280 characters.
- `sell` only reduces a long position (no shorting); `close` sells it all.
- Anything invalid, late or missing becomes `wait`, and the journal records why (`invalid`, `model_failure`).

## The time budget (per bar)

| | |
|---|---|
| Whole bar | 120 s, from the moment it is handled |
| Claude | at most 75 s |
| A buy or a sell | skipped if less than 20 s remain ("budget exhausted") |
| A close | always tried: it reduces risk |
| Our dry-run bar | 5.32 s in all, `over_budget: false` |

## The seatbelts (they always win)

- **STOP file**: blocks buys; sells and closes still pass. Claude is told it's there.
- **Risk limits** (the lab's): daily loss, trades per day, shares and position value per symbol (ours: $500, 4 trades,
  10 SPY shares, $8,000). A buy is refused or cut to fit.
- **Entry window**: no buys on a bar older than 30 minutes, with the market closed, or in the last 10 minutes.
- **Flatten before the close**: on every poll, 10 minutes before the close (12:50 on half days), any long position is
  sold, even if the bar feed is down, without asking the model.
- **No overnight**: a position bought on an earlier day is sold at the next open.
- **Paper guard**: a non-paper account or a live port (7496, 4001) stops the desk.
- **Halts**: no known price, or a sale that can't be confirmed, halts the desk for a person to look.

Every time one acts: a `SEATBELT <name>` warning in the log and a journal record. Tags: `stop_file`, `risk_limits`,
`entry_window`, `flatten_before_close`, `overnight_carry`, `paper_guard`.

## A dry run in five parts

1. The snapshot file (and its size and hash).
2. The `claude -p` call (prompt, schema, no tools, system prompt with its hash, 75-second timeout).
3. The decision that came back.
4. The validator's verdict (`allowed`, `reason`, `shares`, `seatbelt`).
5. The journal line (bar, seen at, instructions hash, snapshot file, raw answer, decision, verdict, elapsed seconds,
   over budget).

## Free data is late

The live loop on our computer saw the 13:35, 13:40 and 13:45 UTC bars 846, 677 and 686 seconds after they closed:
Claude decides on a bar about 11 minutes old. Fine for learning; not for a strategy that needs fresh prices.

## Files

`trading-desk/desk/` (the package; `uv run -m desk [--once] [--dry-run]`), `trading-desk/tests/` (`uv run pytest`: fake
model, fake IB, no network), `data/desk/` (created on the first run, not in git: `journal.jsonl`, `snapshots/`,
`state.json`).
