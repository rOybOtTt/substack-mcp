"""Hourly intraday trader: a 20-minute paper-trading window every market hour (forward test).

    python -m tagym.intraday session [--max-seconds 540]   # run / resume this hour's window
    python -m tagym.intraday report                        # rebuild intraday/REPORT.md

Each window (New York time, hours 9..15):
  xx:35, xx:40, xx:45  decide on the last COMPLETED 5-minute bars (same features and rules as
                       tagym.intraday_bt, so live and backtest cannot drift apart);
                       an order fills at the open of the first 1-minute bar after the decision;
  xx:55                every position is closed at the open of the xx:55 1-minute bar (nothing is
                       left open between windows).
Every pre-registered rule is traded, because none passed the backtest: this is a measurement of
forward returns and of execution (decision-to-fill delay, live fill vs the backtest's assumed price),
not a strategy expected to make money. Each trade is one $1,000 unit; cost 2.5 bps per side.
Data: yfinance (free, about a minute behind). Fills are simulated; no broker is used.
"""
from __future__ import annotations

import json
import sys
import time
from pathlib import Path

import numpy as np
import pandas as pd

from .intraday_bt import COST_BPS, RULES, bar_signals, clean, features
from .paper import watchlist

NY = "America/New_York"
ROOT = Path(__file__).resolve().parents[2]
IDIR = ROOT / "intraday"
STATE, TRADES, SESSIONS, LOG, REPORT = (IDIR / n for n in ("state.json", "trades.csv", "sessions.csv",
                                                             "log.csv", "REPORT.md"))
BT = ROOT / "experiments" / "results" / "intraday_backtest.csv"
UNIT = 1000.0
START_EQUITY = 100000.0
DECIDE = (35, 40, 45)
EXIT_MIN = 55
DATA_WAIT_S = 20  # wait this long after a bar closes before reading it


def now_ny():
    return pd.Timestamp.now(tz=NY).tz_localize(None)


def universe():
    return list(watchlist().ticker) + ["SPY", "QQQ"]


def load_state():
    if STATE.exists():
        return json.loads(STATE.read_text())
    return {"equity": START_EQUITY, "session": None, "sessions_done": 0}


def save_state(s):
    IDIR.mkdir(exist_ok=True)
    STATE.write_text(json.dumps(s, indent=1, default=str))


def append(path, rows):
    if rows:
        IDIR.mkdir(exist_ok=True)
        pd.DataFrame(rows).to_csv(path, mode="a", header=not path.exists(), index=False)


def log(sess, what, detail=""):
    append(LOG, [{"time_ny": str(now_ny())[:19], "session": sess["id"] if sess else "-", "event": what, "detail": detail}])


# ------------------------------------------------------------------ data
def _download(tickers, period, interval):
    import yfinance as yf
    for attempt in range(3):
        try:
            raw = yf.download(tickers, period=period, interval=interval, auto_adjust=False, prepost=False,
                              progress=False, group_by="ticker", threads=True)
            if len(raw):
                return raw
        except Exception as e:  # network hiccup: retry
            err = e
        time.sleep(3 * (attempt + 1))
    raise RuntimeError(f"yfinance {interval} download failed")


def bars5(tickers, cutoff):
    """15 days of 5-minute bars, keeping only bars completed by `cutoff` (bar start <= cutoff - 5 min)."""
    raw = _download(tickers, "15d", "5m")
    out = {}
    for t, x in clean_any(raw, tickers).items():
        out[t] = x[x.index <= cutoff - pd.Timedelta(minutes=5)]
    return out


def bars1(tickers):
    raw = _download(tickers, "1d", "1m")
    return clean_any(raw, tickers, end="15:59", min_rows=1)


def clean_any(raw, tickers, end="15:55", min_rows=500):
    out = {}
    for t in tickers:
        try:
            x = raw[t][["Open", "High", "Low", "Close", "Volume"]].dropna() if isinstance(raw.columns, pd.MultiIndex) \
                else raw[["Open", "High", "Low", "Close", "Volume"]].dropna()
        except KeyError:
            continue
        x.columns = list("ohlcv")
        idx = x.index.tz_convert(NY) if x.index.tz is not None else x.index.tz_localize("UTC").tz_convert(NY)
        x.index = idx.tz_localize(None)
        x = x.between_time("09:30", end)
        if len(x) >= min_rows:
            out[t] = x
    return out


