"""Ways in for the op 5 sites off the road net (P10: 5-02, 5-M2.5; P17: 5-12; and the 5-13 hamlet, H3).
Foot, two ways: players walk any cell that is not deep (depth_band 2) or boat (3) water; AI walks only ai_dry cells (the drop 2 AI network mask).
Each is the shortest walk from the site's pad edge to within 10 m of an op 5 road. Grid 8 m (every second 4 m mask cell), moves to 8 neighbours.
Boat: the nearest boat-network cell (boat_core) to the site, and how far that cell is from the road net.
Usage: offnet5.py <drop2 dir> <op 5 plan> <out>"""
import sys, json, math, numpy as np
from scipy.sparse import coo_matrix
from scipy.sparse.csgraph import dijkstra
from scipy.spatial import cKDTree
D, PLAN, OUT = sys.argv[1:4]
M = np.load(D + "/suddra_masks.npz"); Hh = np.load(D + "/suddra_height_cm.npz")["height_cm"] / 100.0
S = 2; CM = 4.0 * S
band = M["depth_band"][::S, ::S]; dry = M["ai_dry"][::S, ::S].astype(bool); boat = M["boat_core"][::S, ::S].astype(bool); Hs = Hh[::S, ::S]
WALK = {"players": band < 2, "AI": dry}
P = json.load(open(PLAN)); RP = np.vstack([np.array(r["points"], float) for r in P["roads"]]); RID = [r["id"] for r in P["roads"] for _ in r["points"]]; T = cKDTree(RP)
SITES = {"5-02": (1400.0, 12000.0, 98.5, 96.4), "5-M2.5": (3385.0, 12520.0, 45.1, 29.1), "5-12": (600.0, 11000.0, 15.0, 15.0), "5-13": (1840.0, 9705.0, 0.0, 0.0)}
bq = np.argwhere(boat); BXY = np.c_[bq[:, 1] * CM, bq[:, 0] * CM]; BT = cKDTree(BXY)

def graph(w):
    n, m = w.shape; idx = np.arange(n * m).reshape(n, m); rows, cols, wts = [], [], []
    for a, b, L in ((idx[:, :-1], idx[:, 1:], CM), (idx[:-1, :], idx[1:, :], CM), (idx[:-1, :-1], idx[1:, 1:], CM * 1.4142), (idx[:-1, 1:], idx[1:, :-1], CM * 1.4142)):
        a, b = a.ravel(), b.ravel(); ok = w.ravel()[a] & w.ravel()[b]
        rows.append(a[ok]); cols.append(b[ok]); wts.append(np.full(ok.sum(), L))
    r, c, x = np.concatenate(rows), np.concatenate(cols), np.concatenate(wts)
    return coo_matrix((np.r_[x, x], (np.r_[r, c], np.r_[c, r])), shape=(n * m, n * m)).tocsr(), idx

out = {}
for sid, (x, y, hx, hy) in SITES.items():
    R = 3500.0
    i0, i1 = max(0, int((y - R) / CM)), min(band.shape[0], int((y + R) / CM)); j0, j1 = max(0, int((x - R) / CM)), min(band.shape[1], int((x + R) / CM))
    yy, xx = np.mgrid[i0:i1, j0:j1] * CM; near_road = (T.query(np.c_[xx.ravel(), yy.ravel()])[0] <= 10.0)
    res = dict(pad=[x, y])
    for mode, WK in WALK.items():
        w = WK[i0:i1, j0:j1]; G, idx = graph(w); n, m = w.shape
        src = (np.hypot(np.maximum(abs(xx - x) - hx, 0), np.maximum(abs(yy - y) - hy, 0)) <= CM) & w
        if not src.any():
            d = np.where(w, np.hypot(xx - x, yy - y), np.inf); src = d == d.min()
        dist, pred, _ = dijkstra(G, indices=idx[src], min_only=True, return_predecessors=True)
        hit = near_road & np.isfinite(dist)
        if not hit.any(): res[mode] = "NO WALK to the road net within 3.5 km"; continue
        k = int(np.argmin(np.where(hit, dist, np.inf))); path = [k]
        while pred[path[-1]] >= 0: path.append(int(pred[path[-1]]))
        pi, pj = np.unravel_index(path, (n, m)); bb = band[i0:i1, j0:j1][pi, pj]; hh = Hs[i0:i1, j0:j1][pi, pj]; dd = dry[i0:i1, j0:j1][pi, pj]
        seg = np.hypot(np.diff(pi), np.diff(pj)) * CM
        res[mode] = dict(length_m=round(float(dist[k])), wade_m=round(float(seg[bb[:-1] == 1].sum())), low_not_water_m=round(float(seg[(bb[:-1] == 0) & ~dd[:-1]].sum())),
                         lowest_ground_m=round(float(hh.min()), 2), reaches=RID[int(T.query([xx.ravel()[k], yy.ravel()[k]])[1])],
                         at=[round(float(xx.ravel()[k])), round(float(yy.ravel()[k]))], straight_m=round(math.dist((x, y), (xx.ravel()[k], yy.ravel()[k]))))
    db, ib = BT.query((x, y))
    res["boat"] = dict(nearest_boat_water_m=round(float(db)), boat_cell=[round(float(BXY[ib][0])), round(float(BXY[ib][1]))], that_cell_to_road_m=round(float(T.query(BXY[ib])[0])))
    out[sid] = res; print(sid, json.dumps(res))
json.dump(out, open(OUT, "w"), indent=1)
