# Student kit: Lesson 12.1, An IB MCP server in Python

Module 12: Tools, skills and guardrails · AI Algorithmic Trading with Claude Code and Interactive Brokers

Until now the heartbeat decided what Claude sees: one snapshot per bar, pushed to Claude. In this lesson we give Claude
tools it can call itself, through an MCP server we build for our desk:

1. **The server.** `desk/mcp_server/` uses the official `mcp` Python SDK (version 2.3.0 when we built it; `MCPServer`
   replaced `FastMCP` in that version) and talks to the IB paper Gateway with `ib_async` as client ID 20, paper accounts
   only.
2. **Read tools and trade tools.** Seven read tools (`get_quote`, `get_bars`, `get_indicators`, `get_positions`,
   `get_open_orders`, `get_account_summary`, `search_journal`) and, registered separately, four trade tools
   (`place_bracket`, `modify_order`, `cancel_order`, `close_position`). Every trade tool goes through the heartbeat's own
   validator, gates and the lab's risk limits. Every tool that returns a price says the data is delayed.
3. **Project scope.** The server is registered in `.mcp.json` in the desk repo, for this project only. Claude Code asks
   you to approve it the first time, and `/mcp` shows it with its tools.
4. **Permissions.** In manual mode every tool call asks first. We approved the trade tool once per call, and allowed the
   read tools with "Yes, and don't ask again".

## What's in this kit

| File | What it is |
|---|---|
| `prompts.md` | The requests typed in the lesson, the answers we chose, the commands, and the pause-and-try exercise |
| `cheat-sheet.md` | The words, push versus pull, the plumbing, the eleven tools, the safety rules, the permission choices, what we saw on paper |
| `trading-desk/` | The desk exactly as committed at the end of the build (commit dc5f7ee on the `heartbeat` branch): `desk/mcp_server/` (server, read tools, trade tools, IB worker, journal search), `.mcp.json`, the heartbeat with its new `mcp_active` seatbelt, `tests/` (133 tests with a fake IB), `README.md`, `CLAUDE.md`, `pyproject.toml`, `uv.lock` |

## Before you start

- Your `~/trading-desk` from Module 11 (the heartbeat, its seatbelts and journal) and the Trading Lab from Module 10
  (its indicators module, order manager and risk limits). The desk reads the lab read-only from `~/trading-lab`.
- `uv` and Claude Code in the terminal, signed in with your subscription.
- IB Gateway logged in to the **paper** account, API port 4002, and a client ID nothing else uses (the server uses 20,
  the heartbeat 8).
- Time on our computer: about 4 minutes of planning, 15.5 minutes of building, 2 minutes to close the gap from both
  sides.

## Try it yourself

1. In your desk, `/clear`, switch to plan mode (Shift+Tab), and send request 1 in `prompts.md`. Answer the two questions.
2. Before you approve, read the plan for one thing: does every trade tool go through the same validator and risk limits
   as the heartbeat?
3. Restart Claude Code in the desk, choose **Use this MCP server**, and open `/mcp`.

You're done when `/mcp` shows your server connected, and Claude answers one question from your own tools, with no order
placed. Your code, numbers and Claude's answers will differ from the video, and that's fine.

## Good to know

- **Descriptions are part of the prompt.** Claude reads each tool's description before it uses the tool. Say what the
  tool does, what the data is (ours is delayed), and what it refuses.
- **Annotations are hints.** "read-only" and "destructive" in `/mcp` come from the server's tool annotations. They help
  Claude Code and Claude, but the real rules are enforced in the server's code.
- **Trade tools ask.** Keep trade tools on "Yes" for each call. "Yes, and don't ask again" is fine for read tools.
- **IB order ownership.** IB lets only the client that placed an order change or cancel it, so the server manages only
  its own orders, and the heartbeat and the server never trade SPY side by side.
- **Read the honest notes.** Our fill was about a dollar above the delayed bar, so the bracket's reward-to-risk was 0.52,
  below the 2 that CLAUDE.md asks for, and nothing in code enforced it. Rules that matter belong in code.

## Safety

Paper trading only. The server connects to a local paper Gateway only and refuses any account that is not a paper
account. Educational content, not financial advice; nothing here is a recommendation or a promise of profit.
