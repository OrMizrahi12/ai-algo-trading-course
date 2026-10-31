# Student kit: Lesson 16.1, One machine, the whole lab

Module 16: Capstone · AI Algorithmic Trading with Claude Code and Interactive Brokers

Everything we built runs together on **one machine**, on a paper account: the scheduled live engine on QQQ, the AI desk's
heartbeat on SPY, the desk's open-window agent in dry run, and **one dashboard** over all of it. Claude plans the morning
first (what starts, when, with which client ID, limits and logs), fixes two bugs before anything starts, and then we
**break it on purpose**: a short lost connection, a long outage, and a usage limit. Each drill must end flat, with an alert
we received, and everything restored to a baseline.

## What's in this kit

| File | What it is |
|---|---|
| `prompts.md` | Every request typed in the lesson, in order, what Claude did with each one, and the pause-and-try exercise |
| `cheat-sheet.md` | The words, the whole lab in one table (times, parts, client IDs), the two bugs, the three drills and the restore checklist |
| `trading-lab/live/feed.py` | The unfinished-bar fix: a bar counts only once its end is 16 minutes old |
| `trading-lab/live/config.py` | The settle constants (15 minutes of delay plus 1 of margin) |
| `trading-lab/live/risk.py` | Only the lab's own orders count as ours (the desk's `live:desk:`, `live:mcp:`, `live:open:` orders are left alone) |
| `trading-lab/live/kill.py` | The kill switch, which now never touches the desk's orders or its SPY position |
| `trading-lab/live/engines.yaml` | One engine, QQQ only (SPY belongs to the desk's forward test) |
| `trading-lab/scheduler/jobs.py` | The `scanner: false` option (the morning prep updates the data only) |
| `trading-lab/scheduler/schedule.yaml` | What the scheduler runs each day (the scanner back on, as at the end of the lesson) |
| `trading-lab/dashboard/status.py` | The "Everything running" card: every part's state, read-only, and `--hide-engine` for an old card |
| `trading-lab/dashboard/server.py` | The read-only dashboard server (localhost only) |
| `trading-lab/dashboard/__main__.py` | `uv run -m dashboard` and its options |
| `trading-lab/dashboard/index.html` | The dashboard page with the status card |
| `trading-lab/tests/test_live_feed.py` | Tests that a bar the delayed feed may still fill is not final, and is returned only once it settles |
| `trading-lab/tests/test_live_kill.py` | Tests that the kill switch never touches the desk's orders or its SPY position |
| `trading-lab/tests/test_live_runner.py` | Includes the test that a signal first seen after the close places no order |
| `trading-lab/tests/test_scheduler.py` | Tests for the `scanner: false` option |
| `trading-lab/tests/test_dashboard.py` | Tests for the status card (a made-up paper account, DU1234567) |

The files are the lab's state at the end of the lesson. Copy them over your `~/trading-lab` and run `uv run pytest -q`.

## Before you start

- Your `~/trading-lab` (the live engine from module 10, the scheduler, the alerts, the kill switch) and your
  `~/trading-desk` (the heartbeat and the open-window agent from module 15).
- Claude Code in the terminal, signed in with your subscription.
- IB Gateway logged in to a **paper** account, API on port 4002.
- `socat` for the connection drills: on Linux `sudo apt install socat`, on macOS `brew install socat`. On Windows, run
  the drills inside WSL (Ubuntu), or ask Claude for a small Python TCP proxy that does the same job.
- An alert topic on your phone (module 10). Keep its link private.
- A market day for the morning part (US stocks open at 09:30 New York time, 13:30 UTC in October); the drills run after
  the engine has flattened and stopped.

## Try it yourself

1. Before the open, send request 1 in `prompts.md`. Read the plan and answer its questions before anything starts.
2. Clear any old STOP file yourself, then start the desk's parts in their own terminals.
3. After the engine starts, ask Claude to check its first lines and the dashboard (request 5).
4. After the close, plan the drills (request 7), then run them one at a time on paper, never on the scheduled engine.
5. At the end, compare with the baseline and put every setting back (requests 11 and 12).

You're done when each drill ends flat, with an alert you received, and everything is restored to the baseline. Your
times, IDs and Claude's answers will differ from the video, and that's fine.

## Good to know

- **Paper only.** Every drill ran on a paper account. Never run a failure drill against a live-money account.
- **One client ID per part.** Two programs with the same client ID knock each other off the Gateway. Write the IDs down
  and keep other programs' IDs off limits.
- **Real alerts need a real engine.** Dry-run engines send no alerts. If you test alerts with a real engine after the
  close, first check in the code that it can't place an order after the flatten deadline, as we did.
- **Approve deletes by reading them.** The restore asks before `rm`. Read the command first.

Paper account only. Educational content, not financial advice; nothing here is a promise of profit or a recommendation.
