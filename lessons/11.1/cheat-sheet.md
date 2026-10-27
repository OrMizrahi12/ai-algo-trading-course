# Lesson 11.1 cheat sheet: From developer to decision-maker

## The words

| Word | Meaning |
|---|---|
| **Decision-maker** | The part that chooses to buy, sell or wait. Part 1: our code. Part 2: Claude |
| **Heartbeat** | The small program that wakes Claude on every bar, hands it the data, and carries out its checked decisions |
| **Training-data look-ahead** | The model already knows what happened after a past date, because it read about it while it was trained |
| **Forward test** | Running a strategy from now on, on data nobody has seen yet (on paper here) |
| **Experiment ledger** | A dated list of every version of the trader and what it was allowed to do, written before it trades |
| **Contamination check** | Before trading on old data, ask the model to guess the symbol and the date; right more often than chance means the data has leaked |

## Who decides

| | Part 1: the AI creates the strategies | Part 2: the AI is the strategy |
|---|---|---|
| Claude | writes the rules (Python) | reads the market on every 5-minute bar and decides, "wait" included |
| The rules | trade, the same way every time | move into Claude's instructions, skills and memory |
| Python | the strategy and the engine | the heartbeat, the validator, the risk seatbelt, the executor, the journal |
| A backtest | fair, if the code only sees closed bars | not fair: the model may remember what came next |

Python never filters the market for Claude in Part 2. It wakes it, checks its answer, keeps the risk limits, places the
paper order and writes everything down.

## Why a replay can't judge an AI trader

- **It is contaminated.** A model trained on text up to a date (Claude said "about June 2026" in the lesson) knows how
  the markets before that date played out. A decision on those bars can be recall dressed up as skill.
- **The failure is quiet.** It doesn't have to cheat on purpose: knowing an event was coming shapes which dips it buys.
- **Our Part 1 holdout isn't enough.** A rule-based strategy has no memory of the future; a model does. Bars from before
  its cutoff are at best partly clean.
- **Hiding the symbol and the dates is weak.** Big days have recognizable shapes, raw price levels pin the date, volume
  and volatility fingerprint the period, and the model may not notice it is recalling.

## Honest tests, strongest first (Claude's answer in the lesson)

1. **Forward-only paper trading**, from the day you start: clean by construction, and the real goal.
2. **A post-cutoff replay**: bars from after the model's training cutoff.
3. **Anonymized older data with a contamination check**: rebase prices (to 100, or use returns), drop absolute volume,
   shift the dates and keep only the time of day; ask the model to guess the symbol and date first; compare the results
   on old and new data (a big gap means it is remembering, not trading).

If you only do one thing, do forward paper trading, with the contamination check alongside it.

## Rules for the harness

- Feed it closed bars, one at a time, never a file with future rows.
- Fill at the next open, with the engine's own costs; the model never sets its own fills.
- Freeze the prompt before looking at results (tuning on the test bars moves the goalposts).
- Run several repeats: the model's answers vary, so one pass is one sample.
- Log every prompt and decision; count prompt variants as trials, like settings in Part 1.
- Judge it like the strategies: at least 200 trades, results after costs, next to buy-and-hold and a random-entry baseline.
- Be realistic about usage: at 78 five-minute bars a day, a few hundred trades means many thousands of calls.

## The experiment ledger (`experiments/ledger.csv`)

One row per version of the trader, written **before** it trades.

| Column | What goes in it |
|---|---|
| `version` | a name you choose, for example `v1` |
| `model` | the exact model the trader runs on |
| `start_date` | the first day this version trades (on paper) |
| `end_date` | the day it stops; empty while it runs |
| `instructions_file_hash` | a hash of the instructions file, for example from `sha256sum CLAUDE.md`: one changed word means a new version |
| `symbols` | what it may trade |
| `bar_size` | for example `5 mins` |
| `risk_limits` | the limits the seatbelt enforces |
| `notes` | why this version exists |

Change the prompt, the model or a limit, and it is a new row with a new start date. Then every result is tied to exactly
what produced it.

## Two projects, not one

- `~/trading-lab`: the developer's project (code, tests, its own `CLAUDE.md` and `AGENTS.md`).
- `~/trading-desk`: the trader's project, its own private repository.
- Claude Code also reads `CLAUDE.md` files in parent folders, so the trader must not live inside the lab.

## The git identity check

- A new repository has no identity unless git has a **global** one. Claude will pick one if you don't: read what it did.
- Set it once: `git config --global user.name "Your Name"` and `git config --global user.email "ID+username@users.noreply.github.com"`.
- Check a repository: `git log --format='%h %an <%ae> %s'`.
- A force-push replaces the branch, but GitHub may keep the old commit reachable by its hash for a while. Fix the
  identity before the first push.
