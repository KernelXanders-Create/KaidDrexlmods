"""6-M4 Cauldron Apron Town: where its two roads join (call 27 / JOB_5 decision 28), on the drop 2 ground (pack v7).
The town is the dry rise round its sketch point: ground at +0.5 m or higher (the village form rule), joined to the point (8-connected), within 400 m (ASSUMED).
Each road joins where its approach bearing leaves that rise."""
import sys, json, math, numpy as np
from scipy import ndimage as nd
PK, PLAN, OUT = sys.argv[1:4]
H = np.load(PK + "/ground/height_whole_cm.npz")["height_cm"] / 100.0
X0, Y0 = 13600.0, 11200.0; R = 400.0
i0, j0 = int(X0 / 5), int(Y0 / 5); k = int(R / 5)
h = H[j0 - k:j0 + k + 1, i0 - k:i0 + k + 1]; yy, xx = np.mgrid[-k:k + 1, -k:k + 1] * 5.0
lab, _ = nd.label((h >= 0.5) & (np.hypot(xx, yy) <= R), structure=np.ones((3, 3))); L = lab[k, k]
rise = lab == L if L else np.zeros_like(h, bool)
area_ha = rise.sum() * 25 / 1e4
D = json.load(open(PLAN)); roads = D["roads"]
res = dict(point=[X0, Y0], point_z=round(float(H[j0, i0]), 2), rise_area_ha=round(area_ha, 1), rise_z=[round(float(h[rise].min()), 2), round(float(h[rise].max()), 2)],
           rise_extent_m=dict(x=[int(xx[rise].min()), int(xx[rise].max())], y=[int(yy[rise].min()), int(yy[rise].max())]), roads=[])
for name, b, toward in (("N road toward 6-06 NE Esker Fort", 0.0, (13600.0, 12400.0)), ("SSW road toward 6-M3 Tank Laager", 214.0, (12800.0, 10000.0))):
    ux, uy = math.sin(math.radians(b)), math.cos(math.radians(b)); edge = None
    for t in np.arange(0, R, 5.0):
        a, c = int(round(uy * t / 5)) + k, int(round(ux * t / 5)) + k
        if not rise[a, c]: break
        edge = t
    ex, ey = X0 + ux * edge, Y0 + uy * edge
    # beyond the edge: ground along the bearing to the place the road comes from
    far = math.dist((X0, Y0), toward); prof = [(t, float(H[int(round((Y0 + uy * t) / 5)), int(round((X0 + ux * t) / 5))])) for t in np.arange(edge, far, 5.0)]
    wet = [t for t, z in prof if z <= 0.3]
    # nearest planned op 6 road point to the join
    best = min(((math.dist((ex, ey), p), r["id"], p, z) for r in roads for p, z in zip(r["points"], r["points_z"])), key=lambda q: q[0])
    res["roads"].append(dict(road=name, bearing=b, join_xy=[round(ex), round(ey)], join_from_point_m=int(edge), join_ground_z=round(float(H[int(round(ey / 5)), int(round(ex / 5))]), 2),
                             line_to=list(toward), line_m=round(far), first_wet_m_from_point=int(wet[0]) if wet else None, wet_m=len(wet) * 5,
                             nearest_planned_road=best[1], nearest_planned_point=[round(best[2][0]), round(best[2][1])], nearest_planned_m=round(best[0]), nearest_planned_z=best[3]))
json.dump(res, open(OUT, "w"), indent=1); print(json.dumps(res, indent=1))
