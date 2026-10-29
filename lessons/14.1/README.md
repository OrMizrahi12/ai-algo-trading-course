# Student kit: Lesson 14.1, The post-trade review

Module 14: Self-improvement · AI Algorithmic Trading with Claude Code and Interactive Brokers

After every closed trade, our desk now looks back before it may trade again. When a trade closes, the desk wakes Claude
with the trade and the bars since the entry, runs the `post-trade-review` skill from lesson 12.2, writes the review into
the trade note and **one tagged lesson** into `vault/Lessons/`. Until that review exists, a **review gate** in the
Python executor refuses every buy and tells the trader why. Selling and closing are never blocked. We build it, close
the MCP server's door too, and replay one made-up closed trade to watch the refusal, the review and the lesson.

## What's in this kit

| File | What it is |
|---|---|
| `prompts.md` | Every request typed in the lesson, in order, and the pause-and-try exercise |
| `cheat-sheet.md` | The words, how the gate and the review are built, what happens when a trade closes, and the safe ways it fails |
| `trading-desk/` | The files this lesson added or changed in the desk, as committed at the end of the lesson: `desk/execute.py`, `desk/gates.py`, `desk/heartbeat.py`, `desk/journal.py`, `desk/scribe.py`, `desk/snapshot.py`, `desk/trades.py`, `desk/mcp_server/trade.py`, `tests/test_review_gate.py`, `tests/test_scribe.py`, `tests/test_mcp_trade.py`, `tests/mcp_fakes.py`, `vault/README.md`. Copy them over your desk from lesson 13.3 |
| `trading-desk/vault/examples/` | The two notes the real review wrote in our replay: the trade note with its Review section, and the proposed lesson. The trade is made up (fake broker, made-up prices); yours will differ |

## Before you start

- Your `~/trading-desk` with the heartbeat from Module 11, the skills from 12.2 (including `post-trade-review`), the
  guardrails from 12.3, the MCP server from 12.1, and the vault and note writer from Module 13.
- Claude Code in the terminal, signed in with your subscription. The review runs `claude -p`, so the `claude` command
  must work in the terminal where the heartbeat runs.
- Obsidian, with the desk's `vault/` folder open as a vault.
- Time on our computer: about 10 and a half minutes for Claude to build the gate and the review, and under two minutes
  each for the MCP gate and the replay.

## Try it yourself

1. Send requests 1 and 2 in `prompts.md`, or copy the kit's files over your desk and run `uv run pytest -q`.
2. Replay one made-up closed trade (request 3), and open the test notes in Obsidian.
3. Delete the test notes.

You're done when a buy before the review is refused, the same buy after it goes through, and your vault holds one
proposed lesson. Your code, numbers and Claude's answers will differ from the video, and that's fine.

## Good to know

- **Block buys, never sells.** The gate only holds back new entries. Selling and closing always go through, so the desk
  can always get out of a position.
- **No fake reviews.** If Claude can't produce a review, the desk retries every two minutes and stays out of the market.
  Python never writes a review in Claude's place.
- **A lesson is a proposal.** The reviewer writes it with `status: proposed`. It costs nothing in the memory budget and
  the trader never sees it until a person makes it `active`. One trade is an anecdote, not a pattern.
- **We filmed on a Saturday.** The market was closed, so no real trade could close. The replay uses a fake broker and
  made-up prices; only the review call to Claude is real.

Paper account only. Educational content, not financial advice; nothing here is a promise of profit or a recommendation.
