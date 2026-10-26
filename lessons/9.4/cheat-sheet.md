# Lesson 9.4 cheat sheet: Don't let the AI cheat

## The words

| Word | Meaning |
|---|---|
| **Goodhart's law** | When a measure becomes a target, it stops being a good measure. An agent rewarded for passing the judge is rewarded for the number, not for an edge |
| **Rule** | A request in `CLAUDE.md` or `AGENTS.md` ("don't touch the judge"). Claude usually follows it; nothing enforces it |
| **Lock** | Something Claude Code itself enforces: a deny rule or a hook |
| **Deny rule** | `permissions.deny` in `.claude/settings.json`, for example `Edit(./judge/**)`. Claude Code refuses a matching tool call, whatever Claude wants |
| **PreToolUse hook** | A script Claude Code runs before every matching tool call. Exit code 2 blocks the call; what it prints to stderr goes to Claude as the reason |
| **Holdout** | Data kept out of research (here `data/holdout/`, the last six months of QQQ and SPY bars), saved for one final check |
| **Trial ledger** | `research/trials.csv`: the judge writes a row for every setting it scores, before the backtests run. The trial count comes from this file, not from you |
| **Audit log** | `research/audit_log.jsonl`: one line per judge run, crashed or finished, with the time, commit, dirty flag, command, settings, seeds, standards hash, trial counts and the result per rule |
| **Patch** | A file of changes (`git diff` output) that a human reviews and applies with `git apply` |

## Three shortcuts, three defenses

| Shortcut an agent can take | Defense in the Lab |
|---|---|
| Loosen the judge (edit `standards.yaml`, edit the code, grade against a weaker `--standards` file) | Deny rules on `judge/**` and the lock files + `judge_guard.py` (blocks edits, `sed -i`, redirects, `--standards <other file>`) |
| Peek at data it should never tune on | `data/holdout/` with `Read` and `Edit` deny rules + the hook (blocks `cat`, a pandas one-liner, `Grep`/`Glob` into it) |
| Undercount its attempts so the Deflated Sharpe forgives more luck | The trial ledger: the count used is the larger of `--trials` and the distinct (symbol, settings) rows in the ledger |

## How a PreToolUse hook works

1. Claude asks to use a tool (Bash, Edit, Write, Read...). Claude Code runs every PreToolUse hook whose `matcher` fits the
   tool name (`judge_guard.py`: `Bash|Edit|Write|NotebookEdit|Read|Grep|Glob`).
2. The hook reads JSON on stdin: `tool_name`, `tool_input` (the command or the file path), `cwd`.
3. Exit 0: the call goes on to the normal permission checks. Exit 2: the call is blocked and the hook's stderr is the
   reason Claude reads ("PreToolUse:Bash hook error: [...]: Blocked by judge_guard: ...").
4. A deny rule still applies whatever a hook returns. Deny rules are checked first, then ask rules, then allow rules.

## What a deny rule covers, and what it doesn't

- `Read` and `Edit` deny rules cover Claude's file tools and the simple file commands Claude Code recognizes in Bash
  (`cat`, `head`, `tail`, `sed`, `tee`, redirects).
- They don't cover a program that opens the file by itself, such as a Python one-liner. That's why the Lab adds the
  hook, which reads the command text.
- The hook is a text matcher: a path built while the code runs (`'ju' + 'dge'`) gets past it. It stops mistakes and an
  agent pushing too hard. It is **not** a security boundary. For that, make `judge/`, `research/trials.csv` and
  `research/audit_log.jsonl` read-only at the operating system level, or turn on Claude Code's sandbox.
- Lock the lock: deny `Edit` on `.claude/settings.json`, `.claude/settings.local.json` and the hook itself, or one edit
  removes the whole lock. Claude wired up `settings.json` last for that reason.

## The judge after the patch (`judge/scorecard.py`)

- Every run writes a ledger row first, so a crashed or abandoned run still counts.
- Deflated Sharpe trial count = max(`--trials` or the assumed 100, distinct (symbol, settings) rows for that strategy).
  The note under rule 7 says where it came from: `claimed`, `assumed` or `ledger`.
- Rerunning identical settings is on the record but not a new trial.
- Tamper check: the judge refuses to run if `trials.csv` has fewer rows than the committed copy. Commit it often.
- The audit line holds `standards_sha256`, so a run against a loosened standards file shows up.

## Known limits (as Claude reported them)

- A low `--trials` still beats the default: `--trials 5` gives 5, not the assumed 100. The ledger only overrides a claim
  lower than the ledger count (making the assumed 100 a floor too is a one-line change in `effective_trials`).
- The ledger starts empty: grid and Optuna searches that ran outside the judge still depend on an honest `--trials`.
- Uncommitted ledger rows can be deleted unnoticed.
- The audit line records the command as a file path, not the `-m` form.
- The audit log doesn't record the data: a bar update between two runs would change results with nothing in the log to
  explain it. A hash of the data file per line would fix that (a second patch).
- The hook blocks some harmless commands (false positives): `sed` and `cut` reads of the judge or the records (not on its
  read-only list), an `echo` whose text ends in the word "judge", a Python snippet that opens the audit log by path. Use
  `head`, `tail`, `cat`, `grep` or `wc`, or add `cut`, `sed -n` or `awk` to `READ_ONLY` in the hook by hand.
- The hook matches file names, not which copy of the project they're in: it also blocked Claude editing a throwaway copy
  of the hook. The lock guards this project, not every copy of it.

## Side effects of the holdout

- Research now has about 18 months of bars (the cache ends 2026-04-21), not 24: older strategy cards won't reproduce
  exactly.
- `backtests/walk_forward.py` used to assume 24 months; with 18 the last windows were empty and the judge crashed.
  Fixed: the windows end at the data (24 months: 9 windows; 18 months: 6).
- The downloader sends QQQ and SPY bars from `HOLDOUT_START` (`data_pipeline/config.py`) on into `data/holdout/`, and
  counts them as already downloaded. Moving the cutoff is a human decision.
- `data/cache/` and `data/holdout/` are gitignored: the holdout bars exist only on your computer. Back them up.
