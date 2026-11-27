"""Ops 7-8 hand-off: where the final op 5 and op 6 roads come near ops 7-8, and how far the op 6 net is from the op 7 start.
Footprints: ops 7-8 layout members (layout58_ops78_v1.json); sites with no layout use their sketch point. Road band = 3.5 m half width + 3.5 m (the planner's band)."""
import json, math, numpy as np
K = json.load(open("../ops5_8_sketch.json")); sites = {s["id"]: s for s in K["sites"]}
LAY = json.load(open("layout58_ops78_v1.json"))
PLANS = {5: "planner_ops56_v4/op5_main/op5_plan.json", 6: "approaches36/run_a4/op6/op6_plan.json"}
MOVED = {"8-12": (8400, 15500)}          # pack 5: the Escape Pad's north spot
def rect_d(px, py, m):                   # distance from points to a member's rectangle (0 inside)
    w, h = m["size"]; t = math.radians(m.get("yaw", 0)); dx, dy = px - m["x"], py - m["y"]
    u = dx * math.cos(t) - dy * math.sin(t); v = dx * math.sin(t) + dy * math.cos(t)
    return np.hypot(np.maximum(abs(u) - w / 2, 0), np.maximum(abs(v) - h / 2, 0))
foot = []                                # (site, label, fn)
for sid, s in sites.items():
    if s["op"] not in (7, 8): continue
    xy = MOVED.get(sid, s["xy"])
    mem = [m for m in LAY.get(sid, {}).get("members", []) if "size" in m and m.get("x") is not None]
    if mem:
        for m in mem: foot.append((sid, m["comp"], lambda X, Y, m=m: rect_d(X, Y, m)))
    else: foot.append((sid, "sketch point", lambda X, Y, xy=xy: np.hypot(X - xy[0], Y - xy[1])))
out = dict(roads_near=[], start=None)
for op, f in PLANS.items():
    for r in json.load(open(f))["roads"]:
        P = np.array(r["points"], float); Z = np.array(r["points_z"], float)
        for sid, lab, fn in foot:
            d = fn(P[:, 0], P[:, 1]); i = int(d.argmin()); edge = float(d[i]) - 7.0
            lim = 300 if lab == "sketch point" else 150
            if float(d[i]) <= lim:
                out["roads_near"].append(dict(op=op, road=r["id"], site=sid, site_name=sites[sid]["name"], member=lab, closest_xy=[round(P[i, 0]), round(P[i, 1])], road_level_m=round(float(Z[i]), 2),
                                              centre_dist_m=round(float(d[i]), 1), band_edge_dist_m=round(edge, 1)))
st = K["ops"][2]["start"]; best = None
for op, f in PLANS.items():
    for r in json.load(open(f))["roads"]:
        P = np.array(r["points"], float); d = np.hypot(P[:, 0] - st[0], P[:, 1] - st[1]); i = int(d.argmin())
        if best is None or d[i] < best["dist_m"]: best = dict(op=op, road=r["id"], xy=[round(P[i, 0]), round(P[i, 1])], level_m=round(float(r["points_z"][i]), 2), dist_m=round(float(d[i])))
out["start"] = dict(op7_start=st, nearest_road=best)
json.dump(out, open("handoff78/handoff78_v1.json", "w"), indent=1)
for x in sorted(out["roads_near"], key=lambda x: x["band_edge_dist_m"]): print(x)
print(out["start"])
