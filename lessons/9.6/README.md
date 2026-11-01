# Student kit: Lesson 9.6, Don't stop until it passes

Module 9: The strategy factory: goal-driven research loops · AI Algorithmic Trading with Claude Code and Interactive Brokers

The 5-minute runs earlier in this module found nothing. In this lesson the goal becomes something a machine can check:

1. **A bar**: on the sealed holdout alone, after 0.10% round-trip costs, at least 150 trades with a profit factor of at
   least 1.4. Signals on the close, fills at the next open.
2. **A sealed holdout**: free daily bars for 36 US stock ETFs from 2000; research gets 2000 to 2018 (train and validation),
   and every bar from 2019 on is sealed as H1 and never read.
3. **One opening**: at most six frozen candidates, a judge Claude can't edit that opens the holdout once, and every
   configuration counted in a trial ledger.
4. **A Stop gate and `/goal`**: Claude may only stop when the holdout log shows a pass.

Claude set it all up in about 1 hour 47 minutes, we applied the judge ourselves, and then it researched on its own for 30
minutes. Four of five candidates passed the bar. Buy-and-hold of the same ETFs still made more (15.5% a year against
4.7% to 10.8%); the passes had smaller drawdowns. A pass is research, not proof, and not a strategy to trade.

## What's in this kit

| File | What it is |
|---|---|
| `prompts.md` | Everything typed in the lesson, in order: `/model` and `/effort`, the setup request, our answers, the shell-mode commands (apply and test the judge patch, turn the gate on, the refused second opening), the dashboard requests, the `/goal` text, the by-year request, and the pause-and-try exercise |
| `cheat-sheet.md` | The words, the bar and its false-pass odds, the two locks on one door, how to read a pass, and the numbers in the video |
| `protocol-template.md` | A blank pass-the-bar protocol to fill in and commit before any result |

The lab code Claude wrote in the video (the downloader, the holdout judge patch, the gate and the dashboard) is not in this
kit: ask Claude to build yours from the setup request in `prompts.md`, in your own lab. Your numbers will differ.

## Before you start

- You need the trading lab from the earlier lessons of this module (the judge, the guard hook, the commit hook and the
  research gate), Claude Code with auto mode, and `uv`.
- No broker connection is needed: the data is free daily bars from Yahoo through the open-source `yfinance` library,
  for research and educational use under Yahoo's terms.
- Opus 5.5 at effort xhigh uses more of your plan's usage than the lighter setups earlier in the module.

## Disclaimer

Educational content only, not financial advice. Nothing here places an order. A strategy that passes a backtest bar on a
holdout is not a promise of future profit, a recommendation, or a strategy to trade.
