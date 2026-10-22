# Install VS Code: Windows, macOS, Linux

VS Code (Visual Studio Code) is a free code editor from Microsoft. In this course it is the window we read code in.
Version on 2026-10-21: **1.143**. Your number will be newer. Steps follow the official setup pages at
code.visualstudio.com/docs/setup (checked 2026-10-21).

## 1. Download (all systems)

1. Go to **code.visualstudio.com** (the official site; type it or paste it, and avoid look-alike sites in search ads).
2. Click **Download** at the top right. The download page shows one card per system:
   - **Windows**: the installer (`VSCodeUserSetup-...exe`, the "User" installer: no administrator rights needed).
   - **macOS**: **Mac Universal** (runs on Apple silicon and Intel Macs).
   - **Linux**: **Debian/Ubuntu** (`.deb`) or **Red Hat/Fedora** (`.rpm`).

## 2a. Windows

1. Open your **Downloads** folder and double-click the installer.
2. Accept the license, keep the default folder, and click **Next**.
3. On **Select Additional Tasks**, keep **Add to PATH** ticked. This is what makes `code .` work in PowerShell.
   The other boxes are up to you. If the installer offers a separate command for another AI tool, you don't need it
   for this course.
4. Click **Install**, then **Finish**.
5. Close PowerShell and open it again (a new window picks up the new PATH). Check it: `code --version`

## 2b. macOS

1. Open the download from your **Downloads** folder.
2. Move **Visual Studio Code** into your **Applications** folder, then open it from there. If macOS asks whether you
   want to open an app downloaded from the internet, click **Open**.
3. Make the `code` command work in Terminal: in VS Code press **Cmd+Shift+P**, type `shell command`, and run
   **Shell Command: Install 'code' command in PATH** (on newer versions the entry may also mention an optional
   `copilot` command; you only need `code`).
4. Close Terminal and open it again. Check it: `code --version`

## 2c. Linux (Debian, Ubuntu and similar), as in the lesson

1. In a terminal, go to the download and install it with apt:

   ```bash
   cd ~/Downloads
   ls
   sudo apt install ./code_    # press Tab: it completes the full file name
   ```

   `sudo` runs the command as the administrator. It may ask for your password: nothing appears while you type it.
   That's normal. Type it and press Enter.
2. apt lists what it will install (VS Code plus a few small helper packages) and asks `Do you want to continue? [Y/n]`.
   Type `Y` and press Enter.
3. The installer asks: **Add Microsoft apt repository for Visual Studio Code? [yes/no]**. Answer `yes` to get VS Code
   updates with your normal system updates.
4. Lines like `N: Download is performed unsandboxed as root ...` are notes, not errors. On a minimal system you may
   also see `gpg: command not found`; VS Code is still installed. To be sure the update repository works, install
   `gpg` (`sudo apt install gpg`) and run the `.deb` install again.
5. Check it: `code --version`

**Red Hat / Fedora:** the official page recommends adding Microsoft's repository and running `sudo dnf install code`
(exact commands on code.visualstudio.com/docs/setup/linux). Installing the downloaded `.rpm` with
`sudo dnf install ./code-*.rpm` also works, but then VS Code doesn't update itself.

## 3. First launch (all systems)

1. In your terminal, go into the folder you want to open, and open it: `cd ~/practice` then `code .`
   (`.` means "this folder").
2. A welcome dialog offers to sign in (for GitHub Copilot). Nothing in this course needs it: click
   **Continue without Signing In**.
3. Pick a color theme and click **Get Started**.
4. Make everything bigger or smaller with **Ctrl+=** and **Ctrl+-** (Cmd+= and Cmd+- on a Mac).
5. VS Code shows a **Restricted Mode** banner until you trust the folder. Click **Manage**, read the list, and click
   **Trust** only for folders whose contents you know. Your `practice` folder qualifies: you made every file in it.

## If `code .` says "command not found"

- Windows: re-run the installer with **Add to PATH** ticked, then open a new PowerShell window.
- macOS: run the **Shell Command** step above, then open a new Terminal window.
- Linux: open a new terminal; if it still fails, check that the install finished (`code --version`).
