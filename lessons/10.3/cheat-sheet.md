# Lesson 10.3 cheat sheet: Running unattended

## The words

| Word | Meaning |
|---|---|
| **Scheduler** | What starts the jobs at set times. On Linux a systemd timer or cron, on Windows the Task Scheduler, on a Mac launchd. In the Lab: `scheduler/`, a small Python scheduler that can also be started by any of them |
| **Exchange calendar** | The list of trading days, half days and session times. The Lab uses the NYSE calendar from `exchange_calendars` |
| **Half day** | A shortened session (the market closes at 13:00 New York time), for example the Friday after Thanksgiving |
| **Alert** | A short push message to your phone or browser when something needs a human: a fill, a rejected order, a halt, a lost connection, the kill switch. Never for routine bars |
| **Daily log** | One log file per day per engine, `data/live/<strategy>_<symbol>/logs/YYYY-MM-DD.log`, so a month later you can still find a day |
| **ntfy topic** | The private channel name your alerts go to. There is no password: whoever knows the name can read and post. Treat it like a password |
| **STOP file** | `data/live/STOP`, the kill switch from Lesson 10.2. While it exists the runner refuses to start and every buy is refused. The scheduler never clears it |

## The trading day (New York time)

| Job | Full day | Half day | What happens |
|---|---|---|---|
| prep | 09:00 | 09:00 | update the bar cache (`data_pipeline`), then the gap scanner (`scanner.py`) |
| runner start | 09:25 | 09:25 | `python -m live ... --flatten-before-close-min 5`, five minutes before the open |
| flatten | 15:55 | 12:55 | the runner sells anything it holds (close - 5 min) |
| stop + report | 16:05 | 13:05 | the runner is stopped like Ctrl+C, `data/live/reports/YYYY-MM-DD.md` is written (close + 5 min) |

Every time is built in New York time and only then converted to UTC, so daylight saving never shifts the day:

| | New York | UTC in summer (EDT, UTC-4) | UTC in winter (EST, UTC-5) |
|---|---|---|---|
| prep | 09:00 | 13:00 | 14:00 |
| runner | 09:25 | 13:25 | 14:25 |
| flatten | 15:55 | 19:55 | 20:55 |
| stop | 16:05 | 20:05 | 21:05 |

## The scheduler (Lab commits 5c807f6 and bb07911)

| File | What it does |
|---|---|
| `scheduler/plan.py` | The day's timetable from the NYSE calendar: prep and runner at fixed New York times, flatten and stop as offsets from the real close |
| `scheduler/jobs.py` | Runs the day: prep, then the runner as a subprocess (restarted up to 3 times if it dies before the flatten time, never after a halt or STOP), then the stop. It places no orders; a fake clock lets the tests run a whole day |
| `scheduler/report.py` | The daily report, from files only (no IB connection): jobs, scanner top 5, decisions, trades, risk refusals, a halt, NOT FLAT if a position is still open |
| `scheduler/__main__.py` | The command line below |
| `scheduler/schedule.yaml` | Which strategy and symbol the runner starts (or `engines: live/engines.yaml` for several) |
| `tests/test_scheduler.py` | A normal day, the half day, a holiday, both clock changes, the STOP file, late starts, restarts, the report |

```bash
uv run -m scheduler --next 5                      # the next 5 trading days, New York and UTC (read-only)
uv run -m scheduler --next 4 --from 2026-11-24    # from a date: holidays skipped, half days marked
uv run -m scheduler --today --dry-run             # today's plan; runs nothing; says if STOP refuses the runner
uv run -m scheduler --today                       # run today's session, then exit (at once on a holiday)
nohup uv run -m scheduler >> data/live/scheduler.log 2>&1 &    # the daemon: every trading day until you stop it
```

The daemon lives only as long as its process: if the machine restarts, start it again (or let your operating system
start `--today` each weekday morning, see `running-every-day.md`). The IB Gateway must be running and logged in; the
scheduler does not start it.

## Several strategies, one engine (Lab commit 43aff85)

```yaml
# live/engines.yaml
engines:
  - strategy: opening_range_breakout
    symbol: QQQ
    settings: {range_minutes: 15}
  - strategy: donchian_breakout
    symbol: SPY
```

```bash
uv run -m live --config live/engines.yaml --dry-run    # decisions only, no orders
uv run -m live --config live/engines.yaml              # paper orders
```

- One process, one IB connection, one client ID (6). Each pair has its own state file, reconcile, orders and daily log.
- The pairs take turns in a single thread, once a minute. One pair halting does not stop the others; STOP stops all.
- One engine per symbol: IB keeps one position per symbol. A symbol without limits in `risk_limits.yaml` is refused.
- After a reconnect, every pair reconciles, not only the one that noticed.

## Alerts (ntfy)

```bash
uv run -m live.alerts --init    # creates a random NTFY_TOPIC in .env (never overwrites, never committed)
uv run -m live.alerts --test    # sends one test alert
uv run -m live.alerts --link    # prints the browser link
```

- Sent for: fills, rejects (by IB or by your risk limits), halts, a lost connection and its return, the kill switch.
- Never for routine bars, skipped signals or dry runs. No account number in the text.
- Sending runs in the background; a failed send is only logged and can never stop trading.
- Subscribe to the topic in the ntfy phone app or a browser tab. If the topic leaks, delete the `NTFY_TOPIC` line from
  `.env` and run `--init` again.

## The Gateway around your schedule

- **Every night:** the Gateway's auto restart (Configure, Settings, Lock and Exit; set in Module 4). Our computer's clock
  is on UTC, so 11:45 PM there is 7:45 PM in New York, after the close. The engine sees a lost connection, retries,
  reconnects and reconciles before it trades again (Lesson 10.2).
- **Once a week:** you log in again yourself, with your password. No script does that for you.
- **Every morning:** check that the Gateway is logged in before the prep job. On our computer one night's auto restart
  ended logged out and needed the password again.
- A laptop that sleeps is not a server. For real unattended running, the next step is a small always-on machine or a
  cloud server.

## Good to know

- The bars are still late: with free delayed data, the newest 5-minute bar keeps filling in for about 15 minutes after
  its end. A later lesson makes the engine decide only on settled bars.
- Claude slipped once in the video: it moved the STOP file by mistake. Auto mode denied its attempt to move it back, it
  didn't look for a way around that, and we restored the file ourselves. A hook that blocks any move or delete of
  `data/live/STOP` would catch this next time.
