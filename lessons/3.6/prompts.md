# Lesson 3.6 prompts and commands

Everything typed in the lesson, in order. Lines that start with `!` run in the terminal from inside Claude Code
(shell mode): the output goes into the conversation too. Lines that start with `/` are Claude Code commands.

## 1. MCP: plug in a new tool

```text
/mcp
```

```text
! claude mcp add --scope project time -- uvx mcp-server-time
```

```text
! cat .mcp.json
```

```text
/mcp
```

Claude Code loads MCP servers when a session starts, so restart:

```text
/exit
```

```bash
clear
claude --continue
```

Approve the new project server once: **Use this MCP server**.

## 2. Use the time server

```text
/mcp
```

Open `time`, then **View tools**. Then:

```text
Use the time tools: what time is it right now in New York, London and UTC? Is the US stock market open at this moment (regular hours are 9:30 to 16:00 New York time, Monday to Friday)?
```

```text
Commit .mcp.json and push.
```

## 3. Permission rules

A demo secrets file with a fake value, and a check that Git ignores it:

```text
! printf "DEMO_API_KEY=not-a-real-key-123\n" > .env && git check-ignore .env
```

```text
No, keep it. Treat .env as where real secrets will live. Add permission rules to .claude/settings.json: deny Read and Edit on .env, deny git push --force, and ask before any rm command. Keep the existing setting. Commit and push.
```

```text
Test it: show me what is inside .env.
```

## 4. A rule is not a wall

A program started from the shell is not one of Claude's tools, so the deny rule doesn't stop it:

```text
! python3 -c "print(open(\".env\").read())"
```

```text
No, leave it. Real secrets will live outside the repo, and next we add hooks for hard rules.
```

## 5. A PreToolUse hook that blocks live ports

```text
Write a PreToolUse hook: a Python script at .claude/hooks/block_live_ports.py, registered in .claude/settings.json for the Bash, Edit and Write tools. If the command or the new file content mentions port 7496 or 4001 (the live Interactive Brokers ports), block the action with exit code 2 and a clear reason. Keep the existing settings. Don't commit yet.
```

```text
Now change PORT in connect_test.py to 7496.
```

```text
Yes, try the edit so we can watch the hook block it.
```

## 6. A Stop hook

```text
Now add a Stop hook at .claude/hooks/require_commit.py: when you try to finish, if git status shows uncommitted changes, block with exit code 2 and the reason: commit and push your work before you stop. Then commit everything, including both hooks, and push.
```

```text
Add one line to the end of README.md: Hooks in .claude/hooks guard the paper-only rule. Nothing else.
```

## 7. Hooks and the sandbox

```text
/hooks
```

```text
/sandbox
```

In the lesson the sandbox was switched on with **Sandbox commands, with regular permissions** to show the choice, and
switched back off afterwards: in this course the hard rules live in hooks. See `cheat-sheet.md` for what the sandbox
needs on each system.

## Pause and try

1. Add the time server at project scope, restart, approve it, and ask the market-time question.
2. Add a deny rule for `.env`, and test it.
3. Ask Claude for the live-port hook, and try to get past it.

You'll know it worked when an edit to port 7496 fails with your hook's message.
