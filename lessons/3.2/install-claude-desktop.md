# Install Claude Desktop

Claude Desktop is the desktop app: chat, plus a **Code** tab that runs Claude Code in a window, on the same
subscription and the same usage limits as the terminal. In this course the terminal stays our main tool; Desktop is
optional, one click away.

## Windows and macOS

Download the installer from the official page, https://claude.com/download, run it like any other app installer, open
**Claude**, and sign in with the same Claude account you use in the terminal.

## Linux (beta): Ubuntu 22.04+ or Debian 12+, x86_64 or arm64

Official page (checked October 2026): https://code.claude.com/docs/en/desktop-linux

The app installs from Anthropic's apt repository, so updates arrive with your system's normal package updates. These
are the commands we ran in the lesson, in order.

**1. curl and gpg** (fresh systems may not have them):

```bash
sudo apt install curl gnupg
```

**2. Anthropic's signing key.** It prints nothing when it succeeds:

```bash
sudo curl -fsSLo /usr/share/keyrings/claude-desktop-archive-keyring.asc https://downloads.claude.ai/claude-desktop/key.asc
```

**3. Check the key.** The fingerprint must be `31DDDE24DDFAB679F42D7BD2BAA929FF1A7ECACE`, owned by "Anthropic Claude
Code Release Signing":

```bash
gpg --show-keys /usr/share/keyrings/claude-desktop-archive-keyring.asc
```

**4. Register the repository** (one line):

```bash
echo "deb [arch=amd64,arm64 signed-by=/usr/share/keyrings/claude-desktop-archive-keyring.asc] https://downloads.claude.ai/claude-desktop/apt/stable stable main" | sudo tee /etc/apt/sources.list.d/claude-desktop.list
```

**5. Install.** `&&` runs the second command only if the first one succeeds:

```bash
sudo apt update && sudo apt install claude-desktop
```

**6. Open it** from your applications menu (we used Applications > Accessories > Claude), or run `claude-desktop`
in a terminal. Click **Get started** and sign in with the same Claude account as in the terminal. If Chrome asks to
open `xdg-open`, allow it: that's the Linux helper that hands the sign-in link back to the app.

### Problem 1 (ours): "NO_PUBKEY" for packages.microsoft.com

If `apt update` stops with `The repository 'https://packages.microsoft.com/repos/code stable InRelease' is not signed`
and `NO_PUBKEY EB3E94ADBE1229CF`, the VS Code repository from Lesson 3.1 has no valid key (on our computer, `gpg`
wasn't installed yet during the VS Code install, so its key file stayed empty). Check, re-download, check again:

```bash
ls -l /usr/share/keyrings/microsoft.gpg          # 0 bytes = the key is missing
curl -fsSL https://packages.microsoft.com/keys/microsoft.asc | sudo gpg --dearmor --yes -o /usr/share/keyrings/microsoft.gpg
ls -l /usr/share/keyrings/microsoft.gpg          # now about 640 bytes
```

Then run step 5 again.

### Problem 2: "Do you want to continue?" with a very large install

By default apt also installs recommended packages. For Claude Desktop that includes QEMU and its friends, which run a
virtual machine for the Cowork feature (we don't use Cowork in this course). On our computer that was 142 packages and
917 MB. If you don't need Cowork, answer `n`, then install without the recommended extras (13 packages for us):

```bash
sudo apt install --no-install-recommends claude-desktop
```

### If your sign-in isn't remembered

Claude Desktop saves your sign-in in your desktop's keyring. If you installed with `--no-install-recommends` (or on a
minimal system), there may be no keyring, and you sign in again at every start. On desktops other than KDE Plasma:

```bash
sudo apt install gnome-keyring
```

Restart the app and sign in once more. The docs page above covers KDE and a locked keyring.

### Update and uninstall

- Update: the Linux app doesn't update itself; `sudo apt update && sudo apt upgrade` brings new versions.
- Uninstall: `sudo apt remove claude-desktop`, then `sudo rm /etc/apt/sources.list.d/claude-desktop.list` (the
  repository line you added in step 4).

## The Code tab

1. Click **Code** at the top left (the two buttons switch between Chat and Code). Ctrl+= makes everything bigger.
2. It may offer to import a Claude Code session from the terminal; you can close that.
3. At the bottom: **This computer**, then **Choose...** to pick a folder (we picked `practice`).
4. The permission mode button (ours said **Auto**) lists the modes: Auto, Manual, Accept edits, Plan, and Bypass
   permissions. The next lessons cover them.
5. Ask a question, for example: `What files are in this folder, and what does notes.txt say?`

The answer arrives in the window, and the panel on the right shows the environment (this computer, the folder) and
how much of the context is used.
