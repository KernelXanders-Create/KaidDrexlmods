"""Ops 5-8 sketch points vs drop 2 ground. Main comp footprint (yaw 0, size table) at the site point; whole-site disc (all comps' area, ASSUMED layout)."""
import sys, json, math, numpy as np
sys.path.insert(0, sys.argv[3]); import sizes
D, SK = sys.argv[1:3]
h = np.load(D + "/suddra_height_cm.npz")["height_cm"].astype(np.float32) / 100
m = np.load(D + "/suddra_masks.npz"); W = m["water"]; A = m["ai_dry"]; good = (A == 1) & (W == 0) & (h >= 0.5)
P = json.load(open(SK))
MOVES = {"5-05": (5400, 9700), "8-12": (8400, 15500)}   # call 5A (HUMAN); SUD-R34 option (c) (owner)
def sz(c):
    try: hx, hy, ev = sizes.size(c); return hx, hy, "KNOWN" if ev.startswith("KNOWN") else "ASSUMED"
    except Exception: return None
def box(x, y, hx, hy):
    i0, i1 = int((y - hy) / 4), int((y + hy) / 4) + 1; j0, j1 = int((x - hx) / 4), int((x + hx) / 4) + 1
    return slice(max(i0, 0), min(i1, 4096)), slice(max(j0, 0), min(j1, 4096))
def disc(x, y, r):
    i, j = box(x, y, r, r); yy, xx = np.mgrid[i, j]; k = np.hypot(xx * 4 - x, yy * 4 - y) <= r; return yy[k], xx[k]
rows = []
for s in P["sites"]:
    x, y = MOVES.get(s["id"], s["xy"]); szs = [sz(c) for c in s["comps"]]
    main = szs[0]; area = sum(4 * a[0] * a[1] for a in szs if a); r = max(60.0, math.sqrt(area / math.pi) * 1.5) if area else 60.0
    row = dict(id=s["id"], op=s["op"], name=s["name"], role=s["role"], xy=[x, y], comp=s["comps"][0], moved=s["id"] in MOVES)
    ii, jj = disc(x, y, r); row.update(site_r_m=round(r), site_good=round(100 * good[ii, jj].mean()), site_water=round(100 * W[ii, jj].mean()), site_ground=[round(float(h[ii, jj].min()), 2), round(float(h[ii, jj].max()), 2)])
    if main:
        b = box(x, y, main[0], main[1]); g = h[b]; row.update(main_size=[round(2 * main[0]), round(2 * main[1])], size_src=main[2], main_good=round(100 * good[b].mean()), main_water=round(100 * W[b].mean()), main_ground=[round(float(g.min()), 2), round(float(g.max()), 2)])
        if good[b].mean() < 0.9 or g.max() - g.min() > 4.0:
            res = []
            for d in range(8, 801, 8):
                for a in range(0, 360, 10):
                    X, Y = x + d * math.sin(math.radians(a)), y + d * math.cos(math.radians(a)); bb = box(X, Y, main[0], main[1])
                    if good[bb].all() and h[bb].max() - h[bb].min() <= 4.0: res.append((d, round(X), round(Y), a, round(float(h[bb].mean()), 2)))
                if len(res) >= 1 and d > res[0][0] + 150: break
            picks = []
            for q in res:
                if all(min(abs(q[3] - p[3]), 360 - abs(q[3] - p[3])) > 60 for p in picks): picks.append(q)
                if len(picks) == 3: break
            row["dry_spots"] = picks
    else: row.update(main_size="NOT MEASURED (no size)")
    rows.append(row)
json.dump(rows, open(sys.argv[4], "w"), indent=1)
for r in rows:
    flag = "" if r.get("main_good", r["site_good"]) >= 90 and (not r.get("main_ground") or r["main_ground"][1] - r["main_ground"][0] <= 4) else "  <<"
    print(r["id"], r["comp"][:34].ljust(34), r.get("main_size"), "main good", r.get("main_good"), "water", r.get("main_water"), "gr", r.get("main_ground"), "| site r", r["site_r_m"], "good", r["site_good"], "water", r["site_water"], flag, r.get("dry_spots", "")[:3] if r.get("dry_spots") else "")
