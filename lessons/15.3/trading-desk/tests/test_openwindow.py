"""The open-window agent: the SPY desk's safety layers carried over, the window rules added, the SPY desk's instructions untouched."""

import dataclasses
import json
from datetime import date
from types import SimpleNamespace

import pandas as pd
import pytest

from conftest import LIMITS, FakeFeed, FakeModel, WAIT, buy, make_bars, sell
from desk import execute, lab, model, openwindow, snapshot, trades
from desk.heartbeat import Halted
from desk.journal import State
from desk.openwindow import (CONSTITUTION, CLIENT_ID, OpenHeartbeat, OpenJournal, OpenReviewer, OpenWindow, OpenWindowModel,
                             Pick, PicksError, ReviewFailure, Window, parse_picks)

lab_tests = lab.LAB / "tests"
from fake_ib import FakeIB  # noqa: E402  (conftest has put the lab's tests on sys.path)
from live.broker import Broker  # noqa: E402
from live.execution import Executor  # noqa: E402
from live.risk import Risk, load_limits  # noqa: E402

DAY = "2026-10-21"  # a Wednesday, New York on summer time: open 13:30 UTC
OPEN = pd.Timestamp("2026-10-21 13:30", tz="UTC")
PLAN = "Buy if the price breaks above the first bar's high on rising volume. Stop: just under the first bar's low. Give up: close if it falls back into the gap."
LIMITS_XYZ = LIMITS.replace("  SPY:", "  XYZ: {max_shares: 10, max_position_value: 8000}\n  ABC: {max_shares: 10, max_position_value: 8000}\n  SPY:")


def bar_start(k):
    return OPEN + pd.Timedelta(minutes=5 * k)


def good_buy(**k):
    return buy(**{"stop": 600.0, "target": 612.0, **k})


class Rig:
    """One or two names on one fake IB, one shared open-window journal. Bar `k` of the day starts at 13:30 UTC + 5k minutes."""

    def __init__(self, tmp_path, *, limits=LIMITS_XYZ, symbols=("XYZ",), answers=None, k=8, settle_min=0.0, age_min=12.0,
                 dry_run=False):
        self.tmp = tmp_path
        self.bars = make_bars()
        self.ib = FakeIB()
        self.ib.connect("127.0.0.1", 4002)
        self.lab_root = tmp_path / "lab"
        self.lab_root.mkdir(parents=True)
        self.risk = Risk(load_limits(limits), root=self.lab_root)
        self.window = Window.for_day(date(2026, 10, 21))
        self.base = OpenJournal(tmp_path / "open")
        self.now = bar_start(k) + pd.Timedelta(minutes=5 + age_min)
        self.settle_min, self.dry_run = settle_min, dry_run
        self.feeds, self.models, self.beats = {}, {}, {}
        for s in symbols:
            self.add(s, answers, k)

    def set_bar(self, k, age_min=12.0):
        for f in self.feeds.values():
            f.shown = 157 + k  # 156 bars of the two earlier days, then bars 0..k of today
        self.now = bar_start(k) + pd.Timedelta(minutes=5 + age_min)
        self.ib.market_price = float(self.bars["close"].iloc[156 + k])

    def add(self, symbol, answers=None, k=8):
        feed = FakeFeed(self.bars, 157 + k)
        self.ib.market_price = float(self.bars["close"].iloc[156 + k])
        broker = Broker(self.ib, f"live:open:{symbol}", dry_run=self.dry_run, risk=self.risk)
        contract = SimpleNamespace(symbol=symbol, conId=1000 + len(self.beats))
        self.feeds[symbol], self.models[symbol] = feed, FakeModel(answers)
        self.beats[symbol] = OpenHeartbeat(
            window=self.window, plan=PLAN, ib=self.ib, contract=contract, feed=feed, model=self.models[symbol],
            executor=Executor(self.ib, broker, contract, timeout_s=2), broker=broker, risk=self.risk,
            journal=self.base.for_symbol(symbol, DAY), state=State.load(self.tmp / "open" / DAY / symbol), symbol=symbol,
            clock=lambda: self.now, mono=lambda: 0.0, settle_min=self.settle_min)
        return self.beats[symbol]

    @property
    def hb(self):
        return next(iter(self.beats.values()))

    def records(self):
        return [json.loads(l) for l in self.base.path.read_text().splitlines()]

    def orders(self, kind=None):
        return [o for _, o in self.ib.placed if kind is None or o.orderType == kind]


