# Lesson 4.3 prompts

The requests typed in the lesson, in order, ready to copy. Type them at Claude Code's prompt inside your
`trading-lab` folder, with IB Gateway running and logged in to your paper account. Each part starts with `/clear`,
so Claude begins with a fresh session.

## Part 1: contracts and quotes

```text
/clear
```

```text
New lesson: market data. Write market_data.py with small ib_async helpers (client ID 3, Gateway port 4002). First, qualify three contracts: the stock AAPL and the ETF SPY (SMART routing, USD) and the forex pair EURUSD on IDEALPRO, and print each one's conId and primary exchange. Then ask for a snapshot quote for each, first as live data (market data type 1), then as delayed data (type 3). Show me exactly what IB answers, including any error messages, and explain what our paper account gets.
```

## Part 2: bars, small and big

```text
/clear
```

```text
Now bars. In market_data.py add functions for: (1) historical 5-minute bars for AAPL over the last day using TRADES, and for EURUSD using MIDPOINT; (2) 5-second real-time bars for SPY for about one minute, then resample them into 1-minute bars with pandas to show how bigger bars are built from smaller ones (with a 5-minute rule it works the same). Use delayed data where needed. Save whatever arrives as CSV files in data/, print a few rows of each, and tell me honestly which requests worked and which IB refused, and why. Then commit and push.
```

When Claude offers to resample the real AAPL bars, answer:

```text
Yes, resample the real AAPL 5-minute bars into 15-minute bars and show the first rows of both side by side. Commit and push.
```

## Part 3: pacing and the scanner

```text
/clear
```

```text
Last part of market data: IB's market scanner. Write scanner.py that runs the TOP_PERC_GAIN scan on US major stocks (price above 5 dollars, volume above 1 million) and prints the top 10: rank, symbol, and exchange. Then explain IB's pacing limits for historical data and for simultaneous market data lines, and add a small throttle helper to market_data.py that keeps our requests under those limits. Show real output, then commit and push.
```

## Your turn (pause and try)

Pause the video and, with Claude:

1. Get delayed quotes for one stock and one ETF.
2. Pull 5-minute bars for one stock, and resample them into 15-minute bars.

You're done when you've checked the first 15-minute bar by hand: its open, high, low, close and volume.
