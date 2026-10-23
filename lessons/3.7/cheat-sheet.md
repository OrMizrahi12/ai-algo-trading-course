# Claude on autopilot: cheat sheet

## Print mode (`claude -p`)

`claude -p "question"` answers once and exits: no chat, nothing waiting. It loads the same project setup as a normal
session (CLAUDE.md, skills, MCP servers, **hooks**).

| Flag | What it does |
|---|---|
| `--output-format json` | The answer wrapped in data: `result`, `session_id`, `num_turns`, `is_error`, `subtype`, `duration_ms`, `total_cost_usd`... |
| `--json-schema '<schema>'` | Forces the answer into your shape; it arrives in the `structured_output` field |
| `--resume <session id>` | Continues that conversation in a new run (`--continue` picks the most recent one in this folder) |
| `--allowedTools "Write"` | Lets these tools run without asking (print mode starts in **Manual**: anything that needs approval is denied) |
| `--max-turns 3` | A brake: the run stops with `Error: Reached max turns (3)` and a non-zero exit code |

- `total_cost_usd` is an estimate at API prices. On a Pro or Max plan you don't pay it; the run counts against your
  plan's usage.
- Don't use `--bare` on a subscription: it skips your login and needs an API key.
- `jq` helpers: `| jq` (pretty print), `| jq "{result, session_id}"` (pick fields), `| jq -r .session_id` (raw value).

## From Python

```python
import json, subprocess

def ask(prompt, schema):
    out = subprocess.run(["claude", "-p", prompt, "--output-format", "json",
                          "--json-schema", json.dumps(schema)],
                         capture_output=True, text=True, check=True)
    return json.loads(out.stdout)["structured_output"]
```

It runs the same `claude` program you use every day, signed in with your own plan. The full version from the lesson
is `trading-lab/ask_claude.py`.

## Keep Claude working by itself

| | What it is | Lives where | Stops when |
|---|---|---|---|
| `/goal <finish line>` | Claude keeps taking turns; after each one, a separate small model checks the finish line | This session | The finish line is met, it's impossible, your limit ("Stop after 8 turns"), or `/goal clear` |
| `/loop 1m <prompt>` | Re-runs a prompt on a schedule (`/loop <prompt>` without a time lets Claude pick the pace) | This session only | You ask Claude to stop it (Cron Delete), you close Claude Code, or 7 days pass |
| Claude Desktop scheduled task | A saved task that runs on a schedule (hourly, daily, weekdays, weekly, monthly) or with **Run now** | Your computer (**Only on this computer**) | You pause or delete it |

- Goals: write a finish line that Claude's own output can prove (a printed line, a passing test), because the checker
  only reads the conversation. Always add a limit.
- Loops and scheduled tasks spend usage on **every** run, even when nothing changed.
- A local scheduled task runs only while the computer is on and awake (a run can be missed overnight), and starts a few
  minutes late on purpose.
- Pick **Auto** as the task's mode: in Manual, a run with nobody watching stalls on its first question. Turning on
  *Only on this computer* can switch the mode back to Manual, so check it last.
- Time zones: the task uses your computer's clock. 9:35 AM in New York is 13:35 UTC in summer time (EDT) and 14:35 UTC
  in winter (EST).

## The rules of use

From https://code.claude.com/docs/en/legal-and-compliance (*Usage policy*):

- Signing in with your plan is for the people who bought it, for ordinary use of Claude Code.
- Developers building products or services should use API keys. Nobody may route requests through Free, Pro or Max
  plans on behalf of their users, or collect other people's Claude credentials.
- It does not prevent you from signing in to the unmodified Claude Code program with your own subscription: that's what
  `claude -p` from your own script does.
- Usage limits for Pro and Max assume "ordinary, individual" usage.

Our rules in this course: your own machine, your own login. Never share your login or tokens. Don't build something
other people sign in to. Keep loops sensible.

## Paper only

Everything here runs against a **paper** (simulated) account. `connect_test.py --dry-run` prints the host, port and
client ID without connecting; the paper-port check still runs first.
