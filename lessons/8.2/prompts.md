# Lesson 8.2 prompts and commands

Everything typed in the lesson, in order. Lines that start with `!` run in the terminal from inside Claude Code
(shell mode). Lines that start with `/` are Claude Code commands. Every request runs in auto mode. Nothing here needs an
IB connection: the backtests use the cached QQQ bars.

## 1. Tuning, validation and a holdout

```text
/clear
```

```text
Last time the grid winner scored 2.83 in the first year and 0.75 in the second. Let's do it properly. Split our QQQ data three ways: the first 12 months for tuning, the next 6 months for validation, and the last 6 months as a holdout that nothing touches until the very end. Run the opening range grid on the tuning part only. Pick two candidates: the single best cell, and the best cell of a smoothed plateau. Compare them on validation, then run each once on the holdout. Show the three numbers side by side and explain what we learned.
```

Put your own numbers from Lesson 8.1 into the first sentence if they differ from ours. In the video, Claude read the
grid code from Lesson 8.1 (`backtests/optimize.py`), checked the data range (24 months), wrote
`backtests/split_validation.py` (83 lines) and ran it (under a minute). It reused the grid and the plateau logic, ran
the grid on the tuning part only and touched the holdout only at the end, for the two chosen cells. Then the project's
stop hook made it add a line to `AGENTS.md`, commit and push. Run it again any time:

```text
! uv run -m backtests.split_validation
```

After this run, treat the holdout as spent: if you tune again and look at it again, it is no longer a holdout.

## 2. Walk-forward

```text
/clear
```

```text
Now a walk-forward analysis of the opening range breakout on QQQ: tune on 6 months, trade the next 2 months, then roll forward 2 months and repeat. Inside each tuning window let Optuna pick the range length and profit target with 12 trials. Stitch all the traded months into one out-of-sample equity curve and compare it with the fixed 15 minutes and 1R from last time and with buy-and-hold QQQ over the same months. Save a chart to reports/ (I'll open it myself), and tell me how stable the chosen parameters were from window to window.
```

In the video, Claude read the grid optimizer so the walk-forward uses the same conventions, checked the data, wrote
`backtests/walk_forward.py` (222 lines) and ran it (a few minutes; the windows run in parallel). Optuna 5.0 prints a
`FutureWarning` about `constraints_func`; it still works. Claude also re-tuned every window with four more random seeds
to see how stable the picks are, committed and pushed. Open the chart yourself: paste the file's full path into the
browser's address bar, for example `file:///home/<you>/trading-lab/reports/walk_forward_orb.html` (on Windows,
`file:///C:/Users/<you>/trading-lab/...`). Hover a line to read its values. Run it again any time:

```text
! uv run -m backtests.walk_forward
```

## Pause and try

1. Run the split request. Before you read the answer, write down which candidate you expect to win on the holdout.
2. Run the walk-forward request and open the chart. Which line ends highest, and how often did the chosen range length
   change from one window to the next?
3. Find the stability check in the answer: does the pick change when only the random seed changes?

You're done when your holdout has been opened exactly once, and your walk-forward curve sits next to the fixed setting
and buy-and-hold. Your numbers will differ from the video, and that's fine. This is paper research, not a setting to
trade.

## Try next (optional)

- Give Optuna 50 trials per window instead of 12 (`N_TRIALS` in `walk_forward.py`). Does the pick become more stable?
- Tune on 12 months instead of 6 (`TUNE_MONTHS`). You get fewer windows, but each tuning sees more data.
- Lesson 8.3 shakes the strategy in other ways: the trades in a random order (Monte Carlo), higher costs and
  slippage, small changes to the settings, and different market regimes.
