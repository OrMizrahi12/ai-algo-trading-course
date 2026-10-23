# Lesson 3.7 prompts

Every command and request typed in the lesson, in order, ready to copy. Run them inside your `trading-lab` folder.
Parts 1 to 3 are typed in a plain terminal (not inside Claude Code). Parts 4 and 5 are typed at Claude Code's prompt.
Part 6 happens in Claude Desktop.

## Part 1: print mode

```bash
claude -p "In one sentence: what is this project for?"
```

`jq` prints JSON neatly and picks fields out of it. If your computer doesn't have it, install it first (on Ubuntu:
`sudo apt install jq`; on macOS: `brew install jq`).

```bash
claude -p "Name the four folders of this lab." --output-format json | jq
```

```bash
clear
claude -p "Name the four folders of this lab." --output-format json | jq "{result, session_id, num_turns, total_cost_usd}"
```

## Part 2: sessions and structured output

Keep the session ID in a shell variable, then resume that conversation:

```bash
SID=$(claude -p "Remember this: our risk per trade is 1 percent." --output-format json | jq -r .session_id); echo $SID
```

```bash
claude -p --resume $SID "What risk per trade did I give you?"
```

Structured output with a JSON schema (this uses the time MCP server added in Lesson 3.6):

```bash
clear
claude -p "Use the time tools: is the US stock market open right now?" --output-format json --json-schema '{"type":"object","properties":{"open":{"type":"boolean"},"new_york_time":{"type":"string"}},"required":["open","new_york_time"]}' | jq "{structured_output, num_turns}"
```

## Part 3: permissions in print mode

Print mode starts in Manual mode, so this write is refused:

```bash
claude -p "Create the file notebooks/today.md with one line: Market check done."
```

Allow exactly one tool, and cap the turns:

```bash
claude -p "Create the file notebooks/today.md with one line: Market check done." --allowedTools "Write" --max-turns 3 && cat notebooks/today.md
```

```bash
cat notebooks/today.md; git status --short
```

Clean up the test file:

```bash
rm notebooks/today.md && git status --short
```

## Part 4: Claude from Python

Start Claude Code (`claude`) in your `trading-lab` folder, then:

```
Write ask_claude.py with a function ask(prompt, schema) that runs claude -p through subprocess with --output-format json and --json-schema, and returns structured_output as a Python dict. In the main block, ask whether the US stock market is open right now (schema: open as a boolean, new_york_time as a string) and print the result. Run it with uv, then commit and push.
```

## Part 5: a goal and a loop

```
/goal connect_test.py has a --dry-run flag that prints the host, port and client ID without connecting, running uv run python connect_test.py --dry-run shows them, and the change is committed and pushed. Stop after 8 turns.
```

```
/loop 1m use the time tools and reply in one line: New York time, and whether the US stock market is open.
```

Watch a couple of runs, then:

```
Stop the loop.
```

## Part 6: a scheduled task in Claude Desktop

In Claude Desktop, on the **Code** side: **Scheduled** → **New task** → **Set up manually**.

- **Name:** `Market open note`
- **Instructions:**

  ```
  Use the time tools to check whether the US stock market is open. Append one line to notebooks/market-log.md with the New York time and the status. Then commit and push.
  ```

- **Trigger:** Schedule · Weekdays · the time on *your* computer's clock that matches 9:35 AM in New York (in the
  lesson our computer runs on UTC, so 1:35 PM).
- **Advanced settings:** turn on **Only on this computer**, set **Local folder** to your `trading-lab` folder.
- **Mode** (the menu under the instructions box): **Auto**. Turning on *Only on this computer* can switch it back to
  Manual, so check it last. Then **Create**, and **Run now** to test it once.

When you're done practicing, **pause** the task (the switch next to *Active* on its page) or delete it (the bin icon),
so it doesn't keep running and spending your usage.

## Part 7: the rules

The page we read: https://code.claude.com/docs/en/legal-and-compliance (section *Usage policy*). In Chrome, Ctrl+F
(Cmd+F on a Mac) and search for:

```
ordinary, individual
```

## Pause and try

1. **Print mode.** In your Trading Lab, ask one question with `--output-format json`, and pull out the `result` and
   the `session_id` with `jq`. Then resume that session with a follow-up question. You're done when the second
   answer remembers the first.
2. **Python and a loop.** Ask Claude for your own `ask_claude.py`, and run it. Then start a one-minute loop, watch two
   runs, and ask Claude to stop it. You're done when the loop reports that it's cancelled.
