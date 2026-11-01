# Chart-reading checklist (Lesson 2.7)

Use it top to bottom on any 5-minute chart of a US stock or ETF, on your paper account.

## 1. The candle (OHLCV)

- [ ] One candle = one bar of the bar size (here 5 minutes). It carries four prices: **open, high, low, close**.
- [ ] The **body** runs from the open to the close; the **wicks** reach the high and the low.
- [ ] **Green** (or hollow on some charts): the close is above the open. **Red**: the close is below the open.
- [ ] **Volume** (the panel under the chart): the number of shares traded in that bar.
- [ ] In TWS, hover a candle: the bar details at the bottom left of the chart show `date time  H  L  C`. The open is not
      listed there: read it from the body (green: bottom of the body; red: top of the body).

## 2. The timeframe, trend and range

- [ ] The chart title is the bar-size menu (for example `2 Days/5 min candles`). The first part is the **time period**
      shown, the second the **bar size**.
- [ ] Look at the **daily** chart (`1 Year/Daily candles`) for the bigger picture, then go back to the short chart.
- [ ] **Trend up**: higher highs and higher lows. **Trend down**: lower highs and lower lows.
- [ ] **Range**: price moves sideways between two levels and keeps turning back at them.

## 3. Gaps and sessions

- [ ] Yesterday's **last close** vs today's **first bar**: a big jump between them is a **gap** (up or down).
- [ ] Gap size = today's open minus yesterday's close; in percent = gap / yesterday's close x 100.
- [ ] US stocks: the **regular session** runs 9:30 a.m. to 4:00 p.m. New York time. Trading also happens **pre-market**
      (from as early as 4:00 a.m. on some venues) and **after-hours** (until 8:00 p.m.), with much less volume. A 5-minute
      TWS chart shows regular hours by default, so news from those hours shows up as a gap at the open.

## 4. Levels

- [ ] **Resistance**: a price area where rises have stalled before (yesterday's high is a common one).
- [ ] **Support**: a price area where drops have stopped before. One touch is not support yet.
- [ ] Levels are areas, not exact prices, and they break all the time.
- [ ] TWS: **Edit > Horizontal Line**, then one click on the chart. The line shows its price at its middle.

## 5. The opening range

- [ ] The **opening range** = the highest high and the lowest low of the first N minutes of the session.
- [ ] 15 minutes on 5-minute bars = the **first three bars** (9:30, 9:35, 9:40).
- [ ] Mark both with a horizontal line. Note what price does later: above, inside or below the range. That is an
      **observation**, not a signal.

## 6. Volume and VWAP

- [ ] Compare today's volume bars with yesterday's: the open is usually the busiest time of the day.
- [ ] **VWAP** (volume-weighted average price): the average price of today's trades, each weighted by its size. It
      starts fresh at every open. Price above VWAP: today's average buyer is in profit; below: in a loss.

## 7. Indicators (see `indicator-sheet.md`)

- [ ] Add one at a time, and only when you know which question it answers.
- [ ] TWS: **Edit > Studies**, search, **Add**, set the **Period**, **OK**. Remove: select it under Applied Studies, **Remove**.
- [ ] Clean up: **Edit > Clear All Annotations** removes your drawn lines; the small **x** at the top left of an indicator
      panel closes it.

## TWS menu paths used in the lesson

| What | Where |
|---|---|
| Change bar size / time period | Click the chart title (`2 Days/5 min candles`) > Time Period / bar size |
| Horizontal line | Chart menu **Edit > Horizontal Line**, one click on the chart |
| Add an indicator | **Edit > Studies** > search > **Add** > set Period > **OK** |
| Bollinger base average | In Studies, select BOL > **Base Average** (EMA by default) > SMA |
| Remove drawings | **Edit > Clear All Annotations** |
| Remove an indicator | **Edit > Studies** > select under Applied Studies > **Remove** > **OK** |

## My reading (fill in for one day)

| Item | Your value |
|---|---|
| Symbol, date | |
| Yesterday's close | |
| Today's first bar: high / low | |
| Gap (dollars, percent) | |
| Opening range high / low (first 15 minutes) | |
| Yesterday's high (resistance?) | |
| Today's low so far (support?) | |
| Price vs VWAP now (above / below) | |
| Daily chart: trend or range? | |
| RSI(14) now / ATR(14) now | |
