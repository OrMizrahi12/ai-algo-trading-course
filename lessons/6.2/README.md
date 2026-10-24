# Student kit: Lesson 6.2, An event-driven engine

Module 6: The backtest engine · AI Algorithmic Trading with Claude Code and Interactive Brokers

The vectorized backtester from Lesson 6.1 was quick, and easy to fool. In this lesson you planned the real engine with
Claude Code in plan mode, read the plan, and let Claude build it: `backtests/engine.py`, an event-driven backtester that
walks the bars one at a time, shows the strategy only closed bars, fills entries at the next open, checks stops and
targets inside every bar (the stop wins a tie, and a gap through the stop fills at the open), charges commission, half
the spread and slippage, and sizes each trade from the stop distance. Sixteen tests check those rules. Then it ran the
`spy_vwap_reclaim` strategy over two years of SPY bars (−3.08% after costs, an honest negative result) and you traced one
winning and one losing trade, bar by bar.

## What's in this kit

| File | What it is |
|---|---|
| `prompts.md` | Every request typed in the lesson, the commands, and the pause-and-try exercise |
| `cheat-sheet.md` | The fill rules, costs and sizing, how the engine's loop works, the lesson's results and the two traced trades |
| `trading-lab/backtests/engine.py` | The event-driven engine: `run_backtest(bars, strategy)`, `CostModel`, the summary stats |
| `trading-lab/tests/test_engine.py` | The 16 offline tests (tiny hand-made bars and a scripted strategy, no data or IB needed) |
| `trading-lab/CLAUDE.md` | The project memory file, with the new rule: in this solo lab, always commit straight to `main` |

In the lesson Claude also added one line about the engine to the Lab's `AGENTS.md` (in its Layout section). The engine
uses files from earlier lessons, unchanged: `strategies/base.py` and `strategies/spy_vwap_reclaim.py` (Lesson 5.3),
`backtests/vectorized.py` (Lesson 6.1, for `load_bars` and the cost constants) and `indicators.py` (Lesson 5.2).

## Before you start

- The Trading Lab with the Strategy interface and `spy_vwap_reclaim` from **Lesson 5.3**, and the two years of SPY
  5-minute bars in `data/cache/` from **Lesson 6.1**.
- No IB connection is needed: the engine and its tests work offline, from the cache.

## Try it yourself

1. In your `trading-lab` folder, start `claude`, `/clear`, and press Shift+Tab until the footer says **plan mode on**.
2. Send the first request in `prompts.md`, read the plan, and approve it (auto mode is fine).
3. When it's done, read the summary: the rules, the costs, the results table, and anything Claude flags.
4. In the same session, send the trade-trace request and follow one winner and one loser, bar by bar.

You're done when your tests pass, `uv run -m backtests.engine` prints its results, and you can follow one trade from
signal to exit. Your numbers, wording and Claude's replies will differ from the video; the behaviour is what matters.

## Good to know

- The cost numbers (1¢ commission per share per side, a 1¢ spread with half paid on every fill, 1¢ slippage on
  market-type fills) are assumptions. Change them in `CostModel` if you have better ones.
- The engine sizes for 1% risk, but never holds more than 100% of equity (`max_position_pct=1.0`, no leverage). With a
  stop only cents below a $580 price, that cap usually decides the share count, so most trades risk about 0.1%. Leverage
  stays off in this course.
- The −5.2R trade on 2025-11-28 is a half day (the market closed at 13:00). The strategy only flattens at 15:55, so the
  engine's no-overnight rule sold at the next session's open. That's a gap in the strategy's spec, not in the engine.

## Safety

Paper trading only. Educational content, not financial advice. `spy_vwap_reclaim` is a teaching example and lost money
in this test: no result in this lesson is a promise, a recommendation, or a strategy to trade. The engine never touches
a broker and places no orders.
