# Lesson 7.4 prompts and commands

Everything typed in the lesson, in order. Lines that start with `!` run in the terminal from inside Claude Code
(shell mode). Lines that start with `/` are Claude Code commands. Every request runs in auto mode. Nothing here needs an
IB connection: the research uses the web, and the backtests use the cached bars.

## 1. What does the research say?

```text
/clear
```

```text
What do published and independent tests say about the opening range breakout on US stocks and ETFs? Look on the web for the main studies and for independent replications, especially results after costs. Give me a short summary with links: what each claims, on what data and period, whether it used leverage or short selling, and what a skeptic should check before believing it.
```

Claude runs a few web searches and answers with the main studies, the independent replications, a skeptic's checklist
and links. Read its first line: it says whether it read the papers themselves or only search summaries.

## 2. Read the papers themselves

```text
You only read search summaries. Open the two papers themselves and confirm the rules that matter for us: long and short, leverage, position sizing, costs and slippage, the stop, and the exit. Correct anything in your summary that was wrong.
```

Claude fetches both PDFs, extracts their text, and answers with the rules as written, side by side for the two papers,
then a list of corrections to its own first summary, and what it all means for our lab. If a download or a tool fails
on your computer, Claude usually finds another way; let it.

## 3. Build and test the opening range breakout

```text
/clear
```

```text
Build an opening range breakout on our Strategy interface, with a spec and tests: take the high and low of the first N minutes, buy when a 5-minute close breaks above the high, stop at the low of the range, exit at the close. Long only, no leverage, our usual costs. Add a variant that only buys when the price is also above VWAP. Backtest N = 5 and 15 minutes, with and without the VWAP filter, on QQQ and SPY, and put our table next to what the two papers claimed. Explain the differences.
```

The `/clear` wipes the research from the session. In the video, Claude checked the repo for which two papers we meant,
searched again, and said in its answer which papers it assumed. Then it wrote the strategy, its spec and 20 tests, fixed
one test's hand-made data, ran the whole suite (151 tests), ran the 8 backtests, checked why the VWAP rows matched the
plain rows, and committed. Run them yourself any time:

```text
! uv run pytest -q
! uv run -m backtests.orb_comparison
```

## 4. Is the best row safe to trade?

```text
QQQ with a 15-minute range looks like the winner. Is it safe to pick that row and trade it? Answer briefly, without changing any code: what could make it look better than it really is, and what would you check before trusting it?
```

## Pause and try

1. Run the research request, then send Claude to the papers. Compare its corrections with its first summary.
2. Build and test the strategy with the third request, and read the "Why the differences" section.
3. Ask the fourth question about your own best row.

You're done when your strategy passes its tests, your table has all eight rows, and you can give two reasons why the
best row isn't a winner yet. Your numbers will differ from the video, and that's fine.

## Try next (optional)

- Run the same comparison with 10, 20 and 30-minute ranges. Does the result change smoothly, or jump around?
- Rerun it at double and triple costs, the way `backtests/reversion_comparison.py` does in Lesson 7.2.
- Module 8 turns Claude's whole checklist (ranges, costs, concentration, bootstrap, out-of-sample, benchmark) into tools.
