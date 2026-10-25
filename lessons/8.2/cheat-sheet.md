# Lesson 8.2 cheat sheet: out-of-sample and walk-forward

## The words

| Word | Meaning |
|---|---|
| **In sample** | The data you used to choose the settings. A score measured here flatters you |
| **Out of sample** | Data the choice never saw. Only a score measured here tells you something new |
| **Validation set** | Data used to choose between a few candidates. Choosing with it means it is no longer fully unseen |
| **Holdout** | Data nobody looks at until the very end, opened once. Look at it again and tune again, and it stops being a holdout ("spent") |
| **Walk-forward** | Tune on a window of the past, trade the next stretch the tuning never saw, roll forward, repeat. The traded stretches, stitched together, make one out-of-sample equity curve |
| **Parameter stability** | Whether the chosen settings stay similar from window to window (and from one random seed to another) |
| **Sharpe ratio** | Return per unit of day-to-day swing; higher is better |
| **R** | The distance from the entry to the stop. A 1R target sells once the trade has made as much as the stop risked |

## Part 1: tuning, validation, holdout (QQQ 5-minute bars, usual costs, 1% risk per trade, long only, no leverage)

| Part | Dates | Used for |
|---|---|---|
| Tuning (12 months) | 2024-10-21 to 2025-10-20 | the 42-cell grid from Lesson 8.1 (range length x profit target) |
| Validation (6 months) | 2025-10-21 to 2026-04-20 | comparing the two candidates |
| Holdout (6 months) | 2026-04-21 to 2026-10-21 | one run of each candidate, at the very end |

Minimum trades per cell: 50 (half of Lesson 8.1's 100, because the tuning part is half the data). Every cell had at
least 149 trades, so it made no difference.

Two candidates, picked from the tuning data only:
- **Best cell**: 15-minute range, 1R target, Sharpe 2.91. Its neighbours average 2.02: "a bit of a spike".
- **Smoothed plateau**: 15-minute range, no target, Sharpe 1.75. Averaged with its neighbours it scores 2.22, the
  highest average.

| Candidate | Tuning (12 months) | Validation (6 months) | Holdout (6 months) |
|---|---|---|---|
| 15 min / 1R (best cell), Sharpe | 2.91 | 0.53 | 0.85 |
| 15 min / none (plateau), Sharpe | 1.75 | 0.99 | **-0.60** |
| 15 min / 1R, net return | +19.4% | +1.6% | +2.8% |
| 15 min / none, net return | +13.8% | +3.6% | -2.2% |

92 holdout trades for each candidate; holdout maximum drawdown -3% (1R) and -7% (no target).

Claude's reading:
1. **The tuning edge mostly didn't carry over.** About 80% of the tuning score was fitting to that particular year.
2. **The plateau shrank less but still failed.** It lost 43% on validation (the spike lost 82%), then went negative.
3. **The ranking flipped between validation and holdout.** With about 90 trades per period, a 6-month Sharpe has an
   error of roughly ±1.4, so 0.85 against -0.60 is not a meaningful difference. Honest reading: a weak, possibly zero
   edge.
4. **The plateau is partly an illusion.** The none, 5R and 10R columns are identical (those targets are almost never
   reached), so the "flat region" includes copies of one result.
5. **The one robust finding is the range length.** 10 to 20 minutes beat 5 and 45 to 60 minutes; 15 is the sensible
   middle: a coarse, structural choice, not a fitted number.

Next: treat the holdout as spent; use walk-forward to get several out-of-sample periods instead of one; add history
(24 months is too thin to settle a Sharpe of 1 either way).

## Part 2: walk-forward (tune 6 months, trade the next 2, roll forward 2)

9 windows, 18 traded months (2025-04-21 to 2026-10-21), $100,000 at the start. Inside each tuning window Optuna picks the
range length (5 to 60 minutes, in 5-minute steps) and the profit target (0.5 to 10 R) with 12 trials (5 random first),
at least 25 trades per trial; last entry 15:30; each window starts with the account value the previous one ended on.

| Over the same 18 months | Return | Sharpe | Max drawdown | Trades |
|---|---|---|---|---|
| Walk-forward (re-tuned each window) | +7.6% | 0.85 | -5.8% | 249 |
| Fixed 15 min / 1R | +14.5% | 1.50 | -5.2% | 269 |
| Buy-and-hold QQQ | +65.5% | 1.92 | -12.7% | n/a |

- **Tuning lost to not tuning.** Only 3 of the 9 windows beat the fixed settings. Window 5: Optuna chose a 60-minute
  range, and the next 2 months had a Sharpe of -1.7, against +3.1 for the fixed settings.
- **Buy-and-hold won easily.** QQQ rose strongly; the strategy was in a position only about 30% of the time.
- **The fixed settings aren't clean either.** 15 min / 1R was found on all 24 months, including these, so the gap is
  probably a bit flattering to it.

Parameter stability:
- Range length chosen per window: 5, 20, 20, 20, 35, 35, 35, 45 and 60 minutes (sorted). 5 different values; it
  changed at 5 of the 8 roll-forwards, by a median of 15 minutes.
- Profit target: 0.5R three times, 1.1R three times, then 1.5R, 4.3R and 8.3R (median 1.1R).
- With 4 more Optuna seeds per window, the range varied by 5 to 50 minutes inside the same window, and the target by 2
  to 9 R. Across all 45 tunings, 15 minutes was never picked.
- Many settings score nearly the same on 6 months of data, so Optuna picks among near-ties. More trials might narrow
  the spread, but the instability looks mostly like noise in the data.

## Commands

```text
! uv run -m backtests.split_validation   # tuning / validation / holdout (about a minute on our computer)
! uv run -m backtests.walk_forward       # the walk-forward and the chart (a few minutes)
```

The chart is `reports/walk_forward_orb.html`: open it in your browser with its full path, for example
`file:///home/<you>/trading-lab/reports/walk_forward_orb.html`.

Paper research only, not financial advice. No setting here is a recommendation or a strategy to trade.
