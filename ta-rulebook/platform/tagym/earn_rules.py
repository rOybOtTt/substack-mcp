"""Post-earnings drift (PEAD) rules, evaluated with the standard event study."""
import numpy as np

from .earnings import load_events, event_panel

RULES = {
    # name: (direction, horizon, row filter on the events table)
    "earn_all": (1, 60, lambda d: np.ones(len(d), bool)),
    "earn_gap_up_vol": (1, 60, lambda d: (d.ear_exc >= 0.05) & (d.vol_ratio >= 2)),
    "earn_gap_down_vol": (-1, 60, lambda d: (d.ear_exc <= -0.05) & (d.vol_ratio >= 2)),
    "earn_surprise_pos10": (1, 60, lambda d: d.surprise >= 10),
    "earn_surprise_neg10": (-1, 60, lambda d: d.surprise <= -10),
    "earn_agree_pos": (1, 60, lambda d: (d.surprise >= 5) & (d.ear_exc >= 0.03)),
    "earn_agree_neg": (-1, 60, lambda d: (d.surprise <= -5) & (d.ear_exc <= -0.03)),
    "earn_ear_top_decile": (1, 60, lambda d: d.ear_exc >= d.ear_exc.quantile(0.9)),
    "earn_ear_bottom_decile": (-1, 60, lambda d: d.ear_exc <= d.ear_exc.quantile(0.1)),
}


def events(ctx, name):
    d = load_events(ctx)
    return event_panel(ctx, np.asarray(RULES[name][2](d), bool))
