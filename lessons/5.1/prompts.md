# Lesson 5.1 prompts and commands

Everything typed in the lesson, in order. Lines that start with `!` run in the terminal from inside Claude Code
(shell mode). Lines that start with `/` are Claude Code commands.

## 1. Plan the pipeline (plan mode)

```text
/clear
```

Then press **Shift+Tab** until the footer says **plan mode on**. In plan mode Claude reads and plans, but changes
nothing until you approve.

```text
Part 1 of the course starts here: data. Plan a data pipeline for the lab, in a data_pipeline package: a downloader for Interactive Brokers historical bars (client ID 5, Gateway port 4002) that walks backwards in chunks with endDateTime, respects IB's pacing limits and retries on pacing errors, and saves bars into a Parquet cache, one file per symbol and bar size, stored in UTC. Updates must be incremental: download only bars newer than what the cache already has. Start with US stocks AAPL and SPY: 5-minute bars for the last month and 1-minute bars for the last 3 trading days.
```

(In the video the request ends with one more sentence about forex. This course sticks to US stocks and ETFs, so it is
left out here.)

When the plan is ready, read it, then choose **1. Yes, and use auto mode**. Claude builds the package and the offline
tests, runs the `paper-guard` skill and the `lab-reviewer` agent, commits, and then fixes what the reviewer found.

## 2. The first real download

IB Gateway must be running and logged in to paper, with the API on port 4002.

```text
! uv run -m data_pipeline
```

## 3. Run it again (incremental update)

```text
! uv run -m data_pipeline
```

The second run should add zero or one bar per file: only bars that finished since the first run.

## 4. Quality, time and survivorship

```text
/clear
```

```text
Now data quality and time. Add a quality report to data_pipeline: for each cached file check gaps inside sessions, duplicate timestamps, zero or negative prices, bars where high is below low or the close is outside the high-low range, zero-volume bars, and whole trading days missing compared with the NYSE calendar. Show the report for our four files. Then show me the same AAPL bar in UTC and in New York time, and explain why we store UTC. Finally, explain survivorship bias with a real test: ask IB for a well-known delisted US stock and show what comes back. Commit and push.
```

Run the report yourself any time (it works offline, from the cache):

```text
! uv run -m data_pipeline --quality
```

## Useful extras

```text
! uv run -m data_pipeline --dry-run
! uv run pytest -q
! uv run -m data_pipeline --symbols QQQ --bar-sizes 5min
```

`--dry-run` shows what each file would fetch, without connecting to IB. `pytest` runs the offline tests (no Gateway
needed). The last line downloads another symbol or bar size into its own file.

## Pause and try

Build your own pipeline with the two requests above. Run the download twice: the second run should add almost nothing.
Then run the quality report.

You're done when your second run adds a bar or two at most, and your quality report is clean apart from today's newest
bars.
