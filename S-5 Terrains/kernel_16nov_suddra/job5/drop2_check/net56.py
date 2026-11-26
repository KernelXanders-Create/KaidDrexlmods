"""Ops 5-6 road net redrawn on drop 2 (roads R4, HUMAN): minimum spanning tree over shortest dry paths (water rule H > 0.3 m + 10 m, steps <= 14 %),
with Kernel's 4 causeways (R2) opened as fill strips. Sites with no dry path stay off the net (foot / boat / air, R1-R3)."""
import sys, json, math, numpy as np
from scipy import ndimage as nd
from scipy.sparse import coo_matrix
from scipy.sparse.csgraph import dijkstra, minimum_spanning_tree
PK, SK, CW, OUT = sys.argv[1:5]
H = np.load(PK + "/ground/height_whole_cm.npz")["height_cm"] / 100.0
h = H[::2, ::2].copy(); free = ~nd.binary_dilation(H <= 0.3, iterations=2)[::2, ::2]
cws = [c for c in json.load(open(CW)) if c["sites"][0] in ("5-09", "6-07", "6-12", "5-12")]
for c in cws:      # a 7 m road on fill: open the straight strip (3 lattice cells wide) and level it to the ends' mean (ASSUMED fill level)
    (x0, y0), (x1, y1) = c["from_xy"], c["to_xy"]; n = max(int(math.dist((x0, y0), (x1, y1)) / 5), 2)
    for t in np.linspace(0, 1, n):
        i, j = int(round((y0 + t * (y1 - y0)) / 10)), int(round((x0 + t * (x1 - x0)) / 10)); free[i - 1:i + 2, j - 1:j + 2] = True
ny, nx = h.shape; idx = np.arange(ny * nx).reshape(ny, nx); R = []; C = []; W = []
for dj, di in [(0, 1), (1, 0), (1, 1), (1, -1)]:
    A = np.s_[0:ny - dj, max(0, -di):nx - max(0, di)]; B = np.s_[dj:ny, max(0, di):nx - max(0, -di)]
    L = 10 * math.hypot(dj, di); ok = free[A] & free[B] & (np.abs(h[A] - h[B]) <= 0.14 * L)
    R.append(idx[A][ok]); C.append(idx[B][ok]); W.append(np.full(ok.sum(), L))
G = coo_matrix((np.concatenate(W), (np.concatenate(R), np.concatenate(C))), shape=(ny * nx, ny * nx)).tocsr()
P = json.load(open(SK)); XY = {x["id"]: tuple(x["xy"]) for x in P["sites"]}; XY["5-05"] = (5729, 10092)
def node(x, y, r=10):
    i, j = int(y / 10), int(x / 10); i0, j0 = max(i - r, 0), max(j - r, 0); w = np.argwhere(free[i0:i + r + 1, j0:j + r + 1])
    if not len(w): return None
    k = w[np.argmin(((w + [i0, j0] - [i, j]) ** 2).sum(1))]; return idx[k[0] + i0, k[1] + j0]
res = {}
for op in (5, 6):
    ids = (["START"] if op == 5 else []) + [x["id"] for x in P["sites"] if x["op"] == op]
    pts = {k: (tuple([o for o in P["ops"] if o["op"] == op][0]["start"]) if k == "START" else XY[k]) for k in ids}
    nodes = {k: node(*pts[k]) for k in ids}; ids = [k for k in ids if nodes[k] is not None]
    D = dijkstra(G, indices=[nodes[k] for k in ids], directed=False, limit=60000, return_predecessors=True)
    dist, pred = D; M = dist[:, [nodes[k] for k in ids]]
    reach = np.isfinite(M[0]) if op == 5 else np.isfinite(M[[ids.index(max(ids, key=lambda k: np.isfinite(M[ids.index(k)]).sum()))]][0])
    on = [k for k, r in zip(ids, reach) if r]; off = [k for k, r in zip(ids, reach) if not r] + [k for k in pts if nodes.get(k) is None]
    sub = np.array([[M[ids.index(a), ids.index(b)] for b in on] for a in on]); T = minimum_spanning_tree(sub).tocoo()
    links = []
    for a, b, d in zip(T.row, T.col, T.data):
        A_, B_ = on[a], on[b]; s_ = math.dist(pts[A_], pts[B_])
        p = [nodes[B_]]; pr = pred[ids.index(A_)]
        while p[-1] != nodes[A_]: p.append(pr[p[-1]])
        pl = [[int(q % nx * 10), int(q // nx * 10)] for q in p[::-1]]
        links.append(dict(links=[A_, B_], dry_m=round(float(d)), straight_m=round(s_), ratio=round(float(d) / max(s_, 1), 2), points_10m=pl[::5] + [pl[-1]]))
    res[op] = dict(on_net=on, off_net=off, total_km=round(sum(l["dry_m"] for l in links) / 1000, 1), links=sorted(links, key=lambda l: -l["ratio"]), causeways=[c for c in cws if c["sites"][0][0] == str(op)])
    print("op", op, "on", len(on), "off", off, "total km", res[op]["total_km"])
    for l in res[op]["links"]: print("   ", "-".join(l["links"]).ljust(14), l["dry_m"], l["straight_m"], l["ratio"])
json.dump(res, open(OUT, "w"), indent=1)
