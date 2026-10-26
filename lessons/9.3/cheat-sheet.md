# Lesson 9.3 cheat sheet: Building your own loops

## The words

| Word | Meaning |
|---|---|
| **Stop hook** | A script Claude Code runs every time Claude wants to finish. Exit code 2 blocks the finish, and what the script printed goes to Claude as the reason |
| **stop_hook_active** | A field in the hook's input: `true` when Claude is already continuing because a Stop hook blocked it |
| **Block cap** | The most times a hook may block in a row, so a loop always ends (the research gate: 5) |
| **Headless** | `claude -p "..."` runs one task with no chat window, prints the result and exits |
| **Batch loop** | A shell script that runs many headless tasks one after another, each in a fresh session |
| **Done marker** | A file that says "this idea is finished" (`research/batch_logs/<id>.json`), so a rerun skips it |

## Three ways to loop

| | `/goal` (Lesson 9.2) | Your own Stop hook | Headless batch |
|---|---|---|---|
| What checks "done"? | A small model reads the conversation | Your code (it can read files, run checks) | Your script reads each run's JSON |
| Sessions | One | One | A fresh one per idea |
| Budget | In the condition ("stop after 30 turns") | The block cap | `--max-turns` per session + a total time budget |
| Best for | Quick goals in plain words | Exact, repeatable checks | Long, unattended runs; survives usage limits |

## How a Stop hook works

1. Claude finishes a turn and wants to stop. Claude Code runs every Stop hook in `.claude/settings.json` (not when you
   interrupt it).
2. Exit 0: the stop is allowed. Exit 2: the stop is blocked; the hook's stderr is the reason Claude reads next.
   (JSON alternative: `{"decision": "block", "reason": "..."}`.)
3. The input has `stop_hook_active`. Use it, or a counter, so a check that never passes can't loop forever.
4. Claude Code has its own cap on stop-hook continuations, but it resets each time Claude uses a tool. Add your own.
5. The terminal shows a block as "Stop hook error": that is the label, not a crash.

## The research gate (`.claude/hooks/research_gate.py`)

- No `research/goals/ACTIVE`: does nothing (and clears the counter).
- `ACTIVE` names a goal file; its `## Required files` list must exist.
- Missing files: exit 2, "Goal <name> is not done (block N of 5). Create these missing files before you stop:" + list.
- Counter `.claude/research_gate.count` (gitignored): counts up on continuations, resets on a new stop, a passing gate
  or a missing `ACTIVE`; after 5 blocks in a row it gives up and lets Claude stop.
- A bad `ACTIVE` or a goal without the list: a non-blocking error (exit 1), not a silent pass.
- Turn it on: `echo research/goals/<goal>.md > research/goals/ACTIVE`. Turn it off: remove `ACTIVE`.

## The batch script (`scripts/research_batch.sh`)

| Flag | Default | What it does |
|---|---|---|
| `--dry-run` | off | Shows the plan and the commands; calls nothing, writes nothing |
| `--plan-only` | off | Blocks Bash, Edit and Write; pastes the journal row into the prompt; the answer is a test plan |
| `--max-turns N` | 40 | Turn cap for each session |
| `--budget-minutes N` | 240 | Total time budget; each call's `timeout` is what is left |
| `--max-ideas N` | all | Run at most N ideas this time |
| `--only ID` | | Run just this idea, even if it has a done marker |

Exit codes: 0 finished (or time budget used), 1 setup error, 75 stopped on usage-limit wording (rerun after the
reset), 130 interrupted. Files per idea in `research/batch_logs/` (gitignored): `<id>.log`, `<id>.json` (the done
marker, only on `subtype` success and `is_error` false), `<id>.error.json` (the last failed attempt).

## What was tested, and what wasn't

| Tested in the lesson | Not tested |
|---|---|
| The hook blocked a real stop twice (block 1 and 2 of 5) | The release in a real stop with the gate still active (checked by running the hook by hand) |
| 11 hook tests pass | The Lab's full test suite (not run) |
| The dry run lists 7 untested ideas, skips failed and parked ones | The usage-limit stop (a phrase match; no real limit was hit) |
| One plan-only call on H3: 1 turn, 18 seconds, done marker written | Full mode (build, judge, card, journal) |
| A rerun skips H3 because of the done marker | |

## Lessons the run taught

- A headless session runs your project's hooks too. Commit before the batch, or the commit hook adds a turn.
- `--max-turns 3` is tight: a session that reads files first can run out. Put what it needs in the prompt.
- Ask rules (`Bash(rm:*)`) beat auto mode: a delete waits for a person.
- `total_cost_usd` in the JSON is the CLI's estimate, not a bill.
- Trust what was tested, not what was planned.
