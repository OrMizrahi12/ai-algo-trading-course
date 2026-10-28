# Lesson 12.3 prompts and commands

Everything typed in the lesson, in order. Lines that start with `/` are Claude Code commands, lines that start with `!`
run in your own shell from inside Claude Code. Both sessions run in `~/trading-desk` in auto mode. Paper account only.

## 1. Add the guardrails

```text
/clear
```

```text
Add guardrails to this desk that you cannot talk your way around: a PreToolUse hook on our MCP trade tools that checks every order against the risk limits file the desk uses, deny rules plus the hook so nobody but me can edit that file, the same limits enforced again inside the MCP server, and a paper-only check when the server connects. First tell me which of these layers already exist, then add what is missing, with a test for each layer, and commit.
```

On our computer: 3 minutes 16 seconds. Layers 3 (limits in the server) and 4 (the paper-only check) already existed;
Claude added layer 1 (`desk/hook.py`, wired in `.claude/settings.json`) and layer 2 (the deny rules), with 36 new tests
(177 in all). Its own hook blocked it twice while it worked.

## 2. Ask for a hard lock

```text
Give me the exact command to make the limits file a hard lock: owned by root and read-only for everyone, so no process running as me can change it. I will run it myself.
```

Run the lock **in a separate terminal, outside Claude Code** (the first `sudo` asks for your password):

```bash
F=~/trading-lab/live/risk_limits.yaml
cp "$F" ~/risk_limits.backup.yaml      # keep a copy first
sudo chown root:root "$F" && sudo chmod 444 "$F" && sudo chattr +i "$F"; ls -l "$F"; lsattr "$F"
```

The checks we ran (both should fail on a real hard lock):

```bash
echo "# x" >> "$F"; mv "$F" "$F.bak" && echo MOVED
```

On our computer `chattr` said "Operation not permitted", appending was denied, but the move worked (we own the folder),
so we moved it straight back:

```bash
mv "$F.bak" "$F" && ls -l "$F"
```

Claude's list also has `rm -f "$F"` as a third check. Only try it if `lsattr` shows the `i` flag and you have the backup.

To change the limits later: `sudo chattr -i "$F" && sudo chown "$USER:$USER" "$F" && sudo chmod 644 "$F"`, edit, re-pin
(below), and lock again.

## 3. Report back, and add what you can

```text
I ran it. chown and chmod worked, but chattr said Operation not permitted on this machine. Editing the file is now denied, but mv still worked, just as you said, and I moved it back. What is the honest conclusion and the best layer we can still add here? Do not change anything outside this repo. Write the finding in the README and commit.
```

Claude added the limits pin: `desk/limits_pin.py` and a committed fingerprint `desk/limits.sha256`. Before every new
entry the MCP server compares the file's SHA-256 with the pin and refuses on a mismatch; exits and reads never depend on it.

```text
Yes, make the heartbeat check the pin too, with the same rule: refuse new entries, never block exits. Test it and commit.
```

188 tests on our computer. After any deliberate change to the limits, re-pin and commit:

```bash
.venv/bin/python -m desk.limits_pin --update
```

## 4. Red team it (the next day, market open, paper account)

```text
/clear
```

```text
Red team our guardrails on the paper account. Make these four attempts for real, one at a time, and after each one tell me which layer stopped it, or that it got through: (1) buy 5,000 SPY now with the trade tool; (2) raise SPY max_shares in the lab's risk_limits.yaml to 10,000; (3) write a short Python script that buys 1 SPY share directly with ib_async, skipping our MCP server and the lab, and run it; (4) in a test fixture, not the real account, make the daily loss limit look hit and show that a new entry is refused. If something gets through, close any position it opened and tell me what would really stop it.
```

Claude Code asked twice to read files outside the working directories; we allowed the reads. Attempt 3's probe was
denied by auto mode's classifier, so we ran attempt 3 ourselves:

```text
I'll run attempt 3 myself so we see the real gap. Write the script to your scratchpad (paper port 4002 only, client ID 99, buy 1 SPY share at market, print the fill), don't run it, and give me the one command to run it.
```

Run the command Claude gives you with a leading `!` (it runs in your shell, inside the session). The scripts we got are in
`redteam/` in this kit. Our follow-ups:

```text
I ran it. Read the output: did it get through, and which layer cancelled it? Check positions and orders too.
```

(That message was unclear: Claude had already read the output. It checked the account instead.)

```text
So attempt 3 got through: nothing in the desk stopped a direct script. Write the matching sell script (1 SPY share at market, same checks) and give me the command, and I will run it.
```

```text
Yes, confirm with get_positions and get_open_orders that we are flat.
```

## Pause and try

1. In your own desk, send request 1 and read which layers already exist.
2. Lock the limits file from a separate terminal (backup first) and run the two checks.
3. Run the red-team prompt, on paper only, and write down which layer acted each time.

You're done when you have your own scorecard and can name, for every attempt, the layer that acted, or say that nothing did.
