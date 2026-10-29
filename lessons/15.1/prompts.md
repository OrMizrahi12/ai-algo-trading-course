# Lesson 15.1 prompts

Everything typed in the lesson, in order. Lines that start with `/` are Claude Code commands. Interactive Claude Code
sessions in `~/trading-desk` (auto mode). Paper account only.

## 1. Ask for a team

```text
/clear
```

```text
Turn this desk into a team: an analyst, a risk manager and a devil's advocate, each a subagent with short instructions in .claude/agents/. On each bar the trader asks the analyst first, and asks the other two only when the analyst proposes a trade. Record every view and the final decision in the journal. A tie or a veto means wait. Add tests, and measure what the team costs per bar compared with the single trader.
```

On our computer Claude worked for 13 minutes 7 seconds. It read how the desk is built (the guardrail hook blocked one
shell command, so it used its Read tool instead) and took a baseline from the journal: the single trader cost about
2.4 cents a bar and under 6 seconds.

Before building anything it ran one cheap probe of a real subagent, and found two problems:

- The subagent ran in the background, and the answer went out before the subagent had finished. A setting can make a
  subagent wait, so that part is fixable.
- A subagent can only use the tools its parent has. Our trader has one tool, its skills, so a subagent could not even
  read the bar's data. The probe said so: the helper refused to start, because its tools list resolved to nothing.

So it settled the design and said plainly that it departs from what we asked: the three roles are short instruction
files in `.claude/agents/`, but each runs as its own `claude -p` call, and plain code runs the order and the vote in a
new module, `desk/team.py`. It wired a `--team` switch into the session, the heartbeat and the command line (16 lines
in three files), wrote `tests/test_team.py` (two tests failed at first: one used the real clock, one read the orders the
wrong way; both were mistakes in the tests) and got 374 tests passing: the 305 we had plus 69 new.

Then it measured. One real call per role on a saved snapshot cost about 13 cents. It wrote `desk/team_cost.py`, which
replays saved SPY bars through the real model with no orders: six bars as the single trader, six as the team, and a few
bars on the full path, where a made-up buy proposal makes all three roles answer. Older snapshots lacked a newer field,
so it filled it in the way the heartbeat would. The report is `experiments/team-cost.md`.

Its answer listed what it built, the departure, the cost table (see the cheat sheet), why it costs so much, and choices
for us: how it read "tie" (the vote rule in the cheat sheet), that it did not add a ledger row, and that cheaper roles
would cut the cost the most.

## 2. Keep the rule, commit

```text
Keep the vote rule as it is. Show me the cost table, then commit.
```

One commit: "Add the team: analyst, risk manager and devil's advocate consulted before the trader (--team)". 376 tests
passed, no failures, and no orders were placed in any run.

## 3. Watch it on live bars, as a dry run

Two days later, with the market open and the live SPY desk running:

```text
/clear
```

```text
New topic. Let's watch the team from the multi-agent lesson on today's live bars. Run it next to the live SPY desk without touching it: dry run, its own client ID and its own journal, and leave CLAUDE.md, the plugin and the skills alone, so the forward test stays clean. Start it for me, let it see several bars, then show me a decision record where the roles disagreed, if there is one.
```

Claude read how the team is launched and checked that a dry-run broker can't touch the live desk's orders (placing and
cancelling become no-ops). It wrote a small watcher outside the repo that reuses the desk's code on client ID 11, with
its own journal and state in `data/team/`. The first launch failed on an import error (the script lived outside the
repo), so it relaunched with the right path, connected, and put a monitor on the log. It noted one caveat: the watcher
sees the same paper account as the live desk.

- Bar 1: the team and the trader cost 30 cents.
- An event arrived that wasn't ours: the broker's broadcast of the lab's separate QQQ strategy. The watcher ignored it.
- Bar 2: 3 cents, because the other two roles are asked only after a proposed buy.
- After three bars the journal's team block said `go: false`: the analyst proposed wait, not a buy, zero yes votes. No
  roles had disagreed yet.
- After four bars, a summary: SPY's daily trend was down, below its 9- and 21-day averages, and the bars arrived about
  17 minutes late (delayed data). "A disagreement needs a proposed buy first", and Claude would not invent a record.
- Bar 5 cost 3 cents again (almost certainly another wait); the session stood at 42 cents.

## 4. Keep it running, invent nothing

```text
Keep the watcher running until the entry cutoff, and don't invent anything. After the close we'll compare the team with the live desk on the same bars.
```

Claude re-armed its monitor to speak up only on a proposal other than wait, an error or the cutoff, and noted that both
journals are keyed by the same bar times, so they line up bar by bar.

## 5. Compare, honestly

After the close:

```text
The market is closed. Compare the team with the live single trader on the bars they both saw today: how often they agreed, any bar where they differed and why, how long each took per bar, and the usage per bar. Then tell me honestly what one quiet day can and can't say about a team.
```

Claude lined up the two journals: 54 common bars (14:10 to 18:35 UTC) and the same action on 54 of 54, all wait. The
table, the differences, the one real difference and the can and can't say list are in the cheat sheet.

## Pause and try

1. Ask Claude to split your desk into roles with short instructions, with the order and the vote enforced in code.
2. Measure the cost per bar against the single trader on replayed bars, before anything runs live.
3. Run the team next to your desk as a dry run, and compare the two journals, bar by bar.

You're done when you have a cost table, and an honest list of what your comparison can and can't say.
