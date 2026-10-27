# Lesson 11.1 prompts and commands

Everything typed in the lesson, in order. Lines that start with `/` are Claude Code commands; a line that starts with `!`
inside Claude Code runs a shell command directly (shell mode), and Claude sees its output too. Every request below was
sent in auto mode. Nothing in this lesson connects to IB.

## 1. The look-ahead experiment (in the Trading Lab)

```text
/clear
```

Then send:

```text
Quick experiment, no tools: what happened to SPY on April 9, 2025, and what did it do over the following week? Then tell me honestly: if I replayed 2025 bars to you and asked you to trade them, would that be a fair test of you as a trader?
```

Claude answered in 15 seconds on our computer, from memory, and said so ("treat the exact figures as approximate"). Its
verdict: no, it is contaminated; its training data runs to about June 2026, so a decision on 2025 bars would be recall
dressed up as skill, and even our Part 1 holdout (bars from 2026-04-22) is only partly clean for it.

Try it with any market day you remember well. The figures Claude recalls are its memory, not checked data: don't use
them as facts.

## 2. How do we test it honestly?

```text
Part 2 of this course does make you the trader: you'll decide on every 5-minute bar, on paper. So how do we test you honestly? And what if I hide the dates and the symbol?
```

Its answer (14 seconds): hiding helps but doesn't make the test clean, and a plan, strongest first: forward-only paper
trading, a replay of bars from after its cutoff, older data anonymized with a contamination check. The cheat sheet has
the whole list and the rules for the harness.

## 3. The trader's own desk (a second terminal)

```bash
mkdir ~/trading-desk && cd ~/trading-desk && git init -b main
claude
```

Claude Code asks whether you trust the new folder: choose **Yes, I trust this folder**. Then send:

```text
This folder is a new project: an AI trading desk where you will be the decision-maker on paper, on US stocks and ETFs, 5-minute bars. Don't write any trading code yet. Create a short README (paper only, educational), a ledger at experiments/ledger.csv with columns for version, model, start date, end date, instructions file hash, symbols, bar size, risk limits and notes, and a CLAUDE.md that says only: paper only, never touch a live account, explain every term. Commit, then publish it as a private GitHub repository called trading-desk.
```

About half a minute on our computer. The commit first failed ("Author identity unknown"), so Claude set an identity
for this repository on its own, with our personal e-mail, then created the private repository and pushed. If git
already knows who you are globally, this won't happen to you; read the summary either way.

## 4. Fix the identity

```text
Don't put my personal email in the history. Use the same identity as my trading-lab repo (my name and the GitHub noreply address), set it globally so new projects get it too, fix the author of this first commit, and force-push.
```

14 seconds. Claude read the name and the no-reply address from the Lab, set them globally, removed the repository's own
override, rewrote the first commit and force-pushed. If your Lab has no such identity, give Claude your no-reply address
yourself: on GitHub, **Settings > Emails** shows it (the form is `ID+username@users.noreply.github.com`). By hand it is:

```bash
git config --global user.name "Your Name"
git config --global user.email "ID+username@users.noreply.github.com"
```

## 5. Check it yourself (shell mode)

```text
! cat CLAUDE.md experiments/ledger.csv && git log --format='%h %an <%ae> %s'
```

You should see the one rule line, the ledger's header row, and one commit whose author e-mail is your no-reply address.

## Pause and try

1. Ask Claude, with no tools, about a market day you remember well, and whether replaying it would be a fair test.
2. Make your own `~/trading-desk` outside your lab, with the README, the ledger and the `CLAUDE.md` (request 3).
3. Check the author of your first commit before you push (command 5).

You're done when your desk has its own private repository, the ledger has its header row and no versions yet, and the
only e-mail in its history is your GitHub no-reply address. Paper only.
