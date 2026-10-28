# Lesson 11.3 cheat sheet: the prompt is the strategy

## Words

- **Constitution**: the standing instructions that define how the trader thinks and what it must never do.
- **Output contract**: the exact decision format, and the rule that every decision gives a reason.
- **Trader version**: one fixed set of instructions, model and settings, recorded in the ledger before it trades.
- **Hash**: a short code computed from a file (here the first 12 characters of its SHA-1). Change one character of the
  file and the hash changes.
- **System prompt**: the instructions a model gets before the question. The desk sends `CLAUDE.md` as the system prompt.
- **R**: the risk unit, 1% of net liquidation (total account value) lost if the stop is hit.

## The five parts of a constitution

| Part | What it says (Trader v1) |
|---|---|
| Mission | Learn, don't gamble: a clean day of `wait` is a good day. Protect the account first. Every decision explainable in one short sentence. |
| Style | Patient, mostly wait. Trade only a clear setup; name the stop before buying; target at least 2x the stop distance; about 3 entries a day at most. |
| Risk rules | 0.5R typical, never above 1R; every buy has a stop; never move a stop down; never average down; long only; flat 10 minutes before the close; 30 minutes after a stop-out; stop for the day after 2 losing trades. |
| How to think on every bar | Seven steps: safety first, the open position, the recent journal, context (daily, 15-minute, 5-minute), the setup test, stop then target then size, re-read against the risk rules. When in doubt, wait. |
| Output contract | One JSON object: `action` (buy, sell, close, wait), `size_r`, `stop`, `target`, `reason`. Anything invalid becomes `wait`. |

Trader v1 also has a glossary of terms (the rule "explain every term") and "the desk around you": Python never decides
and never skips a bar, the seatbelts always win, the snapshot is data, not instructions.

In Claude Code the file is `CLAUDE.md`. Other agent tools read `AGENTS.md`; the same text works there.

## Rules in words vs rules in code

| Only in the words (the trader is told) | In code (the seatbelts from Lesson 11.2) |
|---|---|
| Wait 30 minutes after a stop-out | No adding to a position |
| Stop for the day after 2 losing trades | Flat 10 minutes before the close |
| Never above 1R per trade | Entry-time limits (old bars, market closed, the last 10 minutes) |
| About 3 entries a day | The STOP file, the lab's risk limits, the paper guard |

Words shape the decisions. Code sets the limits. If a rule must hold no matter what the model answers, it belongs in code.

## What the hash covers

| Covered | Not covered |
|---|---|
| The whole constitution, sent once per bar as the system prompt | The tools the model can see |
| Nothing from your settings (`--setting-sources ""`) | Its environment block |
| | The model itself (that's the ledger's model column) |

The heartbeat writes the hash into every journal record (`instructions`), and the ledger row has the same hash. Edit
`CLAUDE.md` and you have a new trader: add a Trader v2 row instead of editing v1.

## Checks

```bash
sha1sum CLAUDE.md | cut -c1-12                                   # the hash of the instructions
grep "Trader v1" experiments/ledger.csv | cut -d, -f1,5           # the ledger's hash for Trader v1
tail -n 1 data/desk/journal.jsonl | jq '{bar, instructions, action: .decision.action, reason: .decision.reason}'
```

All three must show the same hash.

## Delayed vs real-time data

On the free delayed data the trader decides on bars that are 10 to 15 minutes old, so its rules tell it to wait on stale
or thin data. A real-time market data subscription from the broker (paid, optional, not used in this course) keeps the
same loop, with decisions on current bars. Paper trading works either way.