@pytest.fixture
def rig(tmp_path):
    made = []

    def build(**k):
        made.append(1)
        return Rig(tmp_path / f"rig{len(made)}", **k)

    return build


# -- the window ---------------------------------------------------------------------------------

def test_window_in_summer_time_is_the_users_utc_times_and_follows_the_open_in_winter_time():
    w = Window.for_day(date(2026, 10, 26))
    assert (w.open, w.entry_cutoff, w.flatten) == tuple(pd.Timestamp(f"2026-10-26 {t}", tz="UTC") for t in ("13:30", "15:00", "15:30"))
    winter = Window.for_day(date(2026, 11, 2))  # New York is back on standard time: the open moves to 14:30 UTC
    assert (winter.open, winter.entry_cutoff, winter.flatten) == tuple(pd.Timestamp(f"2026-11-02 {t}", tz="UTC") for t in ("14:30", "16:00", "16:30"))
    assert Window.for_day(date(2026, 10, 24)) is None  # Saturday


def test_client_id_is_not_one_the_lab_or_the_desk_already_uses():
    assert CLIENT_ID not in {1, 2, 3, 4, 5, 6, 7, 8, 9, 20, 30}


# -- entries only on bars that start before the cutoff -----------------------------------------------

def test_a_buy_before_the_cutoff_goes_through_with_its_own_order_tag(rig):
    r = rig(answers=[good_buy()], k=17)  # the 14:55 bar: the last one that may open a trade
    r.hb.tick()
    rec = r.records()[0]
    assert rec["symbol"] == "XYZ" and rec["result"]["status"] == "bought"
    assert r.orders("STP") and all(o.orderRef.startswith("live:open:XYZ:") for o in r.orders())


def test_a_buy_on_a_bar_that_starts_at_the_cutoff_is_refused_but_the_bar_is_still_decided(rig):
    r = rig(answers=[good_buy()], k=18, age_min=5)  # 15:00 bar
    r.hb.tick()
    rec = r.records()[0]
    assert not rec["verdict"]["allowed"] and rec["verdict"]["seatbelt"] == "entry_window" and not r.orders()
    assert len(r.models["XYZ"].calls) == 1  # Python refuses; the model still sees the bar
    assert r.models["XYZ"].calls[0]["session"]["bar_start"]


def test_no_buy_once_the_flatten_time_has_come(rig):
    r = rig(answers=[good_buy()], k=17)
    r.now = pd.Timestamp("2026-10-21 15:30", tz="UTC")
    r.hb.tick()
    rec = r.records()[0]
    assert not rec["verdict"]["allowed"] and "window ends" in rec["verdict"]["reason"] and not r.orders()


# -- everything flat at the end of the window ----------------------------------------------------------

def test_a_long_is_sold_at_the_flatten_time_without_asking_the_model(rig):
    r = rig(answers=[good_buy(), WAIT], k=8)
    r.hb.tick()
    assert r.ib.holdings["XYZ"] > 0
    asked = len(r.models["XYZ"].calls)
    r.now = pd.Timestamp("2026-10-21 15:29", tz="UTC")
    r.hb.wind_down(r.now)
    assert r.ib.holdings["XYZ"] > 0  # one minute early: nothing happens
    r.now = pd.Timestamp("2026-10-21 15:30", tz="UTC")
    r.hb.wind_down(r.now)
    assert r.ib.holdings["XYZ"] == 0 and len(r.models["XYZ"].calls) == asked
    belt = [x for x in r.records() if x.get("seatbelt") == "flatten_window_end"]
    assert len(belt) == 1 and belt[0]["result"]["status"] == "sold" and belt[0]["symbol"] == "XYZ"
    ended = [x for x in r.records() if "trade_closed" in x]
    assert len(ended) == 1 and ended[0]["trade_closed"]["exit_type"] == "seatbelt" and ended[0]["trade_closed"]["symbol"] == "XYZ"


def test_the_desks_close_minus_ten_backstop_is_still_there(rig):
    r = rig(answers=[good_buy()], k=8)
    r.hb.tick()
    r.hb.window = dataclasses.replace(r.window, flatten=r.window.close)  # the window's own seatbelt out of the way
    r.now = pd.Timestamp("2026-10-21 19:50", tz="UTC")  # 15:50 New York
    r.hb.tick()
    assert r.ib.holdings["XYZ"] == 0


# -- finished bars only ----------------------------------------------------------------------------------

