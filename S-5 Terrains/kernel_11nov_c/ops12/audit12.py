"""Audit of the BUILT ops 1 and 2 (your pads_op1 / pads_op2 and roads_ops_1_2.json) on the build-4 ground, by the 12 Nov method.
Your road file has no levels: ops 1-2 are cut into the build-4 grid, so a road's level is the grid under its centreline (bilinear).
Usage: python3 audit12.py <out dir>"""
import sys, os, json, math, collections
import numpy as np
from matplotlib.path import Path
from shapely.geometry import Polygon, LineString, Point
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "../job1/tools"))
import world

OUT = sys.argv[1]; os.makedirs(OUT, exist_ok=True)
H = world.H(); PK = world.PACK
OBJ = {s["id"]: s for s in world.objectives()["sites"]}
ROADS = json.load(open(os.path.join(PK, "ground", "roads_ops_1_2.json")))


def rect(cx, cy, hx, hy, yaw, grow=0.0):
    a = math.radians(yaw); ex = np.array([math.cos(a), -math.sin(a)]); ey = np.array([math.sin(a), math.cos(a)])
    c = np.array([cx, cy]); hx, hy = hx + grow, hy + grow
    return np.array([c - hx * ex - hy * ey, c + hx * ex - hy * ey, c + hx * ex + hy * ey, c - hx * ex + hy * ey])


