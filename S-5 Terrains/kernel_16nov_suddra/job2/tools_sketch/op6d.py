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
