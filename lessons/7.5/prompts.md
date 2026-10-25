# Lesson 7.5 prompts and commands

Everything typed in the lesson, in order. Lines that start with `!` run in the terminal from inside Claude Code
(shell mode). Lines that start with `/` are Claude Code commands. Both requests run in auto mode. Nothing here needs an
IB connection.

## 1. Three position sizers, on the same trades

```text
/clear
```

```text
Teach me position sizing with our lab. Add three sizers to the backtester: fixed fractional, risking 1% of the account per trade; volatility sizing, where a normal day's move (the daily ATR) costs 1%; and a fractional Kelly computed only from trades that already happened, capped. Run the opening range breakout on QQQ with the 15-minute range under each sizer, no leverage, and show me a table and an equity chart in Chrome. Explain the Kelly fraction in plain words and why we cap it.
```

Claude reads the engine and the opening range breakout strategy first, puts the sizing behind a small `Sizer`
interface (the default stays exactly as before), writes `backtests/sizing.py` and its tests, fixes one edge case the
tests found (fewer than 15 sessions of data for the ATR), and writes `reports/sizing_comparison.py`. It then checks how
often the no-leverage cap decides the size, and commits. Run them yourself any time:

```text
! uv run pytest -q
! uv run -m reports.sizing_comparison
```

The report is written to `reports/sizing_comparison.html`. If Claude can't open a browser on your machine, open that
file in Chrome yourself (in the video, Claude said it couldn't see the window, so we opened the file ourselves).

## 2. Three strategies, one account

```text
/clear
```

```text
Now treat our strategies as one account: opening range breakout on QQQ with the 15-minute range, the Donchian breakout on SPY and the Bollinger reversion on QQQ. Show how correlated their daily results are, then run them together on one $100,000 account with a 2% daily loss limit and at most 3 trades a day. Compare the combined account with each strategy alone in one table and explain what diversification did and did not do. Don't open a browser; show everything here.
```

Claude builds `backtests/portfolio.py` (one shared cash pool, the daily loss limit and the trade cap), tests it (a
one-strategy portfolio must match `run_backtest` exactly), runs `backtests/portfolio_comparison.py`, checks the
refusals for lack of cash before it reports, and commits when the Stop hook asks. Run it yourself:

```text
! uv run -m backtests.portfolio_comparison
```

## Pause and try

1. Build the three sizers with the first request, and read the table before Claude's explanation.
2. Find out how often the no-leverage cap decides the size for each sizer.
3. Run the three strategies as one account with the second request, and read the correlation matrix first.

You're done when your sizers pass their tests, your table compares all three on the same trades, and you can say why
your combined account did, or didn't, beat its best strategy. Your numbers will differ from the video, and that's fine.

## Try next (optional)

- Run the sizing comparison on a strategy with wider stops (for example `donchian_breakout`), where the cap binds less
  often, and see how far apart the three sizers move.
- Ask Claude to rerun the combined account with a smaller risk per trade (for example 0.25%) so the strategies can hold
  positions at the same time. Claude named this as the test that would show real diversification, and did not run it.
