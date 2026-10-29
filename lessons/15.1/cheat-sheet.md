# Lesson 15.1 cheat sheet: the multi-agent desk

## Words

| Word | Meaning |
|---|---|
| Subagent | A separate Claude worker with its own instructions and its own context |
| Role | One job on the team, written as a short instruction file in `.claude/agents/` |
| Veto | A role that can block a trade. On our desk only the risk manager can veto |
| Decision record | The written trail of who said what: every view, the count, the trader's answer, the final decision and why |
| Bar | The open, high, low, close and volume of one 5-minute slice |
| Dry run | The desk asks the model and checks the answer, but sends no orders |
| Replay | Saved bars sent through the real model again, with no broker and no orders, to measure time and cost |

## The team

| Role | Asked | Answers |
|---|---|---|
| Analyst | First, on every bar | `buy` / `sell` / `close` / `wait`, with a one-sentence thesis (a buy also gets a stop, a target and a size in R) |
| Risk manager | Only after a proposed buy | `approve` / `abstain` / `veto`, checked against the hard rules (stop, target, size, nothing held, time of day, fresh data, entries per day, losses today) |
| Devil's advocate | Only after a proposed buy, together with the risk manager | `approve` / `abstain` / `object`, with the strongest case against the trade |
| Trader | Always, last | Sees the views and the count, and makes the final call as always |

## The rule for disagreement (written down before it happens)

- A buy goes through only if the team backs it. Otherwise the desk turns it into `wait`.
- The analyst's proposal counts as one yes. A buy needs **at least two yes and more yes than no**.
- **A veto or a tie means wait.** So does a missing, late or invalid view.
- Sells and closes are never blocked: exits are always allowed.
- The order and the count run in code (`desk/team.py`), not in the model's good behaviour.
- Every bar record in the journal gets a `team` block: each view, the count, the trader's answer, the final decision,
  `overridden` (why a buy became a wait) and the team's cost.
- `uv run -m desk --team` turns it on. Without `--team` nothing changes.

## Why separate calls, not subagents

| Problem | What the probe showed |
|---|---|
| They run in the background | The answer went out before the subagent had finished (a setting can make it wait) |
| They can't see the data | A subagent only gets the tools its parent has; our trader has only its skills, so the helper refused to start |

So each role is its own `claude -p` call with no tools, no memory and the bar's full snapshot.

## What the team costs (replay of 6 saved SPY bars, no orders)

Usage figures at list prices, not a bill on a subscription. `uv run -m desk.team_cost`, report in `experiments/team-cost.md`.

| Run | $ per bar | Seconds per bar |
|---|---|---|
| Single trader | 0.015 | 4.4 |
| Team, quiet bar (the analyst says wait) | 0.148 (9.6x) | 8.4 |
| Team, full path (a made-up buy, all three asked) | 0.299 (19.4x) | 17.0 |

- Why so much: the trader sends only what changed each bar, but every role re-reads the whole snapshot.
- Caveat: the full path rests on two bars, and its buy was made up, so it says nothing about what the trader would
  really do.

## One live day, side by side (54 bars, 14:10 to 18:35 UTC)

| | Live single trader | Team |
|---|---|---|
| Agreed | | 54 of 54 (all wait) |
| Analyst proposals | | wait on all 54, 0 failed views |
| Seconds per bar (mean / max) | 8.5 / 15.1 | 10.6 / 18.2 |
| Cost per bar | $0.090 | $0.312 |
| Total cost | $4.85 | $16.83 |

- No bar where they differed: both cited the down trend, and both noted the QQQ position wasn't theirs.
- The analyst added about 6 seconds a bar, but the trader inside the team was faster, so the total was only about 2
  seconds more. Both are far inside the 120-second budget.
- The roles were most of the cost ($14.30 of the team's total, the trader $2.53): about 3.5 times the desk.
- One real difference: the team's trader loaded the market-read skill on 1 of 54 bars; the live desk on all 54, as
  `CLAUDE.md` asks. It didn't matter on a day of waits, but it would matter live.

## What one quiet day can and can't say

| Can say | Can't say |
|---|---|
| The team runs reliably: no failed views, no timeouts | Whether a veto, a majority or an objection improves anything: no buy was proposed, so those parts never ran |
| Its cost and time per quiet bar | Much from 54 of 54 agreement: both designs default to wait on a down-trend day |
| It doesn't cause bad behaviour on a no-trade day | That the trader is independent: it sees the analyst's view first |
| | Who was right: a wait has no outcome |
| | Anything beyond one day, one regime, one session each |

Next evidence: replayed bars where the analyst does propose a buy.

## Safe defaults

- Write the rule before the disagreement.
- A tie or a veto means wait; exits are never blocked.
- Measure the cost per bar on replayed bars before anything runs live.
- Watch a new design as a dry run next to the desk, with its own client ID and journal, and leave the desk alone.
- Don't trust a quiet day.

Paper account only. Educational content, not financial advice; nothing here is a promise of profit or a recommendation.
