# Lesson 15.4 prompts

Everything typed in the lesson, in order. Lines that start with `/` are Claude Code commands; a line that starts with `!`
runs a shell command from inside Claude Code. Interactive Claude Code sessions in `~/trading-desk` (auto mode). Paper
account only.

## 1. Ask for a protocol, before any result

```text
/clear
```

```text
Write a forward-test protocol for our AI trader in experiments/PROTOCOL.md, fixed before we look at any results: the trader version from the ledger, the period, the symbols, the metrics, the baselines (random entries matched on frequency and risk, buy-and-hold SPY, and the ORB strategy on the same days), the minimum number of trades, and when we stop. Include a table of how many trades it takes before a given Sharpe ratio can be told apart from luck. Then build the report script and commit both.
```

On our computer Claude worked for 6 minutes 20 seconds:

- It read the repo first: the ledger, the experiments folder, the desk's trade records and review code, and in the lab
  the metrics, the ORB strategy and module 8's `reports/luck_vs_skill.py` ("How luck fools us").
- It checked the version: the ledger's current row, "Trader v2.2 + settled bars", matches the instruction hash the code
  produces today, and it said it had not looked at any trade result.
- It checked which journal fields mark the run mode (so only the plain desk counts) and how the lab scores a trade in R,
  then locked in the design: a sealed report that shows only coverage and trade counts until the stop rule is met, using
  only plain-mode bars under that hash, measured in R.
- It wrote `desk/forward_report.py` and the tables, then `tests/test_forward_report.py`: the protocol and the script must
  agree, the table must hold up under simulation, the report must stay sealed. One test failed; Claude found the flaw in
  the test (its fixture already held a plain record for the bar meant as a decoy) and rewrote it. 437 tests passed.
- A quick look at the unsealed report on synthetic data only (headed EXPLORATORY: do not quote these numbers) found two
  real bugs: the random arm's trades per replicate used the wrong divisor, and a flat daily series gave a Sharpe of 1e15
  instead of "n/a". Both fixed, plus a check that flags the report when more than 25% of the random draws are dropped.
- 437 tests passed again, and the protocol and the script went into one commit together.

Its answer: "I never read any trade result, so the protocol was fixed before any outcome was visible." Then what the
protocol fixes, the choices you can still change before the period starts, and one honest gap: the random baseline and
the ORB run have only run on synthetic data, because no real bars of the period existed yet. Details in the cheat sheet.

## 2. Print the tables

```text
! uv run -m desk.forward_report --table
```

The two tables (in the cheat sheet). Claude added that they match the tables in `experiments/PROTOCOL.md` exactly, and a
test asserts it, so the protocol can't drift away from the script without the test suite failing. Two things the table
shows: reaching the 100-trade minimum won't settle much, and the bar for "better than luck" falls slowly.

## 3. Day one: run the sealed report

After the close of the first day of the test period, in the desk session:

```text
Today was day one of the forward test. Run the sealed report, exactly as the protocol says, and read it to me: does today count, how many scored trades we have, and what we are allowed to conclude so far.
```

Claude read the protocol and its commit first, then ran `uv run -m desk.forward_report` in its sealed form (no
`--unseal`, no `--write`). Its reading: day one counts (no dropped days, the hash unchanged, the protocol file has a
single commit); zero scored trades (the desk said wait on every bar); we can say the test started cleanly; we can't say
anything about whether the trader is good, bad or lucky; no forecast.

## Pause and try

1. Before you look at any result, ask Claude for a protocol, with the version, the period, the symbols, the metrics, the
   baselines, a minimum number of trades, and a stop rule.
2. Have it build a sealed report, and commit both together.
3. Print the trades table for your own trade rate.

You're done when the protocol is committed before the period starts, and your report says nothing but data quality
until the stop.
