# Lesson 9.6 cheat sheet: Don't stop until it passes

## Words

| Word | Meaning |
|---|---|
| The bar | A pass rule a machine can check. Here: on the sealed holdout alone, after 0.10% round-trip costs, at least 150 trades and a profit factor of at least 1.4 |
| Profit factor | What the winning trades made, divided by what the losing trades lost. 1.4 means $1.40 won for every $1 lost |
| Sealed holdout | Data kept away from research, opened once, by a judge, for frozen candidates |
| Pre-registered protocol | The rules of the search (the bar, the windows, the costs, the candidate limit, where the next holdout comes from), written and committed before any result |
| Frozen candidate | A strategy whose rules and settings are fixed in a file before the holdout is opened, so nothing can be tuned after |
| Trial ledger | Every configuration ever tried, counted. The more tries, the likelier a lucky pass |
| False pass | A strategy with no edge that clears the bar by luck |
| Luck number | How often a strategy with no edge, and as many trades shaped like this one, would still reach the bar's profit factor |
| Buy-and-hold | Simply holding the same ETFs over the same years: the baseline every pass is read against |
| Drawdown | A fall from a peak in account value |

## The windows in the video

| Window | Years | Used for |
|---|---|---|
| Train | 2000 to 2012 | Building ideas |
| Validation | 2013 to 2018 | Checking them |
| H1 (sealed) | 2019-01-01 to 2026-10-29 | One opening, for at most six frozen candidates |
| H2 | Non-US country ETFs, same years | The next holdout, if needed |
| H3 | Future bars | The only holdout nobody can have seen |

## The false-pass odds (Claude's simulation on coin-flip trades)

| Setup | Chance a zero-edge strategy passes |
|---|---|
| 1 candidate, 150 trades | about 5 to 9% |
| 6 candidates, 150 trades | about 27 to 43% (at least one) |
| 6 candidates, 300 trades | about 6 to 16% (at least one) |

The bar also does not subtract drift: in a rising market a long-only rule can look good just by being invested. That is
why buy-and-hold sits next to every result.

## Two locks on one door

- `/goal <condition>`: Claude keeps working until a small model agrees the condition is met.
- A Stop hook gate: the hook runs your own code; with the goal's name in the gate's active file, Claude cannot stop until
  the holdout log shows a pass. You turn the gate on yourself (shell mode, a commit).

## Your part, not Claude's

- Decide the bar, and don't move it after seeing numbers.
- Read the judge patch and apply it yourself (the judge folder is locked, even for Claude).
- Turn the gate on.
- Read every pass next to buy-and-hold and the luck numbers.

## How to read a pass

1. Did it pass the bar on data it never saw, after costs? Then it is a research result, not proof.
2. Put it next to buy-and-hold of the same assets over the same years: return, Sharpe and drawdown.
3. Check the luck number, and remember trades in related assets land on the same days.
4. Look at the years: a pass can rest on a few good years.
5. Ask what the researcher could have known about the holdout period. If the answer is "roughly what happened", the only
   clean test is future bars.

## The numbers in the video

- Setup: about 1 hour 47 minutes; then 17 more minutes for our answers.
- Data: 36 US stock ETFs (IYZ swapped for IJR on the liquidity floor), 153,884 research rows, a sealed holdout of 70,848
  rows.
- The goal: 30 minutes, one turn. 191 research runs, 153 distinct configurations, 33 holding up on validation, five frozen
  candidates (one per distinct idea), one opening.
- Four of five passed: time-series momentum (439 trades, profit factor 3.43), Halloween (288, 3.52), low volatility
  (422, 4.12), pre-holiday (2,268, 1.65). The dip rule failed (1.25).
- Buy-and-hold made 15.5% a year (2019 to 2026, max drawdown -39%); the passes made 4.7% to 10.8% (max drawdowns -15% to
  -39%). Only low volatility beat buy-and-hold on Sharpe (0.87 against 0.80).
- Every rule that passed had losing years.
- A second opening of H1: refused, nothing opened.
