"""5-13 Stake Hamlet: dry rises (ground >= +0.5 m, the village form rule) within 1.2 km of its sketch point (1600, 9000), on the given pack.
Lists each rise's area, level range, nearest point to the sketch point, and how far its edge is from the op 5 roads. Reach 1.2 km is ASSUMED."""
import sys, json, math, numpy as np
from scipy import ndimage as nd
from scipy.spatial import cKDTree
PK, PLAN, OUT = sys.argv[1:4]
H = np.load(PK + "/ground/height_whole_cm.npz")["height_cm"] / 100.0; C = 5.0; P0 = (1600.0, 9000.0); R = 1200.0
i0, i1, j0, j1 = int((P0[1] - R) / C), int((P0[1] + R) / C), int((P0[0] - R) / C), int((P0[0] + R) / C)
sub = H[i0:i1, j0:j1]; yy, xx = np.mgrid[i0:i1, j0:j1] * C
dry = sub >= 0.5; lab, n = nd.label(dry)
RD = json.load(open(PLAN))["roads"]; ALLP = np.vstack([np.array(r["points"], float) for r in RD]); ROAD_IDS = sum([[r["id"]] * len(r["points"]) for r in RD], []); TREE = cKDTree(ALLP)
rows = []
for k in range(1, n + 1):
    m = lab == k; a = m.sum() * C * C / 1e4
    if a < 1.0: continue
    X, Y = xx[m], yy[m]; d = np.hypot(X - P0[0], Y - P0[1]); i = d.argmin()
    pts = np.c_[X, Y]
    rd = float(TREE.query(pts)[0].min()); rr = ROAD_IDS[int(TREE.query(pts)[1][TREE.query(pts)[0].argmin()])]
    rows.append(dict(area_ha=round(float(a), 1), level=[round(float(sub[m].min()), 2), round(float(sub[m].max()), 2)], nearest_xy=[float(X[i]), float(Y[i])], nearest_m=round(float(d[i])),
                     centre_xy=[round(float(X.mean())), round(float(Y.mean()))], bearing_from_point=round(math.degrees(math.atan2(X.mean() - P0[0], Y.mean() - P0[1])) % 360), road_m=round(rd), nearest_road=rr))
rows.sort(key=lambda r: r["nearest_m"])
g = H[int(P0[1] / C), int(P0[0] / C)]
out = dict(point=P0, ground_at_point=round(float(g), 2), dry_within_100m_pct=None, rises=rows)
m100 = np.hypot(xx - P0[0], yy - P0[1]) <= 100; out["dry_within_100m_pct"] = round(float(dry[m100].mean() * 100))
json.dump(out, open(OUT, "w"), indent=1)
print(out["ground_at_point"], out["dry_within_100m_pct"]); [print(r) for r in rows[:12]]
