# A starting point for your own CLAUDE.md

`/init` writes a first version from your project. Read it, keep it short, and add rules as you discover them. The
file is read at the start of every session and again after every compact, so it is the right place for anything
that must survive.

## What makes a good rule

- **Specific and checkable.** "Explain every trading term in plain English the first time you use it" works better
  than "be clear".
- **With its reason.** "Commits use the GitHub no-reply address, so a personal e-mail never shows up in public
  commits" lets Claude apply the rule sensibly in new situations.
- **Short.** Keep the whole file well under 200 lines. Longer files cost context and are followed less reliably.
- **Nothing secret.** The project file goes into Git: no passwords, API keys or personal e-mail addresses.

## A template

```markdown
# CLAUDE.md

## Hard rule

Paper trading only, educational use only. Never add code that places real orders, connects to a live brokerage
account, or handles real money or credentials. Nothing here is financial advice.

## Communication

Explain every trading term in plain English the first time you use it.

## Commands

- Check the environment: `uv run check_lab.py`
- Add a dependency: `uv add <package>`

## Layout

- `data/`: market data for research (keep large or raw files out of Git)
- `strategies/`: strategy definitions and ideas
- `backtests/`: backtest runs and results
- `notebooks/`: exploratory notebooks

## Git

Default branch `main`. Commits use the name `<Your Name>` and `<your GitHub no-reply address>`, so a personal e-mail
never shows up in public commits. Never change `user.email` to a personal address.
```

## Sharing the rules with other coding tools

Other coding tools read `AGENTS.md`. Put the shared rules there, and make `CLAUDE.md` a single line that imports it:

```markdown
@AGENTS.md
```

When a project has a `CLAUDE.md`, Claude Code reads it (and anything it imports) instead of reading `AGENTS.md` on its
own, so the import is what brings the shared rules in. Check with `/memory`: `AGENTS.md` should appear under
Project instructions, marked `@-imported`.
