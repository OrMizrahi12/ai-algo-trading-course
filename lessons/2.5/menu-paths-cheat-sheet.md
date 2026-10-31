# TWS menu paths cheat sheet

Lesson 2.5 · TWS, Mosaic layout, **paper** account, free delayed data. Every path below is what TWS showed in the
lesson. Menus can move between TWS versions: if one looks different, look for the same words nearby.

## The Mosaic screen

| Panel | Where | What it's for |
|---|---|---|
| Order Entry | top left | Build an order (lesson 2.6) |
| Quote panel | below Order Entry | Last price, today's change, bid/ask and their sizes |
| Chart | next to the quote panel | Candles, indicators, drawings |
| Monitor | right | Your watchlists, one per tab |
| Activity | bottom left | Your orders and trades |
| News | bottom right | Headlines from the newswires |
| Layout tabs | very bottom | Mosaic, Classic TWS, Learn, News & Research, and your own layouts |

- **Open any panel:** `New Window` (top left) > **General Tools** > Order Entry, Portfolio, Watchlist, Quote Details,
  Chart ▸ … (a closed panel always comes back from here). `Escape` closes the menu.

## Watchlist

- **New watchlist:** in the Monitor, click the **+** after the last tab > **Watchlist** > *Browse Lists* > **New Watchlist**.
- **Rename it:** right-click the new tab (Watchlist1) > **Rename Watchlist** > type a name (lesson: `Day trading`) > `Enter`.
- **Add a symbol:** click an empty row, type the symbol (`SPY`), press **Shift+Enter** (= stock; it skips the
  instrument chooser). Lesson list: `SPY`, `QQQ`, `AAPL`, `MSFT`, `NVDA`.
- **Add a column:** right-click a column header > **Insert Column** > **Prices** > **Bid** (then again for **Ask**).
  The new column lands to the left of the header you right-clicked. Volume is under **Insert Column** >
  **High/Low/Volume/History**.
- **Delayed data:** olive cells; hover one and TWS says "Delayed Data is Displayed."

## Chart

- **Point the chart at a symbol:** click the symbol in a linked watchlist.
- **Bar size and period:** click the chart title (for example "1 Year/Weekly candles ▾"):
  - **Candle Size** (top part) > **5 min**;
  - **Time Period** (lower part) > **More** > **2 Days** > **5 min candles**. The title then reads "2 Days/5 min candles".
- **Indicators (studies):** chart menu **Edit** > **Studies…** (the Chart Settings window, Studies tab):
  - type `exponential` in the search box > **Exponential Moving Avg.** > **Add** > in *Edit Exponential Moving Avg.*
    set **Period** to `20`;
  - type `vwap` > **Intraday Volume Weighted Average Price** > **Add**;
  - **OK**.
- **Volume and candles:** same window, **Chart Parameters** tab: **Bar type** = Candlestick (the default); under
  **Additional Data and Features** tick **Volume**; **OK**.
- **Horizontal line:** **Edit** > *Annotations* > **Horizontal Line**, then one click on the chart.
- **Trend line:** **Edit** > *Annotations* > **Trend Line**, then **press** on the first point, **drag** to the second,
  **release**. Two separate clicks do not draw it.
- **Delete a drawing:** right-click the line > **Remove This Trendline** (the same item for a horizontal line).
- **Linking:** the chain icon in each panel's title bar shows its color group ("Group windows"). Panels in the same
  group follow each other: click AAPL in the watchlist and the chart switches to AAPL, studies kept.

## Save the workspace

- **Copy the layout:** right-click the **Mosaic** tab at the bottom > **Copy Tab** > *Enter a new Desktop Tab name*:
  `Day trading 5-min` > `Enter`. A new tab appears at the bottom.
- **Save to disk:** **File** > **Layout Settings** > **Save Settings** (no message appears).
- **Find it again:** **File** > **Open Layout Library…** > **My Layouts**: "Day trading 5-min · User Created".
  (The **Layout Library** tab holds ready-made layouts from Interactive Brokers.)

## Checklist: your own workspace

- [ ] A watchlist with SPY and a few US stocks, with Bid and Ask columns
- [ ] A chart on 2 Days / 5 min candles
- [ ] EMA (period 20), Intraday VWAP and Volume on the chart
- [ ] One horizontal line and one trend line (then try deleting one)
- [ ] Clicking a stock in the watchlist switches the chart
- [ ] The layout copied to its own tab, settings saved, and listed under My Layouts
