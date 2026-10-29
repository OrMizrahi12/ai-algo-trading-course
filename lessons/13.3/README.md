# Student kit: Lesson 13.3, Memory that stays sharp

Module 13: Memory with Obsidian · AI Algorithmic Trading with Claude Code and Interactive Brokers

The desk's vault will keep growing: every closed trade can teach a lesson. But whatever the trader reads on every bar
costs tokens on every bar, all day long. In this lesson we split the desk's memory into two tiers, **every bar** and
**lookup only**, and give it a **memory budget**: a script that measures, in tokens, what loads on every bar, fails above
6,000 tokens and says which note to summarise or move. Claude also writes the vault's rules for summarising, archiving
and settling two lessons that disagree. We test it with seeded (made-up) lessons until it goes over budget, bring it back
under, and then ask a normal Claude session to find an archived lesson.

What happened on our computer (paper account, 2026-10-24):

1. In a fresh Claude Code session in `~/trading-desk` (auto mode), with Obsidian open on the vault, we sent request 1.
   Claude found that the trader has no file tools, so before this it received no vault text at all.
2. It wrote `desk/memory.py` and wired a short **memory brief** (one sentence per active lesson) into the first message
   of each day's session. The brief was empty, so the trader's behaviour did not change.
3. The baseline was 1,649 tokens. Nine seeded lessons pushed it to 6,070 and the script failed (exit 1). Claude resolved a
   conflicting pair, added one-sentence summaries (2,103 tokens), then archived every seeded note so the real trader
   never sees a fake lesson. It wrote the README rules and tests, and committed everything in one commit.
4. In a new session we asked Claude to search the vault, archive included, for what applies to a breakout bar on heavy
   volume. It found the archived lessons, said they are all seeded, and questioned one of the rulings.

## What's in this kit

| File | What it is |
|---|---|
| `prompts.md` | Every request typed in the lesson, the budget command, and the pause-and-try exercise |
| `cheat-sheet.md` | The words, the two tiers, the budget numbers, a lesson's life, and the rules for summarising, archiving and conflicts |
| `trading-desk/desk/memory.py` | The memory budget script (`uv run -m desk.memory`) |
| `trading-desk/desk/heartbeat.py` | The heartbeat, now adding the memory brief to the first message of each day's session |
| `trading-desk/tests/test_memory.py` | Tests that run the whole cycle on a temporary vault: over budget, then back under |
| `trading-desk/vault/README.md` | The vault README with its new "Memory budget" section (tiers, statuses, summarising, archiving, conflicts, seeded notes) |
| `trading-desk/vault/Lessons/Archive/` | The nine seeded test lessons, all archived. Every one is made up and says so in a red banner |
| `trading-desk/.claude/vault-skill/vault/SKILL.md` | The vault skill, now pointing at the new rules |

These are the files this lesson added or changed, as committed at the end of the lesson. Copy them over your desk from
lesson 13.2. The folder that starts with a dot (`.claude`) is hidden on most systems.

## Before you start

- Your `~/trading-desk` with the heartbeat from Module 11, the skills and guardrails from Module 12, and the vault from
  lessons 13.1 and 13.2.
- Claude Code in the terminal, signed in with your subscription, and `uv`.
- Obsidian, with the desk's `vault/` folder open as a vault.
- Time on our computer: about 5 minutes for Claude to build and test the budget.

## Try it yourself

1. Send request 1 in `prompts.md`, or copy the kit's files over your desk and run `uv run pytest -q tests/test_memory.py`.
2. Run `uv run -m desk.memory` and read the report.
3. Ask a normal Claude session to find a lesson in `vault/Lessons/Archive/` (request 3).

You're done when the budget script says `ok`, every seeded note sits in the archive, and Claude can still find it when
you ask. Your numbers and Claude's answers will differ from the video, and that's fine.

## Good to know

- **Seeded notes are fake.** They exist only to test the budget. Their counts and prices (including the SPY example) are
  invented. Keep them archived, or delete them from your own vault once you've seen the cycle work.
- **The trader still can't look anything up.** The lookup tier is open to you, interactive Claude sessions and the note
  writer, not to the trader. Giving the trader a lookup skill would change its hashed instructions and start a new
  experiment, so that decision is yours.
- **Token counts are estimates** (characters divided by 3.5, which over-counts a little on purpose).
- **The person decides.** Claude proposes lessons and rulings; only you set a lesson `active`. In the lesson, Claude
  itself questioned one ruling: always check the conditions before comparing evidence.

Paper account only. Educational content, not financial advice; nothing here is a promise of profit or a recommendation.
