# Student kit: Lesson 9.4, Don't let the AI cheat

Module 9: The strategy factory: goal-driven research loops · AI Algorithmic Trading with Claude Code and Interactive Brokers

An agent told to find a strategy that passes the judge has three shortcuts (Goodhart's law): loosen the judge, peek at
data it should never tune on, or undercount its attempts. In this lesson we close all three:

1. **A lock on the judge.** Deny rules in `.claude/settings.json` plus a PreToolUse hook, `.claude/hooks/judge_guard.py`,
   that blocks any edit of `judge/`, grading against another `--standards` file, and any read of `data/holdout/`. The
   lock also covers itself (the settings files and the hook). Claude proved it: three ways to lower `min_trades` and
   three ways to read the holdout, all refused.
2. **A holdout.** The last six months of QQQ and SPY bars (from 2026-04-22) moved from `data/cache/` to
   `data/holdout/`. The downloader now sends new bars from that date on into the holdout.
3. **A record.** A trial ledger (`research/trials.csv`) and an audit log (`research/audit_log.jsonl`) written by the
   judge itself. Claude couldn't edit the judge, so it delivered the change as a patch; we reviewed it in VS Code and
   applied it ourselves. Then a rerun from the audit log matched all 8 rules and did not add a trial.

The hook is a guardrail, not a sandbox: it reads the command text, so code that builds a path while it runs gets past
it. For a hard boundary, make the files read-only at the operating system level or turn on Claude Code's sandbox.

## What's in this kit

The files are the Lab as it was at the end of the lesson, with the patch already applied.

| File | What it is |
|---|---|
| `prompts.md` | The three requests typed in the lesson, the shell-mode commands to review and apply the patch, commands to try the locks by hand, and the pause-and-try exercise |
| `cheat-sheet.md` | The words, three shortcuts and three defenses, how a PreToolUse hook works, what a deny rule covers and what it doesn't, the judge after the patch, known limits |
| `trading-lab/.claude/settings.json` | The Lab's settings: `judge_guard.py` registered as a PreToolUse hook next to the port guard, the deny rules, the ask rule for `rm` |
| `trading-lab/.claude/hooks/judge_guard.py` | The hook (201 lines after the patch): exit code 2 and a clear reason when a command would change the judge, the lock or the two records, or touch the holdout |
| `trading-lab/tests/test_judge_guard.py` | Runs the real hook against a throwaway project (80 cases in the lesson, more after the patch) |
| `trading-lab/judge/scorecard.py` | The judge with the trial ledger, the tamper check and the audit log (from the patch) |
| `trading-lab/tests/test_trial_ledger.py` | Tests for the ledger, the trial count, the tamper check and the audit line, including a crashed run |
| `trading-lab/research/patches/0001-judge-trial-ledger-and-audit-log.patch` | The patch exactly as Claude delivered it, to read and review. It is already applied in this kit's files: don't apply it again |
| `trading-lab/backtests/walk_forward.py`, `tests/test_walk_forward_windows.py` | The fix for the bug the holdout caused: walk-forward windows end where the data ends (24 months: 9 windows; 18 months: 6) |
| `trading-lab/data_pipeline/` (`config.py`, `downloader.py`, `cache.py`, `__main__.py`), `tests/test_data_pipeline.py` | The downloader that routes QQQ and SPY bars from `HOLDOUT_START` on into `data/holdout/`, and its tests |

Also add these lines to the Lab's `.gitignore` (Claude did in the lesson), so the holdout never goes to GitHub:

```text
# Last six months of QQQ and SPY bars, locked away from research (.claude/hooks/judge_guard.py)
data/holdout/
```

Claude also added an entry for `data/holdout/` and a "Locked files" entry to `AGENTS.md`, and described the ledger and
the audit log in the judge's entry. `research/trials.csv` and `research/audit_log.jsonl` are not in the kit: the judge
creates them on its first run. Commit them after runs. No new dependency.

## Before you start

- The Trading Lab with the judge (`judge/scorecard.py`, `judge/standards.yaml`, Lesson 8.4), the commit hook and the
  port guard (Lesson 3.6), and the research setup from Lessons 9.1 to 9.3.
- Up to 24 months of QQQ and SPY 5-minute bars in `data/cache/` (the data pipeline from Lesson 5.1). The holdout split leaves
  about 18 months for research.
- Claude Code in the terminal, signed in with your subscription, in auto mode.
- No IB connection is needed for anything in this lesson.
- Time on our computer: about 5 minutes for the lock and the proof, about 9 minutes for the downloader, the bug fix and
  the patch, about 1 minute for the checks after applying it, about 2 minutes for the rerun.

## Try it yourself

1. `/clear`, then send the first request in `prompts.md`. Before you trust the lock, read the deny rules and the hook's
   docstring. Watch both attacks get refused.
2. Send the second request in the same session. Read the patch in your editor (`Ctrl+P`, the file name; `Ctrl+G`, a
   line number). Preview it with `! git apply --stat ...`, then apply it with `! git apply ... && uv run pytest -q`.
   The `!` makes it your own command: Claude can't apply it, you can.
3. Send the third request: reproduce a judge run from its audit line.

You're done when an edit to the judge is refused, the holdout can't be read, and a rerun from the audit log matches
every rule without adding a trial. Your numbers and Claude's replies will differ from the video; the behaviour is what
matters.

## Good to know

- Deny rules on `Read` and `Edit` cover Claude's file tools and simple file commands in Bash (`cat`, `head`, `tail`,
  `sed`, `tee`, redirects), but not a program that opens the file by itself, like a Python one-liner. The hook adds
  that, by reading the command text.
- Lock the lock: without deny rules on the settings files and the hook itself, one edit would remove the whole lock.
  That's why Claude wrote `settings.json` last.
- The hook also blocks some harmless commands (it read `sed`, `cut`, an `echo` ending in "judge" as changes). Those are
  false positives from the command text, not misses. Claude reads the reason and switches to an allowed command.
- The holdout had side effects: research now has about 18 months of bars, so older strategy cards won't reproduce
  exactly, and the walk-forward code crashed until its windows followed the data. Claude found that bug itself, after
  saying it should have run the judge in its first turn.
- In this kit `--trials` can only raise the count: the judge uses the larger of your claim and the distinct settings in
  the ledger. A low claim like `--trials 5` still beats the default guess of 100; making 100 a floor too is a one-line
  change in `effective_trials`.
- The audit log doesn't record the data. A hash of the data file in each line would close that gap (a second patch
  Claude offered).
- Back up `data/holdout/`: it's gitignored, so the bars exist only on your computer.

## Safety

Paper trading only. Educational content, not financial advice. Nothing in this lesson connects to a broker or places
an order. The strategy in the demo failed the judge (3 of 8 rules); nothing here is a recommendation or a promise of
profit.
