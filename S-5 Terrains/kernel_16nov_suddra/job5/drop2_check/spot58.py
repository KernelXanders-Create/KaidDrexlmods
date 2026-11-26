import sys, json, math, numpy as np
D = sys.argv[1]; x, y, hx, hy = map(float, sys.argv[2:6]); lim = float(sys.argv[6]) if len(sys.argv) > 6 else 8
h = np.load(D + "/suddra_height_cm.npz")["height_cm"].astype(np.float32) / 100
m = np.load(D + "/suddra_masks.npz"); good = (m["ai_dry"] == 1) & (m["water"] == 0) & (h >= 0.5)
def box(X, Y): return slice(max(int((Y - hy) / 4), 0), min(int((Y + hy) / 4) + 1, 4096)), slice(max(int((X - hx) / 4), 0), min(int((X + hx) / 4) + 1, 4096))
b = box(x, y); print("at point: good %.0f%%, water %.0f%%, ground %+.2f..%+.2f" % (100 * good[b].mean(), 100 * m["water"][b].mean(), h[b].min(), h[b].max()))
res = []
for d in range(8, 1601, 8):
    for a in range(0, 360, 10):
        X, Y = x + d * math.sin(math.radians(a)), y + d * math.cos(math.radians(a)); bb = box(X, Y)
        if good[bb].size and good[bb].all() and h[bb].max() - h[bb].min() <= lim: res.append((d, round(X), round(Y), a, round(float(h[bb].min()), 2), round(float(h[bb].max()), 2)))
picks = []
for q in res:
    if all(min(abs(q[3] - p[3]), 360 - abs(q[3] - p[3])) > 60 for p in picks): picks.append(q)
    if len(picks) == 3: break
for p in picks: print("  spot (%d, %d): %d m toward %d deg, ground %+.2f..%+.2f" % (p[1], p[2], p[0], p[3], p[4], p[5]))
if not picks: print("  none within 1600 m")
