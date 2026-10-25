# Lesson 8.3 cheat sheet: stress tests

## The words

| Word | Meaning |
|---|---|
| **Stress test** | Shake one part of a backtest (trade order, costs, settings, market) and watch what breaks |
| **Monte Carlo (trade bootstrap)** | Rebuild many alternative equity curves from the same trades, drawn at random with replacement (a trade can come up twice, another not at all) |
| **Percentile** | The 5th percentile is the bad-luck case: only 5% of curves did worse. The 95th is the good-luck case |
| **Drawdown** | The fall from the account's highest point to its lowest point afterward |
| **Slippage** | The gap between the price you expected and the price you got |
| **Break-even cost** | The cost level (here a multiple of our usual costs) at which the strategy stops making money |
| **Parameter noise** | Nudge every setting a little at random and see whether the result holds |
| **Regime** | A stretch of market behaviour: here each month, rising or falling, calm or wild |
| **Profit factor** | Gross wins divided by gross losses |

## Our results (QQQ 5-minute bars, Oct 2024 to Oct 2026, 15-minute range, 1R target, 1% risk per trade, $100,000)

The real backtest: 354 trades, net $24,671 (+24.7%), max drawdown −5.2% (marked to every bar), win rate 59.6%, average
trade 0.063% of the account.

### Monte Carlo: 354 real trades drawn 354 at a time, with replacement, 5,000 times

| | 5th percentile | Median | 95th percentile | Real backtest |
|---|---|---|---|---|
| Final return | +8.0% | +24.6% | +44.7% | +24.7% |
| Max drawdown (trade to trade) | −8.9% | −5.0% | −3.1% | −4.7% |

Only 0.5% of the curves ended with a loss, and no curve fell more than 20%.

### Cost sweep: commission, spread and slippage scaled together, same trades

| Costs vs. usual | Net profit | Sharpe |
|---|---|---|
| 0x | $28,200 | 1.99 |
| 1x | $24,671 | 1.77 |
| 2x | $21,325 | 1.55 |
| 3x | $18,030 | 1.34 |
| 5x | $11,648 | 0.90 |
| ≈ 9.0x (break-even) | $0 | – |

Usual costs run about $9 a trade ($3,158 in total, about 11% of the gross profit). Profit falls by roughly $3,300 for
each extra multiple; the Sharpe drops below 1 at about 4.5x.

### What Claude said to plan for

1. Costs are not the weak point: at 3x the costs, the strategy keeps about 73% of its profit.
2. Expect a lower return than the backtest: plan for the 5th percentile (about +8%) rather than the median.
3. Plan for a drawdown of about 9%, not the 5% the backtest showed: with 1% risk per trade, roughly nine stop-outs.
4. Treat the average trade as thin (0.06% of the account, 60% win rate): a modest decline in it would hurt more than
   costs.

### Parameter noise: 200 nudged versions

Range 15 ± 7.5 min (rounded to a 5-minute bar), target 1R ± 0.3R, last entry 30 ± 20 min before the close, at random.

| | min | P5 | median | P95 | max |
|---|---|---|---|---|---|
| Sharpe | 0.74 | 0.91 | 1.39 | 1.98 | 2.05 |
| Net profit | $9.9k | $12.2k | $18.8k | $27.3k | $28.2k |
| Max drawdown | −8% | −7% | −6% | −4% | −4% |

All 200 made money and 86% had a Sharpe above 1. But the chosen setting (Sharpe 1.77) is a peak: only 22% of the nudged
versions beat it, so expect about 1.3 to 1.4. Range length matters most (median 1.89 at 15 minutes, about 1.3 at 10 and
20); a larger target hurts (1.53, 1.42 and 1.01 for 0.7-0.9R, 0.9-1.1R and 1.1-1.3R); the last entry time barely
matters (1.34 to 1.42).

### Regime split: 24 months (October 2024 left out, only 8 sessions)

| Regime | Months | Trades | Net P&L | Avg monthly return | Profitable months | Win rate | Profit factor |
|---|---|---|---|---|---|---|---|
| rising + calm | 10 | 143 | $10,503 | 0.9% | 80% | 61.5% | 1.46 |
| rising + wild | 5 | 82 | $6,827 | 1.2% | 60% | 59.8% | 1.40 |
| falling + calm | 2 | 24 | $1,572 | 0.6% | 50% | 62.5% | 1.36 |
| falling + wild | 7 | 99 | $6,328 | 0.9% | 71% | 56.6% | 1.23 |

The worst single month was March 2026 (−3.4%, falling and wild).

## Claude's verdict

**It passes the narrow question**: no small nudge turns it into a loser, and it made money in all four regimes.

**It doesn't earn a clean pass**:
- Short history: 24 months, and the falling + calm row is only 2 months (24 trades).
- Thin edge: about 0.06R per trade, profit factor 1.2 to 1.5 everywhere.
- The Sharpe is optimistic: 1.77 is the top of a hill, and the 15-minute range was picked because it was best on this
  same data.
- The noise sample isn't independent: 200 of 200 profitable is one data path tested 200 ways.
- No crash in the data: nothing like 2022 or a long sideways grind.
- The regime labels use hindsight: they show where the edge sat, not a filter you could trade on.

Claude's view: a credible candidate for continued paper trading, treating the Sharpe as about 1.3 rather than 1.77, and
waiting for more months of paper results before trusting it. That is a view about paper trading, not a promise.

## Two limits of these tests

- The Monte Carlo treats trades as independent; real losing streaks cluster, so the real drawdown risk is probably
  somewhat worse.
- Both tests use the same history the setting was chosen on: they show how much luck mattered inside it, not whether
  the edge holds on new data (Lesson 8.2).

## Commands

```text
! uv run -m reports.orb_stress_test     # Monte Carlo + cost sweep + chart (about 5 minutes on our computer)
! uv run -m reports.orb_noise_regimes   # 200 nudged versions + regime split (about 4 minutes)
```

Paper research only, not financial advice. No setting here is a recommendation or a strategy to trade.
