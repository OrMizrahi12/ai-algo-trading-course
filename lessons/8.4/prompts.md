# Lesson 8.4 prompts and commands

Everything typed in the lesson, in order. Lines that start with `!` run in the terminal from inside Claude Code
(shell mode). Lines that start with `/` are Claude Code commands. Every request runs in auto mode. Nothing here needs an
IB connection: the backtests use the cached bars.

## 1. How luck fools us

```text
/clear
```

```text
Let's see how luck fools us. Create 1,000 strategies on QQQ that enter at random at the open and exit at the close, and show me the best one's Sharpe next to the median. Then compute the Deflated Sharpe Ratio of our opening range breakout with the 15-minute range and the 1R target, counting every setting we tried in this module. Then estimate the Probability of Backtest Overfitting of our 42-cell grid with combinatorially symmetric cross-validation. Explain each number in plain words, and explain combinatorial purged cross-validation briefly. Show everything here, don't open a browser.
```

In the video, Claude read the grid (`backtests/optimize.py`), the search comparison, the noise test and the metrics,
wrote a collection script and an analysis script in its scratchpad, ran the collection in the background (about 12
minutes: the 42 grid cells, 42 random-search trials, 42 Optuna trials and 200 noise versions) and borrowed SciPy for
one run so the project's dependencies stayed unchanged. Nothing was committed yet.

## 2. Save it, numpy only

```text
Yes, save it as reports/luck_vs_skill.py. Rewrite it with numpy only so we don't add a dependency, check the numbers come out the same, add it to AGENTS.md and commit.
```

Claude wrote `reports/luck_vs_skill.py` (181 lines), checked the numpy-only functions against the cached results, ran
the report from scratch, and committed and pushed when the numbers matched. Run it again any time (about 8 minutes):

```text
! uv run -m reports.luck_vs_skill
```

## 3. The judge

```text
/clear
```

```text
Now write our standards down as a judge. Add judge/scorecard.py that takes a strategy name and its settings, runs everything we built in this module, and prints PASS or FAIL for each rule: at least 200 trades, Sharpe after costs, walk-forward result, drawdown at the 5th percentile of the Monte Carlo, break-even cost multiple, Deflated Sharpe and parameter noise. Put the thresholds in judge/standards.yaml, propose sensible ones and explain them. Keep one run to a few minutes per strategy, because our research loops will call it many times. Run it on the opening range breakout on QQQ, the Donchian breakout on SPY and the Bollinger reversion on QQQ, and show the scorecard here.
```

Claude reused the module's helpers, ran every test in one process pool, made `pyyaml` a direct dependency, added
offline tests and committed. Run the judge yourself:

```text
! uv run -m judge.scorecard opening_range_breakout --symbol QQQ --set range_minutes=15 --set target_r=1.0
! uv run -m judge.scorecard donchian_breakout --symbol SPY
! uv run -m judge.scorecard bollinger_rsi_reversion --symbol QQQ
```

Add `--trials N` with the number of settings your research really tried (the Deflated Sharpe needs it; without it the
judge assumes 100). The command exits with code 1 when any rule fails. The offline tests:

```text
! uv run pytest tests/test_scorecard.py -q
```

## 4. Rule 4: judge the settings you would trade

```text
Good catch on rule 3. A judge should test the settings we would actually trade. Add a rule that the fixed settings must have a Sharpe of at least 0.5 on the same walk-forward months, keep the re-tuned check too, rerun the three strategies, show the new scorecard and commit.
```

Claude's first edit script stopped on a mismatched string and changed nothing, so its first scorecards were still the
old seven-rule version; it noticed, checked the real text, applied the edit, reran and committed. The thresholds were
not changed.

## Pause and try

1. Run the luck request. Before you read the answer, write down how high you think the best of 1,000 coin flips will
   score.
2. Save the report, then read its Deflated Sharpe table: how does the answer change with the number of trials?
3. Run the judge on the opening range breakout. Which rules fail, and by how much?

You're done when your best coin flip sits next to its median, and your scorecard prints PASS or FAIL for every rule.
Your numbers will differ from the video, and that's fine. This is paper research, not a strategy to trade.

## Try next (optional)

- Pass the real number of settings you tried with `--trials` and see how rule 7 (Deflated Sharpe) moves.
- Run the judge on another strategy from Module 7. A new strategy needs one entry in `STRATEGIES` in
  `judge/scorecard.py`, with the settings Optuna may tune and their ranges.
- Change a threshold in `judge/standards.yaml` only with a written reason, and never after seeing a result you want
  to rescue.
