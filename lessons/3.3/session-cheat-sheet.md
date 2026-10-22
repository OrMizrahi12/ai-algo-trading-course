# Claude Code session cheat sheet (Lesson 3.3)

## Starting a session

```bash
mkdir trading-lab     # one folder per project
cd trading-lab
claude                # Claude Code works inside the folder you start it in
```

The first time Claude Code opens a folder it asks whether you trust it: it will be able to read, edit and run files
there. Trust only folders whose contents you know.

## Permission modes (Shift+Tab cycles them; the footer shows the current one)

| Mode | What Claude may do without asking | Use it for |
|---|---|---|
| Manual | Read. It asks before edits, shell commands and network access | Learning, sensitive work |
| Accept edits | Edit files in the folder and run common file commands (`mkdir`, `touch`, `mv`, `cp`) | Iterating on code you review |
| Plan | Read and research. Nothing changes until you approve the plan | Anything bigger than a one-liner |
| Auto | Work on its own; a safety check (the classifier) reviews actions before they run | Longer jobs you have planned |

Auto mode is the starting mode in recent versions (it was in ours). It cuts prompts; it does not guarantee safety, so
you still read what Claude did. Official page: https://code.claude.com/docs/en/permission-modes

## Reading a permission prompt

```
Create file  rules.txt
 1 Paper trading only.
Do you want to create rules.txt?
❯ 1. Yes
  2. Yes, and switch to accept edits (...) for this session
  3. No
```

- 1 approves this one action. 2 approves it and stops asking about edits for the rest of the session. 3 refuses, and
  Claude asks what to do instead.
- A change to an existing file shows a **diff**: red lines with `-` go away, green lines with `+` replace them.
  Read it before you answer.

## Undo, shell mode, fresh start

| Type | What it does |
|---|---|
| `/rewind` (or Esc twice on an empty input) | Lists your requests; pick one, then Restore code and conversation, Restore conversation, or Restore code |
| `! <command>` | Shell mode: runs a normal terminal command from inside Claude Code (for example `! cat rules.txt`) |
| `/clear` | Starts a fresh conversation in the same folder; your files stay |

`/rewind` undoes Claude's own file edits only. Files changed by shell commands or by hand are not restored. After a
rewind, your old request comes back into the input box: clear it (or edit it) before you type something new.
Official page: https://code.claude.com/docs/en/checkpointing

## Plan mode in three steps

1. Shift+Tab until the footer says **plan mode on**.
2. Send a prompt that says the goal, the tools, what to make, how to prove it works, how to finish, and where to stop.
3. Read the plan. Approve with "Yes, and use auto mode", approve edits by hand, or tell Claude what to change.

## Words to keep

- **Permission mode**: how much Claude may do without asking you first.
- **Plan mode**: Claude researches and proposes a plan, but changes nothing until you approve.
- **Diff**: the before/after view of a change: red lines removed, green lines added.
- **Commit**: a saved snapshot of the project you can return to.
- **Repository (repo)**: the project folder with its full history; on GitHub it also lives online.
- **uv**: the fast Python tool we use to install Python and the project's libraries.
