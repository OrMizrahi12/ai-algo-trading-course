# Add the quote columns to a TWS watchlist

Shown in the lesson on TWS 10.50 (Mosaic layout), paper account, free delayed data, on 2026-10-22. Menu names can
change between TWS versions; if one differs, look for the closest match.

## Add the columns

1. Open any watchlist in the Mosaic layout (the lesson used **Favorites** in the Monitor panel).
2. **Right-click a column header** → **Column Layout** → **Manage Columns...**
3. The dialog has two lists: on the left, the columns this watchlist shows; on the right, **Available Columns**, every
   column TWS can add, grouped by topic.
4. Type `bid` in the filter box at the top of Available Columns. Select **Bid Size** and click **Add**. Then select
   **Bid** and click **Add** again.
5. Do the same with the filter `ask`: **Ask**, **Add**, then **Ask Size**, **Add**.
6. Filter `spread`: **Spread**, **Add**. Filter `volume`: **Volume**, **Add**.
7. Use the arrows next to the left list if you want to change the order, then click **OK**.

The lesson's watchlist ended with these columns: Financial Instrument, Bid Size, Bid, Ask, Ask Size, Last, Change,
Change %, Spread, Volume.

## Read each column

| Column | What it tells you |
|---|---|
| **Bid** | The highest price any buyer is offering right now. If you sell right now, you get the bid. |
| **Bid Size** | How many shares are wanted at that bid. |
| **Ask** | The lowest price any seller will take right now. If you buy right now, you pay the ask. |
| **Ask Size** | How many shares are on offer at that ask. |
| **Spread** | Ask minus bid. Buying and then selling straight away costs you about this much per share. |
| **Last** | The price of the last trade: the last place a buyer and a seller agreed. |
| **Volume** | Shares traded so far today. In TWS a large number shows as, for example, 2.54M. |

## The lesson's numbers (delayed data, 2026-10-22)

| Symbol | Bid size | Bid | Ask | Ask size | Spread | Volume |
|---|---|---|---|---|---|---|
| SPY | 80 | 767.18 | 767.20 | 40 | 0.02 | 2.54M |
| IBKR | 100 | 83.73 | 84.00 | 2,900 | 0.27 | 100.0K |
| IBIT | 10,400 | 46.38 | 46.39 | 69,500 | 0.01 | 8.22M |

Your numbers will be different: prices and sizes change every second.

## Delayed data

A dark **olive background** behind a price means delayed data. Hover over it and TWS says "Delayed Data is
Displayed". The free data runs about 15 minutes behind the market. That is fine for learning, and a real handicap at
the open, when prices move fast. This course never pays for data.
