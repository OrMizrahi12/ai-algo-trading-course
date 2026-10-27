# Lesson 10.5 prompts and commands

Everything typed in the lesson, in order. Lines that start with `/` are Claude Code commands. Both sessions ran in auto mode,
from the Trading Lab folder. The live part needs IB Gateway logged in to the **paper** account (port 4002); the backtest part
needs no IB connection at all.

## 1. Port the strategy and compare the engines

```text
/clear
```

```text
Install NautilusTrader with its Interactive Brokers extra in a separate uv environment (a new folder next to the lab, do not touch our lab's dependencies), read its current docs, and port our ORB strategy: 15-minute range, QQQ, long only, stop at the range low, 1R target, flat before the close. Backtest it on a copy of our cached QQQ 5-minute bars from 2024-10-21 on (do not read the holdout, and the backfill in my other terminal is still writing older bars) and put the numbers next to our own engine's for exactly the same period and costs. Explain every difference. Show the versions you installed.
```

Leave out the part about the backfill if nothing else is writing your cache. Use your own start date: the point is a period
you have already tested, never the holdout.

On our computer this took 7 minutes 15 seconds. Along the way Claude:

- made `~/nautilus_lab` with its own environment (NautilusTrader 1.231.0 and its IB library, nautilus-ibapi 10.45.1);
- copied the bars (29,070 bars: 370 full sessions and 5 half days, no gaps) and ran our own engine on the same copy;
- found that Nautilus has no "fill at the next bar's open" mode and built a workaround (see `cheat-sheet.md`);
- found that a one-share fake trade capped the exit at one share, and fixed it;
- hit `AccountBalanceNegative` (the backtest stopped early) and allowed cash borrowing, the way our engine behaves;
- paired every trade with ours before trusting the totals.

Nothing was committed: `~/nautilus_lab` lives outside the Lab's repo.

## 2. The same strategy on the paper Gateway, no orders

```text
/clear
```

```text
Take the ORB strategy in ~/nautilus_lab to the IB paper Gateway with the NautilusTrader Interactive Brokers adapter: port 4002, client ID 30, paper account only, and no orders at all (the strategy may log what it would do, but must never submit). Show it connecting, loading the QQQ instrument, pulling recent 5-minute bars and subscribing to new ones. The market is closed now and our data is delayed, so explain what we see. Stop it after a few minutes. Then give me your verdict: when is our own engine enough, and when should someone graduate to a platform like this?
```

Use a client ID nothing else of yours uses. When Claude asks to **read outside the working directories**, we answered
"No, and ask again next time", and then added the one folder on purpose:

```text
/add-dir /home/<you>/nautilus_lab
```

(choose "Yes, for this session"), then:

```text
Done, nautilus_lab is added for this session. Carry on with option 1.
```

About 10 minutes in the video. Claude wrote `live_observe.py`, ran it twice, and reported error 2188 on the bar requests.

## 3. Pin down the difference (no subscription, no patch)

```text
No subscription, we stay on free data. But pin down the exact difference: compare the history request the adapter sends with the one our live feed sends, from the installed source code, and tell me in a few lines. Do not patch the library.
```

```text
Yes, test it once without the subscription.
```

About a minute for the comparison and two minutes for the test. `live_observe.py` in this kit is the version Claude left
at the end: the history request only, `subscribe_bars` removed.

## Pause and try

1. Install NautilusTrader in its own folder, never in the Lab's environment.
2. Port one strategy with request 1 (yours, or the ORB), and compare it with our engine trade by trade, not just the totals.
3. If you try the live adapter, keep it on paper, with no order route at all (request 2).

You're done when the trade counts match, and you can explain every difference that's left.
