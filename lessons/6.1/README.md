# Student kit: Lesson 6.1, How backtests lie, and a first engine

Module 6: The backtest engine · AI Algorithmic Trading with Claude Code and Interactive Brokers

One month of bars is far too little to test a strategy. In this lesson you asked Claude to add a resumable backfill to
the Trading Lab's data pipeline, and pulled two years of 5-minute bars for SPY and QQQ from Interactive Brokers, inside
IB's pacing limits. While it downloaded, you met the four classic ways a backtest lies: look-ahead bias, survivorship
bias, unrealistic fills and missing costs. Then Claude built a first, vectorized backtester for a simple EMA trend rule
and broke it on purpose: a one-bar look-ahead turned +1.67% into +19.40%, and realistic costs turned it into −0.14%.

## What's in this kit

| File | What it is |
|---|---|
| `prompts.md` | Both requests typed in the lesson, the commands, and the pause-and-try exercise |
| `cheat-sheet.md` | The four lies, how the backfill works, how the vectorized backtester works, the lesson's results table |
| `trading-lab/data_pipeline/downloader.py` | The downloader with the new `backfill()` function (walks back one chunk at a time, saves each chunk, resumable) |
| `trading-lab/data_pipeline/__main__.py` | The command, now with `--backfill-years N` (also with `--dry-run`) |
| `trading-lab/data_pipeline/config.py` | The settings, with the new `MAX_EMPTY_CHUNKS` |
| `trading-lab/tests/test_data_pipeline.py` | The offline tests, including the five new backfill tests (no Gateway needed) |
| `trading-lab/backtests/vectorized.py` | The vectorized backtester: honest, look-ahead and costs versions side by side |

The other files of the `data_pipeline` package (`cache.py`, `quality.py`, `__init__.py`) are unchanged since Lesson 5.1.

## Before you start

- The Trading Lab with the `data_pipeline` package from **Lesson 5.1** (and its `Throttle` from `market_data.py`,
  Lesson 4.3) and `indicators.py` from **Lesson 5.2** (the backtester imports `indicators.ema`).
- IB Gateway installed and logged in to **paper** (Lessons 4.1 and 4.2), with the API on port 4002, for the download.
  The backtester itself works offline, from the cache.
- About half an hour for the two-year download. You can keep working meanwhile.

## Try it yourself

1. In your `trading-lab` folder, start `claude`, `/clear`, and send the first request in `prompts.md`.
2. When the download is done, check the quality report: both files should cover about two years.
3. `/clear`, send the second request, and read the three-column table.

You're done when your table shows the look-ahead version far ahead of the honest one, and the costs version below
the honest one. Your numbers, wording and Claude's replies will differ from the video; the behaviour is what matters.

## Good to know

- The cache lives in `data/cache/` and is ignored by Git. The backfill only adds older bars; a normal update
  (`uv run -m data_pipeline`) adds the newest ones.
- Free paper data is delayed. A file updated during the day can end before the close; the next normal update fills it.
- The backtester has no tests yet. Treat its numbers as a first look; the engine gets proper tests later in Module 6.

## Safety

Paper trading only. Educational content, not financial advice. The EMA rule is a teaching example: no result in this
lesson is a promise, a recommendation, or a strategy to trade. The data pipeline refuses any port other than the paper
ports 7497 and 4002 and places no orders; the backtester never touches a broker.
