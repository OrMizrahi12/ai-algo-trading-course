# Lesson 8.3 prompts and commands

Everything typed in the lesson, in order. Lines that start with `!` run in the terminal from inside Claude Code
(shell mode). Lines that start with `/` are Claude Code commands. Every request runs in auto mode. Nothing here needs an
IB connection: the backtests use the cached QQQ bars.

## 1. A Monte Carlo and a cost sweep

```text
/clear
```

```text
Let's stress test the opening range breakout on QQQ with the 15-minute range and the 1R target. First, a Monte Carlo: take its real trades and build 5,000 alternative equity curves by drawing trades at random with replacement. Show me the spread of final returns and of maximum drawdowns, with the 5th and 95th percentiles, next to what the real backtest showed. Second, a cost sweep: rerun it with costs and slippage at 0, 1, 2, 3 and 5 times our usual and find the break-even point. Save one chart to reports/ (I'll open it myself) and explain what I should plan for.
```

In the video, Claude read an earlier report script, the engine's cost model and the metrics, wrote
`reports/orb_stress_test.py` (161 lines) and ran it. The first run's break-even search stopped at 5x the usual costs,
where the strategy was still profitable, so Claude changed it to keep doubling the cost, ran it again (almost five
minutes), added a line to `AGENTS.md` and committed.

Open the chart yourself: paste the file's full path into the browser's address bar, for example
`file:///home/<you>/trading-lab/reports/orb_stress_test.html` (on Windows, `file:///C:/Users/<you>/trading-lab/...`).
Hover a bar or a point to see its value. Run it again any time:

```text
! uv run -m reports.orb_stress_test
```

## 2. Parameter noise and regime splits

```text
/clear
```

```text
Two more stress tests on the opening range breakout on QQQ with the 15-minute range and the 1R target. Parameter noise: run 200 versions where the range length, the target and the last entry time are each nudged a little at random, and show how many still make money and how the Sharpe spreads. Regime splits: label each month of our data as rising or falling and calm or wild for QQQ, and show how the strategy did in each of the four regimes. Show everything here in tables, don't open a browser, and tell me honestly whether this strategy passes.
```

In the video, Claude read the stress test from step 1 and the strategy, wrote `reports/orb_noise_regimes.py` (151 lines)
and ran it (about four minutes). It answered and asked whether to commit to `main`; the project's stop hook ("Commit and
push your work before you stop") fired, and Claude committed and pushed. Run it again any time:

```text
! uv run -m reports.orb_noise_regimes
```

## Pause and try

1. Run the Monte Carlo and cost request and open the chart. Where does the real backtest sit in the spread? What are the
   5th-percentile return and drawdown?
2. Find the break-even cost multiple. How much profit is left at 3x the usual costs?
3. Run the noise and regime request. How many of the 200 versions made money, and how many beat your chosen setting?
   Which regimes made money?

You're done when your chart shows the three panels, you can name the drawdown you'd plan for, and Claude has given you a
verdict, with its reasons. Your numbers will differ from the video, and that's fine. This is paper research, not a
setting to trade.

## Try next (optional)

- Change `SEED` in `orb_stress_test.py` and run it again. How much do the percentiles move?
- Make the nudges bigger (`NOISE` in `orb_noise_regimes.py`). At what size do losing versions appear?
- Ask Claude for a block bootstrap: draw runs of consecutive trades instead of single trades, so losing streaks stay
  together. Is the 5th-percentile drawdown worse?
