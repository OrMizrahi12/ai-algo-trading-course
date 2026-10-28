# Lesson 12.1 prompts and commands

Everything typed in the lesson, in order. Lines that start with `/` are Claude Code commands. Both sessions run in
`~/trading-desk`. Paper account only.

## 1. Build the MCP server (plan mode)

```text
/clear
```

Press Shift+Tab until the footer says **plan mode on**, then send:

```text
Build an MCP server for this desk in Python with the official mcp SDK (check the current version and its docs first), talking to the IB paper Gateway with ib_async on client ID 20, paper accounts only. Read tools: quote, bars (any bar size and duration), indicators using the lab indicators module, positions, open orders, account summary, and a search over our journal. Trade tools, kept separate: place a bracket, modify, cancel and close, each going through the same validator and risk limits as the heartbeat. Write a clear description for every tool, and say honestly that our data is delayed. Tests with a fake IB. Then register it for this project only.
```

Claude asked two questions before the plan. Our answers:

- **Heartbeat** → `1. Refuse, own orders only (Recommended)`: IB lets only the client that placed an order change or
  cancel it, so the trade tools manage only their own orders and refuse while the heartbeat holds SPY.
- **Registration** → `1. Project .mcp.json (Recommended)`: the server is registered in `.mcp.json` in the repo, and
  Claude Code asks for approval on first use. (The other choice, local scope, keeps it private in your own settings.)

Then **Submit**. When the plan is ready, read it, and choose `1. Yes, and use auto mode`.

On our computer: about 4 minutes of planning, 15 minutes 38 seconds of building, 128 tests passing. The smoke test made
one read-only quote call to the paper Gateway that was running; no orders were sent.

## 2. Close the gap from both sides

```text
Close that gap from both sides: the heartbeat must also refuse to trade while the MCP server holds SPY or has an order on it. Add a test for each direction, run everything, then commit.
```

2 minutes 9 seconds on our computer: committed on the `heartbeat` branch, 133 tests passing.

## 3. Use it (the next day, market open)

Start Claude Code in the desk:

```text
claude
```

Choose **Use this MCP server**. Then look at it:

```text
/mcp
```

Select the server, then **View tools**, then a tool to read its description. Press Esc until the dialog closes.

Ask a read-only question (auto mode):

```text
Using only your trading-desk tools, what is SPY doing today on 5- and 15-minute bars, where is it versus VWAP, and do we have anything open?
```

Ctrl+O shows the detailed view with every tool call and its JSON; Ctrl+O again goes back.

Switch to manual mode (Shift+Tab until the footer says **manual mode on**), then the plumbing test:

```text
Now test the trade plumbing on paper: place a tiny SPY bracket with your trade tool (size_r 0.05, a stop and target from the bars you just read). This is a test, not a trade idea. Then show me the order and its stop and target.
```

Our choices at the prompts: **Place Bracket** → `1. Yes` (once). **Get Positions** and **Get Open Orders** →
`2. Yes, and don't ask again`. Then:

```text
Good test. Close the position now and make sure nothing is left open.
```

**Close Position** → `1. Yes` (twice: the first call was refused by the tool for a missing reason, and nothing was sent).

## Pause and try

1. In your own desk, in plan mode, send request 1. Answer the two questions.
2. Read the plan for one thing: does every trade tool go through the same validator and risk limits as the heartbeat?
3. Restart Claude Code, approve the server, and open `/mcp`.

Done when `/mcp` shows your server connected and Claude answers one question from your own tools, with no order placed.
