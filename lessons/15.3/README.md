# Student kit: Lesson 15.3, The stock-open agent

Module 15: Advanced agent designs · AI Algorithmic Trading with Claude Code and Interactive Brokers

The desk has traded one ETF so far. In this lesson a second agent works the **US stock open** next to it. Before the open,
the lab's gap scanner from lesson 7.3 builds a watchlist and Claude picks **at most two names**, each with a written plan:
what makes it buy, where the stop goes, and when to give up. From the open, an **open-window loop** hands Claude each
finished 5-minute bar of those names, inside the desk's risk layer, with new entries only in a short window. We ran it on a
live paper morning, in dry run, and read the journal honestly: the first scan found nothing, the picks came after the
signal, and the journal exposed a real bug that we fixed.

## What's in this kit

| File | What it is |
|---|---|
| `prompts.md` | Every request typed in the lesson, in order, what Claude did with each one, and the pause-and-try exercise |
| `cheat-sheet.md` | The words, the morning in order, how the loop works, our two picks, the bug, the result and what the open taught us |
| `trading-desk/` | The files this lesson added or changed in the desk, as committed after the fix: `desk/openwindow.py` (the loop), `.claude/open-window/constitution.md` (the open agent's own instructions), `tests/test_openwindow.py`, `README.md`, and our day's note `vault/Daily/2026-10-26.md` (the empty first scan, the two picks with their plans, and the open-window review). Copy them over your desk |

## Before you start

- Your `~/trading-desk` and `~/trading-lab` from the earlier lessons: the desk's heartbeat, gates, review gate and journal,
  the vault, and the lab's `scanner.py` (lesson 7.3) and limits file.
- Claude Code in the terminal, signed in with your subscription.
- A paper account in IB Gateway or TWS. The loop runs in dry run by default and never sends an order.
- A market day. Ask for the picks before the open (US stocks open at 09:30 New York time), and leave about two hours for
  the window. On our computer the build took about 10 minutes, each scanner run about 10 minutes.

## Try it yourself

1. Before the open: send request 1 in `prompts.md`, or copy the kit's files over your desk and run `uv run pytest -q`.
2. Make your own decisions (request 2 shows ours): dry run, the limits file, the window, the client ID.
3. Start the loop in its own terminal: `uv run -m desk.openwindow`.
4. After the first bars exist: request 4, the scanner rerun and the picks.
5. During the window: request 5, the journal so far. After it: request 7, the review.

You're done when your journal shows each bar's decision and reason, and you know whether a refusal came from the plan or
from the desk's limits. Your scanner, names, numbers and Claude's answers will differ from the video, and that's fine.

## Good to know

- **The scan can be empty.** On our paper account IB refused the gap scans (error 492), and before the open there are no
  bars of today to measure a gap against. Claude said so and made no picks. Plan for that.
- **The names are not tips.** RRC and HHH are simply what the scanner returned on 26 October 2026. Your scanner will return
  other names on your day.
- **Delayed data hurts most at the open.** Paper market data arrives about 15 minutes late, and the desk waits for finished
  bars, so each bar was decided 16 to 21 minutes after it closed. The one RRC signal had closed before the picks were even
  written, and by the time its data arrived the price was lower.
- **Let the desk enforce the limits.** Our picks were not in the lab's limits file, so they could never be bought. That is
  fine in a dry run, but the model must not decide that itself: the fix in `constitution.md` makes it judge the plan only,
  so the desk's own check runs and the journal records the refusal. Better still, check a pick against the limits file when
  you pick it.
- **Keep the SPY desk clean.** The open agent has its own instructions, client ID and journal, and leaves `CLAUDE.md`, the
  plugin and the skills untouched, so the SPY desk's instruction hash does not change.
- **Single stocks need more care than an ETF.** An exchange can halt a single stock, and its spreads are wider than SPY's.
- **Usage, not a bill.** The cost lines in the loop's log are list prices; on a subscription they are usage figures.

Paper account only. Educational content, not financial advice; nothing here is a promise of profit or a recommendation.
