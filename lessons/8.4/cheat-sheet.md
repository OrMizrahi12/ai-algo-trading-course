# Lesson 8.4 cheat sheet: multiple testing and the scorecard

## The words

| Word | Meaning |
|---|---|
| **Multiple testing** | Trying many strategies or settings and keeping the best. The more you try, the higher the best score climbs by chance alone |
| **Deflated Sharpe Ratio (DSR)** | The probability that a strategy's true Sharpe is above zero after allowing for how many settings were tried, how short the data is and how fat-tailed the returns are. Its bar is the Sharpe the luckiest of N zero-skill tries would reach |
| **Probability of Backtest Overfitting (PBO)** | Cut the history into blocks, use half as training, pick the best setting there and rank it on the other half. PBO is the share of splits where the training winner lands in the bottom half. Pure noise gives about 50% |
| **Combinatorially symmetric cross-validation (CSCV)** | The block method behind PBO: every way of choosing half the blocks as training |
| **Combinatorial purged cross-validation (CPCV)** | Many train/test splits of one history: the timeline is cut into blocks and every combination is tested. Purging removes training data that overlaps the test blocks; an embargo drops a small gap after each one |
| **Scorecard / judge** | A script with fixed rules, written before the results, that says PASS or FAIL. No one argues with it, not even Claude |
| **Sharpe ratio** | Return per unit of day-to-day swing, yearly; higher is better |
| **R** | The distance from the entry to the stop. A 1R target sells once the trade has made as much as the stop risked |

## 1. Luck: 1,000 coin-flip strategies on QQQ

Every session each strategy flips a coin: long or short at the open (or long or flat), out at the close, no costs.
502 sessions (2024-10-21 to 2026-10-21).

| Coin-flip type | Best | 95th percentile | Median | Worst | Sharpe above 1.0 |
|---|---|---|---|---|---|
| long or short | **2.08** | 1.24 | **-0.03** | -2.26 | 101 of 1,000 |
| long or flat | 1.95 | 1.03 | 0.22 | -1.42 | 60 of 1,000 |

None of them has any skill. Our opening range breakout (15 min / 1R, Sharpe 1.77 after costs) beats 95% of the
long-or-short flippers, and the luckiest flipper beats it. The flippers pay no costs, so the comparison is not exact.

## 2. Deflated Sharpe Ratio of ORB 15 min / 1R

Trials counted on the full data: 42 grid cells + 42 random search + 42 Optuna + 200 noise versions = 326. Their Sharpes
spread with a standard deviation of 0.46.

| Trials counted | Sharpe a lucky winner would reach by chance | DSR |
|---|---|---|
| 1 (no deflation) | 0 | 99.3% |
| 42 (grid only) | 1.01 | 85.5% |
| **326 (all full-data runs)** | **1.33** | **72.8%** |
| 908 (plus walk-forward and split-validation tuning runs) | 1.47 | 66.0% |

- The 42 grid cells are 0.75 correlated, so they behave like about 11 independent tries: 92%.
- Claude's reading: a real edge is still more likely than not, but not proven. Treat 66-92% as the honest range and
  lean toward the lower end.
- The Sharpe was 2.91 in the first half of the data and 0.69 in the second. That drop matters more than any formula.

## 3. PBO of the 42-cell grid (CSCV)

- 16 time blocks, 12,870 ways to pick 8 of them as training.
- **PBO 33%** with 16 blocks, 24% with 8 blocks (pure noise: about 50%).
- The training winner's Sharpe falls from 2.00 in training to 1.10 out of sample, and is negative in 9% of splits.
- The slope of out-of-sample against training Sharpe is -0.83: the better a winner looked, the worse it tended to do.
- The whole family is mostly positive (mean Sharpe 1.17); picking the best cell mainly adds about 0.9 of optimism.

## 4. The judge: eight rules (`judge/standards.yaml`)

| # | Rule | Needs |
|---|---|---|
| 1 | Trades | at least 200 |
| 2 | Sharpe after costs (full data) | at least 1.0 |
| 3 | Walk-forward Sharpe, re-tuned (tune 6 months, trade 2, roll) | at least 0.5 |
| 4 | Fixed-settings walk-forward (the same months, no re-tuning) | at least 0.5 |
| 5 | Worst-5% Monte Carlo drawdown (5,000 reshuffles of the real trades) | no worse than -20% |
| 6 | Break-even cost multiple (how many times the usual costs before profit hits zero) | at least 2x |
| 7 | Deflated Sharpe (`--trials`, default 100 "assumed") | at least 95% |
| 8 | Parameter noise (40 versions, every setting nudged up to ±25%) | at least 80% still profitable |

## 5. The scorecards

Default settings for Donchian and Bollinger; 15 min / 1R for the opening range breakout.

| # | Rule | ORB, QQQ | Donchian, SPY | Bollinger, QQQ |
|---|---|---|---|---|
| 1 | Trades | 354 PASS | 541 PASS | 728 PASS |
| 2 | Sharpe after costs | 1.77 PASS | 0.33 FAIL | -0.14 FAIL |
| 3 | Walk-forward, re-tuned | 0.85 PASS | -0.61 FAIL | 0.57 PASS |
| 4 | Fixed-settings walk-forward | 1.50 PASS | 0.23 FAIL | 0.55 PASS |
| 5 | Worst-5% Monte Carlo drawdown | -8.9% PASS | -15.8% PASS | -18.9% PASS |
| 6 | Break-even cost multiple | above 5x PASS | 2.1x PASS | 0.7x FAIL |
| 7 | Deflated Sharpe | 90.8% FAIL | 35.5% FAIL | 10.1% FAIL |
| 8 | Parameter noise | 100% PASS | 55% FAIL | 0% FAIL |
| | **Overall** | **FAIL, 7 of 8** | **FAIL, 3 of 8** | **FAIL, 4 of 8** |

Before rule 4 existed the totals were 6 of 7, 3 of 7 and 3 of 7. Run times: about 80 s, 30 s and 130 s.

- The breakout fails only the Deflated Sharpe, with 100 trials assumed. Claude treats that one as open.
- Bollinger passes rules 3 and 4 although it loses money over the full two years: its first 6 months, which the
  walk-forward only uses for tuning, drag the full-sample number down. The pass is narrow.
- Rule 4 is weaker than rule 3: the fixed settings were chosen while looking at all the data, including those months.
- The thresholds were proposed before any result was seen and were not changed.

Paper research only. Nothing here is a recommendation or a strategy to trade.
