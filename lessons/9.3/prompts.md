# Lesson 9.3 prompts and commands

Everything typed in the lesson, in order. Lines that start with `!` run in the terminal from inside Claude Code
(shell mode). Lines that start with `/` are Claude Code commands. Every request runs in auto mode. Nothing here needs an
IB connection.

## 1. A Stop hook of your own

```text
/clear
```

```text
Let's build our own loop with a Stop hook. Add .claude/hooks/research_gate.py: when a file research/goals/ACTIVE exists, it names a goal file whose done-condition is a list of files that must exist. If any are missing, block the stop and tell Claude which ones. Respect stop_hook_active, allow at most 5 blocks in a row with a counter file, and do nothing when ACTIVE does not exist. Register it next to our commit hook, add tests, then prove it on a tiny goal: two small notes in research/notes/. Show me the hook blocking and then letting you stop, and commit.
```

In the video, Claude read the existing hooks and settings first, noticed that the commit hook blocks on a dirty tree
(so the counter file must be gitignored) and lets Claude stop as soon as `stop_hook_active` is set (which would end a
loop after one block), wrote the hook (113 lines), registered it after `require_commit.py`, added 11 tests (pass) and
committed. Then the demo: it tried to stop and was blocked ("block 1 of 5", both notes missing), wrote one note, was
blocked again ("block 2 of 5", one note missing), wrote the second note, checked the release by running the hook by
hand (exit 0), and committed with `ACTIVE` removed. About 1 minute 10 seconds.

Try the hook by hand (from the Lab folder, in a terminal):

```text
! echo research/goals/tiny_notes.md > research/goals/ACTIVE
! mv research/notes/slippage.md /tmp/slippage.md
! echo '{"stop_hook_active": false}' | CLAUDE_PROJECT_DIR=$PWD python3 .claude/hooks/research_gate.py; echo "exit=$?"
! mv /tmp/slippage.md research/notes/slippage.md
! echo '{"stop_hook_active": true}' | CLAUDE_PROJECT_DIR=$PWD python3 .claude/hooks/research_gate.py; echo "exit=$?"
! mv research/goals/ACTIVE /tmp/ACTIVE.off
```

The first run prints "block 1 of 5" with the missing note and `exit=2`; the second prints nothing and `exit=0`. The
last line switches the gate off again (moving `ACTIVE` out of the way), so your next session isn't blocked. Run the
tests:

```text
! uv run pytest tests/test_research_gate.py -q
```

## 2. A headless batch

```text
/clear
```

```text
Now the headless version for long runs. Write scripts/research_batch.sh that loops over the untested ideas in research/journal.md and runs one fresh claude -p session per idea with JSON output, --max-turns, a total time budget, a log file per idea, and a clean stop when the usage limit is hit, so I can rerun it after the reset and it skips what is done. Add a --dry-run flag. Run the dry run, then one real call on the next idea with --max-turns 3 that only writes a test plan, not code, and show me the log.
```

In the video, Claude checked that `--max-turns` works with a one-word test call, wrote the script, and ran the dry run
(7 untested ideas: H3, A, B, G, D, C, E; H1 and H2 skipped as failed, F and S as parked). The first real call failed
with `error_max_turns` (the session spent its 3 turns reading files), so plan-only mode now pastes the journal row into
the prompt. The next call worked, but the uncommitted script made the commit hook force one more turn, and that turn's
answer replaced the plan in the log; Claude committed the script and reran H3: 1 turn, 18 seconds. The command's `rm`
stopped for approval because of the ask rule `Bash(rm:*)`; we approved it. About 3 minutes.

Run it yourself (commit first, so the commit hook doesn't add a turn):

```text
! scripts/research_batch.sh --dry-run
! scripts/research_batch.sh --plan-only --max-turns 3 --max-ideas 1
! cat research/batch_logs/H3.log
! scripts/research_batch.sh --dry-run --plan-only --max-ideas 1
```

The last dry run should skip the idea you just ran ("done marker research/batch_logs/<id>.json"). Use `--only <id>` to
rerun one idea on purpose. Don't start the full mode (no `--plan-only`) until you have read the script's full-mode
prompt and are ready for a long run: it builds, judges and commits, and it was not run in this lesson.

## Pause and try

1. Build the research gate (request 1) and prove it on a tiny goal of your own: two or three short notes about terms
   from the course.
2. Write the batch script (request 2), run the dry run, and read the list before any real call.
3. Run one plan-only call and read its log: header, command, result line, then the plan.

You're done when the hook blocks a stop with a clear list of missing files, your dry run lists your untested ideas,
and one log ends with `subtype=success`. Your ideas, numbers and replies will differ from the video, and that's fine.
This is paper research, not a strategy to trade.

## Try next (optional)

- Lower `MAX_BLOCKS` to 2 in a copy of the hook and watch the counter give up ("giving up after 2 blocks in a row").
- Ask Claude for the "block on first sight" version it offered, and compare the two in the tests.
- Run two plan-only calls (`--max-ideas 2`) and compare the plans: did each fresh session start from the journal row
  alone?
