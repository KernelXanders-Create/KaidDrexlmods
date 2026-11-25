"""Pack v5: pack v4 plus re-run v4 decisions 1-2 (shore fills at the op 4 north seats; pad fill under 4-07). Sizes and levels ASSUMED."""
import sys, json, math, shutil, numpy as np
A, B = sys.argv[1:3]
shutil.copytree(A, B, dirs_exist_ok=True)
H = np.load(A + "/ground/height_whole_cm.npz")["height_cm"].astype(float) / 100
yy, xx = np.mgrid[0:H.shape[0], 0:H.shape[1]]
log = json.load(open(A + "/ground_requests_applied.json"))
for sid, x, y, hx, hy in [("4-M2", 8400.9, 7841.5, 35.5, 25.5), ("4-M2.3", 8176.6, 7325.9, 30.0, 20.0), ("4-06", 7250.3, 7766.1, 28.4, 34.4)]:
    r = math.hypot(hx, hy) + 20.0; m = np.hypot(xx * 5.0 - x, yy * 5.0 - y) <= r
    lo = float(H[m].min()); H[m] = np.maximum(H[m], 0.75)
    log.append(dict(decision="re-run v4 1", kind="shore fill", site=sid, x=x, y=y, radius_m=round(r, 1), level_m=0.75, lowest_before_m=round(lo, 2), source="HUMAN decision; level and size ASSUMED"))
x, y, hx, hy = 6000.0, 6400.0, 98.5, 96.4
m = (abs(xx * 5.0 - x) <= hx + 20) & (abs(yy * 5.0 - y) <= hy + 20)
lo = float(H[m].min()); H[m] = np.maximum(H[m], 0.75)
log.append(dict(decision="re-run v4 2", kind="pad fill", site="4-07", x=x, y=y, half_size_m=[hx + 20, hy + 20], level_m=0.75, lowest_before_m=round(lo, 2), source="HUMAN decision; level and size ASSUMED"))
np.savez_compressed(B + "/ground/height_whole_cm.npz", height_cm=np.rint(H * 100).astype(np.int32))
json.dump(log, open(B + "/ground_requests_applied.json", "w"), indent=1); [print(l) for l in log[-4:]]
