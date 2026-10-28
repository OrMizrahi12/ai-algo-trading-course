# Lesson 11.4 prompts and commands

Everything typed in the lesson, in order. Lines that start with `/` are Claude Code commands. The requests were sent in
auto mode, in `~/trading-desk`, in a fresh Claude Code session; the live loop ran in a second terminal, also in
`~/trading-desk`.

## 1. One Claude session per trading day

```text
Right now every bar is a brand-new Claude call with no memory (--no-session-persistence). Make the heartbeat keep one Claude session per trading day: start it on the first bar with today's date in the first message, store the session id in the desk state, and continue it with --resume on every later bar, so the trader remembers its own reasoning from earlier today. Roll over to a fresh session each morning, with a short summary of yesterday built from the journal as its first input. Keep the hash honest: the journal must still say which instructions the trader saw. Log how big the context gets on every bar, add tests, and commit. Then prove it on the paper Gateway with --dry-run: run two real bars and show that the second decision can see the first.
```

About six minutes of work, plus a wait for the next bar on the delayed feed. Claude read the heartbeat, the model call,
the journal and the tests, then the session options in `claude --help`, and tested them with a small probe. What it
found: on `--resume`, Claude Code keeps the system prompt of the session's first request, so it added
`--system-prompt-snapshot off` to keep the journal's hash honest. It added a ledger row, **Trader v1.1 (day sessions)**,
ran two real `--dry-run` bars (13:55: a new session, 34,613 tokens; 14:00: the same session, 65,807 tokens) and checked
the memory by asking a **fork** of the session (a copy, so the real one is untouched) what it said on the first bar.
Its report also warned: with full snapshots, the context fills up in about 35 bars.

## 2. Send only what changed

```text
Good catch on the context. Fix it: the first bar of a session still gets the full snapshot, but later bars send only what changed since the last bar: the new bar with its indicators, positions, open orders, the clock and the seatbelt status. The older history is already in the session. Also explain what happens if the window does fill up (compaction) and why we should not rely on it. Test, commit, then measure the context on the next real bar with --dry-run.
```

About five and a half minutes. Claude wrote the delta, broke it on purpose to confirm the new tests can fail (a mutation
check), committed, and measured the next real bar: 14:05, a 2.8 KB delta, +1,702 tokens (a full snapshot added about
31,000). It also tested compaction in a fork with `--autocompact 100000`: the context dropped to under 5k tokens, and the
trader could no longer quote its earlier reason.

## 3. Usage before, a live loop, usage after

In Claude Code:

```text
/usage
```

In a second terminal (the live engine), on the paper Gateway, during US market hours:

```bash
git log --oneline -1 && uv run -m desk
```

Stop it with Ctrl+C when you have enough bars. Then `/usage` again in Claude Code.

## 4. Estimate a full trading day

```text
While you were idle, the heartbeat ran live on paper for 46 minutes and handled 11 real bars (14:10 to 15:00) in today's session. /usage showed 2% of the current session before, and still 2% after; the week stayed at 0%. From the journal's context and cost numbers for those bars and these usage readings, estimate a full trading day on 1-, 5- and 15-minute bars, and explain what it means for which Claude plan to use. Be honest about what we cannot measure precisely.
```

Change the numbers to your own run. About a minute and a half. Claude found that the logged `cost` was the session's
running total, worked out the real cost per bar, and estimated a full day (see `cheat-sheet.md`).

## 5. Journal the cost of each bar

```text
Yes, fix the per-bar cost: journal the cost of each bar, keep the running total too, add a test and commit.
```

About a minute and a half: `bar_cost_usd` and `session_cost_usd` in every record, the running total kept in
`data/desk/state.json`, four new tests and a mutation check, then one real `--dry-run` bar ("cost $0.0188 this bar,
$0.4966 this session").

## Pause and try

1. Make your heartbeat keep one Claude session per trading day, with `--resume` and a morning summary, and keep the hash
   honest (request 1).
2. Send only what changed after the first bar, and measure the context on a real bar (request 2).
3. Run it for an hour on paper, read `/usage` before and after, and ask Claude to estimate your full day (requests 3 and 4).

You're done when your journal shows one session for the whole day, each later bar adds a couple of thousand tokens, and
you know the cost of one bar. Paper account only.
