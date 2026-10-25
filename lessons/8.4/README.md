# Student kit: Lesson 8.4, Multiple testing and the scorecard

Module 8: Optimization and robustness · AI Algorithmic Trading with Claude Code and Interactive Brokers

In this module we tried a lot of settings: a 42-cell grid, a random search, Optuna, and 200 noise versions. The more
you try, the better the best result looks, by chance alone. In this lesson you first measure that luck: 1,000
strategies on QQQ that flip a coin every day, whose best one beats our opening range breakout. Then you deflate the
breakout's Sharpe ratio for every setting we tried (the Deflated Sharpe Ratio), measure how often the grid's winner is
just overfit (the Probability of Backtest Overfitting), and meet combinatorial purged cross-validation in plain words.
Finally you write the lab's standards down as a judge: `judge/scorecard.py` runs every test from this module on one
strategy and prints PASS or FAIL for each rule, with the thresholds and their reasons in `judge/standards.yaml`. No
strategy passes. That is the honest end of the module.

## What's in this kit

| File | What it is |
|---|---|
| `prompts.md` | The four requests typed in the lesson, the commands, and the pause-and-try exercise |
| `cheat-sheet.md` | The words, the coin-flip table, the Deflated Sharpe table, the PBO results, the eight rules and both scorecards |
| `trading-lab/reports/luck_vs_skill.py` | The luck report (numpy and pandas only): 1,000 coin-flip strategies, the Deflated Sharpe Ratio of ORB 15 min / 1R for several trial counts, and the PBO of the 42-cell grid by combinatorially symmetric cross-validation (8 and 16 blocks) |
| `trading-lab/judge/scorecard.py` | The judge: eight PASS/FAIL rules for one strategy and its settings, everything in one process pool; exits 1 if any rule fails; `scorecard(name, symbol, settings, trials=...)` for research loops |
| `trading-lab/judge/standards.yaml` | The thresholds, the test settings and the reasoning for each rule |
| `trading-lab/judge/__init__.py` | Makes `judge` a package (empty) |
| `trading-lab/tests/test_scorecard.py` | Offline tests for the judge's pure parts (no backtests are run) |

The lesson also added an entry for each new file to the layout section of `AGENTS.md`, and `pyyaml` to the project's
dependencies (`uv add pyyaml`). The engine, the metrics and the strategies are unchanged.

## Before you start

- The Trading Lab with the opening range breakout (Lesson 7.4) and its `target_r` (Lesson 8.1), the Donchian breakout
  (Lesson 7.1) and the Bollinger reversion (Lesson 7.2).
- The module 8 scripts the new files import: `backtests/optimize.py` and `backtests/search_comparison.py` (Lesson 8.1),
  `backtests/walk_forward.py` (Lesson 8.2), `reports/orb_stress_test.py` and `reports/orb_noise_regimes.py`
  (Lesson 8.3).
- Two years of QQQ and SPY 5-minute bars in the cache (`data/cache/`).
- No IB connection is needed. Everything runs on the cached bars.
- Both scripts run many backtests in parallel and keep every CPU core busy. On our computer (24 cores) the luck report
  took about 8 minutes (plus a 12-minute first collection while Claude built it), and one scorecard took 30 seconds to
  about 2 minutes.

## Try it yourself

1. In your `trading-lab` folder, start `claude`, `/clear`, and send the luck request in `prompts.md`. Before you read
   the answer, guess how high the best of 1,000 coin flips will score.
2. Ask Claude to save it as a numpy-only report (the second request), and check the numbers come out the same.
3. `/clear`, send the scorecard request, read the table, and then send the rule-4 request.

You're done when your best coin flip sits next to its median, and your scorecard prints PASS or FAIL for every rule.
Your numbers, wording and Claude's replies will differ from the video; the behaviour is what matters.

## Good to know

- The Deflated Sharpe depends on how many trials you count, and our trials are highly correlated neighbours. That is
  why the report prints several counts. Read the range (66-92% in the video), not one number.
- The judge's `--trials` option tells it how many settings the research tried. Without it, the judge assumes 100 and
  says "assumed".
- Rule 3 (walk-forward, re-tuned) judges the strategy plus its tuning. Rule 4 (fixed-settings walk-forward) judges the
  numbers you pass, but those were chosen with all the data in view, so it is the weaker of the two.
- In the video, Claude's first edit for rule 4 stopped on a mismatched string and changed nothing; it noticed, checked
  the real text and applied the edit. Read what a tool printed before you trust a table.
- Optuna 5.0 prints a `FutureWarning` about `constraints_func`; it still works.
- The project's stop hook (Lesson 3.6) made Claude commit and push before it stopped.

## Safety

Paper trading only. Educational content, not financial advice. No setting in this lesson is a recommendation or a
strategy to trade, and nothing here promises a profit: the point of the lesson is to measure a strategy honestly. The
coin-flip winners are luck, not strategies. Nothing in this lesson connects to a broker or places an order.
