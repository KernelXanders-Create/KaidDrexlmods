"""R and S16 rows of the Suddra RETURN_FORMAT, measured the owner's way on the cut grid (K3 sketch ground until drop 2).
Cut grid: pads cut first (every 5 m point inside footprint + 1.5 m takes the pad level); then every point within half the road width + 3.5 m of any
centre line takes the level of the nearest centre-line point (all roads together). Grades are read along each centre line every 1 m, bilinear on that grid.
Usage: python3 cutgrid_check.py <opN_plan.json (planner)> <out.json>"""
import sys, json, math
import numpy as np
from scipy.spatial import cKDTree
from matplotlib.path import Path
import world
from planner import rect

D = json.load(open(sys.argv[1])); H0 = world.H(); G = H0.copy(); C = 5.0
pads = D["sites"] + D.get("squad_positions", [])
xs = [p["x"] for p in pads] + [x for r in D["roads"] for x, y in r["points"]]; ys = [p["y"] for p in pads] + [y for r in D["roads"] for x, y in r["points"]]
i0, i1 = int(min(xs) // C) - 60, int(max(xs) // C) + 60; j0, j1 = int(min(ys) // C) - 60, int(max(ys) // C) + 60
I, J = np.meshgrid(np.arange(i0, i1 + 1), np.arange(j0, j1 + 1)); PX = np.c_[I.ravel() * C, J.ravel() * C]
for p in pads:
    m = Path(rect(p["x"], p["y"], p["hx"], p["hy"], p["yaw"], 1.5)).contains_points(PX, radius=1e-6)
    G[J.ravel()[m], I.ravel()[m]] = p["z"]
# dense centre-line points with their level (0.5 m)
cl, cz, rid = [], [], []
for k, r in enumerate(D["roads"]):
    X = np.array(r["points"], float); Z = np.array(r["points_z"], float); s = np.r_[0, np.cumsum(np.hypot(*np.diff(X, axis=0).T))]
    ss = np.arange(0, s[-1] + 1e-9, 0.5); cl.append(np.c_[np.interp(ss, s, X[:, 0]), np.interp(ss, s, X[:, 1])]); cz.append(np.interp(ss, s, Z)); rid += [k] * len(ss)
cl = np.vstack(cl); cz = np.concatenate(cz); rid = np.array(rid); T = cKDTree(cl)
d, idx = T.query(PX, distance_upper_bound=3.5 + 3.5)
m = np.isfinite(d); G[J.ravel()[m], I.ravel()[m]] = cz[idx[m]]
def bil(x, y):
    c, r = x / C, y / C; c0, r0 = int(math.floor(c)), int(math.floor(r)); fc, fr = c - c0, r - r0
    return G[r0, c0] * (1 - fc) * (1 - fr) + G[r0, c0 + 1] * fc * (1 - fr) + G[r0 + 1, c0] * (1 - fc) * fr + G[r0 + 1, c0 + 1] * fc * fr
out = dict(R1=[], R2=[], R3=[], R4=[], R5=[], R6=[], R7=[])
for k, r in enumerate(D["roads"]):
    X = np.array(r["points"], float); s = np.r_[0, np.cumsum(np.hypot(*np.diff(X, axis=0).T))]; L = s[-1]
    ss = np.arange(0, L + 1e-9, 1.0); P = np.c_[np.interp(ss, s, X[:, 0]), np.interp(ss, s, X[:, 1])]; Z = np.array([bil(x, y) for x, y in P])
    # R1: circle through the points 10 m before and after, every 1 m
    rad = []
    for i in range(10, len(P) - 10):
        A, B, Cc = P[i - 10], P[i], P[i + 10]; cr = abs((B[0] - A[0]) * (Cc[1] - A[1]) - (B[1] - A[1]) * (Cc[0] - A[0]))
        if cr > 1e-9: rad.append((math.dist(A, B) * math.dist(B, Cc) * math.dist(Cc, A) / (2 * cr), i))
    tight = min(rad) if rad else (1e9, 0); out["R1"].append([r["id"], round(tight[0], 1), int(sum(1 for a, _ in rad if a < 12.0))])
    g1 = float(np.max(np.abs(np.diff(Z)))) * 100 if len(Z) > 1 else 0
    g10 = float(np.max(np.abs(Z[10:] - Z[:-10])) / 10 * 100) if len(Z) > 10 else 0
    g20 = float(np.max(np.abs(Z[20:] - Z[:-20])) / 20 * 100) if len(Z) > 20 else 0
    out["R2"].append([r["id"], round(g1, 2)]); out["R3"].append([r["id"], round(g10, 2)]); out["R4"].append([r["id"], round(g20, 2)])
    # R5: stacked legs of the same road
    Zc = np.interp(ss, s, np.array(r["points_z"]))
    TT = cKDTree(P); worst = None
    for a, b in TT.query_pairs(7.0 + 14.0):
        if abs(ss[a] - ss[b]) > 40 and abs(Zc[a] - Zc[b]) > 0.05:
            e = math.dist(P[a], P[b]) - 7.0
            if worst is None or e < worst[0]: worst = (round(e, 1), round(abs(Zc[a] - Zc[b]), 2))
    if worst: out["R5"].append([r["id"]] + list(worst))
    # R7: longest straight (within 1 m of the chord) and largest cut / fill against the natural ground
    best = 0.0; i = 0
    for j in range(2, len(X)):
        A, B = X[i], X[j]; ab = B - A; Lb = np.hypot(*ab)
        q = X[i + 1:j] - A; dd = np.abs(ab[0] * q[:, 1] - ab[1] * q[:, 0]) / max(Lb, 1e-9)
        if (dd > 1.0).any(): i = j - 1
        else: best = max(best, Lb)
    cf = max(abs(z - world.z(x, y)) for (x, y), z in zip(r["points"], r["points_z"]))
    out["R7"].append([r["id"], round(best), round(cf, 2)])
# R6: every road end that meets another road: the parent road's points within 10 m either side of the join are level within 0.05 m
for k, r in enumerate(D["roads"]):
    for e in (0, -1):
        p = np.array(r["points"][e]); dd, ii = T.query(p, k=60)
        for d_, i_ in zip(dd, ii):
            if not np.isfinite(d_) or d_ > 6.0 or rid[i_] == k: continue
            par = rid[i_]; near = np.where((rid == par) & (np.hypot(*(cl - cl[i_]).T) <= 10.0))[0]
            span = float(cz[near].max() - cz[near].min())
            out["R6"].append([r["id"], D["roads"][par]["id"], round(span, 3), "level" if span <= 0.05 else "NOT LEVEL"]); break
S = dict(method=__doc__.split("\n")[1:4],
         R1=dict(limit="0 places under 12 m", places_under_12=sum(x[2] for x in out["R1"]), tightest=min(out["R1"], key=lambda x: x[1])),
         R2=dict(limit="dirt 14 %", worst=max(out["R2"], key=lambda x: x[1]), over=[x for x in out["R2"] if x[1] > 14.0]),
         R3=dict(limit="dirt 14 % over every 10 m", worst=max(out["R3"], key=lambda x: x[1]), over=[x for x in out["R3"] if x[1] > 14.0]),
         R4=dict(limit="dirt 14 % over every 20 m", worst=max(out["R4"], key=lambda x: x[1]), over=[x for x in out["R4"] if x[1] > 14.0]),
         R5=dict(limit="0 stacked-leg pairs", pairs=out["R5"]),
         R6=dict(limit="every junction on a level landing of 20 m or more", joins=len(out["R6"]), not_level=[x for x in out["R6"] if x[3] != "level"]),
         R7=dict(limit="straight <= 150 m; cut / fill <= 4 m", longest_straight=max(out["R7"], key=lambda x: x[1]), largest_cut_fill=max(out["R7"], key=lambda x: x[2])))
json.dump(S, open(sys.argv[2], "w"), indent=1)
print(json.dumps({k: v for k, v in S.items() if k != "method"}, indent=None)[:2500])
