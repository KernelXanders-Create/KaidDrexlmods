"""Pack v6: pack v5 plus the ops 5-6 ground requests (Kernel: ground check ops 5-8 f6a, f6b, f6c; roads R2). Levels and margins ASSUMED."""
import sys, json, math, shutil, numpy as np
A, B = sys.argv[1:3]
shutil.copytree(A, B, dirs_exist_ok=True)
H = np.load(A + "/ground/height_whole_cm.npz")["height_cm"].astype(float) / 100
yy, xx = np.mgrid[0:H.shape[0], 0:H.shape[1]]; X = xx * 5.0; Y = yy * 5.0
log = json.load(open(A + "/ground_requests_applied.json"))
for tag, sid, x, y, hx, hy in [("ops58 f6a", "5-02", 1400, 12000, 98.5, 96.4), ("ops58 f6b", "6-06", 13600, 12400, 77.0, 72.5), ("ops58 f6c", "5-M2.4 (2nd Basic Trenchline)", 3370, 12682, 57.0, 30.0)]:
    m = (abs(X - x) <= hx + 20) & (abs(Y - y) <= hy + 20); lo = float(H[m].min()); H[m] = np.maximum(H[m], 0.75)
    log.append(dict(decision=tag, kind="pad fill", site=sid, x=x, y=y, half_size_m=[hx + 20, hy + 20], level_m=0.75, lowest_before_m=round(lo, 2), source="HUMAN decision; level and margin ASSUMED"))
for c in json.load(open(sys.argv[3])):
    if c["sites"][0] not in ("5-09", "6-07", "6-12", "5-12"): continue
    (x0, y0), (x1, y1) = c["from_xy"], c["to_xy"]; L = max(math.dist((x0, y0), (x1, y1)), 1.0)
    t = np.clip(((X - x0) * (x1 - x0) + (Y - y0) * (y1 - y0)) / L ** 2, 0, 1); d = np.hypot(X - (x0 + t * (x1 - x0)), Y - (y0 + t * (y1 - y0)))
    m = d <= 15.0 + 10.0; lo = float(H[m].min()); H[m] = np.maximum(H[m], 0.75)     # 7 m road + its 10 m water clearance each side, rounded to 25 m half-width
    log.append(dict(decision="ops58 roads R2", kind="causeway fill", site=c["sites"][0], from_xy=c["from_xy"], to_xy=c["to_xy"], gap_m=c["gap_m"], half_width_m=25, level_m=0.75, lowest_before_m=round(lo, 2), source="HUMAN decision; width and level ASSUMED"))
np.savez_compressed(B + "/ground/height_whole_cm.npz", height_cm=np.rint(H * 100).astype(np.int32))
json.dump(log, open(B + "/ground_requests_applied.json", "w"), indent=1); [print(l) for l in log[-7:]]
