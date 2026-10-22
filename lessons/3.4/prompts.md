# The requests typed in Lesson 3.4

Copy them as they are, or change the details. Claude's answers on your computer will differ a little from the video.

## 1. Standing instructions

```text
/init
```

When Claude asks whether to commit and push the new `CLAUDE.md`, add a rule of your own first:

```text
Yes, but first add one rule to CLAUDE.md: explain every trading term in plain English the first time you use it. Then commit and push.
```

Then see every place Claude reads instructions from:

```text
/memory
```

Press Esc to close it.

## 2. What fills the context

```text
/context
```

The output is long: scroll up to the grid at the top. If it lists connector tools (Gmail, Drive, Calendar...) that a
trading project doesn't need:

```text
The context list shows dozens of claude.ai connector tools (Gmail, Drive, Calendar...) that this trading project doesn't need. Turn them off for this project with the disableClaudeAiConnectors setting in .claude/settings.json, and commit it.
```

```text
Yes, push it.
```

Run `/context` again to confirm the connector tools are gone.

## 3. Leave and come back

```text
/exit
```

Claude Code prints the command to resume this exact conversation (`claude --resume` and the session's ID). Or, simpler,
reopen the most recent conversation in this folder:

```bash
claude --continue
```

## 4. Compact, and what it forgets

```text
/compact keep the lab setup decisions and the git identity
```

Ctrl+O shows the full summary; Ctrl+O again comes back. Then check what survived:

```text
Quick check after the compact: which email does Git use in this repo, and why did we pick it?
```

If the reason was lost, write it down where it survives:

```text
Good lesson: the compact summary lost the reason. We picked the GitHub no-reply address so a personal email never shows up in public commits. Add that rule to CLAUDE.md so it survives every compact and every new session, then commit and push.
```

Then the test: `/clear`, and ask again.

```text
/clear
```

```text
Which email should Git commits use in this project?
```

## 5. Model, effort and sessions

```text
/model
```

Arrow keys up and down pick a model; left and right change its effort. Esc keeps what you had.

```text
/effort
```

```text
/resume
```

## 6. AGENTS.md and auto memory

```text
Other coding tools read AGENTS.md instead of CLAUDE.md. Move the shared project rules into AGENTS.md, and make CLAUDE.md import it with an @AGENTS.md line, so both kinds of tools follow the same rules. Commit and push.
```

Check it yourself in shell mode (type `!` first, then the command):

```text
! cat CLAUDE.md; head -8 AGENTS.md
```

```text
/memory
```

Save a personal preference to auto memory:

```text
Remember this for future sessions: when you explain a command, show the command first and keep the explanation to two sentences.
```

## 7. Watch your limits

```text
/usage
```

Press Esc to close it.
