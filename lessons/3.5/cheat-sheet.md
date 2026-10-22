# Skills and subagents: cheat sheet

## Skills

A skill is a folder with a `SKILL.md` file: instructions Claude loads when it needs them.

```
---
name: paper-guard
description: When to use this skill. Name the trigger words: libraries, ports, function names.
---

# The instructions: tables, a checklist, a report format...
```

| Where | Who gets it |
|---|---|
| `.claude/skills/<name>/SKILL.md` in a repo | Everyone who clones the repo (a project skill) |
| `~/.claude/skills/<name>/SKILL.md` | You, in every project (a personal skill) |

- The **description** is always in Claude's context (paper-guard: about 150 tokens). The rest loads only when the
  skill is used. A clear description is what makes Claude load the skill by itself.
- `/skills` lists every skill and its token cost; `/` searches the list; Escape closes it.
- `/<skill-name> <request>` runs a skill by name, for example `/paper-guard check the whole repo`.
- A skills folder created during a session isn't watched yet: `/exit`, then `claude --continue` (same conversation).

## Subagents

A subagent is a helper Claude starts with its own clean context. It does one job; only its summary comes back.

- Ask for them in plain words: "Use two subagents in parallel, both on the Haiku model...".
- The panel at the bottom shows each helper's type, job, running time and tokens. Down arrow selects one, Escape
  goes back.
- Their web pages and file reads stay inside the helpers, so your main conversation stays short.

## Your own subagent

```
---
name: lab-reviewer
description: When Claude should use it.
tools: Read, Grep, Glob      # read-only: it can't edit files
model: haiku                 # a smaller model that uses less
skills:
  - paper-guard
---

What the reviewer does, and how it reports.
```

| Where | Who gets it |
|---|---|
| `.claude/agents/<name>.md` in a repo | This project |
| `~/.claude/agents/<name>.md` | All your projects |

- In the version we recorded, the `/agents` wizard had been removed: ask Claude to create the file, or write it yourself.
- The agent list loads at startup: after creating one, `/exit` and `claude --continue`.
- "Use the lab-reviewer agent to review connect_test.py." A read-only reviewer only reports; Claude makes the edits
  after you say yes.

## Cost

Subagents run on your plan, and every token they use counts toward your limits (in the lesson, about 30,000 tokens
per helper within seconds). Use Haiku for simple side jobs, and keep an eye on the usage bar.

## Paper only

| Program | Paper (allowed) | Live (forbidden in the Trading Lab) |
|---|---|---|
| TWS | 7497 | 7496 |
| IB Gateway | 4002 | 4001 |

Paper account IDs start with `DU`.
