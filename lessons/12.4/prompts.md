# Lesson 12.4 prompts

Everything typed in the lesson, in order. Lines that start with `/` are Claude Code commands. One interactive session in
`~/trading-desk`, auto mode, the desk's MCP server connected, the heartbeat not running. Paper account only.

## 1. Start the loop

```text
/clear
```

```text
/loop 5m You are the desk. Check SPY with your trading-desk tools, follow CLAUDE.md and the skills, and decide for the newest closed 5-minute bar. Act only through the trade tools. End each check with one short line: bar time, decision, why.
```

On our computer `/loop` created a scheduled job (`*/5 * * * *`, "every 5 minutes, next run 4:10 PM"), auto mode's
classifier allowed it, and Claude ran the first check at once: it called the desk's tools, loaded the `market-read` skill,
and answered in 18 seconds:

```text
Bar 11:45-11:50 ET, wait: the daily trend is down, and a long-only desk doesn't buy a downtrend. The data is also about 15 minutes old.
```

It also said the job is session-only and auto-expires after 7 days, and Claude Code added: "Runs until you close this
session · For durable cloud-based loops, use /schedule".

## 2. Steer it between checks

After the second check (4:09 PM, which loaded `market-read` again):

```text
Steering for the next checks: market-read is already loaded in this session, so only reload it if you need a part you don't remember. And add the distance from VWAP to your one-line summary.
```

Claude redid the current line with the VWAP distance ($1.59 above VWAP, about 1.8 atr14). The checks at 4:14 and 4:19 PM
loaded no skill and carried the VWAP distance ($1.93 and $1.86 above).

## 3. Stop it

```text
Stop the loop now, and confirm we are flat with nothing resting.
```

Claude cancelled the job (`CronDelete`), then checked the account: no open positions, no resting orders.

## 4. Compare it with the heartbeat

```text
Compare the last 15 minutes in this session with the Python heartbeat we ran today, using the heartbeat's journal (data/desk/journal.jsonl) and what you did here: decisions per bar, timing, what each one saw, usage, and how each would fail. Then tell me when I should use which.
```

Claude read the last 8 of 27 journal records and said its own timing and usage were partly estimated. Its table is in
`cheat-sheet.md`.

## Pause and try

1. In your desk folder, start a loop every five minutes with your own desk prompt, and let it run three or four checks.
2. Steer it once while it runs, and see that the next check follows.
3. Stop it, confirm you're flat, and ask Claude to compare it with your heartbeat's journal.

You're done when the loop is cancelled, the account is flat with nothing resting, and you can say in one sentence when
you'd use each one.
