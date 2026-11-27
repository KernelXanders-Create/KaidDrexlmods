"""6-M4 town guards (call 27 B, HUMAN): seats for the Small Rectangle FOB and the SSW gun by the SSW shore stub (T2), and the N gun by the N road (T1, 6-M4 -> 6-11).
Rules used (as in the planner checks): pad edge >= 10 m from the +0.3 m line; pad levelled to the middle of its ground, change <= 4 m;
pad edge >= 3 m from a road edge (7 m roads); pads >= 12 m apart; guns: 300 m clear of other pads along the bearing and no ground above the muzzle
(pad + 2.0 m, ASSUMED) within 150 m. 'By the road' = pad edge within 25 m of the road edge (ASSUMED). Yaws tried every 15 deg.
Usage: town64_guards.py <pack> <op 6 plan> <out json>"""
import sys, json, math, numpy as np
PK, PLAN, OUT = sys.argv[1:4]
H = np.load(PK + "/ground/height_whole_cm.npz")["height_cm"] / 100.0; C = 5.0
P = json.load(open(PLAN)); pads = [s for s in P["sites"] if s.get("hx")]
T = (13600.0, 11200.0)
def line(x0, y0, b, L): return np.array([[x0 + d * math.sin(math.radians(b)), y0 + d * math.cos(math.radians(b))] for d in np.arange(0, L + 0.1, 2.0)])
STUB = line(*T, 214.0, 194.0)                                     # T2 shore stub, town point to the K1 landing top
NROAD = np.array([r for r in P["roads"] if r["id"] == "6-M4-6-11"][0]["points"], float)
ROADS = [STUB] + [np.array(r["points"], float) for r in P["roads"]]
SIZES = {"FOB": ("CIS Small Rectangle FOB with GPs", 45.1, 29.1), "GUN": ("CIS Heavy Gun Position + AA (UD)", 29.9, 40.8)}
def uv(X, Y, x, y, yaw):
    t = math.radians(yaw); dx, dy = X - x, Y - y
    return dx * math.cos(t) - dy * math.sin(t), dx * math.sin(t) + dy * math.cos(t)
def rect_d(X, Y, x, y, yaw, hx, hy):
    u, v = uv(X, Y, x, y, yaw); return np.hypot(np.maximum(abs(u) - hx, 0), np.maximum(abs(v) - hy, 0))
def corners(x, y, yaw, hx, hy):
    t = math.radians(yaw); out = []
    for a, b in ((hx, hy), (hx, -hy), (-hx, -hy), (-hx, hy)):   # inverse of uv
        out.append((x + a * math.cos(t) + b * math.sin(t), y - a * math.sin(t) + b * math.cos(t)))
    return out
def ground(x, y, yaw, hx, hy, pad):
    r = math.hypot(hx, hy) + pad + 5; i0, i1 = int((y - r) / C), int((y + r) / C) + 1; j0, j1 = int((x - r) / C), int((x + r) / C) + 1
    yy, xx = np.mgrid[i0:i1, j0:j1] * C; d = rect_d(xx, yy, x, y, yaw, hx, hy)
    return H[i0:i1, j0:j1], d
def zg(x, y):
    j, i = x / C, y / C; j0, i0 = int(j), int(i); fx, fy = j - j0, i - i0
    return (H[i0, j0] * (1 - fx) * (1 - fy) + H[i0, j0 + 1] * fx * (1 - fy) + H[i0 + 1, j0] * (1 - fx) * fy + H[i0 + 1, j0 + 1] * fx * fy)
def facing(x, y, z, b, others):
    mz = z + 2.0; rise = max(zg(x + d * math.sin(math.radians(b)), y + d * math.cos(math.radians(b))) for d in range(0, 151, 5)) - mz
    hit = None
    for d in range(0, 301, 5):
        px, py = x + d * math.sin(math.radians(b)), y + d * math.cos(math.radians(b))
        for o in others:
            if rect_d(np.array(px), np.array(py), o["x"], o["y"], o["yaw"], o["hx"], o["hy"]) <= 0: hit = (d, o["id"]); break
        if hit: break
    return round(float(rise), 2), hit
