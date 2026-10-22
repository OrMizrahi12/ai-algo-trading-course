# Lesson 3.5 prompts

Every request typed in the lesson, in order, ready to copy. Run them inside your `trading-lab` folder, in Claude Code.
Lines that start with `/` or `!` are typed at Claude Code's prompt; `claude --continue` is typed in the terminal.

## Part 1: your first skill

```
/clear
```

```
Create our first project skill at .claude/skills/paper-guard/SKILL.md. Its job: whenever code connects to Interactive Brokers, check that it uses a paper port (TWS 7497, IB Gateway 4002) and never a live port (7496 or 4001), that any account ID starts with DU (paper), and that nothing places orders on a live account. Write a clear description so you load it by yourself, plus a short checklist and the report format. Don't commit yet.
```

Look at the top of the file (the `!` runs a shell command from inside Claude Code):

```
! head -12 .claude/skills/paper-guard/SKILL.md
```

## Part 2: finding the skill

```
/skills
```

Press `/` to search, type `paper`. If nothing matches, the skills folder is newer than the session. Restart:

```
/exit
```

```bash
clear
claude --continue
```

```
/skills
```

## Part 3: the skill at work

Port 7496 is the live port, on purpose: the skill should refuse it.

```
Write connect_test.py: a tiny ib_async script that connects to TWS at 127.0.0.1 on port 7496 and prints the account summary. Don't run it.
```

Run the skill by name:

```
/paper-guard check the whole repo
```

```
Commit the skill and connect_test.py, and push.
```

## Part 4: subagents in parallel

```
/clear
```

```
Use two subagents in parallel, both on the Haiku model to save usage. Subagent 1: look up the ib_async documentation online and summarize how IB.connect() works (host, port, clientId) and what the paper ports are. Subagent 2: audit our repo and list what is still missing before connect_test.py can run against TWS paper. Then combine both into one short checklist.
```

While they run: the Down arrow selects an agent in the panel at the bottom; Escape goes back.

## Part 5: your own subagent

```
Create a project subagent called lab-reviewer in .claude/agents/. It reviews code in this repo for bugs and paper-trading safety, is read-only (Read, Grep and Glob tools only), runs on Haiku, and uses the paper-guard skill. Then use it once to review connect_test.py.
```

If Claude answers that the agent type isn't found, restart (the agent list is loaded at startup):

```
/exit
```

```bash
clear
claude --continue
```

```
Use the lab-reviewer agent to review connect_test.py.
```

After reading the review:

```
Yes, apply all four fixes, then commit everything including the agent file, and push.
```

## Pause and try

1. **A skill of your own.** Ask Claude for a project skill with one rule you never want broken, and a clear
   description. Restart Claude Code, check that `/skills` lists it, then ask for something that should trigger it and
   look for the `Skill(...)` line.
2. **A reviewer of your own.** Ask Claude for a project subagent with only the Read, Grep and Glob tools, on Haiku,
   using your skill. Restart, and ask it to review one file. It worked if the review comes back and no file changed.
