# Lesson 16.2 prompts: Reading the results

Every request typed in the lesson, in order, and what Claude did with each one. All of it ran on a **paper account**, on
Monday evening after the close. Your numbers, IDs, commits and Claude's answers will differ from ours, and that's fine:
the point is the questions, not our results.

## In the lab's Claude Code (`~/trading-lab`, after `/clear`)

### 1. Read everything that ran, honestly

```text
Let's read the results. Walk me through everything that ran on this machine, from the dashboard, the lab's journal
and, read-only, the desk's journals and its forward-test report: the factory strategy and the AI desk, in R where
you can, with today's trades, drawdowns and costs. Show the real numbers, the whole period, no picked dates, and say
what they can and can't tell us.
```

Claude worked for about three minutes, read-only. The judge guard from module 9 blocked one command whose pattern
touched the desk's data folder (the holdout guard); Claude listed the folders explicitly instead. It ran the desk's
forward-test report **sealed**, as the protocol from lesson 15.4 says (one trading day counted, zero closed trades), and
did not unseal it. To see more than one trade, it ran the exact live settings of the factory strategy through the lab's
backtester on the research cache (holdout excluded), and noticed that the backtest measured R as 1% of equity while the
live trade used its real stop distance, so it rescored every backtest trade against its real stop risk.

Its answer, in short: one real strategy trade in the whole record (it won, and that tells us almost nothing); the desk's
157 bars and the variants' 206 bars were all "wait" (nothing to put in R, about $31 of Claude usage logged); the
backtest's 263 trades average +0.12 R with a 95% range that includes zero; and a list of what the numbers can't tell us.
At the end: one thing to look at before the next open (a stop order the desk still saw as live).

### 2. Check the leftover stop, read-only

```text
That matters more than the report. Check the open orders now, read-only. If that stop is still live, cancel it with
the lab's own tools, confirm the account is flat with no open orders, and find out how it was left behind.
```

Claude first checked how the lab's tools connect, so its own check used the same paper-account safeguards, then opened a
fresh read-only paper connection on a free client ID (11). No positions, zero open orders, and IB's completed-orders
list showed the stop as Cancelled, never filled. Nothing was sent and no STOP file was written: a false alarm. The
likely cause (a hypothesis, not tested): the desk's long-lived connection kept an old copy of the order list, because a
client generally isn't told when another client cancels an order. Claude left the desk's code alone and offered to make
the lab's daily report check IB for leftover orders.

### 3. Make the daily report check IB

```text
Good, a false alarm, but a real finding. Yes, add the open-orders check to the daily report, with a test, and commit.
```

Claude kept the report offline by default and added one fresh read-only look at IB at report time (client ID 11, a new
connection every day). The result now reads `LEFT AT IB` when IB still holds a position or an open order in a symbol we
trade, or any order of ours, and `OK (IB not checked)` when the Gateway can't be asked, never a plain OK. Ten new tests
with a fake IB; the whole suite passed (693 tests); committed and pushed. The report still cancels nothing:
`uv run -m live.kill` stays the one tool that does.

## In the desk's Claude Code (`~/trading-desk`), with Obsidian open

### 4. What did the agent learn?

```text
Read the agent journal and lessons in the Obsidian vault: what did the agent learn, which lessons were promoted or
archived, and how did the trader versions change? Keep it short and plain, and fix anything in the vault that is out
of date.
```

About a minute. What the agent learned: nothing real yet (157 decisions, every one "wait"; no trade closed; no decision
used a lesson). Lessons promoted: none for real; the nine "SEED" notes in `Lessons/Archive/` are labelled made-up test
data. The versions, v1 to v2.2, and the one measurable effect so far (the `market-read` skill loaded on 1 of 55 bars in
v2.1, and on 78 of 78 in v2.2). It fixed the out-of-date Trader versions note (the v2.2 row said "not run yet") and
left the experiment ledger alone, because the ledger is for a person to decide.

### 5. What should a learner try next?

```text
Given everything here, what should a learner try next? Three experiments, each with the change, the protocol and what
result would make us drop it. Do not touch the forward test or the plain desk.
```

Three offline replays on saved bars, with no orders, and the drop rule fixed before anyone looks at a result:
(1) the regime gate and the ORB veto replayed without the lab's QQQ position in the snapshots; (2) the team convened on
bars where the analyst proposes a buy; (3) the cost of delayed data, as a share of the stop distance. See
`next-experiments-template.md`.

### 6. Save them, run nothing

```text
Save these three experiments as a note in the vault next to the playbook, then commit the vault changes. Do not run
anything yet.
```

A new note, `vault/Playbook/Next experiments.md`, marked "proposed, nothing run yet", committed with the day's other
vault changes; nothing pushed, nothing run. Claude also pointed out that the playbook folder holds one note per setup, so
a plan doesn't quite fit there, and offered to move it.

## Pause and try

1. Ask Claude (request 1) to walk through everything your lab ran, in R, over the whole period, and to say what it can't
   tell you.
2. Read your agent's journal (request 4) and fix one note that's out of date.
3. Write down one next experiment, with its change, its protocol and its drop rule, before you run it (requests 5 and 6).

You're done when every number you quote comes with its sample size.
