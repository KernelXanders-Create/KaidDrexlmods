"""Op 5 on the drop 2 ground, fourth pass, part 2: 5-12 alone, joined to the part 1 net (planner v3 answer: split off 5-12, HUMAN)."""
from op58d import *          # noqa: F401,F403
import op5d
NAME = "Esker Road 5-12 (drop 2)"
SITES = [s for s in op5d.SITES if s[0] == "5-12"]
POINT_TARGETS = {}
TRUNKS = []
EXTERNAL_PLANS = ["../../job5/drop2_check/planner_ops56_v4/op5_main/op5_plan.json"]
NETS = {"5-12": ["5-12"]}
ROOT = {"5-12": "EXTERNAL_ROADS"}
APPROACHES = {}
SITE_GRADE = {"5-12": 0.14}
ALL_EDGES = ("5-12",)
SITE_MARGIN = {"5-12": 16000}
SITE_JMAX = {"5-12": 0.6}          # planner v3 P9 (HUMAN): ramp piece at the 5-12 junction
# planner v3 P12 (HUMAN): narrow the search to the best junctions of the last run, with a 6 km margin
JOIN_ONLY = ("op5:5-03-5-F.3", "op5:5-F.3-5-M1.2", "5-F (op 5)")
SITE_MARGIN = {"5-12": 6000}
SITE_MARGIN = {"5-12": 16000}      # planner v3 P13 (HUMAN): back to the 16 km margin, joins still narrowed
