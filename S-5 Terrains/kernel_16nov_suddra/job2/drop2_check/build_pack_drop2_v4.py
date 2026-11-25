"""Pack v4: pack v3 plus re-run v2 decision 3 (shore fill at 3-M1.2's third-pass seat, ASSUMED size and level)."""
import sys, json, math, shutil, numpy as np
A, B = sys.argv[1:3]
shutil.copytree(A, B, dirs_exist_ok=True)
H = np.load(A + "/ground/height_whole_cm.npz")["height_cm"].astype(float) / 100
yy, xx = np.mgrid[0:H.shape[0], 0:H.shape[1]]
log = json.load(open(A + "/ground_requests_applied.json"))
x, y, hx, hy = 13874.0, 5552.2, 28.4, 34.4
r = math.hypot(hx, hy) + 20.0; m = np.hypot(xx * 5.0 - x, yy * 5.0 - y) <= r
lo = float(H[m].min()); H[m] = np.maximum(H[m], 0.75)
log.append(dict(decision="re-run v2 3", kind="shore fill", site="3-M1.2", x=x, y=y, radius_m=round(r, 1), level_m=0.75, lowest_before_m=round(lo, 2), source="HUMAN decision; level and size ASSUMED"))
np.savez_compressed(B + "/ground/height_whole_cm.npz", height_cm=np.rint(H * 100).astype(np.int32))
json.dump(log, open(B + "/ground_requests_applied.json", "w"), indent=1); print(log[-1])
