# Student kit: Lesson 10.5, One codebase for backtest and live

Module 10: From backtest to live on paper · AI Algorithmic Trading with Claude Code and Interactive Brokers

Since Module 6 we have used our own engine. In this lesson we try a professional event-driven platform, NautilusTrader, and
find out what it adds and what it costs:

1. **Port one strategy.** Claude installs NautilusTrader in its own folder (the Lab's dependencies stay untouched), reads its
   docs and its installed source, and ports our opening range breakout (15-minute range, QQQ, long only).
2. **Two engines, one table.** The same bars, the same costs: 263 trades in both engines, and net profit within $7. Every
   difference is explained: fill timing, cent rounding, one share on one trade, the stop-or-target rule, cash below zero,
   and docs that describe a newer version than the one installed.
3. **The same strategy, live, on paper.** An observe-only script on the IB paper Gateway with the Nautilus IB adapter: it
   connects, checks the paper account and loads QQQ, but on our free delayed data every bar request fails with IB error
   2188. Two guesses are tested and ruled out.
4. **The verdict.** When our own engine is enough, and the signs that it's time to graduate to a platform.

## What's in this kit

| File | What it is |
|---|---|
| `prompts.md` | The requests typed in the lesson, the `/add-dir` step, and the pause-and-try exercise |
| `cheat-sheet.md` | The words, our engine against a platform, the comparison table, every difference explained, the live adapter on free data, when to graduate, the files |
| `nautilus_lab/` | The scripts Claude wrote: `pyproject.toml`, `nautilus_orb.py` (the port), `run_lab_engine.py`, `compare.py`, `live_observe.py` (observe-only, no orders) |

`nautilus_lab/` is a separate folder next to the Lab, not part of the Lab's repo. Nothing in the Lab changed in this lesson.

## Before you start

- The Trading Lab with its engine, the ORB strategy and cached 5-minute bars (Modules 5 to 7).
- `uv` and Claude Code in the terminal, signed in with your subscription, in auto mode.
- For the live part: IB Gateway logged in to the **paper** account, API port 4002, and a client ID nothing else uses.
- About 1 GB of disk for the new environment (895 MB on our computer). On our computer the port took about 7 minutes and the live part about 10.

## Try it yourself

1. `/clear`, then send request 1 in `prompts.md` with your own start date (never the holdout).
2. Check the trade counts first, then the per-trade differences, then the totals.
3. Optional: request 2 on the paper Gateway. If Claude asks to read outside the working directories, decide on purpose:
   add only the folder it needs with `/add-dir`.

You're done when the trade counts match, and you can explain every difference that's left. Your numbers, versions and
Claude's replies will differ from the video, and that's fine.

## Good to know

- **Keep it separate.** A big framework brings its own versions of pandas, numpy and more; a separate environment keeps
  the Lab's tests and results unchanged.
- **Read the installed source.** The docs online follow the newest release. When they disagree with what you installed,
  the installed code wins.
- **Check the trade count.** A backtest that stops early can still return normally. Compare counts before totals.
- **Same totals aren't proof.** Pair the trades; differences that cancel in the totals can still be large per trade.
- **Free data has limits.** On a delayed-data account the adapter could load the instrument but not pull bars; our own
  engine's poll worked on the same account. A data subscription is your decision, not something the lesson needs.
- **Agreement between engines is not an edge.** The comparison used years the strategy had already been tested on.

## Safety

Paper trading only. `live_observe.py` has no execution client (Nautilus has no route to place an order), its order methods
raise, it asserts host 127.0.0.1 and port 4002, and it stops on any account that doesn't start with `DU`. Educational
content, not financial advice; nothing here is a recommendation or a promise of profit.
