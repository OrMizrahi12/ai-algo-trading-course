# The order book, explained on a drawn example

## What free data shows

On the free (delayed) data every account gets, TWS does not show the order book:

- **Time and Sales** (right-click a symbol, type `time` in the menu's search box): on real-time data it lists every
  trade as it happens (time, price, size, exchange). On free data it shows one row that says **Delayed**, and no
  individual trades.
- **Market Depth** (search `depth`): the window opens with a bid side and an ask side, both **empty**. At the bottom,
  TWS offers the exchanges' depth feeds as paid subscriptions. In the lesson we clicked **No Thanks**. This course
  never subscribes to paid data, so we draw the book instead.

## A drawn order book (made-up numbers, real mechanics)

| Side | Price | Shares waiting |
|---|---|---|
| Sellers | 767.24 | 1,400 |
| Sellers | 767.23 | 800 |
| Sellers | 767.22 | 500 |
| Sellers | 767.21 | 200 |
| Sellers (**ask**, the lowest) | 767.20 | 300 |
| | *spread: 0.01* | |
| Buyers (**bid**, the highest) | 767.19 | 400 |
| Buyers | 767.18 | 900 |
| Buyers | 767.17 | 600 |
| Buyers | 767.16 | 1,200 |
| Buyers | 767.15 | 700 |

Each row is many orders from many traders, queued up at the same price.

## A market order eats the queue

A **market order** says: buy 500 shares, right now, at any price.

1. It takes all 300 shares at the best ask, 767.20. That level is gone.
2. It still needs 200, so it eats into the next level, 767.21, a cent higher.
3. The ask moves up to 767.22, and the last price moves with it.

That is how a price moves: an aggressive order eats the queue.

## A limit order waits

A **limit order** says: buy 20,000 shares at 767.16, a few cents below the bid, and wait. It does not trade. It sits
in the book like a wall. Sellers who want out quickly now run into a big buyer, so the price may hold above that
level, until someone sells right through it, or the order is cancelled.

## A continuous auction

Nobody sets the price. Buyers wait at their bids, sellers wait at their asks, and while they wait, nothing trades.
The moment a buyer accepts an ask, or a seller accepts a bid, a trade prints and becomes the last price. A price is
simply the last place a buyer and a seller agreed. Overnight, buyers and sellers can change their minds, so the next
morning the auction may reopen at a new level: a **gap**.

## Liquidity

**Liquidity** is how much you can trade, quickly, without moving the price. In a thick market, lots of shares wait
close to the price and the spread is tight. In a thin market, few shares wait, the spread is wide, and even a modest
order pushes the price around.

This is educational content, not financial advice.
