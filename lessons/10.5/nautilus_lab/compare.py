"""Compare lab engine vs Nautilus runs. Run from the lab: cd trading-lab && uv run python ~/nautilus_lab/compare.py"""
import os
import sys
import pandas as pd
sys.path.insert(0, os.path.expanduser("~/trading-lab"))
from backtests.metrics import compute_metrics

O = os.path.expanduser("~/nautilus_lab/out")
START = 100_000.0
def T(f):
    t = pd.read_csv(f"{O}/{f}_trades.csv", parse_dates=["entry_time", "exit_time"])
    if f.startswith("nautilus"):  # fill stamp -> start of the 5-min bar it happened in (stamps are bar CLOSE, or open print +1ns)
        for c in ("entry_time", "exit_time"):
            t[c] = (t[c].dt.as_unit("ns") - pd.Timedelta(1, "ns")).dt.floor("5min").dt.as_unit("us")
    return t
lab = T("lab")
lab_eq = pd.read_csv(f"{O}/lab_equity.csv", index_col=0, parse_dates=True).iloc[:, 0]
HALF = 0.005; SL = 0.01
# the lab's entry_price/exit_price include spread+slippage; strip them back to raw bar prices
lab["entry_raw"] = lab.entry_price - HALF - SL
lab["exit_raw"] = lab.apply(lambda r: r.exit_price + HALF if r.reason == "target" else r.exit_price + HALF + SL, axis=1)

def with_r(t):
    t = t.copy()
    cash_before = START + t.net_pnl.cumsum().shift(fill_value=0)
    t["r_multiple"] = t.net_pnl / (0.01 * cash_before)
    return t

runs = {"lab engine": (lab, lab_eq)}
for tag in ["nautilus_next_open", "nautilus_next_open_adaptive", "nautilus_bar_close"]:
    t = with_r(T(tag))
    eq = pd.read_csv(f"{O}/{tag}_equity.csv", index_col=0, parse_dates=True).iloc[:, 0]
    eq.index = eq.index - pd.Timedelta(minutes=5)  # Nautilus stamps bars at their close, the lab at their start
    runs[tag] = (t, eq)

rows = {}
for name, (t, eq) in runs.items():
    m = compute_metrics(t, eq, START)
    rows[name] = {**m, "gross_pnl": t.gross_pnl.sum(), "costs": t.costs.sum(), "final_equity": eq.iloc[-1],
                  "target": (t.reason == "target").sum(), "stop": (t.reason == "stop").sum(), "time": (t.reason == "time").sum(),
                  "shares_mean": t.shares.mean()}
df = pd.DataFrame(rows)
pd.set_option("display.float_format", lambda x: f"{x:,.4f}"); pd.set_option("display.width", 200)
print(df.to_string())

def diff(n):
    a = lab.copy(); b = runs[n][0].copy()
    a["d"] = a.entry_time.dt.tz_convert("America/New_York").dt.date
    b["d"] = b.entry_time.dt.tz_convert("America/New_York").dt.date
    m = a.merge(b, on="d", how="outer", suffixes=("_lab", "_nt"), indicator=True)
    print(f"\n=== {n} vs lab: trade-by-trade ===")
    print(m._merge.value_counts().to_dict())
    m = m[m._merge == "both"]
    same_entry_t = (m.entry_time_lab.dt.floor("5min") == m.entry_time_nt.dt.floor("5min"))
    print("same entry bar:", same_entry_t.sum(), "of", len(m))
    print("same entry raw price (<=1c):", ((m.entry_raw - m.entry_price_nt).abs() < 0.0051).sum())
    print("same shares:", (m.shares_lab == m.shares_nt).sum(), " shares off by 1..3:", ((m.shares_lab - m.shares_nt).abs().between(1, 3)).sum(),
          " max |diff|:", (m.shares_lab - m.shares_nt).abs().max())
    print("same exit reason:", (m.reason_lab == m.reason_nt).sum())
    print("same exit bar:", (m.exit_time_lab.dt.floor("5min") == m.exit_time_nt.dt.floor("5min")).sum())
    print("same exit raw price (<=1c):", ((m.exit_raw - m.exit_price_nt).abs() < 0.0051).sum())
    m["dpnl"] = m.net_pnl_nt - m.net_pnl_lab
    print("net pnl diff per trade: mean %.3f  min %.2f  max %.2f  sum %.2f" % (m.dpnl.mean(), m.dpnl.min(), m.dpnl.max(), m.dpnl.sum()))
    print("trades with |diff| > $5:", (m.dpnl.abs() > 5).sum())
    cols = ["d", "entry_time_lab", "entry_time_nt", "entry_raw", "entry_price_nt", "shares_lab", "shares_nt", "reason_lab", "reason_nt", "exit_raw", "exit_price_nt", "net_pnl_lab", "net_pnl_nt", "dpnl"]
    print(m.reindex(m.dpnl.abs().sort_values(ascending=False).index)[cols].head(8).to_string())
    return m

for n in ["nautilus_next_open", "nautilus_next_open_adaptive", "nautilus_bar_close"]:
    m = diff(n)
    m.to_csv(f"{O}/diff_{n}.csv", index=False)
