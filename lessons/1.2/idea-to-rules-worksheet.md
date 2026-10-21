# Worksheet: from a trading idea to exact rules

The "pause and try" checkpoint of Lesson 1.2. Ten to fifteen minutes, pen and paper or a text file.

**The test of a rule:** a computer (or a stranger) can apply it without asking you anything. If a rule still needs
your judgment ("when the trend looks strong"), it isn't a rule yet.

## 1. The idea, in one sentence

Example: *Buy when the price breaks above yesterday's high.*

Your idea: ______________________________________________

## 2. The market and the bars

- Market (for example EURUSD, or one US stock): __________
- Bar size (for example 5 minutes): __________
- Trading hours you allow (for example 07:00–16:00 UTC): __________

## 3. Entry: exactly when do you get in?

Write yes-or-no tests on numbers. All must be true.

| # | Test (on a closed bar) | Example |
|---|---|---|
| 1 | | The bar closes above yesterday's highest high |
| 2 | | It's the first bar today that does so |
| 3 | | Enter at the open of the next bar |

## 4. Stop: where do you get out if you're wrong?

Example: *1 pip below the low of the breakout bar, but at least 5 pips away from the entry.*

Your stop: ______________________________________________

## 5. Target: where do you take the profit?

Example: *Twice the risk (entry + 2 × (entry − stop)).*

Your target: ______________________________________________

## 6. When NOT to trade

Example: *Only one trade at a time; no new trades in the last hour of the session; skip days with a gap larger than 30 pips.*

Your filters: ______________________________________________

## 7. Check yourself

- [ ] Every test is a comparison of numbers (above, below, equal, at least, at most).
- [ ] No word like "strong", "clear", "looks", "about", "near" is left without a number.
- [ ] You know what happens when the stop and the target are hit in the same bar.
- [ ] You know what happens when a new signal appears while a trade is open.

**The two-person test:** give your rules and the same chart to a friend, or to Claude. If you both mark exactly the
same trades, you have rules. If you argue, you still have an opinion. Find the word that caused the argument and
replace it with a number.

## Optional: let Claude check it

Paste your rules into a new chat in Claude and ask:

```text
Here are my trading rules. Point out every place where a computer would not know exactly what to do, and suggest a precise, numeric version of each one. Don't change the idea itself.
```

Keep your finished rules: in Part 1 of the course you'll turn ideas like this into code and test them properly.