def test_a_bar_is_decided_only_once_it_is_settled(rig):
    r = rig(k=8, settle_min=snapshot.SETTLE_MIN, age_min=10)
    # bar 8 ended 10 minutes ago and bar 7 15: IB is still filling both, so the newest bar decided on is bar 6
    assert [x["bar"] for x in r.hb.tick()] == [bar_start(6).isoformat()]
    r.now += pd.Timedelta(minutes=7)  # bar 8 ended 17 minutes ago
    assert [x["bar"] for x in r.hb.tick()] == [bar_start(7).isoformat(), bar_start(8).isoformat()]


def test_yesterdays_last_bar_is_never_decided_on_and_the_window_so_far_is_not_replayed(rig):
    r = rig(k=-1, settle_min=0.0)  # no bar of today yet: the newest bar is yesterday's last
    r.now = pd.Timestamp("2026-10-21 13:40", tz="UTC")
    assert r.hb.tick() == [] and not r.models["XYZ"].calls
    r.feeds["XYZ"].shown = 157  # bar 0 of today appears
    r.now = pd.Timestamp("2026-10-21 13:51", tz="UTC")
    assert [x["bar"] for x in r.hb.tick()] == [bar_start(0).isoformat()]
    late = rig(k=5)  # started late: bars 0..5 exist, only the newest is decided
    assert [x["bar"] for x in late.hb.tick()] == [bar_start(5).isoformat()] and len(late.models["XYZ"].calls) == 1


def test_the_model_is_not_asked_when_nothing_can_matter(rig):
    r = rig(k=17)
    assert r.hb.wants_bars()
    r.hb.tick()  # the 14:55 bar, the last one that can open a trade
    assert not r.hb.has_entry_bars_left() and not r.hb.wants_bars()  # flat, no entry bar left
    r.ib.holdings["XYZ"] = 3
    assert r.hb.wants_bars()  # something to manage


# -- the lab's risk layer ------------------------------------------------------------------------------------

def test_a_stock_without_limits_in_the_lab_file_cannot_be_bought(rig):
    r = rig(limits=LIMITS, answers=[good_buy()], k=8)  # LIMITS lists SPY only
    r.hb.tick()
    rec = r.records()[0]
    assert rec["result"]["status"] == "refused_by_risk_limits" and not r.orders() and r.ib.holdings.get("XYZ", 0) == 0


def test_the_stop_file_blocks_a_buy(rig):
    r = rig(answers=[good_buy()], k=8)
    (r.lab_root / "STOP").write_text("test")
    r.hb.tick()
    assert r.records()[0]["verdict"]["seatbelt"] == "stop_file" and not r.orders()


def test_a_buy_without_a_stop_is_invalid_and_becomes_wait(rig):
    r = rig(answers=[{**good_buy(), "stop": None}], k=8)
    r.hb.tick()
    assert "invalid" in r.records()[0] and not r.orders()


# -- the review gate, over both names ----------------------------------------------------------------------------

def end_a_trade(r, symbol, key="t1"):
    trade = {"ref": key, "entry_bar": bar_start(2).isoformat(), "entry_seen_at": None, "entry_price": 601.0, "shares": 5, "stop": 600.0,
             "target": 604.0, "size_r": 0.5, "entry_reason": "plan", "lessons": [], "regime": "up",
             "exits": [{"shares": 5, "price": 600.0, "type": "stop", "at": bar_start(4).isoformat()}]}
    r.base.for_symbol(symbol, DAY).append(trades.closed_record(trade, protection_fills=[], now=bar_start(4).isoformat()))


def test_a_finished_trade_in_one_name_holds_back_entries_in_the_other_until_it_is_reviewed(rig):
    r = rig(symbols=("XYZ", "ABC"), answers=[good_buy()], k=8)
    end_a_trade(r, "XYZ")
    r.beats["ABC"].tick()
    rec = [x for x in r.records() if x.get("symbol") == "ABC"][0]
    assert not rec["verdict"]["allowed"] and rec["verdict"]["seatbelt"] == "post_trade_review" and not r.orders()
    assert "post-trade review" in r.models["ABC"].calls[0]["entry_review_gate"]["why_closed"]
    r.base.append({"trade_reviewed": {"key": "t1", "note": "n"}, "at": bar_start(5).isoformat()})
    r.set_bar(9)
    r.beats["ABC"].tick()
    assert r.orders("STP")


# -- one journal, a view per name ---------------------------------------------------------------------------------

