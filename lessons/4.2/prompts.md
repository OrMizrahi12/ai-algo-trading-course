# Lesson 4.2 prompts and commands

Everything typed in the lesson, in order. Lines that start with `!` run in the terminal from inside Claude Code
(shell mode). Lines that start with `/` are Claude Code commands.

## 1. Point the Lab at the Gateway

```bash
cd ~/trading-lab && claude
```

```text
IB Gateway is now running on this computer, logged in to the paper account, API on port 4002 with Read-Only on. Update connect_test.py to connect to the Gateway on port 4002 instead of TWS, run it, and show me the account summary: net liquidation, total cash, buying power, and any positions. Don't commit yet.
```

One edit is blocked by the `block_live_ports.py` hook from Lesson 3.6 (its comment named the live ports); Claude
rewords it. Then the Stop hook blocks the end of the turn because the change isn't committed, and you said not to
commit yet. After nine blocks in a row, Claude Code overrides the hook and ends the turn.

## 2. Fix the Stop hook

```text
That loop is a flaw in our Stop hook from the last module: it blocked you even though I told you to wait. Fix require_commit.py the way the message suggests: if stop_hook_active is true, let you stop. Then commit and push both changes.
```

## 3. Read the paper account

```text
/clear
```

```text
Run connect_test.py against the Gateway and show me the account summary in a small table: net liquidation, total cash, buying power, and any positions.
```

Then look at the Gateway's own window (from the taskbar): the API server, the data farms, the client tabs, and the
API messages.

## 4. Client IDs and real errors

```text
Now teach me two things with real runs. First, client IDs: open two connections at the same time with the same client ID and show the error, then with different IDs. Second, run it once on a port where nothing is listening, like 4003, and show what that failure looks like. Explain which messages are real errors and which are just information, like 2104.
```

Claude writes its test script in its own scratch folder, outside the repo, so `connect_test.py` and its guard stay
untouched.

## 5. Under the hood: IBKR's own client (optional)

```text
/clear
```

```text
Under the hood now. Download the official TWS API (Latest) from IBKR's download page at download2.interactivebrokers.com/installers/tws-api/index.html, and install its Python client into this project from that download, not from PyPI (the ibapi package on PyPI is from 2020). Then write ibapi_hello.py with EWrapper and EClient: wait for nextValidId, request the account summary, print it, and disconnect. Use client ID 2 on port 4002. Run it, compare its length with connect_test.py, then commit and push.
```

Claude's cleanup command uses `rm`, and the ask rule from Lesson 3.6 makes Claude Code ask first: read the command,
then answer **Yes** if it only removes tests and caches from the copied client.

```text
! sed -n 1,52p ibapi_hello.py
```

## Pause and try

Connect your own Lab: point `connect_test.py` at 4002, run it, and read your paper account. Then run two copies with
the same client ID and find error 326. You're done when your table shows your own net liquidation, cash, buying power
and positions.
