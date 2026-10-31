# Lesson 16.2 cheat sheet: Reading the results

## The words

| Word | Meaning |
|---|---|
| R | The money you lose if the stop is hit. +1 R means you made as much as you risked |
| Equity in R | Every result divided by the money at risk, so a 10-share trade and a 100-share trade compare fairly |
| Next experiment | One change, one protocol, one version in the ledger, with its drop rule written first |
| Drawdown | The fall from a peak. A single winning trade has none to measure |
| Sample size | How many trades (or days) a number comes from. Quote it next to every number |

## How to read a result

1. **Separate what ran.** A strategy's trades, plumbing tests (proof runs, kill-switch demos), manual trades and an AI
   desk that waited are different things. Our dashboard's 5 trades held only 1 strategy trade.
2. **Put it in R.** Divide net P&L by the real stop risk of each trade. Our one trade: risk $40.30, gross +$27.70
   (+0.69 R), commission $2.15, net +$25.55 (+0.63 R).
3. **Show the whole period, no picked dates.** For more than one trade, run the exact live settings through the
   backtester over the whole research period (the holdout stays out).
4. **Read the range, not the average.** Our backtest: 263 trades, +0.12 R per trade, but a 95% range from -0.002 to
   +0.243 R. A range that includes zero can't separate skill from luck.
5. **Count the costs at live size.** Live risk was about $40 per trade against about $576 in the backtest, so the same
   $2.15 commission is about 0.053 R live versus 0.02 R in the backtest: roughly a quarter of the average edge.
6. **Say what it can't tell you.** One trade proves nothing. "All wait" is not evidence of anything (patience or
   inertia). One backtest period is one market regime. A forward test needs its full sample (ours: about 100 trades).

## Our Monday's numbers (paper, 22 to 26 Oct 2026)

| What | Result |
|---|---|
| Factory strategy (ORB, QQQ, 15-minute range, no target) | 1 trade, +0.63 R net; skipped a signal 2 days 23 h old |
| AI desk (SPY, Trader v2.2 + settled bars) | 157 bars, all "wait"; 0 trades |
| Desk variants (regime gate, ORB veto, team, open-window agent) | 206 bars, all "wait"; 0 trades |
| Plumbing tests on SPY (22 Oct) | net -$4.38 after $10.22 commissions; not strategy results |
| Claude usage logged by the desk | about $31 (the team about $14.30) |
| Backtest, whole period (21 Oct 2024 to 21 Apr 2026) | 263 trades, +0.12 R average, 54% winners, max drawdown -7.9 R |

A few days of paper trading and one backtest: read every number, conclude nothing from it.

## The leftover stop (a false alarm, a real finding)

- The lab's journal said the QQQ stop was **Cancelled**; the desk's snapshot still showed it **PreSubmitted**. A stop that
  is good till cancelled could sell shares you don't hold.
- Check with a **fresh, read-only** connection on a free client ID, never by guessing. Ours: no positions, 0 open
  orders, the stop Cancelled in IB's completed-orders list.
- Likely cause (a hypothesis, not tested): a long-lived connection keeps an old order list, because a client generally
  isn't told when another client cancels an order.
- The fix in the lab: the daily report now opens a new read-only connection at report time (client ID 11) and says
  `LEFT AT IB`, `OK`, or `OK (IB not checked)`. It never cancels anything.

## Reading an agent's journal

- **Learned:** what the decisions and closed trades actually show. Ours: nothing real yet.
- **Promoted or archived lessons:** check whether they are real. Ours were "SEED" notes, made-up test data.
- **Versions:** what each version changed, and the one effect you can measure (ours: a skill that loaded on 1 of 55
  bars in v2.1 and on 78 of 78 in v2.2).
- **Fix stale notes**, but leave the experiment ledger to a person.

## A next experiment

| Part | Write it before you run |
|---|---|
| Change | One change only |
| Protocol | The metric, the data, the sample, what is compared with what; offline replay, no orders |
| Drop rule | The result that makes you stop, fixed before you look; and when the sample is too small to count |

Template: `next-experiments-template.md`.
