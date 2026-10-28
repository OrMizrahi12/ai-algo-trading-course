# Student kit: Lesson 11.4, Sessions and context across bars

Module 11: Claude as the trader · AI Algorithmic Trading with Claude Code and Interactive Brokers

Until now, every bar was a brand-new Claude call: the trader decided and forgot. In this lesson the heartbeat keeps
**one Claude session per trading day**, continued with `--resume`, with a fresh session each morning that starts from a
summary of yesterday. Later bars send only what changed, so the day fits in the context window, and we see why we don't
rely on compaction. Then the trader runs live on paper for 46 minutes, we read `/usage` before and after, and Claude
estimates a full day on 1-, 5- and 15-minute bars.

## What's in this kit

| File | What it is |
|---|---|
| `prompts.md` | The requests typed in the lesson, the commands, and the pause-and-try exercise |
| `cheat-sheet.md` | The words, the session rules, what goes in each bar, why not compaction, the measured usage, choosing a bar size and a plan, the checks |
| `trading-desk/desk/model.py` | The desk's model call after the lesson: the session flags (`--session-id`, `--resume`, `--system-prompt-snapshot off`) and the context and cost numbers it reads back |
| `trading-desk/desk/snapshot.py` | The snapshot builder, with `delta()`: what a resumed session gets on later bars |
| `trading-desk/experiments/ledger.csv` | The ledger with the Trader v1 and Trader v1.1 (day sessions) rows |

The files are from the end of the lesson (commit "Journal each bar's own cost, and keep the session's running total
too"). Read them as an example; your own Claude will write its own version.

## Before you start

- The trading desk from Lessons 11.1 to 11.3 (`~/trading-desk` with the heartbeat, the constitution and the journal).
- Claude Code in the terminal, signed in with your subscription, in auto mode.
- The IB Gateway logged in to your **paper** account (port 4002), during US market hours.
- Time on our computer: about six minutes for the sessions, five and a half for the delta, an hour of live bars (any
  length works), and a minute and a half each for the estimate and the cost fix.

## Try it yourself

1. Send request 1 in `prompts.md`. Read the report, especially what it says about the context size.
2. Send request 2, and compare the context added by a full snapshot and by a delta.
3. Read `/usage`, run the loop on paper for a while, read `/usage` again.
4. Ask for the full-day estimate with your own numbers (request 4), then fix the per-bar cost (request 5).

You're done when your journal shows one session for the whole day, each later bar adds a couple of thousand tokens, and
you know the cost of one bar. Claude's code, your numbers and the trader's decisions will differ from the video.

## Good to know

- **The hash stays honest only with `--system-prompt-snapshot off`.** Without it, a resumed session keeps the system prompt
  of its first request.
- **Check the memory with a fork.** A fork is a copy of the session, so the real one is untouched.
- **Don't rely on compaction.** The desk starts a new session itself at 80% of the window, with an exact recap from the
  journal.
- **The dollar figures are list-price equivalents** from one quiet stretch, not a bill, and `/usage` shows whole points
  only. Plans, limits and terms change: check the current ones.

## Safety

Paper trading only. The desk refuses live ports and the seatbelts stay in code. Educational content, not financial advice;
nothing here is a recommendation, a strategy to trade, or a promise of profit.
