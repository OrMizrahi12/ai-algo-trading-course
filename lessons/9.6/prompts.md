# Lesson 9.6 prompts and commands

Everything typed in the lesson, in order. Lines that start with `!` run in the terminal from inside Claude Code (shell
mode: your own shell command, not a request to Claude). Lines that start with `/` are Claude Code commands. Every request
runs in auto mode. Nothing in this lesson needs IB Gateway or any broker: the data is free daily bars from Yahoo.

## 1. The strongest setup (a fresh session)

```text
/model
```

Pick Opus 5.5 in the list (it is saved as your default for new sessions). Then:

```text
/effort xhigh
```

xhigh is deeper reasoning than high, just below maximum. It uses more of your plan's usage; for a long, careful setup where
one mistake in the judge can waste the holdout, that is worth it.

## 2. Set everything up first (no strategy search yet)

```text
New research goal, and this time we do not stop until something passes. Our 5-minute runs in this module found nothing: 18 months of data, costs ate every edge, and every run had a small fixed budget. Now we use free daily bars from Yahoo from 2000 on, and a hard bar. Set everything up first, no strategy search yet. 1) Data: download daily bars for a broad universe you choose and fix now (at least 30 liquid US stock ETFs) into data/daily/. Everything from 2019-01-01 on is the sealed holdout: write it to data/holdout/daily/ and never read it. Research data ends 2018-12-31; split it into train and validation. 2) Protocol: write research/goals/pass_the_bar.md and commit it before any result. A candidate passes when, on the sealed holdout alone and after 0.10% round-trip costs, it makes at least 150 trades with a profit factor of at least 1.4. Signals on the close, fills at the next open. At most 6 frozen candidates per holdout opening, every configuration you try goes in the trial ledger, and a holdout is opened only once. Also write down now where the next fresh, never-touched holdout comes from if nothing passes. 3) The holdout judge: an evaluator that opens the holdout once for a frozen candidates file, refuses a second opening, and reports trades, profit factor, win rate, drawdown and profit factor by year, plus the lab's 8 rules from standards.yaml, unchanged, for context. judge/ is locked, so give me a patch to review and apply. 4) A Stop hook gate, so you can only stop when the holdout log shows at least one pass. 5) A research dashboard as its own small localhost page: every trial, the leaderboard, every holdout opening, and the holdout equity curve of each passing strategy, refreshing while you work. Commit, and tell me what to review.
```

In the video this took about 1 hour 47 minutes of Claude's work (auto mode). Our ask rule for `rm` commands stopped Claude
a few times when it cleaned up its own scratchpad clone; read each one and approve it only if it touches the scratchpad.
At the end Claude summarises what is in place, how it built and checked the judge patch, and what you should review.

## 3. Our answers

```text
Answers. 1) The bar stays as written: 150 trades and a profit factor of 1.4 is our bar, and we do not move it after seeing your numbers. Put your false-pass numbers and buy-and-hold next to every result, in the report and on the dashboard, so nobody reads a pass as proof. 2) Equal weight is fine. Make it long only: no shorts, because we model no borrow cost. Update the patch and tell me when it is ready to apply.
```

About 17 more minutes: a luck number next to every result, shorts refused, and the patch updated.

## 4. Apply the judge patch yourself

The judge folder is locked, so the holdout judge arrives as a patch. Read it, then apply and test it in shell mode:

```text
! git apply research/patches/0003-judge-daily-holdout.patch && uv run pytest -q 2>&1 | tail -3 && uv run -m judge.holdout status
```

The tests take a few minutes; Claude Code moves a long command to the background and tells you when it finishes. In the
video Claude then committed exactly the applied files (822 tests, H1 sealed and unopened). Your patch number and test
count will differ.

## 5. The research dashboard

```text
Start the research dashboard in the background so it keeps running while you work, and check that it answers.
```

```text
One change: run it detached with setsid and nohup, logging to research/dashboard.log, so it survives this session and is not one of your background shells. Then stop the background shell.
```

Open http://127.0.0.1:8766 in your browser. It refreshes every 10 seconds.

## 6. Turn the gate on, then set the goal

The Stop gate is your switch. In shell mode:

```text
! echo pass_the_bar.md > research/goals/ACTIVE && git add research/goals/ACTIVE && git commit -q -m "goal: pass the bar on" && git log --oneline -1
```

Claude starts working at once. Type the goal while it works; it is queued, and
ctrl+x ctrl+s sends it now:

```text
/goal Follow research/goals/pass_the_bar.md exactly. Done when uv run -m judge.holdout status shows at least one candidate that passed the bar on a sealed holdout, the dashboard shows its holdout equity curve, and everything is committed. Search broadly, with subagents per strategy family if that helps. Never change the bar, the judge or a sealed holdout. No turn limit.
```

In the video Claude worked for 30 minutes in one turn: three researcher subagents, a fourth family of its own, a selection
rule committed before the results, five frozen candidates, one opening of H1, four of five passing the bar. Then "Goal
achieved".

## 7. Profit factor by year, and a second opening that is refused

Same session:

```text
Add profit factor by year for every opened candidate to the dashboard, read from the holdout log only. Nothing gets reopened. Tell me when the page shows it.
```

Then try to open the holdout again yourself (it must be refused, and nothing may be opened):

```text
! uv run -m judge.holdout open research/goals/candidates/H1.yaml
```

## Pause and try

1. Write your own bar and protocol (start from `protocol-template.md`) and commit it before any result.
2. Seal a holdout, and have Claude write a judge that opens it once, as a patch you review and apply yourself.
3. Turn the gate on, give `/goal` the done condition, and let it run.

You are done when your dashboard shows every trial and every opening, buy-and-hold beside every pass, and a second
opening is refused.
