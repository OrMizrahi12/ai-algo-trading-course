# Lesson 5.3 cheat sheet: a strategy is a spec

## Words

| Word | Meaning |
|---|---|
| Spec | Short for specification: the full, precise rule book of a strategy. If a rule isn't in it, the code doesn't have it |
| Entry / exit | The exact conditions to open and to close a position |
| Stop-loss (stop) | The price where you admit you were wrong and get out: fixed, ATR-based, trailing or time-based |
| Take profit (target) | The price where you lock in the win, often a multiple of the risk |
| R | The dollars you risk per share: entry minus stop. A 2R target sits twice as far above the entry as the stop is below it |
| Filter | A condition that blocks trades (the first 15 minutes, low volume, news days) |
| Look-ahead | Using information you wouldn't have had yet, such as buying at a bar's close that was only known after the bar ended |
| Interface | The agreed shape of a piece of code (what goes in, what comes out), so other parts can plug into it |
| Bracket | An entry with a stop and a profit target attached |

Reminders from Lesson 5.2: **VWAP** is the day's volume-weighted average price, a running "fair price" that resets
every session. The **EMA** is a fast-reacting moving average. **ATR** (average true range) is the average size of a
bar.

## The sections of a spec (`TEMPLATE.yaml`)

| Section | What it pins down | In `spy_vwap_reclaim.yaml` |
|---|---|---|
| `market` | Symbol, instrument, direction | SPY, ETF, long only |
| `timeframe` | Bar size and where the bars come from | 5-minute bars from `data/cache` (Lesson 5.1) |
| `session` | Time zone, session times, opening skip, last entry | New York, 09:30-16:00, skip 15 minutes (first signal bar 09:45), no entries from 15:30 (assumption) |
| `indicators` | Every indicator the rules use, with settings | VWAP (resets every session), EMA 20, ATR 14 (assumption) |
| `entry` | Conditions, trigger, fill, limits | EMA20 above VWAP; previous close at or below VWAP and current close above it; fill at the next bar's open; 1 trade a day, 1 position |
| `stop` | Fixed, ATR, swing, trailing, time | Swing low of the last 10 bars minus 1 cent (assumptions), capped at 1.5 ATR below the entry; trailing and time stops off |
| `take_profit` | Target rule | 2R: entry + 2 x (entry - stop) |
| `exit` | Time exit and what wins when both levels are hit | Sell at the open of the 15:55 bar; stop first when one bar touches both |
| `sizing` | How many shares | Risk 1% of a 100,000 paper account per trade; never more than 100% of equity (no leverage) |
| `filters` | Extra trade blockers | None used (slots for ATR, volume, skip dates, trend) |
| `costs` | Commission and slippage | Zero, as placeholders: set them before you trust any backtest |
| `notes` | Assumptions added beyond the idea, extra rules | Skip the trade if the entry bar's own low is under the stop, or the stop is at or above the entry (a gap) |

Rule of thumb: every vague word becomes a number or a time. "Dip" became "the previous close at or below VWAP",
"before the close" became "15:55", "near the low" became "the lowest low of 10 bars minus 1 cent".

## The four questions Claude asked

1. **Cross rule.** Prior bar below, this bar above (chosen: simple, fires on every reclaim) / below for at least 3 bars
   (fewer trades) / a minimum depth (one more parameter).
2. **Stop rule.** Tighter of the two / wider of the two / swing low capped at 1.5 ATR (chosen: works like the tighter
   rule, but states the intent as a cap).
3. **Entry fill.** Next bar's open (chosen: realistic, no look-ahead) / the signal bar's close (slightly optimistic) /
   a stop-limit above the signal high (some signals never fill).
4. **Flat and limits.** Exit at the 15:55 bar, max 1 trade a day (chosen) / up to 3 trades a day / exit at 15:45.

## The Strategy interface (`strategies/base.py`)

```python
class Strategy(ABC):
    @abstractmethod
    def on_bar(self, bars: pd.DataFrame, position: Position | None) -> Entry | Exit | None: ...
```

- `bars` holds every bar up to and including the one that just closed (UTC index, open/high/low/close/volume). The
  last row is the signal bar. Nothing after it: no look-ahead.
- Return `Entry(stop, target)` (buy at the next bar's open with that bracket), `Exit(reason)` (sell at the next bar's
  open) or `None` (do nothing). Same bars in, same answer out.
- The strategy never sends orders, sizes the trade or touches IB. The engine around it (the backtester now, the paper
  trader later) turns the intent into fills, so a strategy is written once.
- **Timing rule:** a decision is made at a bar's close and filled at the next bar's open. So "sell at the open of the
  15:55 bar" is decided on the close of the 15:50 bar.
- `check_bracket(position, bar)`: did this bar hit the stop or the target? A bar only shows its high and low, not
  which came first, so when it touches both, the stop is assumed (the worse case). A bar that gaps past a level fills
  at the open.
- The engine must re-check that the stop is still below the real fill price, because the fill is the next open, not
  the signal bar's close.

## Commands

| Command | What it does |
|---|---|
| `/clear` | Start a fresh conversation |
| Shift+Tab | Cycle the permission mode until the footer says **plan mode on** |
| `! code -g <file>` | Open a file in VS Code from inside Claude Code (shell mode) |
| `! uv run pytest` | Run every test in `tests/` |
