import json, math, numpy as np, sys
from scipy import ndimage as nd
from scipy.sparse import coo_matrix
from scipy.sparse.csgraph import dijkstra
H = np.load(sys.argv[1] + "/ground/height_whole_cm.npz")["height_cm"] / 100.0
h = H[::2, ::2]; free = ~nd.binary_dilation(H <= 0.3, iterations=2)[::2, ::2]
ny, nx = h.shape; idx = np.arange(ny * nx).reshape(ny, nx); R = []; C = []; W = []
for dj, di in [(0, 1), (1, 0), (1, 1), (1, -1)]:
    A = np.s_[0:ny - dj, max(0, -di):nx - max(0, di)]; B = np.s_[dj:ny, max(0, di):nx - max(0, -di)]
    L = 10 * math.hypot(dj, di); ok = free[A] & free[B] & (np.abs(h[A] - h[B]) <= 0.14 * L)
    R.append(idx[A][ok]); C.append(idx[B][ok]); W.append(np.full(ok.sum(), L))
G = coo_matrix((np.concatenate(W), (np.concatenate(R), np.concatenate(C))), shape=(ny * nx, ny * nx)).tocsr()
def nd_(x, y): return idx[int(y / 10), int(x / 10)]
d12 = dijkstra(G, indices=nd_(600, 11000), directed=False, limit=20000).reshape(ny, nx)   # the 5-12 island
for tgt, xy in (("5-01", (2000, 10000)), ("5-F", (3000, 11000))):
    dt = dijkstra(G, indices=nd_(*xy), directed=False, limit=20000).reshape(ny, nx)
    near = np.isfinite(dt) & (dt <= 6000); isl = np.isfinite(d12)
    E, (ii, jj) = nd.distance_transform_edt(~near, return_indices=True)
    c = np.argwhere(isl); cost = E[c[:, 0], c[:, 1]] * 10 + d12[c[:, 0], c[:, 1]] + dt[ii[c[:, 0], c[:, 1]], jj[c[:, 0], c[:, 1]]]
    k = np.argmin(cost); q = c[k]; t = (ii[q[0], q[1]], jj[q[0], q[1]])
    seg = h[np.linspace(q[0], t[0], 50).round().astype(int), np.linspace(q[1], t[1], 50).round().astype(int)]
    print(tgt, "causeway from", (q[1] * 10, q[0] * 10), "to", (t[1] * 10, t[0] * 10), "gap %.0f m, lowest %+.2f; total 5-12 to %s %.0f m (straight %.0f)" % (E[q[0], q[1]] * 10, seg.min(), tgt, cost[k], math.dist((600, 11000), xy)))
