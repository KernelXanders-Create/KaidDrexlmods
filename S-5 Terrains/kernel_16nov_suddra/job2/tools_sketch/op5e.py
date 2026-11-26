"""Op 5 on the drop 2 ground, fourth pass, part 1: every op 5 site except 5-12 (planner v3 answer: split off 5-12, HUMAN)."""
from op5d import *          # noqa: F401,F403
import op5d
SITES = [s for s in op5d.SITES if s[0] != "5-12"]
NETS = {"op 5": [x for x in op5d.NETS["op 5"] if x != "5-12"]}
ALL_EDGES = ("5-02", "5-M2.5")
SITE_MARGIN = {}
