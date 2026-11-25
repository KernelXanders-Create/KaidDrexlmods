"""Op 3 on the drop 2 real ground: sketch v3 seats with Kernel's ground-check v1 answers (moves, swaps, ground requests ASSUMED built)."""
from op3s import *          # noqa: F401,F403  (TRUNKS, NETS, ASTRIDE, NET_GRADE, SITE_KW, APPROACHES ...)
import op3s, json, os, sizes
NAME = "The Peat-Gas Fields (drop 2)"
_P = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "../part2_sketch/op3_plan_sketch_v3.json")))
_POS = {}
for s_ in _P["sites"]:
    for k_, m_ in enumerate(s_["members"]):
        _POS[s_["id"] if k_ == 0 else f"{s_['id']}.{k_ + 1}"] = (m_["x"], m_["y"])
MOVES = {     # ground check v1 (HUMAN)
 "3-14": (15775.0, 4832.0), "3-14.2": (15705.0, 4832.0),      # f1: the whole site 788 m S (members keep their 70 m offset)
 "3-F.2": (13058.0, 2568.0),                                  # f3: swapped for the CIS Fuel Depot with GPs
 "3-M2.2": (11456.0, 3182.0), "3-M2.4": (11840.0, 3498.0),    # f6
 "3-13": (14404.0, 3496.0),                                   # f8
 "3-09": (15584.0, 6780.0),                                   # f12
}
SWAP = {"3-F.2": "CIS Fuel Depot with GPs"}
_out = []
for t in op3s.SITES:
    sid, name, comp, hx, hy, ev, xy, rad, wm = t
    if sid in SWAP:
        comp = SWAP[sid]; hx, hy, ev = sizes.size(comp)
    xy = MOVES.get(sid, _POS.get(sid, xy))
    _out.append((sid, name, comp, hx, hy, ev, xy, 60, wm))
SITES = _out
