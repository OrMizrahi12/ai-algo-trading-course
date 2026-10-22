# Student kit: Lesson 3.4, Context and memory

Module 3: Claude Code from zero · AI Algorithmic Trading with Claude Code and Interactive Brokers

In this lesson you gave the Trading Lab standing instructions with `/init` and `CLAUDE.md`, added a rule of your own,
read Claude's context window with `/context` and trimmed it with a project setting, came back to a session with
`claude --continue`, compacted a conversation and caught what the summary got wrong, saved the missing rule to
`CLAUDE.md` so it survives, picked a model and an effort level, shared the rules with other coding tools through
`AGENTS.md`, saved a note to auto memory, and checked your usage with `/usage`.

## What's in this kit

| File | What it is |
|---|---|
| `context-memory-cheat-sheet.md` | Where instructions live, what fills the context, compact vs clear, sessions, model and effort, usage |
| `prompts.md` | Every request typed in the lesson, ready to copy, with placeholders where your own details go |
| `claude-md-starter.md` | A short starting point for your own `CLAUDE.md`, and what makes a good rule |
| `trading-lab/` | The Trading Lab as the lesson left it: `CLAUDE.md` importing `AGENTS.md`, and `.claude/settings.json` (for comparison; build your own with Claude) |

## Try it yourself (the pause-and-try checkpoint)

1. In your `trading-lab` folder, start `claude` and run `/init`. Read what it wrote before you say yes.
2. Add one rule of your own (see `prompts.md`), and let Claude commit and push it.
3. Run `/memory` to see every place Claude reads instructions from.
4. Run `/context` and read the grid at the top. If you see connector tools your project doesn't need, turn them off
   for this project with the `disableClaudeAiConnectors` setting (see `prompts.md`).
5. `/compact` with a focus, for example `/compact keep the lab setup decisions and the git identity`.
6. Ask something only your rules can answer. Then `/clear`, and ask again.

You're done when a fresh session, right after `/clear`, answers from your `CLAUDE.md` (or from the `AGENTS.md` it
imports). Your versions, numbers and wording can differ a little from the video; that's expected.

## Good to know

- `CLAUDE.md` is read from disk at the start of every session, and again after every compact. Anything you only said
  in the chat can be lost or summarized wrongly. If it must survive, write it down.
- Never put a personal e-mail address, a password or an API key into `CLAUDE.md` or `AGENTS.md`: they go into Git.
- Auto memory stays on your computer, in your home folder, not in Git. `/memory` shows it and can turn it off.
- Usage limits, plans, model names and versions shown in the video were current at the time of recording
  (October 2026). The course's own account was a busy one; your numbers will differ.

## Next

Lesson 3.5: skills and subagents.
