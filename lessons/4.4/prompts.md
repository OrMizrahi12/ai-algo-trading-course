# Lesson 4.4 prompts

The requests typed in the lesson, in order, ready to copy. Type them at Claude Code's prompt inside your
`trading-lab` folder. Before the first one, untick **Read-Only API** in your paper Gateway (Configure > Settings >
API > Settings).

## Part 1: five orders on SPY (IB Gateway, port 4002)

```text
/clear
```

In the lesson the market closed about 15 minutes later, so the request asks Claude to be quick. Drop that sentence if
you have more time.

```text
Read-Only is now off in the Gateway, so our programs can place orders on the PAPER account. The US market closes at 4 PM New York time, in about 15 minutes, so be quick. Write orders.py (client ID 4, port 4002, refuse anything that is not a DU paper account) and run these on SPY, 1 share each, printing every order status and fill event: 1) a what-if market buy (shows margin and commission, places nothing), 2) a real market buy, 3) a limit buy 5 percent below the market, then cancel it, 4) a bracket: limit buy near the market with a take profit 1 percent above and a stop loss 1 percent below, using parentId and transmit, 5) a trailing stop sell for the share we hold. Then print open orders and positions. Commit and push.
```

## Part 2: OCA, one forex order, and flatten_all

After Claude pointed out that the trailing stop and the bracket's exits both cover the same share:

```text
Good catch on the overlapping sells. Fix it: cancel the trailing stop, and show me an OCA group instead (two exits for the same share where one fill cancels the other). Then try a forex order: buy EURUSD with cashQty 20000 USD on IDEALPRO, and show what IB answers. Finally add a flatten_all() that cancels every open order and closes every position at market, run it, and print open orders and positions again (both should be empty). Commit and push.
```

## Part 3: the same script against TWS (port 7497)

Only one session can be logged in per username, so log out of the Gateway, log in to TWS paper, and check File >
Global Configuration > API > Settings: Enable ActiveX and Socket Clients on, Read-Only API off, socket port 7497.

```text
TWS paper is open now on port 7497 with the API enabled. Run orders.py against TWS instead of the Gateway: client ID 5, the same paper checks, and only these steps: a what-if, then a 1-share SPY limit buy 0.50 below the market that we cancel, then a 1-share SPY marketable limit buy and the matching sell to close. Print every status and fill. I will watch them arrive in TWS.
```

When Claude stopped with error 10168 (no SPY quotes through the API), the answer was:

```text
Delayed data is already on in TWS, but it does not reach the API today. Historical bars do work, so take the reference price from the last 5-minute bar of reqHistoricalData instead of a quote, say that in the output, and run the tws stage now.
```

If TWS then asks whether to deactivate the Order Precautions for all API orders, the lesson answered **No**.
`rejects-and-messages.md` explains what happens next.

## Your turn (pause and try)

Pause the video and, with Claude:

1. Switch off Read-Only API in your paper Gateway.
2. Build `orders.py` with the what-if, market, limit, bracket and OCA steps, and a flatten-all function.
3. Run it while the US market is open, then flatten.

You're done when the open orders and positions print empty at the end.
