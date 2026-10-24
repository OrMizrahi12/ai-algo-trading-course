# Lesson 6.3 cheat sheet: metrics and reports

## The eleven metrics, in one sentence each

| Metric | In plain English | In the lesson |
|---|---|---|
| Net profit | Dollars gained or lost over the whole test, after all costs | −$2,540 |
| CAGR | Compound annual growth rate: the steady yearly % return that would turn the starting money into the ending money | −1.3% |
| Sharpe ratio | Average daily return divided by how much daily returns bounce around, scaled to a year; above 1 is generally considered decent | −0.37 |
| Sortino ratio | Like Sharpe, but only down days count as risk, so big up days are not punished | −0.62 |
| Max drawdown | The worst fall from a previous equity peak to a later low: the most you were ever down from your best | −4.9% |
| Profit factor | Total dollars won divided by total dollars lost; above 1 means winners outweigh losers | 0.91 |
| Expectancy | The average net dollars you make (or lose) per trade | −$10.08 |
| Win rate | The share of trades that finished with a profit after costs | 32.9% |
| Average R | The average trade result in R, where 1R is the amount risked if the stop is hit (1% of equity here) | −0.09 |
| Exposure | The share of bars during which a position was open; the rest of the time you held cash | 7.3% |
| Trades | How many round trips (a buy followed by its sell) were made | 252 |

SPY 5-minute bars, 2024-10-21 to 2026-10-21, $100,000 start, 1% of equity risked per trade, costs included.
Before costs the strategy still lost $742; costs took another $1,798.

## Why Sharpe needs care on a day-trading strategy

- Sharpe = average return ÷ how much returns bounce around (standard deviation), scaled to a year.
- Scaling to a year multiplies by the square root of the number of periods. That step assumes each period is
  independent of the next. Five-minute bars are not: they have rhythms through the day, and when the strategy is flat
  (93% of the time here) most of them are exactly zero. Small distortions get multiplied by a big number.
- So `metrics.py` uses **daily** returns: the equity at the end of each New York session, scaled by 252 trading days
  a year. That is the common convention, so the number can be compared with other strategies.
- The risk-free rate is set to 0%. Read Sharpe and Sortino as a rough guide, not a grade, and never on their own.

## The half-day fix

| | Before (6.2) | After (6.3) |
|---|---|---|
| Last entry | fixed 15:30 | 30 minutes before the day's real close |
| Flatten | fixed 15:55 | 5 minutes before the day's real close |
| Normal day (16:00 close) | 15:30 / 15:55 | 15:30 / 15:55 |
| Half day (13:00 close) | 15:30 / 15:55: the flatten never fires | 12:30 / 12:55 |

The real close comes from `exchange_calendars` (calendar `XNYS`), the same library the data pipeline's quality check
uses. The trade it caught: entered 12:55 on 2025-11-28, sold at Monday's open, −$552, −5.2R (more than five times the
planned loss).

| | Before | After |
|---|---|---|
| Trades | 253 | 252 |
| Win rate | 32.81% | 32.94% |
| Total return | −3.08% | −2.54% |
| Profit factor | 0.90 | 0.91 |
| Average trade | −$12.17 | −$10.08 |
| Average R | −0.11 | −0.09 |
| Max drawdown | −5.46% | −4.93% |
| Costs paid | $1,800 | $1,798 |
| Exits (stop / target / time / overnight) | 165 / 73 / 14 / 1 | 165 / 73 / 14 / 0 |

The strategy still loses money with or without the fix. The fix removed one bad trade, not the real problem.

## The report (`reports/spy_vwap_reclaim.html`)

| Section | What to read in it |
|---|---|
| Header | The test window, the start balance, the risk per trade and the cost assumptions |
| Metric cards | The eleven numbers; losses in red |
| Equity curve | The account value over time; the dotted line is the $100,000 start. Hover for date and value |
| Drawdown | How far below its previous peak the account is at each moment; the lowest point is the max drawdown |
| Monthly returns | The change in account value over each calendar month, green up, red down, and each year's total |
| Trades | Every trade: entry and exit in New York time, shares, prices, exit reason, gross P&L, costs, net P&L and R |

## Rules of thumb

- Inspect trades, not just totals: the half-day bug was one trade in 253.
- A new test should fail on the old code and pass on the new one.
- A metric tells you what happened. The trade list tells you why.
