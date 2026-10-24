# Lesson 7.2 cheat sheet: intraday mean reversion

## The opposite bet

| | Trend (Lesson 7.1) | Mean reversion (this lesson) |
|---|---|---|
| The bet | A move that has started keeps going | A price stretched far from "normal" snaps back toward it |
| Buys | Strength (a breakout, an uptrend) | Weakness (a stretch below the average) |
| Target | None, or far away | Small: back to the average |
| Trades | Fewer, larger | Many, small, so costs matter much more |

## The three measures of "stretched"

- **Bollinger bands**: a 20-bar moving average (the middle band) with bands 2 standard deviations above and below it.
  A close below the lower band is unusually far under the recent average.
- **RSI (2-bar)**: a 0 to 100 score of recent up moves against down moves, here over just 2 bars, so it swings fast.
  Under 10 means the last couple of bars were almost all selling.
- **VWAP**: the volume-weighted average price of the day so far (it resets every session). A close more than 2 ATR
  (average bar size) below VWAP is a stretch too.

## The two strategies (long only, 1% risk per trade, 2 ATR stop, flat before the close)

| | `bollinger_rsi_reversion` | `vwap_stretch_reversion` |
|---|---|---|
| Entry signal | Close below the lower band and 2-bar RSI under 10 | Close more than 2 ATR below VWAP |
| Exit | A bar closes at or above the middle band: sell at the next open | A bar closes at or above VWAP: sell at the next open |
| Stop | 2 ATR below the entry | 2 ATR below the entry |

Assumptions Claude added and wrote into the spec notes: Bollinger at 2 standard deviations, ATR over 14 bars, no entries
before 09:45 or in the last 30 minutes, flat 5 minutes before the close, the midday filter off by default, and the
"signal exit" chosen when Claude asked about the exits.

## The cost table

5-minute bars, 2024-10-21 to 2026-10-21, $100,000 start, 1% risk per trade. Costs: zero = none; usual = the engine's
defaults (1 cent commission per share on each side, a 1 cent spread with half paid on every fill, 1 cent slippage on
market fills); double = twice each.

| Strategy | Symbol | Costs | Trades | Net profit | CAGR | Sharpe | Max drawdown | Profit factor | Win rate | Exposure |
|---|---|---|---|---|---|---|---|---|---|---|
| bollinger_rsi_reversion | SPY | zero | 738 | -$506 | -0.3% | -0.02 | -9.3% | 0.99 | 54.3% | 15.1% |
| bollinger_rsi_reversion | SPY | usual | 738 | -$5,960 | -3.0% | -0.57 | -10.0% | 0.92 | 53.8% | 15.1% |
| bollinger_rsi_reversion | SPY | double | 738 | -$11,139 | -5.7% | -1.11 | -12.6% | 0.85 | 53.1% | 15.1% |
| vwap_stretch_reversion | SPY | zero | 699 | -$9,842 | -5.1% | -0.80 | -11.1% | 0.89 | 43.6% | 23.4% |
| vwap_stretch_reversion | SPY | usual | 699 | -$14,586 | -7.6% | -1.21 | -15.1% | 0.84 | 43.5% | 23.4% |
| vwap_stretch_reversion | SPY | double | 699 | -$19,037 | -10.0% | -1.61 | -19.4% | 0.79 | 43.2% | 23.4% |
| bollinger_rsi_reversion | QQQ | zero | 728 | +$4,061 | 2.0% | 0.34 | -9.5% | 1.04 | 55.6% | 14.9% |
| bollinger_rsi_reversion | QQQ | usual | 728 | -$2,173 | -1.1% | -0.14 | -10.1% | 0.98 | 54.9% | 14.9% |
| bollinger_rsi_reversion | QQQ | double | 728 | -$8,018 | -4.1% | -0.61 | -13.0% | 0.91 | 54.0% | 14.9% |
| vwap_stretch_reversion | QQQ | zero | 653 | -$13,796 | -7.2% | -0.88 | -17.4% | 0.88 | 45.2% | 22.8% |
| vwap_stretch_reversion | QQQ | usual | 653 | -$18,393 | -9.7% | -1.20 | -21.0% | 0.83 | 45.2% | 22.8% |
| vwap_stretch_reversion | QQQ | double | 653 | -$22,775 | -12.1% | -1.52 | -24.6% | 0.79 | 44.6% | 22.8% |

