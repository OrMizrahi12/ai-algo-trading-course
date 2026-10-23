# Lesson 6.1 prompts and commands

Everything typed in the lesson, in order. Lines that start with `!` run in the terminal from inside Claude Code
(shell mode). Lines that start with `/` are Claude Code commands. Both requests run in auto mode.

## 1. Two years of history (the backfill)

IB Gateway must be running and logged in to **paper**, with the API on port 4002.

```text
/clear
```

```text
One month of bars is far too little to test a strategy. Add a backfill option to the data pipeline that walks further back in time in chunks, with the same pacing rules, and can resume if it stops. Test it offline, then fetch two years of 5-minute bars for SPY and QQQ and run the quality check.
```

Claude adds a `--backfill-years N` option and five offline tests, then starts the download in the background. Two years
of 5-minute bars for two symbols is about 200 historical requests, so under IB's pacing limits it takes roughly half an
hour. You can keep working in another terminal meanwhile.

The same download by hand, and a dry run that only shows the plan:

```text
! uv run -m data_pipeline --symbols SPY QQQ --bar-sizes 5min --backfill-years 2 --dry-run
! uv run -m data_pipeline --symbols SPY QQQ --bar-sizes 5min --backfill-years 2
```

If it stops (a lost connection, a pacing error, Ctrl+C), run the same command again: it resumes from the oldest bar
already in the cache.

Then the quality check (offline, from the cache) and a normal update for anything that ends before the close:

```text
! uv run -m data_pipeline --quality
! uv run -m data_pipeline --symbols SPY QQQ --bar-sizes 5min
```

## 2. A first engine, and two lies

```text
/clear
```

```text
Build backtests/vectorized.py, a simple vectorized backtester: on SPY 5-minute bars, be long when the 20-bar EMA is above the 50-bar EMA, flat otherwise and always flat at the close, trading at the next bar's open. Report the trades, total return, win rate and max drawdown. Then break it on purpose in a side-by-side table: a version with a one-bar look-ahead, and a version with realistic costs of one cent a share plus a one-cent spread. Explain what each lie does.
```

Run it yourself any time (it reads the cache, no IB connection):

```text
! uv run -m backtests.vectorized
```

## Pause and try

1. Backfill two years of 5-minute bars for SPY and QQQ with the first request (or the commands above), then run the
   quality check.
2. Build the vectorized backtester with the second request and read its three-column table.

You're done when your table shows the look-ahead version far ahead of the honest one, and the costs version below the
honest one. Your numbers will differ from the video (a different two-year window, a different day), and that's fine.

## Try next (optional)

- Make the costs bigger or smaller (`COMMISSION`, `SPREAD` in `backtests/vectorized.py`) and watch where the edge
  disappears.
- Ask Claude to add a two-bar look-ahead (`lag=-1` in `backtest()`) and compare it with the one-bar version.
