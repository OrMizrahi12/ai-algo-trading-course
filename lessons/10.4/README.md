# Student kit: Lesson 10.4, Journal and dashboard

Module 10: From backtest to live on paper · AI Algorithmic Trading with Claude Code and Interactive Brokers

Until now, what the engine did was scattered: a state file, the console, and whatever IB still remembered. In this
lesson every trade gets written down, with what it really cost:

1. **A SQLite trade journal**, written by the engine only: signals, orders, fills with their commission, and a daily
   account snapshot, plus a view with the P&L per entry ref. A read-only import fills it with today's real paper fills.
2. **What the journal shows.** Real commissions: about $1 on every buy and a little more on every sell. The three
   one-share engine trades each lost about $2 net.
3. **Live against the backtest.** A drift check, bar by bar and trade by trade: the backtest's cost model charged 5¢ for a
   round trip that really cost about $2. IB's minimum per order is the big difference.
4. **Fix the bug, keep the plan.** The journal's orders bug is fixed with a test; the cost model stays as it is, because
   the next test (H3) was registered with it. The finding becomes a new idea in the research journal.
5. **A dashboard that only reads**, on localhost: stats, equity, open positions and every trade net of commission, never
   the account ID.

## What's in this kit

| File | What it is |
|---|---|
| `prompts.md` | The requests typed in the lesson, the commands, and the pause-and-try exercise |
| `cheat-sheet.md` | The words, one writer and many readers, the tables, ready-made queries, the costs we measured, what it means for testing, the dashboard file by file |
| `idea-m.md` | The research journal row Claude added: IB's $1 minimum commission against the per-share cost model, and how to test it after H3 |
| `agents-md-entries.md` | The `AGENTS.md` lines Claude added (`live/journal.py`, `dashboard/`, client ID 7 for the import) |
| `trading-lab/live/` | `journal.py` and `journal_import.py` (new), and `runner.py`, `broker.py`, `config.py`, `__main__.py` as changed in this lesson (Lab commits 307a212 and f738836) |
| `trading-lab/dashboard/` | The dashboard (Lab commit ce492b2): `data.py`, `server.py`, `index.html`, `__main__.py` |
| `trading-lab/tests/` | `test_live_journal.py` and `test_dashboard.py`, and the fake IB they use (`fake_ib.py`, now with commission reports) |

No new dependency: the journal and the dashboard use only Python's standard library (`sqlite3`, `http.server`).

## Before you start

- The Trading Lab with the live engine from Lessons 10.1 to 10.3, and some paper fills of your own from today (IB lists
  only the current day's executions to the import).
- IB Gateway logged in to the **paper** account, API port 4002.
- Claude Code in the terminal, signed in with your subscription, in auto mode.
- Google Chrome (or any browser) for the dashboard.
- Time on our computer: about 13 minutes for the journal, 4.5 minutes for the drift check, under 2 minutes for the
  fix, and a minute and a half for the dashboard.

## Try it yourself

1. `/clear`, then send request 1 in `prompts.md`. Check the import's counts against what IB shows.
2. Run the P&L per entry ref query from `cheat-sheet.md`, and put one real round trip next to your backtest's cost model.
3. Send request 4, then open `127.0.0.1:8765` yourself.

You're done when the journal holds your real fills with their commissions, you can name the cost your model gets wrong,
and the dashboard shows your trades, but never your account number. Your fills, counts and Claude's replies will differ
from the video, and that's fine.

## Good to know

- **Only the engine writes the journal.** Your queries, the drift check and the dashboard only read it. Open it read-only
  (`?mode=ro`) when you query it yourself.
- **The import is safe to run twice.** Rows are keyed by IB's own ids, so a second run adds nothing.
- **An empty commission is not zero.** IB sends commission reports a moment after the fills; until then the journal
  leaves the field empty.
- **Keep your account ID out of screenshots.** The dashboard never selects it; the import's own output does print it.
- **Don't move the goalposts.** If a test is already registered with its settings, a new finding about costs goes into
  the research journal first. Changing the judge's cost rule is your decision.
- **A few trades prove nothing.** The trades in the video were plumbing tests, not a strategy result.

## Safety

Paper trading only. The engine and the import refuse a non-paper port, a remote host and any account that doesn't start
with `DU`; the import connects read-only and places no orders; the dashboard has no IB connection at all. Educational
content, not financial advice; nothing here is a recommendation or a promise of profit.
