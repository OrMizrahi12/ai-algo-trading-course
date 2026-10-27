# Student kit: Lesson 10.3, Running unattended

Module 10: From backtest to live on paper · AI Algorithmic Trading with Claude Code and Interactive Brokers

In Lessons 10.1 and 10.2 the engine ran while we watched it. In this lesson it learns to run itself:

1. **The trading day, in New York time.** Prep at 09:00 (the bar cache and the gap scanner), the engine at 09:25,
   flatten at 15:55, stop and a daily report at 16:05, from the NYSE calendar: holidays skipped, half days ending early,
   daylight saving handled.
2. **A scheduler, planned and checked.** Claude finds no systemd, cron or `at` on our computer and builds a small Python
   scheduler in the Lab. We check its next runs and a dry run ourselves, find two problems, and get them fixed with tests.
   The STOP file (the kill switch from Lesson 10.2) wins: while it exists, the runner is never started.
3. **Several strategies in one engine**, over one IB connection, each with its own state, limits and daily log, and
   **alerts** through ntfy to a private topic, for the moments that need a human.
4. **A slip with the kill switch.** Claude moves the STOP file by mistake, says so, and doesn't work around auto mode's
   refusal to let it move the file back. We restore it ourselves.
5. **Living with the Gateway:** its nightly auto restart, the weekly login, and what still needs a person.

## What's in this kit

| File | What it is |
|---|---|
| `prompts.md` | The requests typed in the lesson, the commands we ran, and the pause-and-try exercise |
| `cheat-sheet.md` | The words, the trading day in New York time and UTC, the scheduler file by file, the commands, several strategies, alerts, the Gateway around your schedule |
| `running-every-day.md` | The README sections Claude wrote: the daily schedule, the systemd timer, cron, launchd and Task Scheduler versions, several strategies, alerts |
| `agents-md-entries.md` | The `AGENTS.md` lines Claude added (`scheduler/`, several strategies, alerts, client ID 6 for every pair) |
| `trading-lab/scheduler/` | The scheduler as it was at the end of the lesson (Lab commit 43aff85): `plan.py`, `jobs.py`, `report.py`, `__main__.py`, `schedule.yaml` |
| `trading-lab/live/` | The new and changed engine files: `multi.py`, `engines.py`, `engines.yaml`, `daily_log.py`, `alerts.py`, and the updated `__main__.py`, `runner.py`, `broker.py`, `kill.py` |
| `trading-lab/tests/` | `test_scheduler.py` (fake clock, fake subprocesses), `test_live_multi.py` and `test_live_alerts.py` (fake IB, fake sender, no network) |

No new dependency: the scheduler uses `exchange_calendars`, `pandas` and `pyyaml`, already in the Lab.

## Before you start

- The Trading Lab with the live engine from Lesson 10.1 and the order management, risk limits, kill switch and reconnect
  handling from Lesson 10.2 (`live/risk.py`, `live/risk_limits.yaml`, `live/kill.py`).
- IB Gateway logged in to the **paper** account, API port 4002, with its auto restart set (Module 4).
- Claude Code in the terminal, signed in with your subscription. Plan mode for the plan, then auto mode.
- For alerts: nothing to install. A browser tab, or the free ntfy app on your phone.
- Time on our computer: about 2 minutes to plan, about 7 minutes to build the scheduler, half a minute for the fixes,
  about 14 minutes for several strategies and the alerts.

## Try it yourself

1. `/clear`, plan mode (Shift+Tab), and send request 1 in `prompts.md`. Read what Claude finds on your machine before you
   approve.
2. In a second terminal, run `uv run -m scheduler --next 5`, a `--next` around your next holiday, and
   `uv run -m scheduler --today --dry-run`.
3. Send request 4, then create your own topic with `! uv run -m live.alerts --init`.
4. Send a test alert, and check that `data/live/STOP` is still there.

You're done when the next runs skip the holidays, the dry run refuses the runner while the STOP file exists, and a test
alert reaches you. Your dates, test counts and Claude's replies will differ from the video, and that's fine.

## Good to know

- **The topic is a secret.** ntfy has no password: anyone who knows the topic name can read your alerts and post to it.
  Use the long random one `--init` makes, keep `.env` out of Git, and never show the topic in a screenshot or a chat.
- **The kill switch wins.** The scheduler never clears `data/live/STOP`. Clearing it (`uv run -m live.kill --clear`) is
  your decision, not Claude's and not the scheduler's.
- **Check the safety switches yourself.** In the video Claude moved the STOP file by mistake. A permission rule or hook
  that blocks moving or deleting `data/live/STOP` is a good next guardrail.
- **The Gateway is not scheduled.** It restarts itself every night and needs you to log in again once a week. On our
  computer one auto restart ended logged out. Check it every morning before 09:00 New York time.
- **The bars are late.** With free delayed data the newest 5-minute bar keeps filling in for about 15 minutes after its
  end; a later lesson makes the engine decide only on settled bars.
- **A laptop that sleeps is not a server.** The next step for real unattended running is a small always-on machine or a
  cloud server.

## Safety

Paper trading only. The engine refuses a non-paper port, a remote host and any account that doesn't start with `DU`, and
checks again before every order; the scheduler places no orders itself. Educational content, not financial advice;
nothing here is a recommendation or a promise of profit.
