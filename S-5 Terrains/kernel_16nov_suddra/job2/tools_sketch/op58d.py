"""Ops 5-6 on the drop 2 ground: sites from the job 5 sketch with Kernel's ground check / layout / roads answers (job5/drop2_check)."""
import json, os, sizes, world
_H = os.path.dirname(os.path.abspath(__file__)); _C = os.path.join(_H, "../../job5/drop2_check")
SK = json.load(open(os.path.join(_H, "../../job5/ops5_8_sketch.json")))
LAY = {}
for f in ("layout58_v1.json", "layout58_ops56_v1.json"):
    for sid, v in json.load(open(os.path.join(_C, f))).items(): LAY[sid] = v["members"] if isinstance(v, dict) else v
MOVES = {"5-05": (5729.0, 10092.0)}                                   # ground check f1 (HUMAN)
SWAP = {"6-03": ["CIS Fuel Depot with GPs"]}                          # ground check f2 (HUMAN)
MEMBER_XY = {("6-M2", 1): (11570.0, 11730.0),                         # layout L3 / L3a: the no-fill spot 106 m out
             ("5-M2", 3): (3370.0, 12682.0),                          # ground check f6c: the filled spot (pack v6)
             ("6-06", 0): (13600.0, 12400.0)}                         # ground check f6b: ground request at the point (not the 240 m layout spot)
WATER_BY_DESIGN = ("6-F", "5-13")                                     # ground check f3, f4 (HUMAN): no pad, no road
OFF_NET = ("5-M4", "5-05", "5-04", "6-M3")                            # roads R2 (HUMAN): island sites with no causeway (foot / boat / air)
def build(op):
    R = {s["id"]: s for s in world.objectives()["sites"]}
    sites, points, order = [], {}, []
    for s in SK["sites"]:
        if s["op"] != op or s["id"] in WATER_BY_DESIGN: continue
        sid = s["id"]; comps = SWAP.get(sid, s["comps"]); x0, y0 = MOVES.get(sid, tuple(s["xy"])); lay = LAY.get(sid, [])
        k_out = 0
        for k, c in enumerate(comps):
            try: hx, hy, ev = sizes.size(c)
            except Exception:
                hx = hy = None
            if c.startswith("Royal Tunnel"): hx, hy, ev = 30.0, 30.0, "ASSUMED: 60 x 60 m (Kernel, layout L5a)"
            if hx is None:
                if k == 0: points[sid] = (float(x0), float(y0))       # a comp with no size: its point is a road target (NOT MEASURED pad)
                continue
            mid = sid if k_out == 0 else f"{sid}.{k_out + 1}"; k_out += 1
            m = next((q for q in lay if q.get("member") == k and "x" in q), None)
            xy = MEMBER_XY.get((sid, k)) or ((float(m["x"]), float(m["y"])) if m else (float(x0), float(y0)))
            sites.append((mid, s["name"] + ("" if mid == sid else f" (member {k_out})"), c, hx, hy, ev, xy, 60, False))
            if sid not in OFF_NET: order.append(mid)
        if sid in points and sid not in OFF_NET: order.append(sid)
    return sites, points, order
BOX = (0, 15995, 0, 15995)
ROUTE_MARGIN = 6000
NET_GRADE = 0.13
ASTRIDE_RAMP_PCT = 12.0
