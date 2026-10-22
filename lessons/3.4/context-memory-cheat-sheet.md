# Context and memory cheat sheet (Lesson 3.4)

## Where instructions live (all load when a session starts)

| Layer | File | Shared? | Use it for |
|---|---|---|---|
| User | `~/.claude/CLAUDE.md` | Only you, in every project | Your personal preferences everywhere |
| Project | `./CLAUDE.md` (or `./.claude/CLAUDE.md`) | Everyone who clones the repo (it goes into Git) | The project's rules, commands, layout |
| Local | `./CLAUDE.local.md` | Only you, this project (add it to `.gitignore`) | Personal notes about this project |
| Import | `@path` inside any of these files | Like the file that imports it | Pulling one file into another, for example `@AGENTS.md` |
| Auto memory | `~/.claude/projects/<project>/memory/` | Only you, on this computer, not in Git | Notes Claude keeps for itself when you ask it to remember |

- `/init` writes a first `CLAUDE.md` from your project. Read it before you commit it.
- `/memory` lists every file Claude reads, opens them, and turns auto memory on or off.
- Auto memory loads the start of its index (`MEMORY.md`, the first 200 lines or 25 KB) at every session start.
- `AGENTS.md` is the file other coding tools read. If your project has a `CLAUDE.md`, Claude Code reads that instead,
  so make `CLAUDE.md` import it with a line `@AGENTS.md`.

Official page: https://code.claude.com/docs/en/memory

## The context window

Everything Claude can see at once, in one session: the system prompt, the built-in tools, tool descriptions from
connectors, your memory files, skills, and the conversation itself. It is counted in **tokens** (small pieces of text,
about three quarters of a word each).

| Type | What it does |
|---|---|
| `/context` | Shows what fills the context right now: a grid, then usage by category (scroll up for the top) |
| `/compact <what to keep>` | Replaces the conversation with a summary and frees the space; say what to keep |
| Ctrl+O | Switches to the detailed view (for example the full compact summary); Ctrl+O again comes back |
| `/clear` | Starts a fresh, empty conversation in the same folder; your files stay |

Keep it lean: turn off what a project doesn't need. In the lesson, a project setting turned off the claude.ai
connector tools for the Trading Lab only:

```json
{
  "disableClaudeAiConnectors": true
}
```

(in `.claude/settings.json`). Claude Code reloads its settings files while it runs.
Official pages: https://code.claude.com/docs/en/context-window · https://code.claude.com/docs/en/settings

## What survives

| Action | What is kept |
|---|---|
| `/compact` | A summary of the conversation. Summaries can drift or lose details |
| `/clear` | Nothing of the chat |
| `CLAUDE.md` | Everything in it: read from disk at every start, and again after every compact |

If it must survive, write it down.

## Sessions

| Type | What it does |
|---|---|
| `/exit` | Leaves cleanly and prints the command to resume this conversation |
| `claude --continue` | Reopens the most recent conversation in this folder, with its history |
| `claude --resume` | Picks a past conversation (or pass its ID) |
| `/resume` | Lists your past sessions in this project, by name, from inside Claude Code |

Official page: https://code.claude.com/docs/en/sessions

## Model and effort

| Type | What it does |
|---|---|
| `/model` | Pick a model (Up/Down). Each model has its own default effort; Left/Right adjust it. Esc keeps what you had |
| `/effort` | The same effort choice as a slider: low, medium, high, xhigh, max |

Effort is how long the model thinks before it acts: faster, or smarter. Higher effort costs more usage; the slider
shows the estimate relative to the default.
Official page: https://code.claude.com/docs/en/model-config

## Watch your limits

`/usage` shows how much of your plan's current session and week you have used, when it resets, and suggestions
(for example: turn off skills you don't use). Context costs usage, so keep it lean. Limits differ by plan.
Official page: https://code.claude.com/docs/en/costs

## Words to keep

| Term | Meaning |
|---|---|
| Context window | Everything Claude can see at once, in one session |
| CLAUDE.md | A file of standing instructions, read at the start of every session and after every compact |
| Auto memory | Notes Claude keeps for itself across sessions, on your computer |
| Compact | Replace the conversation with a summary, to free space |
| Effort | How long the model thinks before it acts |
