# Student kit: Lesson 15.1, The multi-agent desk

Module 15: Advanced agent designs · AI Algorithmic Trading with Claude Code and Interactive Brokers

Until now one trader decided on every bar. In this lesson the desk becomes a **team**: an **analyst** reads the market
and proposes a move, a **risk manager** checks it against the hard rules and can **veto** it, and a **devil's advocate**
argues against it. The trader still makes the final call. A written rule settles disagreement (a tie or a veto means
wait), every view goes into a **decision record** in the journal, and the team's cost per bar is measured on replayed
bars before anything runs live. Then the team watches one live day next to the desk, as a dry run, and we compare the
two journals bar by bar, honestly.

## What's in this kit

| File | What it is |
|---|---|
| `prompts.md` | Every request typed in the lesson, in order, what Claude did with each one, and the pause-and-try exercise |
| `cheat-sheet.md` | The words, the protocol and the vote rule, the cost tables, the live comparison and what one quiet day can and can't say |
| `trading-desk/` | The files this lesson added or changed in the desk, as committed at the end of the build: the three role files in `.claude/agents/` (`analyst.md`, `risk-manager.md`, `devils-advocate.md`), `desk/team.py` (the protocol and the vote, in code), `desk/team_cost.py` (the cost replay), `desk/__main__.py` (the `--team` switch), `desk/heartbeat.py` and `desk/model.py` (the team block in the journal), `tests/test_team.py`, `README.md` and the cost report `experiments/team-cost.md` (with its raw numbers in `team-cost.json`). Copy them over your desk |

## Before you start

- Your `~/trading-desk` from the earlier lessons: the heartbeat, the skills, the guardrails, the journal, the vault and
  saved snapshots of earlier bars in `data/desk/snapshots/` (the cost replay reads them).
- Claude Code in the terminal, signed in with your subscription.
- A paper account in IB Gateway or TWS for the live part (the team never places an order there: it is a dry run).
- Time on our computer: about 13 minutes for Claude to build, test and measure the team; a few minutes for the replay
  alone; the live part runs as long as the market session you give it.

## Try it yourself

1. Send request 1 in `prompts.md`, or copy the kit's files over your desk and run `uv run pytest -q`.
2. Run `uv run -m desk.team_cost` and read `experiments/team-cost.md`: what one bar costs with the team, against the
   single trader, on bars you already have.
3. Only then, on a market day: request 3, the team next to your desk as a dry run with its own client ID and journal.
4. After the close: request 5, the comparison, and the honest list of what it can and can't say.

You're done when you have a cost table, and an honest list of what your comparison can and can't say. Your code,
numbers and Claude's answers will differ from the video, and that's fine.

## Good to know

- **Subagents, or separate calls.** We asked for subagents. Claude probed first and found two problems: a subagent can
  only use the tools its parent has (our trader has only its skills, so a subagent could not read the bar's data), and
  this version starts subagents in the background, so the trader answered before the analyst had. So each role is its
  own `claude -p` call with no tools, reading the full snapshot, and plain code runs the order and the vote. The role
  files in `.claude/agents/` are still the roles' instructions.
- **Off by default.** Without `--team` nothing changes. `uv run -m desk --team` turns the team on.
- **The cost is real.** Every role re-reads the whole snapshot on every bar, while the single trader sends only what
  changed. On our replay a quiet bar cost about 10 times the single trader, a bar with a proposed buy about 19 times.
  These are usage figures at list prices, not a bill on a subscription.
- **One quiet day proves little.** On our live day the analyst said wait on every bar, so the risk manager and the
  devil's advocate were never asked. Agreement on a day of waits is nearly empty. The next evidence is replayed bars
  where the analyst does propose a buy.
- **The live watcher is not in this kit.** On camera Claude wrote a small script outside the desk's folder that reuses
  the desk's code as a dry run on its own client ID, with its own journal in `data/team/`. Ask for the same in your own
  words (request 3); keep it out of the desk's code so the desk's forward test stays clean.

Paper account only. Educational content, not financial advice; nothing here is a promise of profit or a recommendation.
