"""Chart-pattern detectors built on a causal ZigZag.

ZigZag: a swing extreme is CONFIRMED only once price has reversed from it by
`thr` (adaptive: max(min_pct, k*ATR%)). Patterns are evaluated on confirmed
pivots; the trade trigger is the first close beyond the pattern's trigger
level AFTER the last pivot is confirmed, so nothing uses future data.

Pattern definitions follow Edwards & Magee / Bulkowski / O'Neil / Minervini
in spirit; exact numeric tolerances are documented per pattern.
"""
from __future__ import annotations

import numpy as np
import pandas as pd


def zigzag(h, l, c, thr):
    """Returns list of pivots (piv_idx, conf_idx, price, kind) kind=+1 high, -1 low."""
    n = len(c)
    piv = []
    if n < 3:
        return piv
    trend = 0
    ext_i, ext_p = 0, c[0]
    i0 = 0
    while i0 < n and not np.isfinite(c[i0]):
        i0 += 1
    if i0 >= n:
        return piv
    hi_i, hi_p, lo_i, lo_p = i0, h[i0], i0, l[i0]
    for i in range(i0 + 1, n):
        hi, lo, t = h[i], l[i], thr[i]
        if not (np.isfinite(hi) and np.isfinite(lo) and np.isfinite(t)):
            continue
        if trend >= 0:
            if hi >= hi_p:
                hi_i, hi_p = i, hi
            if trend == 0 and lo <= lo_p:
                lo_i, lo_p = i, lo
            if lo <= hi_p * (1 - t) and (trend == 1 or hi_i > lo_i):
                piv.append((hi_i, i, hi_p, 1))
                trend = -1
                lo_i, lo_p = i, lo
                continue
            if trend == 0 and hi >= lo_p * (1 + t) and lo_i < hi_i:
                piv.append((lo_i, i, lo_p, -1))
                trend = 1
                hi_i, hi_p = i, hi
                continue
        if trend == -1:
            if lo <= lo_p:
                lo_i, lo_p = i, lo
            if hi >= lo_p * (1 + t):
                piv.append((lo_i, i, lo_p, -1))
                trend = 1
                hi_i, hi_p = i, hi
    return piv


def _trigger_up(c, start, level, max_bars, invalid_below=None, l=None):
    """First index >= start where close > level, within max_bars; abort if low < invalid_below."""
    end = min(len(c), start + max_bars)
    for j in range(start, end):
        if invalid_below is not None and l[j] < invalid_below:
            return -1
        if c[j] > level:
            return j
    return -1


def _trigger_dn(c, start, level, max_bars, invalid_above=None, h=None):
    end = min(len(c), start + max_bars)
    for j in range(start, end):
        if invalid_above is not None and h[j] > invalid_above:
            return -1
        if c[j] < level:
            return j
    return -1


