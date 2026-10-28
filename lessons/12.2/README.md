# Student kit: Lesson 12.2, Skills for the trader

Module 12: Tools, skills and guardrails · AI Algorithmic Trading with Claude Code and Interactive Brokers

Our trader's constitution, `CLAUDE.md`, goes out with every bar, so it should stay short. In this lesson the detailed
trading know-how moves into four skills that Claude loads only when they fit:

1. **Four skills.** `.claude/skills/` holds `market-read`, `entry-checklist`, `trade-management` and `post-trade-review`,
   each a `SKILL.md` with a name, a "use when" description and the instructions (38 to 47 lines each). `CLAUDE.md` went
   from 77 to 54 lines: the mission, the hard risk rules, the output contract and a short list of the skills.
2. **The trader can really load them.** The heartbeat ran `claude -p` with no tools and no setting sources, so the trader
   could not load a skill at all (it answered "CANNOT"). Now `desk/model.py` passes `--tools Skill --plugin-dir <desk>`,
   and `.claude-plugin/plugin.json` points the plugin at `.claude/skills`. The skills appear as `desk:market-read` and so
   on. `CLAUDE.md` still reaches the trader only once, as the system prompt. The instructions hash covers `CLAUDE.md`, the
   plugin manifest and every skill file, so the ledger has a new row, Trader v2.
3. **Which skills loaded on each bar.** `claude -p` now runs with `--output-format stream-json --verbose` (the plain JSON
   output has no list of tool calls), and every journal record has a `skills` field: `[]` = nothing loaded, a list of
   names in order, or `null` = unknown (a timeout or a failed call).
4. **Fixing our own instructions.** The first three bars loaded no skill: step 1 of the constitution (a safety check for
   stale or thin data) let the trader answer `wait` before it reached step 3 (load market-read). Two sentences in
   `CLAUDE.md` fixed it (Trader v2.1 in the ledger), without forcing anything in Python. On the next bars market-read
   loaded on the first bar of the new session and not again on the next two: a loaded skill stays in the day's session.

## What's in this kit

| File | What it is |
|---|---|
| `prompts.md` | The three requests typed in the lesson, the command we used to print a skill, and the pause-and-try exercise |
| `cheat-sheet.md` | The words, always loaded versus on demand, the four skills, the size-in-R math, the flags, the `skills` field, what we saw on paper |
| `trading-desk/` | The desk at the end of this lesson: `.claude/skills/` (the four skills), `.claude-plugin/plugin.json`, the trimmed `CLAUDE.md` (Trader v2.1), `desk/model.py` with the Skill tool and stream-json, `desk/heartbeat.py` with the `skills` journal field, the MCP server from Lesson 12.1, the day sessions from Lesson 11.4, `experiments/ledger.csv`, `tests/` (177 tests with fakes), `README.md`, `pyproject.toml`, `uv.lock` |

The guardrail hook you may notice in the video (it blocks a command that names the settings file) is built in Lesson 12.3,
so it is not in this kit yet.

## Before you start

- Your `~/trading-desk` from Lesson 12.1 (with the day sessions from Lesson 11.4) and the Trading Lab from Module 10. The
  desk reads the lab read-only from `~/trading-lab`.
- `uv` and Claude Code in the terminal, signed in with your subscription.
- For the dry runs: IB Gateway logged in to the **paper** account, API port 4002, during market hours.
- Time on our computer: about 4 minutes for the skills, about 4 minutes for the skills journal, 1 to 2 minutes for the
  fix, and then the bars themselves (our free data runs about 13 minutes behind).

## Try it yourself

1. Move your own trading know-how into skills, each with a "use when" description, and trim your `CLAUDE.md` (request 1
   in `prompts.md`).
2. Make sure your trader can really load them, and check it with one real model call.
3. Journal the skills on every bar (request 2), and run a few bars on paper with `--dry-run`.

You're done when your journal shows a skill loading on the first flat bar of a session, and not again on every bar after
it. Your code, numbers and Claude's answers will differ from the video, and that's fine.

## Good to know

- **Descriptions decide.** Claude sees only the name and description of every skill on every bar; the body loads when the
  description fits. Write the description as "use when ...", and say when *not* to use it.
- **Each load costs time.** A skill load is one more model turn inside the 120-second bar budget. That is why we did not
  take Claude's offer to reload market-read on every flat bar: on demand is the point.
- **Check what really loads.** A skill that is never loaded does nothing. The `skills` field in the journal is how we
  found out, and the fix was in our own words, not in Python.
- **Skills are instructions, not guarantees.** Anything that must always hold belongs in code (Lesson 12.3).
- **A new instructions hash means a new session.** Editing a skill changes the hash, so the desk starts a fresh session,
  and the ledger gets a new row. Switching git branches rewrites files too, which is why Claude saw every file touched
  at the same minute in the video.

## Safety

Paper trading only. The desk connects to a local paper Gateway only, and `--dry-run` sends no orders. Educational content,
not financial advice; nothing here is a recommendation or a promise of profit.
