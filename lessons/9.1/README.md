# Student kit: Lesson 9.1, Claude as a quant researcher

Module 9: The strategy factory: goal-driven research loops · AI Algorithmic Trading with Claude Code and Interactive Brokers

Module 8 ended with a judge, and nothing passed it. So where do new ideas come from? In this lesson Claude becomes the
Lab's quant researcher. First it searches published research and well-known practitioner ideas for intraday ideas we
could test on our 5-minute SPY and QQQ bars, adds three hypotheses of its own from what the Lab found in modules 7 and
8, and writes everything into a research journal (`research/journal.md`): eleven ideas, each with the reason it might
work, its source, how we would test it, and a score for how promising and how cheap to test it is. Then we run the
research loop once by hand on the top idea, H1 (switch the two reversion strategies off on likely trend days):
hypothesis, spec, code with tests, the judge from Lesson 8.4, and a strategy card. H1 fails the judge. The card records
it as a finished experiment, and Claude recommends stopping instead of fishing for a better threshold.

## What's in this kit

| File | What it is |
|---|---|
| `prompts.md` | The two requests typed in the lesson, the commands, and the pause-and-try exercise |
| `cheat-sheet.md` | The words, where ideas come from, the ranked journal, the research loop, and H1's result |
| `trading-lab/research/journal.md` | The research journal after the lesson: plain-English terms, what the Lab found in modules 7 and 8, the ranked table of 11 ideas with sources and test plans, the suggested order, cautions and the log (H1 marked as failed) |
| `trading-lab/research/cards/h1_reversion_trend_day_filter.md` | The strategy card for H1: idea, rules, settings and where they came from, all eight judge results, the verdict (FAIL), the full scorecard of the best run, the next step, how to reproduce it, and the other seven scorecards verbatim |
| `trading-lab/strategies/specs/reversion_trend_day_filter.yaml` | H1's spec, filled from the Lab's spec template, with the threshold written down before any run |
| `trading-lab/strategies/session_clock.py` | Gains `open_distance_atr` (how far the price is from today's open, in ATR) and `trend_day_blocked` |
| `trading-lab/strategies/bollinger_rsi_reversion.py`, `vwap_stretch_reversion.py` | Both reversion strategies with the new optional setting `max_open_distance_atr` (off by default; exits are never blocked) |
| `trading-lab/strategies/specs/bollinger_rsi_reversion.yaml`, `vwap_stretch_reversion.yaml` | Their specs, bumped to version 2 for the new setting |
| `trading-lab/tests/test_trend_day_filter.py` | Offline tests for the filter: the distance in ATR, no look-ahead, gaps not counted as a move, unknown history blocked, exits never blocked, off by default |
| `trading-lab/judge/scorecard.py` | The judge from Lesson 8.4 with `vwap_stretch_reversion` registered in `STRATEGIES` |

The lesson also added one line about the journal and the cards to the layout section of `AGENTS.md`. Nothing else in
the Lab changed; no new dependency.

## Before you start

- The Trading Lab with the two reversion strategies (Lesson 7.2), the spec template `strategies/specs/TEMPLATE.yaml`
  (Lesson 5.3), the day-type report `reports/reversion_by_day_type.py` (Lesson 7.2), and the judge
  `judge/scorecard.py` with `judge/standards.yaml` (Lesson 8.4).
- Two years of SPY and QQQ 5-minute bars in the cache (`data/cache/`). No IB connection is needed.
- Claude Code's web search. In the video Claude ran about a dozen searches; your results will differ.
- Time: the research request took about 9.5 minutes on our computer, and the research loop about 35 minutes, most of
  it the eight judge runs in the background (2 to 5 minutes each).

## Try it yourself

1. In your `trading-lab` folder, start `claude`, `/clear`, and send the research request in `prompts.md`.
2. Open `research/journal.md` in VS Code with the Markdown preview (Ctrl+Shift+V). Check two of the sources yourself:
   does the link go to the paper Claude named?
3. `/clear`, and send the research-loop request. Read the card when it is done.

You're done when your journal has ranked ideas with sources, and one idea has a strategy card with a verdict. Your
ideas, numbers, wording and Claude's replies will differ from the video; the behaviour is what matters.

## Good to know

- The score is promise (1-5) times cheapness (1-5). A high score means "test this first", not "this will work".
- Rows marked * in the journal rest only on search summaries, not on the papers themselves. Replications of some of the
  papers report much weaker results; treat a paper's numbers as an upper bound. Most papers trade long and short, while
  the Lab's engine is long-only.
- Our engine only shows a strategy the last 200 bars (about 2.5 sessions of 5-minute bars). Claude's first design for
  the filter (a 14-day average range) would have blocked every trade, so it switched to the distance from today's open.
- The threshold (5 ATR) was fixed from the entries' distances alone, before any profit figure was seen, and the judge
  was told how many settings were tried (`--trials 8`). That is what keeps a test honest.
- H1 failed mainly because of costs: both reversion strategies already lose money after costs before any filter. The
  card says what the test shows (this proxy doesn't capture the trend-day effect) and what it doesn't show (that the
  effect is absent).
- The Lab's repo doesn't number modules, so Claude guessed: in the journal and the card it calls the day-type split
  (trend days vs. other days) "module 8". In this course that report comes from Lesson 7.2.
- When Claude tried to wait with a long `sleep`, Claude Code blocked it and suggested a monitor; the project's stop hook
  (Lesson 3.6) made Claude commit and push before it stopped.

## Safety

Paper trading only. Educational content, not financial advice. No idea in the journal is a recommendation, and nothing
here promises a profit: the score is only a test order, and the one idea tested failed. Nothing in this lesson connects
to a broker or places an order.
