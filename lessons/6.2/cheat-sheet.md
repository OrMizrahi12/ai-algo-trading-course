# Lesson 6.2 cheat sheet: an event-driven engine

## Words

| Word | Meaning |
|---|---|
| Event-driven backtest | A loop that processes one bar at a time, oldest first, like live trading |
| Intrabar | What happened inside a bar. We only know its open, high, low and close, not the order of the moves |
| Gap | The price jumps past a level between bars, so an order fills worse than its price |
| Slippage | The difference between the price you wanted and the price you got |
| Spread | The gap between the ask (where you buy) and the bid (where you sell) |
| Position sizing | Choosing the share count so a stop-out costs a fixed share of equity (here 1%) |
| R | A trade's profit measured in units of the dollars it risked. A stop-out is −1R, a 2R target pays twice the risk |
| Profit factor | Total winnings divided by total losses. Below 1.0 the strategy loses money |
| Leverage | Borrowing to hold more than your cash. Off in this course (`max_position_pct=1.0`) |
| Plan mode | Claude Code reads and writes a plan, but changes nothing until you approve (Shift+Tab to switch) |

## The fill rules

1. **Decide at the close, fill at the next open.** The strategy sees only closed bars; its intent fills at the next
   bar's open.
2. **Stops and targets inside every bar**, including the entry bar: the bar's low against the stop, its high against
   the target.
3. **Both touched in one bar: assume the stop.** We can't know which came first, so we take the worse case.
4. **A gap through the stop fills at the open**, never at the stop price. (A gap through the target also fills at the
   open, which is the better price there.)
5. **No position overnight.** A position still open when a new session starts is closed at that session's open.

## Costs and sizing (`CostModel`, assumptions)

| Cost | Default | Paid on |
|---|---|---|
| Commission | 1¢ a share | every buy and sell |
| Spread | 1¢, half of it on every fill | every fill (bar prices are treated as the mid price) |
| Slippage | 1¢ a share | market-type fills only: entries, stops, signal and time exits. A target is a limit order: spread, no slippage |

Sizing: `shares = floor(equity × 1% / risk per share)`, where the risk per share is `fill − stop` plus the exit costs, and
never more than `equity × max_position_pct / fill` (100% of equity, no leverage).
Example from the tests: $100,000 × 1% = $1,000; with $1 of risk per share that's 1,000 shares.

## The loop, for every bar `i`

1. Fill a pending exit at `open[i]`.
2. Fill a pending entry at `open[i]` plus costs (skip it if the stop is not below the real fill).
3. Check the stop and target inside bar `i` (`check_bracket`, stop first).
4. Show the strategy the closed bars up to `i` (the last 200, for speed) and keep its intent for bar `i+1`.

## The results in the lesson (SPY 5-minute, 2024-10-21 to 2026-10-21, $100,000 start, assumed costs)

| Metric | Value |
|---|---|
| Trades | 253 (about one every two days) |
| Win rate | 32.8% |
| Net return | −3.08% |
| Profit factor | 0.90 |
| Average R | −0.11 |
| Max drawdown | −5.46% |
| Costs paid | $1,800 |
| Exits | stop 165, target 73, time 14, overnight 1 |

Before costs the strategy lost about $1,280; costs added another $1,800. A 2R target needs roughly a 33% win rate just to
break even before costs. One instrument, one parameter set, assumed costs: an educational result, not a verdict.

## The two traced trades (New York time)

**Winner** (target hit, +$135.09, +1.76R, 171 shares)

| Bar | High | Low | What happened |
|---|---|---|---|
| 10:45 signal | 581.49 | 581.02 | Closed 581.42, back above VWAP. Stop 581.01, target 582.24 |
| 10:50 | 581.99 | 581.38 | Entry at the open: 581.41 + 0.015 costs = 581.425 |
| 10:55 | 582.18 | 581.84 | Neither touched |
| 11:00 | 582.27 | 581.87 | Target hit: 582.24 minus half the spread = 582.235 |

**Loser** (stop hit, −$108.36, −1.00R, 172 shares; costs $8.60, 8% of the loss)

| Bar | High | Low | What happened |
|---|---|---|---|
| 09:45 signal | 581.55 | 581.12 | Closed 581.55. Stop 580.95, target 582.75 |
| 09:50 | 581.54 | 581.10 | Entry at the open: 581.53 + 0.015 costs = 581.545 |
| 09:55 | 581.52 | 581.17 | Drifted sideways |
| 10:00 | 581.39 | 580.70 | Low under the stop; the bar opened above it, so no gap: fill at the stop less costs, 580.935 |

**Why the 1% rule wasn't binding:** the stop was only about $0.60 below a $581 price, so 1% risk would need about 1,600
shares ($930k of stock). The no-leverage cap cut it to 172 shares: about 0.11% of equity at risk.
