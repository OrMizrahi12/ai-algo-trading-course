# Install Claude Code

Official pages (checked October 2026): https://code.claude.com/docs/en/setup and
https://code.claude.com/docs/en/quickstart

We use the **native installer**: it is the one the docs recommend, and it keeps Claude Code up to date by itself.
(Homebrew and WinGet also work, but they don't update automatically.)

Requirements: macOS 13 or later, Windows 10 (1809) or later, or Ubuntu 20.04+ / Debian 10+; 4 GB of RAM or more; an
internet connection; and a Pro or Max plan (the Free plan doesn't include Claude Code).

## 1. Install

Open a terminal and run the line for your system. The installer shows no progress bar while it downloads, so give it
a minute.

**macOS, Linux, WSL** (Terminal, or any terminal on Linux):

```bash
curl -fsSL https://claude.ai/install.sh | bash
```

**Windows PowerShell** (your prompt starts with `PS C:\`):

```powershell
irm https://claude.ai/install.ps1 | iex
```

**Windows CMD** (your prompt starts with `C:\`, without `PS`):

```bat
curl -fsSL https://claude.ai/install.cmd -o install.cmd && install.cmd && del install.cmd
```

On Windows, also install **Git for Windows** (https://git-scm.com/downloads/win). It's recommended: Claude Code then
uses Git Bash to run commands. Without it, Claude Code uses PowerShell instead. You don't need to run anything as
Administrator.

Tips:

- In a Linux terminal, paste with **Ctrl+Shift+V** (plain Ctrl+V doesn't paste there). On a Mac, Cmd+V.
- If PowerShell says `The token '&&' is not a valid statement separator`, you're in PowerShell: use the PowerShell
  line. If CMD says `'irm' is not recognized`, you're in CMD: use the CMD line.

## 2. Check the install

Open a **new** terminal window, then:

```bash
claude --version
```

It prints a version number, like `2.1.306 (Claude Code)` on the day we recorded. Yours will be newer.

For a full health check:

```bash
claude doctor
```

Look for `Config install method: native`, `Auto-updates: enabled`, and the last line, **No installation issues
found**. Before you sign in, it also says `Not signed in to claude.ai`: that's expected.

If your shell says `claude: command not found` (or "not recognized"), open a new terminal first. If it still fails,
the install folder isn't on your PATH yet; see https://code.claude.com/docs/en/troubleshoot-install.

## 3. The API key check

If your computer has a variable named `ANTHROPIC_API_KEY`, Claude Code can use that key, and bill it, instead of your
subscription. Check that it's empty:

| System | Command | Good result |
|---|---|---|
| macOS, Linux, WSL | `echo "key: $ANTHROPIC_API_KEY"` | `key:` and nothing after it |
| Windows PowerShell | `echo "key: $env:ANTHROPIC_API_KEY"` | `key:` and nothing after it |
| Windows CMD | `echo key: %ANTHROPIC_API_KEY%` | `key: %ANTHROPIC_API_KEY%` (CMD prints the name when the variable doesn't exist) |

If a key is printed and you want to use your plan instead:

- macOS / Linux: run `unset ANTHROPIC_API_KEY`, and remove the `export ANTHROPIC_API_KEY=...` line from your shell
  profile (`~/.bashrc` or `~/.zshrc`) so it doesn't come back.
- Windows PowerShell: `[Environment]::SetEnvironmentVariable("ANTHROPIC_API_KEY", $null, "User")`, then open a new
  terminal.

## 4. Start Claude Code and sign in

```bash
cd ~/practice      # any folder you made yourself; we use the practice folder from Lesson 3.1
claude
```

1. **Text style**: pick the one that reads best in your terminal (we kept Dark mode) and press Enter.
2. **Login method**: choose **1. Claude account with subscription** (Pro, Max, Team, or Enterprise) and press Enter.
   Option 2 (Anthropic Console account) is API billing, not for this course.
3. Your browser opens a claude.ai page: **Claude Code would like to connect to your Claude chat account**. Read the
   list (one line says it will contribute to your Claude subscription usage) and click **Authorize**. If the browser
   asks you to verify that you're human, complete that check.
4. The browser says you're all set up. Back in the terminal: **Login successful. Press Enter to continue**.
5. **Security notes**: Claude can make mistakes, so review what it does; and because of prompt injection risks, only
   use it with code you trust. Press Enter.
6. **Do you trust this folder?** Claude Code will be able to read, edit, and run files there. For a folder you made
   yourself, choose **Yes, I trust this folder** and press Enter.

The session header shows the Claude Code version, the model, your plan and the folder.

## 5. Check your plan and your usage

Inside Claude Code:

| Type | What it shows |
|---|---|
| `/status` | Version, folder, and **Login method**: it should say Claude Pro account or Claude Max account (not an API key) |
| Right arrow (in `/status`) | Moves across the tabs: Status, Config, Usage, Stats |
| `/usage` | The Usage tab directly: current session, current week, and when each one resets |
| Esc | Closes the panel |
| `/exit` | Leaves Claude Code. It prints a `claude --resume ...` command you can use to continue that session later |

## Keep it updated

The native install updates itself in the background. To update right now: `claude update`.

## Uninstall (if you ever need to)

- macOS / Linux / WSL: `rm -f ~/.local/bin/claude` and `rm -rf ~/.local/share/claude`
- Windows PowerShell: `Remove-Item -Path "$env:USERPROFILE\.local\bin\claude.exe" -Force` and
  `Remove-Item -Path "$env:USERPROFILE\.local\share\claude" -Recurse -Force`
