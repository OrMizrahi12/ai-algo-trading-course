# Lesson 9.1 prompts and commands

Everything typed in the lesson, in order. Lines that start with `!` run in the terminal from inside Claude Code
(shell mode). Lines that start with `/` are Claude Code commands. Every request runs in auto mode. Nothing here needs an
IB connection: the backtests use the cached bars.

## 1. Find ideas, with sources

```text
/clear
```

```text
Be my quant researcher. Find me intraday strategy ideas for US stocks and ETFs that we could test on our 5-minute SPY and QQQ data: search for published research and well-known practitioner ideas, and give me the source link for each. Add three hypotheses of your own based on what our lab found in modules 7 and 8. For every idea write the reason it might work, the source, and how we would test it. Put it all in research/journal.md as a table we will keep updating, and rank the ideas by how promising and how cheap to test they are.
```

In the video, Claude checked what the Lab found, re-ran the module 7 and 8 reports, searched the web for about a dozen
papers and practitioner sources, wrote `research/journal.md` (11 ideas, 3 of them its own) and, reminded by the
project's stop hook, committed and pushed it. About 9.5 minutes.

Open the journal with the Markdown preview: in VS Code, Ctrl+P, type `research/journal.md`, Enter, then Ctrl+Shift+V.

## 2. Run the research loop once

```text
/clear
```

```text
Let's run the research loop once by hand. Take the top idea in research/journal.md. Write its spec with our spec template, build the strategy with tests, run it through judge/scorecard.py, and write a strategy card in research/cards/ with the rules, the settings, the full scorecard, your verdict and the next step. Update the journal with the result, and commit. If it fails the judge, that is a finished experiment too.
```

In the video, Claude took H1 (switch the reversion strategies off on likely trend days), added the optional filter
`max_open_distance_atr` to both reversion strategies with tests (181 pass), fixed the threshold at 5 ATR from the
entries' distances alone, wrote the spec, ran eight judge runs in the background (about half an hour), wrote the card,
updated the journal and committed. Verdict: FAIL.

Reproduce one of the runs yourself (2 to 5 minutes each):

```text
! uv run -m judge.scorecard bollinger_rsi_reversion --symbol QQQ --set max_open_distance_atr=5.0 --trials 8
! uv run -m judge.scorecard bollinger_rsi_reversion --symbol QQQ --trials 8
```

The first line is the filtered run, the second the baseline. Swap in `vwap_stretch_reversion` and `--symbol SPY` for the
other six. The filter's tests:

```text
! uv run pytest tests/test_trend_day_filter.py -q
```

## Pause and try

1. Run the research request. Before you read the journal, write down which idea you would test first, and why.
2. Open the journal and check two sources: does each link go to the paper Claude named? Is the row marked * when the
   paper itself wasn't read?
3. Run the loop on the top idea of your own journal. Read the card's verdict and its next step.

You're done when your journal has ranked ideas with sources, and one idea has a strategy card with a verdict. Your
ideas and numbers will differ from the video, and that's fine. This is paper research, not a strategy to trade.

## Try next (optional)

- Ask Claude for the cheap check first: for an idea whose test plan starts with "check the plain statistic with
  pandas", run only that check before any strategy code.
- Before running a loop, write the settings into the spec and the journal row, so the result can't move the goalposts.
- Count every setting you try with `--trials`. Trying a second threshold for H1 on the same two years would be fishing.
