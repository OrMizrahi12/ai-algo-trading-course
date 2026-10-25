# Lesson 8.1 cheat sheet: optimization

## The words

| Word | Meaning |
|---|---|
| **Parameter** | A number in the rules you can change: here the opening range length and the profit target (and, in the search comparison, the last entry time) |
| **Objective** | The one score the search tries to maximize: here the Sharpe ratio (return per unit of day-to-day swing) |
| **Guard rail** | A rule that disqualifies a setting: here fewer than 100 trades |
| **R** | The distance from the entry to the stop. A 1R target sells once the trade has made as much as the stop risked |
| **Grid search** | Try every combination on a fixed list (7 ranges x 6 targets = 42 backtests) |
| **Random search** | Draw settings at random from continuous ranges |
| **Optuna** | A Python library that looks at the trials so far and samples more often where the good settings were (its default sampler is called TPE) |
| **Plateau** | A wide area where the neighbours score almost as well: what a robust setting looks like |
| **Peak** | One bright cell surrounded by weaker ones: often luck |

## Our grid (QQQ 5-minute bars, Oct 2024 to Oct 2026, usual costs, 1% risk per trade, long only, no leverage)

Sharpe ratio by range length (rows) and profit target (columns). Every cell had 286 to 384 trades.

| Range | no target | 1R | 2R | 3R | 5R | 10R |
|---|---|---|---|---|---|---|
| 5 min | 0.47 | 0.59 | 0.48 | 0.19 | 0.35 | 0.47 |
| 10 min | 0.88 | 1.38 | 0.98 | 0.86 | 0.84 | 0.88 |
| **15 min** | 1.00 | **1.77** | 1.15 | 1.00 | 1.00 | 1.00 |
| 20 min | 0.78 | 1.35 | 0.96 | 0.76 | 0.78 | 0.78 |
| 30 min | 0.91 | 1.40 | 0.89 | 0.90 | 0.91 | 0.91 |
| 45 min | 0.76 | 0.91 | 0.69 | 0.74 | 0.76 | 0.76 |
| 60 min | 0.41 | 0.40 | 0.32 | 0.39 | 0.41 | 0.41 |

## Claude's reading: a peak on a ridge

- **Range length is a plateau**: 10 to 30 minutes all score about 0.8 to 1.0 with no target; 5 and 60 minutes are
  clearly worse.
- **The 15-minute / 1R cell is a peak**: its eight neighbours average 1.06 (60% of its 1.77), the worst is 0.78, and a
  2R target drops it to 1.15.
- **The 1R column is a ridge**: it beats the other targets at every range from 10 to 30 minutes (1.35 to 1.77), so a
  tight target looks like a real pattern, but Claude would expect about 1.3 to 1.4 on new data, not 1.77.
- **Smoothing agrees**: averaging each cell with its neighbours puts the best at 20 minutes with no target (1.20).
- **Caveats**: the 5R and 10R columns are nearly copies of "no target" (those targets are almost never hit in a day),
  so there are about four distinct targets; two years is one market regime; choosing the best of 42 cells on the same
  data you score it on inflates the number; the target fills are idealized (a limit order set from the signal bar's
  close, and the stop wins when one bar touches both).

## Three search methods, 42 tries each

| Method | Best setting | Sharpe | Trades | Trials to reach 90% of the grid best (1.59) |
|---|---|---|---|---|
| Grid, 42 cells | 15 min, 1R, last entry 15:30 | 1.77 | 354 | n/a |
| Random search, 42 trials | 25 min, 0.54R, last entry 14:09 | 1.42 | 320 | never |
| Optuna, 42 trials | 30 min, 7.4R, last entry 14:11 | 1.13 | 313 | never |

Best so far after 5, 10, 20, 30 and 42 trials: random 1.09, 1.09, 1.42, 1.42, 1.42 (best at trial 13); Optuna 1.11,
1.11, 1.11, 1.11, 1.13 (best at trial 38). Optuna did not beat random search here: 42 trials are too few for it to learn
much in three dimensions, though its median trial was better (0.89 against 0.65). With one run each, the seed matters.
The grid's winner enters until 15:30, outside the 10:00-15:00 window the searches got; capped at 15:00 it scores 1.75.

## Why the best number is too optimistic

The search tried 42 settings on the same data and kept the highest, so that score is partly luck; on fresh data it would
fall back toward the typical score. Random search's best (1.42) is more than double its median (0.65).

Claude split the data on 2025-10-22 and ran each winner on both years:

| Winner | First year | Second year |
|---|---|---|
| Grid (15 min, 1R) | 2.83 | 0.75 |
| Random search | 2.92 | 0.07 |
| Optuna | 1.35 | 0.89 |

Almost every setting made money (39 of 41 random trials, all 42 Optuna trials), so the strategy has some real edge, but
the size of the headline Sharpe is mostly selection. The split is only a rough check, because the winners were picked
using both years: a real test picks the settings on one period and scores them, untouched, on a later one (Lesson 8.2).

## Commands

```text
! uv run -m backtests.optimize            # the grid (under a minute on our computer)
! uv run -m backtests.search_comparison   # random vs. Optuna vs. grid (about 9 minutes)
! uv run pytest -q                        # the whole suite (166 tests at the end of this lesson)
```

Paper research only, not financial advice. No setting here is a recommendation or a strategy to trade.
