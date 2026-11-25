"""Op 4 on the drop 2 real ground: sketch v3 seats with Kernel's ground-check v1 answers (moves, ground requests ASSUMED built)."""
from op4s import *          # noqa: F401,F403
import op4s, json, os
NAME = "The Drain (drop 2)"
_P = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "../part2_sketch/op4_plan_sketch_v3.json")))
_POS = {}
for s_ in _P["sites"]:
    ms = [m_ for m_ in s_["members"] if isinstance(m_.get("pad"), dict)]
    for k_, m_ in enumerate(ms):
        _POS[s_["id"] if k_ == 0 else f"{s_['id']}.{k_ + 1}"] = (m_["x"], m_["y"])
# 4-M2 members are listed as separate ids in op4s (4-M2, 4-M2.2, 4-M2.3): same order as the plan
MOVES = {
 "4-M1.3": (4800.0, 7672.0), "4-M1.5": (5338.0, 7884.0),      # f5
 "4-02.2": (6594.0, 8442.0),                                  # f9
 "4-10": (12564.0, 8155.0),                                   # f11
 "4-04.2": (9664.0, 5904.0),                                  # f15
}
SITES = [(sid, name, comp, hx, hy, ev, MOVES.get(sid, _POS.get(sid, xy)), 60, wm) for sid, name, comp, hx, hy, ev, xy, rad, wm in op4s.SITES]

# ground check v1 finding 16 (HUMAN): roads on dry ground only; dry roads wind far round the water, so search the whole map
BOX = (0, 15995, 0, 15995)
ROUTE_MARGIN = 6000
