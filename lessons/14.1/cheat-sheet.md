# Lesson 14.1 cheat sheet: the post-trade review

## Words

| Word | Meaning |
|---|---|
| Post-trade review | A structured look back at one closed trade: the plan, what happened, what went well, what went wrong, and why |
| Lesson | One specific, testable sentence, tagged with the setup it applies to (`vault/Lessons/<title>.md`) |
| Review gate | No new entry until the last closed trade's review exists. In code, not a request |
| `trade_closed` / `trade_reviewed` | The two journal records: a trade ended; its review was written |
| Proposed / active | A new lesson is `proposed`; only a person makes it `active`, and only active lessons reach the trader |

## The loop

A trade closes -> the desk reviews it -> it writes one lesson -> only then may it buy again.

## How the gate works (our desk)

| Piece | What it does |
|---|---|
| `desk/journal.py` | Finds the last closed trade and whether a `trade_reviewed` record follows it |
| `desk/gates.py` | Refuses a buy with a plain reason while that review is missing. A bar-level reason (a stale or superseded bar) still wins |
| `desk/execute.py` | Refuses a buy on its own (`ReviewPending`) as a backstop, even if a gate let it through |
| `desk/snapshot.py` | Every snapshot carries `entry_review_gate: {entries_open, why_closed}`, so the trader sees the block before it answers |
| `desk/mcp_server/trade.py` | `place_bracket` reads the heartbeat's journal and refuses the buy too; `close_position` is never blocked |
| Sells and closes | Never blocked: the desk can always get out |

## How the review works

| Step | What happens |
|---|---|
| Wake Claude | After the trade note is written: the trade, the 5-minute bars from entry to exit, the day's counters and the limits |
| One tool | The call's only tool is `Skill`, and it must show that `post-trade-review` was loaded |
| Checks | Rejected and asked again if the skill wasn't loaded, a number isn't in the facts, or the lesson won't fit in 280 characters |
| Python writes | The `## Review` section of the trade note, `reviewed:` in its front matter, and one lesson in `vault/Lessons/` |
| Open the gate | Last of all, `trade_reviewed` is journaled |

## When things go wrong (safe ways to fail)

- **Claude can't review:** retried every 2 minutes, the gate stays shut. Python never writes a review in Claude's place.
- **"Nothing to change":** no lesson note, but the review is recorded and the gate opens.
- **Same lesson again:** a lesson whose title already exists gets one more `seen` and a link to the trade, not a copy.
- **A trade ended but isn't journaled yet:** entries are held back until it is.

## What the review says (our replay, made-up prices)

- Classification: bad trade, good result.
- Rule broken: target at least 2x the stop distance (the entry checklist). The stop was 6.86 below the entry, the target
  only 2.14 above.
- One lesson: "Before buying, check that the target is at least twice as far from entry as the stop, and if it is not,
  pick a closer stop level or skip the trade." Status proposed, seen once.
