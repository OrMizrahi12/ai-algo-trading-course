# Lesson 14.2 prompts

Everything typed in the lesson, in order. Lines that start with `/` are Claude Code commands; a line that starts with `!`
runs a shell command from inside Claude Code. One interactive Claude Code session in `~/trading-desk` (auto mode), with
Obsidian open on the desk's vault beside it. Paper account only.

## 1. Ask for lesson tracking

```text
/clear
```

```text
Add lesson tracking. Record which lessons the trader applied in each decision, and write a script that compares, for each lesson, the trades that applied it with similar trades that did not: count, average R, and how uncertain that is. A lesson may move into the playbook only after 20 applications with a clearly better average R, and it is archived when the evidence turns against it. Every change goes into a rules change log and into Git. Run it on our real journal first, then on a seeded demo dataset, clearly labelled, to show one promotion and one rollback.
```

On our computer Claude worked for 8 minutes 32 seconds. It read how the desk stores its journal, lessons and playbook,
and the real journal (273 tests passed at the start). It made `lessons` a required key of every trader answer, which
broke the MCP trade tools (they build the same decision) and one old test that hand-wrote a sell answer without the key;
it fixed both. It wrote the tracker (`desk/lessons.py`) and ran it on the real journal: no closed trades, no active
lessons, nothing to compare. It wrote the seeded demo (`desk/lesson_demo.py`) in its own folder; on the first try only
16 applications existed by the run date, so it moved the made-up history earlier. 289 tests passed, the memory budget
was 1,753 of 6,000 tokens, and the code went into one commit with the demo's commits after it.

It also said what it changed in `CLAUDE.md` (the trader's output contract) and listed its own choices: the threshold of
10 applications for archiving and rollbacks, the 10-trade minimum comparison group and the 95% bootstrap interval.

## 2. See the reports

```text
Show me the tracker report on our real journal, then on the seeded demo.
```

Real journal: 0 closed trades, no active or promoted lesson, nothing to compare, nothing changed. Seeded demo (every
number made up): on 2026-09-04 "Wait for the retest after a breakout" had 30 applied trades averaging +0.41R against 21
similar ones at -0.09R, a difference of +0.50R with a 95% interval of +0.04R to +0.96R: PROMOTE. On 2026-10-23, counting
only trades after the promotion, 13 applied trades averaged -0.87R against +0.08R: interval -1.56R to -0.37R, ROLLBACK.
The second lesson stayed KEEP both times (8, then 12 of the 20 applications needed).

## 3. The review after every 50 trades

```text
Now the bigger review: every 50 trades, a report that breaks the results down by setup, time of day and market regime, with how uncertain each number is. Build it, then run it on the seeded demo, since our real desk has no trades yet, and save the report as a note in the demo vault.
```

Claude worked for 3 minutes 52 seconds: `desk/review.py`, the regime (the 15-minute trend at entry) and the setup (from
the trade notes) as new trade fields, a guard so a seeded review can never be written into the real vault, and 299 tests.
The demo review is blank on purpose: the demo's setup, time and regime labels are random, so "no clear difference" is
the right answer.

To print the note (shell mode, from inside Claude Code):

```text
! sed -n 12,40p "experiments/lesson-demo-SEEDED/vault/Reviews/Review after 50 trades.md" | cut -c1-140
```

## Pause and try

1. Ask Claude to record which lessons each decision used.
2. Ask for a tracker that compares them with similar trades, with the count and the uncertainty, and that only reports
   by default.
3. Run it on your journal, and on a clearly labelled seeded demo.

You're done when your real journal says not enough data yet, and the demo shows one promotion and one rollback, each in
the change log.
