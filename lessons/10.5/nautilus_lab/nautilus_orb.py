"""ORB (15-minute range, QQQ, long only, stop = range low, 1R target, flat before the close) on NautilusTrader.

Same rules and the same costs as the lab's strategies/opening_range_breakout.py + backtests/engine.py.

Two fill timings (--timing):
  next_open  (default) a decision made at a bar's close fills at the NEXT bar's open, like the lab's engine.
             Nautilus has no such mode (a market order sent from on_bar fills at that bar's close), so each
             bar's open price is also fed as a one-tick TradeTick stamped just after the previous bar's
             close. The strategy sends its pending order from on_trade_tick, so it fills at that open print.
  bar_close  Nautilus' own behaviour: the order goes out in on_bar and fills at that bar's close.

Costs: the lab's CostModel is commission 1c/share per side, spread 1c (half per fill), slippage 1c on
market-type fills (entry, stop, time exit) and none on the limit target. Nautilus fills at the raw price;
the whole per-share cost is charged as commission by OrbFee, which moves cash exactly like paying
a worse price would.

Paper research only. Nothing here touches a broker.
"""
import os

import argparse
import math
from decimal import Decimal

import exchange_calendars as xcals
import pandas as pd

from nautilus_trader.backtest.engine import BacktestEngine
from nautilus_trader.backtest.models import FeeModel
from nautilus_trader.config import BacktestEngineConfig, LoggingConfig, StrategyConfig
from nautilus_trader.model.currencies import USD
from nautilus_trader.model.data import Bar, BarType, TradeTick
from nautilus_trader.model.enums import AccountType, AggressorSide, OmsType, OrderSide, OrderType
from nautilus_trader.model.identifiers import InstrumentId, Symbol, TradeId, Venue
from nautilus_trader.model.instruments import Equity
from nautilus_trader.model.objects import Money, Price, Quantity
from nautilus_trader.trading.strategy import Strategy

NY = "America/New_York"
BAR_MIN = 5
COMMISSION, SPREAD, SLIPPAGE = 0.01, 0.01, 0.01  # = backtests.engine.CostModel defaults
START_EQUITY = 100_000.0

VENUE = Venue("XNAS")
INSTRUMENT_ID = InstrumentId(Symbol("QQQ"), VENUE)
BAR_TYPE = BarType.from_str("QQQ.XNAS-5-MINUTE-LAST-EXTERNAL")


class OrbFee(FeeModel):
    """Per-share lab costs charged as commission: 1c commission + half spread, + slippage on market-type orders."""

    def get_commission(self, order, fill_qty, fill_px, instrument):
        per_share = COMMISSION + SPREAD / 2
        if order.order_type != OrderType.LIMIT:
            per_share += SLIPPAGE
        return Money(round(float(fill_qty) * per_share, 6), USD)


class OrbConfig(StrategyConfig, frozen=True):
    next_open: bool = True
    range_minutes: int = 15
    target_r: float = 1.0
    risk_pct: float = 0.01
    last_entry_minutes_before_close: int = 30
    flatten_minutes_before_close: int = 5


