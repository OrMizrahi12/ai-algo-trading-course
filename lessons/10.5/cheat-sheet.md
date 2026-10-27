# Lesson 10.5 cheat sheet: One codebase for backtest and live

## The words

| Word | Meaning |
|---|---|
| **Platform** (framework) | Someone else's engine that you plug your strategy into. Here: NautilusTrader |
| **Adapter** | The piece that connects a platform to a broker or a data source. Here: Nautilus' Interactive Brokers adapter |
| **Fill model** | The rules a backtester uses to decide when, and at what price, an order fills |
| **Parity** | The same strategy giving the same trades in two engines (or in a backtest and live) |

## Our engine or a platform

| | Our engine (the Lab) | A platform like NautilusTrader |
|---|---|---|
| Backtest and live | Two code paths, kept honest by a parity test | One strategy class for both |
| Fills | Next bar's open, our cost model | Its own matching and fill models (a market order from `on_bar` fills at that bar's close) |
| Venues | Interactive Brokers, stocks | Many adapters: brokers, exchanges, data providers |
| Speed | Plenty for 5-minute bars | Rust core, built for tick data |
| Cost | Ours to maintain, small enough to read | A big framework to learn, docs that move fast, its assumptions inside your results |

## What the comparison showed (our computer, research period 2024-10-21 to 2026-04-21)

Same bars (29,070, a copy of the cache; the holdout never read), same costs, $100,000 start, 1% risk, no leverage.

| | Lab engine | Nautilus, fills at next open | Nautilus, native fills (signal bar's close) |
|---|---|---|---|
| Trades (target / stop / time) | 263 (111/79/73) | 263 (111/79/73) | 263 (111/79/73) |
| Net profit | $20,692.14 | $20,694.29 | $20,698.75 |
| Sharpe | 2.0417 | 2.0419 | 2.0435 |
| Max drawdown | -5.16% | -5.16% | -5.17% |
| Win rate | 61.22% | 61.22% | 60.84% |
| Costs paid | $2,432.95 | $2,434.00 | $2,433.65 |

These are years the strategy was already tested on. The table checks the engines against each other; it is **not** new
evidence for the strategy (on the unseen years it failed: H3 in the research journal, Sharpe 0.03, as Claude's verdict notes).

## Every difference, explained

1. **Fill timing.** Nautilus has no "fill at the next bar's open" mode. With native fills, none of the 263 entries is on the
   same bar as ours, and single trades differ by up to about $20; the totals nearly cancel, which you can't count on.
   To match our engine, Claude feeds each bar's open as a one-tick trade just after the previous bar closes and sends the
   order from that tick (`--timing next_open`). That is a workaround, not a Nautilus feature.
2. **Costs.** Nautilus fills at the raw price, so our per-share costs are charged as commission (`OrbFee`). It rounds each
   commission to whole cents: +-$0.01 on 128 trades.
3. **One share.** On 2026-04-06 the share count was 204 against 203: the cash differed by $1.06, and
   `floor(cash / price)` landed on opposite sides of a whole number (204.0016 vs 203.9998). That is almost all of the $2.15
   profit gap.
4. **Stop and target in the same bar.** Ours assumes the stop (the worse case). Nautilus walks open, high, low, close, so the
   target would win. None of these 263 trades had such a bar; another strategy could.
5. **Stop gaps.** A bar that opens past the stop fills at the open in both.
6. **Cash below zero.** With the position at all of the cash, costs push the balance a few dollars negative and Nautilus
   halts the backtest with `AccountBalanceNegative` (76 trades). It logs an error and returns normally, so always check the
   trade count. `allow_cash_borrowing=True` matches our engine.
7. **Docs versus the installed version.** The "latest" docs online describe a layout that doesn't exist in 1.231.0 (for
   example a `MakerTakerFeeModel` import). Read the installed source when they disagree.

## The live adapter, on free delayed data (2026-10-22, market closed)

| Step | Result |
|---|---|
| Paper check | One account, starting with `DU`: paper |
| Instrument | `QQQ.NASDAQ` loaded (tick 0.01; the "lot 100" in the log is the adapter's default) |
| Data type | Delayed-frozen (15-minute-old prices; the last value when the market is closed) |
| Recent 5-minute bars | Failed: IB error 2188, "Up-to-the-second historical data requires additional subscription for the API", then a 60 s timeout with 0 bars |
| Subscribe to new bars | Failed the same way |

Tested and ruled out: ending the request at the last session close instead of "now", and leaving out the live
subscription. The adapter cancels a request on any IB code except 200; our own downloader treats 2100-2199 codes as
transient and retries. The cause of the 2188 stayed unknown (it would need a trace of the network traffic). On free data,
the adapter loads the instrument and checks the account, but can't pull or stream bars. Our own engine's poll for finished
bars works on the same account.

## When to graduate

Our own engine is enough while you trade one strategy per symbol on 5-minute bars through IB. Move to a platform when:

- a strategy has survived the judge and needs money-grade operation;
- it needs finer data than bars (ticks, quotes, an order book) with realistic simulated fills;
- it runs across many symbols, venues or asset types;
- speed matters;
- the order-state, reconnect and reconciliation code you maintain grows bigger than a one-person lab.

Before any strategy has an edge, graduating only adds complexity.

## The files (`nautilus_lab/` in this kit)

| File | What it does |
|---|---|
| `pyproject.toml` | The separate environment: `nautilus-trader[ib]`, pandas, pyarrow, exchange-calendars |
| `nautilus_orb.py` | The ORB port. `--timing next_open` (default) or `--timing bar_close`, `--adaptive` for adaptive bar ordering |
| `run_lab_engine.py` | Runs our own engine on the same copied bars (run it from the Lab with `uv run`) |
| `compare.py` | Pairs the trades and computes the metrics with the Lab's own `compute_metrics` (run it from the Lab with `uv run`) |
| `live_observe.py` | Observe-only ORB on the IB paper Gateway: a data client only, `submit_order` overridden to raise, host and port 4002 asserted, every account must start with `DU`. As left at the end of the lesson: history request only |

Paths point at `~/nautilus_lab` and `~/trading-lab`; change them if your folders live elsewhere. Copy the bars yourself
(the kit has no market data): a copy of your cache from your start date, never the holdout.
