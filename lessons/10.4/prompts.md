# Lesson 10.4 prompts and commands

Everything typed in the lesson, in order. Lines that start with `/` are Claude Code commands. IB Gateway must be logged in
to the **paper** account (port 4002) for the import; the dashboard needs no IB connection at all. Every request below was
sent in auto mode.

## 1. The trade journal

```text
/clear
```

Then send (change the first sentence to fit what is running on your machine, or leave it out):

```text
New topic, unrelated to H3 (the backfill is running in my other terminal with client ID 5; leave it alone and do not touch data/cache). Add a SQLite trade journal to live/: tables for signals, orders, fills (with commission) and daily account snapshots, written by the engine only, with tests. Then import today's paper fills and orders from IB (read-only, its own client ID) so the journal starts with real rows, and show me a few sqlite3 queries in the terminal: today's fills with commission, and P&L per entry ref.
```

On our computer this took about 13 minutes. Along the way:

- our own hook blocked a test file that named the live trading port; Claude followed the existing guard tests and left
  the live port out of the file instead of working around the hook;
- the first real import (19 orders, 10 fills, read-only on client ID 7) showed two problems: empty commissions, and
  kill switch sells with a generic `live:kill` ref; both were fixed with tests;
- the `sqlite3` command-line tool wasn't installed, so the queries ran through Python's `sqlite3` module.

Claude ended without a commit, so the next request starts with one.

## 2. Live against the backtest (the drift check)

```text
Your journal work is not committed yet (git status shows it), please commit it first. Then the drift check for today: replay today's QQQ session through the backtester with ORB 15 and compare, bar by bar, with what the live engine logged today (bar lines, decisions, delays). Then compare our three real one-share SPY fills from the journal with what the backtester's fill and cost model would have assumed for the same moments: price, commission, total cost. Put it in one table and explain every difference. Use one small history request with its own client ID; the backfill is still running.
```

About 4.5 minutes in the video (Lab commit `307a212` for the journal). Use your own symbol, strategy and fills: the point
is one table with the model's cost and the real cost side by side.

## 3. Fix the bug, keep the plan

```text
Yes, fix the journal orders bug (quantity and average price from the fills), with a test, and commit. Do NOT change CostModel now: H3 was pre-registered with the default costs and has not run yet. Instead add the $1 minimum commission finding as a new idea in research/journal.md (what it would change, how to test it after H3), and commit that too.
```

Lab commits `f738836` (the orders fix, 43 tests) and `dc7c900` (idea M, see `idea-m.md`). If your next test is already
written down with its settings, a finding like this goes into the research journal first, not into the cost model.

## 4. A dashboard that only reads

```text
/clear
```

```text
Build a small dashboard for our live paper engine that reads the trade journal read-only: account equity over time, open positions, every trade with its net P&L after commission, and simple stats (trades, win rate, net P&L, commissions paid). Run it on localhost only, never show the account ID, keep it out of the engine process, add tests, then start it and open it in Chrome. Commit when it works.
```

About a minute and a half, 18 tests, Lab commit `ce492b2`. Claude couldn't open Chrome from its session, so we opened it
ourselves: a new tab, then

```text
127.0.0.1:8765
```

## 5. Why the costs win

```text
It opened in Chrome and looks right. Explain in a few lines why three trades were up before costs but lost money after them, and what that means for the way we test strategies.
```

Claude corrected us: two of the three were up before costs, not three.

## Commands

```bash
uv run -m live.journal_import          # today's orders, fills and an account snapshot from IB, read-only, client ID 7
uv run -m dashboard                    # the dashboard on http://127.0.0.1:8765 (read-only, Ctrl+C to stop)
uv run pytest tests/test_live_journal.py tests/test_dashboard.py -q
```

## Pause and try

1. Ask for the journal (request 1) and import your own paper fills, read-only.
2. Run the P&L per entry ref query (see `cheat-sheet.md`) and put one real round trip next to your backtest's cost model.
3. Build the dashboard (request 4) and open it yourself.

You're done when the journal holds your real fills with their commissions, you can name the cost your model gets wrong,
and the dashboard shows your trades, but never your account number. Your fills, counts and Claude's replies will differ
from the video, and that's fine. Paper account only.
