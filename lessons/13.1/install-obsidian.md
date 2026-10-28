# Install Obsidian and create the vault

Obsidian is free and needs no account. Always download it from the official site: **https://obsidian.md**, then
**Download**. The page lists every platform. In the lesson the version was 1.14.5 ("Last updated October 22, 2026");
yours may be newer, and that's fine.

## Linux (Ubuntu), as in the video

1. On the download page, under **Linux**, click **Deb** (the Ubuntu package). It gives you a menu entry and an `obsidian`
   command. The file lands in `~/Downloads`, named like `obsidian_1.14.5_amd64.deb`.
2. In a terminal:

   ```bash
   cd ~/Downloads && ls
   sudo apt install ./obsidian_1.14.5_amd64.deb     # use your file's exact name; the ./ matters
   ```

   `sudo` asks for your password. Apt lists what it will install (Obsidian and one small library) and asks
   `Do you want to continue? [Y/n]`: type `y`. A red line at the end that starts with `N: Download is performed
   unsandboxed as root` is harmless.
3. Check it: `which obsidian` prints `/usr/bin/obsidian`.
4. Open it from the applications menu (on our computer: Applications, Office, Obsidian) or by typing `obsidian`.

Other Linux choices on the same page: **AppImage** (one file: make it executable with `chmod +x` and run it), **Snap**,
an AppImage for ARM computers, and **Flatpak** (community maintained).

## Windows

1. On the download page, under **Windows**, click **Universal** to download the installer.
2. Run the downloaded file and follow the installer. Windows may ask you to confirm that you want to run it.
3. Open Obsidian from the Start menu.

## macOS

1. On the download page, under **Mac**, click **Universal** to download the disk image (`.dmg`).
2. Open it and drag **Obsidian** into **Applications**.
3. Open Obsidian from Applications. The first time, macOS may ask you to confirm that you want to open an app downloaded
   from the internet.

## Create the vault (every system)

1. The first screen offers three choices: **Create new vault**, **Open folder as vault**, and **Open vault from Obsidian
   Sync** (sign in). You don't need an account for this course: skip the sign-in.
2. **Create new vault** → **Create**.
3. Vault name: `vault`. Location: **Browse**, and pick your desk folder (`trading-desk` in your home folder).
4. Obsidian shows where it will go (your home folder, then `trading-desk`). Click **Create**.
5. You get one **Welcome** note and, if you open it, the graph view.

Check it from the terminal (macOS and Linux; in Windows use PowerShell with `dir -Force vault`):

```bash
cd ~/trading-desk && ls -a vault && cat vault/Welcome.md
```

You see a hidden `.obsidian` folder (Obsidian's own settings for this vault) and `Welcome.md`, a plain Markdown file.
A link is just a note name in double square brackets, like `[[create a link]]`.
