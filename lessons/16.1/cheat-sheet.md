# Lesson 16.1 cheat sheet: One machine, the whole lab

## The words

| Word | Meaning |
|---|---|
| Failure drill | You cause a failure on purpose, to check the system handles it |
| Fail safe | When something breaks, the system ends in the safest state, with no new risk |
| Usage budget | The Claude usage you plan for a day. The engine uses none; the desk asks Claude on every bar |

## The whole lab on one machine (our Monday)

| When (UTC) | Part | IB client ID | Notes |
|---|---|---|---|
| all day | IB Gateway, paper | | port 4002, logged in before the session |
| 13:00 | Data update | 5 | shares IB's history limit with the scan and the desk |
| about 13:02 | Gap scan | 4 | skipped on our Monday (`scanner: false`) |
| 13:25 | Live engine (module 10), QQQ only | 6 | started by the scheduler; flattens 19:55, stopped 20:05 |
| from 12:38 | The desk's heartbeat, SPY | 8 | started by us, in its own terminal |
| from 12:38 | The desk's open-window agent, dry run | 10 | started by us, in its own terminal |
| after the close | Journal import, read-only | 7 | |
| always | One dashboard | none | reads the lab's and the desk's files, read-only |

The desk's IDs 8, 10, 20 and 30 are off limits to the lab. Our engine's limits: 10 shares and $8,000 per position, 4
trades a day, $500 daily loss.

## Two bugs found before anything started

- **The unfinished bar.** With delayed data, IB's newest bar can still be filling about 15 minutes after the clock says
  it ended. Our own bar-delay log showed bars first seen 11 to 14 minutes after their close. The fix: a bar counts only
  once its end is 16 minutes old (`closed_bars` in `live/feed.py`, constants in `live/config.py`). The engine now sees
  each bar 16 to 20 minutes after it closes, and signals older than 30 minutes are skipped: about 10 minutes of room.
- **The desk collision.** The desk's order references also start with `live:` (`live:desk:`, `live:mcp:`, `live:open:`),
  so the lab's kill switch would have cancelled the desk's orders, and the desk's buys would have counted toward the
  lab's trade limit. Now only the lab's own orders count as ours (`live/risk.py`), with tests that the kill switch leaves
  the desk's SPY orders and shares alone.

Still worth knowing: the account-wide loss limit counts the whole paper account, so a loss on the desk's SPY can pause
the engine's QQQ buys.

## The three drills

| Drill | How | What should happen | What we saw |
|---|---|---|---|
| 3. Usage limit | A test outside both repos makes the desk's Claude call fail three ways (usage-limit exit, error result, timeout) | Flat desk: no entry, no order, no halt. Position open: the stop stays at the broker and the Python seatbelt still flattens before the close. Limit resets: trading resumes | 7 of 7 tests passed, nothing in the desk changed |
| 1. Short cut | A drill engine connects through a proxy (port 7497 to 4002); the proxy is killed for about 25 s | Socket disconnect, reconnect on the next loop, the lost and back alerts, a clean reconcile | Cut 20:07:16, back 20:07:41; never shown as a halt |
| 2. Long outage | The proxy is killed for about 100 s, longer than the 60-second reconnect window | Connection lost, 6 failed reconnects 10 s apart, a halt, the halt alert, the engine exits | Halted at 20:12:59; the card showed it at 100 s; no orders in either drill |

Rules we kept: never cut the scheduled engine or the Gateway; one drill at a time; drills 1 and 2 only after the engine
had flattened and stopped; a baseline before, a comparison after.

## Restore checklist

- The proxy killed and its port closed; no drill engine left running.
- The drill's state folder deleted (Claude Code asked before the `rm`; read the command, then approve).
- `data/live` compared with the baseline: identical except SQLite's two housekeeping files (`-shm`, `-wal`).
- Not touched: the real engine's state, the STOP file, the scheduler, the dashboard, the desk.
- What you can't undo: the alert history on your alert topic. Keep the topic link private: anyone with it can read your
  alerts.

## Good to know

- **Plan before anything starts.** Ask for the plan, answer its questions, then let it start things.
- **Dry run sends no alerts.** To test real alerts, Claude ran a real engine after the close. Check in the code that it
  can't place an order after the flatten deadline before you allow that, or keep it dry and test the alerts another way.
- **A STOP file blocks the engine.** Claude Code's auto mode won't remove a kill switch for you. Check who wrote it, then
  clear it yourself: `! uv run -m live.kill --clear`.
- **The scheduler reads its settings at startup.** After changing `scheduler/schedule.yaml`, restart it.
- **Usage.** While the usage limit is hit, the desk still calls Claude on every bar and each call fails safely: safe, but
  wasted. Plan the day's Claude usage like any other budget.

Paper account only. Educational content, not financial advice; nothing here is a promise of profit or a recommendation.
