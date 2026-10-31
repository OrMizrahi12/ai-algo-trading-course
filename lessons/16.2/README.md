# Student kit: Lesson 16.2, Reading the results

Module 16: Capstone · AI Algorithmic Trading with Claude Code and Interactive Brokers

Everything we built has run on a paper account: the factory strategy on the live engine, the AI desk and its variants.
In this lesson we read the results honestly. Claude walks through every number in R, over the whole period, with no
picked dates, and says what the numbers can and can't tell us. We chase a stop order that looked live and make the lab's
daily report check IB for leftovers. We read the agent's journal and versions in the Obsidian vault. And we write three
next experiments, each with a change, a protocol and a drop rule, before running any of them.

This is a few days of paper trading. The lesson reads real numbers and draws no conclusion from them: no profit claim,
and no investment advice.

## What's in this kit

| File | What it is |
|---|---|
| `prompts.md` | Every request typed in the lesson, in order, what Claude did with each one, and the pause-and-try exercise |
| `cheat-sheet.md` | The words, how to read a result in six steps, our Monday's numbers, the leftover stop, reading an agent's journal, and the shape of a next experiment |
| `next-experiments-template.md` | The three next experiments from the lesson as a vault note: change, protocol and drop rule for each. Use the shape, write your own |
| `trading-lab/` | The lab files the lesson's commit changed: `scheduler/report.py` (the fresh read-only look at IB, `LEFT AT IB`), `scheduler/__main__.py`, `live/config.py` (`REPORT_CLIENT_ID = 11`) and `tests/test_scheduler.py` (the new tests with a fake IB) |

The same commit also added client ID 11 to the client-ID list in the lab's `AGENTS.md`, and one line to the README's
timetable (the report at close + 5 minutes now includes the look at IB). Make those two edits by hand, or ask Claude to.

## Before you start

- Your `~/trading-lab` from the earlier lessons: the live engine, its journal, the scheduler and its daily report, the
  dashboard, and the backtester with its research cache (the holdout stays out).
- Your `~/trading-desk`: its journals, the sealed forward-test report from lesson 15.4, the variants from module 15 and
  the Obsidian vault.
- Claude Code in the terminal, signed in with your subscription, and Obsidian with the desk's vault open.
- A paper account in IB Gateway or TWS. Request 2 opens a read-only connection; pick a client ID no other program uses.
- Time on our computer: about 3 minutes for the walkthrough, 2 for the stop check, 4 for the report change, and a few
  minutes each in the desk.

## Try it yourself

1. After a few days (or weeks) of your own paper runs, send request 1 in `prompts.md` in the lab's Claude Code.
2. If the answer flags anything still live at IB, check it read-only (request 2) before the next open.
3. Copy the `trading-lab/` files over your lab (or send request 3) and run `uv run pytest -q`.
4. In the desk's Claude Code, send request 4, then requests 5 and 6. Commit the note before you run anything.

You're done when every number you quote comes with its sample size. Your numbers, dates and Claude's answers will differ
from the video, and that's fine.

## Good to know

- **Read-only first.** The walkthrough changed nothing; the stop check used a fresh read-only connection on a free
  client ID; nothing in the desk's code was touched.
- **Sealed stays sealed.** The desk's forward-test report shows no profit or ratio until its stop rule (about 100 scored
  trades or the end of the period). Reading the desk's raw journals doesn't bypass the seal: they hold decisions, not
  profits.
- **Your desk may differ.** Our variants were inert for a reason specific to our Monday (the lab's QQQ position sat in
  every snapshot). Your next experiments come from your own journal.
- **Paper only.** Every order in this course goes to a paper account. Nothing here is a recommendation to trade.
