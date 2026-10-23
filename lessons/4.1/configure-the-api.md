# Configure the Gateway's API (the lesson's settings)

In the Gateway's status window: **Configure → Settings**. The window is called "TWS Configuration (Simulated
Trading)" (the Gateway uses the same settings window as TWS). The number in its title is your paper account: keep it
private.

## API → Settings

| Setting | What we use | Why |
|---|---|---|
| Read-Only API | **On** (ticked; the default) | Programs can read data but never place orders. It stays on until the order lessons. |
| Socket port | **4002** (the default) | The Gateway's paper port. Our code connects here. |
| Master API client ID | **Empty** | Each program connects with its own client ID; we don't need a master yet. |
| Everything else | Leave the defaults | Later lessons come back to what they need. |

There is no "Enable ActiveX and Socket Clients" box in the Gateway: its API is always on. On this Gateway version
the page also has no trusted-IP or "localhost only" option: programs on the same computer can connect.

## API → Precautions

Leave every **Bypass …** box **unticked**. Each one would skip one of IBKR's order warnings for API orders.

## Lock and Exit

1. By default the Gateway logs off every night (Auto logoff, 11:45 PM in the lesson).
2. Choose **Auto restart**. The page then says "The application will automatically restart at 11:45 PM". The time is
   your computer's clock (our computer runs on UTC). Pick a time when you don't need the Gateway.
3. Click **OK**. IBKR confirms that the platform will restart daily: click **OK**.

What Auto restart means:

- The Gateway restarts itself every day without asking for your password again, for up to a week.
- About once a week, after IBKR's weekend reset, you log in again by hand (and approve on your phone if asked).

## Last

Back in the status window, tick **Show API messages**: when a program connects, its messages appear there.

You're done when the status window shows **API Server: connected** and both data farms **ON**.
