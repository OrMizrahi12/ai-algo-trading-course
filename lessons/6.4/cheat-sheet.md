# Lesson 6.4 cheat sheet: verify the engine

## Two ways to check an engine

| Check | What it does | What it proves | What it can't prove |
|---|---|---|---|
| Known-answer test | A tiny case worked out by hand first; the engine must hit those numbers exactly | The engine's arithmetic: fills, costs, sizing, cash | That the strategy is any good, or rules the tiny case doesn't touch |
| Cross-check | The same bars, rules and costs in an independent engine, compared trade by trade | Two engines written by different people agree (or every difference has a cause) | Anything both engines share, such as the same data or the same rule |

If a check is off by a cent, either the engine is wrong or your understanding is. Both are worth knowing.

## The known-answer test

One session of 5-minute bars, $100,000 to start, 1% of equity risked per trade. The engine's default costs, per share:
$0.01 commission on each side, a $0.01 spread with half ($0.005) paid on every fill, and $0.01 slippage on market-type
fills only. A target is a limit order (it fills at your price or better), so it gets no slippage.

The bars (bars are numbered from 0): bar 1 signals with a stop at 99.00 and a target at 102.00; trade 1 buys at bar 2's
open, 100.00; bar 3's low, 98.90, goes through the stop. Bar 5 signals with a stop at 98.10 and a target at 100.70;
trade 2 buys at bar 6's open, 99.20; bar 9's high, 100.90, passes the target.

| | Trade 1 (stopped out) | Trade 2 (hits its target) |
|---|---|---|
| Buy price paid | 100 + 0.005 + 0.01 = 100.015 | 99.20 + 0.015 = 99.215 |
| Risk per share, with costs | 1.015 + 0.035 = 1.050 | 1.115 + 0.035 = 1.150 |
| Shares | 1,000.00 / 1.05, rounded down = 952 | 990.004 / 1.15, rounded down = 860 |
| Cash after buying | 100,000 - 95,214.28 - 9.52 = 4,776.20 | 99,000.40 - 85,324.90 - 8.60 = 13,666.90 |
| Sell price received | 99 - 0.015 = 98.985 | 100.70 - 0.005 = 100.695 (no slippage) |
| Cash after selling | 4,776.20 + 94,233.72 - 9.52 = 99,000.40 | 13,666.90 + 86,597.70 - 8.60 = 100,256.00 |
| Gross profit or loss | -952.00 | +1,290.00 |
| Costs | 47.60 (fees 19.04, spread 9.52, slippage 19.04) | 34.40 (fees 17.20, spread 8.60, slippage 8.60) |
| Net profit or loss | -999.60 | +1,255.60 |
| R (profit as a multiple of the money risked) | -1.00 | +1.27 |

Final equity: **$100,256.00**. The test also checks the equity at three bar closes: 100,166.60 after bar 2, 99,000.40
after bar 3 and 100,010.90 after bar 8. The stop-out loses exactly 1% of equity because the costs are part of the sizing.
The gap-through-stop rule is not in this test: the earlier engine tests from Lesson 6.2 cover it.

## The cross-check, in numbers

All 38,976 SPY 5-minute bars (2024-10-21 to 2026-10-21), backtesting.py 0.6.6:

| | Our engine | backtesting.py |
|---|---|---|
| Trades | 252 | 252 |
| Win rate | 32.94% | 32.94% |
| Return, zero costs | -0.738% | -0.738% |
| Return, with costs | -2.540% | -2.540% |

All 252 trades match by entry time, share count, exit time, exit reason and net P&L. Exits: 165 stops, 73 targets and 14
time exits; 26 trades exit on their own entry bar, and all of them match too.

## Every difference, and its cause

None of them were bugs in our engine.

1. **Cost model.** backtesting.py has one cost per fill and applies its spread to entries only. Our engine charges a
   target exit 1 cent per share less than a stop (no slippage on a limit order). With one flat cost the gap was
   $113.16; the 73 target exits explained $112.43 of it. Charging target exits 1 cent less closed the gap.
2. **Share counts off by one** on 25 trades: the 1-cent gap shifted the equity just enough to change a rounded-down
   share count. They disappeared with fix 1.
3. **A bug in the comparison script**: the commission was counted twice. Found and fixed.
4. **Position cap and commission (not fixed, only masked).** Our engine's "never hold more than 100% of equity" cap
   ignores commission, so cash can dip about $1 below zero. backtesting.py rejected one trade (2026-07-10) for that
   reason. The final run doesn't trigger it, but our engine is a little looser than a real broker. That goes on the list
   for later.

Caveats: to size like our engine, backtesting.py had to peek at the next bar's open, for sizing only, never for the
signal; a real broker couldn't do that. And the check isn't fully independent: both sides use the same data, the same
NYSE calendar and the same reading of the spec.

Something a cross-check can't catch: 251 of 252 trades use 95% or more of the account, because the 100% cap binds
before the 1% risk rule. Both engines share that rule, so they agree on it. Agreement isn't the same as right.

## A map of engines (versions at the time of recording, October 2026)

| | backtesting.py | vectorbt | NautilusTrader | QuantConnect LEAN |
|---|---|---|---|---|
| Version | 0.6.6 | 1.2.0 | 1.231.0 | no usable release number (master branch and cloud platform) |
| Best at | Simple, readable single-asset backtests, with an optimizer and interactive plots | Fast parameter sweeps: thousands of variants at once | One event-driven engine for research and production | A full platform: data, research, backtesting and live trading, many asset classes |
| Fills | Market orders at the next bar's open (or the same bar's close if you ask); stop and limit orders trigger inside the bar | Orders computed in bulk from arrays of signals; flat fees and slippage | A simulated matching engine you can configure, from bars down to the order book | The fill model follows the brokerage model; for IB, IB's fee schedule |
| Live with Interactive Brokers | Not mentioned in its docs: treat it as backtest only | No (open-source version) | Yes: an adapter for TWS or IB Gateway | Yes, in the cloud or self-hosted |
| When you'd use it | As a cross-check | To sweep big parameter grids fast | When one strategy should run in backtest and live | For other asset classes, options, or data you don't want to clean yourself |

Our lab's on-bar design already matches the event-driven model of NautilusTrader and LEAN. What it lacks is live order
management and more realistic fills, such as partial fills and queue position (your place in line at a price). Official
pages: backtesting.py https://kernc.github.io/backtesting.py/ · vectorbt https://vectorbt.dev/ · NautilusTrader
https://nautilustrader.io/docs/latest/ · LEAN https://github.com/QuantConnect/Lean

## Key terms

- **Known-answer test**: a test whose expected result you worked out by hand before running the code.
- **Cross-check**: the same experiment run in an independent engine, compared trade by trade.
- **Limit order**: an order that fills only at your price or better; here, the target, with no slippage.
- **Position cap**: the most of your equity one position may hold (100% in our engine, no leverage).
