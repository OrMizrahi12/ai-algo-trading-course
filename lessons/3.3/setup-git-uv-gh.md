# Git, uv and the GitHub CLI on Windows, macOS and Linux

In the lesson, Claude installed uv and the GitHub CLI for us on Linux (Git was already there). On your computer you can
let Claude do the same, or install them yourself first with the official commands below. Commands and versions were
current at the time of recording (October 2026); the linked official pages are the reference.

## 1. Git

| System | How |
|---|---|
| Windows | Git for Windows from https://git-scm.com/downloads/win (you installed it with Claude Code in lesson 3.2) |
| macOS | Run `git --version` in Terminal. If Git is missing, macOS offers to install the Command Line Tools: accept. (Or run `xcode-select --install`.) |
| Linux (Debian/Ubuntu) | Usually installed. If not: `sudo apt install git` |

Check: `git --version` prints a version.

## 2. uv (and Python 3.12)

Official page: https://docs.astral.sh/uv/getting-started/installation/

macOS and Linux:

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

Windows (PowerShell):

```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

Alternatives: `brew install uv` (macOS) or `winget install --id=astral-sh.uv -e` (Windows).

Open a new terminal, then check: `uv --version`. Python itself comes through uv: `uv python install 3.12`.

If a new terminal says `uv: command not found`, uv's folder is not on your PATH yet. On macOS and Linux the installer
puts uv in `~/.local/bin`; add this line to `~/.bashrc` (or `~/.zshrc` on a Mac), then open a new terminal:

```bash
export PATH="$HOME/.local/bin:$PATH"
```

Why not `pip install uv`? On many Linux systems the system Python is "externally managed" and pip refuses, as it
did in the lesson. The official installer avoids that.

## 3. The GitHub CLI (`gh`)

Official page: https://cli.github.com (Linux details: https://github.com/cli/cli/blob/trunk/docs/install_linux.md)

| System | How |
|---|---|
| Windows | `winget install --id GitHub.cli` |
| macOS | `brew install gh` |
| Linux (Debian/Ubuntu) | GitHub's apt repository, below |

```bash
(type -p wget >/dev/null || (sudo apt update && sudo apt install wget -y)) \
	&& sudo mkdir -p -m 755 /etc/apt/keyrings \
	&& out=$(mktemp) && wget -nv -O$out https://cli.github.com/packages/githubcli-archive-keyring.gpg \
	&& cat $out | sudo tee /etc/apt/keyrings/githubcli-archive-keyring.gpg > /dev/null \
	&& sudo chmod go+r /etc/apt/keyrings/githubcli-archive-keyring.gpg \
	&& sudo mkdir -p -m 755 /etc/apt/sources.list.d \
	&& echo "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/githubcli-archive-keyring.gpg] https://cli.github.com/packages stable main" | sudo tee /etc/apt/sources.list.d/github-cli.list > /dev/null \
	&& sudo apt update \
	&& sudo apt install gh -y
```

`sudo` asks for your password. Claude cannot type it for you, so if Claude's install step needs it, run that step
yourself (inside Claude Code, start the line with `!`).

Log in (you, not Claude):

```bash
gh auth login -h github.com -p https -w
```

It prints a one-time code and the address https://github.com/login/device . Open it in a browser where you're signed
in to GitHub, type the code (it expires after 15 minutes; never use a code someone else sent you), and authorize
GitHub CLI. GitHub may ask you to confirm it's you (GitHub Mobile, a passkey, an authenticator code or your
password). Check: `gh auth status`.

## 4. Your GitHub no-reply e-mail address

Every commit records a name and an e-mail. Once you push to GitHub, anyone who can see the repository can see them.
To keep your personal address out of the history, use GitHub's no-reply address:

1. On GitHub: your profile picture → **Settings** → **Emails** (in the Access section).
2. Turn on **Keep my email addresses private**. GitHub shows your no-reply address there; it looks like
   `12345678+yourname@users.noreply.github.com`.
3. In your project folder:

```bash
git config user.name "Your Name"
git config user.email "12345678+yourname@users.noreply.github.com"
```

(Add `--global` to use it in every repository on your computer.) Commits made before the change keep the old address:
ask Claude to fix the first commit's author, as in the lesson (`prompts.md`, request 3).

Official page: https://docs.github.com/en/account-and-profile/setting-up-and-managing-your-personal-account-on-github/managing-email-preferences/setting-your-commit-email-address
