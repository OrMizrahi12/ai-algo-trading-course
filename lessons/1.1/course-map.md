# Course map (Lesson 1.1)

16 modules, from zero to an AI trading desk on a paper account. The running project is the **Trading Lab**: you start
it in Lesson 3.3 and grow it lesson by lesson. Part 2 adds a second project beside it, the **trading desk**.

## Foundations (Modules 1–4)

**Module 1: Welcome**
- 1.1 What you will build
- 1.2 Three ways to trade, and where AI fits

**Module 2: Markets from zero, on a real trading platform** (Trader Workstation, on paper)
- 2.1 Your broker: IBKR accounts and installing TWS
- 2.2 What a market is, live in TWS
- 2.3 The map of markets, in TWS
- 2.4 Trading styles on real charts
- 2.5 TWS as your charting platform
- 2.6 Orders, costs and leverage, by hand
- 2.7 Reading price on the chart
- 2.8 Risk before profit

**Module 3: Claude Code from zero**
- 3.1 The terminal in one lesson
- 3.2 Choosing a plan and installing Claude Code
- 3.3 Your first session: building the Trading Lab
- 3.4 Context and memory
- 3.5 Skills and subagents
- 3.6 MCP, hooks and permissions
- 3.7 Claude on autopilot

**Module 4: IB Gateway and the API**
- 4.1 TWS or IB Gateway, and installing the Gateway
- 4.2 The first connection
- 4.3 Market data through the API
- 4.4 Orders through the API

## Part 1: The AI creates the strategies (Modules 5–10)

Claude builds deterministic Python strategies and the tools to test them honestly. The strategies then run on their
own, without the AI, live on paper.

**Module 5: Data and strategy foundations**
- 5.1 The data pipeline
- 5.2 Python for traders, with Claude
- 5.3 A strategy is a spec

**Module 6: The backtest engine**
- 6.1 How backtests lie, and a first engine
- 6.2 An event-driven engine
- 6.3 Metrics and reports
- 6.4 Trust, but verify the engine

**Module 7: Day-trading strategies**
- 7.1 ETF breakouts and trend
- 7.2 Intraday mean reversion
- 7.3 Stocks at the open I: the gap scanner
- 7.4 Stocks at the open II: opening range and VWAP
- 7.5 Risk and position sizing in depth

**Module 8: Optimization and robustness**
- 8.1 Optimization
- 8.2 Out of sample and walk-forward
- 8.3 Stress tests
- 8.4 Multiple testing and the scorecard

**Module 9: The strategy factory: goal-driven research loops**
- 9.1 Claude as a quant researcher
- 9.2 "Don't stop until": `/goal`
- 9.3 Building your own loops
- 9.4 Don't let the AI cheat
- 9.5 The factory at scale (the leaderboard)
- 9.6 Don't stop until it passes (the research dashboard)

**Module 10: From backtest to live on paper**
- 10.1 The execution engine
- 10.2 Order management that survives
- 10.3 Running unattended
- 10.4 Journal and dashboard
- 10.5 Advanced: one codebase for backtest and live

## Part 2: The AI is the strategy (Modules 11–15)

Claude is the trader: on every 5-minute bar it gets the data and decides, including deciding to do nothing, inside
safety rules enforced in code.

**Module 11: Claude as the trader**
- 11.1 From developer to decision-maker
- 11.2 The agent loop
- 11.3 The prompt is the strategy
- 11.4 Sessions and context across bars

**Module 12: Tools, skills and guardrails**
- 12.1 An IB MCP server in Python
- 12.2 Skills for the trader
- 12.3 Guardrails Claude cannot talk its way around
- 12.4 The always-on desk

**Module 13: Memory with Obsidian**
- 13.1 Obsidian as the trader's brain
- 13.2 The journal the agent writes itself
- 13.3 Memory that stays sharp

**Module 14: Self-improvement**
- 14.1 The post-trade review: learning from every trade
- 14.2 Keep or discard
- 14.3 An agent that rewrites its own playbook

**Module 15: Advanced agent designs**
- 15.1 The multi-agent desk
- 15.2 Variants and hybrids
- 15.3 The stock-open agent
- 15.4 Judging an AI trader

## Capstone (Module 16)

- 16.1 One machine, the whole lab
- 16.2 Reading the results
- 16.3 Before real money

## Where the tour's five parts are built

| Part of the lab | Built in |
|---|---|
| The strategy factory and its leaderboard | Module 9 (9.5, 9.6) |
| A strategy running live on paper | Module 10 (10.1–10.3), the capstone (16.1) |
| The AI desk deciding on every 5-minute bar | Modules 11–12, 15 |
| Its Obsidian brain | Modules 13–14 |
| The dashboard | 10.4, the capstone (16.1, 16.2) |
