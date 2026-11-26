"""Seat each member of a site on good ground near the site point: axis-aligned (yaw 0 or 90), fully good, ground range <= 8 m, 17 m clear of seated members."""
import sys, json, math, numpy as np
sys.path.insert(0, sys.argv[2]); import sizes
D = sys.argv[1]; SK = sys.argv[3]; ids = sys.argv[4].split(",")
h = np.load(D + "/suddra_height_cm.npz")["height_cm"].astype(np.float32) / 100
m = np.load(D + "/suddra_masks.npz"); good = (m["ai_dry"] == 1) & (m["water"] == 0) & (h >= 0.5)
P = {s["id"]: s for s in json.load(open(SK))["sites"]}
out = {}
for sid in ids:
    s = P[sid]; x0, y0 = s["xy"]; seated = []; rows = []
    for k, c in enumerate(s["comps"]):
        try: hx, hy, ev = sizes.size(c)
        except Exception: rows.append(dict(member=k, comp=c, status="NOT MEASURED (no size): not seated")); continue
        best = None
        for d in range(0, 801, 8):
            for a in (range(0, 360, 10) if d else [0]):
                X, Y = x0 + d * math.sin(math.radians(a)), y0 + d * math.cos(math.radians(a))
                for yaw, ax, ay in ((0, hx, hy), (90, hy, hx)):
                    b = (slice(int((Y - ay) / 4), int((Y + ay) / 4) + 1), slice(int((X - ax) / 4), int((X + ax) / 4) + 1))
                    if not good[b].all() or h[b].max() - h[b].min() > 8.0: continue
                    if any(max(abs(X - q[0]) - ax - q[2], abs(Y - q[1]) - ay - q[3]) < 17 for q in seated): continue
                    best = (d, X, Y, yaw, ax, ay, float(h[b].min()), float(h[b].max())); break
                if best: break
            if best: break
        if not best: rows.append(dict(member=k, comp=c, status="no spot within 800 m")); continue
        d, X, Y, yaw, ax, ay, lo, hi = best; seated.append((X, Y, ax, ay))
        rows.append(dict(member=k, comp=c, size=[round(2 * hx), round(2 * hy)], size_src="KNOWN" if ev.startswith("KNOWN") else "ASSUMED", x=round(X), y=round(Y), yaw=yaw, from_point_m=d, ground=[round(lo, 2), round(hi, 2)]))
    out[sid] = rows
    print(sid, s["name"]); [print("  ", r) for r in rows]
json.dump(out, open(sys.argv[5], "w"), indent=1)
