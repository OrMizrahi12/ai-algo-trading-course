# Lesson 13.3 prompts

Everything typed in the lesson, in order. Lines that start with `/` are Claude Code commands. Interactive Claude Code
sessions in `~/trading-desk` (auto mode), with Obsidian open on the desk's vault beside them. Paper account only.

## 1. Ask for a memory budget

```text
/clear
```

```text
Our vault will keep growing. Decide what the trader needs on every bar and what it can look up only when it needs it. Then add a memory budget: a script that measures, in tokens, what loads on every bar, fails above 6,000 tokens, and says which note to summarise or move. Write the rules for summarising, archiving and resolving lessons that disagree into the vault README. To test it, add a few seeded notes, clearly marked as seeded and not real trades, until it goes over budget, then bring it back under.
```

On our computer Claude worked for 4 minutes 45 seconds. One of its first commands was blocked by the guardrail hook from
lesson 12.3 (it named the settings file), so it switched to read-only commands. It found that the trader has only the
Skill tool, wrote `desk/memory.py`, wired the memory brief into `desk/heartbeat.py`, and measured a baseline of 1,649
tokens. Then the seeded test: 5 notes, 4,192 tokens; 9 notes, 6,070 tokens and exit 1; the conflicting pair resolved
(5,575); one-sentence summaries (2,103); then every seeded note archived. It wrote the README rules and
`tests/test_memory.py`.

## 2. Run the budget and commit

```text
Run the budget script so I can see its report, then commit.
```

Then, in the same session, we ran it ourselves (the `!` runs a shell command from Claude Code's prompt):

```text
! uv run -m desk.memory
```

Our report: `1214` for the constitution `CLAUDE.md`, `105`, `123`, `116` and `91` for the four skills, `1649 TOTAL of 6000
allowed: ok`. Yours will differ.

## 3. Find a lesson in the archive

```text
/clear
```

```text
Use the vault the way its README says. Say a 5-minute bar on heavy volume just closed above the opening range high. Search the vault, including the archive, for what we learned about entering breakouts. Tell me what applies now, what was superseded and why, and which notes are seeded.
```

Claude read the README and the rules, then the playbook, searched the lessons including `Lessons/Archive/`, and answered
in 29 seconds. It said the vault has no real lessons about breakouts (all are seeded), listed what applies now from the
opening range breakout playbook, explained the superseded note, and questioned the ruling: the README's first step
(check whether the conditions differ) may have been skipped, so the person should decide. It changed no files.

## Pause and try

1. Ask Claude to split your trader's memory into every bar and on demand, and to add a budget script.
2. Seed a few clearly marked fake lessons until the script fails, then bring it back under.
3. Ask a normal session to find a lesson in the archive.

You're done when the budget script says `ok`, every seeded note sits in the archive, and Claude can still find it when
you ask.
