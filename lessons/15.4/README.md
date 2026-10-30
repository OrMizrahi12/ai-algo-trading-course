# Student kit: Lesson 15.4, Judging an AI trader

Module 15: Advanced agent designs · AI Algorithmic Trading with Claude Code and Interactive Brokers

We have a trader, a few variants and a few days of paper journals. The tempting move is to look at the results and then
decide what counts. Once you have looked, every choice after that bends toward what you saw: the same trap as backtest
overfitting from module 8. So in this lesson we write the rules **before any result exists**:

- a **forward-test protocol** in `experiments/PROTOCOL.md`: the trader version (from the ledger), the period, the symbol,
  the metrics, three baselines, a minimum number of trades and a stop rule, committed before the test period starts;
- a **sealed report** (`uv run -m desk.forward_report`) that prints only data quality until the stop rule is reached;
- a **table** of how many trades it takes before a given Sharpe ratio can be told apart from luck.

Then, after the first day of the test, we run the sealed report exactly as the protocol says: one valid day, zero trades,
and nothing to conclude yet.

## What's in this kit

| File | What it is |
|---|---|
| `prompts.md` | Every request typed in the lesson, in order, what Claude did with each one, and the pause-and-try exercise |
| `cheat-sheet.md` | The words, what the protocol fixes, the baselines, the verdict rule, the two tables and how to read them, and what day one could and couldn't say |
| `trading-desk/` | The four files of the desk commit that added the protocol: `experiments/PROTOCOL.md`, `desk/forward_report.py` (the sealed report), `tests/test_forward_report.py` and the desk's `README.md`. Copy them over your desk, then change the version, the hash and the dates to your own **before** your test period starts |

## Before you start

- Your `~/trading-desk` from the earlier lessons: the heartbeat, the journal, the version ledger
  `experiments/ledger.csv` with its instruction hash, and the settled-bars fix from lesson 15.2.
- Your `~/trading-lab`, read-only: the protocol's ORB baseline runs the lab's `opening_range_breakout` with its own
  backtest engine, and module 8's `reports/luck_vs_skill.py` explains why luck needs a baseline.
- Claude Code in the terminal, signed in with your subscription.
- A paper account in IB Gateway or TWS, and the desk running in plain mode on market days.
- Time on our computer: about 6 minutes for the protocol, the report and the tests; the test itself runs for months.

## Try it yourself

1. Before you look at any result of your current trader version, send request 1 in `prompts.md` (or copy the kit's files
   and change the version, the hash and the dates to yours).
2. Read the protocol Claude writes. Change anything you disagree with now, in a new commit, before the first day of the
   period. After that day, the file stays as it is.
3. Run `uv run -m desk.forward_report --table` and read the two tables for your own trade rate.
4. After each market day, run `uv run -m desk.forward_report` (sealed). It tells you whether the day counted and how many
   scored trades you have. It tells you nothing about profit, on purpose.

You're done when the protocol is committed before the period starts, and your report says nothing but data quality until
the stop. Your numbers, dates and Claude's answers will differ from the video, and that's fine.

## Good to know

- **Fixed before any result.** Claude checked that the ledger's current row matched the hash the code produces, and said
  it had not looked at any trade result. The protocol was written on a Saturday, before any bar of the test period existed.
- **Only plain-mode bars count.** The test covers one version in one mode: no `--team`, `--regime-gate` or `--orb-veto`.
  A change to the instruction hash or to the mode ends the test that day. The side-by-side runs from lessons 15.1 to 15.3
  write their own journals and never enter it.
- **R, not dollars.** The main metric is the average result per trade in R (R is what you lose if the stop is hit). The
  lab caps the paper position at 10 shares, so dollar returns of the account mean little.
- **Random entries are the real baseline.** 2,000 random runs with the same number of entries per day as the trader, each
  random trade copying the stop distance and target of the trader's matching trade: same frequency, same risk. The
  verdict compares the trader with them only. Buy-and-hold SPY and the lab's ORB strategy are context.
- **The baselines have not met real data yet.** On camera they ran only on synthetic data in the tests, because no real
  bars of the period existed yet. Run the report on your first real day to check that they work.
- **The unsealed look is exploratory.** Claude used `--unseal` once, on synthetic data only, to check the layout, and
  found two real bugs that way. Unsealed numbers are headed EXPLORATORY and must not be quoted as the result.
- **Expect to wait.** With 100 trades, only a true yearly Sharpe near 4 is seen 80% of the time, and a result must reach
  about 2.6 just to beat luck. A yearly Sharpe of 1 would need about 1,559 trades, roughly 74 months at one trade a day.
  "We can't tell yet" is the honest answer for weeks, often months.
- **Day one on camera:** one valid trading day, zero trades (the desk said wait on every bar). That is valid data and a
  clean start. It is not evidence for or against the trader, and it allows no forecast.

Paper account only. Educational content, not financial advice; nothing here is a promise of profit or a recommendation.
