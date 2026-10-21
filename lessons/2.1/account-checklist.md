# Your account: the checklist

Facts below come from IBKR's official pages as read on 2026-10-21. Check the live pages, as they change.

## What this course needs

- [ ] **An IBKR Pro account.** IBKR's API documentation lists "A funded and opened IBKR Pro account" as the first
      requirement. The API works only with IBKR Pro: if your account is IBKR Lite, switch it to Pro in your account
      settings first. (interactivebrokers.com/docs/tws-api/doc/notes-limitations/requirements)
- [ ] **Opened:** your application has been approved.
- [ ] **Funded:** real money has been deposited. (The market data subscriptions you may add later also need a
      minimum account balance; see `market-data-and-permissions.md`.)
- [ ] **A paper trading account.** New individual accounts get one automatically, tied to the live account. Its
      username and account number are in your account settings: **Settings → Account Configuration → Paper Trading
      Account**. (ibkrguides.com, "About Paper Trading Accounts" and "Paper Trading Account")
- [ ] **Two-factor login.** IBKR requires two-factor authentication for all users. The simplest option is IB Key in
      the IBKR Mobile app: when TWS asks, you approve the login on your phone.

## Opening an account (if you don't have one yet)

On interactivebrokers.com, **Open Account** starts the application in three steps:

1. Create a username and password.
2. Confirm your email and phone number.
3. Complete the application.

You'll need personal and contact details, income and tax information, your trading experience and objectives, and
funding details. A regulated broker has to verify who you are, so have an ID document ready.

## What about the free trial?

IBKR's free trial gives you the platforms with simulated money, but its data is delayed by 10 to 15 minutes (except
OTC spot FX and metals), and it is not the funded IBKR Pro account the API requires. In this course we use a funded
IBKR Pro account and its paper account.

## The paper account in short

- It works like a real account (most order types, all instruments available to your account, almost every part of
  TWS), but trades are never sent to an exchange: the simulator fills them at real market prices and sizes.
- It starts with USD 1,000,000 of paper money. You can reset it later in the account settings.
- Its trading permissions and market data are the same as your live account's.
- Limitations include: fills simulated from the top of the book (no deep book), stops and other complex orders
  always simulated, and some order types not supported. Results on paper can look better than with real money.
- The TWS login window turns **red** with "SIMULATED TRADING" when the Paper Trading tab is selected. If you don't
  see the red look, you are not on paper.
