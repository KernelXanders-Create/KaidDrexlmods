"""Op 3 drop 2, fourth pass: op3r2 with re-run v2 decision 3 (HUMAN): 3-M1.2 pinned at its third-pass seat, shore fill there (pack v4)."""
from op3r2 import *          # noqa: F401,F403
import op3r2
SITES = [(sid, n, c, hx, hy, ev, (13874.0, 5552.2) if sid == "3-M1.2" else xy, rad, wm) for sid, n, c, hx, hy, ev, xy, rad, wm in op3r2.SITES]
