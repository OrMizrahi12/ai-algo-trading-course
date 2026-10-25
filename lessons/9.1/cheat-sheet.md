# Lesson 9.1 cheat sheet: Claude as a quant researcher

## The words

| Word | Meaning |
|---|---|
| **Hypothesis** | A testable claim about the market with a reason it might work ("the last half hour continues the day's move, because option and leveraged-ETF hedgers trade in that direction near the close") |
| **Edge** | A reason a strategy should keep working after costs. Without one, a good backtest is probably luck |
| **Research journal** | The running record of every idea: why it might work, its source, how to test it, its scores, its status and result |
| **Strategy card** | A one-page summary of one tested idea: rules, settings and where they came from, the full scorecard, the verdict and the next step. Failed ideas get a card too |
| **Research loop** | Hypothesis, spec, code with tests, the judge, the strategy card |
| **Fishing** | Trying more settings on the same data until something passes. Every try is another trial, and the winner is mostly luck |
| **ATR** | Average true range: the average size of one bar (here a 5-minute bar) |
| **Proxy** | A measurable stand-in for an idea (here "5 ATR from today's open" for "a trend day") |

## Where ideas come from

1. **Published research**: papers that measured a pattern over many years (journals, SSRN working papers).
2. **Practitioner work**: books, blogs and well-known setups.
3. **Market structure**: the open, the close, scheduled events such as Federal Reserve meetings.
4. **Your own hypotheses**: from what your own lab already measured.

## The journal Claude wrote (score = promise x cheap, 1-5 each)

| Rank | Idea | Score |
|---|---|---|
| 1 | H1 (own): skip the two reversion strategies on likely trend days | 20 |
| 2 | H2 (own): replace the breakout's 1R target with a time-based exit | 15 |
| 3 | H3 (own): run ORB 15 min / 1R on older years it has never seen | 12 |
| 3 | Last-half-hour momentum (Gao et al. 2018; Baltussen et al. 2021) | 12 |
| 3 | Noise-area intraday momentum on SPY (Zarattini, Aziz, Barbon) | 12 |
| 3 | Small-gap fade | 12 |
| 7 | Overnight vs. intraday return split (Lou, Polk, Skouras) | 10 |
| 8 | Long-above-VWAP trend on QQQ (Zarattini, Aziz) | 8 |
| 8 | Same-time-of-day continuation (Heston et al.) | 8 |
| 10 | Pre-FOMC drift (Lucca, Moench) | 4 |
| 10 | ORB on "stocks in play" | 4 |

A high score means "test this first", not "this will work". The last two score low because the Lab lacks the data.

Caveats Claude wrote down: rows marked * rest only on search summaries, not on the papers; replications of the
Concretum-group papers (noise area, VWAP, ORB) report much weaker results, so treat paper numbers as upper bounds; the
papers trade long and short, while the Lab's engine is long-only.

## H1 through the loop

- **Idea**: the two reversion strategies lose on trend days (profit factor 0.43-0.68) and win on other days
  (1.18-1.71), but that label used hindsight. Can a rule known at the time of the trade capture it?
- **Filter**: no new entry when `abs(signal close - today's first open) / ATR(14) > 5.0`. Exits are never blocked; off
  by default (`max_open_distance_atr`).
- **Design catch**: a 14-day average range was the first idea, but the engine shows a strategy only the last 200 bars
  (about 2.5 sessions), so it would have blocked every trade.
- **Threshold**: 5 ATR, fixed before any run from the entries' distances alone (the two-thirds mark was 4.7-5.6 ATR).
- **Judge**: 8 runs (baseline and filtered, 2 strategies, SPY and QQQ), `--trials 8`.

| Strategy | Symbol | Run | Trades | Sharpe | Rules passed |
|---|---|---|---|---|---|
| bollinger_rsi_reversion | QQQ | baseline | 728 | -0.14 | 4 of 8 |
| bollinger_rsi_reversion | QQQ | filtered | 473 | -0.05 | 3 of 8 |
| bollinger_rsi_reversion | SPY | baseline | 738 | -0.57 | 2 of 8 |
| bollinger_rsi_reversion | SPY | filtered | 512 | -0.68 | 2 of 8 |
| vwap_stretch_reversion | QQQ | baseline | 653 | -1.20 | 1 of 8 |
| vwap_stretch_reversion | QQQ | filtered | 424 | -1.30 | 1 of 8 |
| vwap_stretch_reversion | SPY | baseline | 699 | -1.21 | 1 of 8 |
| vwap_stretch_reversion | SPY | filtered | 488 | -1.53 | 1 of 8 |

**Verdict: FAIL.** A finished experiment, not a strategy to trade.

- Costs are the problem: all four unfiltered runs already lose money after costs (break-even 0.0x to 0.8x of usual costs).
- The filter removes 30-35% of trades; the loss shrinks in all four pairs, the Sharpe improves in only one, walk-forward
  gets worse in all four. The removed trades were slightly profitable before costs.
- Deflated Sharpe under 24% everywhere.
- The test shows this proxy doesn't capture the trend-day effect; it doesn't show the effect is absent.
- **Next step**: stop H1 (other thresholds on the same two years would be fishing); next in the journal is H2.

## The loop, in one line

Write the hypothesis and its reason; write the spec and fix the settings before any run; build it with tests; run the
judge with the true trial count; write the card, pass or fail; update the journal; commit.
