"""Op 5 Esker Road on the drop 2 ground (planner run asked by Kernel, 26 Nov)."""
from op58d import *          # noqa: F401,F403
import op58d, math
NAME = "Esker Road (drop 2)"
SITES, POINT_TARGETS, _ORD = op58d.build(5)
_start = (5200.0, 7800.0)
_ORD.sort(key=lambda k: math.dist(_start, dict((s[0], s[6]) for s in SITES).get(k, POINT_TARGETS.get(k, _start))))
_ORD.remove("5-M1")
TRUNKS = [[dict(stop=("xyz", _start), name="op 5 start", label="op 5 start (job 5 sketch)"), dict(stop=("site", "5-M1"), through=False, kind="dirt", width=7.0, grade=0.14)]]
NETS = {"op 5": _ORD}
ROOT = {"op 5": "TRUNK"}
APPROACHES = {f'{s["id"]} {s["name"]}': [f'{a["way"]} ({a["bearing"]} deg)' for a in s.get("approaches", [])] for s in op58d.SK["sites"] if s["op"] == 5 and s["role"] in ("FINAL", "main")}

# planner v1 answers (HUMAN): P3 the tunnel holdout is a foot link from the Turbolaser Tower; P4 / P5 the 5-02 and 5-12 roads route at 14 % per step
_ORD.remove("5-M2"); NETS = {"op 5": _ORD}
SITE_GRADE = {"5-02": 0.14, "5-12": 0.14}
# planner v2 (AI, carrying out P2 / P4 / P5): 5-02 and 5-M2.5 face water on their nearest edges, so they try every edge;
# 5-12's kept road (roads R5) winds about 47.6 km, so its search margin covers the whole map
ALL_EDGES = ("5-02", "5-M2.5", "5-12")
SITE_MARGIN = {"5-12": 16000}
