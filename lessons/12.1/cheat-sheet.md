# Lesson 12.1 cheat sheet: an IB MCP server

## Words

| Word | Meaning |
|---|---|
| MCP (Model Context Protocol) | A standard way to give Claude tools from another program |
| MCP server | The program that offers the tools. Ours is Python, talking to IB |
| Tool description | The text Claude reads to decide when and how to use a tool. It is part of the prompt |
| Read tool / trade tool | A read tool looks at the world; a trade tool changes it (places, changes or cancels orders) |
| Project scope | A server registered in `.mcp.json` in the repo, for this folder only |
| Annotation | A hint a server sends about a tool (read-only, destructive). Hints only: the rules live in code |
| Bracket | A buy with a protective stop and a profit target; when one of them fills, the other is cancelled |
| R | The money lost if the stop is hit: 1R = 1% of the account's net liquidation (total value) |

## Push or pull

- **Push (Module 11):** every 5 minutes the heartbeat packs one snapshot and wakes Claude. Claude sees only that file.
- **Pull (this lesson):** Claude calls tools when it needs something: other bar sizes, an indicator, the open orders,
  the journal.

## The plumbing

Claude Code starts the server (`.venv/bin/python -m desk.mcp_server`, from `.mcp.json`) and talks to it through standard
input and output (stdio). The server talks to the IB paper Gateway (127.0.0.1, port 4002) as client ID 20. Claude never
touches the Gateway; it sees only the tools and what they return.

## The eleven tools

| Tool | Kind | What it does |
|---|---|---|
| `get_quote` | read | Bid, ask, last, previous close, volume (delayed) |
| `get_bars` | read | Closed bars of any IB bar size and duration (delayed) |
| `get_indicators` | read | EMA 9/21, RSI 14, ATR 14, Bollinger bands, VWAP from the lab's indicators module, plus a glossary |
| `get_positions` | read | Positions with their owner (this server or the heartbeat) |
| `get_open_orders` | read | Working orders, their owner, and whether they can be managed here |
| `get_account_summary` | read | Paper account check, net liquidation, cash, buying power, the dollar size of 1R |
| `search_journal` | read | The heartbeat's and the server's journals, filtered by text, action, tool, seatbelt, result, time |
| `place_bracket` | trade | Buys SPY with a stop and a target, sized from `size_r` (at most 1R), through the heartbeat's validator, gates and the lab's risk limits |
| `modify_order` | trade | Moves a stop (only up) or a target of this server's own orders |
| `cancel_order` | trade (destructive) | Cancels this server's order; refuses to remove the stop that protects a live position |
| `close_position` | trade (destructive) | Sells the server's whole SPY position with a marketable limit; cancels its stop and target |

## Safety rules in the server's code

- Paper only: the lab's paper connection refuses anything but a local paper account (`DU...`) and the paper ports.
- SPY only, long only; no tool takes a side, an account or a symbol.
- Own orders only (IB lets only the placing client change an order); refuses while the heartbeat holds SPY or rests
  orders on it. The heartbeat refuses too while any server order rests (its seatbelt `mcp_active`).
- Its own flatten: every 30 seconds it checks the clock and sells its own position 15 minutes before the close.
- Errors come back as a readable `ToolError`, so Claude sees why a trade was refused.
- Separate state and journal (`data/mcp/`), so it never races the heartbeat.

## Permissions we chose

| Mode | What happened |
|---|---|
| Auto mode | Six read-tool calls ran without a prompt |
| Manual mode | Every tool call asked first. Trade tools: `Yes` for each call. Read tools: `Yes, and don't ask again` |

## What we saw on paper

- Read question: SPY drifting sideways slightly above VWAP, nothing open, data delayed (the newest bar 11.5 minutes old);
  by the desk rules, a wait.
- Plumbing test: `size_r` 0.05 sized to 100 shares, cut to 10 by the lab's risk limits; bought 10 SPY at 762.97, stop
  761, target 764. The fill was about a dollar above the delayed bar, so reward-to-risk was 0.52 (CLAUDE.md asks for 2;
  not enforced in code).
- Close: sold 10 at 763.00, about $0.70 lost before commissions; stop and target cancelled; nothing open.
