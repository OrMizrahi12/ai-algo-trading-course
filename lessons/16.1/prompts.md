# Lesson 16.1 prompts: One machine, the whole lab

Every request typed in the lesson, in order, and what Claude did with each one. All of it ran on a **paper account**.
Your times, IDs, commits and Claude's answers will differ from ours, and that's fine.

## Monday morning, before the open (12:20 UTC, in the lab's Claude Code)

### 1. Ask for the whole lab, and a plan first

```text
Today we run the whole lab on one machine, starting before the 13:30 UTC open. On it: the Gateway (already logged in,
paper), this morning's data update, the live engine from module 10 with the factory's strategies, the AI desk in
~/trading-desk (its forward test starts today: plain heartbeat on SPY, client 8), and the desk's open-window agent in dry
run (client 10). One rule: the forward test must stay clean, so nothing else trades SPY or touches the desk's code.
First, the live engine has the same unfinished-bar flaw we found in the desk: fix it, with a test. Then give me the
morning sequence: what starts in which order, with which client ID, limits and logs, and how we watch all of it on one
dashboard. Show me the plan before you start anything.
```

Claude read the feed code first, read-only, and showed a plan without starting anything: Step 1, the unfinished-bar flaw
(no real-time data, bars arrive 15 to 20 minutes late, so the newest bar IB returns can still be forming); Step 2, the
sequence (13:00 data update on client 5, about 13:02 a gap scan on client 4, 13:25 the engine on QQQ only on client 6,
20:05 the scheduler stops it, after the close the journal import on client 7, read-only), a pacing risk, the desk's IDs
(8, 10, 20 and 30) kept off limits, alerts and an emergency stop that touches only our orders; Step 3, one dashboard
with a status strip. It also found two things it didn't create (an unpushed commit and today's gap scan file) and asked
three questions.

### 2. Our answers

```text
1) QQQ only today. 2) Yes, read the desk's fix, read-only. 3) I start the heartbeat and the dry-run agent myself, each
in its own terminal. Their journals are under ~/trading-desk/data: read them read-only for the dashboard. Push
<the unpushed commit>. The gap scan file came from the open-window agent this morning: it found nothing, IB refused the
scan before the open. Keep it out of git and skip the 13:02 scan; the agent reruns it at 13:50. Go ahead: fix and test
first, then start the scheduler and the dashboard.
```

Claude worked for about 14 minutes. It read the desk's fix and wrote the same rule into the lab's feed with the lab's
own constants (a bar counts only once its end is 16 minutes old). It found a second bug: the desk's orders carry the
same `live:` prefix as the lab's, so our kill switch would have cancelled them and their buys would have counted toward
our trade limit. It wrote a test for that (the first run failed, it fixed it until every test passed), removed the SPY
engine, added a `scanner: false` option to the scheduler and a status card to the dashboard, then started the dashboard
and the scheduler. When it tried to clear an old STOP file, Claude Code's auto mode refused (removing a kill switch
weakens a safety control), so it left the file for us.

### 3. Clear the old STOP file yourself (shell mode)

Type an exclamation mark in Claude Code's prompt, then the command:

```text
! uv run -m live.kill --clear
```

It printed `STOP file removed.` and Claude checked that the dashboard and the scheduler were still running.

### 4. Start the desk, each part in its own terminal

```bash
cd ~/trading-desk && uv run -m desk          # the heartbeat on SPY, client 8
uv run -m desk.openwindow                    # a second terminal: the open-window agent, dry run by default, client 10
```

Then open the dashboard (ours ran at `http://127.0.0.1:8765`).

## 13:26 UTC: the engine's first lines

### 5. Check the start

```text
It's 13:26 UTC and the scheduler started the engine. Check its first lines, the data update and the dashboard card,
and tell me if anything looks wrong before the open.
```

The engine connected to a paper account on port 4002 as client 6, reconciled clean (flat, no open orders), caught up
through Friday's last bar and skipped a three-day-old entry signal. The data update ran clean but covers only AAPL and
SPY (the engine reads its bars from IB directly). One wrong guess: Claude thought the desk wasn't running.

### 6. Correct it

```text
Both desk parts are running: I started them at 12:38 in their own terminals, so Friday's bar is simply the newest bar
there is. Leave the data list as it is. Yes, hide the stale SPY card, commit, and we wait for the open.
```

On the way, a `pkill` command matched its own shell. Claude checked that the engine and the scheduler were untouched,
restarted only the dashboard with the stale card hidden, and committed.

## After 19:00 UTC: failure drills, on paper

### 7. Plan the drills

```text
It's past 19:00 UTC and the desk's entry window is over, so we run the failure drills now, on paper. One: cut the API
connection briefly and show that the engine and the desk reconnect and reconcile. Don't log out or restart the Gateway
itself: its password isn't available here. Two: a longer outage, so we see the alerts fire. Three: a usage-limit error
from claude -p, simulated in a test outside the desk's code, showing the desk stops entering while the Python layer
still manages the position. Nothing in the desk's code changes. Plan first, then run them one at a time, and at the end
tell me exactly what you restored.
```

Claude planned a safe cut: a separate drill engine connects through a small proxy (`socat`, port 7497 to the Gateway's
4002), and only the proxy is killed. The desk always connects to 4002, so the desk got an offline test instead. Drill 3
first; drills 1 and 2 after 20:05, once the engine has flattened and stopped.

### 8. Go

```text
Go. Yes to the offline test for the desk, and yes to real alerts for drill two. Start with drill three now; drills one
and two after 20:05 as you planned.
```

Drill 3: a test outside both repos imports the desk's model code read-only and makes the Claude call fail three ways (a
usage-limit exit, an error result, a timeout). 7 of 7 tests passed: with a flat desk, no entry and no order over three
bars and no halt; with a position open, the stop stays at the broker and the Python seatbelt still flattens before the
close; when the limit resets, the desk trades again.

## 20:05 UTC: drills one and two

### 9. Run them

```text
It's 20:05 UTC. The engine has flattened and the scheduler has stopped it. Run drills one and two now, show me the log
lines, the alerts and the dashboard card, and restore everything after.
```

Claude saw that dry-run engines don't send alerts, so it started a different strategy on QQQ as a real engine, in a
fresh, separate state folder, after a baseline of the journal.

### 10. A check, typed while it worked

```text
One check before the non-dry engine runs: show me in the code that it cannot send any order after the close, or keep
it dry and test the alerts another way.
```

The message waited in the queue while drill 1 ran. When it landed, Claude stopped the engine first, said it should have
asked before starting a real engine, showed the check in the code that blocks every entry after the flatten deadline,
and pushed a new test that proves it.

### 11. Drill two

```text
Good, that's enough proof. Run drill two with the real alerts, then restore everything and compare data/live with the
baseline.
```

The proxy was cut for about 100 seconds. The engine lost the connection, failed 6 reconnect attempts 10 seconds apart,
halted and sent the halt alert. The restore asked before deleting the drill folder (a permission rule on `rm`); we read
the command and approved it.

### 12. Put the scanner back

```text
Set the scanner back to true and commit. That's the drills done.
```

Claude committed and restarted the scheduler so it reads the file again, and flagged one thing for tomorrow: the morning
scan and the open-window agent's scan share IB's history limit.

## Pause and try

1. Ask Claude for your own morning sequence, with a client ID, limits and logs for every part, and a plan before
   anything starts.
2. On paper, run a short and a long connection drill through a proxy, never on the scheduled engine.
3. Simulate a usage-limit error in a test, and check that nothing new gets entered.

You're done when each drill ends flat, with an alert you received, and everything is restored to the baseline.
