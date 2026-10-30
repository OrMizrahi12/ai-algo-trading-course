# Lesson 15.2 cheat sheet: variants and hybrids

## Words

| Word | Meaning |
|---|---|
| Pure agent | Our desk's foundation: Claude sees every bar and decides, even when the answer is wait |
| Regime filter | A rule that labels the market state, like trending or ranging |
| Veto design | Code proposes, and the model can only refuse |
| Hybrid | Code and model share the decision |
| ATR | Average true range: the typical size of a bar (here over 14 five-minute bars) |
| Opening range breakout (ORB) | Buy when a 5-minute bar closes above the high of the first 5 minutes after the open |
| Settled bar | A bar that ended long enough ago (16 minutes, on delayed paper data) that it will not change any more |
| Dry run | The desk asks the model and checks the answer, but sends no orders |

## Three designs

| Design | Who decides when to ask the model | Who decides the trade | Switch |
|---|---|---|---|
| Pure agent (the foundation) | Every bar, always | Claude | none (the default) |
| Regime gate | A fixed rule in code (plus every safety case) | Claude, once awake | `--regime-gate` |
| ORB veto | The lab's strategy, when it signals | The strategy proposes; Claude may only approve or veto | `--orb-veto` |

The variants are optional, off by default, and `--orb-veto` cannot be combined with `--team` or `--regime-gate`.

## The regime gate

- **The rule** (lab research card H1, fixed in advance, never tuned):
  `distance = |last close - today's first open| / ATR(14)`; **trending when distance > 5.0**, ranging otherwise.
- **Why this number.** No regime threshold could be known live where we first pointed: the lab's day-type labels use
  hindsight. H1's rule is the only live-knowable one. The lab's verdict on H1 was FAIL as a filter for its reversion
  strategies, and here it only decides when to spend a model call, which the lab never tested.
- **The wake rule** we chose: trending bars only, plus always when a long is held, an order is open or a fill appeared,
  on the first bar after a start, and in the last 30 minutes before the close.
- **Skipped bars** are journaled as a desk `wait` with `model_asked: false` and a `regime_gate` field; the next call's
  update carries them. Once awake, Claude decides everything, and the risk gates and the flatten seatbelt run as before.
- **The ledger.** Same instructions hash as Trader v2.2 (CLAUDE.md and the skills are unchanged), so compare by the row
  "Trader v2.2 + regime gate" and the journal fields, not by hash.

**Replay** (`uv run -m desk.regime_replay --trace`, 79 saved snapshots, before the unfinished-bar fix):

