# Lesson 13.3 cheat sheet: memory that stays sharp

## Words

| Word | Meaning |
|---|---|
| Token | The unit a language model reads in: a short word or a piece of a long one, about 3 to 4 characters of English |
| Memory budget | A maximum size for what loads every bar (our desk: 6,000 tokens) |
| Summarise | Compress a lesson into one sentence that keeps every condition (at most 80 tokens for the whole line) |
| Archive | Move a lesson out of the way, to `vault/Lessons/Archive/`, still searchable, never deleted |
| Conflict | Two notes that give opposite advice |
| Seeded note | A made-up test note (`seeded: true`, name starts with `SEED`, a red banner). Never a real lesson |
| Memory brief | One summary sentence for each active lesson, added to the first message of each day's session |

## Two tiers

| Tier | What | Cost |
|---|---|---|
| Every bar | The constitution `CLAUDE.md`, the name and description of each skill, and the memory brief | Counted, at most 6,000 tokens |
| Lookup only | `Rules/` (already in `CLAUDE.md`), `Playbook/`, `Trades/`, `Daily/`, `Weekly/`, `Market/`, the full text of lessons, `Lessons/Archive/` | Zero per bar |
| Not counted | The market snapshot: data, not memory (a full one is about 30,000 tokens) | |

The trader has no file tools: it can't open the lookup tier by itself. You, interactive Claude sessions (with the vault
skill) and the note writer can.

## The budget script

```bash
uv run -m desk.memory
```

- Tokens are estimated as characters divided by 3.5 (no tokenizer offline; it over-counts a little on purpose).
- Exits 1 above 6,000 tokens, warns above 5,000, and warns if a seeded note is active.
- Over budget, it says what to do, in order: summarise any lesson over 80 tokens, then archive the lessons with the
  lowest `seen`, oldest `last_seen` first.

Our numbers (2026-10-24): `CLAUDE.md` 1,214 + four skills 435 = 1,649 of 6,000. The seeded test: 5 notes 4,192; 9 notes
6,070 (fail); conflict resolved 5,575; summaries 2,103; then all seeded notes archived.

## A lesson's life (`status`)

| Status | Meaning | Loads every bar? | Folder |
|---|---|---|---|
| `proposed` | Written by Claude, not yet approved | No | `Lessons/` |
| `active` | Approved by the person; needs `summary`, `seen`, `last_seen` | Yes | `Lessons/` |
| `disputed` | Disagrees with another lesson, tie not resolved | No | `Lessons/` |
| `superseded` | Replaced by a better lesson (`superseded_by`) | No | `Lessons/Archive/` |
| `archived` | Retired to save room | No | `Lessons/Archive/` |

## When two lessons disagree

1. **Check whether the conditions differ.** "Wait for the retest" and "buy the strong breakout" may both be right, one
   when volume is normal and one when it is high. Then keep both, with the condition in each summary.
2. **Else compare the evidence.** At least 2 more real trades behind it (`seen`) wins; with `seen` within 1, a
   `last_seen` at least 7 days newer wins. Anything else is a tie.
3. **Write the ruling down.** The loser gets `status: superseded`, `superseded_by`, `resolved` and a reason, and moves to
   the archive; the winner gets `replaces`.
4. **On a tie, neither is trusted.** Both become `disputed` and the person decides.

`CLAUDE.md` and the risk limits always win over any lesson, and a lesson never loosens a risk rule.
