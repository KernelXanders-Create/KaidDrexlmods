"""Ops 5-8 sketch links vs drop 2 ground: shortest dry path (router's water rule: H > 0.3 m, 10 m clear), steps no steeper than 14 % on a 10 m lattice."""
import sys, json, math, numpy as np
from scipy import ndimage as nd
from scipy.sparse import coo_matrix
from scipy.sparse.csgraph import dijkstra
PK, SK, OUT = sys.argv[1:4]
H = np.load(PK + "/ground/height_whole_cm.npz")["height_cm"] / 100.0
s = 2; h = H[::s, ::s]; free = ~nd.binary_dilation(H <= 0.3, iterations=2)[::s, ::s]
ny, nx = h.shape; idx = np.arange(ny * nx).reshape(ny, nx); R = []; C = []; W = []
for dj, di in [(0, 1), (1, 0), (1, 1), (1, -1)]:
    A = np.s_[0:ny - dj, max(0, -di):nx - max(0, di)]; B = np.s_[dj:ny, max(0, di):nx - max(0, -di)]
    L = 10 * math.hypot(dj, di); ok = free[A] & free[B] & (np.abs(h[A] - h[B]) <= 0.14 * L)
    R.append(idx[A][ok]); C.append(idx[B][ok]); W.append(np.full(ok.sum(), L))
G = coo_matrix((np.concatenate(W), (np.concatenate(R), np.concatenate(C))), shape=(ny * nx, ny * nx)).tocsr()
P = json.load(open(SK)); XY = {x["id"]: tuple(x["xy"]) for x in P["sites"]}
XY.update({"5-05": (5729, 10092), "8-12": (8400, 15500)})      # ground check v1 f1 (HUMAN); SUD-R34 (c)
ST = {o["op"]: tuple(o["start"]) for o in P["ops"]}
def node(x, y, r=10):
    i, j = int(y / 10), int(x / 10); w = np.argwhere(free[max(i - r, 0):i + r + 1, max(j - r, 0):j + r + 1])
    if not len(w): return None, None
    k = w[np.argmin(((w + [max(i - r, 0), max(j - r, 0)] - [i, j]) ** 2).sum(1))]; q = (k[0] + max(i - r, 0), k[1] + max(j - r, 0))
    return idx[q], round(10 * math.hypot(q[0] - i, q[1] - j))
rows = []; cache = {}
for rd in P["roads"]:
    a, b = rd["links"]; pa = ST[rd["op"]] if a == "START" else XY[a]; pb = ST[rd["op"]] if b == "START" else XY[b]
    na, sa = node(*pa); nb, sb = node(*pb)
    row = dict(op=rd["op"], links=[a, b], straight_m=round(math.dist(pa, pb)), snap_m=[sa, sb])
    if na is None or nb is None: row["result"] = "end not on free ground within 100 m"; rows.append(row); continue
    if na not in cache: cache[na] = dijkstra(G, indices=na, return_predecessors=True, directed=False, limit=80000)
    d, pred = cache[na]
    if not np.isfinite(d[nb]): row["result"] = "NO DRY PATH (within 80 km)"; rows.append(row); continue
    p = [nb]
    while p[-1] != na: p.append(pred[p[-1]])
    row.update(result="dry path", dry_m=round(float(d[nb])), ratio=round(float(d[nb]) / max(row["straight_m"], 1), 2))
    rows.append(row)
json.dump(rows, open(OUT, "w"), indent=1)
#for r in rows: print(r["op"], "-".join(r["links"]).ljust(14), r["straight_m"], r["result"], r.get("dry_m", ""), r.get("ratio", ""), "snap", r["snap_m"])
# dry "islands": connected pieces of the dry, <= 14 % graph; which sites (and op starts) share one
from scipy.sparse.csgraph import connected_components
nc, lab = connected_components(G, directed=False)
isl = {}
for o in sorted(ST): 
    n, _ = node(*ST[o]); isl.setdefault(o, {}).setdefault(int(lab[n]) if n is not None else None, []).append("START")
for x in P["sites"]:
    n, _ = node(*XY[x["id"]]); isl.setdefault(x["op"], {}).setdefault(int(lab[n]) if n is not None else None, []).append(x["id"])
sizes_ = np.bincount(lab)
out2 = {o: [dict(island=k, area_km2=(round(float(sizes_[k]) * 100 / 1e6, 1) if k is not None else None), sites=v) for k, v in sorted(d.items(), key=lambda t: -len(t[1]))] for o, d in isl.items()}
json.dump(out2, open(OUT.replace(".json", "_islands.json"), "w"), indent=1)
for o, v in out2.items():
    print("op", o); [print("   island", e["island"], e["area_km2"], "km2:", e["sites"]) for e in v]
