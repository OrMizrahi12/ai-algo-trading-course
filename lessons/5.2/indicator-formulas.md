# Indicator formulas

The six indicators in `trading-lab/indicators.py`, in plain words and formulas. An **indicator** is a number computed
from past bars. Every function in the file is **causal**: a row uses only that row and earlier ones. Early rows
without enough history are NaN (not defined yet).

`n` is the window length in bars. `close`, `high`, `low` and `volume` are columns of the bars.

## Look-ahead

**Look-ahead** means using a value you couldn't have known at that bar's time. An indicator with look-ahead makes a
backtest look better than reality. The lesson's test for it: compute every indicator on the full data and on data cut
off at two points (row 300 and row 901). The earlier rows must be identical. If cutting off the future changes the
past, the indicator was peeking.

## Simple moving average (SMA)

The plain mean of the last `n` closes.

```
SMA = (close[t] + close[t-1] + ... + close[t-n+1]) / n
```

pandas: `close.rolling(n).mean()`

## Exponential moving average (EMA)

Like the SMA, but recent closes count more. Each new close moves the average a fixed share of the way toward it:

```
alpha = 2 / (n + 1)
EMA[t] = EMA[t-1] + alpha * (close[t] - EMA[t-1])
```

Seeded with the SMA of the first `n` closes, as TA-Lib does.

## Wilder's smoothing

A running average that moves `1/n` of the way toward each new value. It's an EMA with `alpha = 1/n`, so it reacts
more slowly than the usual EMA of the same `n`. RSI and ATR use it.

```
avg[t] = avg[t-1] + (value[t] - avg[t-1]) / n
```

Seeded with the plain average of the first `n` values.

## RSI (Relative Strength Index)

From 0 to 100: how strong recent gains are compared with recent losses.

```
change = close[t] - close[t-1]
gain = change if change > 0 else 0
loss = -change if change < 0 else 0
RSI = 100 * avg_gain / (avg_gain + avg_loss)     # both Wilder-smoothed over n bars (usually 14)
```

This is the same as the textbook `100 - 100 / (1 + avg_gain / avg_loss)`. Above 70 is often read as "overbought",
below 30 as "oversold". Those are readings of past prices, not signals.

## True range and ATR (Average True Range)

**True range** is a bar's full travel, including any gap from the previous close:

```
TR = max(high - low, |high - previous close|, |low - previous close|)
```

**ATR** is the Wilder average of the true range over `n` bars (usually 14): the typical size of a bar, in dollars.
It's handy later for setting stop distances.

## Bollinger Bands

An SMA with one band `k` standard deviations above it and another `k` below (usually `n = 20`, `k = 2`):

```
middle = SMA(close, n)
upper  = middle + k * std(close over n bars)
lower  = middle - k * std(close over n bars)
```

The bands widen when the market gets volatile and narrow when it's calm. The lesson uses the **population** standard
deviation (divide by `n`, pandas `std(ddof=0)`), as TA-Lib does.

## Session VWAP (volume-weighted average price)

The average price paid so far today, where busy bars count more.

```
typical price = (high + low + close) / 3
VWAP = running sum of (typical price * volume) / running sum of volume     # both reset each New York day
```

pandas: group by the New York date, keep running totals with `cumsum()`, and divide. A new date starts new totals, so
yesterday never leaks into today. A bar with zero running volume gives NaN, not a division by zero.

## Matching a library exactly

Small conventions decide whether your numbers match a library's. The lesson matched TA-Lib's: the EMA and Wilder's
smoothing start from a plain average of the first window, and Bollinger Bands use the population standard deviation.
Otherwise our numbers would drift from the library's, and the tests would fail for the wrong reason.

## Ours vs TA-Lib, from the lesson

The last bar in the cache (October 21, 2026, 15:40 New York, close 772.85):

| Indicator | Ours | TA-Lib | Difference |
|---|---|---|---|
| SMA(20) | 773.136000 | 773.136000 | 1.4e-12 |
| EMA(20) | 772.924185 | 772.924185 | 1.1e-13 |
| RSI(14) | 48.568107 | 48.568107 | 0 |
| ATR(14) | 0.610439 | 0.610439 | 3.3e-16 |
| BB upper | 775.171941 | 775.171941 | 6.5e-12 |
| BB middle | 773.136000 | 773.136000 | 1.4e-12 |
| BB lower | 771.100059 | 771.100059 | 3.8e-12 |
| VWAP | 771.952364 | n/a | n/a |

Differences around a trillionth are floating-point rounding noise, not a bug. TA-Lib has no session VWAP, so the
tests check ours by hand on a tiny two-session example: typical prices 10, 11, 12 with volumes 100, 300, 100 give
10, 10.75 and 11; on day two it restarts at 20.

## Your own, or a library?

- **Write your own** to learn how an indicator works, and to control the details, like where a session starts.
- **Use a library** for speed and trust, and as the referee in your tests.
- In this lesson we did both: our code from scratch, TA-Lib as the referee.
