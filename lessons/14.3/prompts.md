# Lesson 14.3 prompts

Everything typed in the lesson, in order. Lines that start with `/` are Claude Code commands. One interactive Claude Code
session in `~/trading-desk` (auto mode), with Obsidian open on the desk's vault beside it. Paper account only.

## 1. Ask for one proposal

```text
/clear
```

```text
Let the desk improve its own playbook and skills, safely. Each change is proposed as a patch in proposals/ with the reason and the evidence from the lesson tracker. Then run the checks: tests, memory budget, risk files untouched. Apply it only if they pass and, when approval mode is on, only after I approve it. Each applied change is a commit and a new trader version in the ledger. Approval mode is on by default. Make one proposal from what we have now and show me.
```

On our computer Claude worked for 4 minutes. It found no proposal system and no lesson data yet (0 closed trades), so it
used the journal: under the current instructions (v2.1) the `market-read` skill was loaded on 1 of 55 bars. The guardrail
hook from lesson 12.3 blocked two shell commands because their text named guarded files, so Claude switched to the Write
tool and touched no guarded file. It wrote proposal 0001 (`proposals/0001-market-read-load-first.patch` and `.md`) and the
tool `desk/proposals.py`. The checks found one flaw in its own checker (a test reads the folder name) and one real problem
in the proposal (every skill description must start with "Use "), which it reworded. Then it confirmed that approval mode
blocks the apply: "checks passed, but approval mode is ON: a person must approve".

## 2. Approve

```text
First commit the proposal system itself. Then: approve.
```

The tool went in as its own commit, then `apply 0001 --approved` ran every check again (299 of 299 tests, memory budget
1,796 of 6,000 tokens, the limits file still matches its pin), applied the one-line change and committed it. The ledger
gained a row, `Trader v2.2 (proposal 0001)`, with a new instructions hash. To roll back: `git revert` that commit. Claude
named two small flaws: the commit subject repeated the id, and the tool had no tests.

```text
Yes, fix the doubled commit subject and add tests for desk/proposals.py, then commit.
```

Six new tests in `tests/test_proposals.py`; 305 of 305 pass.

## 3. What changed, and why

```text
Write the what-changed-and-why report across all trader versions so far, from the ledger and git history, as a note in the vault. Check that every change to the trader's instructions has its ledger row, and say plainly if one is missing.
```

Claude recomputed the instructions hash at every commit that touched the trader's instructions and compared it with the
ledger. The ledger was not complete: the lessons-key change from lesson 14.2 had no row. It also found five early bars on
instructions the ledger never lists, a start date off by a day, and empty end dates. It did not edit the ledger on its
own: "Adding a row ... rewrites the record of what was run, so I left that to you."

```text
Fix the ledger: add the missing row and the end dates, keep the old values visible in the notes column, and commit it with the note.
```

The ledger fix and the report (`vault/Versions/Trader versions.md`) went in as one commit. Claude also corrected one of
its own earlier claims: the v2.2 ledger note never had the doubled id; only the commit subject did.

## Pause and try

1. Ask Claude for a proposal tool like ours, with the checks, and approval mode on.
2. Let it make one proposal from your own journal, read its evidence, and approve it only if the evidence holds.
3. Ask for the what-changed-and-why report, and check that every change has its ledger row.

You're done when your ledger has a new trader version, and the report explains every row.
