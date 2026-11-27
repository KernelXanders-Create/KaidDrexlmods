"""Pack v9: pack v8 plus approaches A6 (HUMAN): widen the 3-M2 causeway fill round 3-M2.3's seat on the 3-M2 trunk, (11461, 3440),
yaw 85, half-size 28.4 x 34.4 m, so its pad edge is 10 m clear of the +0.3 m line. Fill to +0.75 m out to 30 m beyond the pad edge (10 m clear + 20 m margin; ASSUMED)."""
import sys, json, math, shutil, numpy as np
A, B = sys.argv[1:3]
shutil.copytree(A, B, dirs_exist_ok=True)
H = np.load(A + "/ground/height_whole_cm.npz")["height_cm"].astype(float) / 100
log = json.load(open(A + "/ground_requests_applied.json"))
x0, y0, hx, hy, yaw = 11461.4, 3440.0, 28.4, 34.4, 85.0
yy, xx = np.mgrid[0:H.shape[0], 0:H.shape[1]]; X = xx * 5.0; Y = yy * 5.0
t = math.radians(yaw); u = (X - x0) * math.cos(t) - (Y - y0) * math.sin(t); v = (X - x0) * math.sin(t) + (Y - y0) * math.cos(t)
de = np.hypot(np.maximum(abs(u) - hx, 0), np.maximum(abs(v) - hy, 0)); m = de <= 30
lo = float(H[m].min()); before = H[m].copy(); H[m] = np.maximum(H[m], 0.75)
log.append(dict(decision="approaches ops 3-6 A6", kind="causeway widening round a seated checkpoint", site="3-M2.3", x=x0, y=y0, yaw=yaw, reach_beyond_pad_m=30, level_m=0.75,
                lowest_before_m=round(lo, 2), fill_m3=int((H[m] - before).sum() * 25), source="HUMAN decision; level and reach ASSUMED"))
np.savez_compressed(B + "/ground/height_whole_cm.npz", height_cm=np.rint(H * 100).astype(np.int32))
json.dump(log, open(B + "/ground_requests_applied.json", "w"), indent=1); print(log[-1])
