# Lesson 12.2 cheat sheet: skills for the trader

## Words

| Word | Meaning |
|---|---|
| Skill | A folder with a `SKILL.md` file (a name, a description and instructions) that Claude loads when the description fits |
| Progressive disclosure | Only the description is always visible; the body loads when it is needed |
| Checklist | A short list of conditions that must all hold before we act |
| Constitution | The trader's `CLAUDE.md`: sent as the system prompt with every bar |
| Plugin folder | A folder with `.claude-plugin/plugin.json`; `--plugin-dir` makes its skills available as `<plugin>:<skill>` |
| R | The money lost if the stop is hit: 1R = 1% of net liquidation (total account value) |

## Always loaded versus on demand

| Always, on every bar | On demand |
|---|---|
| `CLAUDE.md`: mission, hard risk rules, output contract, the skill list | A skill's body, when its description fits the bar |
| Every skill's name and description | `market-read` when flat, `entry-checklist` before a buy, `trade-management` while holding, `post-trade-review` after a trade |

## The four skills (`.claude/skills/<name>/SKILL.md`)

| Skill | Use when | What it does |
|---|---|---|
| `market-read` | Every flat bar, before deciding anything new | Data freshness, daily, 15-minute and 5-minute trends, a one-line verdict |
| `entry-checklist` | Only when about to `buy` | The gates, the stop, a target at least 2x the stop distance, the size in R |
| `trade-management` | A long is held | Hold, sell part, or close |
| `post-trade-review` | The first bar after a trade ended | Cooldown and loss counters, one lesson per trade |

## Size in R (from `entry-checklist`)

- Dollars at risk = `size_r` x 0.01 x net liquidation (0.5 typical, 1.0 at most).
- Assumed fill = close x 1.005 (half a percent above the last close).
- Shares = floor(dollars at risk / (fill - stop)), capped so there is no leverage, and by the lab's risk limits.
- Example: net liquidation 100,000, close 500, stop 497, `size_r` 0.5 -> $500 at risk, fill 502.50, risk per share 5.50,
  90 shares, target at least 500 + 2 x 3.00 = 506. The trader sends `size_r`, never shares.

## How the trader gets its skills

```text
claude -p ... --tools Skill --plugin-dir <desk folder> --setting-sources "" --output-format stream-json --verbose
```

- `--tools Skill`: the only tool the trader has (it can load skills and answer, nothing else).
- `--plugin-dir`: the desk folder is a plugin (`.claude-plugin/plugin.json` -> `"skills": "./.claude/skills"`), so the
  skills load as `desk:market-read` and so on.
- `--setting-sources ""`: no project settings, so `CLAUDE.md` is not auto-loaded a second time (it is the system prompt).
- `stream-json`: lists every tool call, so the heartbeat can journal which skills loaded.

## The `skills` journal field

| Value | Meaning |
|---|---|
| `[]` | Nothing was loaded on that bar |
| `["desk:market-read", ...]` | What was loaded, in order |
| `null` | Unknown (a timeout, a failed call, or a bar from before this change) |

## What we saw on paper (dry run, no orders)

| Bar (UTC) | Instructions | Skills loaded | Session | Decision |
|---|---|---|---|---|
| 15:10, 15:15, 15:20 | Trader v2 | none | new (the hash changed) | wait (stale or thin data) |
| 15:25 | Trader v2.1 | `desk:market-read` | new | wait |
| 15:30, 15:35 | Trader v2.1 | none | resumed | wait |

The fix (two sentences in `CLAUDE.md`): market-read comes first on every flat bar, even when a wait is expected; the
safety check in step 1 only rules out a buy, it does not end the bar.
