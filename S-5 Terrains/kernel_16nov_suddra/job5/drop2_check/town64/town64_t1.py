"""T1 (HUMAN): the planned 6-M4 -> 6-11 road is the town's north road. Where it leaves the town's dry rise (+0.5 m, as town64.py), and its level there."""
import sys, json, math, numpy as np
from scipy import ndimage as nd
PK, PLAN = sys.argv[1:3]
H = np.load(PK + "/ground/height_whole_cm.npz")["height_cm"] / 100.0
X0, Y0, k = 13600.0, 11200.0, 80; i0, j0 = int(X0 / 5), int(Y0 / 5)
h = H[j0 - k:j0 + k + 1, i0 - k:i0 + k + 1]; yy, xx = np.mgrid[-k:k + 1, -k:k + 1] * 5.0
lab, _ = nd.label((h >= 0.5) & (np.hypot(xx, yy) <= 400), structure=np.ones((3, 3))); rise = lab == lab[k, k]
r = [r for r in json.load(open(PLAN))["roads"] if r["id"] == "6-M4-6-11"][0]
pts = r["points"] if math.dist(r["points"][0], (X0, Y0)) < math.dist(r["points"][-1], (X0, Y0)) else r["points"][::-1]
zs = r["points_z"] if pts is r["points"] else r["points_z"][::-1]
last = None
for p, z in zip(pts, zs):
    a, c = int(round((p[1] - Y0) / 5)) + k, int(round((p[0] - X0) / 5)) + k
    if not (0 <= a <= 2 * k and 0 <= c <= 2 * k and rise[a, c]): break
    last = (p, z)
p, z = last
print(json.dumps(dict(road="6-M4-6-11", road_length_m=r["length_m"], join_xy=[round(p[0]), round(p[1])], join_from_point_m=round(math.dist(p, (X0, Y0))),
                      join_bearing=round(math.degrees(math.atan2(p[0] - X0, p[1] - Y0)) % 360), road_level_m=round(z, 2), ground_m=round(float(H[int(round(p[1] / 5)), int(round(p[0] / 5))]), 2))))
