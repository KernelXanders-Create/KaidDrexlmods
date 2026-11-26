"""Shortest fill causeway from each small dry island (with an ops 5-6 site) to the main dry island: straight line between nearest free cells (router's water rule)."""
import sys, json, math, numpy as np
from scipy import ndimage as nd
PK, SK, OUT = sys.argv[1:4]
H = np.load(PK + "/ground/height_whole_cm.npz")["height_cm"] / 100.0
h = H[::2, ::2]; free = ~nd.binary_dilation(H <= 0.3, iterations=2)[::2, ::2]
lab, n = nd.label(free, structure=np.ones((3, 3))); big = np.bincount(lab.ravel()); big[0] = 0; main = int(np.argmax(big))
dist, (ii, jj) = nd.distance_transform_edt(lab != main, return_indices=True)
P = json.load(open(SK)); XY = {x["id"]: tuple(x["xy"]) for x in P["sites"]}; XY.update({"5-05": (5729, 10092)})
pts = {"START op6": tuple([o for o in P["ops"] if o["op"] == 6][0]["start"])}
pts.update({k: v for k, v in XY.items() if k[0] in "56"})
def lab_at(x, y):
    i, j = int(y / 10), int(x / 10); w = lab[i - 10:i + 11, j - 10:j + 11]; ls = set(w[w > 0].ravel()); return max(ls, key=lambda l: big[l]) if ls else 0
done = {}; rows = []
for k, (x, y) in pts.items():
    L = lab_at(x, y)
    if L in (0, main): continue
    if L not in done:
        c = np.argwhere(lab == L); d = dist[c[:, 0], c[:, 1]]; q = c[np.argmin(d)]; t = (ii[q[0], q[1]], jj[q[0], q[1]])
        nseg = max(int(math.dist(q, t)) * 2, 2); si = np.linspace(q[0], t[0], nseg).round().astype(int); sj = np.linspace(q[1], t[1], nseg).round().astype(int)
        seg = h[si, sj]; done[L] = dict(island_km2=round(big[L] * 100 / 1e6, 2), from_xy=[int(q[1] * 10), int(q[0] * 10)], to_xy=[int(t[1] * 10), int(t[0] * 10)],
                                       gap_m=round(float(d.min()) * 10), lowest_ground_m=round(float(seg.min()), 2), sites=[])
    done[L]["sites"].append(k)
rows = list(done.values()); json.dump(rows, open(OUT, "w"), indent=1)
for r in rows: print(r)
