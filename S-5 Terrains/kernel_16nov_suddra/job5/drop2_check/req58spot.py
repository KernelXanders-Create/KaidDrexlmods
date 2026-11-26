"""For a member that needs a ground request beside its site: the spot within R m of the point, 17 m clear of the seated members, needing the least fill (fewest cells below good)."""
import sys, json, math, numpy as np
D = sys.argv[1]; spec = json.loads(sys.argv[2])
h = np.load(D + "/suddra_height_cm.npz")["height_cm"].astype(np.float32) / 100
m = np.load(D + "/suddra_masks.npz"); good = (m["ai_dry"] == 1) & (m["water"] == 0) & (h >= 0.5)
for name, (x0, y0), (hx, hy), seated, R in spec:
    best = None
    for dx in range(-R, R + 1, 8):
        for dy in range(-R, R + 1, 8):
            if math.hypot(dx, dy) > R: continue
            for yaw, ax, ay in ((0, hx, hy), (90, hy, hx)):
                X, Y = x0 + dx, y0 + dy
                if any(max(abs(X - q[0]) - ax - q[2], abs(Y - q[1]) - ay - q[3]) < 17 for q in seated): continue
                b = (slice(int((Y - ay) / 4), int((Y + ay) / 4) + 1), slice(int((X - ax) / 4), int((X + ax) / 4) + 1))
                g = h[b]; bad = (~good[b]).mean()
                if g.max() - g.min() > 8: continue
                key = (round(bad, 3), math.hypot(dx, dy))
                if best is None or key < best[0]: best = (key, X, Y, yaw, float(g.min()), float(g.max()))
    print(json.dumps(dict(member=name, x=best[1], y=best[2], yaw=best[3], bad_pct=round(100 * best[0][0], 1), from_point_m=round(best[0][1]), ground=[round(best[4], 2), round(best[5], 2)])))
