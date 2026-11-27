"""Op 6 The Cauldron on the drop 2 ground. The op 6 start is boat / air (roads R3, HUMAN), so the net grows from 6-M1 (AI: the central main on the redrawn net)."""
from op58d import *          # noqa: F401,F403
import op58d, math
NAME = "The Cauldron (drop 2)"
SITES, POINT_TARGETS, _ORD = op58d.build(6)
_r = dict((s[0], s[6]) for s in SITES)["6-M1"]
_ORD.remove("6-M1"); _ORD.sort(key=lambda k: math.dist(_r, dict((s[0], s[6]) for s in SITES).get(k, POINT_TARGETS.get(k, _r))))
NETS = {"op 6": _ORD}
ROOT = {"op 6": "6-M1"}
APPROACHES = {f'{s["id"]} {s["name"]}': [f'{a["way"]} ({a["bearing"]} deg)' for a in s.get("approaches", [])] for s in op58d.SK["sites"] if s["op"] == 6 and s["role"] in ("FINAL", "main")}
import approaches56_v2; APPROACHES = approaches56_v2.for_op(6)     # reviewed list v2 (HUMAN) replaces the sketch's AI drafts

# planner P7 (HUMAN): 6-03 joins over a built ramp piece; the join may step up to 0.7 m there (ramp spec: rise 0.67 m MEASURED, 4.8 m at 14 %, 7 m deck)
SITE_JMAX = {"6-03": 0.7}
