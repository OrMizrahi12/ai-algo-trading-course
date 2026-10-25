# Lesson 8.1 prompts and commands

Everything typed in the lesson, in order. Lines that start with `!` run in the terminal from inside Claude Code
(shell mode). Lines that start with `/` are Claude Code commands. Every request runs in auto mode. Nothing here needs an
IB connection: the backtests use the cached QQQ bars.

## 1. A grid search and its heatmap

```text
/clear
```

```text
Let's optimize the opening range breakout on QQQ. Add backtests/optimize.py with a grid search over the range length (5, 10, 15, 20, 30, 45 and 60 minutes) and a profit target (none, 1, 2, 3, 5 and 10 R). Use the Sharpe ratio as the objective and ignore any cell with fewer than 100 trades. Save a heatmap to reports/ (I'll open it myself), and tell me whether the best cell sits on a stable plateau or a lucky peak.
```

In the video, Claude read the strategy and an earlier comparison script, added an optional `target_r` to the strategy
(with two tests), wrote `backtests/optimize.py` and started the grid in the background. Its first wait loop found its
own process and waited about ten minutes; when Claude read the log, the grid had crashed while building its table
(pandas turned the "none" target into a missing value). Claude fixed it, ran the grid again (under a minute), ran the
whole suite (166 tests), added a line to `AGENTS.md` and committed.

Open the heatmap yourself: paste the file's full path into the browser's address bar, for example
`file:///home/<you>/trading-lab/reports/optimize_orb_qqq.html` (on Windows, `file:///C:/Users/<you>/trading-lab/...`).
Hover a cell to see its range, target and Sharpe. Run the grid again any time:

```text
! uv run -m backtests.optimize
```

## 2. Random search vs. Optuna vs. the grid

```text
/clear
```

```text
Now compare search methods on the opening range breakout on QQQ. Install Optuna with uv. Run a random search and an Optuna search with 42 trials each, over continuous ranges: range length 5 to 60 minutes, profit target 0.5 to 10 R, and last entry time 10:00 to 15:00. Same objective as our grid: Sharpe, at least 100 trades. Show the best result of each method next to the grid's best (15 minutes, 1R, Sharpe 1.77), how many trials each needed to get close, and explain why the best number any search finds is too optimistic.
```

Put your own grid's best into the request if it differs from ours. In the video, Claude installed Optuna
(`uv add optuna`), wrote `backtests/search_comparison.py`, ran 84 backtests (about 9 minutes), noticed that the grid's
winner enters until 15:30 (outside the 10:00-15:00 window) and re-scored it capped at 15:00 (1.75). Then the project's
stop hook made it add a line to `AGENTS.md`, commit and push. Run it again any time:

```text
! uv run -m backtests.search_comparison
```

## Pause and try

1. Run the grid request and open the heatmap. Plateau or peak? Decide before you read Claude's answer.
2. Run the search comparison. Which method found the best setting, and after how many trials?
3. Find the year split in the answer: how does each winner do in the first year and in the second?

You're done when your heatmap opens, you can say whether your best cell is a plateau or a peak, and your table compares
all three methods. Your numbers will differ from the video, and that's fine. This is paper research, not a setting to
trade.

## Try next (optional)

- Run the search comparison with another `SEED` in `search_comparison.py`. Does the ranking of random search and
  Optuna stay the same?
- Give both searches 200 trials instead of 42. Does Optuna pull ahead when it has more trials to learn from?
- Lesson 8.2 picks the settings on one period and scores them, untouched, on a later one (walk-forward).
