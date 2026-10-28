"""Red team (4): in a FAKE account, make the daily loss limit look hit and show a new entry is refused.

Run from your desk: .venv/bin/python -m pytest -q -s path/to/test_redteam_daily_loss.py
No Gateway, no account: everything runs against the desk's in-memory fake broker.
"""

import json
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path.home() / "trading-desk" / "tests"))  # the desk's own test fakes
from mcp_fakes import anyio_backend, data, mcp_rig  # noqa: F401,E402

pytestmark = pytest.mark.anyio


def args(rig):
    return {"size_r": 0.5, "stop": round(rig.ref - 3, 2), "target": round(rig.ref + 8, 2), "reason": "red team: loss-limit test"}


def day_opened_at_100k(rig):
    """Record the day's first net-liquidation reading ($100,000), as the lab does on its first check of the day."""
    assert rig.risk._day_start_equity(rig.ib) == 100_000.0


async def test_control_down_400_still_allowed(mcp_rig):
    rig = mcp_rig()
    day_opened_at_100k(rig)
    rig.ib.net_liquidation = 99_600.0  # down $400, under the $500 limit
    async with rig.client() as c:
        out = await c.call_tool("place_bracket", args(rig))
    assert not out.is_error and data(out)["status"] == "bought"


async def test_down_600_refuses_a_new_entry(mcp_rig):
    rig = mcp_rig()
    day_opened_at_100k(rig)
    rig.ib.net_liquidation = 99_400.0  # down $600, past the $500 limit
    async with rig.client() as c:
        out = await c.call_tool("place_bracket", args(rig))
    text = out.content[0].text
    print("REFUSAL TEXT:", text)
    assert out.is_error and "daily_loss_limit" in text
    assert [o for _, o in rig.ib.placed if o.action == "BUY"] == []  # no buy order ever reached the fake IB
    print("JOURNAL:", json.dumps(rig.journal()[-1]))
    assert rig.journal()[-1]["outcome"] == "refused"
