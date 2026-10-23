# Lesson 6.1 cheat sheet: how backtests lie, and a first engine

## Words

| Word | Meaning |
|---|---|
| Backtest | Running a strategy's rules over past data to see what would have happened |
| Vectorized backtest | Computing the signal, the position and the profit for every bar at once with whole-column math, no loop. Fast, short, and easy to fool |
| Look-ahead bias | Using information you could not have had at the moment of the decision |
| Survivorship bias | Testing only on what still exists today (Lesson 5.1: IB has no data for delisted stocks) |
| Fill | The price you actually trade at |
| Costs | Commission, the bid-ask spread and slippage |
| Spread | The gap between the ask (where you buy) and the bid (where you sell) |
| Equity curve | The account value over time |
| Max drawdown | The deepest drop of the equity curve from a peak |
| Backfill | Walking further back in history, one chunk at a time, from the oldest bar you already have |

## The four classic lies

1. **Look-ahead bias.** The signal comes from a bar's close, but the trade fills at that same bar's open, five minutes
   earlier. Honest timing: decide at the close, trade at the **next** bar's open.
2. **Survivorship bias.** A stock list built from today's names skips every company that died along the way. SPY and
   QQQ are funds that still trade, so it does not affect this lesson's test; it matters when you pick stocks.
3. **Unrealistic fills.** Buying at the exact close that created the signal, filling every limit order the moment the
   price touches it, never slipping on a stop.
4. **Missing costs.** A few cents a share is nothing per trade, and a lot over hundreds of trades.

## The backfill

```text
uv run -m data_pipeline --symbols SPY QQQ --bar-sizes 5min --backfill-years 2 [--dry-run]
```

- Starts at the oldest cached bar (or now, if there is no cache) and asks for the week before it, then the week before
  that, through the same throttle, retries and pacing handling as the normal update.
- Writes every chunk to the cache as soon as it arrives, so the cache never has a hole. Rerun the same command to
  resume after a stop.
- Gives up after 6 empty chunks in a row (`MAX_EMPTY_CHUNKS`), so a symbol without older data does not burn requests.
- In the lesson: about 200 requests, about half an hour; both files ended with 38,976 bars (2024-10-21 09:30 to
  2026-10-21 15:55 New York time), about 500 trading days.

## The vectorized backtester (`backtests/vectorized.py`)

| Piece | How it works |
|---|---|
| Signal | 1 when EMA(20) > EMA(50) on a bar's close, else 0 (EMAs from `indicators.ema`, not reset each morning) |
| Position | The signal shifted by one bar: `pos = signal.shift(1)`. Never carried overnight |
| Profit per bar | `pos × (next open − this open) × 100 shares`; the last bar of the day exits at its own close |
| Look-ahead version | `lag=0`: the bar's own close decides the position held from its open |
| Costs version | 1¢ commission + ½¢ (half the 1¢ spread, opens treated as the midpoint) = 1.5¢ a share per fill, 3¢ a round trip |

## The results in the lesson (SPY 5-minute, 2024-10-21 to 2026-10-21, 100 shares, $100,000 start)

| | honest | look-ahead | honest + costs |
|---|---|---|---|
| trades | 604 | 599 | 604 |
| total return | +1.67% | +19.40% | −0.14% |
| win rate | 42.4% | 48.1% | 42.2% |
| max drawdown | −5.93% | −2.57% | −6.75% |
| avg profit per trade | $2.77 | $32.39 | −$0.23 |
| costs paid | $0 | $0 | $1,812 |

The rule is a teaching example, not a strategy to trade. Your numbers will differ.

## Rules of thumb

- If a backtest looks far better than it should, suspect a look-ahead first.
- Costs scale with the number of trades: an edge smaller than the cost of trading it is no edge.
- A backtester without tests is a claim, not a tool. (The engine gets its own tests later in this module.)
