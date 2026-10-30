# Lesson 15.3 cheat sheet: the stock-open agent

## Words

| Word | Meaning |
|---|---|
| Watchlist handoff | The scanner's ranked list, given to Claude as its input |
| Trading window | The time span when new entries are allowed |
| Halt | An exchange pause in a single stock's trading |
| Gap | Today's open compared with yesterday's close |
| Relative volume | Today's volume so far, compared with a normal day at the same time |
| Bar | The open, high, low, close and volume of one 5-minute slice |
| Stop | A resting order that sells at the loss limit |
| Dry run | The loop asks the model and runs the gates, but sends no orders |
| R | The risk of one trade: entry minus stop. About -1R means the stop was hit |

## The morning, in order

| Time (UTC) | What happened on our paper day (2026-10-26) |
|---|---|
| 12:03 | First scan: 0 measured, 0 passed (IB error 492; no bars before the 13:30 open). No picks |
| 12:15 | Our decisions: dry run only, limits file untouched, window widened, client 10 in the lab's docs |
| 12:39 | The loop starts (dry run, client ID 10) and re-reads the note every minute |
| 13:30 | The US open (09:30 New York) |
| 13:50 | We ask for the rerun; two scanner runs stop at Claude's own time limits |
| 13:55-14:00 | The RRC bar that met the buy rule (closed at $53.17) |
| 14:08-14:13 | The background scan finishes (the note says about 14:08; Claude was told at 14:13): 49 names pass the lab's filters |
| about 14:16 | The picks are in the note; that RRC bar reaches the loop, about 16 minutes late, with RRC near $52.70 |
| 14:25 | The journal shows the finding: the model waited because RRC had no limits entry |
| 14:28-14:29 | The fix is committed; the loop restarts |
| 15:00 / 15:30 | Last bar that may open a trade starts before 15:00; everything flat and the loop disconnects at 15:30 |

The window follows the New York open: when New York changes its clocks (2 November 2026), the UTC times move by an hour.

## The open-window loop

- Its own module (`desk/openwindow.py`), its own instructions (`.claude/open-window/constitution.md`), client ID 10, order
  tag `live:open:<SYMBOL>`, journal in `data/open/`. The SPY desk's `CLAUDE.md`, plugin and skills are untouched, so its
  instruction hash stays the same.
- Each name reuses the desk's heartbeat, so the safety layers carry over: settled bars only, the STOP file, the limits pin,
  the lab's risk layer, and the review gate.
- Picks live in today's note, at most two blocks, each with `Buy if:`, `Stop:` and `Give up:`. A block without all three
  is ignored; more than two is refused.
- Dry run is the default. In dry run the lab's risk check still runs, so an unlisted name is journaled as
  `refused_by_risk_limits`.
- `uv run -m desk.openwindow` (add `--once` for a single pass).

## Our two picks (scanner output on that day: an example, never a tip)

| Name | What the scanner showed | Buy if | Stop | Give up |
|---|---|---|---|---|
| RRC | Gap +11.2% (4.2 ATR), relative volume 43.8x, about $53 | A finished bar closes above $53.08 on at least 300,000 shares, not more than $1 above | $52.40 | A close below $51.90 before buying |
| HHH | Gap +4.1% (1.2 ATR), relative volume 6.7x, about $73, faded from $74.90 | A bar closes above $74.90 on more volume than the bar before | $73.00 | A close below $72.68 |

Headlines: IB listed three news providers, but every headline request timed out, so the picks rest on price and volume only.

## The bug the journal found

| What we wanted | What happened |
|---|---|
| The model judges the plan; the desk enforces the limits and journals a refusal | The model saw RRC had no limits entry and answered `wait` itself, so the desk's check never ran and no refusal was journaled |

The fix (one paragraph of the agent's instructions): judge the plan only; a missing limits entry is not a reason to wait; if
the buy condition is met, answer `buy` and let the desk refuse. A running loop keeps its old instructions until it restarts,
and bars it already decided are not decided again.

## The result (dry run, nothing sent)

| | RRC | HHH |
|---|---|---|
| Decisions | 14, all wait | 14, all wait |
| Buy rule met | Once: the 09:55 New York bar closed at $53.17 on 417,000 shares | Never: best close after the plan $73.84 |
| Decided after the bar closed | 16 to 21 minutes | 16 to 21 minutes |

Model calls: $1.89 in all, at list prices (usage on a subscription, not a bill).

**Not a result:** a buy at $53.17 would have had its $52.40 stop touched on the 10:55 bar, about -1R. But that fill was not
reachable: when the bar's data arrived, RRC was near $52.70.

## What the open taught us, on delayed data

1. The signal can come before the plan. Write plans early enough, or accept that the first move is gone.
2. The price moves before you can act. A rule judged on a 16-minute-old close needs a check of where the price is now.
3. Check a pick against the limits file when you pick it, so a name that cannot be bought is not picked.
4. Scans take time and can be refused. Budget the scan, and plan for an empty result.
5. Single stocks need more care than an ETF like SPY: a stock can be halted, and spreads are wider.

Paper account only. Educational content, not financial advice; nothing here is a promise of profit or a recommendation.
