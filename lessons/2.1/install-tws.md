# Install Trader Workstation (TWS): Windows, macOS, Linux

Versions on 2026-10-21: **Stable 10.50.1f** (the one we use), Latest 10.51.1d. Your numbers will be newer; pick the
tab named **Stable**. Both Stable and Latest update themselves when you log in. The two **Offline** versions never
update themselves (IBKR suggests them for API users who want to pin one exact version; we come back to this in
module 4).

## 1. Download (all systems)

1. Go to **interactivebrokers.com**.
2. Open the **Platforms** menu. Under **Platform Downloads**, choose **Trader Workstation**.
   (Direct page: interactivebrokers.com/en/trading/download-tws.php)
3. Click the **Stable** tab.
4. Pick the card for your system and click **Download**:
   - **Windows** (64-bit; also for Windows 11 Arm devices): an `.exe` installer.
   - **Apple Silicon** (M-series Macs) or **Apple Intel Processor**: a `.dmg` installer. Not sure which Mac you have?
     Apple menu → **About This Mac**: "Chip Apple M…" means Apple Silicon; "Processor … Intel" means Intel.
   - **Linux** (64-bit): a `.sh` installer script (about 106 MB on 2026-10-21).

The installers bring their own Java runtime: you don't need to install Java yourself.

## 2a. Windows

1. Open your **Downloads** folder and double-click the TWS installer (`tws-stable-windows-x64.exe` or similar).
2. If Windows asks "Do you want to allow this app to make changes to your device?", click **Yes**.
3. In the setup wizard click **Next** through the steps. Keep the default folder (`C:\Jts`) and keep the desktop
   icon.
4. On the last page keep **Run Trader Workstation** checked and click **Finish**.
5. Later, start TWS from the desktop icon or the Start menu ("Trader Workstation").

## 2b. macOS

1. Open your **Downloads** folder and double-click the `.dmg` file.
2. In the window that opens, double-click the installer. If macOS asks whether you want to open an app downloaded
   from the internet, click **Open**.
3. Follow the setup wizard (**Next** through the steps; keep the defaults).
4. Finish with **Run Trader Workstation** checked.
5. Later, start TWS from **Applications → Trader Workstation** (or Launchpad / Spotlight: type "Trader Workstation").

## 2c. Linux (as shown in the lesson)

1. Open your **Downloads** folder in the file manager, right-click an empty area and choose **Open Terminal Here**
   (or open a terminal and type `cd ~/Downloads`).
2. Type these three commands, pressing Enter after each:

   ```
   ls
   chmod +x tws-stable-linux-x64.sh
   ./tws-stable-linux-x64.sh
   ```

   `ls` lists the files, `chmod +x` lets the script run as a program, `./…` runs it. A line like
   `dbind-WARNING … accessibility bus` may appear: it is harmless.
3. The setup wizard opens: **Next**, keep the folder `Jts` in your home folder (about 738 MB), **Next**, wait for it to
   install, keep **Run Trader Workstation** checked, **Finish**.
4. Later, start TWS from your applications menu or the desktop icon the installer created.

## 3. First launch: log in to paper

1. The login window shows two tabs: **Live Trading** and **Paper Trading**. Click **Paper Trading**. The window turns
   **red** with "SIMULATED TRADING" across the top.
2. Type your username and password and click **Paper Log In**.
   - Many accounts can use their normal username here. If yours can't, use the paper username shown in your account
     settings under **Settings → Account Configuration → Paper Trading Account**.
3. If IBKR asks for two-factor approval, approve it in **IBKR Mobile** on your phone.
4. TWS shows a warning: "This is not a brokerage account. This is a 'paper' trading account…". Click
   **I understand and accept**.
5. TWS opens in the **Mosaic** layout. Maximize the window.
6. Text too small? Click the **Aa** button at the top right (**Font Size Adjustment**) and click **Larger** a few
   times. **Smaller** takes it back.
7. Check the paper markers: the red strip "THIS IS NOT A BROKERAGE ACCOUNT. THIS IS A PAPER TRADING ACCOUNT FOR
   SIMULATED TRADING." and a paper account number (it starts with "DU") at the top right. Keep that number private.

## 4. If prices are missing or delayed

- Prices on a **dark olive background** are delayed (about 15 minutes). That is normal: this course uses the free
  delayed data and the free price history. Real-time prices are an optional paid add-on (see
  `market-data-and-permissions.md`, "Optional").
- "**No market data permissions for IDEALPRO CASH**" on EUR.USD or another currency pair means your account has no
  Forex trading permission. You don't need it: this course trades US stocks and ETFs, not forex.
