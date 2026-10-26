# Student kit: Lesson 9.3, Building your own loops

Module 9: The strategy factory: goal-driven research loops · AI Algorithmic Trading with Claude Code and Interactive Brokers

In Lesson 9.2, `/goal` kept Claude working until a condition was met. `/goal` is a built-in Stop hook. In this lesson
we build the other two kinds of loop ourselves:

1. **A Stop hook of our own.** Claude writes `.claude/hooks/research_gate.py`: when `research/goals/ACTIVE` exists, it
   names a goal file whose "Required files" list must exist before Claude may stop. Missing files block the stop
   (exit code 2) and are listed for Claude; a counter allows at most 5 blocks in a row. Claude registers it next to the
   commit hook, adds 11 tests, and proves it on a tiny goal (two short notes): the hook blocked the stop twice in the
   live session, and the release was checked by running the hook by hand.
2. **A headless batch.** Claude writes `scripts/research_batch.sh`: one fresh `claude -p` session per untested idea in
   the research journal, with JSON output, `--max-turns`, a total time budget, a log and a done marker per idea, and a
   clean stop (exit 75) when a session fails with usage-limit wording. A dry run lists the ideas; one plan-only call on
   idea H3 wrote a test plan in 1 turn and 18 seconds. The usage-limit stop and the full mode were not tested, and
   Claude says so.

## What's in this kit

| File | What it is |
|---|---|
| `prompts.md` | The two requests typed in the lesson, the commands to try the hook and the batch yourself, and the pause-and-try exercise |
| `cheat-sheet.md` | The words, how a Stop hook works, the batch script's flags and files, what was and wasn't tested, and which loop to use when |
| `trading-lab/.claude/hooks/research_gate.py` | The Stop hook (113 lines): does nothing without `research/goals/ACTIVE`; blocks with exit code 2 and the list of missing files; counter in `.claude/research_gate.count`, at most 5 blocks in a row |
| `trading-lab/.claude/settings.json` | The Lab's settings with `research_gate.py` registered as a second Stop hook, after `require_commit.py` |
| `trading-lab/tests/test_research_gate.py` | 11 tests that run the real hook against a throwaway project folder |
| `trading-lab/research/goals/tiny_notes.md` | The demo goal: two notes, with a `## Required files` list |
| `trading-lab/research/notes/stop_order.md`, `slippage.md` | The two notes Claude wrote to satisfy the demo goal |
| `trading-lab/scripts/research_batch.sh` | The headless batch script (`--dry-run`, `--plan-only`, `--max-turns`, `--budget-minutes`, `--max-ideas`, `--only`) |

Also add these lines to the Lab's `.gitignore` (Claude did in the lesson):

```text
# Research batch logs and done markers (scripts/research_batch.sh)
research/batch_logs/
.claude/research_gate.count
```

`research/goals/ACTIVE` is not in the kit: Claude removed it in its last commit so the gate is off. Create it only
while you want the gate on (see `prompts.md`). Nothing else in the Lab changed; no new dependency.

## Before you start

- The Trading Lab with the commit hook `.claude/hooks/require_commit.py` and the port guard
  `.claude/hooks/block_live_ports.py` (both from Lesson 3.6), and the research journal `research/journal.md`
  (Lesson 9.1, with H1 and H2 filled in by Lessons 9.1 and 9.2).
- Claude Code in the terminal, signed in with your subscription. `claude -p` uses the same sign-in.
- No IB connection is needed: the hook demo writes notes, and the plan-only batch call only reads.
- Time on our computer: about 1 minute 10 seconds for Claude to build and prove the hook, about 3 minutes for the batch
  script, the dry run and the plan-only call.

## Try it yourself

1. `/clear`, then send the first request in `prompts.md`. Read the hook before you trust it: what does it do when
   `ACTIVE` is missing, and what happens after 5 blocks in a row?
2. Watch the demo: Claude tries to stop, the hook blocks and names the missing notes, Claude writes them.
3. `/clear`, then send the second request. Read the dry run's list before any real call.
4. Open the log of the plan-only call in `research/batch_logs/` and read it like a lab notebook: the header, the
   command, the result line, then the plan.

You're done when the hook blocks a stop with a clear list of missing files, your dry run lists your untested ideas,
and one log ends with `subtype=success`. Your ideas, numbers and Claude's replies will differ from the video; the
behaviour is what matters.

## Good to know

- `stop_hook_active` is `true` when Claude is already continuing because a Stop hook blocked it. The gate uses it to
  tell a continuation (count up) from a new stop (reset). Claude Code has its own cap on stop-hook continuations, but
  it resets whenever Claude uses a tool, so a hook that lets Claude work between blocks needs its own cap.
- Claude flagged one decision for you: `require_commit.py` lets Claude stop as soon as `stop_hook_active` is set, which
  would end any loop after one block. The gate counts instead. A "block on first sight" version is a small change if
  you prefer it.
- A headless session still runs your project's hooks. In the lesson the script was not yet committed, so the commit
  hook forced one more turn and that turn's answer replaced the plan in the log. Commit before you run the batch.
- The first real call failed with `error_max_turns`: the session spent its 3 turns reading files. In plan-only mode the
  script now pastes the journal row into the prompt, so no reads are needed. The script did the right thing with the
  failure: no done marker, and the loop went on.
- The `rm` in Claude's command stopped for approval even in auto mode, because the Lab's settings have the ask rule
  `Bash(rm:*)`. Ask rules beat auto mode.
- The cost figure in the JSON (`total_cost_usd`, about $0.08 for the plan-only call) is the CLI's own estimate, not a
  bill; on a subscription, `claude -p` runs on your plan's usage.
- Untested, as Claude reported: the usage-limit stop (a phrase match on the error output, exit 75; no real limit was
  hit) and the full mode (build, judge, card, journal). Treat both as unproven until you see them work.

## Safety

Paper trading only. Educational content, not financial advice. Nothing in this lesson connects to a broker or places
an order; the batch's full mode allows only the paper IB Gateway port 4002 and keeps the port guard hook on. The H3
test plan is a plan, not a result, and nothing here is a recommendation or a promise of profit.
