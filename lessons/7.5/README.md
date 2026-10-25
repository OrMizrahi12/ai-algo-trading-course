# Student kit: Lesson 7.5, Risk and position sizing

Module 7: Day-trading strategies · AI Algorithmic Trading with Claude Code and Interactive Brokers

Every strategy so far answered "when to buy". This lesson answers "how much". You had Claude add three position sizers
to the Trading Lab's backtester: fixed fractional (a stop-out costs 1% of the account), volatility sizing (a normal
day's move, the daily ATR, costs 1%) and a capped fractional Kelly computed only from trades that had already closed.
On the same 354 opening range breakout trades on QQQ (15-minute range), the three sizers gave three different equity
curves, and the no-leverage cap turned out to decide the size of most trades. Then you ran three strategies on one
$100,000 account with a 2% daily loss limit and at most 3 trades a day, looked at the correlation of their daily
results, and saw that the combined account ended below the best strategy alone, because without leverage the
strategies take turns for the cash.

## What's in this kit

| File | What it is |
|---|---|
| `prompts.md` | The two requests typed in the lesson, the commands, and the pause-and-try exercise |
| `cheat-sheet.md` | The three sizers in one line each, the Kelly formula with a worked example, both result tables, and Claude's findings and caveats |
| `trading-lab/backtests/sizing.py` | The three sizers (`FixedFractional`, `VolatilityTarget`, `FractionalKelly`) and `kelly_fraction` |
| `trading-lab/backtests/engine.py` | The engine with the new `sizer=` argument (the default behaves exactly as before; the no-leverage cap applies after any sizer) |
| `trading-lab/reports/sizing_comparison.py` | The same trades under the three sizers: one table and one equity chart in an HTML page |
| `trading-lab/tests/test_sizing.py` | Offline tests for the sizers and the engine wiring (9 tests) |
| `trading-lab/backtests/portfolio.py` | `run_portfolio`: several strategies on one shared account, with a daily loss limit and a trade cap |
| `trading-lab/backtests/portfolio_comparison.py` | The correlation matrix and the one table: each strategy alone vs. combined, with and without the rules |
| `trading-lab/tests/test_portfolio.py` | Offline tests for the portfolio engine (4 tests, including "one strategy matches `run_backtest` exactly") |

The lesson also added the new files to the layout section of `AGENTS.md`.

## Before you start

- The Trading Lab from **Lesson 7.4**: the engine with its `CostModel` and the no-leverage cap, the metrics, and the
  three strategies this lesson uses: `opening_range_breakout` (Lesson 7.4), `donchian_breakout` (Lesson 7.1) and
  `bollinger_rsi_reversion` (Lesson 7.2).
- Two years of SPY and QQQ 5-minute bars in the cache (`data/cache/SPY_5min.parquet` and `QQQ_5min.parquet`).
- No IB connection is needed: everything in this lesson runs offline, from the cache.

## Try it yourself

1. In your `trading-lab` folder, start `claude`, `/clear`, and send the first request in `prompts.md`. Read the table
   before Claude's explanation: which rows have the same number of trades, and which columns change?
2. Ask Claude (or check yourself) how often the no-leverage cap decides the size for each sizer.
3. `/clear`, send the second request, and read the correlation matrix before the table.

You're done when your sizers pass their tests, your table compares all three on the same trades, and you can say in
one sentence why your combined account did, or didn't, beat its best strategy. Your numbers, wording and Claude's
replies will differ from the video; the behaviour is what matters.

## Good to know

- The sizer only picks a share count. The engine then caps it so a position never costs more than the cash in the
  account (no leverage). With a tight stop, like the opening range breakout's, the cap decides most trades, so the
  sizers look more alike than they would on a strategy with wider stops.
- Volatility sizing ignores the strategy's stop; it uses the daily ATR of sessions that closed before the trade.
  Fractional Kelly uses only closed trades; before 30 of them it falls back to plain 1%.
- The Kelly fraction assumes you know your win rate and payoff exactly. You don't: they are estimates from past trades.
  That is why it is always cut down (here: half) and capped (here: 2%). Kelly is shown here as a way to think about
  risk, not as a bet size to use.
- In the combined account every trade uses about the whole account, so whichever signal fires first takes the cash and
  the others are refused (1,618 refusals for lack of cash in the video, mostly the same signal repeating bar after bar).
  Leverage, or a smaller risk per trade, would let the strategies hold positions together; that test was not run.
- Run times: `uv run -m reports.sizing_comparison` under a minute; `uv run -m backtests.portfolio_comparison` about 3
  minutes. The HTML report is written to `reports/` and is gitignored.

## Safety

Paper trading only. Educational content, not financial advice. No sizing method, multiplier, cap or leverage is
recommended: the lesson compares how they behave on two years of cached data. No result in this lesson is a promise,
a recommendation, or a strategy to trade. Nothing in this lesson connects to a broker or places an order.
