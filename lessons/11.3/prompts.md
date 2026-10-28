# Lesson 11.3 prompts and commands

Everything typed in the lesson, in order. Lines that start with `/` are Claude Code commands; a line that starts with `!`
inside Claude Code runs a shell command directly (shell mode), and Claude sees its output too. Every request below was
sent in auto mode, in `~/trading-desk`.

## 1. Write the constitution

```text
/clear
```

Then send:

```text
Help me write this desk's constitution in CLAUDE.md: the instructions the trader reads on every bar. Interview me first with a few questions (style, risk, what to avoid), then write it: mission, style, risk rules, how to think on every bar, and the output contract our heartbeat expects. Keep it under 120 lines and keep the paper-only line. Then hash it and add Trader v1 to experiments/ledger.csv, and commit.
```

Claude read the scaffold and the heartbeat first, then interviewed us in four tabs. Our answers:

| Question | Our answer |
|---|---|
| Style: what trading style on 5-minute SPY bars? | 4. Patient, mostly wait (trade only clear setups, wait on most bars) |
| Risk: how much per trade, how many trades a day? | 1. Cautious: 0.5R typical, max 1R (R = 1% of the account lost if the stop hits; about 3 entries a day; reward-to-risk at least 2) |
| Avoid (pick all that apply) | Chasing and revenge trades; moving or widening stops; trading on stale or thin data; and our own line: `Never average down into a loser, and be flat 10 minutes before the close` |
| Hash target: which file should be hashed for the Trader v1 row? | 2. Make CLAUDE.md the only instructions (one source: the journal hash equals the ledger hash) |

Claude asked the fourth question itself: it found that the heartbeat hashed a second file, `desk/instructions.md`, as
the system prompt. About a minute and a half later: `CLAUDE.md` written (77 lines), `desk/model.py` sends it as the system
prompt, `desk/instructions.md` deleted, the Trader v1 row added with the hash `73a60f566379`, committed. Its report also
said two things to know: `CLAUDE.md` was sent twice per bar, and some rules are advice, not enforced.

## 2. Once per bar

```text
Good catch on the double send. Make CLAUDE.md reach the trader exactly once per bar, keep the hash it records the same, run the tests, and commit.
```

About a minute and a half. Claude tested the options of `claude -p` and measured by asking the model to quote every place
the paper-only sentence appears in its context. It added `--setting-sources user,local`, committed, and reported one miss
in its own first check. Note its last point: with the `user` source, a personal `~/.claude/CLAUDE.md` would still reach
the trader on every bar.

## 3. Nothing from our settings

```text
Yes, switch it to local. The hash should describe everything the trader sees, so my personal settings must not leak in. Test and commit.
```

Half a minute. Claude chose an empty source list (`--setting-sources ""`) instead of `local`, because `local` could still
load a `.claude/settings.local.json` that git ignores, and added a test that pins it. It said honestly what it hadn't
proved: the hash doesn't cover the tool list or the environment the model sees.

## 4. Read it yourself

```text
! wc -l CLAUDE.md && git log --oneline -4 && head -60 CLAUDE.md
```

Then scroll up through the file. (`head -60` stops before the output contract; open `CLAUDE.md` to see all 77 lines.)

## 5. Trader v1 on a live bar (a terminal in `~/trading-desk`, market hours, paper Gateway)

```bash
git log --oneline -1 && sha1sum CLAUDE.md | cut -c1-12
uv run -m desk --once
uv run -m desk
```

`--once` handles the newest closed bar and stops (a restart never repeats a bar it already handled). The loop picks up
each new bar; stop it with Ctrl+C. Then read the last decision and compare the hash with the ledger:

```bash
tail -n 1 data/desk/journal.jsonl | jq '{bar, instructions, action: .decision.action, reason: .decision.reason}'
grep "Trader v1" experiments/ledger.csv | cut -d, -f1,5
```

On our computer the 13:50 UTC bar got `wait`: "Last 5-minute bar has very thin volume (35k), so data looks incomplete.
Price is below ema9/ema21 (smoothed averages) and vwap (volume-weighted average price) after a gap down; rsi14 (momentum,
0-100) is 41. No clear long setup, so I stay out." One bar and one `wait` is not a result.

## Pause and try

1. Ask Claude to interview you and write your own trader's constitution in `CLAUDE.md`, with the five parts.
2. Make it the only instructions, hash it, and add your Trader v1 row to the ledger.
3. Ask which of your rules the code enforces and which are only words.

Paper only.
