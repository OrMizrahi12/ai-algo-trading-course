# Student kit: Lesson 14.3, An agent that rewrites its own playbook

Module 14: Self-improvement · AI Algorithmic Trading with Claude Code and Interactive Brokers

Our desk already reviews every closed trade and writes lessons. Now it may improve its own playbook and skills, safely.
Every change is a **proposal**: a patch with its reason and its evidence, checked automatically (tests, the memory
budget, the risk files untouched) and applied only after a person approves. Each applied change is a commit and a new
**trader version** in the ledger. Then a report explains what changed, and why, across every version, and checks that
the ledger is complete.

## What's in this kit

| File | What it is |
|---|---|
| `prompts.md` | Every request typed in the lesson, in order, and the pause-and-try exercise |
| `cheat-sheet.md` | The words, the pipeline, what a proposal may change, the tool's commands and checks, and what a good proposal says |
| `trading-desk/` | The files this lesson added or changed in the desk, as committed at the end of the lesson: `desk/proposals.py`, `tests/test_proposals.py`, `proposals/0001-market-read-load-first.patch` and `.md`, `.claude/skills/market-read/SKILL.md` (with the applied change), `experiments/ledger.csv` (with the Trader v2.1.1 and v2.2 rows), `vault/README.md` and `vault/Versions/Trader versions.md`. Copy them over your desk from lesson 14.2 |

Our proposal, our ledger and our report come from our desk's journal. Yours will propose something else, and that's fine:
the method is what you keep.

## Before you start

- Your `~/trading-desk` with the heartbeat and ledger from Module 11, the skills from 12.2, the guardrails from 12.3,
  the memory budget from 13.3, and the lesson tracker from 14.2.
- Claude Code in the terminal, signed in with your subscription.
- Obsidian, with the desk's `vault/` folder open as a vault.
- Time on our computer: about 4 minutes for Claude to build the tool and the first proposal, under a minute each for the
  approval and the tests, and about 3 minutes for the report and the ledger fix.

## Try it yourself

1. Send request 1 in `prompts.md`, read the proposal, and approve it only if its evidence holds.
2. Ask for the report (request 3) and open it in Obsidian.
3. Decide yourself whether the ledger should be corrected.

You're done when your ledger has a new trader version, and the report explains every row. Your code, numbers and Claude's
answers will differ from the video, and that's fine.

## Good to know

- **Approval mode stays on.** A proposal that passes every check still waits for a person.
- **Out of reach.** A proposal may change only skills and the playbook. `CLAUDE.md`, the risk limits, the guardrail hook,
  the settings and the desk's code (including the review gate from lesson 14.1) are refused.
- **New instructions, new version.** Any change to what the trader reads changes the instructions hash, and the heartbeat
  starts a new session. The ledger row keeps results tied to the version that produced them.
- **Not run yet.** Version 2.2 had no bars when we filmed. Its success test needs a real trading session, on paper.

Paper account only. Educational content, not financial advice; nothing here is a promise of profit or a recommendation.
