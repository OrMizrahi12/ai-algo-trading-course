# Lesson 10.1 prompts and commands

Everything typed in the lesson, in order. Lines that start with `/` are Claude Code commands. The build runs in plan
mode first, then auto mode. IB Gateway must be logged in to the **paper** account (port 4002) for the dry run, the live
run and the closing check.

## 1. Plan the engine (plan mode)

```text
/clear
```

Press Shift+Tab until the footer says "plan mode on", then send:

```text
Plan a live paper engine in a new live/ package that runs our existing strategies unchanged. Data path: our account has no real-time data, so poll the Gateway once a minute for recent 5-minute historical bars and only use bars that have CLOSED; they arrive about 15 to 20 minutes late, so log the delay of every bar. Add a state file on disk, reconciliation with IB positions and open orders on every start, orders as marketable limits with a timeout, and a runner for one strategy on one symbol. Add a parity test that replays cached bars through the live path and must give exactly the backtester's signals. Paper account only: refuse any account that does not start with DU.
```

The "15 to 20 minutes" came from a test of the data path before filming (Lesson 10.1, "One strategy, two engines").
Measure your own: the engine logs the delay of every bar to `data/live/<strategy>_<symbol>/bar_delay.csv`.

In the video Claude sent two Explore subagents to read the code, then wrote the plan: the files (`config`, `broker`,
`feed`, `state`, `reconcile`, `execution`, `step`, `registry`, `runner`), the tests (a fake IB that fills orders by the
backtester's own rules, the parity test), the build order in six committed steps, and its decisions (a wall-clock
flatten deadline, the stop and target resting at IB as a one-cancels-other pair, a mismatch on start halts, a first
start never trades on old signals, live bars never written to the research cache or the holdout). We chose
"Yes, and use auto mode".

## 2. Build it

After step 1 (the paper guard, checked by the `paper-guard` skill from Module 3):

```text
Good. Continue with steps 2 to 6 without stopping between them, commit after each step, then run the dry run against the Gateway.
```

About 18 minutes in the video, 434 tests at the end. Once, our ask rule for `rm` (Lesson 3.6) stopped auto mode: Claude
wanted to delete the dry run's state file to rerun it. We answered Yes.

## 3. A review before the first trade

```text
Yes, run the lab-reviewer on the live engine before we trade. Fix anything it finds, then commit.
```

The `lab-reviewer` is the Lab's review subagent from Module 3. It found 17 items and no paper-safety problems; Claude
fixed most of them with tests (448 tests, parity still exact, commit `3512adc`) and listed three it left open.

## 4. The first live run (a second terminal)

```bash
uv run -m live --strategy opening_range_breakout --symbol QQQ --set range_minutes=15
```

Stop it with Ctrl+C. Start it again with the same command (Up arrow, Enter).

## 5. A console you can supervise

```text
I started it live in the other terminal. It works, but the console is too quiet to supervise: on start it should print the account (paper DU check), the reconcile result (state vs IB positions and open orders), and every new bar should print its decision, even "no signal". Ctrl+C should shut down cleanly with no traceback. Keep the log file as it is. Tests, then commit.
```

Claude did not open a second Gateway connection while the live run held client ID 6; it tested the console offline,
including a real Ctrl+C sent to a subprocess (458 tests, commit `95dad8b`). Restart the engine to get the new console.

## 6. Close the session, read-only

```text
Confirmed: clean start, reconcile OK, bar lines, clean Ctrl+C. I stopped it for today. Close the session: read-only, check IB that we are flat with no open orders, summarize the bar delays from bar_delay.csv, and tell me what has still never been tested for real.
```

## Pause and try

1. Plan the engine in plan mode with request 1. Read the plan's decisions before you approve.
2. Let Claude build it (request 2), then run the lab reviewer before you trade (request 3).
3. Run it on paper, stop it with Ctrl+C, start it again, and read the reconcile line.

You're done when the parity test passes, a restart prints `reconcile ... -> OK`, and every bar prints its decision. Your
bars, delays and decisions will differ from the video, and that's fine. Paper account only.
