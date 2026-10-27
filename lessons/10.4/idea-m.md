# Idea M in the research journal (Lab commit dc7c900)

The row Claude added to `research/journal.md` after the drift check. `CostModel` itself was not changed: H3 was
pre-registered with the default costs and had not run yet.

**#:** M

**Idea:** **IB's $1 minimum commission per order (own finding from the trade journal)**. The engine's `CostModel` charges 1 cent per share per side; IB charged at least $1.00 per order on every real paper fill. Put a per-order minimum (and the sell-side fee) into the cost model as an option and see what it does to the strategies at the position sizes we can actually trade.

**Why it might work:** The journal (`entry_pnl`, 2026-10-22) shows 1-share round trips paying $2.0157 (model: $0.02, about 100x) and the 10-share manual round trip paying $2.157 (model: $0.20, about 11x). Buys paid $1.00003 and $1.00 for 1 and 10 shares, i.e. the $1 minimum, not a per-share rate; sells paid about 2.06e-5 of the sale value on top (a sell-side regulatory fee, my reading). The risk limits cap a position near $8,000 (about 10 shares of SPY or QQQ), so live the minimum always binds and the model UNDERSTATES cost. The backtest sizes 1% risk of $100,000 over a stop a few dollars away, probably hundreds of shares, where the minimum may not bind and the 1-cent model may OVERSTATE cost (IB's per-share rate above the minimum is not observed in our fills; check IB's fee schedule, 0.5 cent is only the usual figure). So the backtest and the live engine sit in different cost regimes, and every Sharpe so far was measured in the first.

**Source:** Own: `live/journal.py` `entry_pnl` view, drift check of 2026-10-22 (SPY proof and kill-switch fills).

**How we would test it:** **Not before H3 has run and its card is written** (H3 is pre-registered with the default `CostModel`, which must not change until then). Then: (1) add optional `commission_min_per_order` and `sell_fee_pct` to `CostModel`, default 0 so every existing result reproduces exactly (test that); the engine charges per order, `max(shares x rate, minimum)`. (2) Measure the shares per trade of ORB QQQ 15 min / 1R, Donchian and the reversion pair in the existing backtests (do not assume). (3) Re-run each at two sizes: the backtest's own ($100,000, 1% risk) and the live-limit size (`max_position_pct` about 0.08), with the minimum on and off; report net, Sharpe and cost as a share of the average winning trade. (4) Find the position size above which the minimum stops mattering. Backtests only: no scorecard run and no new strategy, so nothing counts as a trial. Changing the judge's cost assumptions (`judge/`, locked) is the user's decision, not part of this idea.

**Promise:** 4

**Cheap:** 5

**Score:** **20**

**Status:** queued: after H3 (cost-model change, not a strategy; the batch skips it and it has no line in `families.txt`)

From the suggested order:

6. **M** (minimum commission): only after H3 has run, because it changes the cost model H3 is frozen with; it decides whether the live position cap is big enough for any strategy to pay its fees.
