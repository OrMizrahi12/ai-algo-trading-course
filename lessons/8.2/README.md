# Student kit: Lesson 8.2, Out-of-sample and walk-forward

Module 8: Optimization and robustness · AI Algorithmic Trading with Claude Code and Interactive Brokers

Lesson 8.1 ended on a warning: the grid's best setting scored 2.83 in the first year and 0.75 in the second. A score
measured on the data you tuned on flatters you. In this lesson you test the opening range breakout on QQQ only on data
its settings never saw. First a three-way split: 12 months to tune the grid, 6 months of validation to compare two
candidates (the single best cell and a smoothed plateau), and a 6-month holdout opened once, at the very end. Then a
walk-forward analysis: Optuna tunes on 6 months, the strategy trades the next 2 months it never saw, the windows roll
forward 2 months at a time (9 windows, 18 traded months), and the traded months are stitched into one out-of-sample
equity curve next to the fixed 15 minutes / 1R from Lesson 8.1 and buy-and-hold QQQ. The results are honest and not
flattering: the tuning score mostly didn't carry over, re-tuning lost to one fixed setting, both lost to buy-and-hold,
and the chosen settings changed from window to window (and with the random seed).

## What's in this kit

| File | What it is |
|---|---|
| `prompts.md` | The two requests typed in the lesson, the commands, and the pause-and-try exercise |
| `cheat-sheet.md` | The words (in sample, out of sample, validation, holdout, walk-forward, parameter stability), the split and its results, the walk-forward table and the stability check |
| `trading-lab/backtests/split_validation.py` | Tuning / validation / holdout (12 / 6 / 6 months): the 42-cell grid on the tuning part only, the best cell and the best smoothed-plateau cell, each run on validation and once on the holdout |
| `trading-lab/backtests/walk_forward.py` | The walk-forward: tune 6 months with Optuna (12 trials), trade the next 2, roll 2; chained equity curve vs. fixed 15 min / 1R and buy-and-hold QQQ; a stability check with 4 more seeds; writes `reports/walk_forward_orb.html` |

The lesson also added one line per script to the layout section of `AGENTS.md`. The engine, the metrics, the strategies
and `backtests/optimize.py` are unchanged.

## Before you start

- The Trading Lab with the opening range breakout (Lesson 7.4) and its optional `target_r` (Lesson 8.1), the shared
  engine, and `backtests/optimize.py` from Lesson 8.1 (`split_validation.py` reuses its grid and its plateau logic).
- Optuna, installed with `uv add optuna` in Lesson 8.1.
- Two years of QQQ 5-minute bars in the cache (`data/cache/QQQ_5min.parquet`).
- No IB connection is needed. Everything runs on the cached bars.
- Both scripts run many backtests in parallel and use every CPU core for a while. The split took under a minute on our
  computer; the walk-forward a few minutes.

## Try it yourself

1. In your `trading-lab` folder, start `claude`, `/clear`, and send the split request in `prompts.md`. Decide before
   you read the answer which candidate you expect to hold up on the holdout.
2. `/clear`, send the walk-forward request, open the chart yourself, and read the stability part of the answer.
3. Compare the walk-forward with the fixed setting and with buy-and-hold over the same months.

You're done when your holdout has been opened exactly once, and your walk-forward curve sits next to the fixed setting
and buy-and-hold. Your numbers, wording and Claude's replies will differ from the video; the behaviour is what matters.

## Good to know

- A holdout works only once. After you have looked at it, any further tuning that you check against it turns it into
  more tuning data. Claude calls it "spent" at the end of the first run.
- Six months hold only about 90 trades of this strategy, so a 6-month Sharpe ratio has an error of roughly ±1.4. Two
  candidates whose scores differ by less than that can't be told apart.
- The fixed 15 minutes / 1R was found on all 24 months, including the ones the walk-forward trades, so it has seen the
  data. The comparison flatters it a little.
- Walk-forward results depend on Optuna's random seed (`SEED = 7` in `walk_forward.py`); the stability check re-tunes
  every window with 4 more seeds.
- Optuna 5.0 prints a `FutureWarning` about `constraints_func`; it still works.
- The project's stop hook (Lesson 3.6) made Claude commit and push before it stopped.

## Safety

Paper trading only. Educational content, not financial advice. No setting in this lesson is a recommendation or a
strategy to trade, and nothing here promises a profit: the point of the lesson is to measure a strategy honestly.
Nothing in this lesson connects to a broker or places an order.
