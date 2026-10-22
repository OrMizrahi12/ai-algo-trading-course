# Plans and limits

Prices and limits change. Everything below is what the official pages said **at the time of recording (October
2026)**. Always check the current pages before you buy:

- Plans and prices: https://claude.com/pricing
- The Max plan, its tiers and its usage limits: https://support.claude.com/en/articles/11049741-what-is-the-max-plan

## The plans

| Plan | Price (at the time of recording) | Claude Code |
|---|---|---|
| Free | $0 | Not included |
| Pro | $17 per month with an annual subscription ($200 billed up front), or $20 billed monthly | Included |
| Max 5x | $100 per month | Included, 5 times Pro's usage per session |
| Max 20x | $200 per month | Included, 20 times Pro's usage per session |

The Max prices are for web subscriptions; the support article notes that mobile pricing may vary.

## How the limits work

- **Session limit**: your session-based usage limit resets every **five hours**.
- **Weekly limit**: on top of that, there is a weekly limit across all models, which resets at a fixed time each week.
- **One shared pool**: chat on claude.ai, Claude Desktop and Claude Code all count against the same limits.
- **Where to see them**: on claude.ai under Settings > Usage, and inside Claude Code with `/usage` (or `/status`, then
  the right arrow to the Usage tab). Both show your current session, your current week, and when each one resets.
- **When you hit a limit**: Claude Code tells you when it resets, and you wait. Usage credits would let you keep going
  at extra cost; in this course we keep them off.

## Which plan for this course?

- **Pro is enough to start.** In part one, Claude writes our strategies, and then they run on their own, as plain
  code. Claude is only busy while we build.
- **Max is for part two.** There, Claude makes the trading decisions itself, on every 5-minute bar, for hours. That is
  where the higher limits earn their price.
- Start with Pro, and upgrade when you get there.

## The API key trap

Claude Code can also be billed through an API key (an Anthropic Console account, paid per use). This course uses your
subscription instead. If your computer has an environment variable named `ANTHROPIC_API_KEY`, Claude Code can use that
key instead of your plan, so check that it is empty before you sign in (see `install-claude-code.md`).

Educational content only, not financial advice.
