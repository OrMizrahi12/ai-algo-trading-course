# Lesson 13.2 cheat sheet: the journal the agent writes itself

## Words

| Word | Meaning |
|---|---|
| Trade note | One Markdown note per closed trade, written by the desk (`vault/Trades/YYYY-MM-DD HHMM SPY.md`) |
| Thesis | The reason for the trade, written before the entry (the note's "Why I bought") |
| Summary note | A daily or weekly note that links and sums up the trade notes (`vault/Daily/`, `vault/Weekly/`) |
| Journal | The desk's own record: one JSON line per bar (decisions, orders, fills), plus `trade_closed` lines |
| R | 1% of the account: the money lost if a trade's stop is hit. "+1R" is a profit of that size |
| Front matter | The `---` block at the top of a note; Obsidian shows it as properties |

## Numbers and thinking

- The **journal** keeps the numbers: every bar, decision, order and fill, as the code saw them.
- The **vault** keeps the thinking: rules, setups, and now one note per trade, per day and per week, linked together.
- The writer turns the first into the second, after the fact. It never trades and never changes the trader's
  instructions.

## How the writer is built (our desk)

| Piece | What it does |
|---|---|
| `desk/trades.py` | Follows a trade from its buy until the desk is flat again; the heartbeat journals a `trade_closed` record |
| `desk/heartbeat.py` | Hands each closed trade (and each bar) to the writer, in a background thread, so no bar is delayed |
| `desk/scribe.py` | The writer: Python gathers the facts from the journal, computes every number and link, and writes the files |
| The Claude call | A separate `claude -p` call with no tools at all (`--tools ""`): it only returns sentences in a schema |
| Number check | A sentence with a number that is not in the journal facts is rejected and asked again; after 3 failures the note gets a plain Python summary |
| Folder guard | Files are written only in `vault/Trades`, `vault/Daily`, `vault/Weekly`; `..` paths, `Rules/`, `Templates/`, `.obsidian/` and symlinks are refused (and tested) |

## When notes appear

| When | What the writer writes |
|---|---|
| A trade closes | Its trade note from the template (properties, links, why I bought, checklist, what happened, review); the day's note lists it and updates its counters |
| After the day's last bar is in the journal (from 16:10 New York time; at the latest 17:00) | "How the day went" in the day's note; a plan or lessons written by hand are kept |
| Friday, same condition | The week's summary, linking every trade note and daily note of the week |
| The heartbeat starts after a missed day | The earlier day's note is filled in (up to two days back) |

## What the trade note contains

- 14 properties: type, date, symbol, setup, entry time, entry price, stop, target, size in R, exit time, exit price, exit
  type, result in R, classification (good or bad trade, good or bad result).
- Links: the setup in `Playbook/`, the day in `Daily/`, the risk rules.
- "Why I bought": one sentence a beginner can follow (the thesis).
- The checklist, left unticked: the journal does not record those checks, so ticking them would be inventing.
- "What happened": the facts from the journal as a list, then a paragraph.
- Review: the classification and one lesson (or "nothing to change").
- If a stop or target filled and the broker did not report the price, the exit price and result stay empty.

## Check what it wrote

- Count it yourself: ask Claude to compare the notes with the journal before you commit them.
- Our check found one real error: the writer ran at 16:10, but the delayed free data feed journaled the day's last bar
  (15:55) at 16:11, so Friday was counted one bar short (77 instead of 78). The fix: write the day's notes only once its
  last bar is in the journal, or an hour after the close if it never arrives; earlier days are always written.
- A note that says "seen once" or "not a pattern" is doing its job: one day is an anecdote.
