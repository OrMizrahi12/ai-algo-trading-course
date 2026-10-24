# Lesson 6.4 prompts and commands

Everything typed in the lesson, in order. Lines that start with `!` run in the terminal from inside Claude Code
(shell mode). Lines that start with `/` are Claude Code commands. All three requests run in auto mode. Only the third
one uses the web; nothing here needs an IB connection.

## 1. A known-answer test

```text
/clear
```

```text
Let's prove our engine with a known-answer test. Make a tiny set of 12 hand-made SPY bars with two trades, one stopped out and one hitting its target, and work out by hand, in a table, every fill, cost, share count and the final equity. Then write the test that checks the engine gets exactly those numbers, and run it.
```

Claude reads the engine and the strategy interface first, puts the hand calculation in the test file's docstring, and
only then runs the test. Run it yourself any time:

```text
! uv run pytest tests/test_engine_known_answer.py -v
```

Then check the table by hand, row by row, the way you would check someone's homework. `cheat-sheet.md` has the numbers.

## 2. Cross-check with backtesting.py

```text
/clear
```

```text
Now cross-check against an independent library. Install backtesting.py, run spy_vwap_reclaim in it on the same two years of SPY bars with the same fills and costs as closely as it allows, and compare trade count, total return, win rate and the first ten trades side by side. Explain every difference you find.
```

Claude adds the library as a development dependency (`uv add --dev backtesting`), writes
`backtests/crosscheck_backtestingpy.py` and runs it, with zero costs and with costs. Run it and the whole test suite
yourself:

```text
! uv run -m backtests.crosscheck_backtestingpy
! uv run pytest -q
```

## 3. A map of engines

```text
/clear
```

```text
In a short table, compare backtesting.py, vectorbt, NautilusTrader and QuantConnect LEAN: what each is best at, how it models fills, whether it can trade live with Interactive Brokers, and when someone like me would outgrow our own engine. Check the current versions and official docs on the web and give me the links.
```

## Pause and try

1. Write your known-answer test with the first request, and check the table by hand.
2. Cross-check your engine with the second request, and read every difference.
3. Ask for the map of engines with the third request, and open its links.

You're done when your known-answer test passes, and your cross-check matches trade for trade, or every difference has a
reason. Your numbers will differ from the video, and that's fine.

## Try next (optional)

- Add a third hand-made trade that gaps through its stop at the open, work out its fill by hand, and add it to the
  known-answer test.
- Ask Claude to cross-check the vectorized EMA rule from Lesson 6.1 the same way.