| | |
|---|---|
| Woken | 10 bars, all safety cases (6 in the exit window, 4 on the first bar or after a fill); the regime woke none |
| Skipped | 69 bars (87%); 66 of the 75 bars while the market was open |
| What the skipped bars cost | $1.11 of the $1.42 spent, and 396 s of bar time (the journal's real figures, list prices) |
| Missed actions | none: the real trader waited on every skipped bar |
| Caveat | not one trending bar in about two days (largest distance 3.95 ATR): the savings come from sleeping through quiet days, not from the filter finding anything; about 1.3 sessions, no real trade |

## The ORB veto

- **Signal**: the lab's `OpeningRangeBreakout` with default settings, imported unchanged. Buys when a 5-minute bar
  closes above the high of the first 5 minutes after the open. Stop = the range low, no target, at most one signal a day.
- **Claude** is asked only when there is a signal and nothing is held. It gets the full snapshot plus the signal and can
  only answer approve or veto, with a reason. It can't change the size (fixed at 0.5 R by the desk), the stop or the
  target; an answer with extra keys is invalid.
- **A veto, or a missing, late or invalid answer, becomes a wait.** Every desk gate still applies after an approval.
- **While a position or order is open** Claude is not asked: the stop and the pre-close flatten manage it.
- **The ledger row** hashes only `.claude/orb/veto.md` (the text Claude is given), so it is not comparable with the
  other rows by hash.

**Replay** (`uv run -m desk.orb_replay --ask`, 79 saved snapshots, before the unfinished-bar fix):

| | |
|---|---|
| As the desk saw the bars | 0 signals |
| On the newest version of each bar | 1 signal: 2026-10-23, 09:55 New York, close 760.94 above the range high 760.73, stop 759.72 ($1.22 a share). Claude approved: the data was 13 minutes old (under the 30-minute limit), the stop about $1.22 below entry, no trades or losses that day, the close above the range high and VWAP |
| Caveat | the desk's own snapshot of that bar showed a close of 760.54, below the range high: live, no signal. One signal says nothing about how often Claude would veto |
| Finding | 61 of the 178 saved bars closed at a different price in a later snapshot |

## Unfinished bars (the finding that mattered most)

| | |
|---|---|
| Why the bars changed | Paper market data is about 15 minutes delayed, so IB returns only bars that started at least 15 minutes ago, and the newest is still being filled: its close, high, low and volume change on the next poll. The lab's feed called a bar closed as soon as the wall clock said 5 minutes were over |
| Measured on 79 snapshots | the newest bar differed from its final version in 63; the second newest never did. 12 minutes after its close the newest bar held a median of 21% of its final volume (0.69 at 13 minutes, 0.88 at 14, complete from about 15) |
| The fix | `snapshot.settled_bars` drops every bar whose end is less than 16 minutes old (15 delay + 1 margin), in the heartbeat and the MCP trade path. A bar is now decided 16 to 21 minutes after its close instead of 10 to 15, still inside the 30-minute stale limit. The flatten seatbelt still gets the newest known price |
| Tests | `tests/test_settled.py`: a fake feed that behaves like delayed IB. With the fix every bar the desk decides on equals its final version; with the settle step off, the same run decides on a partial bar |
| What it invalidates | every decision before the fix (all earlier ledger rows and the comparisons built on them); both replays above; the approved ORB signal appeared only on a later version of the bar. The lab's own live engine has the same flaw (left alone: the lab is read-only). The MCP tool `get_bars` still returns raw bars |

Check your own desk for this before you compare anything.

## One live day, three designs (2026-10-26, paper, dry runs)

The variants ran beside the live plain desk with their own client IDs (41 and 42) and journals, from the 14:35 UTC bar
to the close. All designs shared one paper account, which also held the lab's 10 QQQ shares.

| On the 62 bars all three recorded (14:35 to 19:40 UTC) | Pure agent (live desk) | Regime gate | ORB veto |
|---|---|---|---|
| Decisions | 62 wait | 62 wait | 62 wait |
| Model called | 62 of 62 (by design) | 62 of 62: woke for a safety case on every bar ("holding a long" on 60, "open orders" on 2) | 0 of 62: returned wait because a position or order was open |
| Reasons | daily trend down, QQQ not ours (all 62) | daily trend not up, chop; QQQ mentioned on 5 | one fixed line: a position or order is open |
| Cost (list prices) | $6.26 ($0.101 a bar) | $5.52 ($0.089 a bar) | $0.00 |
| Input tokens per bar | about 175k | about 135k | none recorded |
| Seconds per bar (mean / max) | 8.6 / 15.3 | 6.1 / 11.8 | 0.07 / 0.7 |
| Skills loaded | market-read on 62 | market-read on 62 | none |

The gate labelled 47 bars trending and 15 ranging. Without the QQQ position it would have skipped those 15, about a
quarter of the calls and about $1.30: an estimate from the labels, not something the run showed.

**What one day can't say**

- The regime gate is meant to skip calm bars, but it skipped nothing: the QQQ position made its safety rule fire on
  every bar, so it was a pure agent in disguise. Its small saving came from a shorter session and fewer tokens read.
- The ORB veto never consulted the lab's strategy, so we don't know whether it signalled. Its $0.00 is not a saving.
- All three said wait on every bar: no profit or loss to compare. A quiet down-trend day can't tell a good design from
  a cautious one.
- The reasons differed (QQQ mentioned on 62 bars against 5): chance or the shorter session, not checked.
- One day, one market, one session each, one shared account.

**What it suggests, weakly**: all three ran cleanly all day; the gate's potential saving is modest (about a quarter of
the calls on a day with 15 ranging bars). A hint, not a ranking.

**Next evidence**: rerun with a snapshot that shows only SPY, or on a day when the account holds nothing else. Then count
what the gate skipped that the pure agent would have acted on, and how many signals the ORB strategy gave and how many
Claude vetoed. Changing the snapshot means touching the desk code, so it was not done.

## Rules to keep

1. Fix the threshold before you test, and never tune it on the bars you judge it on.
2. Check what your data really is: delayed data means the newest bar may not be finished.
3. Watch out for a shared account: a rule that looks at "any position" sees positions that aren't yours.
4. Never call a variant better after one day. Cheaper is not better.