def grid_in(poly):
    c = np.array(poly)
    I, J = np.meshgrid(np.arange(int(c[:, 0].min() // 5) - 1, int(c[:, 0].max() // 5) + 2), np.arange(int(c[:, 1].min() // 5) - 1, int(c[:, 1].max() // 5) + 2))
    m = Path(c).contains_points(np.c_[I.ravel() * 5.0, J.ravel() * 5.0], radius=1e-6)
    return J.ravel()[m], I.ravel()[m]


def pads_of(op):
    out = []
    for p in json.load(open(os.path.join(PK, "ops_1_2", f"pads_op{op}.json")))["pads"]:
        hx = p.get("hx") or p.get("hu"); hy = p.get("hy") or (p.get("hv") / 2 if p.get("hv") else None)
        out.append(dict(p, hx=hx, hy=hy, yaw=p.get("yaw", 0.0), profile=p.get("kind") == "pass profile"))
    return out


def grades(X, Z):
    sg = np.hypot(*np.diff(X, axis=0).T); s = np.r_[0, np.cumsum(sg)]
    res = dict(point_to_point=float((np.abs(np.diff(Z)) / np.maximum(sg, 1e-9)).max() * 100) if len(sg) else 0.0)
    for b in (10.0, 20.0):
        w = 0.0; where = None
        for i in range(len(s)):
            j = np.searchsorted(s, s[i] + b)
            if j < len(s):
                g = abs(Z[j] - Z[i]) / (s[j] - s[i])
                if g > w: w, where = g, (round(float(X[i, 0]), 1), round(float(X[i, 1]), 1))
        res[f"over_{int(b)}_m"] = w * 100; res[f"over_{int(b)}_m_at"] = where
    over = 0.0                                     # length of road over 14 % on a 20 m base
    for i in range(len(s)):
        j = np.searchsorted(s, s[i] + 20.0)
        if j < len(s) and abs(Z[j] - Z[i]) / (s[j] - s[i]) > 0.1405: over += sg[i] if i < len(sg) else 0
    res["length_over_14_pct_m"] = over; res["length_m"] = float(s[-1]) if len(s) else 0.0; res["spacing_min_m"] = float(sg.min()) if len(sg) else 0.0
    return res


def straight(X, tol=1.0):
    best = 0.0; i = 0
    for j in range(2, len(X)):
        a, b = X[i], X[j]; ab = b - a; L = np.hypot(*ab)
        if L < 1e-6: continue
        q = X[i + 1:j] - a; d = np.abs(ab[0] * q[:, 1] - ab[1] * q[:, 0]) / L
        if (d > tol).any(): i = j - 1
        else: best = max(best, L)
    return best


report = {}
for op in (1, 2):
    pads = pads_of(op); R = {}
    src = f"(ao{op})"
    roads = [r for r in ROADS if src in r.get("src", "")]
    # ---- pads: the built level against the grid under footprint + 1.5 m (ops 1-2 are cut in: this is the flatness of what was built)
    P = []
    for p in pads:
        J, I = grid_in(rect(p["x"], p["y"], p["hx"], p["hy"], p["yaw"], 1.5))
        dev = np.abs(H[J, I] - p["z"])
        P.append(dict(site=p["site"], comp=p["comp"], x=p["x"], y=p["y"], z=p["z"], hx=p["hx"], hy=p["hy"], yaw=p["yaw"], points=int(len(J)),
                      max_off_level_m=round(float(dev.max()), 2), points_off_over_0_5_m=int((dev > 0.5).sum()), profile=p["profile"]))
    polys = {p["site"]: Polygon(rect(p["x"], p["y"], p["hx"], p["hy"], p["yaw"])) for p in pads}
    lv = {p["site"]: p["z"] for p in pads}
    spacing = sorted((round(polys[a].distance(polys[b]), 1), a, b, round(abs(lv[a] - lv[b]), 2)) for i, a in enumerate(polys) for b in list(polys)[i + 1:])
    water = []
    for p in pads:
        c = rect(p["x"], p["y"], p["hx"], p["hy"], p["yaw"]); J, I = grid_in(rect(p["x"], p["y"], p["hx"] + 10, p["hy"] + 10, p["yaw"]))
        water.append((int((H[J, I] <= 0.3).sum()), p["site"]))
    # ---- roads
    RD = []
    for r in roads:
        X = np.array(r["points"], float); Z = np.array([world.z(x, y) for x, y in X])
        g = grades(X, Z); w = 10.0 if r["kind"] == "main" else 7.0; lim = 10.0 if r["kind"] == "main" else 14.0
        RD.append(dict(link=r["link"], kind=r["kind"], width_m=w, limit_pct=lim, points=len(X), **{k: (round(v, 1) if isinstance(v, float) else v) for k, v in g.items()},
                       straight_max_m=round(straight(X), 1), over_limit=bool(max(g["point_to_point"], g["over_10_m"], g["over_20_m"]) > lim + 0.05)))
    # road edge to pads not served (the road's own pads: its last 25 m may meet them)
    clr = []
    for r in roads:
        X = np.array(r["points"], float); w = 10.0 if r["kind"] == "main" else 7.0
        ln = LineString(X).buffer(w / 2) if len(X) > 1 else None
        if ln is None: continue
        ends = set(r["link"].replace("-through", "").split("-")[0:1])
        for sid, pol in polys.items():
            served = sid in r["link"]
            if served:
                keep = [k for k in range(len(X)) if pol.distance(Point(X[k])) > 25.0 + w / 2]
                if len(keep) < 2: continue
                d = pol.distance(LineString(X[keep[0]:keep[-1] + 1]).buffer(w / 2))
            else: d = pol.distance(ln)
            if d < 3.0: clr.append((round(d, 1), sid, r["link"], "served" if served else ""))
    clr.sort()
    # ---- connectivity of the road net (pieces whose points come within 12 m are joined), against the sites with a vehicle approach
    from scipy.spatial import cKDTree
    par = list(range(len(roads)))
    def f(a):
        while par[a] != a: a = par[a]
        return a
    trees = [cKDTree(np.array(r["points"], float)) for r in roads]
    for i in range(len(roads)):
        for j in range(i + 1, len(roads)):
            if trees[i].sparse_distance_matrix(trees[j], 12.0).nnz: par[f(i)] = f(j)
    comp_of_site = {}
    for p in pads:
        pol = polys[p["site"]]
        for i, r in enumerate(roads):
            if pol.distance(LineString(np.array(r["points"], float)).buffer(5)) < 15.0: comp_of_site.setdefault(p["site"], set()).add(f(i))
    nets = collections.Counter(f(i) for i in range(len(roads)))
    sites_op = [s for s in OBJ.values() if s["op"] == op]
    veh = [s["id"] for s in sites_op if "vehicles" in open(os.path.join(PK, "design", "PURPOSE_MAP.md")).read().split(f"| {s['id']} |")[1].split("\n")[0]] if sites_op else []
    off = [v for v in veh if not any(k.startswith(v) for k in comp_of_site)]
    mains = [p for p in pads if OBJ.get(p["site"], {}).get("role") in ("FINAL", "MAIN")]
    mm = sorted((round(math.dist((a["x"], a["y"]), (b["x"], b["y"]))), a["site"], b["site"]) for i, a in enumerate(mains) for b in mains[i + 1:])
    report[f"op{op}"] = dict(
        pads=dict(count=len(pads), off_level=[p for p in sorted(P, key=lambda q: -q["max_off_level_m"]) if p["max_off_level_m"] > 0.5][:10],
                  closest_pairs=spacing[:6], pairs_breaking_rule_1_or_4=[s for s in spacing if s[0] < 12.0 or (s[3] > 0.01 and s[0] < 17.0)],
                  near_water=[w_ for w_ in sorted(water, reverse=True) if w_[0] > 0][:8]),
        roads=dict(count=len(roads), over_limit=sum(r["over_limit"] for r in RD), length_km=round(sum(r["length_m"] for r in RD) / 1000, 2),
                   length_over_14_pct_km=round(sum(r["length_over_14_pct_m"] for r in RD) / 1000, 2),
                   worst=sorted(RD, key=lambda r: -max(r["point_to_point"], r["over_10_m"]))[:8], straight_over_150=[r for r in RD if r["straight_max_m"] > 150],
                   all=RD),
        clearance_under_3_m=clr[:20], road_pieces=len(roads), road_groups=len(nets), group_sizes=sorted(nets.values(), reverse=True),
        vehicle_sites_without_a_road_within_15_m=off, mains_closest=mm[:4])
json.dump(report, open(os.path.join(OUT, "audit_ops_1_2.json"), "w"), indent=1, default=str)
for k, v in report.items():
    print(k, "pads", v["pads"]["count"], "| off level >0.5:", [(p["site"], p["max_off_level_m"]) for p in v["pads"]["off_level"]][:6])
    print("   pad pairs breaking 12 m / 17 m:", v["pads"]["pairs_breaking_rule_1_or_4"][:6], "| near water:", v["pads"]["near_water"][:4])
    print("   roads", v["roads"]["count"], v["roads"]["length_km"], "km | over limit", v["roads"]["over_limit"], "| km over 14 %", v["roads"]["length_over_14_pct_km"],
          "| straights > 150:", [(r["link"], r["straight_max_m"]) for r in v["roads"]["straight_over_150"]])
    print("   worst:", [(r["link"], r["kind"], r["point_to_point"], r["over_10_m"], r["over_20_m"]) for r in v["roads"]["worst"][:5]])
    print("   clearance < 3 m:", v["clearance_under_3_m"][:6])
    print("   road groups", v["road_groups"], v["group_sizes"][:6], "| vehicle sites with no road:", v["vehicle_sites_without_a_road_within_15_m"], "| mains:", v["mains_closest"])
