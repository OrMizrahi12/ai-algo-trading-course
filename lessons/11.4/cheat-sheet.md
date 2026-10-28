# Lesson 11.4 cheat sheet: sessions and context across bars

## Words

- **Session**: one continuous Claude conversation, with its own memory of what was said.
- **`--resume`**: continue a saved session by its id (`claude -p ... --resume <session id>`).
- **Context window**: how much a session can hold (the trader's model reported a 1M-token window).
- **Compaction**: Claude Code replacing the older part of a conversation with a summary it writes itself, to make room.
- **Daily rollover**: a fresh session each trading day, whose first message is a short summary of the day before.

## One session per trading day

| When | What the heartbeat does |
|---|---|
| First bar of the New York day | Starts a new session (`--session-id <new uuid>`), keeps the id in `data/desk/state.json`. First message: today's date, a summary of the previous day from the journal (counts, trades, seatbelts, last decision), and a recap of today if bars were already handled |
| Every later bar | `--resume <id>`: the trader can read its own earlier reasoning |
| `CLAUDE.md` changed | A new session, so one conversation never mixes two sets of instructions |
| A resume fails | That bar is `wait`; the next bar starts a new session with a recap from the journal |
| Context at 80% of the window | The desk ends the session itself and starts a new one (full snapshot + exact journal recap) |

**Keep the hash honest.** On `--resume`, Claude Code keeps the system prompt of the session's first request unless you pass
`--system-prompt-snapshot off`. Without it, an edit to `CLAUDE.md` at lunch would not reach the trader, and the
instructions hash in the journal would be wrong.

**Check the memory without touching the session.** Ask a fork (a copy) of the session what it said earlier.

## What goes in each bar

| Every bar (the delta, after the first bar) | Already in the session | Looked up only when needed (modules 12-13) |
|---|---|---|
| New 5- and 15-minute bars with indicators, today's daily bar, the clock, positions, open orders, fills, account, STOP flag, risk limits, journal entries the session hasn't seen | Earlier bars and the trader's own earlier decisions | Older history, past trades, notes: through tools and memory |

Measured on our computer (one session, `--dry-run`, paper Gateway):

| Bar | Input | Bytes | Context after | Added |
|---|---|---|---|---|
| 13:55 | full | ~63k | 34,613 | |
| 14:00 | full | ~66k | 65,807 | +31,194 |
| 14:05 | delta | 2.8 KB | 67,509 | +1,702 |

With full snapshots the window would fill around bar 32 (about 2.5 hours after the open). With deltas a full 5-minute
day is about 35k + 77 × 1.7k ≈ 165k tokens, roughly 17% of the window.

## Why not rely on compaction

1. It loses the trader's own words (in a fork compacted at 100k, it could no longer quote its earlier reason).
2. You can't audit it: the memory would hold a paraphrase you never see.
3. It happens at a moment you don't choose, maybe in the middle of a trade.

## Usage: one live morning, extrapolated

Eleven live bars (14:10 to 15:00, all `wait`): the context grew from 69,603 to 87,378 tokens (7.0% to 8.7%), about +1.7k
per bar, 4 to 10 seconds per bar. `/usage`: current session 2% before and 2% after, week 0%.

Real cost per bar, at list-price equivalents: about $0.13 for a full snapshot, $0.016 to $0.018 for a delta.

| Bars | Per day | End-of-day context | Cost per day (list-price equivalent) |
|---|---|---|---|
| 15-minute | 26 | ~80k (8%) | ~$0.50 |
| 5-minute | 78 | ~174k (17%) | ~$1.70 |
| 1-minute | 390 | ~735k (74%) | ~$21 |

Cost grows roughly with the square of the number of bars, because every bar re-reads the whole conversation. These are
estimates from one quiet stretch, not what a plan charges; the meter shows whole points only. Your numbers will differ.

## Choosing a bar size and a plan

- **5-minute bars** are the course default: time for Claude to think, and a day that fits easily in a plan.
- **15-minute bars** are the lighter option.
- **1-minute bars** are too fast to think, too stale on the free delayed data (about 13 minutes behind), and expensive.
- To run an AI trader all day next to your own work with Claude, a **Max** plan gives the headroom. That's about usage
  limits, not about making money.
- Anthropic's pages (checked October 2026): `claude -p` signed in with your plan draws from your subscription limits, and
  the advertised Pro and Max limits assume ordinary, individual use. Terms change: read the current ones (Lesson 16.3).

## Checks

- One session id in the journal for the whole day (`session.id`), a new one the next morning.
- Each later bar records `input: delta` and adds a couple of thousand tokens of context.
- Each record has `bar_cost_usd` (this bar) and `session_cost_usd` (the running total).
- The journal's `instructions` hash still matches your ledger row.
