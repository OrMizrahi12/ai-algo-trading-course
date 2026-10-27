# Lesson 10.1 cheat sheet: The execution engine

## The words

| Word | Meaning |
|---|---|
| **Execution engine** | The program that turns a strategy's decisions into (paper) orders: it fetches bars, calls the strategy, places orders, follows the fills and keeps its state. In the Lab: the `live/` package |
| **Closed bar** | A bar whose time span is over. A strategy only ever decides on closed bars, never on the bar that is still forming. In this lesson's engine a bar counts as closed once its 5 minutes are over on the clock (see "Late bars" below) |
| **State** | What the engine believes: its position, its stop and target, the last bar it stepped. Saved to `data/live/<strategy>_<symbol>/state.json` after every change, written atomically (a crash never leaves half a file) |
| **Reconciliation** | On every start, comparing the saved state with what IB actually holds (positions and open orders) before doing anything else. A match: carry on. Anything it cannot explain: halt and say so. It never "fixes" a mismatch by itself |
| **Parity test** | Replaying cached bars through the live path and requiring exactly the backtester's decisions (bar, position, decision) at every step. If the live path and the backtest disagree, the test fails |
| **Marketable limit** | A limit order priced through the market (a buy limit a little above the last price), so it fills like a market order but can never fill at a crazy price. If it does not fill within the timeout, it is cancelled |
| **OCA pair** | "One cancels all": the stop and the target rest at IB together; when one fills, IB cancels the other. Good-till-cancelled, so they keep protecting the position even if the engine dies |
| **Dry run** | Everything except sending orders: connect, read bars, reconcile, decide, log what it would do |
| **Paper account** | IB's simulated account. Its ID starts with `DU`. The engine refuses any other account, before every order |

## One strategy, two engines

```text
backtest:  cached bars -> on_bar(bars, position) -> simulated fills -> report
live:      IB history, polled once a minute -> closed bars only -> on_bar(bars, position) -> marketable limit
           -> IB paper -> fill -> stop/target pair at IB -> state.json
```

`on_bar` is the same function in both. The strategy never knows whether it is live. Sizing, costs and orders belong
to the engine.

## The engine, file by file (Lab commits 5e08982 to 95dad8b)

| File | What it does |
|---|---|
| `live/config.py` | Paper port and local host only (refuses anything else at import), client ID 6, poll every 60 s, order timeout 30 s, limit offset 0.5%, flatten 10 minutes before the close, signals older than 30 minutes skipped |
| `live/broker.py` | The only place that places or cancels orders. Checks the port, the host and that every account starts with `DU`, before every order. Dry run sends nothing |
| `live/feed.py` | Polls IB for recent 5-minute bars once a minute (the account has no real-time data), keeps the bars whose 5 minutes are over, logs the delay of every new bar to `bar_delay.csv`, and checks for missing bars against the NYSE calendar |
| `live/step.py`, `live/registry.py` | The pure core: the same 200-bar window and filters the backtester uses, and the list of strategies the engine can run |
| `live/execution.py` | Sizing like the backtester (1% risk, no leverage), the marketable limit with its timeout, the OCA stop and target, exits that re-price wider and then halt |
| `live/state.py`, `live/reconcile.py` | `state.json` (atomic writes, a lock so two copies can't run) and the reconcile on every start |
| `live/runner.py`, `live/__main__.py`, `live/console.py` | The loop (poll, step, act), the command line, and the operator's console: the account check and reconcile result at start, then one line per bar with its decision |
| `tests/test_live_*.py`, `tests/fake_ib.py`, `tests/sim_ib.py` | The tests. `test_live_parity.py` replays cached QQQ bars through the whole live path and compares every decision with `run_backtest`, at 0 and 20 minutes of lag |

## Commands

```bash
uv run -m live --strategy opening_range_breakout --symbol QQQ --set range_minutes=15 --dry-run --once   # one poll, no orders
uv run -m live --strategy opening_range_breakout --symbol QQQ --set range_minutes=15                    # live on paper
uv run pytest tests/test_live_parity.py                                                                 # the parity test
```

Stop it with Ctrl+C: the state is saved, and any stop and target stay resting at IB until the next start checks them.

## Reading the console

```text
account   : DU....... paper account (every account starts with DU), 127.0.0.1:4002, client ID 6
run       : opening_range_breakout on QQQ
state     : .../state.json loaded, last bar stepped 2026-10-22 14:05 ET
reconcile : state says flat | IB says 0 QQQ; open orders: none
          -> OK
bar 2026-10-22 14:10 ET  O 704.37  H 704.60  L 704.22  C 704.50  (seen 11m after close) | flat | no signal
```

- No `account` line, or an account that does not start with `DU`: stop. The engine refuses it anyway.
- `reconcile ... -> OK` before anything else. A `PROBLEM` line and `NOT OK` means the engine halted: check IB
  yourself, fix it, then start with `--clear-halt`.
- One line per bar, even "no signal". If the lines stop for longer than a few minutes, something is wrong.

## Late bars (free, delayed data)

- Our paper account has no real-time subscription. A real-time bar stream is refused, and streaming updates of
  history gave nothing; polling recent 5-minute bars once a minute works.
- In the lesson every bar arrived about 10.5 to 11 minutes after its close (a thin sample: 35 minutes of one afternoon).
- The engine counts a bar as closed once its 5 minutes are over on the clock. With delayed data the newest bar IB
  sends can still be filling in for a while after that. How late is late enough is a question the course comes back
  to: a later lesson measures it and makes the feed wait until a bar has settled.
- Because the bars are late, the engine has deliberate differences from the backtest: a wall-clock flatten deadline,
  entry signals older than 30 minutes skipped, and the first start never trades on old signals.

## What one supervised run proves (and what it doesn't)

Proven in the lesson: the paper check, the bar feed and its delays, reconcile on start and restart, the console, a
clean Ctrl+C, and parity with the backtester on cached bars. Not yet: any real order through `live/` (no signal fired),
the stop and target pair at IB, re-pricing, the flatten deadline, an overnight position, half days, a restart with a
real position. Next step: one supervised session with a deliberately small size.

## Safety

Paper account only. The engine refuses non-paper ports, remote hosts and any account that does not start with `DU`.
Educational content, no profit promises, not financial advice.
