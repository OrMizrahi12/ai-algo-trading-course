# Cheat sheet: Lesson 13.1, Obsidian as the trader's brain

## Words

| Word | Meaning |
|---|---|
| **Vault** | An Obsidian folder of Markdown notes. Ours is `~/trading-desk/vault`, inside the desk's Git repository. |
| **Wikilink** | A note's name in double square brackets, `[[VWAP reclaim]]`: a link between notes. Obsidian draws the graph from them. |
| **Template** | A note skeleton we copy for every new trade or day (`Templates/Trade note`, `Templates/Daily note`). |
| **Graph view** | Obsidian's map of the notes and their links. |
| **Properties** | The block between `---` lines at the top of a note (`type`, `date`, `setup`, `readonly` ...). Obsidian shows it as a table. |

## Markdown is the database

- Every note is a plain `.md` file. Obsidian reads and shows them; Claude Code reads and writes them with its own file tools.
- `.obsidian/` holds Obsidian's settings for this vault. `workspace.json` (open tabs, layout) changes all the time, so it
  is git-ignored.
- Everything else is committed with the repo, so every change to the desk's memory is reviewable.

## The vault Claude designed

| Folder | What lives there | Who writes it |
|---|---|---|
| `Rules/` | Copies of the risk rules: `Constitution risk rules` (from `CLAUDE.md`) and `Lab risk limits` (from `risk_limits.yaml`) | Nobody in the vault. A person updates the source, then refreshes the copy |
| `Playbook/` | One note per setup: `Opening range breakout`, `VWAP reclaim`, from the lab's own definitions | Claude may add a setup or a dated "What we have seen" line; a setup's rules change only with your say-so |
| `Market/` | Notes about the market: a trending or choppy day, an event day, data quirks | Claude |
| `Trades/` | One note per trade, from the trade template, written after the trade ends | Claude |
| `Daily/` | One note per trading day: plan, counters, trades, how the day went | Claude |
| `Lessons/` | One sentence of "do this differently", linked to its trades; "seen once" until it repeats | Claude proposes; you decide what becomes a rule |
| `Templates/` | `Trade note`, `Daily note` | You. Copy them, never fill them in place |
| `README` | The map: folders, how a day flows, conventions | Claude, with you |

## Read-only, honestly

- The rules notes carry `readonly: true` and a warning: *this note is a copy; a person edits the source; if they disagree,
  the source wins.*
- That is a **convention**. The skill tells Claude not to edit `Rules/`, but nothing in the file system enforces it.
- What binds the trader is still `CLAUDE.md`, the lab's limits file, and the guardrails from Lesson 12.3. The vault never
  changes the desk's behaviour by itself.

## Where the vault skill lives, and why

| Place | What happens |
|---|---|
| `.claude/skills/vault/` (inside the desk) | Hashed into the heartbeat trader's instructions: a new skill there starts a new trader session mid-day and records a new instructions version in the ledger. The trader has only the Skill tool, so it could not use it anyway |
| `.claude/vault-skill/vault/` (what we chose) | Committed with the desk, outside the hashed folder. Turn it on for your interactive sessions with `ln -s "$PWD/.claude/vault-skill/vault" ~/.claude/skills/vault` |

## Install in one line (Ubuntu)

```bash
cd ~/Downloads && sudo apt install ./obsidian_1.14.5_amd64.deb && which obsidian
```

Use the name of the file you downloaded. Windows and macOS: see `install-obsidian.md`.
