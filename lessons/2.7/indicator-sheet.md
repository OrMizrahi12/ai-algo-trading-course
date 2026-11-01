# Indicator sheet (Lesson 2.7)

Every indicator below is a calculation on past prices. It describes what already happened. None of them predicts the
next bar, and a reading on its own is not a reason to buy or sell.

| Indicator | What it measures | How it's calculated (in words) | Usual settings | What it does NOT tell you |
|---|---|---|---|---|
| **Volume** | How many shares traded in each bar | Counted by the exchange, one bar at a time | none | Whether those shares were buys or sells: every trade has a buyer and a seller |
| **VWAP** (volume-weighted average price) | The average price paid today | Each trade's price weighted by its number of shares, averaged over the day; restarts every session | intraday, resets at the open | Where price goes next. It's a reference line, not a target |
| **SMA** (simple moving average) | Smoothed price | The plain average of the last N closes | 20 (also 50, 200 on daily charts) | Direction ahead. It always lags: the smoothing is the lag |
| **EMA** (exponential moving average) | Smoothed price that reacts sooner | An average that gives the newest closes more weight | 20 | The same: it lags, just less than the SMA |
| **RSI** (relative strength index) | The balance of recent up moves against recent down moves, on a 0 to 100 scale | Average size of up closes vs average size of down closes over N bars, turned into a 0 to 100 number | 14; many traders mark 70 (overbought) and 30 (oversold) | That price will turn. A low RSI says price fell hard, not that it will rise |
| **ATR** (average true range) | How far price typically travels in one bar, in dollars | True range = the bar's high minus its low, or the distance from the previous close if the bar gapped (whichever is larger), averaged over N bars | 14 | Direction. Only the size of the moves |
| **Bollinger Bands** | Volatility around an average | A 20-bar moving average, with one line two standard deviations above it and one two below | 20 bars, 2 standard deviations, base average SMA | That a touch of a band is a signal. Wide bands mean big swings, narrow bands mean calm |

## The lesson's readings (QQQ, 5-minute bars, October 22, 2026, delayed data)

- Gap: yesterday's last close 725.21; today's first bar (9:30) high 714.74, low 712.45. A gap down of more than 11
  dollars, about 1.5%.
- Opening range (first three bars): high 714.74, low 712.45, both on the 9:30 bar. Price poked above it at 10:00, then
  broke below it at 10:10 and stayed under VWAP for the rest of the recorded morning.
- After the gap, the EMA(20) bent down before the SMA(20); the Bollinger Bands widened, the upper band to about 732.50.
- RSI(14) sank to about 15 at 10:30; it was back near 36 at 11:20.
- ATR(14) jumped at the gap (the gap counts in the true range) and climbed to about 2.35 dollars at 10:30-10:35. It fell to
  about 1.5 at 10:40, when the 9:30 gap bar left the 14-bar window, and read about 1.33 at 11:20.

These numbers belong to one morning. Your chart will show different ones.

## Settings in TWS

- In TWS, a study's default period is often 9: change it in the Studies window (Period).
- TWS draws the RSI panel with grid lines at 20, 40, 60 and 80. The usual 70 and 30 lines are not drawn there, so
  picture them yourself.
- TWS's Bollinger Bands default to an EMA as the base average; the classic definition uses a simple moving average.
