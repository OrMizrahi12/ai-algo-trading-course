# Student kit: Lesson 3.2, Choosing a plan and installing Claude Code

Module 3: Claude Code from zero · AI Algorithmic Trading with Claude Code and Interactive Brokers

Claude Code comes with a paid Claude plan, so this lesson starts with the plans and their usage limits. Then you
install Claude Code with the official one-line installer, sign in with your subscription (not an API key), read your
usage meters, and install Claude Desktop, whose Code tab runs the same Claude Code in a window.

## What's in this kit

| File | What it is |
|---|---|
| `plans-and-limits.md` | Free, Pro and Max, the 5-hour and weekly limits, and which plan fits this course (prices at the time of recording, with the official links) |
| `install-claude-code.md` | Step-by-step install for Windows, macOS and Linux, the API key check, signing in, `/status` and `/usage`, and fixes for common problems |
| `install-claude-desktop.md` | Claude Desktop for Windows and macOS, and the Linux (beta) apt steps we ran, including the two problems we hit and their fixes |

## Try it yourself (the pause-and-try checkpoint)

On your own computer (PowerShell on Windows, Terminal on a Mac, any terminal on Linux):

```bash
curl -fsSL https://claude.ai/install.sh | bash      # Windows PowerShell: irm https://claude.ai/install.ps1 | iex
claude --version
echo "key: $ANTHROPIC_API_KEY"                      # Windows PowerShell: echo "key: $env:ANTHROPIC_API_KEY"
cd ~/practice                                       # the folder from Lesson 3.1 (any folder works)
claude
```

Sign in with your Claude account in the browser, then type `/status` inside Claude Code.

You're done when `echo` prints `key:` and nothing after it, and `/status` shows **Login method: Claude Pro account**
or **Claude Max account**. Type `/exit` to leave Claude Code.

## Next

Lesson 3.3: your first real session. We build the Trading Lab folder, with Claude Code.
