# Student kit: Lesson 11.3, The prompt is the strategy

Module 11: Claude as the trader · AI Algorithmic Trading with Claude Code and Interactive Brokers

In Part 2, Claude is the trader, so its instructions are its strategy. In this lesson Claude interviews us and writes the
trader's **constitution** in `~/trading-desk/CLAUDE.md`: a mission, a trading style, risk rules, how to think on every
bar, and the output contract the heartbeat from Lesson 11.2 expects. We make that file the trader's only instructions,
sent once per bar with nothing from our own settings, register it as **Trader v1** in the experiment ledger with its
hash, and run it on one live bar on paper.

## What's in this kit

| File | What it is |
|---|---|
| `prompts.md` | The requests typed in the lesson, the interview answers we chose, the commands, and the pause-and-try exercise |
| `cheat-sheet.md` | The five parts of a constitution, the words, rules in words vs rules in code, what the hash covers and what it doesn't, the checks |
| `trading-desk/CLAUDE.md` | The constitution exactly as committed in the lesson (77 lines; its hash is `73a60f566379`) |
| `trading-desk/experiments/ledger.csv` | The ledger with its header row and the Trader v1 row |
| `trading-desk/desk/model.py` | The desk's model call after the lesson: `CLAUDE.md` as the system prompt, no tools, no setting sources |

Use the constitution as an example to read, not as a file to copy: the point of the lesson is to write your own, with
your own answers to the interview.

## Before you start

- The trading desk from Lessons 11.1 and 11.2 (`~/trading-desk` with the heartbeat, its tests and the journal).
- Claude Code in the terminal, signed in with your subscription, in auto mode.
- For the live bar: the IB Gateway logged in to your **paper** account (port 4002), during US market hours.
- Time on our computer: about a minute and a half for the constitution, a minute and a half for the once-per-bar fix,
  half a minute for the stricter settings, and one bar for the live run.

## Try it yourself

1. In `~/trading-desk`, `/clear`, then send request 1 in `prompts.md` and answer Claude's questions with your own choices.
2. Read the report. Ask which rules the code enforces and which are only words.
3. Make sure the constitution reaches the trader exactly once per bar, with nothing from your settings (requests 2 and 3).
4. In market hours, check the hash, run the desk on a bar, and compare the journal's `instructions` with your ledger row.

You're done when the instructions hash in your journal matches your ledger row, and every decision in it gives a
reason. Claude's questions, your constitution and the trader's decisions will differ from the video, and that's fine.

## Good to know

- **Words shape the decisions; code sets the limits.** Some risk rules in the constitution (the cooldown, the two-loss
  limit, the 1R cap, three entries a day) are only words. The seatbelts from Lesson 11.2 (no adding to a position, the
  10-minute flatten, the entry-time limits) are in code and hold whatever the prompt says.
- **One source, one hash.** Making `CLAUDE.md` the only instructions means the hash in every journal record equals the
  hash in the ledger, so every decision traces back to one trader version.
- **Change the words, change the trader.** Any edit to `CLAUDE.md` changes its hash. Add a new ledger row (Trader v2)
  instead of editing the v1 row.
- **What the hash doesn't cover.** The tools the model can see, its environment and the model itself. That's why the
  ledger also has a model column.
- **Delayed data.** With the free delayed data, the trader decides on bars that are 10 to 15 minutes old. A real-time
  market data subscription (paid, optional, not used in this course) keeps the same loop on current bars.

## Safety

Paper trading only. The constitution's first line says it, the desk refuses live ports, and the seatbelts stay in code.
Educational content, not financial advice; nothing here is a recommendation, a strategy to trade, or a promise of profit.
