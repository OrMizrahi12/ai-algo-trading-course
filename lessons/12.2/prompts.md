# Lesson 12.2 prompts and commands

Everything typed in the lesson, in order. Lines that start with `/` or `!` are typed in Claude Code. Both sessions run in
`~/trading-desk`, in auto mode. Paper account only.

## 1. Move the know-how into four skills

```text
/clear
```

```text
Our CLAUDE.md should stay short because it loads on every bar. Move the detailed trading know-how into four skills in .claude/skills: market-read, entry-checklist, trade-management and post-trade-review. Give each a description that says exactly when to use it, keep each under 80 lines, and make entry-checklist include the position-size math in R. Then trim CLAUDE.md so it points to them. Check that the trader really can load these skills when the heartbeat runs it, run the tests, and commit.
```

About 4 minutes on our computer: the four skills, CLAUDE.md from 77 to 54 lines, the trader wired to the Skill tool and a
plugin folder, one real model call as a check, 141 tests passing (at that point), a new ledger row (Trader v2), committed.

Print a skill without leaving Claude Code (`!` runs a shell command):

```text
!cat .claude/skills/entry-checklist/SKILL.md
```

## 2. Journal which skills load on each bar (the next day, market hours)

```text
Make the heartbeat record which skills the trader actually loaded on each bar, taken from Claude's own output (its Skill tool calls), and put them in the journal, so we can see that skills load on demand and not on every bar. Add a test and commit. Then run the heartbeat on the paper Gateway with --dry-run for a few real bars, and show me per bar which skills were loaded and why. The trader now keeps one session per day, so also tell me whether a skill loaded on an earlier bar is still known on later bars.
```

About 4 minutes: stream-json output, the `skills` journal field, committed. The dry run handled three bars (15:10 to 15:20
UTC): no skill loaded on any of them. A throwaway probe showed that a skill loaded on one bar is still known on the next
bar of the same session.

## 3. Find out why a skill never loaded

```text
Find out why the trader skipped desk:market-read on those bars although CLAUDE.md tells it to load it first. Don't force it in Python: look at what the trader was told and what it saw. If our instructions are unclear or contradict each other, propose the smallest change, make it, record it in the ledger, then run the next real bars with --dry-run and show the skills column again.
```

About 1.5 minutes for the diagnosis and the fix (two sentences in CLAUDE.md, Trader v2.1 in the ledger), then about 11
minutes of waiting for new bars on the delayed feed. Result: 15:25 loaded `desk:market-read` (a new session), 15:30 and
15:35 loaded nothing (the session resumed). All three were `wait`; no orders.

The heartbeat commands Claude ran:

```text
uv run -m desk --once --dry-run
```

## Pause and try

1. Move your own trading know-how into skills, each with a "use when" description, and trim your `CLAUDE.md`.
2. Make sure your trader can really load them, and check it with one real model call.
3. Journal the skills on every bar, and run a few bars on paper with `--dry-run`.

Done when your journal shows a skill loading on the first flat bar of a session, and not again on every bar after it.
