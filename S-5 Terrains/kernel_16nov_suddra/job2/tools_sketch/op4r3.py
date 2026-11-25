"""Op 4 drop 2, fifth pass: op4r2 with re-run v4 decision 1 (HUMAN): the three north checkpoints pinned at their fourth-pass seats (pack v5 fills there)."""
from op4r2 import *          # noqa: F401,F403
import op4r2
PIN = {"4-M2": (8400.9, 7841.5), "4-M2.3": (8176.6, 7325.9), "4-06": (7250.3, 7766.1)}
SITES = [(sid, n, c, hx, hy, ev, PIN.get(sid, xy), rad, wm) for sid, n, c, hx, hy, ev, xy, rad, wm in op4r2.SITES]
ASTRIDE_ROAD = dict(op4r2.ASTRIDE_ROAD, **{"4-M2": "rail bridge N", "4-M2.3": "rail bridge N", "4-06": "4-02.2"})