class Orb(Strategy):
    def __init__(self, config: OrbConfig):
        super().__init__(config)
        self.cal = xcals.get_calendar("XNYS")
        self._close_cache: dict = {}
        self.day = None
        self.rng_high = self.rng_low = None
        self.rng_n = 0
        self.broke = False
        self.pending = None  # ("entry", stop, target, ref_px) or ("exit",)
        self.fills: list[dict] = []
        self.equity_rows: list[tuple] = []
        self.skipped_zero_qty = 0

    # -- helpers -----------------------------------------------------------------------------
    def session_close(self, date):
        if date not in self._close_cache:
            self._close_cache[date] = self.cal.session_close(pd.Timestamp(date))
        return self._close_cache[date]

    def balance(self) -> float:
        acct = self.portfolio.account(VENUE)
        return float(acct.balance_total(USD).as_double())

    def net_qty(self) -> int:
        return int(self.portfolio.net_position(INSTRUMENT_ID))

    # -- lifecycle ---------------------------------------------------------------------------
    def on_start(self):
        self.instrument = self.cache.instrument(INSTRUMENT_ID)
        self.subscribe_bars(BAR_TYPE)
        if self.config.next_open:
            self.subscribe_trade_ticks(INSTRUMENT_ID)

    def on_bar(self, bar: Bar):
        cfg = self.config
        end = pd.Timestamp(bar.ts_event, unit="ns", tz="UTC")
        start = (end - pd.Timedelta(minutes=BAR_MIN)).tz_convert(NY)
        close_px = bar.close.as_double()
        qty = self.net_qty()
        self.equity_rows.append((end, self.balance() + qty * close_px))

        if start.date() != self.day:
            self.day, self.rng_high, self.rng_low, self.rng_n, self.broke = start.date(), None, None, 0, False
        session_close = self.session_close(start.date())
        flatten_now = end >= session_close - pd.Timedelta(minutes=cfg.flatten_minutes_before_close)
        may_enter = start < session_close - pd.Timedelta(minutes=cfg.last_entry_minutes_before_close)

        if qty > 0:
            if flatten_now:
                self.pending = ("exit",)
                if not cfg.next_open:
                    self.fire(close_px)
            return

        open_at = pd.Timestamp.combine(start.date(), pd.Timestamp("09:30").time()).tz_localize(NY)
        range_end = open_at + pd.Timedelta(minutes=cfg.range_minutes)
        if open_at <= start < range_end:
            h, l = bar.high.as_double(), bar.low.as_double()
            self.rng_high = h if self.rng_high is None else max(self.rng_high, h)
            self.rng_low = l if self.rng_low is None else min(self.rng_low, l)
            self.rng_n += 1
            return
        if start < range_end or self.rng_n < cfg.range_minutes // BAR_MIN or self.broke:
            return
        if close_px > self.rng_high:  # strictly above; only the first such bar of the day counts
            self.broke = True
            if may_enter and self.rng_low < close_px:
                target = close_px + cfg.target_r * (close_px - self.rng_low)
                self.pending = ("entry", self.rng_low, target)
                if not cfg.next_open:
                    self.fire(close_px)

    def on_trade_tick(self, tick: TradeTick):
        if self.pending is not None:
            self.fire(tick.price.as_double())

    # -- orders ------------------------------------------------------------------------------
    def fire(self, ref_px: float):
        """Send the pending order. `ref_px` is the price it is expected to fill at (open print or bar close)."""
        pending, self.pending = self.pending, None
        if pending[0] == "exit":
            if self.net_qty() > 0:
                self.cancel_all_orders(INSTRUMENT_ID)
                self.close_all_positions(INSTRUMENT_ID, tags=["time"])
            return
        _, stop, target = pending
        if self.net_qty() != 0:
            return
        cash = self.balance()
        fill = ref_px + SPREAD / 2 + SLIPPAGE
        risk_ps = fill - stop + 2 * COMMISSION + SPREAD / 2 + SLIPPAGE  # same formula as backtests/engine.py
        if not stop < fill or risk_ps <= 0:
            return
        qty = math.floor(cash * self.config.risk_pct / risk_ps)
        qty = min(qty, math.floor(cash / fill))  # no leverage
        if qty <= 0:
            self.skipped_zero_qty += 1
            return
        orders = self.order_factory.bracket(
            instrument_id=INSTRUMENT_ID,
            order_side=OrderSide.BUY,
            quantity=Quantity.from_int(qty),
            tp_price=Price.from_str(f"{target:.2f}"),
            sl_trigger_price=Price.from_str(f"{stop:.2f}"),
            tp_post_only=False,  # a plain limit sell, so a gap above it can fill at the open
        )
        self.submit_order_list(orders)

    def on_order_filled(self, event):
        order = self.cache.order(event.client_order_id)
        if order.order_type == OrderType.STOP_MARKET:
            reason = "stop"
        elif order.order_type == OrderType.LIMIT and order.side == OrderSide.SELL:
            reason = "target"
        elif order.side == OrderSide.SELL:
            reason = "time"
        else:
            reason = "entry"
        self.fills.append({
            "time": pd.Timestamp(event.ts_event, unit="ns", tz="UTC"),
            "side": order.side.name, "qty": int(event.last_qty), "px": event.last_px.as_double(),
            "commission": event.commission.as_double(), "reason": reason,
        })


