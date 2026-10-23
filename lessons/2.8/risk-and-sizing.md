# Risk and sizing: the arithmetic from Lesson 2.8

## R: one unit of risk

Before you enter a trade, you pick a **stop**: the price where your idea is proven wrong and you get out. The money
you lose if the stop is hit is **R**, one unit of risk. Results are measured in R: a win of 2 R made twice what you
risked; a loss at the stop is -1 R.

## Risk a fixed percent

A simple rule: risk the same percent of your current balance on every trade.

| Balance | Risk per trade | 1 R |
|---|---|---|
| USD 10,000 | 1% | USD 100 |
| USD 12,000 | 1% | USD 120 |
| USD 8,000 | 1% | USD 80 |

When the account grows, R grows with it. When it shrinks, R shrinks too, so a losing streak slows itself down.

## Position sizing

```
shares = risk amount / (entry price - stop price)
```

**Example 1.** Balance USD 10,000, risk 1% = USD 100. A stock at 50.00 with a stop at 49.00 risks USD 1.00 per
share: 100 / 1.00 = **100 shares** (a USD 5,000 position).

**Example 2.** The same USD 100 of risk on SPY at 760.00 with a stop at 758.50 (USD 1.50 per share):
100 / 1.50 = 66.7, rounded down to **66 shares**. But 66 shares cost about USD 50,160, five times the account.
Without borrowing, the cash buys 13 shares (USD 9,880), and the real risk is 13 x 1.50 = USD 19.50.

The risk rule is a ceiling: the size can be smaller, never bigger. Always round down. (The prices are round
illustrations, not quotes.)

## Expectancy

The average result per trade, in R:

```
expectancy = win rate x average win (R) - loss rate x average loss (R)
```

| Win rate | A win pays | Expectancy |
|---|---|---|
| 45% | 1.5 R | 0.45 x 1.5 - 0.55 x 1 = **+0.13 R** |
| 35% | 1.5 R | 0.35 x 1.5 - 0.65 x 1 = **-0.13 R** |
| 35% | 2.5 R | 0.35 x 2.5 - 0.65 x 1 = **+0.22 R** |
| 70% | 0.3 R | 0.70 x 0.3 - 0.30 x 1 = **-0.09 R** |

The win rate alone says almost nothing. The win rate and the payoff together decide the expectancy.

## Drawdown and losing streaks

- **Drawdown**: the drop from the highest balance so far to a later low, in percent.
- **Losing streak**: losses in a row. Long streaks are normal even with a positive expectancy: in the lesson, the
  typical future of the 45% / 1.5 R strategy had 8 losses in a row.

Eight losses in a row at 1% risk cost about 7.7% (0.99^8 = 0.923). At 20% risk they cost about 83% (0.80^8 = 0.168).

## Why big drawdowns are dangerous

| Loss | Gain needed to get back |
|---|---|
| -10% | +11.1% |
| -25% | +33.3% |
| -50% | +100% |
| -75% | +300% |
| -90% | +900% (what's left has to grow tenfold) |

**Risk of ruin** is the chance that a sizing rule drives the account so deep that it cannot realistically come back.
The simulator counts a path as "ruined" when it ever falls below half of the start.

## What the lesson's simulator showed (one run, 200 trades, 100 futures, USD 10,000)

| 45% win rate, 1.5 R | A: 1% | B: 5% | C: 20% | C: 50% |
|---|---|---|---|---|
| Median end balance | USD 12,331 | USD 21,022 | USD 2,421 | USD 0 |
| Median max drawdown | 13% | 54% | 99% | 100% |
| Fell below -50% | 0% of paths | 20% | 91% | 100% |

The edge did not change; only the size did. More risk helps only up to a point; past it, the same edge shrinks the
account. These are illustrations of arithmetic on random draws, not predictions.

Educational content only, not financial advice. Paper (simulated) account only.