def test_each_name_sees_only_its_own_bars_and_snapshots_stay_in_the_open_window_folder(rig):
    r = rig(symbols=("XYZ", "ABC"), k=8)
    r.beats["XYZ"].tick(), r.beats["ABC"].tick()
    assert [x["symbol"] for x in r.records() if x.get("bar")] == ["XYZ", "ABC"]
    assert len(r.base.for_symbol("XYZ", DAY).tail()) == 1 and len(r.base.bar_records()) == 2
    assert (r.tmp / "open" / DAY / "XYZ" / "snapshots").is_dir() and r.base.path == r.tmp / "open" / "journal.jsonl"


# -- the trader's instructions are its own ------------------------------------------------------------------------

def test_the_trader_has_no_tools_no_plugin_and_not_the_spy_constitution():
    m = OpenWindowModel(symbol="XYZ", plan=PLAN, window=Window.for_day(date(2026, 10, 21)))
    s = model.Session("sid", intro="intro")
    cmd = m.command(s)
    assert cmd[cmd.index("--tools") + 1] == "" and "--plugin-dir" not in cmd
    assert cmd[cmd.index("--system-prompt") + 1] == CONSTITUTION.read_text()
    assert model.INSTRUCTIONS.read_text() not in " ".join(cmd) and cmd[cmd.index("--setting-sources") + 1] == ""
    assert s.instructions == openwindow.constitution_hash() and "--session-id" in cmd


def test_the_spy_desks_instruction_hash_does_not_include_the_open_window_files():
    assert CONSTITUTION not in model.instruction_files()
    assert not any(p.is_relative_to(CONSTITUTION.parent) for p in model.instruction_files())
    assert not (model.SKILLS_DIR / "open-window").exists()


def test_every_message_carries_the_plan_and_the_windows_clock():
    w = Window.for_day(date(2026, 10, 21))
    m = OpenWindowModel(symbol="XYZ", plan=PLAN, window=w)

    def snap(start, now):
        return {"session": {"bar_start": start.tz_convert("America/New_York").isoformat(), "now": now.tz_convert("America/New_York").isoformat()}}

    last = m.with_window(snap(bar_start(17), bar_start(20)))["open_window"]
    assert last["bar_may_open_a_trade"] and last["plan"] == PLAN and last["entry_last_bar_start_ny"] == "10:55" and last["flatten_at_ny"] == "11:30"
    assert not m.with_window(snap(bar_start(18), bar_start(21)))["open_window"]["bar_may_open_a_trade"]
    assert not m.with_window(snap(bar_start(17), w.flatten))["open_window"]["bar_may_open_a_trade"]


def test_the_session_intro_holds_the_plan_and_the_window(rig):
    r = rig(k=8)
    s = r.hb._open_session(bar_start(8))
    assert not s.resume and PLAN in s.intro and "15:00 UTC" in s.intro and "15:30 UTC" in s.intro and s.instructions == openwindow.constitution_hash()


# -- the picks in the daily note ----------------------------------------------------------------------------------

NOTE = f"""---
type: daily
---
# 2026-10-21

## Plan
- x

## {openwindow.PICKS_HEADING}
Scan said things.

### AAA (gap up)
Buy if: it holds above the open and volume is rising.
Stop: under the first bar's low.
Give up: if it closes back under yesterday's high.

### BBB
Buy if: it breaks the first bar's high.
Stop: under the first bar's low.
Give up: 11:00.

### CCC
Just watching.

## Trades
- none
"""


def test_picks_are_read_from_the_note_and_a_plan_must_say_when_to_buy_where_the_stop_goes_and_when_to_give_up():
    picks, skipped = parse_picks(NOTE)
    assert [p.symbol for p in picks] == ["AAA", "BBB"] and skipped == ["CCC"] and "Give up" in picks[0].plan
    assert parse_picks("# note\n") == ([], [])


def test_three_picks_are_refused_not_trimmed():
    three = NOTE.replace("### CCC\nJust watching.", "### CCC\nBuy if: x\nStop: y\nGive up: z")
    with pytest.raises(PicksError):
        parse_picks(three)


def test_a_note_with_no_picks_section_means_no_picks(tmp_path):
    (tmp_path / "Daily").mkdir()
    (tmp_path / "Daily" / "2026-10-21.md").write_text("# day\n\n## Plan\n- x\n")
    assert openwindow.load_picks(date(2026, 10, 21), tmp_path) == ([], [])
    assert openwindow.load_picks(date(2026, 10, 22), tmp_path) == ([], [])


# -- the review ---------------------------------------------------------------------------------------------------