def build_data(bars: pd.DataFrame, instrument: Equity, with_open_ticks: bool):
    """Bars stamped at their CLOSE (Nautilus' convention), plus optional open prints just after the previous close."""
    data = []
    ends = (bars.index + pd.Timedelta(minutes=BAR_MIN)).as_unit("ns").asi8  # pandas 3 defaults to us
    starts = bars.index.as_unit("ns").asi8
    last_end = None
    n = 0
    for i, (ts, r) in enumerate(bars.iterrows()):
        if with_open_ticks:
            # right after the previous bar's close when it is the same session's previous bar, else at the start
            t = starts[i] + 1 if (last_end is not None and last_end == starts[i]) else starts[i]
            n += 1
            data.append(TradeTick(
                INSTRUMENT_ID, Price.from_str(f"{r.open:.2f}"), Quantity.from_int(100_000_000),
                AggressorSide.BUYER, TradeId(f"T{n}"), int(t), int(t)))
        data.append(Bar(
            BAR_TYPE, Price.from_str(f"{r.open:.2f}"), Price.from_str(f"{r.high:.2f}"),
            Price.from_str(f"{r.low:.2f}"), Price.from_str(f"{r.close:.2f}"),
            Quantity.from_int(int(r.volume)), int(ends[i]), int(ends[i])))
        last_end = ends[i]
    return data


def run(bars: pd.DataFrame, timing: str = "next_open", adaptive: bool = False):
    instrument = Equity(
        instrument_id=INSTRUMENT_ID, raw_symbol=Symbol("QQQ"), currency=USD,
        price_precision=2, price_increment=Price.from_str("0.01"), lot_size=Quantity.from_int(1),
        isin="US46090E1038", ts_event=0, ts_init=0,
        maker_fee=Decimal(0), taker_fee=Decimal(0),
    )
    engine = BacktestEngine(BacktestEngineConfig(logging=LoggingConfig(log_level="ERROR")))
    engine.add_venue(
        venue=VENUE, oms_type=OmsType.NETTING, account_type=AccountType.CASH, base_currency=USD,
        starting_balances=[Money(START_EQUITY, USD)], fee_model=OrbFee(),
        bar_adaptive_high_low_ordering=adaptive,
        allow_cash_borrowing=True,  # lab engine lets cash dip a few dollars below 0 when the no-leverage cap binds
    )
    engine.add_instrument(instrument)
    engine.add_data(build_data(bars, instrument, with_open_ticks=timing == "next_open"))
    strat = Orb(OrbConfig(next_open=timing == "next_open"))
    engine.add_strategy(strat)
    engine.run()
    final_cash = float(engine.portfolio.account(VENUE).balance_total(USD).as_double())
    engine.dispose()
    return strat, final_cash


def to_trades(strat: Orb) -> pd.DataFrame:
    """Pair each entry fill with the sell fill that closes it; same columns as the lab engine's trades."""
    rows, entry = [], None
    for f in strat.fills:
        if f["side"] == "BUY":
            entry = f
        else:
            assert entry is not None and entry["qty"] == f["qty"], (entry, f)
            gross = f["qty"] * (f["px"] - entry["px"])
            comm = entry["commission"] + f["commission"]
            rows.append({
                "entry_time": entry["time"], "exit_time": f["time"], "entry_price": entry["px"],
                "exit_price": f["px"], "shares": f["qty"], "reason": f["reason"],
                "gross_pnl": gross, "costs": comm, "net_pnl": gross - comm,
            })
            entry = None
    return pd.DataFrame(rows)


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--timing", choices=["next_open", "bar_close"], default="next_open")
    ap.add_argument("--adaptive", action="store_true", help="bar_adaptive_high_low_ordering=True")
    ap.add_argument("--bars", default=os.path.expanduser("~/nautilus_lab/data/QQQ_5min_from_2024-10-21.parquet"))
    ap.add_argument("--out", default=os.path.expanduser("~/nautilus_lab/out"))
    ap.add_argument("--limit-days", type=int, default=0, help="only the first N sessions (smoke test)")
    a = ap.parse_args()
    bars = pd.read_parquet(a.bars)
    if a.limit_days:
        days = bars.index.tz_convert(NY).normalize().unique()[: a.limit_days]
        bars = bars[bars.index.tz_convert(NY).normalize().isin(days)]
    strat, final_cash = run(bars, a.timing, a.adaptive)
    trades = to_trades(strat)
    tag = f"nautilus_{a.timing}{'_adaptive' if a.adaptive else ''}"
    trades.to_csv(f"{a.out}/{tag}_trades.csv", index=False)
    eq = pd.Series(dict(strat.equity_rows), name="equity")
    eq.to_csv(f"{a.out}/{tag}_equity.csv")
    print(f"{tag}: {len(trades)} trades, final cash {final_cash:,.2f}, "
          f"sum(net_pnl) {trades.net_pnl.sum():,.2f}, zero-qty skips {strat.skipped_zero_qty}")
    print(trades.reason.value_counts().to_dict())
