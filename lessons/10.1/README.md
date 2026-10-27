# Student kit: Lesson 10.1, The execution engine

Module 10: From backtest to live on paper · AI Algorithmic Trading with Claude Code and Interactive Brokers

Until now our strategies have only met the backtester. In this lesson Claude builds the Lab's live paper engine, the
`live/` package, around them:

1. **One strategy, two engines.** The same `on_bar` function, fed by the market instead of by history. On free, delayed
   data the engine asks IB for the recent 5-minute bars once a minute and logs how late every bar is.
2. **Planned, then built in six committed steps:** the paper guard, the state file and reconcile, the bar feed, the step
   function with the parity test, execution with marketable limits and a one-cancels-other stop and target, the runner.
3. **A dry run, then a review** by our own `lab-reviewer` subagent before the first trade: 17 findings, the serious ones
   fixed with tests, three left open with reasons.
4. **A supervised run on paper:** a console that shows the paper account, the reconcile result and one line per bar, a
   clean Ctrl+C, a restart, and an honest list of what one run proves and what only the tests have seen.

## What's in this kit

| File | What it is |
|---|---|
| `prompts.md` | The requests typed in the lesson, the live command, and the pause-and-try exercise |
| `cheat-sheet.md` | The words, one strategy and two engines, the engine file by file, the commands, reading the console, late bars, what one run proves |
| `trading-lab/live/` | The engine as it was at the end of the lesson (Lab commit 95dad8b): `config.py`, `broker.py`, `feed.py`, `state.py`, `reconcile.py`, `step.py`, `registry.py`, `execution.py`, `runner.py`, `console.py`, `__main__.py` |
| `trading-lab/tests/fake_ib.py`, `tests/sim_ib.py` | A fake Interactive Brokers for the unit tests, and a simulated one that fills orders by the backtester's own rules (for the parity test) |
| `trading-lab/tests/test_live_*.py` | The engine's tests: the paper guard, the feed, the state, reconcile, the step function, execution, the runner, the console (including a real Ctrl+C sent to a running copy) and the parity test |

Also add this line to the Lab's `.gitignore` (Claude did in the lesson), so the engine's runtime files stay out of Git:

```text
data/live/
```

Claude also added client ID 6 for `live` to the client ID list in `AGENTS.md`, and a `live/` entry to its Layout section
describing the engine (the paper checks, the closed-bar feed, the state and reconcile, the deliberate differences from the
backtest). No new dependency: the engine uses `ib_async`, `pandas` and `exchange_calendars`, already in the Lab.

## Before you start

- The Trading Lab with the backtester (Module 6), the strategies (Module 7), the judge and the holdout (Modules 8 and 9),
  the `paper-guard` skill and the `lab-reviewer` subagent (Module 3), the port hook and the ask rule for `rm`
  (Lesson 3.6), and the data pipeline with cached QQQ bars (Lesson 5.1).
- IB Gateway logged in to the **paper** account, API port 4002 (Module 4).
- Claude Code in the terminal, signed in with your subscription. Plan mode for the plan, then auto mode.
- Time on our computer: about 3 minutes to plan, about 5 minutes for step 1, about 18 minutes for steps 2 to 6 and the
  dry run, about 10 minutes for the review and its fixes, about 5 minutes for the console. The live run itself is as long
  as you watch it.

## Try it yourself

1. `/clear`, switch to plan mode (Shift+Tab), and send request 1 in `prompts.md`. Read the plan's decisions before you
   approve.
2. Let Claude build it (request 2) and run the lab reviewer before you trade (request 3).
3. Start the engine in a second terminal with the live command, stop it with Ctrl+C, start it again, and read the
   reconcile line.

You're done when the parity test passes, a restart prints `reconcile ... -> OK`, and every bar prints its decision.
Your bars, delays, decisions and Claude's replies will differ from the video, and that's fine.

## Good to know

- The bars are late. In the lesson every bar arrived about 10.5 to 11 minutes after its close (35 minutes of one
  afternoon); a test before filming saw about 15. The engine counts a bar as closed once its 5 minutes are over on the
  clock. With delayed data the newest bar IB sends can still be filling in after that; the course measures how late is
  late enough in a later lesson and makes the feed wait for settled bars.
- A first start never trades on old signals, and later restarts skip entry signals older than 30 minutes. Exits are
  never skipped.
- Reconcile halts on anything it can't explain and never trades to fix it. Check IB yourself, fix it, then start with
  `--clear-halt`. `--flatten-on-mismatch` is the one automatic action, and it is off by default.
- One connection per client ID: the engine uses 6, the data pipeline 5. While the engine runs, use a different client
  ID for anything else (Claude did, for the read-only check at the end).
- No decision fired in the video, so the engine has never sent a real order there: the order path, the stop and target
  pair at IB, re-pricing and an unconfirmed cancel have only met the fakes. The proof that the engine decides like the
  backtester is the parity test.
- Check the size. The paper account in the video holds about $1M, not the $100,000 the tests assume: at 1% risk a
  position could be about 1,400 QQQ shares.
- Don't tune a strategy on what the live sessions show: those bars are holdout data.

## Safety

Paper trading only. The engine refuses a non-paper port, a remote host and any account that doesn't start with `DU`,
and checks again before every order. Educational content, not financial advice; nothing here is a recommendation or a
promise of profit.
