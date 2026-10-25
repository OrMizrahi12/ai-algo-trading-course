# Lesson 7.5 cheat sheet: risk and position sizing

## Position size: how many shares a trade buys

The strategy decides **when** to buy. The sizer decides **how much**. The engine then applies the no-leverage cap to
whatever the sizer says: a position never costs more than the cash in the account.

| Sizer | Shares | Idea |
|---|---|---|
| Fixed fractional | equity × 1% ÷ (entry − stop + costs) | Hitting the stop costs about 1% of the account |
| Volatility (daily ATR) | equity × 1% ÷ daily ATR | A normal day's move costs 1%; the stop is ignored. Quiet stock: bigger position. Wild stock: smaller |
| Fractional Kelly | equity × (½ × Kelly, between 0.25% and 2%) ÷ (entry − stop + costs) | Kelly from closed trades only; plain 1% before 30 trades |
| No-leverage cap (on all three) | at most cash ÷ price | With a tight stop, the cap decides the size |

Worked examples ($100,000 account, 1% = $1,000 at risk; illustration numbers, not from the lab):

- Fixed fractional: stop $2 below the entry → $1,000 ÷ $2 = 500 shares.
- Volatility: a normal day's move (daily ATR) of $5 → $1,000 ÷ $5 = 200 shares.
- The cap: stop only $0.50 below a $500 stock → 1% would mean 2,000 shares = $1,000,000. The cap allows
  $100,000 ÷ $500 = 200 shares, so the real risk is only 200 × $0.50 = $100 (0.1%).

## The Kelly fraction

f = W − (1 − W) ÷ B, where W is the win rate and B is the average win divided by the average loss.

It answers: if I knew my win rate and my payoff exactly, what share of the account should I risk per trade to grow it
fastest over time?

- Example: W = 0.5, wins twice the losses (B = 2): f = 0.5 − 0.5 ÷ 2 = 25%.
- The lesson's breakout (all QQQ trades): W = 0.52, average win +0.88R, average loss −0.82R, so B ≈ 1.08 and
  f ≈ 7.9%. Half Kelly ≈ 4%, above the 2% cap.