def reviewer_run(answers):
    calls = []

    def run(cmd, **kw):
        calls.append((cmd, kw))
        a = answers[min(len(calls), len(answers)) - 1]
        return SimpleNamespace(returncode=0, stdout=json.dumps({"structured_output": a}), stderr="")

    run.calls = calls
    return run


GOOD = {"good_trade": True, "rule_broken": "none", "review": "The stop was hit at 600.0 as planned.", "lesson": "nothing to change"}


def test_a_review_writes_the_note_and_journals_trade_reviewed_last(rig, tmp_path):
    r = rig(k=8)
    end_a_trade(r, "XYZ")
    run = reviewer_run([GOOD])
    rv = OpenReviewer(r.base, vault=tmp_path / "vault", run=run, background=False)
    (tmp_path / "vault").mkdir()
    assert execute.review_block(r.base) is not None
    rv.kick(bar_start(6))
    note = tmp_path / "vault" / "Open window" / "2026-10-21 0940 XYZ.md"
    assert note.exists() and "## Review" in note.read_text() and "stop (a resting order" in note.read_text()
    assert execute.review_block(r.base) is None
    cmd = run.calls[0][0]
    assert cmd[cmd.index("--tools") + 1] == "" and "--plugin-dir" not in cmd


def test_a_review_with_invented_numbers_is_not_written_and_entries_stay_shut_then_it_is_retried(rig, tmp_path):
    r = rig(k=8)
    end_a_trade(r, "XYZ")
    (tmp_path / "vault").mkdir()
    clock = [0.0]
    run = reviewer_run([{**GOOD, "review": "It lost 4.7 dollars."}] * 2 + [GOOD])
    rv = OpenReviewer(r.base, vault=tmp_path / "vault", run=run, background=False, mono=lambda: clock[0])
    rv.kick(bar_start(6))
    assert execute.review_block(r.base) is not None and not list((tmp_path / "vault").rglob("*.md"))
    rv.kick(bar_start(6))
    assert len(run.calls) == 2  # not retried before the wait is over
    clock[0] = openwindow.REVIEW_RETRY_AFTER_S + 1
    rv.kick(bar_start(6))
    assert execute.review_block(r.base) is None


def test_a_failing_claude_call_leaves_the_gate_shut(rig, tmp_path):
    r = rig(k=8)
    end_a_trade(r, "XYZ")
    (tmp_path / "vault").mkdir()

    def run(cmd, **kw):
        return SimpleNamespace(returncode=1, stdout="", stderr="boom")

    OpenReviewer(r.base, vault=tmp_path / "vault", run=run, background=False).kick(bar_start(6))
    assert execute.review_block(r.base) is not None
    with pytest.raises(ReviewFailure):
        OpenReviewer(r.base, vault=tmp_path / "vault", run=run, background=False).review(r.base.unreviewed_trades()[0], bar_start(6))


# -- the runner ------------------------------------------------------------------------------------------------

class Loader:
    def __init__(self, picks):
        self.picks = picks

    def __call__(self):
        if isinstance(self.picks, Exception):
            raise self.picks
        return self.picks, []


def runner(r, picks, reviewer=None):
    rv = reviewer or SimpleNamespace(kick=lambda now: None, join=lambda t=None: None)
    loader = Loader(picks)
    clock = SimpleNamespace(now=r.now)
    made = []

    def make(pick):
        made.append(pick.symbol)
        return r.beats[pick.symbol]

    w = OpenWindow(window=r.window, make_heartbeat=make, load=loader, journal=r.base, reviewer=rv, clock=lambda: r.now)
    w.made, w.loader = made, loader
    return w


def test_nothing_runs_before_the_open_and_no_picks_means_no_bars_are_decided(rig):
    r = rig(k=8)
    w = runner(r, [])
    r.now = pd.Timestamp("2026-10-21 13:00", tz="UTC")
    assert w.step() == "waiting" and not w.made
    r.now = pd.Timestamp("2026-10-21 14:00", tz="UTC")
    assert w.step() == "running" and not w.made and not r.base.path.exists()


def test_the_runner_never_watches_more_than_two_names_and_refuses_a_list_that_breaks_the_rule(rig):
    r = rig(symbols=("XYZ", "ABC", "DEF"), k=8)
    w = runner(r, [Pick("XYZ", PLAN), Pick("ABC", PLAN)])
    r.now = pd.Timestamp("2026-10-21 14:00", tz="UTC")
    w.step()
    assert w.made == ["XYZ", "ABC"]
    w.loader.picks = [Pick("XYZ", PLAN), Pick("ABC", PLAN), Pick("DEF", PLAN)]
    w.step()
    assert w.made == ["XYZ", "ABC"]  # a third name is not started
    w.loader.picks = PicksError("3 picks")
    w.step()
    assert w.made == ["XYZ", "ABC"]


