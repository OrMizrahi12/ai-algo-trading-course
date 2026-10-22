# MCP, permissions, hooks and the sandbox: cheat sheet

Lesson 3.6 · Checked against the Claude Code documentation on 2026-10-22. Menus and wording can change between versions.

## MCP: new tools for Claude

An **MCP server** is a small program that gives Claude new tools through a standard protocol (the Model Context
Protocol). Claude Code starts it and talks to it.

| Task | Command |
|---|---|
| Add a server that runs on your computer | `claude mcp add --scope project <name> -- <command> [args...]` |
| The lesson's server | `claude mcp add --scope project time -- uvx mcp-server-time` |
| List, inspect, remove | `claude mcp list` · `claude mcp get <name>` · `claude mcp remove <name>` |
| Inside a session | `/mcp`: servers, status, and each server's tools |

**Scopes** (who gets the server):

| Scope | Stored in | Who gets it |
|---|---|---|
| `local` (the default) | `~/.claude.json` | you, in this project only |
| `project` | `.mcp.json` in the repo | everyone who clones the repo; each person approves it once |
| `user` | `~/.claude.json` | you, in every project |

- Claude Code loads MCP servers when a session starts: after adding one, `/exit` and `claude --continue`.
- A server can run code on your computer. Approve project servers one at a time, and check its tools in `/mcp`
  (the time server's two tools are read-only).
- Keep secrets out of `.mcp.json`: it is committed.

## Permission rules

In `.claude/settings.json` (project, committed), `.claude/settings.local.json` (just you) or
`~/.claude/settings.json` (all your projects):

```json
{
  "permissions": {
    "deny": ["Read(./.env)", "Edit(./.env)", "Bash(git push --force:*)", "Bash(git push -f:*)"],
    "ask": ["Bash(rm:*)"]
  }
}
```

- Order: **deny** first, then **ask**, then **allow**. A deny rule always wins.
- The rules bind **Claude's own tools** (Read, Edit, Bash...). A program started by a shell command, such as a Python
  one-liner, can still open the file.
- Bash rules match the **start** of a command. Variants (other options, a longer command, another program) can slip
  past.
- So: keep real secrets out of the project folder, and use hooks for hard rules.

## Hooks: your code, every time

A **hook** is a command that Claude Code runs at a fixed moment. It reads a JSON description of the event on stdin.

| Event | When it runs | Exit code 2 means |
|---|---|---|
| `PreToolUse` | just before a tool runs (the `matcher` picks the tools, e.g. `Bash\|Edit\|Write`) | block the tool call; stderr goes to Claude as the reason |
| `Stop` | when Claude is about to finish its turn | don't stop yet; stderr goes to Claude, and it keeps working |

- Exit code 0: carry on. Any other code (including 1) is a non-blocking error: use **2** to enforce a rule.
- Register hooks in the settings file under `"hooks"`; `$CLAUDE_PROJECT_DIR` points to the project folder.
- `/hooks` lists every hook by event and source. The menu is read-only: edit the settings file, or ask Claude.
- Claude Code caps how many times in a row a Stop hook can send Claude back to work, so a hook that can never be
  satisfied can't trap it forever.
- The lesson's live-port hook checks the literal text of the command or new content. A port computed at runtime would
  get through, so `connect_test.py` keeps its own paper-port and paper-account checks too.

## The sandbox

`/sandbox` turns on an operating-system fence around the **shell commands** Claude runs: which files they can write
and which websites they can reach. It is off by default.

| System | What it needs |
|---|---|
| macOS | nothing: it uses the built-in Seatbelt framework |
| Linux, and Windows with WSL 2 | `bubblewrap` and `socat` (e.g. `sudo apt-get install bubblewrap socat`); `/sandbox` shows what is missing |
| Windows (native) | not supported: run Claude Code inside WSL 2 to use it |

- Modes: **auto-allow** (sandboxed commands run without asking) or **regular permissions** (the usual prompts).
- It covers shell commands only. Claude's file tools follow the permission rules; hooks and MCP servers run outside it.
- Commands you type yourself with `!` usually run outside the sandbox.

## Sources

- MCP in Claude Code: https://code.claude.com/docs/en/mcp
- Permissions: https://code.claude.com/docs/en/permissions
- Hooks: https://code.claude.com/docs/en/hooks
- Sandboxing: https://code.claude.com/docs/en/sandboxing
- The time server: https://github.com/modelcontextprotocol/servers/tree/main/src/time
