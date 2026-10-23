# Student kit: Lesson 4.2, The first connection

Module 4: IB Gateway and the API · AI Algorithmic Trading with Claude Code and Interactive Brokers

In this lesson Python talked to your broker for the first time. You asked Claude to point the Trading Lab's
`connect_test.py` at IB Gateway on the paper port 4002, run it, and show the paper account: net liquidation, total
cash, buying power and positions. On the way, the Stop hook from Lesson 3.6 got stuck in a loop, and you fixed it
with `stop_hook_active`. Then you made two programs fight over one client ID, saw error 326, and learned which
messages are real errors and which are only status notes. Last, you looked under the hood: Claude downloaded IBKR's
official TWS API, installed its Python client (`ibapi`) and wrote `ibapi_hello.py`, with its callbacks and its
reader thread.

## What's in this kit

| File | What it is |
|---|---|
| `prompts.md` | Every request and command typed in the lesson, ready to copy, plus the pause-and-try exercise |
| `cheat-sheet.md` | Ports, client IDs, the messages that are errors and the ones that are not, `ib_async` vs `ibapi` |
| `trading-lab/connect_test.py` | The connection test after the lesson: IB Gateway, paper port 4002, read-only, paper accounts only |
| `trading-lab/.claude/hooks/require_commit.py` | The Stop hook with the fix: it lets Claude stop when `stop_hook_active` is true |
| `trading-lab/ibapi_hello.py` | The same account summary with IBKR's official `ibapi` client: callbacks, `nextValidId`, a reader thread |
| `trading-lab/pyproject.toml` | The project file after the lesson: `ib-async`, plus `ibapi` installed from a local folder |

Folders that start with a dot (`.claude`) are hidden in some file browsers: use `ls -a`, or show hidden files.

## Before you start

- IB Gateway installed and logged in to **paper** (Lesson 4.1), with the API on port 4002. You need the Trading Lab
  from Module 3, with `uv`, the `paper-guard` skill and both hooks from Lesson 3.6.
- **One login at a time.** IBKR allows one session per username. If TWS (Module 2) is still logged in with the same
  paper username, the Gateway loses its session ("RE-LOGIN IS REQUIRED", then "EXISTING SESSION DETECTED"). Close
  TWS, then reconnect the Gateway.
- Replace your `.claude/hooks/require_commit.py` with the fixed one from this kit, or ask Claude for the same fix
  (the request is in `prompts.md`). The Lesson 3.6 version can block a turn again and again when you tell Claude not
  to commit yet.
- `ibapi_hello.py` is optional. It needs IBKR's own Python client, which is **not** in this kit: get the TWS API from
  IBKR's download page (link in `cheat-sheet.md`) and copy its `source/pythonclient` folder to
  `vendor/tws-api-python` in your project, then run `uv add --no-workspace ./vendor/tws-api-python`. The copy of
  `ibapi` on PyPI is from 2020: don't `pip install ibapi`.

## Try it yourself

1. In your `trading-lab` folder, start `claude` and ask for the first request in `prompts.md` (point
   `connect_test.py` at port 4002, run it, show the account summary).
2. Check what you see against the Gateway's own window: **API Server** connected, a tab for each client ID that
   connected, and the API messages.
3. Run two copies at the same time with the same client ID (the client-ID request in `prompts.md`). The second one
   should fail with error 326, "client id is already in use", while your code only sees a timeout.

You're done when your table shows your own net liquidation, cash, buying power and positions, and you've seen error
326. Your numbers, wording and Claude's replies will differ from the video; the behaviour is what matters.

## Safety

Paper trading only. Educational content, not financial advice. The scripts refuse any port other than the paper ports
7497 (TWS) and 4002 (IB Gateway), and refuse to go on unless every account starts with `DU`, IBKR's prefix for paper
accounts. Never put a live-account login into this project.
