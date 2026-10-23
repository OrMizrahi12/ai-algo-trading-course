# Student kit: Lesson 3.6, MCP, hooks and permissions

Module 3: Claude Code from zero · AI Algorithmic Trading with Claude Code and Interactive Brokers

In this lesson you plugged a new tool into Claude: the official **time** MCP server, added at project scope so it lives
in the Trading Lab's `.mcp.json`. Claude used it to read the clock in New York, London and UTC and to tell whether the
US stock market was open. Then you added permission rules that keep Claude's own tools away from `.env`, and saw their
limit: a Python command run from the shell still read the file. Last, you wrote two hooks: a **PreToolUse** hook that
blocks any command or edit mentioning a live Interactive Brokers port, and a **Stop** hook that keeps Claude working
until its changes are committed. You looked at both in `/hooks`, and at the choices in `/sandbox`.

## What's in this kit

| File | What it is |
|---|---|
| `prompts.md` | Every command and request typed in the lesson, ready to copy, plus the pause-and-try exercise |
| `cheat-sheet.md` | MCP, permissions, hooks and the sandbox on one page: commands, files, exit codes, limits |
| `trading-lab/.mcp.json` | The project MCP config written by `claude mcp add --scope project` |
| `trading-lab/.claude/settings.json` | The project settings after the lesson: the connector setting from 3.4, the permission rules, both hooks |
| `trading-lab/.claude/hooks/block_live_ports.py` | The PreToolUse hook exactly as Claude wrote it |
| `trading-lab/.claude/hooks/require_commit.py` | The Stop hook exactly as Claude wrote it |
| `trading-lab/README.md` | The README with the line added in the Stop-hook test |

Folders that start with a dot (`.claude`) and files like `.mcp.json` are hidden in some file browsers: use `ls -a`, or
show hidden files.

## Before you start

- You need the Trading Lab from Lessons 3.3 to 3.5 and `uv` (installed in Lesson 3.3). `uvx` comes with `uv`: it
  downloads and runs the time server the first time Claude Code starts it.
- The `.env` in the lesson holds a fake value (`DEMO_API_KEY=not-a-real-key-123`). Never put a real key in a project
  folder to test this: the lesson shows that a program run from the shell can still read it.
- The hooks call `python3`. On Windows, if `python3` doesn't start Python, change the two `command` lines in
  `.claude/settings.json` to `python` (or `py`), or ask Claude to do it.

## Try it yourself

1. In your `trading-lab` folder, run `/mcp` to see what's there, then
   `! claude mcp add --scope project time -- uvx mcp-server-time`.
2. `/exit`, then `claude --continue`. Approve the new server once ("Use this MCP server").
3. `/mcp` should show **Project MCPs** with `time` connected and two read-only tools. Ask the market-time question
   from `prompts.md`.
4. Ask Claude to add a deny rule for `.env` (Read and Edit), then ask it to show you the file. The Read tool should be
   refused.
5. Ask for the live-port PreToolUse hook (the request is in `prompts.md`). It works as soon as the settings file is
   saved: check it with `/hooks`, then ask Claude to change a port to 7496.

You're done when the edit fails with your hook's message, `Blocked: ...`, and the file is unchanged. Your wording and
Claude's replies will differ from the video; the behaviour is what matters.

## Known issue, fixed in lesson 4.2

The `require_commit.py` Stop hook in this kit is the version built in this lesson. It can keep Claude from stopping
when it is told to wait, because it does not check `stop_hook_active`. Lesson 4.2 finds and fixes this; its kit has the
fixed hook (`lessons/4.2/trading-lab/.claude/hooks/require_commit.py`). Use that one in your own lab.

## Safety

Paper trading only. Educational content, not financial advice. Ports 7496 (TWS) and 4001 (IB Gateway) are Interactive
Brokers' live, real-money ports; this course only ever uses the paper ports 7497 and 4002.
