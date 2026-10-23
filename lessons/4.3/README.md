# Student kit: Lesson 4.3, Market data through the API

Module 4: IB Gateway and the API · AI Algorithmic Trading with Claude Code and Interactive Brokers

In this lesson Claude wrote `market_data.py` for the Trading Lab. It qualified three contracts (Apple's stock, the SPY
ETF and the EUR/USD forex pair), asked IB for live and for delayed snapshot quotes, and showed IB's real answers,
refusals included. Then it pulled 5-minute historical bars, tried 5-second real-time bars, and built bigger bars from
smaller ones with pandas, checked by hand. Last, it wrote `scanner.py` for IB's market scanner and added a small
throttle that keeps our requests under IB's pacing limits.

## What's in this kit

| File | What it is |
|---|---|
| `prompts.md` | The four requests typed in the lesson, ready to copy, plus the pause-and-try exercise |
| `market-data-basics.md` | Contracts, the four market data types, every IB message from the lesson, what a paper account gets, and what live data costs |
| `bars-and-resampling.md` | What a bar is, TRADES vs MIDPOINT, and how small bars become big ones, with the lesson's 13:30 bar worked by hand |
| `pacing-and-scanner.md` | IB's pacing limits as documented, how the throttle works, and the market scanner (with one correction to what Claude said) |
| `trading-lab/market_data.py` | The script at the end of the lesson: contracts, snapshots, historical and real-time bars, `resample_bars`, the throttle |
| `trading-lab/scanner.py` | The scanner script: the top 10 `TOP_PERC_GAIN` stocks on major US exchanges |

## Before you start

- You need the Trading Lab from Module 3 and IB Gateway from Lesson 4.1, logged in to your **paper** account, with
  the API on socket port **4002**.
- `market_data.py` uses `ib_async` and `pandas`. If your project doesn't have pandas yet: `uv add pandas`.
- Each program that connects to the Gateway at the same time needs its own client ID. Here `market_data.py` uses
  **3** and `scanner.py` uses **4**, so neither clashes with the earlier scripts.
- The kit has no data files. The CSV files in `data/` are created when you run the script with your own account.

## Run it

From your `trading-lab` folder, with the Gateway running:

```bash
uv run market_data.py --snapshots   # contracts, live and delayed snapshots, then the bars
uv run market_data.py               # contracts and bars only
uv run market_data.py --resample-aapl   # offline: 5-minute AAPL bars -> 15-minute bars (needs data/AAPL_5min_TRADES.csv)
uv run scanner.py                   # the top 10 TOP_PERC_GAIN stocks
```

## Try it yourself

1. Start Claude Code in your `trading-lab` folder and ask, in your own words, for delayed quotes for one stock and one
   ETF of your choice.
2. Then ask for 5-minute historical bars for one stock, and have them resampled into 15-minute bars, side by side.
3. Pick the first 15-minute bar and check it by hand against the three 5-minute bars it came from.

You're done when the first 15-minute bar checks out by hand: its open, high, low, close and volume. Your prices,
times and Claude's wording will differ from the video; the method is what matters.

## Good to know

- Without a paid subscription, our paper account gets **delayed** US stock and ETF data, about 15 minutes behind.
  That's fine for learning and testing, not for judging a trade at the current price.
- IB's answers depend on your account. If yours has live subscriptions, the live request may work for you. If
  something is refused, read the error code: `market-data-basics.md` lists every one from the lesson.
- The scanner's symbols in the video were that day's examples. They are not tips and not recommendations.
- Paper (simulated) account only. Educational content, not financial advice.
- Menus, versions, prices and limits were current at the time of recording (October 2026).
