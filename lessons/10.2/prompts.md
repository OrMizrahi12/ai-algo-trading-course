# Lesson 10.2 prompts and commands

Everything typed in the lesson, in order. Requests go to Claude Code (in auto mode). Lines in `bash` blocks were typed
in our second terminal, the one we call "live engine", inside the `trading-lab` folder. Every command here talks to IB
Gateway logged in to the **paper** account, and the order commands only work during the regular US session
(09:30-16:00 New York time).

## 1. Brackets with a memory

```text
/clear
```

```text
Make the live/ order path survive restarts. 1) Every entry is one bracket: the marketable limit parent plus the stop and optional target as OCA children, sent together, children sized to what actually filled. 2) An idempotent orderRef built from strategy, symbol, session date and signal bar time: before sending, check open orders and today's executions for that ref and never send it twice. 3) Tests with the fake IB, including a restart between send and fill. Then give me a way to prove it on paper today without waiting for a signal: a one-share test entry on SPY through the same live/ code, which I can run twice to show the second run sends nothing. Paper only, 1 share, flat at the end.
```

In the video this took about 15 minutes (484 tests, commit `358beb4`). Claude loaded the paper-guard skill first, found
and fixed a gap (a refused stop left the held entry to vanish quietly; now it halts), and disabled its own duplicate
check for a moment to prove that five tests fail without it.

## 2. The proof, twice

```bash
uv run -m live.proof
```

Run it, then run it again the same day:

```bash
uv run -m live.proof
```

In the video: run 1 bought 1 SPY at 762.32 with its stop and target, sold it at 762.30, cancelled the stop and target
(the `Error 202 ... Order Canceled` lines are expected), and printed `orders sent by this run: 4`, `end state: SPY flat,
no open orders`, `RESULT: OK`. Run 2 printed `the ref is already known, so NOTHING is sent`, `orders sent by this run: 0`
and `RESULT: OK (the ref was not sent twice)`.

## 3. Quieter console

```text
I ran the proof twice on paper. Run 1: 1 SPY bought at 762.32 and sold at 762.30, 4 orders, flat, RESULT OK. Run 2: the ref was found, 0 orders sent, OK. Two problems: the console is flooded with ib_async's raw INFO lines (keep them in the log file only), and the earlier orders print as "order #0" (show IB's permId instead). Fix both, test, commit.
```

About 3 minutes (commit `8fb3bbd`). Then the third run, now readable:

```bash
uv run -m live.proof
```

## 4. Risk limits and a kill switch

```text
Now put risk limits outside the strategy. live/risk.py reads limits from a YAML (max shares and max position value per symbol, max trades per day, a daily loss limit) and checks them before every order leaves the program; a refused order is logged with the reason. Remember the paper account is about $1M, so the YAML must cap size well below what 1% risk would allow. Add a kill switch: uv run -m live.kill cancels all our orders, sells our positions and writes a STOP file that the runner checks every loop and on start. Tests first. Then prove it on paper now: open a 1-share SPY position with its resting stop through our own code, run the kill switch, show we are flat with no open orders, and show the runner refusing to start while STOP exists.
```

About 9 minutes (523 tests, commit `b268b49`). Claude ran the paper demo itself and checked the result on a separate,
read-only connection instead of trusting the kill switch's own report.

## 5. The kill switch, by hand

```bash
uv run -m live.kill --clear
uv run -m live.proof --keep --name kill_demo2
uv run -m live.kill
uv run -m live --strategy opening_range_breakout --symbol QQQ --set range_minutes=15
echo $?
cat live/risk_limits.yaml
uv run -m live.proof --name stop_check2
```

What each one does: remove the STOP file; buy 1 SPY and leave it open with its stop and target resting at IB (`--keep`;
any new `--name` gives a new ref); the kill switch (STOP file, cancel our orders, sell, check flat); the runner refuses
to start while STOP exists; `echo $?` prints its exit code, 3; the limits; a buy attempt while STOP exists is refused
(`RISK REFUSED: STOP file exists ... Nothing was sent`). We left STOP in place.

## 6. The failure drills

```text
I repeated your kill switch demo by hand and it works; STOP is still in place. Now the failures, for real on paper, before the 4 PM close. First add fake-IB tests for partial fills and IB rejects if any are missing. Then: 1) get IB itself to reject an order through our Broker (an invalid price increment or whatever IB really refuses) and show it is logged with IB's code and reason, with no retry loop; 2) show what the runner does when the API connection drops while it runs: reconnect, reconcile, carry on or halt. Tell me exactly what to run in my other terminal and what you will do to drop the connection. Clear STOP only when we need it, and leave us flat.
```

Claude found bugs that were already there (a refused order read as "not filled", a refused exit re-sent up to 4 times,
no reconnect at all), fixed them with tests (540 tests, commits `2680378`, `282c121`, `4c12ba3`), made IB refuse an order
with `uv run -m live.probe reject` (error 110, "The price does not conform to the minimum price variation for this
contract"), and set up a relay on port 7497 in front of the Gateway so it could cut the connection without touching the
Gateway. The runner command it gave us:

```bash
uv run -m live --strategy opening_range_breakout --symbol SPY --set last_entry_minutes_before_close=600 --port 7497
```

`last_entry_minutes_before_close=600` means it can never enter a trade, so the drill can't buy anything.

The first run crashed when the relay went down. Our report:

```text
It did not reconnect. The runner started fine on 7497 (reconcile OK), then crashed within seconds of the drop: ConnectionError: Socket disconnect, raised from ib.sleep(POLL_SECONDS) in runner.run, a full traceback, back at the prompt. No "connection lost" line, so your script is probably still waiting. Fix it so a drop during the sleep is caught and goes through the reconnect path, add a test that raises from sleep like this, then tell me when to run it again. We have about 35 minutes before the close.
```

After the fix (192 live tests, commit `1965ac6`) we ran the same runner command again: a short outage reconnected and
reconciled, a long one made 6 attempts 10 seconds apart and halted cleanly.

## 7. Cleanup and the failure table

```text
Both worked on my console. A: connection lost, attempts 1 to 3 failed, back, reconcile OK, bars carried on. B: six failed attempts 10 seconds apart, then HALT and a clean exit. Do the cleanup now: stop the relay, re-arm STOP, check we are flat with no open orders, commit, and give me a short table of every failure we handled today and how.
```

Before your next paper session: `uv run -m live.kill --clear`.

## 8. Pause and try

1. Make entries brackets with an idempotent ref (request 1), then run the proof twice (part 2). The second run must
   send 0 orders.
2. Add the limits and the kill switch (request 4), open one share with `--keep`, and kill it (part 5).
3. Drill one failure: a reject (`uv run -m live.probe reject`) or a dropped connection (request 6).

You're done when your second proof run sends zero orders, the kill switch leaves you flat with STOP in place, and your
runner reconnects after a short drop or halts cleanly after a long one.
