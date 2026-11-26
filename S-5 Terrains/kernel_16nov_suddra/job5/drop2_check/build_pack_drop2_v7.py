"""Pack v7: pack v6 plus the ops 5-6 planner v1 ground requests (P1, P2). Levels, slopes and margins ASSUMED."""
import sys, json, math, shutil, numpy as np
A, B = sys.argv[1:3]
shutil.copytree(A, B, dirs_exist_ok=True)
H = np.load(A + "/ground/height_whole_cm.npz")["height_cm"].astype(float) / 100
yy, xx = np.mgrid[0:H.shape[0], 0:H.shape[1]]; X = xx * 5.0; Y = yy * 5.0
log = json.load(open(A + "/ground_requests_applied.json"))
# P1: 6-03's road meets 6-05 at the pad's edge with a 0.67 m step. An apron round 6-05 (pad +3.75 m, yaw 15) that runs at 8 % from the pad edge out to 30 m,
# filling where the ground is lower and cutting where it is higher, so a joining road lands on the pad's level.
x0, y0, hx, hy, yaw, zp = 10200.0, 11800.0, 98.5, 96.4, 15.0, 3.75
t = math.radians(yaw); u = (X - x0) * math.cos(t) - (Y - y0) * math.sin(t); v = (X - x0) * math.sin(t) + (Y - y0) * math.cos(t)
de = np.hypot(np.maximum(abs(u) - hx, 0), np.maximum(abs(v) - hy, 0)); m = (de > 0) & (de <= 30)
lo_, hi_ = zp - 0.08 * de, zp + 0.08 * de; new = np.clip(H, lo_, hi_); ch = float(np.abs(new - H)[m].max())
H[m] = new[m]
log.append(dict(decision="ops56 planner P1", kind="apron round the 6-05 pad (cut and fill)", site="6-05", x=x0, y=y0, pad_level_m=zp, slope_pct=8, reach_m=30, max_change_m=round(ch, 2), source="HUMAN decision; slope and reach ASSUMED"))
# P2: fills under 5-M2.3 (Basic Trenchline, yaw 90) and 5-M2.5 (Small Rectangle FOB) at their layout seats, so they pass the planner's water rule (+0.3 m, 15 m clear)
for sid, x, y, ax, ay in [("5-M2.3", 3476.0, 12644.0, 30.0, 57.0), ("5-M2.5", 3386.0, 12521.0, 45.0, 29.0)]:
    m = (abs(X - x) <= ax + 20) & (abs(Y - y) <= ay + 20); lo = float(H[m].min()); H[m] = np.maximum(H[m], 0.75)
    log.append(dict(decision="ops56 planner P2", kind="pad fill", site=sid, x=x, y=y, half_size_m=[ax + 20, ay + 20], level_m=0.75, lowest_before_m=round(lo, 2), source="HUMAN decision; level and margin ASSUMED"))
np.savez_compressed(B + "/ground/height_whole_cm.npz", height_cm=np.rint(H * 100).astype(np.int32))
json.dump(log, open(B + "/ground_requests_applied.json", "w"), indent=1); [print(l) for l in log[-3:]]