def test_a_pick_added_after_the_open_is_picked_up_while_entries_are_still_possible(rig):
    r = rig(k=8)
    w = runner(r, [])
    r.now = pd.Timestamp("2026-10-21 14:00", tz="UTC")
    w.step()
    w.loader.picks = [Pick("XYZ", PLAN)]
    w.step()
    assert w.made == ["XYZ"] and r.models["XYZ"].calls


def test_at_the_end_of_the_window_the_runner_sells_and_is_done_only_when_flat_and_reviewed(rig, tmp_path):
    r = rig(answers=[good_buy(), WAIT], k=8)
    (tmp_path / "vault").mkdir()
    rv = OpenReviewer(r.base, vault=tmp_path / "vault", run=reviewer_run([GOOD]), background=False)
    w = runner(r, [Pick("XYZ", PLAN)], reviewer=rv)
    assert w.step() == "running" and r.ib.holdings["XYZ"] > 0
    r.now = pd.Timestamp("2026-10-21 15:30", tz="UTC")
    asked = len(r.models["XYZ"].calls)
    first = w.step()  # sells; the trade has just ended, its review is written in the same pass
    assert r.ib.holdings["XYZ"] == 0 and len(r.models["XYZ"].calls) == asked
    assert first in ("winding_down", "done")
    r.now += pd.Timedelta(minutes=1)
    assert w.step() == "done" and execute.review_block(r.base) is None


def test_an_unconfirmed_sale_halts_the_agent(rig):
    r = rig(answers=[good_buy()], k=8)
    r.hb.tick()
    r.ib.freeze = True  # nothing fills any more
    r.now = pd.Timestamp("2026-10-21 15:30", tz="UTC")
    with pytest.raises(Halted):
        for _ in range(6):
            r.hb.wind_down(r.now)


# -- dry run: no order, no shared budget, but the gates and the lab's limit check are journaled -----------------------

def test_a_dry_run_buy_sends_nothing_and_says_what_it_would_have_bought(rig):
    r = rig(answers=[good_buy()], k=8, dry_run=True)
    r.hb.tick()
    res = r.records()[0]["result"]
    assert res["status"] == "dry_run" and res["would_buy"]["shares"] > 0 and res["would_buy"]["stop"] == 600.0
    assert not r.ib.placed and not r.ib.holdings and r.risk._entries_today(r.ib) == 0  # the lab's trade budget is untouched
    m = OpenWindowModel(symbol="XYZ", plan=PLAN, window=r.window, dry_run=True)
    session = {"bar_start": bar_start(8).isoformat(), "now": r.now.isoformat()}
    assert m.with_window({"session": session})["open_window"]["dry_run"] is True


def test_a_dry_run_shows_a_stock_missing_from_the_lab_file_as_a_refusal(rig):
    r = rig(limits=LIMITS, answers=[good_buy()], k=8, dry_run=True)  # that file lists SPY only
    r.hb.tick()
    rec = r.records()[0]
    assert rec["result"]["status"] == "refused_by_risk_limits" and rec["result"]["dry_run"] and not r.ib.placed
    assert any(b["name"] == "risk_limits" for b in rec["seatbelts"])


def test_a_dry_run_still_applies_the_window_and_the_review_gate(rig):
    late = rig(answers=[good_buy()], k=18, age_min=5, dry_run=True)
    late.hb.tick()
    assert late.records()[0]["verdict"]["seatbelt"] == "entry_window" and "result" not in late.records()[0]
    r = rig(answers=[good_buy()], k=8, dry_run=True)
    end_a_trade(r, "XYZ")
    r.hb.tick()
    assert r.records()[-1]["verdict"]["seatbelt"] == "post_trade_review"


def test_the_runner_is_a_dry_run_unless_orders_are_asked_for():
    import inspect
    src = inspect.getsource(openwindow.main)
    assert "--send-orders" in src and "dry_run=not args.send_orders" in src and "if args.send_orders else None" in src


def test_the_constitution_tells_the_trader_to_judge_the_plan_and_leave_the_limits_check_to_the_desk():
    text = openwindow.CONSTITUTION.read_text()
    assert "is NOT a reason" in text and "journals a" in text and "cannot be bought at all" not in text
