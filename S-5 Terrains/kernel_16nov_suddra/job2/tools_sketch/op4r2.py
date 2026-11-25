"""Op 4 drop 2, second pass: op4r plus Kernel's re-run v1 decisions 3-5."""
from op4r import *          # noqa: F401,F403
import op4r, op4s
WIDE = {"4-F", "4-M1.5", "4-02.2", "4-07"}       # decisions 3-4 (HUMAN): search out to 300 m (rad 125 x 2.4)
FIX = {"4-M2": (8522.9, 7779.1)}                  # decision 5 (HUMAN): keep the north seat on the rail bridge N road
SITES = [(sid, n, c, hx, hy, ev, FIX.get(sid, xy), 125 if sid in WIDE else rad, wm) for sid, n, c, hx, hy, ev, xy, rad, wm in op4r.SITES]
ASTRIDE_ROAD = dict(getattr(op4s, "ASTRIDE_ROAD", {}), **{"4-M2": "rail bridge N"})
