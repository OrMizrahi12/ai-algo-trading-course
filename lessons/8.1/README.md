# Student kit: Lesson 8.1, Optimization

Module 8: Optimization and robustness · AI Algorithmic Trading with Claude Code and Interactive Brokers

Lesson 7.4 ended with a checklist, and its first item was robustness: a real edge should change smoothly when you change
the settings. In this lesson you had Claude search the settings of the opening range breakout on QQQ. First a grid
search: 7 range lengths x 6 profit targets = 42 backtests, scored by the Sharpe ratio, with a heatmap you open in the
browser and Claude's reading of its shape (plateau or peak). Then a random search and an Optuna search with 42 trials
each, over continuous ranges, next to the grid's best. The grid's winner (15 minutes, 1R, Sharpe 1.77) is a peak on a
1R ridge; neither search came close to it; and when Claude split the data by year, the same winner scored 2.83 in the
first year and 0.75 in the second. The best setting any search finds is not a forecast.

## What's in this kit

| File | What it is |
|---|---|
| `prompts.md` | The two requests typed in the lesson, the commands, and the pause-and-try exercise |
| `cheat-sheet.md` | The words (parameter, objective, R, plateau, peak), our grid table, Claude's reading, the three search methods side by side, and the year split |
| `trading-lab/backtests/optimize.py` | The grid search: range length x profit target, 42 backtests in parallel, Sharpe as the objective, cells under 100 trades ignored; prints the grid, judges plateau vs. peak and writes `reports/optimize_orb_qqq.html` |
| `trading-lab/backtests/search_comparison.py` | Random search vs. Optuna (42 trials each) vs. the grid, over range length 5-60 minutes, target 0.5-10 R and last entry 10:00-15:00, plus each winner on the first and the second year |
| `trading-lab/strategies/opening_range_breakout.py` | The opening range breakout from Lesson 7.4, with the new optional `target_r` (default: no target, so earlier results don't change) |
| `trading-lab/tests/test_strategy_opening_range_breakout.py` | Its tests, with two new ones for `target_r` |

The lesson also added Optuna as a dependency (`uv add optuna`, which changes `pyproject.toml` and `uv.lock`) and two
lines to the layout section of `AGENTS.md`. The engine, the metrics and the other strategies are unchanged.

## Before you start

- The Trading Lab with the opening range breakout from **Lesson 7.4** (`strategies/opening_range_breakout.py` and its
  tests) and the shared engine with its `CostModel`.
- Two years of QQQ 5-minute bars in the cache (`data/cache/QQQ_5min.parquet`).
- No IB connection is needed. The searches run on the cached bars.
- The grid and the search run many backtests in parallel and use every CPU core for a while. The grid finished in under
  a minute on our computer; the search comparison took about 9 minutes.

## Try it yourself

1. In your `trading-lab` folder, start `claude`, `/clear`, and send the grid request in `prompts.md`. Open the heatmap
   yourself, and decide before reading Claude's answer: is the best cell on a plateau or a peak?
2. `/clear`, send the search comparison request, and compare the three methods' best results and how many trials each
   needed.
3. Read the "why the best number is too optimistic" part of the answer, and find your own year split.

You're done when your heatmap opens, you can say whether your best cell is a plateau or a peak, and your table compares
all three methods. Your numbers, wording and Claude's replies will differ from the video; the behaviour is what matters.

## Good to know

- When Claude waits for a background job, check what it waits for. In the video, its wait loop searched for the
  optimizer's process by name and found itself, so it waited about ten minutes for a job that had already crashed.
  Claude found the bug when it read the log.
- The project's stop hook (Lesson 3.6) made Claude commit and push before it stopped.
- Optuna 5.0 prints a `FutureWarning` about `constraints_func`; it still works.
- Search results depend on the random seed (`SEED = 7` in `search_comparison.py`), and each method ran once.
- The year split is only a rough check: the winners were picked using both years. Lesson 8.2 picks the settings on one
  period and tests them, untouched, on a later one.

## Safety

Paper trading only. Educational content, not financial advice. No setting in this lesson is a recommendation or a
strategy to trade: the point of the lesson is that the best setting of a search looks better than it really is.
Nothing in this lesson connects to a broker or places an order.
