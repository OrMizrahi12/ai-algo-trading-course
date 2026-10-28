# Student kit: Lesson 11.2, The agent loop

Module 11: Claude as the trader · AI Algorithmic Trading with Claude Code and Interactive Brokers

In Lesson 11.1 we drew the loop and gave the trader its own desk. In this lesson we build the loop and run it:

1. **The heartbeat.** On every closed 5-minute bar of SPY, Python packs everything into one snapshot (5-minute,
   15-minute and daily bars with indicators, positions, open orders, the account, the session clock, the last journal
   entries) and wakes Claude with `claude -p`. Python never filters what Claude sees and never decides.
2. **The decision contract.** Claude must answer in one JSON shape, enforced with `--json-schema`: an action (buy, sell,
   close or wait), a size in R, a stop, a target and a short reason. A validator checks it; anything invalid, late or
   missing becomes `wait`, with the reason in the journal.
3. **Seatbelts in code.** The STOP file, the lab's risk limits, the entry window, a flatten 10 minutes before the close,
   no overnight positions and the paper guard always win over the model, and every time one acts it is logged and
   journaled.
4. **One bar by hand, then live.** A dry run on a real bar (snapshot, call, decision, verdict, journal line), then the loop
   live on the paper Gateway for three bars. Every decision was `wait`, each with a reason in plain English.

## What's in this kit

| File | What it is |
|---|---|
| `prompts.md` | The requests typed in the lesson, the answers we chose, the commands, and the pause-and-try exercise |
| `cheat-sheet.md` | The words, the loop step by step, the decision contract, the time budget, the seatbelts and their log tags, the five parts of a dry run, the free-data delay |
| `trading-desk/` | The desk exactly as committed at the end of the lesson (commit 97df5d3 on the `heartbeat` branch): `desk/` (heartbeat, snapshot, decision, model, gates, seatbelts, execute, journal, budget, lab bridge, `instructions.md`), `tests/` (88 tests with a fake model and a fake IB), `README.md`, `CLAUDE.md`, `pyproject.toml`, `uv.lock` |

## Before you start

- Your `~/trading-desk` from Lesson 11.1, and the Trading Lab from Module 10 (its live bar feed, order manager, risk
  limits, STOP file and journal). The desk reads the lab read-only from `~/trading-lab` (`TRADING_LAB` changes the path).
- `uv` and Claude Code in the terminal, signed in with your subscription (`claude -p` uses the same sign-in, no API key).
- IB Gateway logged in to the **paper** account, API port 4002, and a client ID nothing else uses (the desk uses 8).
- Time on our computer: about 4 minutes of planning, 13 minutes of building, 2.5 minutes for the seatbelts. One bar took
  5.32 seconds from snapshot to journal line.

## Try it yourself

1. In your desk, `/clear`, switch to plan mode (Shift+Tab), and send request 1 in `prompts.md`.
2. Before you approve, read the plan for one thing: does Python ever filter the bars or decide for the model?
3. Send request 2 (the seatbelts). Then, with the market open, run one bar as a dry run (request 3) and read all five parts.

You're done when your journal has a line for a real bar, with a decision, a reason and a verdict, and no order went out.
Your code, numbers and Claude's decisions will differ from the video, and that's fine.

## Good to know

- **A wait is a decision.** On a gap-down morning Claude waited on every bar, and said why. A clean day of `wait` is a
  good day for a careful desk.
- **The model can't break the contract.** The schema and the validator decide what an answer may be; a broken answer is
  never repaired by guessing, it becomes `wait`.
- **Seatbelts are not strategy.** Python never chooses a trade; it only refuses an unsafe one, or sells before the close.
  That is Python enforcing your rules.
- **Free data is late.** Our bars arrived 11 to 14 minutes after they closed. Fine for learning; a strategy that needs
  fresh prices needs a real-time data subscription, which is your decision and not needed for this course.
- **Read the honest notes.** Claude said the flatten was only tested against the fake IB, that a halted desk does nothing,
  and that the flatten sells every SPY share in the account. Read the summary before you trust a change.

## Safety

Paper trading only. The desk connects to the paper Gateway only (port 4002) and stops on any non-paper account or a live
port. Keep the STOP file in place until you decide to let it place paper orders. Educational content, not financial
advice; nothing here is a recommendation or a promise of profit.
