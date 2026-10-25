# Student kit: Lesson 8.3, Stress tests

Module 8: Optimization and robustness · AI Algorithmic Trading with Claude Code and Interactive Brokers

A backtest is one path through history: one order of trades, one level of costs, one setting, one market. In this
lesson you had Claude shake the opening range breakout on QQQ (15-minute range, 1R target) four ways. A Monte Carlo
draws its 354 real trades at random with replacement, 5,000 times, and shows the spread of final returns and maximum
drawdowns next to the real backtest. A cost sweep reruns it at 0, 1, 2, 3 and 5 times our usual costs and finds the
break-even point. Then 200 versions with the range length, the target and the last entry time nudged at random, and a
split of the 24 months into rising or falling, calm or wild. The strategy survives all four, but it doesn't earn a clean
pass, and the honest numbers to plan with are the bad end of each spread.

## What's in this kit

| File | What it is |
|---|---|
| `prompts.md` | The two requests typed in the lesson, the commands, and the pause-and-try exercise |
| `cheat-sheet.md` | The words (Monte Carlo, percentile, drawdown, slippage, break-even cost, parameter noise, regime), our results, what Claude said to plan for, and its verdict |
| `trading-lab/reports/orb_stress_test.py` | The Monte Carlo (5,000 draws of the real trades with replacement, compounded as a % of the account) and the cost sweep (0/1/2/3/5x usual, then a bisection for the break-even multiple); writes `reports/orb_stress_test.html` with three panels |
| `trading-lab/reports/orb_noise_regimes.py` | Parameter noise (200 nudged versions: range 15 ± 7.5 min, target 1R ± 0.3R, last entry 30 ± 20 min before the close) and the regime split (each month rising or falling, calm or wild); prints tables only |

The lesson also added two lines to the layout section of `AGENTS.md`. The engine, the metrics and the strategies are
unchanged.

## Before you start

- The Trading Lab with the opening range breakout and its `target_r` from **Lesson 8.1**, the shared engine with its
  `CostModel`, and the report scripts from earlier lessons (the new scripts follow `reports/sizing_comparison.py`).
- Two years of QQQ 5-minute bars in the cache (`data/cache/QQQ_5min.parquet`).
- No IB connection is needed. Both stress tests run on the cached bars.
- Both scripts run many backtests. On our computer the stress test took about 5 minutes (Claude's notes say about 3) and
  the noise and regime script about 4 minutes.

## Try it yourself

1. In your `trading-lab` folder, start `claude`, `/clear`, and send the Monte Carlo and cost request in `prompts.md`.
   Open the chart yourself. Before reading Claude's answer, find the 5th percentile of the final return and of the
   drawdown: those are the numbers to plan for.
2. `/clear`, send the parameter noise and regime request, and read Claude's verdict. Does your strategy pass, and what
   are its reasons not to?

You're done when your chart shows the three panels, you can name the drawdown you'd plan for, and Claude has given you a
verdict, with its reasons. Your numbers, wording and Claude's replies will differ from the video; the behaviour is what
matters.

## Good to know

- The first run's break-even search only looked up to 5x the usual costs, and the strategy was still profitable there.
  Claude changed it to keep doubling the cost until the profit reaches zero (about 9x).
- The Monte Carlo treats trades as independent. Real losing streaks cluster, so the real drawdown risk is probably
  somewhat worse than the reshuffle suggests.
- The Monte Carlo drawdowns are trade to trade; the backtest's headline drawdown (−5.2%) is marked to every bar, which is
  why the chart shows the real drawdown as −4.7%.
- Both stress tests use the same two years the setting was chosen on. They measure how much luck mattered inside that
  history, not whether the edge holds on new data: that is what Lesson 8.2's split and walk-forward tests are for.
- The regime labels use the whole month (hindsight). They show where the edge sat, not a filter you could trade on.
- The project's stop hook (Lesson 3.6) made Claude commit and push before it stopped, straight to `main`.
- Seeds: `SEED = 42` in `orb_stress_test.py`, `SEED = 11` in `orb_noise_regimes.py`.

## Safety

Paper trading only. Educational content, not financial advice. Nothing in this lesson connects to a broker or places an
order. "A credible candidate for continued paper trading" is Claude's view about paper trading, not a recommendation or a
promise: no setting in this lesson is a strategy to trade with real money.