How to read it: the trades, the exposure and almost the same win rate in every row of one strategy and symbol: the
signals don't change, only the costs do. Bollinger is roughly break-even before costs (profit factor 0.99 on SPY, 1.04
on QQQ), and the costs on about 730 trades turn that into a loss. VWAP stretch loses even with zero costs: no edge
here. Doubling the costs costs roughly $5k more per run on Bollinger and $4-5k more on VWAP.

## When reversion stops working: trend days vs other days

A trend day is one of the top third of sessions (per symbol) by the absolute move from the open to the close: 168 of
502 sessions. The cutoff is a 0.58% move for SPY and 0.82% for QQQ. Each trade counts on the day it was entered. Usual
costs. R = profit in units of the 1% risked; a stop-out is a trade that hit its 2 ATR stop.

| Strategy | Symbol | Day type | Trades | Net profit | Avg R | Win rate | Stop-outs |
|---|---|---|---|---|---|---|---|
| bollinger_rsi | SPY | Trend | 243 | -$12,189 | -0.052 | 46% | 120 (49%) |
| bollinger_rsi | SPY | Other | 495 | +$6,229 | +0.014 | 58% | 185 (37%) |
| bollinger_rsi | QQQ | Trend | 253 | -$16,532 | -0.066 | 47% | 121 (48%) |
| bollinger_rsi | QQQ | Other | 475 | +$14,359 | +0.031 | 59% | 164 (35%) |
| vwap_stretch | SPY | Trend | 283 | -$29,316 | -0.113 | 28% | 186 (66%) |
| vwap_stretch | SPY | Other | 416 | +$14,730 | +0.040 | 54% | 170 (41%) |
| vwap_stretch | QQQ | Trend | 279 | -$43,381 | -0.173 | 27% | 182 (65%) |
| vwap_stretch | QQQ | Other | 374 | +$24,988 | +0.076 | 59% | 140 (37%) |

What Claude found:

- **The sign flips.** All four combinations lose on trend days and win on other days. Profit factor (gross wins
  divided by gross losses) is 0.43-0.68 on trend days and 1.18-1.71 on the rest.
- **Trend days cost more than the other days earn.** For example, vwap_stretch on SPY loses $29k on trend days
  against $15k gained elsewhere.
- **Stop-outs explain it.** The strategies buy a dip, and on a trend day the dip is often just the first leg of a move
  down that keeps going. vwap_stretch is stopped out on about 65% of its trend-day trades, against about 40% otherwise.
- **Bollinger holds up better, probably.** Claude's reading is that its very oversold 2-bar RSI requirement screens out
  some slow grinding declines. It said plainly that it hadn't tested that.
- **Even "other days" are thin**: +0.014 to +0.076 R per trade, small edges that costs could erase.

## The caveats (the most important part)

- **Hindsight.** Trend days were defined with the day's full open-to-close move. You can't know that at 10 a.m., so
  this shows where the edge goes, not a tradable filter. A usable version needs a signal available early in the day,
  such as the first hour's range or the gap at the open.
- The dollar totals are plain sums of trade P&L, not compounded, on a $100,000 starting account.
- Two years of two highly correlated symbols: treat the pattern as consistent rather than proven.

## Key terms

- **Mean reversion**: the idea that a price far from its average tends to come back toward it.
- **Bollinger bands**: a moving average with bands two standard deviations above and below it.
- **RSI (2-bar)**: a 0-100 score of recent up versus down moves; very low means sharply oversold over the last bars.
- **Spread**: the gap between the best bid and the best ask; you pay part of it on every trade.
- **Trend day**: a day that moves far in one direction from the open and keeps going.
