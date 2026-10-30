# Lesson 15.4 cheat sheet: judging an AI trader

## Words

| Word | Meaning |
|---|---|
| Forward-test protocol | The plan, fixed in advance: what is tested, on which days, how it is measured, against what, and when it stops |
| Baseline | What you compare against, so a result means something |
| Minimum track record | How many trades, or days, before a result says anything |
| Forward test | Judging a system only on days that come after its rules were written down |
| R | What you lose if the stop is hit; a trade's result in R is (exit - entry) / (entry - stop), costs included |
| Sharpe ratio | Average result divided by how much it bounces around; "yearly" scales a daily figure by the square root of 252 |
| Sealed report | A report that prints only data quality (days, bars, trade counts) until the stop rule is reached |
| p value | Here: the share of random runs that did at least as well as the trader |

## What the protocol fixes (as committed on our computer)

| Item | Value |
|---|---|
| Version | Trader v2.2 + settled bars, by its instruction hash; only plain-mode bars (no `--team`, `--regime-gate`, `--orb-veto`) |
| Ends early if | the instruction hash or the mode changes (that day ends the test), or a safety event |
| Period | 2026-10-26 to 2027-04-19: the first 120 NYSE trading days |
| Symbol | SPY only, long only, 5-minute bars, decisions on settled bars |
| Primary metric | Average result per trade in R, with a 95% bootstrap range |
| Second metric | Daily Sharpe ratio (a day without a trade counts as 0) |
| Minimum | 100 scored closed trades |
| Stop | 100 scored trades or the last day of the period, whichever comes first |
| A day counts if | at least 95% of its entry-window bars are in the saved data and were decided by the trader under this hash |

## Baselines

1. **Random entries, matched on frequency and risk:** 2,000 replicates; each day, as many random entries as the trader
   made; each random trade copies the stop distance and target of the trader's matching trade. Filled at the next bar's
   open, without the trader's data delay (this favours the baselines slightly). If more than 25% of the draws are dropped,
   the report flags it.
2. **Buy-and-hold SPY:** each counted day open to close, and the whole period. Context only.
3. **The lab's ORB strategy:** default settings, run by the lab's engine on the same days. Context only.

## Verdict rule (applied once, at the stop)

- **Better than luck:** p below 0.05 against the random entries, with at least 100 scored trades (and at most 10% unscored).
- **Not distinguishable from luck:** at least 100 scored trades, p of 0.05 or more. Not the same as "no edge".
- **Inconclusive:** fewer than 100 scored trades at the end of the period. No performance claim may be made.
- "Beats ORB" or "beats the market" only if the Sharpe ranges don't overlap, and then only as a hypothesis.

## How many trades it takes (`uv run -m desk.forward_report --table`)

| True yearly Sharpe | Per trade | Trades for a 50% chance to see it | Trades for an 80% chance | Months at 1 trade a day (80%) |
|---|---|---|---|---|
| 0.5 | 0.031 | 2,728 | 6,233 | 296.8 |
| 1.0 | 0.063 | 682 | 1,559 | 74.2 |
| 1.5 | 0.094 | 304 | 693 | 33.0 |
| 2.0 | 0.126 | 171 | 390 | 18.6 |
| 3.0 | 0.189 | 76 | 174 | 8.3 |
| 4.0 | 0.252 | 43 | 98 | 4.7 |

| Trades so far | Yearly Sharpe needed to beat luck (5%, one-sided) |
|---|---|
| 10 | 8.26 |
| 20 | 5.84 |
| 30 | 4.77 |
| 50 | 3.69 |
| 100 | 2.61 |
| 200 | 1.85 |
| 500 | 1.17 |
| 1,000 | 0.83 |

How to read it: with 100 trades, only a true yearly Sharpe near 4 is seen about 80% of the time, and a result must reach
about 2.6 just to beat luck. **This test can confirm a very strong edge or a very bad system. It cannot confirm a modest
one.** The only lever for detecting a smaller edge is a longer test, changed in the protocol and the script in a new commit
before the period starts. The tables assume roughly bell-shaped results; rare big losses make the real bar higher.

## Day one on camera (sealed report)

| Question | Answer |
|---|---|
| Does today count? | Yes: 1 trading day, 1 counted, no dropped days; the hash unchanged; the protocol file has a single commit |
| Scored trades | None: 0 closed trades (the desk said wait on every bar); 100 more needed |
| What we can say | Day one is valid data, and the test has started cleanly |
| What we can't say | Anything about whether the trader is good, bad or lucky; a day with no trades is evidence for neither |
| Forecast | None. If the period ends with fewer than 100 trades, the verdict is inconclusive |

One day, zero trades: a tiny sample by design of the calendar, not a result.

## Rules to keep

1. Write the protocol first, and commit it before the period starts.
2. Compare against baselines, above all random entries with the same frequency and risk.
3. Keep the results sealed until the stop. Unsealed numbers are exploratory.
4. Expect to wait: "we can't tell yet" is the honest answer for weeks.

Paper account only. Educational content, not financial advice; nothing here is a promise of profit or a recommendation.
