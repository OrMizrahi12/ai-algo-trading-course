# Student kit: Lesson 10.2, Order management that survives

Module 10: From backtest to live on paper · AI Algorithmic Trading with Claude Code and Interactive Brokers

In Lesson 10.1 the Lab got its live paper engine. In this lesson its orders learn to survive:

1. **Brackets with a memory.** Every entry is one bracket (the buy, held back until its stop and target are sent with
   it), and every order carries an idempotent reference built from the strategy, the symbol, the session date and the
   signal bar. Before sending, the engine looks for that reference at IB; a restart or a retry can't buy the same signal
   twice. A one-share proof on SPY, run twice on paper: the second run sends nothing.
2. **Risk limits outside the strategy.** A YAML file of limits (size, dollars, trades per day, daily loss) checked in the
   broker before every order, and a kill switch that cancels our orders, sells our positions and keeps the engine from
   starting until we clear it.
3. **Failure drills on paper.** A real reject from IB (error 110), and a connection cut on purpose twice: a short outage
   (reconnect, reconcile, carry on) and a long one (six tries, then a clean halt). Plus an honest table of what was
   shown on paper and what only the fake IB has seen.

## What's in this kit

| File | What it is |
|---|---|
| `prompts.md` | The requests typed in the lesson, the commands typed in the second terminal, our two follow-ups, and the pause-and-try exercise |
| `cheat-sheet.md` | The words, what survives a restart, the limits, the commands and exit codes, the failure table, the numbers in the video |
| `agents-md-entries.md` | The four entries Claude added to the Lab's `AGENTS.md` in this lesson |
| `trading-lab/live/refs.py` | The idempotent order reference: building it, and finding it at IB (open orders, today's executions, this session's orders) |
| `trading-lab/live/execution.py`, `live/broker.py` | `Executor.enter` sends one bracket and resizes the children to what filled; `Broker` is the only way to place an order, checks the risk limits first and records IB's refusals |
| `trading-lab/live/reconcile.py`, `live/state.py`, `live/runner.py` | The intent written before the first order, the restart that adopts whatever IB did, the stop-file check every loop, and the reconnect after a dropped connection |
| `trading-lab/live/risk.py`, `live/risk_limits.yaml` | The pre-trade risk check and its limits (10 shares or $8,000 per position for SPY and QQQ, 4 trades a day, a $500 daily loss limit) |
| `trading-lab/live/kill.py` | The kill switch (`uv run -m live.kill`, `--clear`) |
| `trading-lab/live/proof.py` | The one-share proof on SPY (`uv run -m live.proof`, `--keep`, `--name`) |
| `trading-lab/live/probe.py` | Makes IB refuse an order on purpose (`uv run -m live.probe reject`) |
| `trading-lab/live/__main__.py`, `live/config.py`, `live/console.py` | The command line (limits loaded before connecting, `--port` for paper ports only), the reconnect settings, the console lines |
| `trading-lab/tests/fake_ib.py` | The fake IB, now with held orders, bracket children that wake on the parent's fill, executions, refusals and dropped connections |
| `trading-lab/tests/test_live_*.py` | The tests: restarts between send and fill, the proof, the limits, the kill switch, refusals, partial fills and reconnects |

These are the files as they were at the end of the lesson (Lab commit `0d00738`). They replace the same files from the
Lesson 10.1 kit; everything else in `live/` is unchanged. No new dependency (`pyyaml` was already in the project).

## Before you start

- The Trading Lab with the live engine from Lesson 10.1, the paper guard skill (Lesson 3.5) and the hook that blocks
  live ports (Lesson 3.6).
- IB Gateway logged in to the **paper** account, API on port 4002.
- The regular US session (09:30-16:00 New York time) for every command that places an order. The tests run any time.
- Claude Code in the terminal, signed in with your subscription, in auto mode, and a second terminal in the
  `trading-lab` folder.
- Time on our computer: about 15 minutes for the brackets, 3 for the quieter console, 9 for the limits and the kill
  switch, and about 25 for the failure drills, including the fix after the first drop.

## Try it yourself

1. `/clear`, then send request 1 in `prompts.md`. Read `live/refs.py` and the restart tests before you trust them.
2. Run `uv run -m live.proof` twice during market hours. The second run must send 0 orders.
3. Send request 4, then open one share with `--keep` and run the kill switch yourself (part 5).
4. Drill one failure: `uv run -m live.probe reject`, or ask for the dropped-connection drill (request 6).
5. Before your next paper session: `uv run -m live.kill --clear`.

You're done when your second proof run sends zero orders, the kill switch leaves you flat with STOP in place, and your
runner reconnects after a short drop or halts cleanly after a long one. Your prices, order IDs and Claude's replies will
differ from the video; the process is what matters.

## Good to know

- The proof's first run really buys and sells one share on the paper account. Commissions apply (about $1 each way on
  paper). It refuses to run outside the regular session, near the close, if SPY isn't flat, or on any account that
  isn't a paper (DU) account.
- The first proof run in the video flooded the console with library log lines full of account details. After the fix
  they go to `data/live/proof_entry_SPY/events.log`; the console shows only the proof's own lines.
- An order from an earlier session comes back from IB with order ID 0. Name orders by `permId`, which never changes.
- Sells and cancels are never refused by the limits, so a stop or the kill switch always goes out. That also means a
  limit won't stop an accidental short sale.
- The kill switch sells the whole position in our symbols, including a share you bought by hand in the same symbol.
- The daily loss limit counts from the day's first net-liquidation reading. If the engine starts late in the day, losses
  before that aren't counted.
- With delayed data the newest 5-minute bar is 15-20 minutes late and may still be filling in. The proof uses it only
  to place the stop and target; Lesson 16.1 makes the engine decide only on settled bars.
- The dropped-connection drill cuts a relay (`socat`) in front of the Gateway, never the Gateway itself. A real network
  outage or the Gateway's daily restart may look different; that is not shown in this lesson.
- Partial fills, a restart between send and fill, and a stop that fills in part were tested against the fake IB only.
  The fake IB is Claude's model of IB; a real run is the real check.

## Safety

Paper trading only. Educational content, not financial advice. Every order in this lesson was one share on the paper
account, and every take ended flat with no open orders. Nothing here is a recommendation or a promise of profit.
