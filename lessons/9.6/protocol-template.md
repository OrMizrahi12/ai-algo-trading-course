# Pass-the-bar protocol (template)

Fill this in, then commit it before any result. Change nothing in it after you have seen a number; if you must, amend it in
a new commit that says why, and only before any holdout is opened.

## Goal

A candidate passes when, on the sealed holdout alone and after ______ round-trip costs, it makes at least ______ trades with
a profit factor of at least ______.

Signals on: ______ (for example the close). Fills at: ______ (for example the next open).

## Universe and data

- Assets: ______ (fixed now, with the rule that chose them, e.g. a liquidity floor measured on research years only)
- Source: ______ (adjusted for dividends and splits: yes / no)
- Research data: ______ to ______
  - Train: ______ to ______ (build ideas)
  - Validation: ______ to ______ (check them)
- Sealed holdout H1: ______ to ______ (written aside, never read; only file and row counts printed)

## Rules of the search

- At most ______ frozen candidates per holdout opening, each with its rules and settings in one file.
- Every configuration tried goes into the trial ledger.
- A holdout is opened once. A second opening is refused.
- Candidates are chosen on research numbers only. Selection rule (written before seeing the results): ______
- Sizing: ______ Long only / shorts allowed: ______ (and the borrow cost, if shorts)

## What every result shows

- Trades, profit factor, win rate, drawdown, profit factor by year
- The luck number (how often a zero-edge strategy with as many trades would reach the bar)
- Buy-and-hold of the same assets over the same years: return, Sharpe, drawdown

## If nothing passes

- The next fresh, never-touched holdout comes from: ______ (H2)
- After that: ______ (H3, for example future bars, frozen first)

## Known weaknesses (write them down now)

- The chance of a false pass with this bar and this many candidates: ______
- What the researcher may already know about the holdout period: ______
