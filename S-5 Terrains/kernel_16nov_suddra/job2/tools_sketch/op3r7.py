"""Op 3 drop 2, approaches A6 pass (HUMAN): op3r6 on pack v9, with 3-M2.3 pinned at its A5 seat (11461, 3440) on the 3-M2 trunk, where the causeway is widened."""
from op3r6 import *          # noqa: F401,F403
import op3r6
SITES = [(sid, n, c, hx, hy, ev, (11461.4, 3440.0) if sid == "3-M2.3" else xy, rad, wm) for sid, n, c, hx, hy, ev, xy, rad, wm in op3r6.SITES]
ASTRIDE_ROAD = dict(op3r6.ASTRIDE_ROAD, **{"3-M2.3": "trunk-1:"})
