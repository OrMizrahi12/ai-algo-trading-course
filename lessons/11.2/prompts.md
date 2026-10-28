# Lesson 11.2 prompts and commands

Everything typed in the lesson, in order. Lines that start with `/` are Claude Code commands. Both sessions run in
`~/trading-desk`. Paper account only.

## 1. Build the heartbeat (plan mode)

```text
/clear
```

Press Shift+Tab until the footer says **plan mode on**, then send:

```text
Build the heartbeat for this desk. On every closed 5-minute bar of SPY (use the live bar source from ~/trading-lab/live), write a snapshot with 5-minute, 15-minute and daily bars, our indicators, positions, open orders, the account, the session clock and the last journal entries. Then run claude -p in this folder with a JSON schema for the decision: buy, sell, close or wait, with size in R, stop, target and a short reason. Validate the answer, pass it through the lab's risk limits and STOP file, execute with the lab's order manager on paper, and journal everything. Give each bar a 120-second budget. Python must never filter or decide anything for the model: Claude sees every bar. Tests with a fake model and a fake IB.
```

Claude asked two questions before the plan. Our answers:

- **Sell meaning** → `1. Reduce long only (Recommended)`: `sell` only sells part or all of a long position we hold; no
  shorting, so every risk limit applies.
- **Lab import** → `1. Path dependency (Recommended)`: the desk reads the lab's modules read-only; nothing is copied.
  (While building, Claude found the lab has no build system, so it puts the lab's folder on `sys.path` instead.)

Then **Submit**. When the plan is ready, read it, and choose `1. Yes, and use auto mode`.

On our computer: about 4 minutes of planning and 13 minutes of building. 64 tests passed, a real `claude -p` call
answered in 9.9 seconds on a test snapshot, and a dry run on a real SPY bar answered `wait` in 5.4 seconds.

## 2. The seatbelts

```text
Good work. One change: add the automatic flatten before the close, the same as the lab. The model decides every trade, but hard safety rules (STOP, the risk limits, being flat before the close, no overnight) are seatbelts that live in code and always win. That is not Python trading; it is Python enforcing our rules. Log and journal it whenever a seatbelt acts, add tests, then commit everything.
```

2 minutes 37 seconds on our computer: committed as one commit on a new branch, `heartbeat`, with 88 tests passing.

## 3. One bar by hand (market open, a fresh session)

```text
/clear
```

```text
The market is open. Run one heartbeat bar as a dry run, so no orders, then show me what happened: the snapshot file it wrote, the exact claude -p call, the JSON decision that came back, the validator verdict and the journal line. Also tell me how late the newest bar arrived.
```

If there is no new closed bar yet (our first try found none), wait for one:

```text
Poll again. On our free data a bar shows up about 11 minutes after it closes, so the 9:30 bar should land around 9:46 New York. Wait until 9:50, then run the same dry run and show me everything I asked for.
```

Change the times to your own clock. We moved the lab's STOP file aside before this session; with it in place, a dry run
works the same way, and the snapshot says `stop_file_present: true`.

## 4. The snapshot in VS Code, then the live loop (a second terminal)

```bash
cd ~/trading-desk && code data/desk/snapshots/<the file from the dry run>.json
```

```bash
uv run -m desk
```

Stop it with Ctrl+C (Python prints a `KeyboardInterrupt` traceback: it was sleeping between polls; nothing was half done).
Then read the last decisions:

```bash
tail -n 3 data/desk/journal.jsonl | jq '{bar, action: .decision.action, reason: .decision.reason}'
```

`uv run -m desk --once --dry-run` handles one bar and sends no orders. Without `--dry-run`, and without the STOP file,
a `buy` would place a bracket order on the **paper** account.

## Pause and try

1. In your own desk, in plan mode, send request 1.
2. Before you approve, read the plan for one thing: does Python ever filter the bars, or decide for the model?
3. Send request 2, then run one bar as a dry run (request 3) and read all five parts.

You're done when your journal has a line for a real bar, with a decision, a reason and a verdict, and no order went out.
