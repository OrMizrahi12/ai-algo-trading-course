# Student kit: Lesson 14.2, Keep or discard

Module 14: Self-improvement · AI Algorithmic Trading with Claude Code and Interactive Brokers

Our desk now writes a lesson after every closed trade. But a lesson is only a guess until the trades say otherwise. In
this lesson the trader records **which lessons shaped each decision**, and a tracker compares the trades that applied a
lesson with **similar trades that didn't**: the count, the average R and how uncertain that is. A lesson is **promoted**
into the playbook only after 20 applications with a clearly better average R, **archived** when the evidence turns
against it, and a promoted lesson can be **rolled back**. Every change goes into a rules change log and into Git. Then a
deeper review breaks every 50 trades down by setup, time of day and market regime.

## What's in this kit

| File | What it is |
|---|---|
| `prompts.md` | Every request typed in the lesson, in order, and the pause-and-try exercise |
| `cheat-sheet.md` | The words, the tracker's rules, how to read an interval, the 50-trade review, and the safe defaults |
| `trading-desk/` | The files this lesson added or changed in the desk, as committed at the end of the lesson: `CLAUDE.md` (the trader's new `lessons` key), `README.md`, `desk/lessons.py` (the tracker), `desk/lesson_demo.py` (the seeded demo), `desk/review.py` (the 50-trade review), `desk/decision.py`, `desk/trades.py`, `desk/heartbeat.py`, `desk/memory.py`, `desk/scribe.py`, `desk/mcp_server/trade.py`, `tests/test_lessons.py`, `tests/test_review.py`, `tests/conftest.py`, `tests/test_decision.py`, `tests/test_seatbelts.py`, `vault/README.md` and the vault skill. Copy them over your desk from lesson 14.1 |
| `trading-desk/experiments/lesson-demo-SEEDED/` | The seeded demo's notes: its rules change log (one promotion, one rollback), the two lessons, the playbook list and the review after 50 trades. **Every number in it is made up.** `uv run -m desk.lesson_demo` rebuilds the whole folder, including the 80 made-up trade notes left out here |

## Before you start

- Your `~/trading-desk` from lesson 14.1: the heartbeat, the skills, the guardrails, the MCP server, the vault, the note
  writer and the post-trade review.
- Claude Code in the terminal, signed in with your subscription, and Obsidian open on the desk's `vault/` folder.
- Time on our computer: about 8 and a half minutes for Claude to build the tracker, under 20 seconds for the reports, and
  about 4 minutes for the 50-trade review.

## Try it yourself

1. Send request 1 in `prompts.md`, or copy the kit's files over your desk and run `uv run pytest -q`.
2. Run `uv run -m desk.lessons` on your real journal. With few or no trades it says there is nothing to compare: that is
   the right answer.
3. Run `uv run -m desk.lesson_demo` and read the demo's change log.
4. Optional: request 3, the review after every 50 trades.

You're done when your real journal says not enough data yet, and the demo shows one promotion and one rollback, each in
the change log. Your code, numbers and Claude's answers will differ from the video, and that's fine.

## Good to know

- **Report-only by default.** `uv run -m desk.lessons` changes nothing. `--apply` makes the changes, `--commit` also
  commits them. The tracker promotes without asking a person, which goes further than the vault's rule that only a person
  makes a lesson active, so run it with `--apply` only when you have looked at the report.
- **Not enough data yet is a normal answer.** A new desk has no closed trades. The tracker says so and changes nothing.
- **Seeded means made up.** The demo is labelled "DEMO (seeded, made-up data)" everywhere, lives in its own folder, and
  the tracker refuses to apply seeded trades to the real vault. Its outcome is built in: it shows the machinery, not a
  real lesson.
- **No lesson touches the risk limits.** Lessons shape decisions. The risk limits and the guardrails from lesson 12.3
  stay outside anything the tracker can change.

Paper account only. Educational content, not financial advice; nothing here is a promise of profit or a recommendation.
