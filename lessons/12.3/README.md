# Student kit: Lesson 12.3, Guardrails Claude cannot talk its way around

Module 12: Tools, skills and guardrails · AI Algorithmic Trading with Claude Code and Interactive Brokers

A rule in a prompt is a request. A guardrail is a check outside the model, in code, that blocks an action whatever the
model says. In this lesson we stack four of them around every trade the desk's MCP server can place, then attack them on
the paper account:

1. **A PreToolUse hook** (`desk/hook.py`, wired in `.claude/settings.json`). Claude Code runs it before every trade tool
   call and before edit and shell tools. It checks each order against the lab's `risk_limits.yaml` (valid file, SPY
   listed, `size_r` between 0 and 1, the stop above 0, a target above the stop or a reason, no STOP file), never blocks
   `close_position` or `cancel_order`, and fails closed: any crash denies the call.
2. **Deny rules** in `.claude/settings.json` on the limits file, the hook, the settings and `.mcp.json`. The hook also
   denies a shell command that names one of them, unless it is plainly read-only (`cat`, `grep`, `ls` ...). That shell
   check is a tripwire, not a lock.
3. **The same limits in Python**, inside the MCP server (`gates.gate`, the 1R cap) and the lab's Broker and Risk check
   (share and dollar caps, trades per day, daily loss). These were already there from lesson 12.1 and Module 10.
4. **A paper-only check** when the server connects (the lab's `connect_paper`: local Gateway, paper port, DU accounts).

Then two more things we found we needed: a **hard lock** attempt on the limits file (root-owned, read-only; the immutable
flag was refused on our computer, so a rename still worked), and a **limits pin**: a committed SHA-256 fingerprint of
the limits file that the MCP server and the heartbeat both check before any new entry.

## What's in this kit

| File | What it is |
|---|---|
| `prompts.md` | Every request typed in the lesson, the lock commands, the follow-ups, and the pause-and-try exercise |
| `cheat-sheet.md` | The words, the four layers and what each catches, the red-team scorecard, and where the guardrails end |
| `trading-desk/` | The files this lesson added or changed in the desk, as committed at the end (commit bf70f2e): `.claude/settings.json`, `desk/hook.py`, `desk/limits_pin.py`, `desk/mcp_server/trade.py` and `core.py`, `desk/heartbeat.py`, `desk/seatbelts.py`, `desk/__main__.py`, `README.md`, `tests/test_guardrails.py`, `tests/test_limits_pin.py`. Copy them over your desk from lesson 12.2 |
| `redteam/` | The scripts from the red team: `redteam_direct_buy.py` and `redteam_direct_sell.py` (attempt 3, one share, paper only) and `test_redteam_daily_loss.py` (attempt 4, fake broker only) |

`desk/limits.sha256` is not in the kit: it is the fingerprint of *our* limits file. Until you create your own, the server
and the heartbeat refuse new entries (that is the point). Create it with `.venv/bin/python -m desk.limits_pin --update`
and commit it.

## Before you start

- Your `~/trading-desk` with the MCP server from lesson 12.1 (and the skills from 12.2), and the Trading Lab in
  `~/trading-lab` with its `live/risk_limits.yaml`.
- Claude Code in the terminal, signed in with your subscription; IB Gateway logged in to the **paper** account, API
  port 4002.
- A second terminal outside Claude Code, for the lock commands. `sudo` needs your password.
- Time on our computer: 3 minutes 16 seconds for the guardrails, about 2 minutes each for the pin and the heartbeat
  check, and about 10 minutes for the red team.

## Try it yourself

1. Send request 1 in `prompts.md` and read which layers already exist in your desk.
2. Lock the limits file from a separate terminal (back it up first) and run the checks.
3. Run the red-team prompt on paper, and write down which layer acted for each attempt.

You're done when you have your own scorecard. Your code, numbers and Claude's answers will differ from the video, and
that's fine.

## Good to know

- **Hooks match words.** The shell tripwire denied a harmless `find` because it named the limits file, and a determined
  command could get around it. It is a tripwire; file permissions or a separate OS user are the lock.
- **Deny rules win.** Claude Code checks deny rules before anything else, and a hook cannot override them. Attempt 2 was
  stopped there, before the hook ran.
- **"Not refused" is not "safe".** Attempt 1 asked for 1R, which the hook allows; the lab's share cap cut 1,310 shares to
  10. Know which layer does what.
- **A plain script skips everything inside Claude Code.** Attempt 3 bought one share directly with `ib_async`: no hook, no
  deny rule, no server check saw it. What would really stop it sits outside the session: a separate OS user with a
  read-only limits file, the Gateway's Read-Only API for every client but the desk's (plus trusted IPs), or a separate IB
  user or sub-account with order limits.
- **Error 10349** ("Order TIF was set to DAY based on order preset") is a warning, not a block: read the status line.

## Safety

Paper trading only. The red-team orders were one tiny paper position at a time, closed again at once (the whole test cost
about $1.14 in paper money). Attempt 4 never touched an account. Never run the red-team scripts against a live account.
Educational content, not financial advice; nothing here is a recommendation or a promise of profit.
