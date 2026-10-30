# Student kit: Lesson 15.2, Variants and hybrids

Module 15: Advanced agent designs · AI Algorithmic Trading with Claude Code and Interactive Brokers

Our desk is a **pure agent**: on every bar Claude sees everything and decides, even when the answer is wait. That stays
the foundation. This lesson builds two **optional variants** next to it, each behind its own switch and off by default:

- a **regime gate**: plain code labels each bar as trending or ranging with a rule fixed in advance, and wakes Claude
  only when the rule allows (plus every safety case). Once awake, Claude still decides everything;
- an **ORB veto**: the lab's opening range breakout strategy, unchanged, proposes the trades, and Claude may only
  approve or veto each signal, with a reason.

Along the way Claude finds that the desk was deciding on bars that weren't finished yet (the paper data is delayed),
and fixes it. Then all three designs run side by side on one live paper day, and we compare them, honestly.

## What's in this kit

| File | What it is |
|---|---|
| `prompts.md` | Every request typed in the lesson, in order, what Claude did with each one, and the pause-and-try exercise |
| `cheat-sheet.md` | The words, the three designs, the regime rule and the wake rule, the veto rules, the replays, the unfinished-bar fix, the live comparison and what one day can and can't say |
| `trading-desk/` | The desk files this lesson added or changed, as committed after the unfinished-bar fix: the regime gate (`desk/regime.py`, `desk/regime_replay.py`, `tests/test_regime.py`), the ORB veto (`.claude/orb/veto.md`, `desk/orb_veto.py`, `desk/orb_replay.py`, `tests/test_orb_veto.py`), the settled-bars fix (`desk/snapshot.py`, `desk/mcp_server/core.py`, `tests/test_settled.py`, `tests/conftest.py`, `tests/mcp_fakes.py`), the switches (`desk/__main__.py`, `desk/heartbeat.py`, `desk/model.py`), `README.md` and the version ledger `experiments/ledger.csv`. Copy them over your desk |

## Before you start

- Your `~/trading-desk` from the earlier lessons (the heartbeat, the skills, the journal, the `--team` switch from
  lesson 15.1) and saved snapshots of earlier bars in `data/desk/snapshots/` (both replays read them).
- Your `~/trading-lab`, read-only: the regime rule comes from its research card H1, and the ORB veto imports its
  `opening_range_breakout` strategy unchanged.
- Claude Code in the terminal, signed in with your subscription.
- A paper account in IB Gateway or TWS for the live part. The variants run as dry runs: they record decisions and send
  no orders.
- Time on our computer: about 4 minutes for each build, about 5 minutes for the fix; the live part runs as long as the
  market session you give it.

## Try it yourself

1. Send requests 1 and 2 in `prompts.md` (the regime gate), or copy the kit's files over your desk and run
   `uv run pytest -q`.
2. Run `uv run -m desk.regime_replay` and `uv run -m desk.orb_replay`: what each design would have done on bars you
   already have.
3. Send request 4 on your own desk: does it decide on bars that weren't finished yet? Fix that first: every comparison
   you make later depends on it.
4. On a market day: request 5, the variants next to your desk as dry runs, each on its own client ID and journal.
5. After the close: request 6, the comparison, and the honest list of what one day can and can't say.

You're done when you have both switches, off by default, and an honest list of what your replay can and can't say.
Your code, numbers and Claude's answers will differ from the video, and that's fine.

## Good to know

- **The threshold is fixed in advance.** We asked for thresholds from our research. Claude found none that can be known
  live (the lab's day-type labels use hindsight), and offered the only live-knowable number: H1's rule, trending when
  the last close is more than 5 ATR from today's first open. H1 failed as a strategy filter and its card says not to tune
  it. Never tune a gate on the bars you will judge it on: the savings figure becomes circular.
- **Skipped bars are not lost.** A bar the gate skips is journaled as a `wait` with `model_asked: false` and a
  `regime_gate` field, and the next call's update carries the skipped bars.
- **The veto can only refuse.** Claude never creates a trade or changes the size, the stop or the target. A veto, or a
  missing, late or invalid answer, becomes a wait, and every desk gate still applies after an approval.
- **Unfinished bars.** Paper market data is about 15 minutes delayed, so the newest bar IB returns is still being filled.
  The desk now decides only on bars that ended at least 16 minutes ago (`snapshot.settled_bars`). Every decision and
  replay made before that fix used a partial newest bar; the ledger says so. The lab's own live engine has the same
  flaw; Claude treated the lab as read-only and left it alone.
- **A shared account contaminates "any position" rules.** On the live day the lab's own QQQ position sat on the same
  paper account. The regime gate woke Claude on every bar for a safety case ("holding a long"), and the veto never asked
  the strategy because "a position is open". One day showed no ranking at all.
- **Costs** are Claude Code's usage figures at list prices, not a bill on a subscription.
- **The live watcher is not in this kit.** On camera Claude wrote a small script outside the desk's folder that runs each
  variant as a dry run on its own client ID (41 and 42 on our computer), with its own journal in `data/regime/` and
  `data/orbveto/`. Ask for the same in your own words (request 5); keep it out of the desk's code so the desk's forward
  test stays clean.

Paper account only. Educational content, not financial advice; nothing here is a promise of profit or a recommendation.
