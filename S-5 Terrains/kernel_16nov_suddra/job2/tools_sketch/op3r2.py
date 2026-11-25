"""Op 3 drop 2, second pass: op3r plus Kernel's re-run v1 decisions 3-4 (300 m pad search for the no-pad sites)."""
from op3r import *          # noqa: F401,F403
import op3r
WIDE = {"3-03", "3-04.2", "3-10.2", "3-10.3"}     # re-run v1 decisions 3-4 (HUMAN): search out to 300 m (rad 125 x 2.4)
SITES = [(sid, n, c, hx, hy, ev, xy, 125 if sid in WIDE else rad, wm) for sid, n, c, hx, hy, ev, xy, rad, wm in op3r.SITES]
