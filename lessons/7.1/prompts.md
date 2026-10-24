# Lesson 7.1 prompts and commands

Everything typed in the lesson, in order. Lines that start with `!` run in the terminal from inside Claude Code
(shell mode). Lines that start with `/` are Claude Code commands. Nothing here needs an IB connection: everything runs
offline, on the cached SPY and QQQ 5-minute bars.

## 1. The shape of a trading day (auto mode)

```text
/clear
```

```text
Before we write day-trading strategies, show me the shape of a trading day. Using our two years of SPY and QQQ 5-minute bars, compute for every 5-minute slot from 09:30 to 15:55 New York the average absolute move in percent and the average volume. Save an interactive chart to reports/ and open it, and tell me what it says about when trading is active and when it's quiet.
```

Rebuild the chart yourself any time (the HTML file is ignored by Git, the script is committed):

```text
! uv run -m reports.intraday_profile
```

## 2. Two trend strategies (plan mode, then auto mode)

```text
/clear
```

Press Shift+Tab until the footer says "plan mode on", then send:

```text
Plan two intraday trend strategies for SPY and QQQ 5-minute bars, written once on our Strategy interface with a spec and tests each. One: a Donchian breakout, buy when the close breaks above the highest high of the last 20 bars, stop at the 20-bar low or 2 ATR, exit at the close. Two: an EMA trend rule, long while the 20-bar EMA is above the 50-bar EMA and price is above VWAP. Long only, flat before the close, our usual costs. Then backtest both on SPY and QQQ, once trading all day and once with no new entries from 11:30 to 14:00, and give me one table.
```

Claude asks two questions. The answers chosen in the lesson (both were its recommendations):

- Donchian stop: **Tighter of the two**: whichever is closer to the entry, the 20-bar low or entry minus 2 ATR.
- EMA exits: **Trend-flip exit + 2 ATR stop**: sell when either condition stops being true, a protective stop 2 ATR
  below the entry, flat before the close, no profit target.

Read the plan, then approve it with **Yes, and use auto mode**. Run the tests and the comparison yourself:

```text
! uv run pytest -q
! uv run -m backtests.trend_comparison
```

The comparison takes a few minutes (eight runs over about 39,000 bars each).

## 3. The average R puzzle

```text
Something looks odd: Donchian on SPY made $4,759 but its average R is -0.01. How can the average trade lose a little and the total still make money? Find out, and do the hand check of one trade per strategy that you skipped.
```

## 4. Keep the cap, fix R, find the outlier

```text
Keep the cap, no leverage, and report R against a fixed 1% so the number isn't misleading. Rerun the comparison. Also tell me how much of Donchian's SPY profit came from that one trade on April 9, 2025, and what happened in the market that day.
```

## Pause and try

1. Ask Claude for the shape of the trading day in your own cached data (prompt 1).
2. Build one of the two trend strategies with a spec and tests, and backtest it (prompt 2, or one strategy only).
3. Ask how much of the result comes from its single best trade, for example:

```text
How much of this strategy's net profit comes from its single best trade, and from its best five? Show the total with and without them, and the date of the best trade.
```

You're done when you know how much of the result rests on the best trade. Your numbers will differ from the video,
and that's fine.
