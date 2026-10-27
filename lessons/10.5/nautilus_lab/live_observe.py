"""ORB (15-minute range, QQQ, long only, stop = range low, 1R target) watching the IB PAPER Gateway. NO ORDERS.

Safety, in layers:
  1. Only a DATA client is configured. No execution client exists, so Nautilus has no route to place an order.
  2. The strategy never calls submit_*; those methods are overridden to raise, as a second lock.
  3. Host 127.0.0.1, port 4002 (IB Gateway paper) are asserted before the node is built.
  4. On start, every account IB reports must begin with DU (paper); otherwise the node stops.

Usage: timeout --signal=INT 240 .venv/bin/python live_observe.py
"""

import math

import exchange_calendars as xcals
import pandas as pd
from ibapi.common import MarketDataTypeEnum

from nautilus_trader.adapters.interactive_brokers.common import IB
from nautilus_trader.adapters.interactive_brokers.config import (
    InteractiveBrokersDataClientConfig,
    InteractiveBrokersInstrumentProviderConfig,
    SymbologyMethod,
)
from nautilus_trader.adapters.interactive_brokers.factories import (
    IB_CLIENTS,
    InteractiveBrokersLiveDataClientFactory,
)
from nautilus_trader.config import LiveExecEngineConfig, LoggingConfig, StrategyConfig, TradingNodeConfig
from nautilus_trader.live.node import TradingNode
from nautilus_trader.model.data import Bar, BarType
from nautilus_trader.model.identifiers import InstrumentId
from nautilus_trader.trading.strategy import Strategy

HOST, PORT, CLIENT_ID = "127.0.0.1", 4002, 30
NY = "America/New_York"
BAR_MIN = 5
INSTRUMENT_ID = InstrumentId.from_str("QQQ.NASDAQ")  # IB_SIMPLIFIED symbology: SYMBOL.PRIMARY_EXCHANGE
BAR_TYPE = BarType.from_str("QQQ.NASDAQ-5-MINUTE-LAST-EXTERNAL")
HYPOTHETICAL_EQUITY = 100_000.0  # only to show a share count; there is no account behind it

assert HOST == "127.0.0.1" and PORT == 4002, "paper IB Gateway on localhost only"


class ObserveConfig(StrategyConfig, frozen=True):
    range_minutes: int = 15
    target_r: float = 1.0
    risk_pct: float = 0.01
    history_days: int = 3


