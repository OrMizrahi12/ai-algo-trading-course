# The requests typed in Lesson 3.3

Copy them as they are, or change the details. Claude's answers on your computer will differ a little from the video.

## 1. A tiny first request (manual mode)

```text
Create a file called rules.txt with one line: Paper trading only.
```

```text
Change it to say: Paper trading only. Never a live account.
```

Then `/rewind`, pick the second request, and choose "Restore code and conversation". Check with `! cat rules.txt`.

## 2. The Trading Lab (plan mode)

```text
Set up this folder as our Trading Lab, a Python project. Use uv to install Python 3.12 and create the project. Make folders for data, strategies, backtests and notebooks, a README that says what the lab is for (paper trading only, educational), a .gitignore for Python, and a small check_lab.py that prints the Python version and today's date. Run it. Then make the first Git commit. Don't install any trading libraries yet.
```

Why it works: it names the goal, the tools (uv, Python 3.12), what to make, how to prove it works (run the script),
how to finish (the first commit) and where to stop (no trading libraries yet).

## 3. If Claude set a Git identity you don't want in your history

Replace the two placeholders with your own name and your GitHub no-reply address (see `setup-git-uv-gh.md`):

```text
Two fixes. First, I don't want my personal email in the history: set this repo's Git identity to the name <Your Name> and the email <your GitHub no-reply address>, and fix the first commit's author. Second, add uv's folder to my PATH so new terminals can find uv.
```

## 4. A private GitHub repository

```text
Now publish this repo to my GitHub as a PRIVATE repository called trading-lab. Install the GitHub CLI if it's missing, and tell me when you need me to log in.
```

When Claude asks you to log in, run it yourself with the `!` in front:

```text
! gh auth login -h github.com -p https -w
```

It prints a one-time code (keep it to yourself) and opens, or tells you to open, https://github.com/login/device .
If Claude offers to rename the branch to `main`:

```text
Yes, rename it to main.
```
