---
type: plan
status: proposed, nothing run yet
---
# Next experiments

A template for the note we saved in the lesson (`vault/Playbook/Next experiments.md`), with the three experiments Claude
proposed for **our** desk on Monday 2026-10-26. Your desk, your journal and your numbers will differ: keep the shape
(change, protocol, drop rule), and write your own before you run anything.

Rules for every experiment in this note:

- It is an **offline replay** on saved bars: no orders, no change to the plain desk, its `CLAUDE.md`, its skills or the
  forward test.
- The **drop rule is fixed before anyone looks at a result**. Write it down, commit it, then run.
- One change per experiment, and a new row in the experiment ledger if it ever becomes a trader version.

Terms: **R** is the money lost if a trade's stop is hit. The **stop distance** is the gap between the entry price and
the stop. A **replay** feeds saved bars to a design as if they were live. A **veto** is a role saying "no" to a proposed
buy. A **bar** is the open, high, low, close and volume of one 5-minute slice.

Why these three (our Monday): the lab's QQQ position and its stop order sat in every desk snapshot, so the regime gate
never gated and the ORB veto never asked Claude; the team's risk manager and devil's advocate were never asked, because
the analyst said "wait" on all 54 bars; and the open-window agent's one rule-met signal arrived about 16 to 21 minutes
late.

## 1. Test the two variants without the QQQ position

- **Change:** replay the regime gate and the ORB veto on the desk's saved snapshots (`data/desk/snapshots`), with the
  lab's QQQ position and stop order removed from each snapshot.
- **Protocol:** write the metrics down first: the share of bars the gate would skip, and how many signals the lab's
  strategy gives per day. Then run the replay and compare the gate's skipped bars with what the plain agent said on the
  same bars. The snapshots cover only a few days, so the sample size is the first limit.
- **Drop it if:** the gate skips fewer than 20% of bars, or skips any bar where the plain agent proposed something other
  than "wait"; for the ORB veto, the strategy signals on fewer than 1 day in 5, so there is nothing to veto.

## 2. Make the team convene

- **Change:** run the team on bars where the analyst does propose a buy.
- **Protocol:** replay with the real model on saved bars chosen because the lab's ORB strategy fired on them (from
  experiment 1); no orders. Record each role's vote, the count, and whether the trader agreed. For every bar, also
  compute what the buy would have returned in R, from the bars after it. Budget first: in our desk, a buy-proposal bar
  for the team cost about 19 times a single trader's bar.
- **Drop it if:** the vetoed buys did no worse in R than the approved ones, or the roles agreed with the analyst on nearly
  every bar (extra cost, no extra information). With fewer than about 20 buy-proposal bars, log it as "not testable yet"
  rather than "failed".

## 3. Measure the cost of delayed data

- **Change:** nothing in the desk. Measure how far price moves between a signal bar's close and when the desk could act,
  16 to 21 minutes later.
- **Protocol:** for each historical bar where the lab's ORB strategy signals, compute the price change from the signal
  close to the close 20 minutes later, as a fraction of the stop distance (comparable between days). Our Monday gave one
  data point: about 58% of a $0.77 stop distance. That is a single case, not a finding. Check what history the lab's
  cache holds before promising a sample size.
- **Drop it if:** the median move is under 10% of the stop distance (the delay isn't a real cost). With fewer than 30
  signals, report the numbers as anecdotes and stop.

Start with experiment 1: experiment 2 depends on its signal bars.
