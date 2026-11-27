"""5-13 on the NNE rise (H1 a, HUMAN). The hamlet point is the rise point at least 80 m inside its +0.5 m edge that is nearest the old sketch point (80 m ASSUMED: room for a ring of about 30 houses).
From it, the two ways in (call 28: NNE toward 5-01, SE toward 5-09) are traced on the bearing to each site: where they leave the rise, and the wet (<= +0.3 m) metres before the nearest op 5 road."""
import sys, json, math, numpy as np
from scipy import ndimage as nd
from scipy.spatial import cKDTree
PK, PLAN, OUT = sys.argv[1:4]
H = np.load(PK + "/ground/height_whole_cm.npz")["height_cm"] / 100.0; C = 5.0; P0 = (1600.0, 9000.0)
def z(x, y): return float(H[int(round(y / C)), int(round(x / C))])
i0, i1, j0, j1 = int(7800 / C), int(10800 / C), int(400 / C), int(3400 / C)
sub = H[i0:i1, j0:j1]; lab, _ = nd.label(sub >= 0.5); k = lab[int(8925 / C) - i0, int(1825 / C) - j0]; rise = lab == k
inner = nd.distance_transform_edt(rise) * C >= 80.0
yy, xx = np.mgrid[i0:i1, j0:j1] * C; d = np.where(inner, np.hypot(xx - P0[0], yy - P0[1]), np.inf); a = np.unravel_index(d.argmin(), d.shape)
pt = (float(xx[a]), float(yy[a]))
RD = json.load(open(PLAN))["roads"]; ALLP = np.vstack([np.array(r["points"], float) for r in RD]); IDS = sum([[r["id"]] * len(r["points"]) for r in RD], []); T = cKDTree(ALLP)
SK = {s["id"]: s for s in json.load(open("../ops5_8_sketch.json"))["sites"]}
out = dict(rise_area_ha=round(float(rise.sum()) * C * C / 1e4, 1), point=pt, ground_at_point=round(z(*pt), 2), moved_from_sketch_m=round(math.dist(pt, P0)), ways={})
for sid in ("5-01", "5-09"):
    tx, ty = SK[sid]["xy"]; b = math.degrees(math.atan2(tx - pt[0], ty - pt[1])) % 360; L = math.dist(pt, (tx, ty))
    leave = None; wet = 0.0; road = None
    for s in np.arange(0, L, 5.0):
        x, y = pt[0] + s * math.sin(math.radians(b)), pt[1] + s * math.cos(math.radians(b)); g = z(x, y)
        inr = rise[int(round(y / C)) - i0, int(round(x / C)) - j0] if (i0 <= y / C < i1 and j0 <= x / C < j1) else False
        if leave is None and not inr: leave = dict(xy=[round(x), round(y)], dist_m=float(s), ground_m=round(g, 2))
        if g <= 0.3: wet += 5.0
        dd, ii = T.query((x, y))
        if leave and dd <= 10.0: road = dict(road=IDS[ii], xy=[round(x), round(y)], dist_m=float(s)); break
    out["ways"][sid] = dict(site=SK[sid]["name"], bearing=round(b), straight_m=round(L), leaves_rise=leave, wet_m_before_road=wet, meets_road=road)
json.dump(out, open(OUT, "w"), indent=1); print(json.dumps(out, indent=1))
