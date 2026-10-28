# Lesson 12.4 cheat sheet: the always-on desk

## Words

| Word | Meaning |
|---|---|
| `/loop` | A Claude Code command that repeats a prompt on an interval, inside the session (`/loop 5m <prompt>`) |
| Scheduled job | What `/loop` creates under the hood (`CronCreate`, here `*/5 * * * *`); `CronDelete` cancels it |
| Push | The heartbeat: Python builds a snapshot and pushes it to Claude on every bar |
| Pull | The always-on desk: Claude fetches what it wants with its own tools on every check |
| Context drift | One long session keeps piling up history; compaction has to summarize it sooner or later |
| Steering | A message you type between checks; the next checks follow it |

## How `/loop` behaved on our computer

- The first check runs at once; then the job fires about every 5 minutes.
- Session-only: it auto-expires after 7 days and runs only until you close the session. For durable loops Claude Code
  points to `/schedule`.
- It fires only between turns, when the session is idle; a missed fire is not caught up, so a bar can be missed.
- A `*/5` job is not delayed: each run starts about 4 minutes 45 seconds after the previous one (that is why our second
  check came at 4:09, not 4:10). Claude said in its table that the scheduler "can run up to 50% of the period late"; that
  is true for other intervals, not for every 5 minutes (Claude Code docs, scheduled tasks).
- Each check is a full Claude turn: our four checks took 18, 6, 7 and 5 seconds of model time, plus the waits.

## Heartbeat or loop: Claude's comparison (our run, partly estimated)

| | Python heartbeat | This session (the `/loop`) |
|---|---|---|
| Decisions | wait on every bar: daily downtrend, about 2 atr14 above VWAP, thin volume on several bars | wait on all four checks: daily downtrend, 1.8 to 2.2 atr14 above VWAP |
| Timing | 3.9 to 13 s per bar, far inside the 120 s budget; fires on every bar, never skips | tens of seconds per check; fires only when the session is idle, can miss a bar (Claude also said "up to 50% late": not for a 5-minute loop) |
| What it saw | a fixed snapshot: about 58 KB at the start of a session, then deltas of about 2.9 KB | whatever Claude chose to fetch: positions, 5-minute and daily indicators, sometimes the quote and the journal |
| Usage | logged per bar | not logged; the context keeps growing across checks |
| Skills | the skills field was empty on the bars Claude read | loaded market-read on the flat bars |
| Safety | schema-validated output, invalid answers become wait; the seatbelts and the STOP file | no schema check; only the trade tools' own limits |

## How each one fails

- **Heartbeat:** misses whatever its snapshot doesn't contain; every instruction change forces a full resend (three
  instruction versions within about 25 minutes that day); invalid output becomes wait, so a bug fails toward doing
  nothing.
- **Loop:** dies when the session closes; can miss or delay bars; nothing validates a skipped skill or a slip in
  judgment; its trade tools can't touch the heartbeat's shares.

## When to use which

| Use | When |
|---|---|
| The heartbeat | Any unattended or all-day run, anything you want reproducible, any time money (even paper money) is at risk. It has the validator, the seatbelts, a cost log and a per-bar journal |
| The always-on session | A short, supervised stretch: testing a new skill or prompt, looking into a bar or the journal, manual cleanup. Stop the loop once you step away |
| Never | Both at once: neither can manage the other's position |

## Ending a loop session

1. Ask Claude to stop the loop (it calls `CronDelete`), or close the session.
2. Confirm with the trade tools: no open positions, no resting orders.
3. Start the next run in a fresh session.
