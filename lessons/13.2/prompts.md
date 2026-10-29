# Lesson 13.2 prompts

Everything typed in the lesson, in order. Lines that start with `/` are Claude Code commands. One interactive Claude Code
session in `~/trading-desk` (auto mode), with Obsidian open on the desk's vault beside it. Paper account only.

## 1. Ask for the writer

```text
/clear
```

```text
Today the vault fills itself. When a trade closes, have the heartbeat notice it and run a separate Claude call (not the trader) that reads the trade from the journal and writes its note in vault/Trades from the Trade note template, linking the playbook setup and today's daily note. After the close, the same writer fills in today's daily note, and on Fridays a weekly summary that links every trade note of the week. The writer may only write inside vault/, and it must never invent a number. Test it with a fake trade, then show me the note it wrote.
```

On our computer Claude worked for 8 minutes 58 seconds. It read the desk's heartbeat, journal and vault; auto mode's
classifier denied one read of the trading lab's folder, so it worked from the desk's own code and tests. It added
`desk/trades.py` (a trade from its buy until the desk is flat again, and a `trade_closed` journal record), hooks in
`desk/heartbeat.py`, the writer `desk/scribe.py`, and `tests/test_scribe.py` (with a fake Claude), then ran a real Claude
call on a fake trade. 237 tests passed.

## 2. Look at the fake note in Obsidian

```text
Copy that fake note into vault/Trades with TEST at the start of its name, so I can open it in Obsidian. Do not commit the test note. Commit everything else.
```

The fake trade: a VWAP reclaim, 10 shares at 600.0, stop 597.0, target 606.0, closed by hand at 603.0, +1.0R. These are
made-up test numbers, not SPY's real price.

```text
Looks good. Delete the test note now.
```

## 3. Run the desk on paper

In a separate terminal, in `~/trading-desk`, with IB Gateway logged in to the paper account:

```bash
uv run -m desk
```

The heartbeat catches up on the bars since its last run, then follows the live bars. When a trade closes, the writer
writes its note; after 16:10 New York time it fills in the day's "How the day went"; on Friday after the close it writes
the week's summary. On our computer no trade closed during the session, and the writer filled in the previous day's note
as soon as the heartbeat started.

## 4. Check the writer against the journal

The next morning, back in the Claude Code session:

```text
The desk ran through Friday's close and stopped overnight. Check what the vault writer wrote in vault/ against the journal, then commit those notes.
```

Claude found one real error: the notes said 77 bars for Friday, the journal had 78. The writer ran at 16:10 New York
time, and the delayed data feed only journaled the day's last bar (15:55) at 16:11. Claude corrected the count and
committed the notes, then suggested a code fix.

```text
Yes, make that fix, with a test, and commit it.
```

## Pause and try

1. Ask Claude for a writer like ours: a separate call with no tools, Python writing the files, and a number check.
2. Test it with a fake trade, open the note in Obsidian, then delete it.
3. Run your desk on paper through a close, and check the notes against the journal.

You're done when a fake trade gives you a note with every number from the journal, and the daily note after the close
matches the journal's bar count.
