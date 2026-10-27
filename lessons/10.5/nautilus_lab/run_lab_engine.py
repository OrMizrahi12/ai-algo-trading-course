"""Run OUR engine on the copied bars (not data/cache). Usage: cd trading-lab && uv run python <this> """
import os
import sys
import pandas as pd
sys.path.insert(0, os.path.expanduser("~/trading-lab"))
from backtests.engine import run_backtest, CostModel
from strategies.opening_range_breakout import OpeningRangeBreakout, OpeningRangeBreakoutParams

bars = pd.read_parquet(os.path.expanduser("~/nautilus_lab/data/QQQ_5min_from_2024-10-21.parquet"))
strat = OpeningRangeBreakout(OpeningRangeBreakoutParams(range_minutes=15, target_r=1.0))
res = run_backtest(bars, strat)
res.trades.to_csv(os.path.expanduser("~/nautilus_lab/out/lab_trades.csv"), index=False)
res.equity.to_csv(os.path.expanduser("~/nautilus_lab/out/lab_equity.csv"))
for k, v in res.stats.items(): print(k, v)
print(CostModel())
