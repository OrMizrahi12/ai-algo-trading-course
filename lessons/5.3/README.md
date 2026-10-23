# Student kit: Lesson 5.3, A strategy is a spec

Module 5: Data and strategy foundations · AI Algorithmic Trading with Claude Code and Interactive Brokers

Before any strategy code, the strategy is written down. In this lesson you gave Claude a trading idea in plain English
(SPY 5-minute bars, buy when the close crosses back above VWAP while the 20-bar EMA is above VWAP, a stop under the
swing low or 1.5 ATR, a 2R target, flat before the close) and asked it to turn the idea into a spec, asking you about
anything ambiguous first. Claude asked four questions with options (the cross rule, the stop rule, the entry fill, the
flat time and trade limit), then wrote a commented `TEMPLATE.yaml` and the filled `spy_vwap_reclaim.yaml`, marking
every assumption it added. In a second session, in plan mode, Claude designed one `Strategy` interface that the
backtester (Module 6) and the paper trader (later) will both use, coded the strategy from its spec, and tested it with
small hand-made bar sequences. Two tests failed because of the test data, Claude found out why with real numbers, and
51 tests passed. A detour onto a Git branch ended with a merge back into `main`.

The strategy is an example of how to write a spec, not a recommendation. Its results are unknown until we test it in
Module 6, and they may well be poor.

## What's in this kit

| File | What it is |
|---|---|
| `prompts.md` | Every request and command typed in the lesson, ready to copy, plus the pause-and-try exercise |
| `cheat-sheet.md` | The sections of a spec, the four questions and the answers chosen, R and 2R, look-ahead, the Strategy interface and its timing rule |
| `trading-lab/strategies/specs/TEMPLATE.yaml` | The spec template: every section a strategy can have, with a short comment on every field |
| `trading-lab/strategies/specs/spy_vwap_reclaim.yaml` | The filled spec for the lesson's idea, assumptions marked `ASSUMPTION` |
| `trading-lab/strategies/base.py` | The one `Strategy` interface: `Position`, `Entry`, `Exit`, `Strategy.on_bar` and `check_bracket` |
| `trading-lab/strategies/spy_vwap_reclaim.py` | The strategy coded from its spec; its numbers live in `SpyVwapReclaimParams` |
| `trading-lab/strategies/__init__.py` | Makes the folder a Python package |
| `trading-lab/tests/test_strategy_spy_vwap_reclaim.py` | Offline tests on hand-made bars: entry, capped stop, stop hit, target hit, time exit, the first-15-minutes filter and more |

## Before you start

- The Trading Lab from Modules 3 to 5, with `uv`, the Stop hook from Lesson 3.6 (it asks Claude to commit and push
  before it stops) and the `lab-reviewer` agent from Lesson 3.5.
- `indicators.py` from **Lesson 5.2**. The strategy and the tests import its `vwap`, `ema` and `atr` and its
  `SESSION_TZ`. Without it, `import indicators` fails.
- `pandas` and `pytest` in the project (both were added in earlier lessons).
- No IB connection is needed: nothing in this lesson talks to Interactive Brokers.

## Try it yourself

1. In your `trading-lab` folder, start `claude`, run `/clear`, and send the first request in `prompts.md` (or your own
   idea in the same shape). Answer Claude's questions; pick the options that match what you really mean.
2. Open the spec with `! code -g strategies/specs/<your_spec>.yaml` and read every `ASSUMPTION` line. Change any value
   you disagree with in the YAML, not in code.
3. `/clear`, press **Shift+Tab** until the footer says **plan mode on**, and send the second request. Read the plan
   before you approve it, especially the judgment calls.
4. Run the tests: `! uv run pytest`.

You're done when every rule in your spec is a number or a time, every guess is marked as an assumption, and your
tests pass. Your idea, numbers and Claude's wording will differ from the video; that's the point.

## Good to know

- Claude committed the second session on a new branch, `strategy-interface`, because its Git guidance says not to
  commit straight to the default branch. For a solo lab we asked it to merge into `main`, push and delete the branch
  (third request in `prompts.md`). From then on it committed to `main`.
- In the video Claude skipped the reviewer pass that its own plan listed, and said so. Ask for it if you want it.
- The spec's costs are zero on purpose, as placeholders: set real commissions and slippage before you trust any
  backtest.
- The strategy only decides. Fills, share count and costs belong to the engine (the backtester in Module 6, the paper
  trader later).

## Safety

Paper trading only. Educational content, not financial advice, and nothing in this lesson is a recommendation to buy
or sell anything. No orders are sent in this lesson: the strategy code never talks to IB.
