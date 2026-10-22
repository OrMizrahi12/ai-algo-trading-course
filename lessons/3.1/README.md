# Student kit: Lesson 3.1, The terminal in one lesson

Module 3: Claude Code from zero · AI Algorithmic Trading with Claude Code and Interactive Brokers

Claude Code lives in the terminal, so this lesson gets you comfortable there first. You opened a terminal, read its
prompt, moved around and managed files with ten short commands, picked up the tricks that make you fast, and
installed VS Code, the editor we read code in for the rest of the course.

## What's in this kit

| File | What it is |
|---|---|
| `terminal-cheat-sheet.md` | Every command from the lesson, with the Windows PowerShell and macOS equivalents |
| `install-vscode.md` | Step-by-step VS Code install for Windows, macOS and Linux, plus the first launch |

## Try it yourself (the pause-and-try checkpoint)

On your own computer (PowerShell on Windows, Terminal on a Mac, any terminal on Linux):

```bash
mkdir practice
cd practice
touch notes.txt                      # Windows PowerShell: New-Item notes.txt
echo 'Plan the trade, trade the plan.' > notes.txt
cat notes.txt
code .
```

You're done when `cat` prints your line in the terminal and VS Code shows the same file. Add a second line in VS
Code, save it (Ctrl+S, or Cmd+S on a Mac), and run `cat notes.txt` again: both lines are there.

If `code .` says "command not found", see the last section of `install-vscode.md`.

## Next

Lesson 3.2: choosing a Claude plan and installing Claude Code, right in the terminal.
