# Install IB Gateway: Windows, macOS, Linux

Versions on 2026-10-21: **Stable 10.50.1f** (the one we use), Latest 10.51.1d. Your numbers will be newer: pick the
tab named **Stable**. Neither version updates itself; to upgrade, you download and install again.

## 1. Download (all systems)

1. Open IBKR's IB Gateway download page: **interactivebrokers.com/en/trading/ibgateway-stable.php**
   (on interactivebrokers.com it is also under **Platforms**; the page is titled "Download IB Gateway").
2. Click the **Stable** tab.
3. Pick the card for your system and click **Download**:
   - **Windows** (64-bit; also for Windows 11 Arm devices): an `.exe` installer.
   - **Apple Silicon** (M-series Macs) or **Apple Intel Processor**: a `.dmg` installer. Not sure which Mac you
     have? Apple menu → **About This Mac**: "Chip Apple M…" means Apple Silicon; "Processor … Intel" means Intel.
   - **Linux (x86_64)** for most PCs, or **Linux (ARM64)**: a `.sh` installer script (about 326 MB on 2026-10-21).

The installers bring their own Java runtime: you don't need to install Java yourself.

## 2a. Windows

1. Open your **Downloads** folder and double-click the IB Gateway installer.
2. If Windows asks "Do you want to allow this app to make changes to your device?", click **Yes**.
3. In the setup wizard click **Next**, keep the default folder, and click **Next** again.
4. On the last page keep **Run IB Gateway** checked and click **Finish**.
5. Later, start it from the Start menu: type "IB Gateway".

## 2b. macOS

1. Open your **Downloads** folder and double-click the `.dmg` file.
2. In the window that opens, double-click the installer. If macOS asks whether you want to open an app downloaded
   from the internet, click **Open**.
3. Follow the setup wizard: **Next**, keep the default folder, **Next**.
4. Finish with **Run IB Gateway** checked.
5. Later, start it from **Applications** (or Spotlight: type "IB Gateway").

## 2c. Linux (as shown in the lesson)

1. Open your **Downloads** folder in the file manager, right-click an empty area and choose **Open Terminal Here**
   (or open a terminal and type `cd ~/Downloads`).
2. Type these three commands, pressing Enter after each:

   ```
   ls -lh
   chmod +x ibgateway-stable-standalone-linux-x64.sh
   ./ibgateway-stable-standalone-linux-x64.sh
   ```

   `ls -lh` lists the files with their sizes, `chmod +x` lets the script run as a program, `./…` runs it. You will see
   "Unpacking JRE" and "Starting Installer". A line like `dbind-WARNING … accessibility bus` may appear: it is
   harmless.
3. The setup wizard opens: **Next**, keep the folder (`Jts/ibgateway/1050` in your home folder, about 991 MB),
   **Next**, wait for it to install, keep **Run IB Gateway 10.50** checked, **Finish**.
4. Later, start it from your applications menu or the desktop icon the installer created.

## 3. First launch: log in to paper

1. The login window asks two things before any password:
   - **API Type**: choose **IB API**. (FIX CTCI is selected by default; it is a protocol for institutions, not for us.)
   - **Trading Mode**: choose **Paper Trading**. A red **SIMULATED TRADING** bar appears.
2. Type your **paper** username and password and click **Paper Log In**. Depending on your account, IBKR may ask you
   to approve the login in the **IBKR Mobile** app.
3. If you see **Existing session detected**, another session with the same username is open (for example TWS).
   **Continue Login** disconnects it.
4. IBKR shows a warning that this is a paper account for simulated trading. Read it and confirm.
5. The status window opens. You want: **Interactive Brokers API Server: connected**, **Market Data Farm: ON**,
   **Historical Data Farm: ON**.

Next: set up the API with `configure-the-api.md`.
