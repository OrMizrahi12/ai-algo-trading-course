# Lesson 15.3 prompts

Everything typed in the lesson, in order. Lines that start with `/` are Claude Code commands. Interactive Claude Code
sessions in `~/trading-desk` (auto mode). Paper account only.

## 1. Before the open: the stock-open agent

At 12:02 UTC, an hour and a half before the US open:

```text
/clear
```

```text
Today we add a stock-open agent next to the desk. Before the US open, run the lab's gap scanner from lesson 7.3 in ~/trading-lab (its own client ID) to get today's watchlist. Then read each candidate yourself: the gap, relative volume, the daily chart and any headline IB gives us, and pick at most two names to watch, with a written plan for each: what would make you buy, where the stop goes, and when you'd give up. Save the picks and plans to today's daily note in the vault. Then build the open-window loop: from the 13:30 UTC open it gives you each finished 5-minute bar of those names and you decide bar by bar, with the same risk layer, review gate and settled-bars rule as the desk. New entries only on bars that start before 14:30 UTC, everything flat by 15:00 UTC. Its own client ID and its own journal. Leave CLAUDE.md, the plugin and the skills untouched: the SPY desk's forward test starts today and their hash must not change. Paper only. Tests, then commit.
```

On our computer Claude worked for about 10 minutes. It read the desk and the lab, and noted that the lab's limits file
lists only SPY and QQQ. It ran the lab's `scanner.py` on client ID 4 (read-only) at 12:03 UTC: **0 stocks measured, 0
passed**. IB refused the gap scans for this paper account (error 492, missing scanner permissions), and before 09:30 New
York there are no bars of today to measure a gap against. Claude did not make up a watchlist.

It built the loop anyway: its own instructions in `.claude/open-window/constitution.md` (outside the files the SPY desk's
hash covers), `desk/openwindow.py` (window times, a parser for the picks in the note, a journal per name, the trader model,
a heartbeat per name, a reviewer and the runner), `tests/test_openwindow.py` (30 new tests; two failed at first, both test
mistakes), a real `claude -p` check that the new agent has no tools and does not see the SPY desk's instructions or skills,
today's daily note with an empty picks section, and a README section. 467 tests passed, the SPY desk's instruction hash was
unchanged, and it committed.

Its answer ended with four things to know before picks exist: no stock can be bought yet (the lab's limits list only SPY
and QQQ); the lab's risk budget is shared with the SPY desk; the SPY trader would see this agent's positions; and the lab's
docs did not list client ID 10 yet.

## 2. Our decisions

```text
Thanks. My decisions: 1) Keep the SPY desk's forward test clean. Today the open agent runs in dry run only: no orders, none of the shared budget used, and the SPY trader never sees its positions. 2) Leave the limits file alone. In dry run, journal what the gates would say, so a name that isn't listed shows up as a refusal. 3) The bars arrive about 15 minutes late, so widen the window: new entries on bars that start before 15:00 UTC, flat by 15:30. 4) Add client 10 to the lab's AGENTS.md list. Commit. At 13:50 UTC I'll ask you to rerun the scanner and pick.
```

Claude found that the lab's executor skips its risk check in dry run, so an unlisted name would have passed as a harmless
"would place". It wired the lab's risk check into the open agent's dry run and made dry run the default (sending orders
needs an explicit flag), widened the window (entries on bars that start before open + 90 minutes, flat at open + 120
minutes, so the times follow the New York open when the clocks change), added a line to the agent's instructions that the
data is 16 to 21 minutes old, added tests (471 passing), committed, and committed the lab's `AGENTS.md` change.

## 3. Start the loop (before the open)

In a second terminal, in `~/trading-desk`:

```text
uv run -m desk.openwindow
```

It runs in dry run by default, on client ID 10, and re-reads today's note every minute.

## 4. After the open: rerun the scanner and pick

At 13:50 UTC, in the same session:

```text
It's 13:50 UTC and the market is open. Rerun the gap scanner now, read the candidates yourself, and write at most two picks with their plans into today's note. The loop on the right has been running in dry run since 12:39 and re-reads the note every minute.
```

The first two scanner runs were stopped by Claude's own time limits (the scanner takes about 6 seconds per name and writes
its list only at the end). The third ran in the background with no limit and finished about 14:08 UTC: 49 stocks passed the
lab's filters. Every headline request timed out, so the picks rest on price and volume only. Claude wrote two picks into
the note, each with `Buy if:`, `Stop:` and `Give up:` (see `trading-desk/vault/Daily/2026-10-26.md`), and checked that the
loop could parse them.

## 5. The journal so far

```text
Show me the loop's journal for RRC and HHH so far: each bar, the decision and the reason, in a short table.
```

The finding: on the RRC 13:55 UTC bar the plan's buy rule was met, but the model saw that RRC has no entry in the limits
file and answered `wait` itself. So the desk's own limits check never ran, and the journal had no `refused_by_risk_limits`
record. Claude proposed a small change to the open-window instructions, and did not make it while the loop was running.

## 6. The fix

```text
Yes, make that change and commit it. I'll restart the loop when you're done.
```

New wording in `.claude/open-window/constitution.md`: judge the plan only; a name missing from the risk limits is not a
reason to wait; if the plan's buy condition is met, answer `buy`, and the desk checks the limits itself and journals the
refusal. One test, 472 passing, the SPY desk's hash unchanged, and one commit that also carries the day's picks.

Then restart the loop in its terminal: `Ctrl+C`, then

```text
clear; uv run -m desk.openwindow
```

## 7. After the window: the result

At 15:35 UTC, after the loop disconnected on its own at 15:30:

```text
Back to the open-window agent. Its entry window is over. Give me today's result for RRC and HHH from its journal: what it decided on each bar and why, whether its plans' buy rules were ever met, and what today taught us about trading the open on delayed data. Write a short review into today's note.
```

28 decisions, all `wait`, in a dry run. RRC's buy rule was met once and the agent still waited (the problem fixed in step
6); HHH's never. The would-be RRC fill is labelled "not a real result": it was not reachable on delayed data. The review is
the "Open-window result" section of the note in this kit.

## Pause and try

1. Before the open, run your scanner and ask Claude for at most two picks, each with `Buy if:`, `Stop:` and `Give up:`.
2. Run an open-window loop in dry run, with its own client ID and journal, and a window that ends.
3. After the window, ask for the journal, and check every bar where a buy rule was met.

You're done when your journal shows each bar's decision and reason, and you know whether a refusal came from the plan or
from the desk's limits.
