"""Op 3 drop 2, second pass: op3r plus Kernel's re-run v1 decisions 3-4 (300 m pad search for the no-pad sites)."""
from op3r import *          # noqa: F401,F403
import op3r
WIDE = {"3-03", "3-04.2", "3-10.2", "3-10.3"}     # re-run v1 decisions 3-4 (HUMAN): search out to 300 m (rad 125 x 2.4)
SITES = [(sid, n, c, hx, hy, ev, xy, 125 if sid in WIDE else rad, wm) for sid, n, c, hx, hy, ev, xy, rad, wm in op3r.SITES]

# re-run v2 decision 1 (HUMAN): pin 3-M1.2 at its v2 seat on the trunk, and ramp the flattened stretch out at <= 12 % (ASSUMED, under the 14 % rule)
SITES = [(sid, n, c, hx, hy, ev, (13838.1, 5447.2) if sid == "3-M1.2" else xy, rad, wm) for sid, n, c, hx, hy, ev, xy, rad, wm in SITES]
ASTRIDE_ROAD = dict(getattr(op3r, "ASTRIDE_ROAD", {}), **{"3-M1.2": "trunk"})
ASTRIDE_RAMP_PCT = 12.0
