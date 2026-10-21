# The three ways to trade, on one page

| | 1. Discretionary | 2. Systematic (algorithmic) | 3. AI agent |
|---|---|---|---|
| **Who decides** | A person, by judgment | Fixed rules, written as code | An AI model, every time it is asked |
| **What you saw** | A chart: daily, then 5-minute candles; support and resistance read by eye; a hand on the Buy button | Claude turned "buy pullbacks in an uptrend" into exact rules, Python code and a signal table; the rerun gave identical signals | Claude, prompted as a day trader on a paper account, decided "do nothing"; on Retry it decided "no trade" again, with new reasons and different trigger levels |
| **Same data in, same decision out?** | Not guaranteed | Yes, every time | Not guaranteed |
| **Strengths** | Judgment and experience; flexible; reacts to things no rule foresaw (like breaking news) | Testable on past data (a backtest); repeatable; never tired or scared; runs without any AI once the code is written | Judgment like a person's at machine speed; reads everything you give it; explains every decision; never bored |
| **Limits** | Inconsistent (two traders, or one on a bad day, read the same chart differently); emotional; hard to test honestly; doesn't scale | Rigid: only knows the situations you wrote down; easy to fool yourself by tuning the rules until the past looks perfect (overfitting) | Not deterministic, so it can't be backtested the honest way; costs usage on every bar it reads; needs guardrails it can't talk its way around |
| **Where it lives in this course** | You: you pick the ideas, set the standards, review the results and own every decision | Part 1: the AI creates the strategies (backtest engine, strategies, optimization, the strategy factory, live on paper) | Part 2: the AI is the strategy (Claude decides on every 5-minute bar, with tools, guardrails, memory in Obsidian and a review after every trade) |

## Key terms

- **Discretionary trading**: a person reads the market and decides each trade by judgment.
- **Systematic (algorithmic) trading**: fixed rules, written as code, decide every trade. Same data in, same trades out.
- **Backtest**: running a strategy's rules over past data to see what it would have done.
- **AI agent**: an AI model that receives the data, reasons, and makes the decision itself, every time it's asked.
- **Paper trading**: trading simulated money on a real platform with real prices. Nothing real is at risk.

## Small glossary from the lesson

- **Candle (bar)**: one period of price action (for example 5 minutes) with its open, high, low and close.
- **Moving average**: the average closing price of the last N bars; a smooth line that shows the direction.
- **Pip**: for EURUSD, the fourth decimal of the price (0.0001), the usual unit of a currency move.
- **Spread**: the gap between the buy and the sell price, one of the costs of every trade.
- **Support / resistance**: a price level where the market has repeatedly turned up (a floor) or stalled (a ceiling).
- **Stop / target**: where you get out if you are wrong / where you take the profit.
