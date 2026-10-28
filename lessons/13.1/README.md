# Student kit: Lesson 13.1, Obsidian as the trader's brain

Module 13: Memory with Obsidian · AI Algorithmic Trading with Claude Code and Interactive Brokers

Until now our desk kept what it knows in scattered places: the rules in `CLAUDE.md`, the limits in the lab's
`risk_limits.yaml`, the setups in Python, and the history in the heartbeat's journal. In this lesson the desk gets a
notebook: an **Obsidian vault**, a folder of plain Markdown notes inside `~/trading-desk`. Obsidian shows the notes, their
links and the graph; Claude Code reads and writes the same files with its own file tools. Markdown is the database.

What happened on our computer (paper account, 2026-10-23):

1. We downloaded Obsidian 1.14.5 from the official site, obsidian.md (Download page, Linux, **Deb**), and installed it in the
   terminal with `sudo apt install ./obsidian_1.14.5_amd64.deb`.
2. We opened Obsidian (Applications, Office, Obsidian), skipped the sign-in, and created a vault named `vault` in
   `~/trading-desk`. No account is needed.
3. In a fresh Claude Code session in `~/trading-desk` (auto mode), with Obsidian open beside it, we asked Claude to design
   the vault as the desk's memory. It made the folders, a README note, two read-only rules notes, the two playbook setups
   from the lab's own definitions, two templates and today's daily note.
4. Before adding the vault skill, Claude asked where it should go, and recommended **outside** `.claude/skills/`: that
   folder is hashed into the heartbeat trader's instructions, and the heartbeat was running. We agreed. It committed
   everything in one commit.

## What's in this kit

| File | What it is |
|---|---|
| `install-obsidian.md` | Installing Obsidian on Linux (as in the video), Windows and macOS, and creating the vault |
| `prompts.md` | The design prompt typed in the lesson, our answer to Claude's question, and the pause-and-try exercise |
| `cheat-sheet.md` | The words, the vault's folders and who writes each one, how notes link, and the read-only convention |
| `trading-desk/vault/` | The vault exactly as Claude wrote it in the lesson (README, Rules, Playbook, Templates, Daily, empty Market, Trades and Lessons, and Obsidian's small settings files) |
| `trading-desk/.claude/vault-skill/vault/SKILL.md` | The vault skill: how Claude reads and writes the vault |

The folders that start with a dot (`.obsidian`, `.claude`) are hidden on most systems. Show hidden files to see them.

## Before you start

- Your `~/trading-desk` from Modules 11 and 12 (a Git repository with `CLAUDE.md`, the skills and the guardrail hook).
- Claude Code in the terminal, signed in with your subscription.
- About 15 minutes.

## Try it yourself

1. Install Obsidian from obsidian.md (`install-obsidian.md`) and create a vault named `vault` inside your desk folder.
2. Start a fresh Claude Code session in your desk folder and send the design prompt from `prompts.md`. Answer its questions.
3. Open a setup note in Obsidian and follow its links in the graph view.

You're done when the folders, the README note, the rules notes, the two setups and today's daily note show up in Obsidian,
and the vault is committed. Your notes will not match ours word for word: Claude writes them from your own desk, and that's
fine. You can also compare with, or start from, the files in `trading-desk/vault/`.

## Turn the vault skill on

The skill does not load on its own, on purpose. To use it in your interactive sessions, run this once from your desk folder:

```bash
ln -s "$PWD/.claude/vault-skill/vault" ~/.claude/skills/vault
```

Keep it out of `.claude/skills/` inside the desk: everything there is hashed into the heartbeat trader's instructions,
so a new skill there would start a new trader session mid-day and record a new instructions version in the ledger. The
heartbeat trader has only the Skill tool and no file tools, so it could not use the vault skill anyway.

## Good to know

- **It's just files.** Every note is a `.md` file. You can read and edit them in any editor; Obsidian adds the links,
  the graph and the properties view on top.
- **Read-only is a convention.** The rules notes say `readonly: true` and carry a warning, and the skill tells Claude not
  to edit them, but nothing in the file system enforces it. The real rules stay in `CLAUDE.md` and the lab's limits file:
  if a copy and its source disagree, the source wins.
- **The guardrail hook still works.** In the lesson, one of Claude's own shell commands was blocked because it named
  guarded files. Claude read them one at a time instead and changed none of them.
- **The placeholder node.** The graph shows a faint `{{date:YYYY-MM-DD}}` node: the day link inside the trade-note template. It turns
  into a real date when the template is used.
- **`workspace.json` is ignored.** Obsidian rewrites it constantly (open tabs, window layout), so the vault's
  `.gitignore` keeps it out of Git.
- **sudo asks for your password.** On our computer it did not; on yours it will, once.

## Safety

Paper trading only. The vault is notes: it never places an order and never changes the desk's behaviour by itself.
Educational content, not financial advice; nothing here is a recommendation or a promise of profit.
