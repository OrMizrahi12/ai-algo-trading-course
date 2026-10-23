# Student kit: Lesson 4.1, TWS or IB Gateway, and installing the Gateway

Module 4: IB Gateway and the API · AI Algorithmic Trading with Claude Code and Interactive Brokers

In this lesson you saw why our programs talk to IB Gateway instead of Trader Workstation (TWS): to a program the two
are identical, but the Gateway draws no charts and uses fewer resources. Then you watched the Gateway being
downloaded (the Stable version), installed on Linux, logged in to a paper account through the IB API, and configured:
Read-Only API on, socket port 4002, no master client ID, the order precautions left alone, and a daily Auto restart.

## What's in this kit

| File | What it is |
|---|---|
| `tws-or-gateway.md` | TWS and IB Gateway side by side, and the four ports to know |
| `install-ib-gateway.md` | Exact steps to download, install and first-launch IB Gateway on Windows, macOS and Linux |
| `configure-the-api.md` | The settings from the lesson, as a checklist, plus the daily restart and the weekly login |

## Try it yourself

1. Install IB Gateway **Stable** for your system with `install-ib-gateway.md`.
2. Log in with **IB API** and **Paper Trading** selected, using your paper username.
3. Go through `configure-the-api.md`: Read-Only API on, socket port 4002, Auto restart in Lock and Exit.
4. You're done when the status window shows the API server **connected** and both data farms **ON**.

## Remember

- Everything in this course runs on a **paper (simulated) account**. Never choose Live Trading for anything in this
  course, and never point a program at the live ports 4001 or 7496.
- One username can be logged in in one place at a time. Logging in to the Gateway with your paper username
  disconnects a TWS paper session that uses the same username (and the other way round).
- Your paper username and account number are private. Don't post them in screenshots or forums.
- Versions, menus and prices change. What you see on IBKR's pages today wins over this kit.
- This is educational content, not financial advice.
