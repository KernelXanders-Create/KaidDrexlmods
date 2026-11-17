"""Decision 43: re-seat every checkpoint astride a road of its net. Each checkpoint pad is centred on the nearest road point where it fits
(pad change <= 4 m over footprint + 1.5 m; 17 m from other pads' footprints; off the +0.3 m line by 15 m on the grid; other roads' bands 3 m clear),
its local y axis (the passage, ASSUMED) along the road, its level the road's level there; the road points inside the footprint take the pad level.
A spur that only served the checkpoint is removed. Usage: python3 reseat.py <opN_plan.json> (rewritten) -> prints the moves."""
import sys, json, math
import numpy as np
from shapely.geometry import Polygon, LineString, Point
from scipy import ndimage
import world
from planner import rect

p = sys.argv[1]; D = json.load(open(p)); H = world.H(); C = 5.0
water = ndimage.binary_dilation(H <= 0.3, iterations=3)
def change(x, y, hx, hy, yaw, z):
    c = rect(x, y, hx, hy, yaw, 1.5); pol = Polygon(c)
    I, J = np.meshgrid(np.arange(int(c[:, 0].min() // C), int(c[:, 0].max() // C) + 2), np.arange(int(c[:, 1].min() // C), int(c[:, 1].max() // C) + 2))
    m = np.array([pol.contains(Point(a * C, b * C)) for a, b in zip(I.ravel(), J.ravel())])
    jj, ii = J.ravel()[m], I.ravel()[m]
    return float(np.abs(H[jj, ii] - z).max()), bool(water[jj, ii].any())
moves = []
cps = [s for s in D["sites"] if "Checkpoint" in s["comp"]]
for s in cps:
    sid = s["id"]
    spurs = [r for r in D["roads"] if sid in r["links"]]
    others_end_on = lambda r: any(r2 is not r and min(math.dist(r2["points"][e], q) for q in r["points"]) < 6 for r2 in D["roads"] for e in (0, -1))
    cand = [r for r in D["roads"] if r not in spurs or others_end_on(r)]
    best = None
    for r in cand:
        X = np.array(r["points"]); Z = np.array(r["points_z"]); n = len(X)
        for i in range(3, n - 3):
            t = X[min(i + 2, n - 1)] - X[max(i - 2, 0)]; yaw = math.degrees(math.atan2(t[0], t[1])) % 180
            d0 = math.dist((s["x"], s["y"]), X[i])
            if best and d0 >= best[0]: continue
            x, y, z = float(X[i, 0]), float(X[i, 1]), float(Z[i])
            pol = Polygon(rect(x, y, s["hx"], s["hy"], yaw))
            if any(pol.distance(Polygon(rect(o["x"], o["y"], o["hx"], o["hy"], o["yaw"]))) < 17.0 for o in D["sites"] if o["id"] != sid): continue
            # the road must run along the passage through the whole footprint (within 2 m of the axis)
            ax = LineString([(x - (s["hy"] + 1) * math.sin(math.radians(yaw)), y - (s["hy"] + 1) * math.cos(math.radians(yaw))), (x + (s["hy"] + 1) * math.sin(math.radians(yaw)), y + (s["hy"] + 1) * math.cos(math.radians(yaw)))])
            inside = [k for k in range(n) if pol.buffer(1.5).contains(Point(X[k]))]
            if not inside or max(ax.distance(Point(X[k])) for k in inside) > 2.0: continue
            if any(pol.buffer(3.0 + 3.5).intersects(LineString(r2["points"])) for r2 in D["roads"] if r2 is not r and r2 not in spurs): continue
            ch, wet = change(x, y, s["hx"], s["hy"], yaw, z)
            if ch > 4.0 or wet: continue
            best = (d0, r["id"], x, y, yaw, z, ch, inside)
    if not best: moves.append(dict(id=sid, status="NO SEAT FOUND on its net")); continue
    d0, rid, x, y, yaw, z, ch, inside = best
    r = next(r for r in D["roads"] if r["id"] == rid)
    for k in inside: r["points_z"][k] = round(z, 3)
    removed = [sp["id"] for sp in spurs if not others_end_on(sp) and sp["id"] != rid]
    D["roads"] = [rr for rr in D["roads"] if rr["id"] not in removed]
    moves.append(dict(id=sid, comp=s["comp"], from_xy=[s["x"], s["y"]], to_xy=[round(x, 1), round(y, 1)], moved_m=round(d0), on_road=rid, yaw=round(yaw), z=round(z, 2), pad_change_m=round(ch, 2), spurs_removed=removed))
    s.update(x=round(x, 1), y=round(y, 1), yaw=round(yaw), z=round(z, 3), max_change_m=round(ch, 2), astride=dict(road=rid, offset_m="<= 2 (MEASURED)", angle_deg=0, passage_axis="local y (ASSUMED)"), reseated_m=round(d0))
D["reseat_moves"] = moves
json.dump(D, open(p, "w"), indent=1)
for m in moves: print(m)
