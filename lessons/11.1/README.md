# Student kit: Lesson 11.1, From developer to decision-maker

Module 11: Claude as the trader · AI Algorithmic Trading with Claude Code and Interactive Brokers

This lesson opens Part 2 of the course. In Part 1, Claude wrote the rules and the rules traded. From now on, Claude itself
is the decision-maker: on every 5-minute bar it reads the market and decides to buy, sell or wait. Before it trades a
single bar, we set up two things:

1. **An honest way to judge it.** Asked about April 9, 2025, Claude answers from memory and says a replay of 2025 would
   not be a fair test: it already knows what happened (training-data look-ahead). The honest test is a forward test, on
   paper, on bars that come after the day you start.
2. **The trader's own project.** A separate folder and a private repository, `~/trading-desk`, outside the Trading Lab,
   so the developer's instructions never load into the trader's sessions. It holds a short README, a one-line
   `CLAUDE.md` and an experiment ledger that gets a row for every version of the trader before it trades.

## What's in this kit

| File | What it is |
|---|---|
| `prompts.md` | The requests typed in the lesson, the commands, and the pause-and-try exercise |
| `cheat-sheet.md` | The words, who decides in Part 1 and Part 2, why a replay can't judge an AI trader, the honest tests (strongest first), rules for the harness, the ledger's columns, the git identity check |
| `trading-desk/` | The three files Claude created in the lesson, exactly as committed: `README.md`, `CLAUDE.md`, `experiments/ledger.csv` (header row only) |

No new dependency and no trading code yet: the desk starts empty on purpose.

## Before you start

- Claude Code in the terminal, signed in with your subscription, in auto mode.
- The Trading Lab from the earlier lessons (only for the first experiment).
- The GitHub CLI signed in (`gh auth status`), as set up in Lesson 3.3.
- Time on our computer: under a minute for each answer, about half a minute for the desk, and 14 seconds for the
  identity fix.

## Try it yourself

1. In your lab, `/clear`, then send request 1 in `prompts.md` (no tools), with a market day you remember well.
2. Make your own `~/trading-desk` outside your lab and send request 3. Read what Claude did before you push anything.
3. Check the author of your first commit with the shell-mode command in `prompts.md`.

You're done when your desk has its own private repository, the ledger has its header row and no versions yet, and the
only email in its history is your GitHub no-reply address. Claude's answers will differ from the video, and that's fine.

## Good to know

- **A model's memory is not a backtest.** Anything before its training cutoff may already be "known". Treat old data as
  contaminated unless a contamination check says otherwise.
- **Keep the trader out of the lab.** Claude Code also reads the `CLAUDE.md` files in parent folders, so a trader inside
  the lab would get the developer's instructions too.
- **Read what Claude did.** With no git identity on a new repository, Claude picked one for us, our personal e-mail.
  Set your identity once, globally, with the GitHub no-reply address, before the first push.
- **A force-push doesn't erase everything.** GitHub may keep an old commit reachable by its hash for a while. Another
  reason the desk repository is private.

## Safety

Paper trading only. The desk's `CLAUDE.md` says it in its first words, and nothing in this lesson connects to a broker.
Educational content, not financial advice; nothing here is a recommendation or a promise of profit.
