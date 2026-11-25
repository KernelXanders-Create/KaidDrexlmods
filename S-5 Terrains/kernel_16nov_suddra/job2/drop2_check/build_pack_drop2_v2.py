"""Pack v2: the drop 2 pack plus Kernel's re-run decisions 2 and 6 as ASSUMED fills."""
import sys, json, math, shutil, numpy as np
from scipy import ndimage as nd
A, B = sys.argv[1:3]
shutil.copytree(A, B, dirs_exist_ok=True)
H = np.load(A + "/ground/height_whole_cm.npz")["height_cm"].astype(float) / 100
yy, xx = np.mgrid[0:H.shape[0], 0:H.shape[1]]
log = json.load(open(A + "/ground_requests_applied.json"))
# decision 2: the 16.7 % step at (13824, 5436) is where the 3-M1.2 pad level (+1.417 m) meets the trunk (+0.66 m), MEASURED.
# Ground request: an apron sloping out from the pad edge at 8 % (ASSUMED) down to the ground, so the road comes in at the pad level.
x0, y0, hx, hy, yaw, zp = 13855.3, 5461.8, 28.4, 34.4, 46.0, 1.417
t = math.radians(yaw); X_, Y_ = xx * 5.0 - x0, yy * 5.0 - y0
u = X_ * math.cos(t) - Y_ * math.sin(t); v = X_ * math.sin(t) + Y_ * math.cos(t)
de = np.hypot(np.maximum(abs(u) - hx, 0), np.maximum(abs(v) - hy, 0))
ap = zp - 0.08 * de; m = (de <= 30) & (ap > H)
ch = float((ap - H)[m].max()) if m.any() else 0.0; H[m] = ap[m]
log.append(dict(decision="re-run 2", kind="apron from the 3-M1.2 pad edge", x=x0, y=y0, pad_level_m=zp, slope_pct=8, reach_m=30, max_fill_m=round(ch, 2), source="HUMAN decision; slope and reach ASSUMED"))
# decision 6: shore fills under the four seats, ground raised to >= 0.75 m within the pad's half-diagonal + 20 m (ASSUMED size)
for sid, x, y, hx, hy in [("3-M1.2", 13855.3, 5461.8, 28.4, 34.4), ("4-06", 7516.4, 7652.4, 28.4, 34.4),
                          ("4-M2", 8522.9, 7779.1, 35.5, 25.5), ("4-M2.3", 8231.0, 7262.1, 30.0, 20.0)]:
    r = math.hypot(hx, hy) + 20.0; m = np.hypot(xx * 5.0 - x, yy * 5.0 - y) <= r
    lo = float(H[m].min()); H[m] = np.maximum(H[m], 0.75)
    log.append(dict(decision="re-run 6", kind="shore fill", site=sid, x=x, y=y, radius_m=round(r, 1), level_m=0.75, lowest_before_m=round(lo, 2), source="HUMAN decision; level and size ASSUMED"))
np.savez_compressed(B + "/ground/height_whole_cm.npz", height_cm=np.rint(H * 100).astype(np.int32))
json.dump(log, open(B + "/ground_requests_applied.json", "w"), indent=1)
[print(l) for l in log[-5:]]