class OrbObserver(Strategy):
    def __init__(self, config: ObserveConfig):
        super().__init__(config)
        self.cal = xcals.get_calendar("XNYS")
        self.day = None
        self.rng_high = self.rng_low = None
        self.rng_n = 0
        self.broke = False
        self.n_hist = self.n_live = 0

    # -- second lock: this class can never send an order ---------------------------------------
    def submit_order(self, *a, **k):
        raise RuntimeError("observe-only: orders are disabled")

    def submit_order_list(self, *a, **k):
        raise RuntimeError("observe-only: orders are disabled")

    # -- lifecycle -----------------------------------------------------------------------------
    def on_start(self):
        accounts = set()
        for c in IB_CLIENTS.values():
            accounts |= c.accounts()
        self.log.info(f"IB accounts reported by the Gateway: {sorted(accounts)}")
        if not accounts or not all(a.startswith("DU") for a in accounts):
            self.log.error("NOT a paper (DU...) account: stopping")
            self.stop()
            return

        self.instrument = self.cache.instrument(INSTRUMENT_ID)
        if self.instrument is None:
            self.log.error(f"{INSTRUMENT_ID} not loaded")
            self.stop()
            return
        self.log.info(
            f"Instrument loaded: {self.instrument.id} {type(self.instrument).__name__} "
            f"tick {self.instrument.price_increment} lot {self.instrument.lot_size}",
        )
        # End the history request at the last finished session close, not "now": an end time of "now" makes IB
        # treat it as up-to-the-second data (error 2188), which this delayed-data account has no subscription for.
        now = self.clock.utc_now()
        end = self.cal.previous_close(now.floor("min") + pd.Timedelta(minutes=1)).tz_convert("UTC")
        self.request_bars(BAR_TYPE, start=end - pd.Timedelta(days=self.config.history_days), end=end)
        # subscribe_bars removed for this test: its keepUpToDate request needs a real-time data subscription
        self.log.info("Requested recent 5-min bars (history only, no subscription)")

    def on_historical_data(self, data):
        if isinstance(data, Bar):
            self.n_hist += 1
            self.step(data, live=False)

    def on_bar(self, bar: Bar):
        self.n_live += 1
        self.step(bar, live=True)

    # -- the ORB rule, logging only ------------------------------------------------------------
    def step(self, bar: Bar, live: bool):
        end = pd.Timestamp(bar.ts_event, unit="ns", tz="UTC")
        start = (end - pd.Timedelta(minutes=BAR_MIN)).tz_convert(NY)
        tag = "LIVE" if live else "hist"
        age = (self.clock.utc_now() - end).total_seconds() / 60
        if live or self.n_hist <= 3:
            self.log.info(
                f"[{tag}] bar {start:%Y-%m-%d %H:%M} NY  O {bar.open} H {bar.high} L {bar.low} C {bar.close} "
                f"V {bar.volume}  (closed {age:,.0f} min ago)",
            )
        if start.date() != self.day:
            self.day, self.rng_high, self.rng_low, self.rng_n, self.broke = start.date(), None, None, 0, False
        session_close = self.cal.session_close(pd.Timestamp(start.date()))
        open_at = pd.Timestamp.combine(start.date(), pd.Timestamp("09:30").time()).tz_localize(NY)
        range_end = open_at + pd.Timedelta(minutes=self.config.range_minutes)
        close_px = bar.close.as_double()
        if open_at <= start < range_end:
            h, l = bar.high.as_double(), bar.low.as_double()
            self.rng_high = h if self.rng_high is None else max(self.rng_high, h)
            self.rng_low = l if self.rng_low is None else min(self.rng_low, l)
            self.rng_n += 1
            return
        if start < range_end or self.rng_n < self.config.range_minutes // BAR_MIN or self.broke:
            return
        if close_px > self.rng_high:
            self.broke = True
            if start < session_close - pd.Timedelta(minutes=30) and self.rng_low < close_px:
                target = close_px + self.config.target_r * (close_px - self.rng_low)
                qty = math.floor(HYPOTHETICAL_EQUITY * self.config.risk_pct / (close_px - self.rng_low))
                self.log.warning(
                    f"[{tag}] WOULD BUY {qty} QQQ near {close_px:.2f}, stop {self.rng_low:.2f}, "
                    f"target {target:.2f} -- NOT SENT (observe-only)",
                )


def main():
    data_cfg = InteractiveBrokersDataClientConfig(
        ibg_host=HOST,
        ibg_port=PORT,
        ibg_client_id=CLIENT_ID,
        market_data_type=MarketDataTypeEnum.DELAYED_FROZEN,  # no real-time subscription on this account
        use_regular_trading_hours=True,
        instrument_provider=InteractiveBrokersInstrumentProviderConfig(
            symbology_method=SymbologyMethod.IB_SIMPLIFIED,
            load_ids=frozenset([INSTRUMENT_ID]),
        ),
    )
    config = TradingNodeConfig(
        logging=LoggingConfig(log_level="INFO", use_pyo3=False),
        exec_engine=LiveExecEngineConfig(reconciliation=False),
        data_clients={IB: data_cfg},  # no exec_clients on purpose
    )
    node = TradingNode(config=config)
    node.trader.add_strategy(OrbObserver(ObserveConfig()))
    node.add_data_client_factory(IB, InteractiveBrokersLiveDataClientFactory)
    node.build()
    try:
        node.run()
    finally:
        node.dispose()


if __name__ == "__main__":
    main()
