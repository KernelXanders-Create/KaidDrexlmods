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