# ------------------------------------------------------------------ decisions
def decide(sess, minute, when):
    """Run every rule at decision time hh:minute on completed 5-minute bars; queue orders."""
    h = sess["hour"]
    t = h * 60 + minute
    day = pd.Timestamp(sess["date"])
    cutoff = day + pd.Timedelta(minutes=t)
    tick = universe()
    B = bars5(tick, cutoff)
    if "SPY" not in B:
        log(sess, "NO_DATA", f"decision {minute}: SPY bars missing")
        return None
    F = {s: features(x).set_index(["day", "tod"]) for s, x in B.items()}
    spy = F["SPY"]
    key, pkey = (day, t - 5), (day, t - 10)
    last_bar = max(spy.index)[1] if len(spy) else None
    if key not in spy.index:
        log(sess, "STALE_DATA", f"decision {minute}: SPY bar {t-5} not available yet (last {last_bar})")
        return None
    sb = spy.loc[key]
    taken = set(map(tuple, sess["taken"]))
    orders = []

    def add(rule, sym, side):
        if (rule, sym) in taken:
            return
        taken.add((rule, sym))
        orders.append({"rule": rule, "symbol": sym, "side": int(side), "minute": minute,
                       "decided_at": str(when)[:19], "fill_after": str((when + pd.Timedelta(minutes=1)).floor("min"))[:19]})

    for sym, fi in F.items():
        if key not in fi.index:
            continue
        b = fi.loc[key]
        pb = fi.loc[pkey] if pkey in fi.index else None
        for rule, side in bar_signals(sym, t, b, sb, pb).items():
            add(rule, sym, side)
    if minute == 35:
        add("C0_spy_long", "SPY", 1)
        # R5 cross-sectional momentum and R6 periodicity (same construction as the backtest)
        mom, per = {}, {}
        for sym, fi in F.items():
            if sym in ("SPY", "QQQ") or key not in fi.index:
                continue
            mom[sym] = fi.loc[key].ret_open - sb.ret_open
            o = fi.o.unstack()
            a, z = h * 60 + 35, h * 60 + 55
            if a in o.columns and z in o.columns:
                w = (o[z] / o[a] - 1).drop(day, errors="ignore").dropna().tail(10)
                if len(w) >= 5:
                    per[sym] = w.mean()
        for rule, sc, k in (("R5_xs_momentum", mom, 5), ("R6_periodicity", per, None)):
            sc = pd.Series(sc).dropna().sort_values()
            if len(sc) < 30:
                continue
            n = k or max(1, len(sc) // 5)
            for s_ in sc.index[-n:]:
                add(rule, s_, 1)
            for s_ in sc.index[:n]:
                add(rule, s_, -1)
        if h == 15:
            for sym in ("SPY", "QQQ"):
                fi = F.get(sym)
                if fi is not None and (day, 595) in fi.index:
                    r = fi.loc[(day, 595)].c / fi.loc[(day, 595)].prev_close - 1
                    if np.isfinite(r) and r != 0:
                        add("R4_mkt_momentum", sym, np.sign(r))
    sess["taken"] = [list(x) for x in taken]
    sess["orders"] += orders
    sess["decisions"].append({"minute": minute, "at": str(when)[:19], "signals": len(orders),
                              "spy_last_bar": int(last_bar) if last_bar is not None else None})
    log(sess, "DECIDE", f"{h:02d}:{minute:02d} -> {len(orders)} orders (rules: "
        + ", ".join(f"{r} {sum(1 for o in orders if o['rule'] == r)}" for r in sorted({o['rule'] for o in orders})) + ")")
    return len(orders)


# ------------------------------------------------------------------ fills
def fill_entries(sess, one):
    """Fill queued orders at the open of the first 1-minute bar at/after `fill_after`."""
    keep = []
    for o in sess["orders"]:
        x = one.get(o["symbol"])
        fa = pd.Timestamp(o["fill_after"])
        bar = x[x.index >= fa] if x is not None else None
        if bar is None or bar.empty:
            keep.append(o)
            continue
        day = pd.Timestamp(sess["date"])
        t = day + pd.Timedelta(minutes=sess["hour"] * 60 + o["minute"])
        bt = x[x.index >= t]
        o.update(entry_time=str(bar.index[0])[:19], entry_px=float(bar.o.iloc[0]),
                 bt_entry_px=float(bt.o.iloc[0]) if len(bt) else None)
        sess["positions"].append(o)
    sess["orders"] = keep


def close_all(sess, one, state):
    day = pd.Timestamp(sess["date"])
    t_exit = day + pd.Timedelta(minutes=sess["hour"] * 60 + EXIT_MIN)
    rows = []
    for p in sess["positions"]:
        x = one.get(p["symbol"])
        if x is None or x.empty:
            continue
        at = x[x.index >= t_exit]
        if len(at):
            px, when = float(at.o.iloc[0]), at.index[0]
        else:  # no xx:55 bar yet: last price before it
            px, when = float(x.c.iloc[-1]), x.index[-1]
        g = p["side"] * (px / p["entry_px"] - 1) * 1e4
        bt = p["side"] * (px / p["bt_entry_px"] - 1) * 1e4 if p.get("bt_entry_px") else None
        net = g - 2 * COST_BPS
        rows.append({"session": sess["id"], "date": sess["date"], "hour": sess["hour"], "rule": p["rule"],
                     "symbol": p["symbol"], "side": p["side"], "decided_at": p["decided_at"],
                     "entry_time": p["entry_time"], "entry_px": round(p["entry_px"], 4),
                     "bt_entry_px": round(p["bt_entry_px"], 4) if p.get("bt_entry_px") else None,
                     "exit_time": str(when)[:19], "exit_px": round(px, 4), "gross_bps": round(g, 2),
                     "net_bps": round(net, 2), "bt_gross_bps": round(bt, 2) if bt is not None else None,
                     "shortfall_bps": round(bt - g, 2) if bt is not None else None,
                     "pnl": round(UNIT * net / 1e4, 2)})
    append(TRADES, rows)
    unfilled = len(sess["orders"])
    pnl = sum(r["pnl"] for r in rows)
    state["equity"] = round(state["equity"] + pnl, 2)
    lag = [d.get("lag_s") for d in sess["decisions"] if d.get("lag_s") is not None]
    append(SESSIONS, [{"session": sess["id"], "date": sess["date"], "hour": sess["hour"], "started": sess["started"],
                       "ended": str(now_ny())[:19], "decisions": len(sess["decisions"]), "trades": len(rows),
                       "unfilled": unfilled,
                       "gross_bps": round(float(np.mean([r["gross_bps"] for r in rows])), 2) if rows else None,
                       "net_bps": round(float(np.mean([r["net_bps"] for r in rows])), 2) if rows else None,
                       "pnl": round(pnl, 2), "equity": state["equity"],
                       "first_decision_late_s": sess.get("first_decision_late_s"), "status": "done"}])
    log(sess, "CLOSE", f"{len(rows)} trades closed, {unfilled} unfilled, P&L {pnl:+.2f} (unit ${UNIT:.0f}/trade)")
    return rows


# ------------------------------------------------------------------ session loop
def start_session(state, now):
    h = now.hour
    if now.minute >= 46 or h < 9 or h > 15 or (h == 9 and now.minute < 15):
        return None
    sess = {"id": f"{now.date()} {h:02d}:35", "date": str(now.date()), "hour": h, "started": str(now)[:19],
            "decisions": [], "orders": [], "positions": [], "taken": []}
    state["session"] = sess
    log(sess, "START", f"window {h:02d}:35-{h:02d}:55")
    return sess


def run_session(max_seconds=540):
    state = load_state()
    now = now_ny()
    if now.dayofweek >= 5:
        print("weekend - no session"); return "SESSION DONE"
    sess = state.get("session")
    if sess and sess["date"] != str(now.date()) or sess and now.hour > sess["hour"] and now.minute >= 5:
        if sess.get("positions") or sess.get("orders"):  # an interrupted window: close it with what we have
            close_all(sess, bars1(sorted({p["symbol"] for p in sess["positions"]}) or ["SPY"]), state)
        state["session"] = sess = None
    if sess is None:
        sess = start_session(state, now)
        if sess is None:
            print(f"{str(now)[:16]} NY: outside a trading window (xx:30-xx:46, hours 9-15) - nothing to do")
            save_state(state)
            return "SESSION DONE"
    deadline = time.time() + max_seconds
    day = pd.Timestamp(sess["date"])
    plan = [("decide", m) for m in DECIDE] + [("close", EXIT_MIN)]
    for kind, m in plan:
        if kind == "decide" and any(d["minute"] == m for d in sess["decisions"]):
            continue
        due = day + pd.Timedelta(minutes=sess["hour"] * 60 + m, seconds=DATA_WAIT_S + (60 if kind == "close" else 0))
        wait = (due - now_ny()).total_seconds()
        if wait > 0:
            if time.time() + wait > deadline:  # sleep what this call may, then hand back to the caller
                time.sleep(max(0.0, deadline - time.time() - 5))
                save_state(state)
                print(f"CONTINUE: next step {kind} {sess['hour']:02d}:{m:02d} at {str(due)[11:19]} NY")
                return "CONTINUE"
            time.sleep(wait)
        if kind == "decide":
            late = (now_ny() - (due - pd.Timedelta(seconds=DATA_WAIT_S))).total_seconds()
            if late > 8 * 60:  # this decision point is long gone (the session started late): skip it
                sess["decisions"].append({"minute": m, "at": str(now_ny())[:19], "signals": 0, "skipped": "late"})
                log(sess, "SKIP", f"decision {m}: started {late:.0f}s late")
                save_state(state)
                continue
            if sess.get("first_decision_late_s") is None:
                sess["first_decision_late_s"] = round(late, 1)
            n = decide(sess, m, now_ny())
            if n is None:  # the bar was not published yet: one retry 30 s later
                time.sleep(30)
                n = decide(sess, m, now_ny())
            if n is None:
                sess["decisions"].append({"minute": m, "at": str(now_ny())[:19], "signals": 0, "skipped": "no data"})
            sess["decisions"][-1]["lag_s"] = round(late, 1)
            syms = sorted({o["symbol"] for o in sess["orders"]})
            if syms:
                time.sleep(max(0, 65 - (now_ny().second)))  # let the fill minute print
                fill_entries(sess, bars1(syms))
            save_state(state)
        else:
            syms = sorted({p["symbol"] for p in sess["positions"]} | {o["symbol"] for o in sess["orders"]})
            one = bars1(syms) if syms else {}
            fill_entries(sess, one)
            rows = close_all(sess, one, state)
            state["sessions_done"] = state.get("sessions_done", 0) + 1
            state["session"] = None
            save_state(state)
            report()
            net = np.mean([r["net_bps"] for r in rows]) if rows else float("nan")
            print(f"SESSION DONE {sess['id']}: {len(rows)} trades, mean net {net:+.2f} bps, "
                  f"P&L {sum(r['pnl'] for r in rows):+.2f}, equity {state['equity']:,.2f}")
            return "SESSION DONE"
    save_state(state)
    return "SESSION DONE"


# ------------------------------------------------------------------ report
def report():
    tr = pd.read_csv(TRADES) if TRADES.exists() else pd.DataFrame()
    se = pd.read_csv(SESSIONS) if SESSIONS.exists() else pd.DataFrame()
    bt = pd.read_csv(BT).set_index("rule") if BT.exists() else pd.DataFrame()
    st = load_state()
    L = ["# Intraday forward test: 20-minute windows every market hour", "",
         "Every pre-registered rule from `tagym/intraday_bt.py` is traded on paper in each window (xx:35-xx:55 New York),",
         "one $1,000 unit per trade, 2.5 bps cost per side, flat at xx:55. None of the rules passed the 60-day backtest,",
         "so this measures forward returns and execution; it is not expected to make money.", ""]
    if len(se):
        L += [f"Sessions: {len(se)} ({se.date.min()} → {se.date.max()}), trades: {len(tr)}, "
              f"P&L {se.pnl.sum():+,.2f} on $1,000 units, equity {st['equity']:,.2f}.", ""]
        L += ["| Session | Trades | Unfilled | Mean gross (bps) | Mean net (bps) | P&L | Started late (s) |", "|---|---|---|---|---|---|---|"]
        for r in se.itertuples():
            L.append(f"| {r.session} | {r.trades} | {r.unfilled} | {r.gross_bps} | {r.net_bps} | {r.pnl:+.2f} | {r.first_decision_late_s} |")
        L.append("")
    if len(tr):
        L += ["## By rule: forward vs backtest", "",
              "| Rule | Trades | Fwd gross | Fwd net | Hit rate | Backtest gross | Backtest net | Shortfall vs backtest price |",
              "|---|---|---|---|---|---|---|---|"]
        for rule, g in tr.groupby("rule"):
            b = bt.loc[rule] if rule in bt.index else None
            L.append(f"| {rule} | {len(g)} | {g.gross_bps.mean():+.2f} | {g.net_bps.mean():+.2f} | {(g.net_bps > 0).mean():.0%} | "
                     f"{'' if b is None else f'{b.gross_bps:+.2f}'} | {'' if b is None else f'{b.net_bps:+.2f}'} | "
                     f"{g.shortfall_bps.mean():+.2f} |")
        L += ["", "Shortfall = return at the backtest's assumed entry (the 5-minute bar's open) minus the return at the live fill "
              "(the next 1-minute bar after the decision). Positive = the live delay cost money.", ""]
    L += ["## Rules", ""] + [f"- **{k}**: {v}" for k, v in RULES.items()]
    IDIR.mkdir(exist_ok=True)
    REPORT.write_text("\n".join(L) + "\n")


if __name__ == "__main__":
    a = sys.argv[1:]
    if not a or a[0] == "session":
        ms = int(a[a.index("--max-seconds") + 1]) if "--max-seconds" in a else 540
        print(run_session(ms))
    elif a[0] == "report":
        report()
