# Lesson 10.3 prompts and commands

Everything typed in the lesson, in order. Lines that start with `/` are Claude Code commands, lines that start with `!`
run in your own shell from inside Claude Code. The scheduler is planned in plan mode, then built in auto mode. IB Gateway
must be logged in to the **paper** account (port 4002) for the engine itself; the scheduler commands below only read the
calendar.

## 1. Plan the trading day (plan mode)

```text
/clear
```

Press Shift+Tab until the footer says "plan mode on", then send:

```text
Make the engine run itself on trading days, in New York time: prep at 09:00 (update the bar cache and run the gap scanner), start the live runner at 09:25, flatten at 15:55, stop and write a short daily report at 16:05. Use the exchange calendar so holidays are skipped and half days end early, and DST is handled. First check what scheduler this Linux machine actually has (systemd user timers, cron, or nothing) and pick the simplest reliable option; explain the choice. Put the Windows Task Scheduler and macOS launchd equivalents in the README. Respect the STOP file: a scheduled start must not clear it. Show me the next scheduled runs at the end.
```

On our computer Claude found no systemd, no cron and no `at`, and a clock on UTC, so it chose a small Python scheduler in
the repo (`scheduler/`) built on the NYSE calendar. On your machine it may choose a systemd timer, cron, launchd or the
Task Scheduler instead, and that's fine: the rules below stay the same. We chose "Yes, and use auto mode". The build took
about 7 minutes (27 scheduler tests, Lab commit `5c807f6`).

## 2. Check it yourself (a second terminal)

```bash
uv run -m scheduler --next 5
uv run -m scheduler --next 4 --from 2026-11-24
uv run -m scheduler --today --dry-run
```

The first shows the next five sessions in New York time and in UTC. The second shows the Thanksgiving week: November 26
is skipped and November 27 is a half day (flatten 12:55, stop 13:05). Pick dates around the next holiday or half day of
your own year. The dry run prints today's plan and runs nothing.

## 3. The two things we found

```text
I ran --next 5, --next 4 --from 2026-11-24 and --today --dry-run. Thanksgiving and the half day are right. Two things: the "UTC offset" column header is there but the column is empty, and --today --dry-run says "would run: opening_range_breakout QQQ" although the STOP file exists, so it should say the runner would be refused. Fix both with tests and commit.
```

Half a minute later: Lab commit `bb07911`, 30 scheduler tests. Run the same commands again:

```bash
uv run -m scheduler --next 3 --from 2026-11-25
uv run -m scheduler --today --dry-run
```

With the STOP file from Lesson 10.2 in place, the dry run says the runner would be refused and prep would still run.

## 4. Several strategies and alerts

```text
Next: run more than one strategy at once. Let one engine process run several (strategy, symbol) pairs from a config file, for example ORB on QQQ and Donchian breakout on SPY, over ONE IB connection with one client ID, each with its own state, limits from risk_limits.yaml, and its own daily log file (one file per day). Then alerts: send a short push message through ntfy.sh to a private random topic kept in .env (not committed) for fills, rejects, a halt, a lost connection and the kill switch, never for routine bars. Tests with the fake IB. At the end send one test alert and give me the ntfy web link for the topic so I can watch it in Chrome. Use plan mode thinking but go ahead and build.
```

About 14 minutes in the video, 634 tests, Lab commit `43aff85`. Claude can't read or edit `.env` (our permission rules
deny it), so the topic is created by you:

```text
! uv run -m live.alerts --init
```

Then Claude sends one test alert (`uv run -m live.alerts --test`). The topic is the only secret: never paste it into a
chat, a commit or a screenshot.

## 5. Put the kill switch back (only if it is missing)

In the video Claude moved `data/live/STOP` into its scratchpad by mistake, and auto mode refused to let it move the file
back. Claude gave us the exact command with its own scratchpad path; we ran it ourselves and read the file back:

```text
! mv <the path Claude gives you>/STOP.bak data/live/STOP && ls -la data/live/STOP && cat data/live/STOP
```

Check that `data/live/STOP` exists before any scheduled day. Clearing it (`uv run -m live.kill --clear`) is your decision.

## 6. Did the alert arrive?

```bash
set -a; . ./.env; set +a; curl -s "https://ntfy.sh/$NTFY_TOPIC/json?poll=1" | python3 -m json.tool
cat live/engines.yaml
```

The first asks the ntfy server for the topic's messages without printing the topic. Or subscribe to your topic in the
ntfy phone app and watch the test alert arrive as a notification.

## Pause and try

1. Plan the scheduler in plan mode with request 1, then check `--next` and `--today --dry-run` yourself.
2. Add the engines file and the alerts (request 4), and create your own long, random topic with `--init`.
3. Send a test alert, and make sure `data/live/STOP` is still in place.

You're done when the next runs skip the holidays, the dry run refuses the runner while the STOP file exists, and a test
alert reaches you. Your dates, test counts and Claude's replies will differ from the video, and that's fine. Paper
account only.
