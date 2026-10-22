# Student kit: Lesson 3.5, Skills and subagents

Module 3: Claude Code from zero · AI Algorithmic Trading with Claude Code and Interactive Brokers

In this lesson you wrote the Trading Lab's first skill, **paper-guard**, which checks that any code connecting to
Interactive Brokers uses a paper port and a paper (DU) account, and watched Claude load it by itself. Then you ran two
subagents in parallel on Haiku, and built a read-only reviewer subagent, **lab-reviewer**, that found four real issues
in `connect_test.py`.

## What's in this kit

| File | What it is |
|---|---|
| `prompts.md` | Every request typed in the lesson, ready to copy, plus the two pause-and-try exercises |
| `cheat-sheet.md` | Skills and subagents on one page: where the files live, the commands, the restart rule, the cost |
| `trading-lab/.claude/skills/paper-guard/SKILL.md` | The paper-guard skill exactly as Claude wrote it in the lesson |
| `trading-lab/.claude/agents/lab-reviewer.md` | The lab-reviewer subagent exactly as Claude wrote it |
| `trading-lab/connect_test.py` | The test script after the reviewer's four fixes (paper port check, DU check, `readonly=True`) |
| `trading-lab/pyproject.toml` | The project file with the `ib-async` dependency added by `uv add` |

The `.claude` folders start with a dot, so some file browsers hide them: use `ls -a`, or show hidden files.

## Try it yourself

**Checkpoint 1: a skill of your own.**

1. In your `trading-lab` folder, start `claude` and ask for a project skill with one rule you never want broken, and
   a clear description (the paper-guard request in `prompts.md` is a good model).
2. If `.claude/skills/` didn't exist before, Claude Code isn't watching it yet: `/exit`, then `claude --continue`.
3. `/skills` should list your skill as a project skill. Search for its name.
4. Ask for something that should trigger it, and look for the `Skill(<name>)` line in Claude's reply.

**Checkpoint 2: a reviewer of your own.**

1. Ask Claude for a project subagent with only the Read, Grep and Glob tools, on Haiku, that uses your skill
   (the lab-reviewer request in `prompts.md`).
2. Restart (`/exit`, then `claude --continue`): the agent list is loaded at startup.
3. Ask it to review one file.

You're done when the review comes back and `git status` shows that no file changed. Your output will differ from the
video in the details; that's expected.

## Good to know

- Everything here runs against a **paper** (simulated) account. The live ports (TWS 7496, IB Gateway 4001) are
  forbidden in the Trading Lab, and paper-guard refuses them.
- `connect_test.py` is not run in this lesson. We connect to TWS for the first time in Module 4.
- Subagents use the same plan as you do: every token they use counts toward your usage limits. Use a smaller model
  (Haiku) for simple side jobs.
- Menus, versions and limits shown in the video were current at the time of recording (October 2026). In that version
  the `/agents` wizard had been removed, so we asked Claude to write the agent file.

## Next

Lesson 3.6: MCP, hooks and permissions.
