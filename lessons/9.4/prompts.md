# Lesson 9.4 prompts and commands

Everything typed in the lesson, in order. Lines that start with `!` run in the terminal from inside Claude Code
(shell mode: your own shell command, not a request to Claude). Lines that start with `/` are Claude Code commands.
Every request runs in auto mode. Nothing here needs an IB connection.

## 1. Lock the judge

```text
/clear
```

```text
Goodhart's law: if I tell an agent to find profit, it will bend the rules if it can. Right now nothing stops you from editing judge/standards.yaml or the judge code. Lock it. Add deny rules for judge/ and for a holdout folder, and a PreToolUse hook judge_guard.py that blocks any Edit, Write or Bash command that would change the judge or read data/holdout/, with a clear message. Move the last six months of QQQ and SPY bars into data/holdout/ so research never sees them. Add tests, commit, then prove it: try to lower a threshold in standards.yaml and try to read the holdout, and show me both blocks.
```

In the video, Claude read the settings, the hooks and the cache, split both 5-minute files at 2026-04-22 (six months
before the last bar: 29,070 bars stay in `data/cache/`, 9,906 move to `data/holdout/` for each of QQQ and SPY; the small
SPY 1-minute file moved whole), wrote `.claude/hooks/judge_guard.py` (165 lines) and 80 tests (pass), updated
`.gitignore` and `AGENTS.md`, and wired up `.claude/settings.json` last, because after that it can't edit it. The full
suite passed (274) and it committed. Then the proof: lowering `min_trades` from 200 to 20 with the Edit tool (refused
by the deny rule), with `sed -i` (blocked by the hook) and by grading against a weaker copy with
`--standards /tmp/weak.yaml` (blocked by the hook); reading the holdout with the Read tool (deny rule), `cat` and a
pandas one-liner (both blocked by the hook). About 5 minutes.

## 2. The trial ledger and the audit log, as a patch

Same session, no `/clear`: Claude keeps the lock in mind and answers its own open question (the downloader).

```text
Yes, make the downloader send bars from the cutoff onward into data/holdout/. Now the quieter way to cheat: --trials is just a number I type, so a run can claim fewer attempts than it really made and the Deflated Sharpe looks better. The judge should keep its own trial ledger in research/trials.csv and count trials from it, so --trials can only raise the count, never lower it. Every judge run should also append one line to research/audit_log.jsonl with the time, git commit, command, settings, seed and result. You can't edit the judge, so put the judge change, its tests and your hook fix into one patch file in research/patches/, explain what it changes, and give me the exact command to apply it. I'll review it and apply it myself.
```

In the video this took about 9 minutes, with four permission prompts, all approved. Each command removed files in a
throwaway copy of the Lab (the ask rule `Bash(rm:*)` overrides auto mode), and changed folder before a `git` command or
used a variable Claude Code can't check before it runs. Claude also found and fixed a bug from its own first turn: with
six months held out, the walk-forward code still assumed 24 months and the judge crashed.

Review the patch before you apply it. In VS Code: `Ctrl+P`, type `0001-judge-trial-ledger`, Enter; `Ctrl+G` jumps to a
line. Then, in Claude Code:

```text
! git apply --stat research/patches/0001-judge-trial-ledger-and-audit-log.patch
! git apply research/patches/0001-judge-trial-ledger-and-audit-log.patch && uv run pytest -q 2>&1 | tail -3
```

The first line only previews (6 files, 328 insertions, 16 deletions in the video). The second applies the patch and
runs the full suite (320 passed in the video). Then tell Claude it's applied: it checked the guard fix, ran the judge
for real, showed that its own append to `research/trials.csv` is blocked, and committed.

## 3. Reproduce a result from the audit log

```text
Good. Now reproduce that donchian run from the audit log alone: read the line, rebuild the exact command and settings from it, run it again, and show me side by side that every rule's result matches. Then tell me whether the rerun added a new trial to the ledger.
```

In the video all 8 rules matched (405 trades, Sharpe after costs 0.39, Deflated Sharpe 35.7%, verdict FAIL 3 of 8),
and the rerun added a ledger row but not a new trial (distinct count still 1). Our commit hook then asked for a commit
and push.

Try the locks by hand (from the Lab folder; each of these should be refused when Claude runs it, and the tests prove
it without Claude):

```text
! uv run pytest tests/test_judge_guard.py tests/test_trial_ledger.py tests/test_walk_forward_windows.py -q
! tail -n 1 research/audit_log.jsonl
! uv run -m judge.scorecard donchian_breakout --symbol SPY 2>&1 | tail -14
! wc -l research/trials.csv
```

Run the judge twice with the same settings: `trials.csv` gains a row each time, but the "ledger" count in the audit line
stays the same. Commit the ledger after runs: the judge only notices deleted rows against the committed copy.

## Pause and try

1. Lock your judge (request 1). Read the deny rules in `.claude/settings.json` and the hook's docstring before you
   trust them, then watch both attacks get refused.
2. Ask for the ledger and the audit log as a patch (request 2). Review it in your editor, preview it with
   `git apply --stat`, and apply it yourself.
3. Reproduce one judge run from its audit line (request 3).

You're done when an edit to the judge is refused, the holdout can't be read, and a rerun from the audit log matches
every rule without adding a trial. Your numbers will differ from the video, and that's fine. This is paper research,
not a strategy to trade.

## Try next (optional)

- Ask Claude for the second patch it offered: a hash of the data file in each audit line, so a changed bar shows up.
- Make `judge/` and the two record files read-only for your user at the operating system level, or turn on Claude
  Code's sandbox, and see what the hook no longer needs to catch.
- Add `cut`, `sed -n` or `awk` to the hook's read-only list by hand (Claude can't), and rerun its tests.
