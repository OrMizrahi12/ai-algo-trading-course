# Six trading styles on one page

Lesson 2.4 · a trading style comes down to one choice: how long you hold a trade.

## One line, from microseconds to years

```
microseconds   seconds   minutes   hours   days   weeks   months   years
|-- HFT --|
             |---- scalping ----|
                       |--- day trading ---|  <- every position closed before the market closes
                                              |---- swing ----|
                                                      |---- position ----|
                                                                   |-- investing --|
```

## Compared

| | High-frequency trading | Scalping | Day trading | Swing trading | Position trading | Investing |
|---|---|---|---|---|---|---|
| **Holding time** | Microseconds | Seconds to minutes | Minutes to hours, flat by the close | Days to a few weeks | Weeks to months | Years |
| **Capital** | Millions (servers next to the exchange, data, engineers) | US day-trading margin rules apply (lesson 2.6) | US day-trading margin rules apply (lesson 2.6) | Can start small | Can start small | Can start small |
| **Your time** | A team of engineers | The whole session at the screen | The whole session at the screen | A check or two a day; fits around a job | A few hours a week | A few hours a year |
| **Stress** | An engineering race, not a human one | Highest: fast decisions all day | High, but you sleep with no open positions | Overnight and weekend gaps | Calm day to day; long losing stretches test patience | Calm day to day; long losing stretches test patience |
| **Costs (spread + commission) as a share of the move** | Tiny per trade, paid at huge scale | Largest | Large | Small | Smaller | Smallest |
| **Overnight risk** | No | No | No | Yes | Yes | Yes |

**Overnight risk**: while the market is closed, news still happens, and the price can open far from where it closed
(a gap). Day traders avoid it by closing every position before the close; every longer style carries it.

**Costs**: every trade pays a spread and a commission. On a trade aiming at a few cents they eat a big share of the
profit; on a trade aiming at dollars they are small. The shorter the holding time, the more costs matter. Lesson 2.6
measures them.

## Why this course day trades on 5-minute bars

1. **Enough trades to measure**: 78 bars a day, about 20,000 a year, so a strategy trades often enough to be tested.
2. **Few enough to reason about**: for you, and later for Claude, which reads every bar.
3. **Costs stay small next to the move**: SPY's spread is often a single cent, about 3% of the 1-minute candles in the
   lesson (about 30 cents high to low), about 1% of the 5-minute candles (about a dollar), a fraction of a percent of a
   daily candle (about 6 dollars).
4. **Years of free history** in 5-minute bars on the paper account.
5. **Flat by the close**: no overnight risk.

These are teaching reasons, not a promise. Day trading is hard, and most strategies fail their tests: that's why this
course tests everything, on paper, first. No style is "best": each fits different time, money and nerves.
