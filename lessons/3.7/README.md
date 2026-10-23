# Student kit: Lesson 3.7, Claude on autopilot

Module 3: Claude Code from zero · AI Algorithmic Trading with Claude Code and Interactive Brokers

In this lesson Claude worked without a chat. You ran it in print mode (`claude -p`) from a plain terminal, got its
answers as JSON and in a shape you defined with a JSON schema, resumed a session by its ID, and saw how permissions,
`--max-turns` and the Trading Lab's Stop hook behave when nobody is there to click. Then you called Claude from Python
(`ask_claude.py`), gave it a goal with `/goal`, ran a one-minute `/loop` and stopped it, and created a weekday
scheduled task in Claude Desktop that logged whether the market was open. Last, you read the rules for using your own
subscription this way.

## What's in this kit

| File | What it is |
|---|---|
| `prompts.md` | Every command and request typed in the lesson, ready to copy, plus the two pause-and-try exercises |
| `cheat-sheet.md` | Print-mode flags, the Python wrapper, goals vs loops vs scheduled tasks, and the rules of use on one page |
| `trading-lab/ask_claude.py` | The wrapper exactly as Claude wrote it: `ask(prompt, schema)` runs `claude -p` and returns a dict |
| `trading-lab/connect_test.py` | The test script after the goal: a `--dry-run` flag that prints host, port and client ID without connecting |
| `trading-lab/notebooks/market-log.md` | The line the scheduled task wrote in the lesson (yours will have your own time) |

## Before you start

- You need the Trading Lab from Lessons 3.3 to 3.6, `uv`, and the time MCP server from Lesson 3.6 (the market-time
  questions use it).
- `jq` prints and filters JSON in the terminal. Install it if `jq --version` doesn't work (Ubuntu: `sudo apt install
  jq`; macOS: `brew install jq`; Windows: `winget install jqlang.jq`).
- Claude Desktop's scheduled tasks are on the **Code** side of the app, under **Scheduled**.
- Everything in this lesson runs on your own plan. Loops and scheduled tasks spend usage on every run: keep them short
  while you practice, and pause or delete the scheduled task when you're done.

## Try it yourself

**Checkpoint 1: print mode.**

1. In your `trading-lab` folder, run a question with `claude -p "..." --output-format json | jq "{result, session_id}"`.
2. Save the session ID: `SID=$(claude -p "Remember this: ..." --output-format json | jq -r .session_id)`.
3. `claude -p --resume $SID "..."` with a follow-up question.

You're done when the second answer remembers the first.

**Checkpoint 2: Python and a loop.**

1. Start `claude` and ask for `ask_claude.py` (the request is in `prompts.md`). Run it with `uv run ask_claude.py`.
2. `/loop 1m` with a one-line request, watch two runs, then ask Claude to stop the loop.

You're done when Claude reports that the loop is cancelled. Your wording, times and Claude's replies will differ from
the video; the behaviour is what matters.

## Good to know

- Print mode starts in **Manual** mode: a write or command that needs approval is refused unless you allow that tool
  with `--allowedTools`. Hooks still run, which is why the Trading Lab's Stop hook kept Claude going until
  `--max-turns` stopped it.
- `total_cost_usd` in the JSON is an estimate at API prices; on a Pro or Max plan the run counts against your usage
  instead of being billed.
- A `/loop` lives only as long as its Claude Code session, and expires after 7 days. A Claude Desktop task with
  **Only on this computer** runs only while the computer is on and awake.
- Use your own machine and your own login. Never share your login or tokens, and don't build something other people
  sign in to with your plan.
- Nothing in this lesson connects to Interactive Brokers: `connect_test.py --dry-run` exits before connecting. We
  connect to the paper account for the first time in Module 4.
- Menus, versions and limits shown in the video were current at the time of recording (October 2026).
