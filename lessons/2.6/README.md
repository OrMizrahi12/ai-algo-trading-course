# Student kit: Lesson 2.6, Orders, costs and leverage, by hand

Module 2: Markets from zero, on a real trading platform · AI Algorithmic Trading with Claude Code and Interactive Brokers

In this lesson you place every important order type by hand in Trader Workstation (TWS), on the paper account: a
market buy, a limit order that waits (and how to change and cancel it), a stop and a stop-limit, a trailing stop with
time in force GTC, and a bracket whose two exits form an OCA group. Then you close the position, read the fills in the
Trades tab, do the math on what one round trip cost, read buying power in the Account window, see what leverage does to
a result, and open and close a short sale.

## What's in this kit

| File | What it is |
|---|---|
| `order-types-cheat-sheet.md` | Each order type of the lesson: what it does, how to build it in TWS, what the confirmation shows, and its catch |
| `cost-worksheet.md` | The lesson's round trip worked out step by step, a blank worksheet for your own trades, and the leverage arithmetic |

## Try it yourself

1. Log in to TWS with your **paper** account (Mosaic layout). Use **one share** for every order.
2. Place a **market** buy, then a **limit** buy below the market; change the limit price once (click the **U**), then
   cancel it.
3. Place a **stop** and a **stop-limit** under your position, look at them on the chart, and cancel both.
4. Place a **trailing stop** with time in force **GTC**. Note the auto-cancel date TWS gives it.
5. Place a **bracket** (Advanced > Bracket) on another stock, check the OCA group on the confirmation, then cancel the
   parent.
6. Cancel everything still working, close your position, and fill in `cost-worksheet.md` from the **Trades** tab.
7. You're done when your account is **flat**, nothing is working in **Orders**, and you can say what each fill cost you.

## Remember

- Everything in this course runs on a **paper (simulated) account**. Paper fills are simulated: real money gives
  different fills and real costs.
- Free market data is **delayed**, about 15 minutes behind the market. Your fills come at the real price of the moment,
  so they will differ from the quote on your screen.
- **Buying power** is what the account lets you buy, not what you should risk. Margin and leverage multiply losses too.
- A **short** loses when the price rises, and with real money it can also pay a fee to borrow the shares.
- Your paper account number is private (TWS shows it at the top right, in the Trades tab and in some window titles).
  Don't post it in screenshots or forums.
- TWS menus and dialogs can change between versions. Prices change every day: your numbers will differ from the lesson's.
- This is educational content, not financial advice. The symbols in the lesson are examples, not recommendations.

Next lesson: 2.7, Reading price on the chart.
