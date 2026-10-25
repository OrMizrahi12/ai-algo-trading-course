# Lesson 7.4 cheat sheet: opening range and VWAP

## The idea in one paragraph

The first minutes after the 9:30 New York open are the busiest of the day. The **opening range** is the high and the low
of the first N minutes (here 5 or 15). An **opening range breakout (ORB)** buys when a 5-minute bar closes above the
range high, puts the stop at the range low, and (in our version) sells 5 minutes before the close if the stop isn't hit.
The bet: a move out of the opening range keeps going for the rest of the day. **VWAP** (the day's volume-weighted
average price) can be a filter: only buy when the close is also above what the average buyer paid today.

## Our strategy: `opening_range_breakout` (long only, no leverage)

| Rule | Our version |
|---|---|
| Range | High and low of the first `range_minutes` (5 or 15) after 09:30 |
| Entry | The first 5-minute close strictly above the range high; one entry per day, no re-entry after a stop-out |
| VWAP variant | `require_above_vwap=True`: the breakout close must also be above VWAP |
| Stop | The range low |
| Target | None: hold to the stop, or flatten 5 minutes before the close |
| Sizing | 1% risk per trade, capped at 100% of equity (no leverage) |
| Costs | The engine's usual costs: 1c commission per share each side, 1c spread (half per fill), 1c slippage on market fills |

## Our results (Oct 2024 to Oct 2026, 5-minute bars, $100,000 start, usual costs)

| Symbol | Range | Variant | Trades | Net profit | CAGR | Sharpe | Max drawdown | Profit factor | Win rate |
|---|---|---|---|---|---|---|---|---|---|
| QQQ | 5 min | plain | 384 | $8,204 | 4.0% | 0.47 | -8.5% | 1.09 | 43.0% |
| QQQ | 5 min | above VWAP | 384 | $8,204 | 4.0% | 0.47 | -8.5% | 1.09 | 43.0% |
| QQQ | 15 min | plain | 354 | $15,263 | 7.4% | 1.00 | -7.5% | 1.19 | 52.3% |
| QQQ | 15 min | above VWAP | 354 | $15,263 | 7.4% | 1.00 | -7.5% | 1.19 | 52.3% |
| SPY | 5 min | plain | 392 | -$6 | 0.0% | 0.03 | -6.9% | 1.00 | 36.2% |
| SPY | 5 min | above VWAP | 392 | -$6 | 0.0% | 0.03 | -6.9% | 1.00 | 36.2% |
| SPY | 15 min | plain | 362 | $10,860 | 5.3% | 0.91 | -4.9% | 1.18 | 46.4% |
| SPY | 15 min | above VWAP | 362 | $10,860 | 5.3% | 0.91 | -4.9% | 1.18 | 46.4% |

Every above-VWAP row equals the plain row: on all 502 days, the first breakout close was already above VWAP, so the
filter never changed a trade.

## What the papers did (as Claude read them in the PDFs)

| | Zarattini & Aziz (2023): QQQ / TQQQ | Zarattini, Barbon & Aziz (2024): all US stocks |
|---|---|---|
| Direction | Long and short, in the direction of the first 5-minute candle (doji skipped); about 51% long, 49% short | Long and short, same direction rule |
| Entry | At the open of the second 5-minute candle | A stop order at the first 5 minutes' high (long) or low (short) |
| Stop | The first candle's low (long) or high (short) | 10% of the 14-day ATR from the entry |
| Exit | A 10R target or the 4pm close | The 4pm close |
| Sizing and leverage | 1% risk per stop-out, up to 4x leverage; TQQQ (a 3x fund) on top | 1% risk, up to 4x |
| Costs | $0.0005 per share commission; "We assumed no slippage in fills" | $0.0035 per share commission; no slippage, spread or borrow cost mentioned |
| Sample | January 2016 to 17 February 2023, no out-of-sample period | January 2016 to December 2023, no out-of-sample period |

Their headline claims, with those assumptions: QQQ about 675% with 4x leverage, TQQQ 1,484% (vs 169% for QQQ); the
top 20 "stocks in play" over 1,600% net with a Sharpe of 2.81 (vs 198% for the S&P 500), but the same ORB on all stocks
only 29% (Sharpe 0.48), and the edge fades with longer ranges (5 min 1,637%, 15 min 272%, 30 min 21%, 60 min 39%).
These are the authors' backtests, not results anyone should expect.

## Why our numbers differ (Claude's reading)

1. **The VWAP filter did nothing**: early in the day VWAP is an average of prices at or below the breakout.
2. **No leverage**: the stop is usually a few cents away, so the no-leverage cap limits the size; real risk was 0.23% to
   0.55% of equity per trade, not 1%.
3. **Costs**: spread and slippage cost about $3,000 per run, the whole gross profit of SPY at 5 minutes.
4. **Long only**: the papers trade both directions; we skip the short half.
5. **A different era and a 2-year sample**: about 380 trades is too few to tell an edge from luck.
6. **Stocks in play**: the 2024 edge comes from picking stocks with unusual opening volume; SPY and QQQ are closer to the
   29% all-stocks baseline.

## "Is the best row safe to trade?" No, not yet

What could make it look better than it is: picking the best of 8 (selection bias), a tiny sample (354 trades in one
regime), gross vs net ($18.6k gross, $15.3k net, slippage guessed at 1c), idealized fills at the open, two years of
mostly rising markets, and a thin cushion from the no-leverage cap.

What to check first (module 8): other ranges (10, 20, 30 minutes: a real edge degrades smoothly), 2x and 3x costs,
dropping the best 5 to 10 trades or days, a bootstrap confidence interval, out-of-sample data (choose on one period,
test on another: this matters most), SPY as a cross-check, and buy-and-hold QQQ as a benchmark. Only then, a few months
of paper trading to compare live fills with the backtest.

## Key terms

- **Opening range**: the high and low of the first N minutes of the session.
- **Breakout**: a trade triggered when price moves beyond a range.
- **VWAP**: the volume-weighted average price of the day so far (it resets every session).
- **Leverage**: a position larger than the account's cash; we keep it off.
- **Selection bias**: picking the best of many noisy results makes it look better than it is.
