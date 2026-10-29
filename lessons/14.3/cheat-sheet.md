# Lesson 14.3 cheat sheet: an agent that rewrites its own playbook

## Words

| Word | Meaning |
|---|---|
| Self-modification | The agent changing its own instructions (its skills, its playbook) |
| Proposal | A suggested change, waiting for its checks and a person's approval: a patch plus a note with the reason and the evidence |
| Trader version | A row in `experiments/ledger.csv`. A new one every time the instructions hash changes |
| Instructions hash | A 12-character fingerprint of the exact text the trader reads (`CLAUDE.md`, the plugin manifest, every skill file). Any edit changes it |
| Approval mode | On by default: a proposal that passes every check still waits for `--approved` |

## The pipeline

A reason (the journal, or a lesson from the lesson tracker) -> a proposal (patch + note) -> automatic checks -> a person
approves -> a commit and a new trader version in the ledger.

## What a proposal may change (our desk)

| May change | Refused |
|---|---|
| `.claude/skills/<name>/SKILL.md` | `CLAUDE.md` (the constitution and its risk rules) |
| `vault/Playbook/*.md` | `.claude/settings*`, `.mcp.json`, `.claude-plugin/` |
| | The desk's code: `desk/hook.py`, `gates.py`, `seatbelts.py`, `limits_pin.py`, `execute.py` ... and every other file outside skills and the playbook |
| | `desk/limits.sha256`, `vault/Rules/` |

## The tool: `desk/proposals.py`

| Command | What it does |
|---|---|
| `uv run -m desk.proposals check 0001` | Runs the checks and prints PASS or FAIL for each |
| `uv run -m desk.proposals apply 0001` | Runs the checks again; with approval mode on, stops: "a person must approve" |
| `uv run -m desk.proposals apply 0001 --approved` | Applies the patch, adds the ledger row, commits |
| `--no-approval` | Turns approval mode off (we keep it on) |
| `git revert <commit>` | Rolls a proposal back; give its ledger row an `end_date` |

## The checks

1. Only skills or playbook files change.
2. The risk files are untouched.
3. The patch applies.
4. On a throw-away copy with the patch applied: the tests pass and the memory budget (6,000 tokens) holds.
5. The limits file still matches its pin.

## A good proposal says

- **The change**, as small as possible (ours: one line, the `description:` of `market-read`).
- **Why**, from the evidence.
- **The evidence, and its limits** (ours: no closed trades, so only the journal, which is weaker evidence; every
  decision was "wait", so it says nothing about profit).
- **A success test** and when to roll back (ours: the share of flat bars that load `market-read` after one session, was
  2%; revert if it stays low).

## The what-changed-and-why report

`vault/Versions/Trader versions.md`: one row per version (start, hash, commit, what changed, why), what was found and
fixed, and the bars the journal shows per version. Ask Claude to check that every change to the instructions has its
ledger row. Fixing the ledger rewrites the record, so it is your decision: keep the old values visible in the notes.

Paper account only. Educational content, not financial advice; nothing here is a promise of profit or a recommendation.