def seat(kind, road, near_xy, bearing, placed, want):
    comp, hx, hy = SIZES[kind]; best = None
    for yaw in range(0, 180, 15):
        for dx in np.arange(-260, 261, 5.0):
            for dy in np.arange(-260, 261, 5.0):
                x, y = near_xy[0] + dx, near_xy[1] + dy
                rd = rect_d(road[:, 0], road[:, 1], x, y, yaw, hx, hy).min() - 3.5
                if not (3.0 <= rd <= 25.0): continue
                if min(rect_d(R[:, 0], R[:, 1], x, y, yaw, hx, hy).min() for R in ROADS) - 3.5 < 3.0: continue
                g, d = ground(x, y, yaw, hx, hy, 10.0)
                if (g[d <= 10.0] <= 0.3).any(): continue
                gin = g[d <= 0]; z = (gin.min() + gin.max()) / 2; ch = (gin.max() - gin.min()) / 2
                if ch > 4.0: continue
                others = pads + placed
                if any(min(rect_d(np.array([c[0] for c in corners(x, y, yaw, hx, hy)]), np.array([c[1] for c in corners(x, y, yaw, hx, hy)]), o["x"], o["y"], o["yaw"], o["hx"], o["hy"]).min(),
                           rect_d(np.array([c[0] for c in corners(o["x"], o["y"], o["yaw"], o["hx"], o["hy"])]), np.array([c[1] for c in corners(o["x"], o["y"], o["yaw"], o["hx"], o["hy"])]), x, y, yaw, hx, hy).min()) < 12.0
                       or rect_d(np.array(o["x"]), np.array(o["y"]), x, y, yaw, hx, hy) <= 0 for o in others): continue
                f = facing(x, y, z, bearing, others) if kind == "GUN" else None
                if f and (f[0] > 0 or f[1]): continue
                sc = want(x, y, rd)
                if best is None or sc < best["score"]:
                    best = dict(id=None, comp=comp, x=round(float(x), 1), y=round(float(y), 1), yaw=yaw, hx=hx, hy=hy, z=round(float(z), 2), change_m=round(float(ch), 2),
                                ground=[round(float(gin.min()), 2), round(float(gin.max()), 2)], road_edge_m=round(float(rd), 1),
                                from_town_point_m=round(math.dist((x, y), T)), score=sc,
                                facing=dict(bearing=bearing, rise_150m_m=f[0], clear_300m=not f[1]) if f else None)
    return best
out = {}; placed = []
landing = (13492.0, 11039.0)
fob = seat("FOB", STUB, (13540.0, 11110.0), None, placed, lambda x, y, rd: math.dist((x, y), landing))          # south edge: as near the landing end of the stub as it goes
fob["id"] = "6-M4 FOB"; placed.append(fob); out["FOB"] = fob
def other_side(x, y):     # the SSW gun stands on the stub's other side from the FOB
    s = lambda px, py: np.sign((STUB[-1, 0] - STUB[0, 0]) * (py - STUB[0, 1]) - (STUB[-1, 1] - STUB[0, 1]) * (px - STUB[0, 0]))
    return s(x, y) != s(fob["x"], fob["y"])
g1 = seat("GUN", STUB, (13540.0, 11110.0), 214, placed, lambda x, y, rd: math.dist((x, y), landing) + (0 if other_side(x, y) else 1e6))
g1["id"] = "6-M4 SSW gun"; placed.append(g1); out["SSW gun"] = g1
NJ = (13776.0, 11376.0)                     # T1: where the N road leaves the town's rise
g2 = seat("GUN", NROAD, NJ, 0, placed, lambda x, y, rd: math.dist((x, y), NJ))
if g2: g2["id"] = "6-M4 N gun"; out["N gun"] = g2
g2b = seat("GUN", NROAD, NJ, 45, placed, lambda x, y, rd: math.dist((x, y), NJ))
if g2b: g2b["id"] = "6-M4 N gun (along the road, 45 deg)"; out["N gun, road bearing"] = g2b
json.dump(out, open(OUT, "w"), indent=1)
for k, v in out.items(): print(k, {kk: vv for kk, vv in (v or {}).items() if kk != "score"})
