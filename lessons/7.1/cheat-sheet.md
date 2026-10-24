# Lesson 7.1 cheat sheet: ETF breakouts and trend

## Words

- **ETF**: a fund that trades on the exchange like one stock. **SPY** follows the S&P 500, **QQQ** the Nasdaq-100.
- **Breakout**: price moving beyond its recent range (here: a close above the highest high of the last N bars).
- **Donchian channel**: the highest high and the lowest low of the last N bars (here N = 20).
- **ATR (average true range)**: the typical size of one bar. "2 ATR" is room for about two normal bars.
- **Trend following**: buying what is already rising, and holding while it keeps rising.
- **EMA (exponential moving average)**: a moving average that gives the latest bars more weight. EMA20 above EMA50 =
  the short-term trend is up.
- **VWAP (volume-weighted average price)**: the average price paid today, weighted by volume; it resets every day.
- **Midday lull**: the quiet middle of the US session (roughly 11:30 to 14:00 New York) with smaller moves and volume.
- **Time-of-day filter**: a rule that only allows entries in certain hours (here: no new entries 11:30 to 14:00).
- **Edge-triggered entry**: buy only on the bar where a condition switches on, not on every bar while it stays on.
- **R**: a trade's result in units of risk. After this lesson, 1R is a fixed 1% of equity at entry.
- **Position cap**: the engine never buys more than 100% of equity (no leverage), so with a tight stop the real risk is
  smaller than 1%.
- **Outlier**: one result far away from the rest. Always check how much of a total rests on the best trade(s).

## The shape of a trading day (our data: SPY and QQQ 5-minute bars, about 500 sessions per slot)

| Window (New York) | SPY move | QQQ move | SPY volume | QQQ volume |
|---|---|---|---|---|
| 09:30-10:00 | 0.082% | 0.133% | 920k | 809k |
| 10:00-11:30 | 0.064% | 0.091% | 546k | 452k |
| 11:30-14:00 | 0.048% | 0.064% | 369k | 288k |
| 14:00-15:30 | 0.044% | 0.057% | 454k | 294k |
| 15:30-16:00 | 0.058% | 0.071% | 1.35M | 694k |

- The open is the busiest period; the 09:30 bar alone moves about 0.10% (SPY) and 0.17% (QQQ).
- Activity fades into midday, then volume climbs into the close. The 15:55 bar is the busiest of the day (it probably
  includes the closing auction).
- A small bump at 14:00: on some days that is when the Federal Reserve announces its decisions (a likely reason, not
  something this chart proves).
- QQQ moves about 1.4 to 2 times as much as SPY per bar.

## The two strategies (textbook teaching examples, not recommendations)

| | `donchian_breakout` | `ema_trend` |
|---|---|---|
| Entry | the close breaks above the highest high of the previous 20 bars | the bar where EMA20 > EMA50 and close > VWAP becomes true |
| Stop | the tighter of the 20-bar low and entry - 2 ATR (ATR 14) | entry - 2 ATR |
| Exit | flat 5 minutes before the close | trend flip (either condition fails), or flat before the close |
| Target | none | none |
| Time rules | first signal 09:45, no entries in the last 30 minutes, optional no-entry window | same |

## The eight runs (2024-10-21 to 2026-10-21, $100,000 start, usual costs, long only)

| Strategy | Symbol | Window | Trades | Net profit |
|---|---|---|---|---|
| donchian_breakout | SPY | all day | 541 | +$4,759 |
| donchian_breakout | SPY | no 11:30-14:00 | 420 | -$7,082 |
| ema_trend | SPY | all day | 888 | -$10,245 |
| ema_trend | SPY | no 11:30-14:00 | 580 | -$1,740 |
| donchian_breakout | QQQ | all day | 532 | -$1,586 |
| donchian_breakout | QQQ | no 11:30-14:00 | 397 | -$8,179 |
| ema_trend | QQQ | all day | 890 | -$6,455 |
| ema_trend | QQQ | no 11:30-14:00 | 580 | -$11,707 |

- 7 of 8 runs lost money or roughly broke even. The midday filter made 3 of 4 runs worse.
- After the R fix, every average R is within 0.02 of zero: none of the eight shows an edge.

## The average R puzzle

- Average R counts every trade equally; dollars count big-risk trades more.
- With the 100%-of-equity cap, about 99% of Donchian trades were capped: the real risk averaged $258, not $1,000.
- Example (EMA trade #54): stop about $0.89 below a $603.25 entry; 1% risk wanted 1,082 shares (over $650,000 of SPY),
  the cap allowed 164 shares, so a stop-out would cost about $145.
- The fix chosen: keep the cap (no leverage) and measure R against a fixed 1% of equity (commit `6ca7131`).

## One day made the profit

| Donchian on SPY, all day | Net profit |
|---|---|
| All 541 trades | +$4,759 |
| Without the April 9, 2025 trade | -$3,706 |
| Without the best 5 trades | -$9,143 |

April 9, 2025: a 90-day pause on most of the new US "reciprocal" tariffs was announced in the early afternoon (New
York time), and the S&P 500 closed up about 9.5%. The strategy's 20-bar breakout signal came at 12:45, before the news;
the trade rode the spike to the 15:55 flatten (+8.6% on the position). That is luck with timing, not evidence of an edge.

## Checklist before you trust a backtest

1. Does the sum of the trades equal the change in equity?
2. Rebuild one trade by hand from the raw bars.
3. How much of the total comes from the best trade, and from the best five?
4. Does each metric measure what its name says (here: R)?
