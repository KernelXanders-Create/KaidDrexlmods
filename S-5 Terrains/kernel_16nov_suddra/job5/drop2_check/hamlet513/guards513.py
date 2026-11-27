"""5-13 Stake Hamlet guards (call 28 B, HUMAN) at the new point (1840, 9705) (H1 a, H2 a), with no roads in: each gate stands astride a street stub that ends at the shore (H3 c).
Stubs: from the point on the bearing of each way in (NNE toward the 5-01 -> 5-F.3 road, 31 deg; SE toward the 5-09 -> 5-M1 road, 123 deg), to where the ground first drops below +0.5 m; 7 m wide (ASSUMED).
Gates: centred on the stub, the pad's long side along it (ASSUMED), as far out as the rules allow. Gun: between the gates on the side facing the op 5 start, facing it.
Rules as for the 6-M4 guards: pad edge >= 10 m from the +0.3 m line; level to the middle, change <= 4 m; pads >= 12 m apart; a pad not astride a stub keeps 3 m from its edge;
guns 300 m clear of pads on the bearing, no ground above the muzzle (pad + 2.0 m, ASSUMED) within 150 m. Usage: guards513.py <pack> <op 5 plan> <out>"""
import sys, json, math, numpy as np
PK, PLAN, OUT = sys.argv[1:4]
H = np.load(PK + "/ground/height_whole_cm.npz")["height_cm"] / 100.0; C = 5.0
PT = (1840.0, 9705.0); START = (5200.0, 7800.0)
pads = [s for s in json.load(open(PLAN))["sites"] if s.get("hx")]
def z(x, y): return float(H[int(round(y / C)), int(round(x / C))])
def zg(x, y):
    j, i = x / C, y / C; j0, i0 = int(j), int(i); fx, fy = j - j0, i - i0
    return float(H[i0, j0] * (1 - fx) * (1 - fy) + H[i0, j0 + 1] * fx * (1 - fy) + H[i0 + 1, j0] * (1 - fx) * fy + H[i0 + 1, j0 + 1] * fx * fy)
def at(b, s): return (PT[0] + s * math.sin(math.radians(b)), PT[1] + s * math.cos(math.radians(b)))
def stub(b):
    s = 0.0
    while zg(*at(b, s + 2.0)) >= 0.5: s += 2.0
    return s, np.array([at(b, t) for t in np.arange(0, s + 0.1, 2.0)])
def uv(X, Y, x, y, yaw):
    t = math.radians(yaw); dx, dy = X - x, Y - y; return dx * math.cos(t) - dy * math.sin(t), dx * math.sin(t) + dy * math.cos(t)
def rect_d(X, Y, x, y, yaw, hx, hy):
    u, v = uv(X, Y, x, y, yaw); return np.hypot(np.maximum(abs(u) - hx, 0), np.maximum(abs(v) - hy, 0))
def corners(o):
    t = math.radians(o["yaw"]); return np.array([(o["x"] + a * math.cos(t) + b * math.sin(t), o["y"] - a * math.sin(t) + b * math.cos(t)) for a, b in ((o["hx"], o["hy"]), (o["hx"], -o["hy"]), (-o["hx"], -o["hy"]), (-o["hx"], o["hy"]))])
def gap(a, b):
    ca, cb = corners(a), corners(b)
    if rect_d(np.array(a["x"]), np.array(a["y"]), b["x"], b["y"], b["yaw"], b["hx"], b["hy"]) <= 0: return 0.0
    return float(min(rect_d(ca[:, 0], ca[:, 1], b["x"], b["y"], b["yaw"], b["hx"], b["hy"]).min(), rect_d(cb[:, 0], cb[:, 1], a["x"], a["y"], a["yaw"], a["hx"], a["hy"]).min()))
