# Student kit: Lesson 12.4, The always-on desk

Module 12: Tools, skills and guardrails · AI Algorithmic Trading with Claude Code and Interactive Brokers

Until now the desk ran on a **heartbeat**: a Python process that wakes on every closed 5-minute bar, builds a snapshot,
and pushes it to Claude in one call with a strict answer format. In this lesson we run the same desk the other way: one
long, interactive Claude Code session in `~/trading-desk`, with the desk's MCP server connected, and the `/loop` command.
Every five minutes Claude wakes up on its own, pulls what it wants with its tools, follows `CLAUDE.md` and the skills,
decides, and may act only through the guarded trade tools. Then we compare the two.

What happened on our computer (paper account, 2026-10-23, the heartbeat not running):

1. `/loop 5m` with the desk prompt created a scheduled job (every 5 minutes), and Claude ran the first check at once.
2. Four checks in about 15 minutes (bars 11:45 to 12:05 Eastern time), four waits: a daily downtrend on a long-only desk,
   with the price stretched above VWAP. No order was sent.
3. Between checks we steered it: "only reload market-read if you need a part you don't remember, and add the distance
   from VWAP". The next two checks did both.
4. We stopped the loop, and Claude confirmed: job cancelled, flat, nothing resting.
5. We asked Claude to compare the session with the heartbeat's journal. Its table is in `cheat-sheet.md`.

No code changed in this lesson, so there are no desk files in this kit: you run the desk you already have.

## What's in this kit

| File | What it is |
|---|---|
| `prompts.md` | Every message typed in the lesson (the loop prompt, the steering message, the stop message, the comparison request) and the pause-and-try exercise |
| `cheat-sheet.md` | The words, how `/loop` behaves, the heartbeat vs loop comparison, how each one fails, and when to use which |

## Before you start

- Your `~/trading-desk` from lessons 12.1 to 12.3: the MCP server in `.mcp.json`, `CLAUDE.md`, the skills, and the
  guardrail hook.
- Claude Code in the terminal, signed in with your subscription; IB Gateway logged in to the **paper** account, API port
  4002.
- The heartbeat **stopped**. Never run the heartbeat and the loop at the same time: neither can manage the other's
  position.
- About 15 to 20 minutes, most of it waiting for the next check.

## Try it yourself

1. Start a fresh Claude Code session in `~/trading-desk` and send the `/loop` prompt from `prompts.md`.
2. Let it run three or four checks. Steer it once between checks, and see that the next check follows.
3. Stop it with the stop message, and confirm that the account is flat with nothing resting.
4. Ask for the comparison with your heartbeat's journal.

You're done when the loop is cancelled, the account is flat with nothing resting, and you can say in one sentence when
you would use each one. Your bars, numbers and Claude's answers will differ from the video, and that's fine.

## Good to know

- **The loop lives and dies with the session.** It is session-only, auto-expires after 7 days, and runs only until you
  close the session. Close the terminal and nothing is watching. For durable loops Claude Code points to `/schedule`.
- **The first check runs at once.** Claude does not wait for the first tick.
- **It fires when the session is idle.** If Claude is busy, the check waits for the turn to end, and a missed fire is not
  caught up, so a bar can be missed.
- **Steering is the point.** You can talk to the desk between checks, and the next check uses what you said. The
  heartbeat can't do that: you change its files instead.
- **The context grows.** Every check adds history to the same session. Keep loops short, and start a fresh session for
  the next run.
- **Usage is real.** Each check is a full Claude turn with tool calls. The heartbeat logs a cost per bar; the loop logs
  nothing. Keep loops short and stop them when you step away.

## Safety

Paper trading only. The loop can place orders through the trade tools, so the same guardrails apply as in lesson 12.3:
the hook, the deny rules, the limits in the server, and the paper-only check. Always end with the loop cancelled and the
account flat. Educational content, not financial advice; nothing here is a recommendation or a promise of profit.