def detect_all(panel, atr_pct: pd.DataFrame, volr: pd.DataFrame, k_atr=2.5, min_pct=0.04):
    o, h, l, c = (panel[k] for k in ["Open", "High", "Low", "Close"])
    cols = c.columns
    names = ["pat_double_bottom", "pat_double_top", "pat_inv_head_shoulders", "pat_head_shoulders",
             "pat_bull_flag", "pat_asc_triangle", "pat_cup_handle", "pat_vcp", "pat_desc_triangle"]
    out = {n: np.zeros(c.shape, bool) for n in names}
    H, L, C = h.values, l.values, c.values
    THR = np.maximum(min_pct, k_atr * atr_pct.values)
    VR = volr.values
    for k in range(len(cols)):
        hk, lk, ck, tk = H[:, k], L[:, k], C[:, k], THR[:, k]
        piv = zigzag(hk, lk, ck, tk)
        for m in range(2, len(piv)):
            p2, p1, p0 = piv[m - 2], piv[m - 1], piv[m]  # p0 most recent
            conf = p0[1]
            # ---- double bottom: L1 H L2 ; |L2/L1-1|<=3%, H >= 1.10*min(L), 10..120 bars apart
            if p0[3] == -1 and p1[3] == 1 and p2[3] == -1:
                L1, Hm, L2 = p2[2], p1[2], p0[2]
                gap = p0[0] - p2[0]
                if abs(L2 / L1 - 1) <= 0.03 and Hm >= 1.10 * min(L1, L2) and 10 <= gap <= 120:
                    j = _trigger_up(ck, conf, Hm, 60, invalid_below=min(L1, L2) * 0.97, l=lk)
                    if j > 0:
                        out["pat_double_bottom"][j, k] = True
            # ---- double top: H1 L H2 ; signal close below L
            if p0[3] == 1 and p1[3] == -1 and p2[3] == 1:
                H1, Lm, H2 = p2[2], p1[2], p0[2]
                gap = p0[0] - p2[0]
                if abs(H2 / H1 - 1) <= 0.03 and Lm <= 0.90 * max(H1, H2) and 10 <= gap <= 120:
                    j = _trigger_dn(ck, conf, Lm, 60, invalid_above=max(H1, H2) * 1.03, h=hk)
                    if j > 0:
                        out["pat_double_top"][j, k] = True
            if m >= 4:
                q4, q3, q2, q1, q0 = piv[m - 4], piv[m - 3], piv[m - 2], piv[m - 1], piv[m]
                # ---- inverse H&S: LS(L) H1 HEAD(L) H2 RS(L)
                if q0[3] == -1 and q2[3] == -1 and q4[3] == -1:
                    LS, H1, HD, H2, RS = q4[2], q3[2], q2[2], q1[2], q0[2]
                    if HD < 0.97 * min(LS, RS) and abs(RS / LS - 1) <= 0.07 and abs(H2 / H1 - 1) <= 0.07 \
                            and (q0[0] - q4[0]) <= 200:
                        neck = max(H1, H2)
                        j = _trigger_up(ck, q0[1], neck, 60, invalid_below=HD, l=lk)
                        if j > 0:
                            out["pat_inv_head_shoulders"][j, k] = True
                # ---- H&S top: LS(H) L1 HEAD(H) L2 RS(H)
                if q0[3] == 1 and q2[3] == 1 and q4[3] == 1:
                    LS, L1, HD, L2, RS = q4[2], q3[2], q2[2], q1[2], q0[2]
                    if HD > 1.03 * max(LS, RS) and abs(RS / LS - 1) <= 0.07 and abs(L2 / L1 - 1) <= 0.07 \
                            and (q0[0] - q4[0]) <= 200:
                        neck = min(L1, L2)
                        j = _trigger_dn(ck, q0[1], neck, 60, invalid_above=HD, h=hk)
                        if j > 0:
                            out["pat_head_shoulders"][j, k] = True
                # ---- ascending triangle: H L H L with flat tops (within 2%) and rising lows (+3%)
                if q0[3] == -1 and q1[3] == 1 and q2[3] == -1 and q3[3] == 1:
                    Ha, La, Hb, Lb = q3[2], q2[2], q1[2], q0[2]
                    if abs(Hb / Ha - 1) <= 0.02 and Lb >= 1.03 * La and (q0[0] - q3[0]) <= 150:
                        j = _trigger_up(ck, q0[1], max(Ha, Hb), 40, invalid_below=La, l=lk)
                        if j > 0:
                            out["pat_asc_triangle"][j, k] = True
                # ---- descending triangle: L H L H flat bottoms, falling highs -> breakdown
                if q0[3] == 1 and q1[3] == -1 and q2[3] == 1 and q3[3] == -1:
                    La, Ha, Lb, Hb = q3[2], q2[2], q1[2], q0[2]
                    if abs(Lb / La - 1) <= 0.02 and Hb <= 0.97 * Ha and (q0[0] - q3[0]) <= 150:
                        j = _trigger_dn(ck, q0[1], min(La, Lb), 40, invalid_above=Ha, h=hk)
                        if j > 0:
                            out["pat_desc_triangle"][j, k] = True
            # ---- bull flag: pole L->H >= 20% in <= 15 bars, pullback L2 retraces <= 50%, break above H
            if p0[3] == -1 and p1[3] == 1 and p2[3] == -1:
                Lp, Hp, Lf = p2[2], p1[2], p0[2]
                if Hp / Lp - 1 >= 0.20 and (p1[0] - p2[0]) <= 15 and (Hp - Lf) <= 0.5 * (Hp - Lp) \
                        and (p0[0] - p1[0]) <= 25:
                    j = _trigger_up(ck, conf, Hp, 25, invalid_below=Lf, l=lk)
                    if j > 0:
                        out["pat_bull_flag"][j, k] = True
            # ---- cup with handle: H1 (lip) -> L cup (12-35% deep) -> H2 (within 5% below/2% above H1)
            #      35..325 bars, then handle low L3 (<=12% below H2, upper half of cup), break H2 on vol>=1.4x
            if m >= 3 and p0[3] == -1 and p1[3] == 1 and p2[3] == -1 and piv[m - 3][3] == 1:
                H1, Lc, H2, L3 = piv[m - 3][2], p2[2], p1[2], p0[2]
                depth = 1 - Lc / H1
                dur = p1[0] - piv[m - 3][0]
                if 0.12 <= depth <= 0.35 and 35 <= dur <= 325 and 0.95 * H1 <= H2 <= 1.02 * H1 \
                        and L3 >= 0.88 * H2 and L3 >= (Lc + H2) / 2 and (p0[0] - p1[0]) <= 40:
                    end = min(len(ck), conf + 30)
                    for j in range(conf, end):
                        if lk[j] < L3:
                            break
                        if ck[j] > H2 and VR[j, k] >= 1.4:
                            out["pat_cup_handle"][j, k] = True
                            break
            # ---- VCP: >=3 successive pullbacks (H->L) with shrinking depth, last depth <= 10%
            if m >= 5 and p0[3] == -1:
                depths = []
                ok = True
                for s in range(3):
                    hi_p = piv[m - 1 - 2 * s]
                    lo_p = piv[m - 2 * s]
                    if hi_p[3] != 1 or lo_p[3] != -1:
                        ok = False; break
                    depths.append(1 - lo_p[2] / hi_p[2])
                if ok and depths[0] < depths[1] < depths[2] and depths[0] <= 0.10 and depths[2] <= 0.35:
                    pivot_hi = piv[m - 1][2]
                    end = min(len(ck), conf + 30)
                    for j in range(conf, end):
                        if lk[j] < p0[2]:
                            break
                        if ck[j] > pivot_hi and VR[j, k] >= 1.5:
                            out["pat_vcp"][j, k] = True
                            break
    return {n: pd.DataFrame(v, index=c.index, columns=cols) for n, v in out.items()}
