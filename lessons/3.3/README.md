# Student kit: Lesson 3.3, Your first session: building the Trading Lab

Module 3: Claude Code from zero · AI Algorithmic Trading with Claude Code and Interactive Brokers

In this lesson you started Claude Code in its own folder, learned the permission modes, read a diff before approving
it, undid a change with `/rewind`, planned a bigger job in plan mode, and let Claude build the first version of the
Trading Lab: Python 3.12 with uv, four folders, a README, a `.gitignore`, a check script, the first Git commit, and a
private GitHub repository.

## What's in this kit

| File | What it is |
|---|---|
| `session-cheat-sheet.md` | Permission modes, Shift+Tab, reading a permission prompt and a diff, `/rewind`, `!` shell mode, `/clear` |
| `prompts.md` | Every request typed in the lesson, ready to copy, with a placeholder where your own details go |
| `setup-git-uv-gh.md` | Git, uv and the GitHub CLI on Windows, macOS and Linux, plus your GitHub no-reply e-mail address |
| `trading-lab/` | The Trading Lab exactly as the first commit left it (for comparison; build your own with Claude) |

## Try it yourself (the pause-and-try checkpoint)

1. In a terminal: `mkdir trading-lab`, `cd trading-lab`, `claude`. Trust the folder (it's yours and it's empty).
2. Press Shift+Tab a few times and watch the footer: manual, accept edits, plan, auto.
3. In manual mode, ask for `rules.txt` with one line, approve it, ask for a change, read the diff, then undo it with
   `/rewind` → "Restore code and conversation". Check with `! cat rules.txt`.
4. `/clear`, switch to plan mode, and send the Trading Lab request from `prompts.md`. Read the plan before you approve.
5. Read Claude's summary. If it set a Git e-mail you don't want in your history, ask for the no-reply address
   (see `setup-git-uv-gh.md`).
6. `/clear`, then ask Claude to publish the folder as a **private** GitHub repository. Log in yourself when it asks:
   `! gh auth login -h github.com -p https -w`.

You're done when:

```bash
uv run check_lab.py
```

prints `Python version: 3.12.…` and today's date, and your repository on GitHub shows the **Private** badge with your
files. Your versions and output can differ a little from the video; that's expected.

## Good to know

- Claude chose some things for us on camera (the uv installer, a Git identity). Always read what Claude did, not
  only whether it worked.
- `/rewind` undoes Claude's own file edits. It does not undo changes made by shell commands or by hand: Git is your
  long-term history.
- Usage limits, plans and versions shown in the video were current at the time of recording (October 2026).

## Next

Lesson 3.4: context and memory, so Claude remembers how the Lab works.
