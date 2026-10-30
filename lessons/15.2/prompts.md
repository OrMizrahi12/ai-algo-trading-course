# Lesson 15.2 prompts

Everything typed in the lesson, in order. Lines that start with `/` are Claude Code commands. Interactive Claude Code
sessions in `~/trading-desk` (auto mode). Paper account only.

## 1. Ask for a regime gate

```text
/clear
```

```text
Build a regime-gated variant of the desk. A deterministic regime filter labels each bar as trending or ranging, using only information known at that bar, with thresholds taken from our module 7 research in ~/trading-lab, not tuned on any forward data. Claude is woken only on bars the filter allows; once awake it still decides everything. Make it a switch next to --team, add tests, and replay our saved snapshots to show which bars would have woken Claude and what that saves.
```

Claude read the desk and searched the lab's research, then asked two questions before writing any code:

- **Which threshold source?** There are no regime thresholds where we pointed it: the lab's day-type labels use
  hindsight (the month's direction, the top third of days by open-to-close move), so they can't be known live. The only
  live-knowable number is H1's rule, "more than 5 ATR from the day's open", fixed in advance; H1 failed as a strategy
  filter and its card says not to tune it. Options: H1's 5 ATR rule (recommended), "I'll point you to the numbers", or
  derive thresholds from the saved snapshots (Claude advised against it: tuning on the data it would replay makes the
  savings figure circular). **We chose H1's rule.**
- **Which bars should wake Claude?** Options: trending only plus always when holding (recommended), ranging only plus
  always when holding, trending only with no exceptions. **We chose trending only, plus always when holding**: Claude is
  also always woken on the first bar after a trade ends and in the exit window before the close, so a stop-out or a
  flatten is never missed.

On our computer Claude then worked for 3 minutes 46 seconds. It read the heartbeat, the lab's `open_distance_atr`
function and how snapshots are built, and wrote four pieces: the regime filter `desk/regime.py` (83 lines), a hook in
the heartbeat, the `--regime-gate` switch and a replay report `desk/regime_replay.py` (109 lines). It added
`tests/test_regime.py`: 398 tests passed, 14 of them new.

Its answer (details in the cheat sheet): the switch is off by default; the threshold's source and the lab's FAIL verdict
on H1; what the gate does; the replay over 79 saved snapshots (10 bars woken, 69 skipped, all 10 wakes safety cases,
the regime itself woke none; the skipped bars cost $1.11 of $1.42); and the caveats: not one trending bar in about two
days, so the savings come from sleeping through quiet days, not from the filter finding anything; a tiny sample; and
CLAUDE.md still says Python never skips a bar (left alone so the instruction hash doesn't change).

## 2. Commit and record it

```text
Commit it, and add a ledger row for the gated variant.
```

Claude checked the instructions hash: unchanged (the same as Trader v2.2), so the gate is a run mode, not an
instruction change, and the ledger row "Trader v2.2 + regime gate" says to compare it by that row and by the journal
fields `regime_gate` and `model_asked: false`. One commit: "Add the regime gate: wake Claude only on trending bars and
safety cases (--regime-gate)". Claude also noted that the `--team` switch never got a ledger row.

## 3. The opposite design: a strategy with a Claude veto

```text
Now the opposite design. Use the lab's opening_range_breakout strategy unchanged to propose the trades. Claude reads the full context and may only veto a signal, with a reason; it never creates a trade or changes size, stop or target. Add it as a third switch with tests and a ledger row, and replay it on the days we have saved, showing every signal and what Claude said about it.
```

Claude worked for 4 minutes 22 seconds. It read the lab's strategy and the team code, found the opening range on the
saved days, wrote the veto's instructions (`.claude/orb/veto.md`: "You are the veto of a PAPER trading desk"), the veto
module `desk/orb_veto.py` and a replay `desk/orb_replay.py` (lab defaults, fixed size 0.5 R, stop = opening range low,
no target). The replay found one signal. A small fix made "today" the New York trading day. `tests/test_orb_veto.py`
uses a fake Claude and a fake broker, no network. 419 tests passed; then the replay ran for real with one live call for
that signal (Claude called it "a few cents of API money": on a subscription that is usage, not a bill), the readme, the
hash of the veto's prompt for the ledger, and 421 tests passed. One commit: "Add the ORB veto: the lab's
opening_range_breakout proposes, Claude may only veto (--orb-veto)".

The replay: **0 signals as the desk saw the bars**; 1 signal on the newest version of the bars (2026-10-23, 09:55 New
York, a close of 760.94 above the range high of 760.73, stop 759.72), which Claude approved with a reason. The caveat:
when the desk first saw that bar it closed at 760.54, below the range high, so live the desk would have seen no signal.
And a finding: **61 of the 178 saved bars closed at a different price in a later snapshot** than in the first one that
showed them. Claude did not investigate it.

## 4. Find out why the bars changed

```text
That revision finding matters more than the veto. Find out why those bars changed, and whether the live desk decides on bars that were not finished yet. Fix it if so, with a test.
```

Claude worked for 4 minutes 33 seconds. It read the lab's bar feed and the desk's snapshot code and measured: in 63 of
79 snapshots the newest bar differed from its final version; the second newest never did. The bug: the feed calls a bar
closed by the wall clock, but the paper data lags about 15 minutes, so the newest "closed" bar is still filling. It added
a settle step (`snapshot.settled_bars`) to the heartbeat and the MCP trade path. One existing test broke (the older fake
feeds have no delay, so the test rig now turns the settle step off by default); the new `tests/test_settled.py` uses a
fake feed that behaves like delayed data. 429 tests passed. One commit: "Decide only on finished bars: drop bars IB is
still filling (delayed data)".

Its answer began: "Yes, the live desk was deciding on bars that weren't finished." Then why, what it measured, the fix
and what it invalidates (see the cheat sheet). It has not run the fix against the live Gateway.

## 5. Run the variants beside the live desk

Two days later, with the market open, in the same session that still ran the team watcher from lesson 15.1:

```text
New topic, the variants lesson. Run the regime-gated desk and the ORB-veto desk the same way as the team watcher: dry run, their own client IDs and journals, nothing in the desk edited. Let them run beside the live plain desk until the close. After the close we'll build one comparison table from the journals: decisions, reasons, model calls and usage per design.
```

Claude checked which files and state each variant writes, so the launchers stay isolated, then wrote one small watcher
script outside the repo that takes a variant name, and launched both: the regime gate on client ID 41 with its journal
in `data/regime/`, the ORB veto on 42 in `data/orbveto/`. Git status stayed clean. It warned us before the day played
out: the two variants started at the 14:35 UTC bar, about 25 minutes after the others, so compare only bars all designs
saw; all designs share one paper account, including the lab's 10 QQQ shares, and the veto asks "is a position or order
open?", so it may decide differently because of that position; and the veto's usage will show as a count of calls.

## 6. The comparison, honestly

After the close:

```text
Now the variants. Build the comparison table for the three designs on the bars they all saw today: the pure agent (the live desk), the regime-gated desk and the ORB veto. Decisions, reasons, how often the model was called, and usage per design. Then your honest reading: what, if anything, one day says about which design is better.
```

Claude lined up the three journals: 62 common bars (14:35 to 19:40 UTC). "None of the three designs did anything
different, and the QQQ position kept the two variants from showing what they are for. One day gives no ranking." The
table and the can and can't say list are in the cheat sheet.

## Pause and try

1. Ask Claude for a regime-gated switch, with a threshold fixed in advance, never tuned on the data you'll judge it on.
2. Ask for a strategy with a veto, where Claude can only refuse.
3. Replay your saved bars through both, and check whether your desk decides on unfinished bars.

You're done when you have both switches, off by default, and an honest list of what your replay can and can't say.
