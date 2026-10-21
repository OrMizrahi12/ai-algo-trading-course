# The prompts from Lesson 1.2

Typed exactly as on screen. Attach your own CSV of 5-minute bars (columns: time, open, high, low, close) to a new
chat in Claude before you send the first prompt of each part. The lesson's data file is not included; any free
source of 5-minute bars works. If your file holds a different market, change "EURUSD" to its name.

Your answers will differ from the lesson's: different data, a different day, and every AI answer is written fresh.

## Way two: rules a computer follows (one chat, three prompts)

1. With your CSV attached:

```text
These are real EURUSD 5-minute bars. Turn this idea into exact rules a computer can follow: buy when price pulls back in an uptrend. Use a 20-bar and a 50-bar moving average. Then code the rules in Python, run them on this file, and list every buy signal with its entry, stop and target.
```

2. In the same chat, after the answer:

```text
Run the exact same code on the same file again. Are the signals identical?
```

3. In the same chat:

```text
Be honest: does this result prove that the strategy makes money?
```

What to look for: the rules written as yes-or-no tests, the signal table, the problems Claude raises about its own
run, identical signals on the rerun, and an honest "no" to the last question (a handful of trades proves nothing).

## Way three: the AI is the trader (a new chat)

With your CSV attached:

```text
You are a day trader on a paper account. These are real EURUSD 5-minute bars, and the last bar has just closed. Decide now: buy, sell, or do nothing. If you trade, give your entry, stop and target. Explain your decision in three short points.
```

Then press **Retry** under the answer and compare the two answers: the decision, the reasons and the levels.

What to look for: there are no rules here, the model makes the call; the reasoning is written fresh each time, and
nothing guarantees the same decision twice.

## A note on use

These prompts are for learning how each approach behaves. They are not trading advice, and the answers are not
signals to trade. Read the terms of the AI service you use: some providers' terms do not allow relying on their
services to buy or sell securities.
