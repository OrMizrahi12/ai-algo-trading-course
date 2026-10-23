# Student kit: Lesson 5.1, The data pipeline

Module 5: Data and strategy foundations · AI Algorithmic Trading with Claude Code and Interactive Brokers

Part 1 of the course starts with data. In this lesson you asked Claude, in plan mode, to plan a data pipeline for the
Trading Lab: a downloader for Interactive Brokers historical bars that walks backwards in chunks, stays inside IB's
pacing limits and retries when IB says slow down, and a Parquet cache in UTC that updates incrementally. Claude built
it with offline tests, the `lab-reviewer` agent found two serious bugs (silent gaps from timeouts and data-farm drops,
and a partial first day), and Claude fixed them. The first real run downloaded about a month of 5-minute bars and three
days of 1-minute bars for AAPL and SPY; the second run added only the bars that were new. Then a quality report
checked every file against the NYSE calendar, the same bar was shown in UTC and New York time, and a real test showed
survivorship bias: IB has no data at all for delisted companies.

## What's in this kit

| File | What it is |
|---|---|
| `prompts.md` | Every request and command typed in the lesson, ready to copy, plus the pause-and-try exercise |
| `cheat-sheet.md` | IB's pacing limits, bars per session, UTC vs New York time, the quality checks, survivorship bias, the commands |
| `trading-lab/data_pipeline/config.py` | The settings: paper port 4002, client ID 5, symbols, bar sizes, chunk sizes, retry backoff |
| `trading-lab/data_pipeline/cache.py` | One Parquet file per symbol and bar size, timestamps in UTC, written atomically |
| `trading-lab/data_pipeline/downloader.py` | The downloader: walks backwards in chunks, throttles, retries pacing errors and dropped data farms, drops the forming bar |
| `trading-lab/data_pipeline/quality.py` | The quality report: duplicates, bad prices, OHLC errors, zero volume, gaps, missing NYSE days |
| `trading-lab/data_pipeline/__main__.py` | The command: `uv run -m data_pipeline` (`--dry-run`, `--quality`, `--symbols`, `--bar-sizes`) |
| `trading-lab/data_pipeline/__init__.py` | Makes the folder a Python package |
| `trading-lab/tests/test_data_pipeline.py` | Offline tests for the downloader with a fake IB (no Gateway needed) |
| `trading-lab/tests/test_quality.py` | Offline tests for the quality report: hand-built bars with one known defect each |
| `trading-lab/pyproject.toml` | The project file after the lesson: adds `pyarrow`, `exchange-calendars` and `pytest` |

## Before you start

- IB Gateway installed and logged in to **paper** (Lessons 4.1 and 4.2), with the API on port 4002. One login at a
  time: close TWS if it uses the same paper username.
- The Trading Lab from Modules 3 and 4, with `uv`, the `paper-guard` skill, the `lab-reviewer` agent (Lesson 3.5) and
  both hooks (Lesson 3.6).
- `market_data.py` from **Lesson 4.3**. The downloader imports its `Throttle` (the helper that keeps historical
  requests under IB's pacing limits), and the tests import it too. Without it, `import market_data` fails.
- Client ID 5 must be free on your Gateway (the pipeline uses it). If one of your own scripts already uses 5, change
  `CLIENT_ID` in `data_pipeline/config.py`.

## Try it yourself

1. In your `trading-lab` folder, start `claude`, press **Shift+Tab** until the footer says **plan mode on**, and send
   the first request in `prompts.md`. Read the plan before you approve it.
2. Let Claude build and test it. Ask for the `lab-reviewer` agent and the `paper-guard` skill before the commit if
   Claude doesn't run them by itself.
3. Run `! uv run -m data_pipeline` twice. The first run fills the cache; the second should add only a bar or two.
4. Send the second request in `prompts.md` (quality report, UTC vs New York, survivorship test), then run
   `! uv run -m data_pipeline --quality`.

You're done when your second run adds a bar or two at most, and your quality report is clean apart from today's newest
bars. Your numbers, wording and Claude's replies will differ from the video; the behaviour is what matters.

## Good to know

- Free paper data is delayed (about 15 minutes for US stocks). A run near the close misses the last bars of the day;
  the next run fills them in. That's stale, not corrupt.
- The cache lives in `data/cache/` and is ignored by Git (`.gitignore`). Delete that folder to download everything
  again from scratch (about 9 requests per symbol).
- Survivorship bias: IB has no data for stocks that no longer trade, so anything you backtest on IB history only sees
  the survivors. Treat those results as an upper bound.

## Safety

Paper trading only. Educational content, not financial advice, and no data in this lesson is a recommendation to buy
or sell anything. The pipeline refuses any port other than the paper ports 7497 (TWS) and 4002 (IB Gateway), connects
read-only, places no orders, and disconnects unless every account starts with `DU`, IBKR's prefix for paper accounts.
Never put a live-account login into this project.
