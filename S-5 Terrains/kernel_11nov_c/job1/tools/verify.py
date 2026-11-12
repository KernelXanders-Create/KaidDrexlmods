"""Independent check of an op plan, measured the way the owner measures (12 Nov sheet), not with the planner's own code.
- pads: every 5 m grid point inside footprint + 1.5 m (polygon test, yaw clockwise from north) -> max |ground - pad level|
- roads: grade between every pair of handed-over points, and over every 10 m and 20 m stretch along them
- roads: straight runs (points within 1 m of the chord), road edge to every pad not served by the road
Usage: python3 verify.py <opN_plan.json>"""
import sys, json, math
import numpy as np
from matplotlib.path import Path
from shapely.geometry import Polygon, LineString, Point
import world

H = world.H()


def rect(cx, cy, hx, hy, yaw, grow=0.0):
    a = math.radians(yaw); ex = np.array([math.cos(a), -math.sin(a)]); ey = np.array([math.sin(a), math.cos(a)])
    c = np.array([cx, cy]); hx, hy = hx + grow, hy + grow
    return np.array([c - hx * ex - hy * ey, c + hx * ex - hy * ey, c + hx * ex + hy * ey, c - hx * ex + hy * ey])


def pad_change(s):
    c = rect(s["x"], s["y"], s["hx"], s["hy"], s["yaw"], 1.5)
    I, J = np.meshgrid(np.arange(int(c[:, 0].min() // 5) - 1, int(c[:, 0].max() // 5) + 2), np.arange(int(c[:, 1].min() // 5) - 1, int(c[:, 1].max() // 5) + 2))
    m = Path(c).contains_points(np.c_[I.ravel() * 5.0, J.ravel() * 5.0], radius=1e-6)
    h = H[J.ravel()[m], I.ravel()[m]]
    return int(m.sum()), float(np.abs(h - s["z"]).max())


def grades(r):
    X = np.array(r["points"]); Z = np.array(r["points_z"]); sg = np.hypot(*np.diff(X, axis=0).T); s = np.r_[0, np.cumsum(sg)]
    out = {"point_to_point": float((np.abs(np.diff(Z)) / np.maximum(sg, 1e-9)).max() * 100)}
    for b in (10.0, 20.0):
        w = 0.0
        for i in range(len(s)):
            j = np.searchsorted(s, s[i] + b)
            if j < len(s): w = max(w, abs(Z[j] - Z[i]) / (s[j] - s[i]))
        out[f"over_{int(b)}_m"] = w * 100
    return out


def straight(r, tol=1.0):
    X = np.array(r["points"]); best = 0.0; i = 0
    for j in range(2, len(X)):
        a, b = X[i], X[j]; ab = b - a; L = np.hypot(*ab)
        if L < 1e-6: continue
        q = X[i + 1:j] - a; d = np.abs(ab[0] * q[:, 1] - ab[1] * q[:, 0]) / L
        if (d > tol).any(): i = j - 1
        else: best = max(best, L)
    return best


if __name__ == "__main__":
    D = json.load(open(sys.argv[1]))
    pads = D["sites"] + D["squad_positions"]
    print("pads (footprint + 1.5 m, polygon test):")
    worst = sorted(((pad_change(s)[1], s["id"], pad_change(s)[0], s["max_change_m"]) for s in pads), reverse=True)
    for w, sid, n, own in worst[:6]: print(f"  {sid}: {w:.2f} m over {n} points (plan says {own})")
    print("  FAIL" if worst[0][0] > 4.0 else "  all <= 4.0 m")
    print("roads:")
    over = 0
    for r in D["roads"]:
        g = grades(r); st = straight(r)
        bad = max(g.values()) > 14.05
        over += bad
        print(f"  {r['id']}: point {g['point_to_point']:.1f} %, 10 m {g['over_10_m']:.1f} %, 20 m {g['over_20_m']:.1f} %, straight {st:.0f} m{'  OVER 14 %' if bad else ''}")
    print(f"  {over} of {len(D['roads'])} roads over 14 %")
    polys = {s["id"]: Polygon(rect(s["x"], s["y"], s["hx"], s["hy"], s["yaw"])) for s in pads}
    near = []
    for r in D["roads"]:
        X = np.array(r["points"])
        for sid, pol in polys.items():
            if sid in r["links"]:
                keep = [k for k in range(len(X)) if pol.distance(Point(X[k])) > 25.0 + r["width_m"] / 2]
                if len(keep) < 2: continue
                ln = LineString(X[keep[0]:keep[-1] + 1]).buffer(r["width_m"] / 2)
            else: ln = LineString(X).buffer(r["width_m"] / 2)
            near.append((pol.distance(ln), sid, r["id"]))
    near.sort()
    print("road edge to pads, closest:", [(round(a, 1), b, c) for a, b, c in near[:3]])