Why it is always cut down and capped (Claude's three reasons):

1. **The inputs are estimates.** Win rate and payoff come from past trades and are noisy. Betting too much costs far
   more than betting too little, because oversized losses compound. Half Kelly gives up about a quarter of the growth
   and cuts the swings by about half.
2. **Past edges fade.** Kelly trusts the history completely; the future rarely matches it.
3. **A few lucky early trades can inflate the estimate.** The 2% cap stops a hot streak from producing a huge bet;
   the 0.25% floor keeps trading going so new evidence keeps coming in.

The multiplier (0.5), cap (2%) and floor (0.25%) are Claude's picks and are settings in `FractionalKelly`. Kelly is a
way to think about risk here, not a bet size to copy.

## Same trades, three sizers

QQQ opening range breakout, 15-minute range, 5-minute bars 2024-10-21 to 2026-10-21, $100,000 start, usual costs, no
leverage, long only, flat before the close. The same 354 entries and exits in every row.

| Sizer | Trades | Net profit | CAGR | Sharpe | Max drawdown | Profit factor | Win rate | Avg position | Avg risk if stopped | Worst trade |
|---|---|---|---|---|---|---|---|---|---|---|
| Fixed fractional | 354 | $15,263 | 7.4% | 1.00 | −7.5% | 1.19 | 52.3% | 98.9% | 0.5% | −1.0% |
| Volatility (daily ATR) | 354 | $12,695 | 6.2% | 1.31 | −4.5% | 1.27 | 52.3% | 65.5% | 0.3% | −0.6% |
| Fractional Kelly | 354 | $20,003 | 9.5% | 1.11 | −7.6% | 1.24 | 52.3% | 99.6% | 0.6% | −1.3% |

How often the no-leverage cap decided the size: 95% of fixed-fractional trades, 99% of Kelly's, 8% of volatility
sizing's.

Claude's reading:

- **The no-leverage cap decides most of the size.** The breakout's stop is the opening range's low, close to the entry,
  so a 1% risk would need more shares than the account can pay for. The table understates how different the sizers
  could be on a strategy with wider stops.
- **Not a clean win for Kelly.** It earned the most, but its worst trade was −1.30%, bigger than the 1% rule: a gap
  through the stop cost more than the stop distance, and the larger share count made that worse.
- **Volatility sizing earned less but was smoother**: the best Sharpe and the smallest drawdown, because it shrinks the
  position when the market is jumpy.
- **The edge is thin**: 52% wins, +0.88R / −0.82R.

## Correlation and account rules

- **Correlation** of daily results: +1 = they win and lose on the same days, 0 = unrelated, −1 = opposite. A flat day
  counts as 0. Diversification needs low correlation.
- **Daily loss limit**: no new entries for the rest of the session once the account is 2% below the previous close.
  Open positions keep their own stops (the limit does not close them).
- **Maximum trades per day**: at most 3 entries per session across all strategies.
- **One shared account, no leverage**: when several strategies signal on the same bar they are served in a fixed order
  (here ORB, Donchian, Bollinger: an arbitrary choice that favours ORB).

Correlation of daily results (502 sessions):

| | ORB QQQ | Donchian SPY | Bollinger QQQ |
|---|---|---|---|
| ORB QQQ | 1.00 | 0.56 | 0.15 |
| Donchian SPY | 0.56 | 1.00 | 0.11 |
| Bollinger QQQ | 0.15 | 0.11 | 1.00 |

ORB and Donchian are close to the same bet (both buy upward breakouts, and SPY and QQQ move together; 0.61 on days all
three traded). Bollinger buys dips and is the only real diversifier in the set.

## Each strategy alone vs. one combined account

5-minute bars, usual costs, 1% risk per trade, $100,000 (each strategy alone on its own $100,000; combined on one).

| Account | Trades | Net profit | CAGR | Sharpe | Sortino | Max drawdown | Profit factor | Win rate | Avg R | Exposure |
|---|---|---|---|---|---|---|---|---|---|---|
| ORB QQQ 15min (alone) | 354 | $15,263 | 7.4% | 1.00 | 1.66 | −7.5% | 1.19 | 52.3% | 0.04 | 43.1% |
| Donchian SPY (alone) | 541 | $4,759 | 2.4% | 0.33 | 0.74 | −6.1% | 1.07 | 39.9% | 0.01 | 41.6% |
| Bollinger QQQ (alone) | 728 | −$2,173 | −1.1% | −0.14 | −0.17 | −10.1% | 0.98 | 54.9% | 0.00 | 14.9% |
| Combined, no account rules | 1,075 | $11,720 | 5.7% | 0.54 | 0.83 | −9.7% | 1.07 | 49.0% | 0.01 | 66.4% |
| Combined, 2% limit + 3 trades/day | 959 | $13,877 | 6.7% | 0.64 | 1.07 | −8.7% | 1.08 | 48.3% | 0.01 | 63.5% |

What diversification did:

- Worst session: the combined account fell at most 4.8% in one day (3.0% with the rules); Bollinger alone fell 3.9%.
- The weak strategy was blended with two better ones, so the account still made money.

What it did not do:

- **No higher return.** Blending beats the average of the three, not the best one.
- **No stacking of positions.** The stops are tight, so each trade hits the no-leverage cap and uses about 100% to 110%
  of the account. Whichever signal fires first takes all the cash; the others are refused. Combined trades: 959 to
  1,075, against 1,623 if all ran alone.
- **Order matters**, and the order chosen favours ORB.

The two rules: the 2% loss limit fired in only 3 sessions (the worst day still reached −3.0%, because open positions
keep their stops); 3 trades a day did most of the work (241 entries refused). The ruled account made $2.2k more than the
unruled one, which with 3 limit days is probably path luck, not proof that the rules help.

Caveats: two years of data; the ORB result carries the whole combination; each strategy alone sizes against its own
$100k while the combined account shares one pool; leverage or a smaller risk per trade would let the strategies hold
positions together, which is the test that would show real diversification, and it was not run.

## Key terms

- **Position size**: how many shares a trade buys.
- **Fixed fractional**: size so that hitting the stop loses a fixed share of the account (here 1%).
- **Volatility sizing**: size by how much the instrument normally moves (the daily ATR), so quiet and wild days risk the same.
- **Kelly fraction**: the bet size that maximizes long-run growth if your win rate and payoff are known exactly.
- **Correlation**: how much two strategies' daily results move together (+1 together, 0 unrelated, −1 opposite).
- **Daily loss limit**: stop opening new trades for the day after losing a set amount.
