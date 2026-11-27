"""Op 3 drop 2, approaches A5 pass (HUMAN): op3r5, with a ramp piece where the 1-F -> 3-M1 trunk leaves the 1-F FOB point (the leg may step up to 0.4 m there),
and 3-M1.2 held to that trunk (its pin at (13874, 5552) is kept)."""
from op3r5 import *          # noqa: F401,F403
import op3r5
TRUNKS = [[dict(l) for l in ch] for ch in op3r5.TRUNKS]
for ch in TRUNKS:
    if ch[-1]["stop"] == ("site", "3-M1"): ch[-1]["jmax"] = 0.4
ASTRIDE_ROAD = dict(op3r5.ASTRIDE_ROAD, **{"3-M1.2": "trunk-101:"})
