# Student kit: Lesson 2.7, Reading price on the chart

Module 2: Markets from zero, on a real trading platform · AI Algorithmic Trading with Claude Code and Interactive Brokers

In this lesson you read a price chart in Trader Workstation (TWS), on the paper account, with QQQ (the Nasdaq-100 ETF)
on 5-minute candles. You read a candle's open, high, low and close, switch to the daily chart to tell a trend from a
range, look at a gap and the trading sessions behind it, mark resistance, support and the opening range with horizontal
lines, and read volume and VWAP. Then you add four classic indicators (a simple moving average, RSI, ATR and Bollinger
Bands), see what each one really measures on the same chart, and clean the chart up again.

## What's in this kit

| File | What it is |
|---|---|
| `chart-reading-checklist.md` | A step-by-step checklist for reading any chart, the TWS menu paths of the lesson, and a blank sheet for your own reading |
| `indicator-sheet.md` | What each indicator of the lesson measures, how it is calculated (in words), its usual settings, and what it does NOT tell you |

## Try it yourself

1. Log in to TWS with your **paper** account and open a chart of **QQQ** or **SPY** on **2 Days / 5 min candles**.
2. Hover one candle and read its **high, low and close** in the bar details at the bottom left; read the open from the
   candle's body.
3. Switch the chart to **1 Year / Daily** candles. Find one **trend** (higher highs and higher lows, or lower highs and
   lower lows) and one **range** (sideways between two levels). Switch back to 5-minute candles.
4. Compare **yesterday's last close** with **today's first bar**: is there a gap? How big, in dollars and in percent?
5. With **Edit > Horizontal Line**, mark yesterday's high, today's low so far, and the high and low of the **first three
   5-minute bars** (the 15-minute opening range).
6. Add **RSI 14** and **ATR 14** (Edit > Studies), read their values on today's bars, then remove them again.
7. You're done when you can say, for today: the size of the gap, the opening range, and whether price sits above or
   below **VWAP**.

## Remember

- Everything in this course runs on a **paper (simulated) account**. The symbols are examples, not recommendations.
- Free market data is **delayed**, about 15 minutes behind the market. Your chart will show different prices and dates.
- Indicators are calculations on **past** prices. They describe what already happened; none of them predicts the next
  bar. A level, a break or an indicator reading is an observation, not a signal.
- Later in the course, these same indicators are computed in Python, and trading rules built on them are tested on years
  of data before anyone trusts them.
- Your paper account number is private (TWS shows it at the top right and in window titles). Don't post it in
  screenshots or forums.
- TWS menus and dialogs can change between versions.
