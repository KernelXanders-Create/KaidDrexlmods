"""print where a graded layout's infeasible ground points are (python3 diag.py layout.json site)"""
import sys, json, collections
from gtown import TG, windows_for, FIXED
LAY = json.load(open(sys.argv[1])); site = sys.argv[2]
fx = json.load(open(FIXED[site])) if site in FIXED else None
T = TG.grade(LAY, windows_for(site), fx)
pts = [T.G.xy(j, i) for j, i in T.G.infeasible_where]
print(len(pts), "infeasible:", sorted(pts)[:40])
import numpy as np
G = T.G; F = ~np.isnan(G.fix); fj, fi = np.nonzero(F); fz = G.fix[fj, fi]
for (j, i) in T.G.infeasible_where[:6]:
    d = np.hypot((fj - j) * 5.0, (fi - i) * 5.0)
    lo = fz - 0.6 * d; hi = fz + 0.6 * d
    a = lo.argmax(); b = hi.argmin()
    print(G.xy(j, i), "needs >=", round(lo[a], 2), "from", G.owner[fj[a], fi[a]], G.xy(fj[a], fi[a]), round(fz[a], 2), "| <=", round(hi[b], 2), "from", G.owner[fj[b], fi[b]], G.xy(fj[b], fi[b]), round(fz[b], 2))
