# Student kit: Lesson 2.8, Risk before profit

Module 2: Markets from zero, on a real trading platform · AI Algorithmic Trading with Claude Code and Interactive Brokers

In this lesson you measure risk in R, size a trade from its stop, and work out a strategy's expectancy from its win
rate and its payoff. Then the risk simulator runs one strategy at three risk sizes, on exactly the same wins and
losses, to show what drawdowns, losing streaks and oversized bets do to an account.

## What's in this kit

| File | What it is |
|---|---|
| `risk-simulator.html` | The simulator from the lesson: one HTML file, no install and no internet needed |
| `risk-and-sizing.md` | R, position sizing, expectancy, drawdown and risk of ruin, with the lesson's worked examples and a recovery table |

## Open the simulator

Save `risk-simulator.html` anywhere (the lesson uses the Downloads folder) and double-click it. It opens in your
browser. Nothing is installed and nothing is sent anywhere: all the numbers are computed on your computer.

- **Win rate**: the share of trades that win.
- **Reward : risk**: how many R a win pays. A loss always costs 1 R.
- **Trades per path** and **Paths**: each path is one possible future, a run of trades in a row.
- **Starting balance** and **Risk per trade** for A, B and C: three sizes of the same strategy.
- **Run again** draws new random futures. Moving a slider keeps the same random draws, so you see only the effect of
  the change.

The three panels always get the same wins and losses, in the same order; only the size differs. Under each panel:
the median end balance, the median of each path's largest drawdown, the median of each path's longest losing
streak, the share of paths that ever fell below half the start, and the worst and best path.

## Try it yourself

1. Find a win rate and a payoff with a positive expectancy (the green number on the left).
2. Raise C's risk per trade, step by step, until most of its futures fall below half.
3. You're done when you can explain why the same edge keeps A safe and ruins C.

Your numbers will differ from the video when you click **Run again**; the pattern is what matters.

## Good to know

- The simulator draws wins and losses at random from the win rate you set. Real trades are not coin flips, and past
  results do not predict future ones. Its numbers are illustrations of arithmetic, not predictions or promises.
- The prices in the sizing examples are round illustrations, not quotes or recommendations.
- Paper (simulated) account only in this course. Educational content, not financial advice.
