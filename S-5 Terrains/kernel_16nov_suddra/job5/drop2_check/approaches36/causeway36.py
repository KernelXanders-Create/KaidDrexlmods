"""Fill causeways on a wet approach side: the straight line from the site's centre to the place the approach comes from.
Wet = ground at or below +0.3 m. Each wet stretch is filled to +0.75 m, 50 m wide (25 m half-width, as the ops 5-6 causeways; ASSUMED);
stretches less than 50 m apart are joined (ASSUMED). Volume counts the fill above the ground under the 50 m deck only (no side slopes: ASSUMED).
Usage: PACK_C=<pack> python3 causeway36.py name x0 y0 x1 y1 start_m"""
import sys, os, math, json, numpy as np
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "../../../job2/tools_sketch"))
import world
nm = sys.argv[1]; x0, y0, x1, y1, st = map(float, sys.argv[2:7]); L = math.dist((x0, y0), (x1, y1)); ux, uy = (x1 - x0) / L, (y1 - y0) / L; px, py = -uy, ux
d = np.arange(st, L, 5.0)
zc = np.array([world.z(x0 + ux * t, y0 + uy * t) for t in d])
zw = np.array([[world.z(x0 + ux * t + px * o, y0 + uy * t + py * o) for o in np.arange(-25, 26, 5)] for t in d])     # across the 50 m deck
wet = zc <= 0.3
pcs = []; i = 0
while i < len(wet):
    if wet[i]:
        j = i
        while j < len(wet) and wet[j]: j += 1
        if pcs and d[i] - pcs[-1][1] < 50: pcs[-1][1] = d[j - 1] + 5
        else: pcs.append([d[i], d[j - 1] + 5])
        i = j
    else: i += 1
out = []
for a, b in pcs:
    k = (d >= a) & (d < b); fill = np.clip(0.75 - zw[k], 0, None)
    out.append(dict(from_m=int(a), to_m=int(b), length_m=int(b - a), lowest_ground_m=round(float(zc[k].min()), 2), max_fill_m=round(float(fill.max()), 2),
                    fill_m3=int(fill.sum() * 5 * 5)))
r = dict(approach=nm, line_from=[x0, y0], line_to=[x1, y1], line_m=round(L), bearing=round(math.degrees(math.atan2(ux, uy)) % 360), pieces=out,
         causeway_m=sum(p["length_m"] for p in out), fill_m3=sum(p["fill_m3"] for p in out), max_fill_m=max([p["max_fill_m"] for p in out], default=0),
         worst_10m_grade_dry_pct=round(float((np.abs(np.diff(zc[::2])) / 10 * 100)[~(wet[::2][1:])].max()), 1))
print(json.dumps(r))
