# Student kit: Lesson 13.2, The journal the agent writes itself

Module 13: Memory with Obsidian · AI Algorithmic Trading with Claude Code and Interactive Brokers

The desk's journal keeps the numbers: one line per bar, with every decision, order and fill. Since lesson 13.1 the desk
also has an Obsidian vault for the thinking. In this lesson we connect the two. When a trade closes, the heartbeat hands
it to a **writer**: a separate Claude call with no tools, which only writes sentences, while Python computes every number
and writes the files, only inside `vault/Trades`, `vault/Daily` and `vault/Weekly`. After the close the writer fills in
the day's note, and on Fridays it writes the week's summary. We test it with a fake trade, run the desk on paper, and
check what it wrote against the journal.

## What's in this kit

| File | What it is |
|---|---|
| `prompts.md` | Every request typed in the lesson, the command that runs the desk, and the pause-and-try exercise |
| `cheat-sheet.md` | The words, how the writer is built, when notes appear, what a trade note contains, and how to check it |
| `trading-desk/` | The files this lesson added or changed in the desk, as committed at the end of the lesson: `desk/scribe.py`, `desk/trades.py`, `desk/heartbeat.py`, `desk/journal.py`, `desk/__main__.py`, `tests/test_scribe.py`, `vault/README.md`. Copy them over your desk from lesson 13.1 |
| `trading-desk/vault/` (examples) | The notes the writer wrote on our paper desk: `Daily/2026-10-22.md`, `Daily/2026-10-23.md`, `Weekly/2026-W43.md` (no trades that week), plus the two templates from lesson 13.1 they are built from. Yours will differ |

## Before you start

- Your `~/trading-desk` with the heartbeat from Module 11 and the guardrails from 12.3, and the vault from lesson 13.1
  (with its `Templates/Trade note.md` and `Templates/Daily note.md`).
- Claude Code in the terminal, signed in with your subscription. The writer runs `claude -p`, so the `claude` command
  must work in the terminal where the heartbeat runs.
- Obsidian, with the desk's `vault/` folder open as a vault.
- IB Gateway logged in to the **paper** account (API port 4002) for the live part.
- Time on our computer: about 9 minutes for Claude to build and test the writer; the live part runs as long as the
  session.

## Try it yourself

1. Send request 1 in `prompts.md`, or copy the kit's files over your desk and run `uv run pytest -q tests/test_scribe.py`.
2. Look at the fake note in Obsidian, then delete it.
3. Run the desk on paper through a close, and ask Claude to check the notes against the journal.

You're done when a fake trade gives you a note with every number from the journal, and the daily note after the close
matches the journal's bar count. Your code, numbers and Claude's answers will differ from the video, and that's fine.

## Good to know

- **No trade closed while we filmed.** Every bar was a wait, so the trade note in the video is the fake test trade.
  When your desk closes a real trade, the same writer writes its note.
- **The writer can't touch files.** Its Claude call has no tools; Python writes the files and refuses any other folder.
- **Never a made-up number.** If a price is unknown (for example, a stop filled and the broker sent no price), the field
  stays empty and the note says so.
- **Delayed data needs patience.** With free, delayed data the last bar of the day arrives about 15 minutes late. The
  final version waits for it (or for 17:00 New York time) before writing the day's notes.

Paper account only. Educational content, not financial advice; nothing here is a promise of profit or a recommendation.
