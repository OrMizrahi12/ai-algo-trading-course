# Cheat sheet: paper vs live

Lesson 16.3 · AI Algorithmic Trading with Claude Code and Interactive Brokers · Educational content only, not advice.

## Key terms

- **Live account**: an account with real money: real fills, real losses. Everything in this course ran on paper.
- **Slippage, fees and taxes**: costs that paper does not fully show. Slippage is the gap between the price you saw and
  the price you got.
- **Terms of service / usage policy**: the rules a provider sets for using its products.

## What changes from paper to live

| | On paper (this course) | Live |
|---|---|---|
| Fills | The simulator decides the fill | Your order meets a real market: it can fill in pieces, late, or not at all, at a worse price than you saw (slippage) |
| Data | Free, delayed data (in lesson 16.2, one signal reached us more than 16 minutes late) | Real-time data usually comes with a market-data subscription, and its own cost |
| Costs | Commissions were charged (at 10 shares, one commission was about 0.05 R) | Commissions, and there can also be exchange and regulatory fees, and taxes on any gains, which depend on where you live |
| You | A loss is a number | A loss is your money, and it changes how people decide. Rules decided in advance (kill switch, risk limits, review gate) are there for that |

## What the official pages say (as shown in the lesson, October 2026)

- **Interactive Brokers, knowledge base article 252** (last updated November 11, 2024): a paper trading account is a
  simulated account trading in a simulated market; it is not a real market and prices cannot exactly match; IBKR also
  simulates the exchange's role; the fills "in no way" indicate what would happen in the real market; no simulator could
  be perfect.
- **FINRA Regulatory Notice 26-10** (published April 20, 2026; effective June 4, 2026; phase-in period ends October 20,
  2027): new intraday margin standards replace the day trading margin requirements in their entirety, including the day
  trade count for designating a "pattern day trader" and the $25,000 minimum equity requirement; they are amendments to
  FINRA Rule 4210; members that need more time may phase them in over 18 months.
- **Anthropic Usage Policy** (the version effective November 12, 2026): for high-risk use cases, a qualified person must
  remain accountable and the impacted individual must know AI was involved; the requirements are a qualified human in the
  loop and disclosure; finance is a high-risk area: "a personalized recommendation to buy, sell, hold, or allocate among
  specific investment products", and advice on someone's own taxes.
- **Anthropic Consumer Terms of Service** (effective October 8, 2025): they govern Claude.ai, Claude Pro and other services
  for individuals; the Commercial Terms govern any Anthropic API key. Section 3, item 9: you may not rely upon the Services
  to buy or sell securities or to provide or receive advice about securities and other financial products, as Anthropic is
  not a broker-dealer or a registered investment adviser. Item 7: except via an Anthropic API key or where explicitly
  permitted, you may not access the Services through automated or non-human means, whether through a bot, script, or
  otherwise.

Read each page yourself before you rely on any of it: these are short notes, and pages change.