def fit(o):
    r = math.hypot(o["hx"], o["hy"]) + 15; i0, i1 = int((o["y"] - r) / C), int((o["y"] + r) / C) + 1; j0, j1 = int((o["x"] - r) / C), int((o["x"] + r) / C) + 1
    yy, xx = np.mgrid[i0:i1, j0:j1] * C; d = rect_d(xx, yy, o["x"], o["y"], o["yaw"], o["hx"], o["hy"]); g = H[i0:i1, j0:j1]
    if (g[d <= 10.0] <= 0.3).any(): return None
    gi = g[d <= 0]; ch = (gi.max() - gi.min()) / 2
    return None if ch > 4.0 else dict(z=round(float((gi.max() + gi.min()) / 2), 2), change_m=round(float(ch), 2), ground=[round(float(gi.min()), 2), round(float(gi.max()), 2)])
def facing(o, b, others):
    mz = o["z"] + 2.0; rise = max(zg(o["x"] + d * math.sin(math.radians(b)), o["y"] + d * math.cos(math.radians(b))) for d in range(0, 151, 5)) - mz
    for d in range(0, 301, 5):
        px, py = o["x"] + d * math.sin(math.radians(b)), o["y"] + d * math.cos(math.radians(b))
        for p in others:
            if rect_d(np.array(px), np.array(py), p["x"], p["y"], p["yaw"], p["hx"], p["hy"]) <= 0: return round(rise, 2), (d, p["id"])
    return round(rise, 2), None
out = dict(point=PT, ground_at_point=round(z(*PT), 2), stubs={}, members=[])
GATES = [("NNE gate", "CIS Small Checkpoint with GPs", 28.4, 34.4, "KNOWN", 31), ("SE gate", "TKTA Checkpoint Fixed (Mono)", 20.0, 30.0, "ASSUMED (60 x 40 m, as in the ops 5-8 layout)", 123)]
placed = []
for nm, comp, hx, hy, src, b in GATES:
    L, line = stub(b); out["stubs"][nm] = dict(bearing=b, length_m=L, shore_xy=[round(line[-1][0]), round(line[-1][1])], shore_ground_m=round(zg(*line[-1]), 2))
    best = None
    for s in np.arange(0, L + 0.1, 2.5):
        x, y = at(b, s); o = dict(id=nm, comp=comp, x=round(x, 1), y=round(y, 1), yaw=b % 180, hx=hx, hy=hy, size_src=src, along_stub_m=float(s))
        f = fit(o)
        if not f or any(gap(o, p) < 12.0 for p in pads + placed): continue
        o.update(f); best = o
    out["members"].append(best); placed.append(best)
STUBS = [stub(b)[1] for b in (31, 123)]
bs = round(math.degrees(math.atan2(START[0] - PT[0], START[1] - PT[1])) % 360)
mid = ((placed[0]["x"] + placed[1]["x"]) / 2, (placed[0]["y"] + placed[1]["y"]) / 2)
best = None
for yaw in range(0, 180, 15):
    for dx in np.arange(-250, 251, 5.0):
        for dy in np.arange(-250, 251, 5.0):
            x, y = PT[0] + dx, PT[1] + dy
            own = math.degrees(math.atan2(x - PT[0], y - PT[1])) % 360
            if not (31 < own < 123): continue                 # between the two stubs: the wedge that holds the side facing the start
            o = dict(id="gun", comp="CIS Heavy Gun Position + AA (UD)", x=float(x), y=float(y), yaw=yaw, hx=29.9, hy=40.8, size_src="KNOWN")
            if min(rect_d(Sx[:, 0], Sx[:, 1], x, y, yaw, 29.9, 40.8).min() for Sx in STUBS) - 3.5 < 3.0: continue
            if any(gap(o, p) < 12.0 for p in pads + placed): continue
            f = fit(o)
            if not f: continue
            o.update(f); fc = facing(o, bs, pads + placed)
            if fc[0] > 0 or fc[1]: continue
            sc = math.dist((x, y), mid)
            if best is None or sc < best[0]: best = (sc, dict(o, facing=dict(bearing=bs, why="toward the op 5 start (call 28 B)", rise_150m_m=fc[0], clear_300m=True), from_point_m=round(math.dist((x, y), PT))))
out["members"].append(best[1] if best else dict(id="gun", status="NO SEAT"))
for m in out["members"]:
    if m and "x" in m: m["from_point_m"] = round(math.dist((m["x"], m["y"]), PT))
json.dump(out, open(OUT, "w"), indent=1); print(json.dumps(out, indent=1))
