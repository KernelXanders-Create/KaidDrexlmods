"""K5: Perys v5 on the real ground with the real catalogue (PROPOSED).

Run:  python3 tools/perys_v5.py <pack dir> <out dir>
Hand-drawn: street lines (in a slope frame: a = along the contour toward SE,
b = downhill toward NE, origin at the NW road port), the square, the quay group.
Scripted: street levels, model packing per block on shared pads, checks, plot.
"""
import json, math, sys, collections
import numpy as np
from shapely.geometry import Polygon, LineString, Point, box
from shapely.ops import unary_union

PACK, OUT = sys.argv[1], sys.argv[2]
H = np.load(PACK + "/perys/height_perys_natural_1m.npy"); X0, Y0 = 4880.0, 2950.0
CAT = {b["model_id"]: b for b in json.load(open(PACK + "/catalogue/buildings.json"))["buildings"]}
V4 = json.load(open(PACK + "/perys/perys_v4_layout.json"))
RNG = np.random.default_rng(7)

def hz(x, y):
    fx, fy = x - X0, y - Y0
    c0, r0 = int(math.floor(fx)), int(math.floor(fy)); tx, ty = fx - c0, fy - r0
    a = H[r0, c0] * (1 - tx) + H[r0, c0 + 1] * tx; b = H[r0 + 1, c0] * (1 - tx) + H[r0 + 1, c0 + 1] * tx
    return float(a * (1 - ty) + b * ty)

def hz_vec(xs, ys):
    fx, fy = xs - X0, ys - Y0; c0 = np.floor(fx).astype(int); r0 = np.floor(fy).astype(int); tx, ty = fx - c0, fy - r0
    a = H[r0, c0] * (1 - tx) + H[r0, c0 + 1] * tx; b = H[r0 + 1, c0] * (1 - tx) + H[r0 + 1, c0 + 1] * tx
    return a * (1 - ty) + b * ty

def quick_cf(poly, pz, step=1.5):
    g = poly.buffer(1.5, join_style=2); x0, y0, x1, y1 = g.bounds
    xs, ys = np.meshgrid(np.arange(x0, x1 + 0.01, step), np.arange(y0, y1 + 0.01, step))
    from shapely import contains_xy
    m = contains_xy(g, xs, ys)
    if not m.any(): return 0.0
    v = hz_vec(xs[m], ys[m]); return float(max(v.max() - pz, pz - v.min(), 0))

# slope frame
P0 = np.array([5087.3, 3408.5]); CU = np.array([math.sin(math.radians(132)), math.cos(math.radians(132))])
DU = np.array([math.sin(math.radians(42)), math.cos(math.radians(42))])
def W(a, b): return tuple(P0 + a * CU + b * DU)

def chaikin(p, it=3):
    p = np.array(p, float)
    for _ in range(it):
        q = [p[0]]
        for u, v in zip(p[:-1], p[1:]): q += [0.75 * u + 0.25 * v, 0.25 * u + 0.75 * v]
        q.append(p[-1]); p = np.array(q)
    return p

def resample(line, step=5.0):
    n = max(2, int(math.ceil(line.length / step)) + 1)
    return [line.interpolate(i / (n - 1), normalized=True).coords[0] for i in range(n)]

def max_run(line, tol=1.5, step=2.0):
    pts = np.array(resample(line, step)); best = 0.0
    for i in range(len(pts) - 1):
        j = i + 1
        while j + 1 < len(pts):
            a, b = pts[i], pts[j + 1]; ab = b - a; v = pts[i:j + 2] - a
            if (np.abs(ab[0] * v[:, 1] - ab[1] * v[:, 0]) / (np.linalg.norm(ab) + 1e-9)).max() > tol: break
            j += 1
        best = max(best, float(np.linalg.norm(pts[j] - pts[i])))
    return best

# ------------------------------------------------------------------ hand design
D = {
 "M": dict(cls="main", w=8.0, ab=[(0, 0), (30, 10), (62, 8), (96, 20), (128, 17), (160, 28), (184, 24), (206, 33), (228, 36), (252, 47), (278, 58), (302, 62)],
           grade=4.5, name="Odos Perys (main street, AI road)"),
 "U": dict(cls="lane", w=5.0, ab=[(14, -31), (44, -27), (78, -25), (110, -16), (140, -18), (166, -4), (190, -4), (214, 8), (238, 4), (266, 14), (290, 25), (318, 26)],
           grade=17, name="Ano Rouga (upper lane)"),
 "K": dict(cls="lane", w=5.0, ab=[(28, 45), (62, 43), (96, 55), (112, 52)], grade=17, name="Kato Rouga west (lower lane)"),
 "K2": dict(cls="lane", w=5.0, ab=[(212, 74), (234, 80), (256, 82), (280, 94), (306, 98), (326, 112)], grade=17, name="Kato Rouga east (lower lane)"),
 "C1": dict(cls="lane", w=4.5, ab=[(44, -27), (52, -10), (62, 8), (62, 26), (62, 43)], grade=17, name="cross lane west"),
 "C2": dict(cls="lane", w=4.5, ab=[(214, 8), (220, 22), (226, 36), (222, 54), (212, 74)], grade=17, name="cross lane east"),
 "C3": dict(cls="lane", w=4.5, ab=[(266, 14), (260, 30), (256, 50), (256, 66), (256, 82)], grade=17, name="cross lane far east"),
 "C4": dict(cls="lane", w=4.5, ab=[(110, -16), (106, 2), (100, 20), (98, 38), (96, 55)], grade=17, name="cross lane centre"),
 "UP": dict(cls="path", w=3.0, ab=[(150, -14), (154, 4), (160, 21)], grade=40, name="stair path to the square"),
 "HL": dict(cls="lane", w=5.0, ab=[(62, 43), (60, 70), (58, 92), (57, 112)], grade=17, name="harbour link (to v4 harbour road)"),
}
SQ_AB = [(140, 26), (182, 28), (190, 46), (180, 64), (148, 62), (136, 44)]      # downhill of M, open to the NE (sea)
SQ_OPEN = ((182, 66), (148, 62))                                                 # the open (seaward) edge

def street_levels(name, pts):
    """Street level: natural ground smoothed, then grade-limited both ways."""
    s = [0.0]
    for a, b in zip(pts[:-1], pts[1:]): s.append(s[-1] + math.dist(a, b))
    g = np.array([hz(*p) for p in pts]); k = max(1, int(round(15 / 5)))
    z = np.array([g[max(0, i - k):i + k + 1].mean() for i in range(len(g))])
    lim = D[name]["grade"] / 100.0
    if name == "M": z[0] = 59.4
    for _ in range(50):
        for i in range(1, len(z)): z[i] = min(max(z[i], z[i - 1] - lim * (s[i] - s[i - 1])), z[i - 1] + lim * (s[i] - s[i - 1]))
        for i in range(len(z) - 2, 0 if name == "M" else -1, -1): z[i] = min(max(z[i], z[i + 1] - lim * (s[i + 1] - s[i])), z[i + 1] + lim * (s[i + 1] - s[i]))
    return np.array(s), z

STREETS = {}
for k, d in D.items():
    line = LineString(chaikin([W(*p) for p in d["ab"]], 3))
    pts = resample(line, 5.0)
    if k == "M":
        pts[0] = (5087.3, 3408.5)
    if k == "HL":
        pts[-1] = tuple(next(x for x in V4["streets"] if x["id"] == "HR")["points"][0])   # meet v4's harbour road exactly
    line = LineString(pts)
    s, z = street_levels(k, pts)
    STREETS[k] = dict(d, id=k, line=line, pts=pts, s=s, z=z, rib=line.buffer(d["w"] / 2, cap_style=2))
HR = next(s for s in V4["streets"] if s["id"] == "HR")
STREETS["HR"] = dict(cls="main", w=HR["width_m"], name="harbour road (v4 HR, unchanged)", id="HR", line=LineString(HR["points"]),
                     pts=HR["points"], s=None, z=None, rib=LineString(HR["points"]).buffer(HR["width_m"] / 2, cap_style=2), grade=None, keep=True)
RIBS = unary_union([v["rib"] for v in STREETS.values()])
SQ = Polygon([W(*p) for p in SQ_AB]).buffer(0)
QUAY = box(5632, 3546, 5722, 3584)
def _sq_level():
    x0, y0, x1, y1 = SQ.bounds; xs, ys = np.meshgrid(np.arange(x0, x1, 1.0), np.arange(y0, y1, 1.0))
    from shapely import contains_xy
    m = contains_xy(SQ, xs, ys); v = hz_vec(xs[m], ys[m]); return round(float(v.mean()), 1), float(v.max()), float(v.min())
SQZ, SQ_GMAX, SQ_GMIN = _sq_level()
def AB(x, y):
    v = np.array([x, y]) - P0; return float(v @ CU), float(v @ DU)
SQ_SPLIT_B = 45.0                      # the step between the upper and lower terrace of the square
def _terrace(lo):
    x0, y0, x1, y1 = SQ.bounds; xs, ys = np.meshgrid(np.arange(x0, x1, 1.0), np.arange(y0, y1, 1.0))
    from shapely import contains_xy
    m = contains_xy(SQ, xs, ys); bb = np.array([AB(x, y)[1] for x, y in zip(xs[m], ys[m])])
    sel = (bb >= SQ_SPLIT_B) if lo else (bb < SQ_SPLIT_B); v = hz_vec(xs[m][sel], ys[m][sel]); return round(float(v.mean()), 1)
SQ_UP, SQ_LO = _terrace(False), _terrace(True)
def sq_z(x, y): return SQ_UP if AB(x, y)[1] < SQ_SPLIT_B else SQ_LO

def zs(st, x, y):
    if st["z"] is None: return hz(x, y)
    p = st["line"].project(Point(x, y)); return float(np.interp(p, st["s"], st["z"]))

# ------------------------------------------------------------------ models
def dims_along(m, door):
    """(frontage along the street, depth into the lot) for a door facing the street."""
    return (m["width_m"], m["depth_m"]) if door in ("front", "back") else (m["depth_m"], m["width_m"])

def yaw_for(bearing_to_street, door):
    off = {"front": 0, "right": 90, "back": 180, "left": 270}[door]
    return (bearing_to_street - off) % 360

def footprint(mid, x, y, yaw):
    m = CAT[mid]; a = math.radians(yaw)
    ex = np.array([math.cos(a), -math.sin(a)]); ez = np.array([math.sin(a), math.cos(a)]); c = np.array([x, y])
    w, d = m["width_m"] / 2, m["depth_m"] / 2
    return Polygon([c + w * ex + d * ez, c - w * ex + d * ez, c - w * ex - d * ez, c + w * ex - d * ez])

TWIN = {}
for mid, m in CAT.items():
    TWIN[mid] = f"{m['family']}|{m['width_m']}|{m['depth_m']}"
POOLS = {
    "square": ["SF06", "SF01", "SF08", "SF15", "WH09", "SF16", "WH02", "WH21"],
    "main": ["WH01", "WH02", "WH03", "WH04", "WH09", "WH11", "WH21", "WH23", "WH12", "WH07", "WH08", "ND03", "ND05", "ND01", "ND02", "SF01", "SF08", "SF15", "SF16", "WH24", "WH22", "WH19", "WH18"],
    "lane": ["WH01", "WH04", "WH03", "WH11", "WH12", "WH08", "WH24", "ND01", "ND02", "ND03", "ND04", "WH06", "WH17", "WH19", "WH22", "WH23", "WH18", "WH05", "SF16", "SF15"],
    "quay": ["IN01", "IN02", "IN03", "SF15", "SF16"],
}
CAP_MODEL, CAP_TWIN = 0.11, 0.14
TARGET_N = 96

class Town:
    def __init__(self):
        self.B = []; self.polys = []; self.count = collections.Counter(); self.twin = collections.Counter(); self.pad = 0

    def ok_poly(self, poly, pad_group, why=None):
        if poly.intersects(RIBS.buffer(0.3)) and poly.intersection(RIBS.buffer(0.3)).area > 0.01:
            if why is not None:
                why["street"] += 1
                for kk, vv in STREETS.items():
                    if poly.intersects(vv["rib"].buffer(0.3)): why["st_" + kk] += 1
            return False
        if poly.intersects(SQ) and poly.intersection(SQ).area > 0.01:
            if why is not None: why["square"] += 1
            return False
        for b, q in zip(self.B, self.polys):
            gap = 0.0 if b["pad_group"] == pad_group else 0.3
            if poly.distance(q) < gap or poly.intersection(q).area > 0.001:
                if why is not None: why["building"] += 1
                return False
        return True

    def allowed(self, mid):
        n = max(len(self.B), 40)
        return self.count[mid] + 1 <= CAP_MODEL * TARGET_N and self.twin[TWIN[mid]] + 1 <= CAP_TWIN * TARGET_N

    def add(self, mid, x, y, yaw, door, pad_group, pad_z, street, role):
        poly = footprint(mid, x, y, yaw)
        b = dict(id=f"B{len(self.B) + 1:03d}", model_id=mid, x=round(x, 2), y=round(y, 2), yaw_deg=round(yaw % 360, 2), door_side=door,
                 garrison=False, pad_group=pad_group, pad_z_m=round(pad_z, 2),
                 door_bearing_deg=round((yaw + {"front": 0, "right": 90, "back": 180, "left": 270}[door]) % 360, 1),
                 street=street, role=role)
        self.B.append(b); self.polys.append(poly); self.count[mid] += 1; self.twin[TWIN[mid]] += 1
        return b

    def pack_side(self, st, side, pool, max_depth, role, jitter=3.0, max_blk=6):
        """Walk one side of a street. Each building takes the street's local direction
        at its own middle; buildings in one block touch and share one pad (the street
        level at the block's first door). A block ends at 3-6 buildings, when a door's
        street level drifts more than 0.8 m from the pad, or when nothing fits."""
        line, w = st["line"], st["w"]; L = line.length; s = 1.5
        while s < L - 5:
            self.pad += 1; pg = f"P{self.pad:03d}"; blk = 0; s0 = s
            pad_z = zs(st, *line.interpolate(s + 5).coords[0]); jit = RNG.uniform(-jitter, jitter); fails = 0
            want = int(RNG.integers(3, max_blk + 1))
            while blk < want and fails < 4 and s < L - 5:
                cands = [m for m in pool if self.allowed(m)]; RNG.shuffle(cands); placed = False
                if role == "main" and RNG.random() < 0.55:          # the main street must read sci-fi: try sci-fi first
                    cands.sort(key=lambda mm: 0 if CAT[mm]["family"] == "scifi" else 1)
                for mid in cands[:10]:
                    m = CAT[mid]; door = m["door_side"]; fw, dp = dims_along(m, door)
                    if dp > max_depth or (m["tall"] and role != "square"): PW["depth"] += 1; continue
                    if s + fw > L - 2: PW["end"] += 1; continue
                    smid = s + fw / 2
                    q0 = np.array(line.interpolate(max(smid - 3, 0)).coords[0]); q1 = np.array(line.interpolate(min(smid + 3, L)).coords[0])
                    t = (q1 - q0) / (np.linalg.norm(q1 - q0) + 1e-9)
                    ang = math.radians(jit); t = np.array([math.cos(ang) * t[0] - math.sin(ang) * t[1], math.sin(ang) * t[0] + math.cos(ang) * t[1]])
                    n = np.array([-t[1], t[0]]) * side
                    door_pt = np.array(line.interpolate(smid).coords[0]) + n * (w / 2 + 0.35)
                    if abs(zs(st, *door_pt) - pad_z) > 0.8: PW["drift"] += 1; continue
                    yaw = yaw_for(math.degrees(math.atan2(-n[0], -n[1])) % 360, door)
                    good = False
                    for extra in (0.0, 0.5, 1.0, 1.6):            # step back off a curve rather than drop the house
                        cen = door_pt + n * (extra + dp / 2)
                        poly = footprint(mid, cen[0], cen[1], yaw)
                        lim_cf = 3.2 if (role == "main" and m["family"] == "scifi") else 2.4   # sci-fi on the main street may go near the limit (listed)
                        if quick_cf(poly, pad_z) > lim_cf: PW["cutfill"] += 1; break
                        if self.ok_poly(poly, pg, PW): good = True; break
                    if not good: continue
                    self.add(mid, cen[0], cen[1], yaw, door, pg, pad_z, st["id"], role); blk += 1; PW["placed"] += 1
                    s += fw + 0.08; placed = True; break
                if not placed:
                    fails += 1; s += 1.5
            if blk:
                self.nblk = getattr(self, "nblk", 0) + 1
                s += RNG.uniform(2.8, 4.0) if self.nblk % 4 == 0 else 0.31   # passage every 4th block, else a 0.31 m step (just over the 0.3 m minimum)
            else:
                self.pad -= 1; s = max(s, s0 + 2.0)

T = Town()
WHY = collections.Counter(); WHYQ = collections.Counter(); PW = collections.Counter()

def build():
    M, U, K, K2 = STREETS["M"], STREETS["U"], STREETS["K"], STREETS["K2"]
    # square ring first (sci-fi core) and the landmark
    sqc = np.array(SQ.centroid.coords[0])
    T.pad += 1
    lm_xy = np.array(W(168, 54))
    yaw = math.degrees(math.atan2(*(sqc - lm_xy))) % 360
    T.add("ND07", lm_xy[0], lm_xy[1], yaw, "front", f"P{T.pad:03d}", sq_z(*lm_xy), "SQ", "landmark")
    # square ring: the NW and SE sides (the SW side is the main street, the NE side stays open to the sea)
    sqz = SQZ
    for side_pts in ([(148, 62), (136, 44), (140, 26)], [(182, 28), (190, 46), (180, 64)]):
        line = LineString([W(*p) for p in side_pts])
        ss = np.linspace(0, line.length, 60); zz = np.array([sq_z(*line.interpolate(v).coords[0]) for v in ss])
        fake = dict(id="SQ", line=line, w=0.0, s=ss, z=zz)
        # the side of travel that points away from the square centre
        mid = np.array(line.interpolate(0.5, normalized=True).coords[0]); q = np.array(line.interpolate(0.55, normalized=True).coords[0])
        t = (q - mid) / np.linalg.norm(q - mid); nl = np.array([-t[1], t[0]])
        side = 1 if np.dot(nl, mid - sqc) > 0 else -1
        PW.clear()
        for _ in range(2):   # two passes so short leftovers still get a building
            T.pack_side(fake, side, POOLS["square"] + ["SF17", "WH11", "WH24", "WH04"], 22.0, "square", jitter=0.0, max_blk=5)
    print("RING", dict(PW), [ (round(v,1)) for v in (SQ_UP, SQ_LO)])
    # main street both sides; lanes both sides; lower lanes' seaward side one row
    mainpool = POOLS["main"] + ["SF01", "SF08", "SF15", "SF16", "SF01", "SF15"]      # sci-fi weighted on the main street
    T.pack_side(M, +1, mainpool, 16.6, "main")       # left of travel (SE) = north-east = downhill side
    T.pack_side(M, -1, mainpool, 16.6, "main")
    T.pack_side(STREETS["U"], +1, POOLS["lane"], 11.5, "lane")     # U: +1 faces the main street's back rows
    T.pack_side(STREETS["U"], -1, POOLS["lane"], 16.5, "lane")
    for k in ("K", "K2"):
        T.pack_side(STREETS[k], -1, POOLS["lane"], 11.5, "lane")   # K: -1 faces the main street's back rows
        T.pack_side(STREETS[k], +1, POOLS["lane"], 16.5, "lane")
    for k in ("C1", "C2", "C3", "C4", "HL"):
        T.pack_side(STREETS[k], +1, POOLS["lane"], 12.0, "lane")
        T.pack_side(STREETS[k], -1, POOLS["lane"], 12.0, "lane")
    # quay group: low halls on the apron's landward strip, doors to the quay (north)
    T.pad += 1; pg = f"P{T.pad:03d}"; x = 5652.0
    for mid in ["IN01", "SF15", "IN02", "SF16", "IN03"]:
        m = CAT[mid]; door = m["door_side"]; fw, dp = dims_along(m, door)
        if x + fw > 5720: break
        cen = (x + fw / 2, 3547.0 + dp / 2)
        yaw = yaw_for(0.0, door)
        poly = footprint(mid, cen[0], cen[1], yaw)
        if T.ok_poly(poly, pg, WHYQ):
            T.add(mid, cen[0], cen[1], yaw, door, pg, 2.2, "QY", "quay"); x += fw + 0.05

build()
print("square ring rejects", dict(WHY), "quay rejects", dict(WHYQ), "pack", dict(PW))

# ------------------------------------------------------------------ garrison
ENT = [b for b in T.B if CAT[b["model_id"]]["enterable"]]
prio = {"square": 0, "quay": 1, "main": 2, "lane": 3, "landmark": 9}
ENT.sort(key=lambda b: (prio.get(b["role"], 5), RNG.random()))
gsel = []
for b in ENT:
    if len(gsel) >= 50: break
    if all(math.dist((b["x"], b["y"]), (g["x"], g["y"])) > 14 or b["role"] in ("square", "quay") for g in gsel):
        gsel.append(b)
for b in ENT:
    if len(gsel) >= 46: break
    if b not in gsel: gsel.append(b)
for b in gsel: b["garrison"] = True

# ------------------------------------------------------------------ retaining walls
WALLS = []
for k, st in STREETS.items():
    if st.get("keep") or st["cls"] == "path": continue
    line, w = st["line"], st["w"]; L = line.length; s = 0.0
    while s + 6.94 <= L:
        for side in (1, -1):
            p0 = np.array(line.interpolate(s).coords[0]); p1 = np.array(line.interpolate(s + 6.94).coords[0])
            t = (p1 - p0) / np.linalg.norm(p1 - p0); n = np.array([-t[1], t[0]]) * side
            a0, a1 = p0 + n * (w / 2 + 0.6), p1 + n * (w / 2 + 0.6)
            mid = (a0 + a1) / 2; zst = zs(st, *((p0 + p1) / 2))
            bank = hz(*(mid + n * 3.0)) - zst
            seg = LineString([a0, a1])
            covered = any(seg.distance(q) < 2.5 for q in T.polys) or seg.intersects(SQ) or seg.buffer(0.9).intersects(RIBS.difference(st["rib"].buffer(0.5)))
            if bank > 1.5 and not covered:
                WALLS.append(dict(model_id="WL01", points=[[round(a0[0], 2), round(a0[1], 2)], [round(a1[0], 2), round(a1[1], 2)]], street=k, bank_m=round(bank, 2)))
        s += 6.94

# ------------------------------------------------------------------ checks
def cutfill(poly, pz):
    g = poly.buffer(1.5, join_style=2); x0, y0, x1, y1 = g.bounds; v = []
    for yy in np.arange(math.floor(y0), math.ceil(y1) + 1):
        for xx in np.arange(math.floor(x0), math.ceil(x1) + 1):
            if g.contains(Point(xx, yy)): v.append(hz(xx, yy))
    return max(v) - pz, pz - min(v)

CHK = {}
cfs = []
for b, q in zip(T.B, T.polys):
    c, f = cutfill(q, b["pad_z_m"]); b["cut_m"] = round(max(c, 0), 2); b["fill_m"] = round(max(f, 0), 2); cfs.append(max(c, f, 0))
cfs = np.array(cfs)
CHK["pad_cut_fill_m"] = dict(max=round(float(cfs.max()), 2), median=round(float(np.median(cfs)), 2), n_over_2_5=int((cfs > 2.5).sum()),
                             n_over_4=int((cfs > 4).sum()), near_limit=[b["id"] for b, v in zip(T.B, cfs) if 2.5 < v <= 4.0])
ov_bb = 0; ov_list = []
for i in range(len(T.B)):
    for j in range(i + 1, len(T.B)):
        a, b = T.polys[i], T.polys[j]
        if a.intersection(b).area > 0.01: ov_bb += 1; ov_list.append((T.B[i]["id"], T.B[j]["id"]))
        elif T.B[i]["pad_group"] != T.B[j]["pad_group"] and a.distance(b) < 0.3: ov_bb += 1; ov_list.append((T.B[i]["id"], T.B[j]["id"], "gap<0.3"))
ov_br = [b["id"] for b, q in zip(T.B, T.polys) if q.intersection(RIBS).area > 0.01]
CHK["overlaps"] = dict(building_pairs=ov_bb, pairs=ov_list[:10], building_vs_street=len(ov_br), list=ov_br)
CHK["straight_runs_m"] = {k: round(max_run(v["line"]), 1) for k, v in STREETS.items()}
cnt = collections.Counter(b["model_id"] for b in T.B); n = len(T.B)
tw = collections.Counter(TWIN[b["model_id"]] for b in T.B)
CHK["model_share"] = dict(largest=[cnt.most_common(1)[0][0], round(100 * cnt.most_common(1)[0][1] / n, 1)],
                          largest_twin_group_pct=round(100 * tw.most_common(1)[0][1] / n, 1), distinct_models=len(cnt))
door_fail = []
SQB = SQ.buffer(0.6); QB = QUAY.buffer(0.6); RB = RIBS.buffer(0.6)
for b in T.B:
    m = CAT[b["model_id"]]; a = math.radians(b["door_bearing_deg"]); half = (m["depth_m"] if b["door_side"] in ("front", "back") else m["width_m"]) / 2
    p = Point(b["x"] + (half + 3) * math.sin(a), b["y"] + (half + 3) * math.cos(a))
    if not (RB.contains(p) or SQB.contains(p) or QB.contains(p)): door_fail.append(b["id"])
CHK["door_check"] = dict(ok=n - len(door_fail), fail=len(door_fail), fail_ids=door_fail)
gr = {}
for k, st in STREETS.items():
    if st["z"] is None:
        z = np.array([hz(*p) for p in st["pts"]]); s = [0.0]
        for a, b in zip(st["pts"][:-1], st["pts"][1:]): s.append(s[-1] + math.dist(a, b))
        s = np.array(s); nat = z
    else:
        z, s = st["z"], st["s"]; nat = np.array([hz(*p) for p in st["pts"]])
    g = np.abs(np.diff(z)) / np.maximum(np.diff(s), 1e-6)
    gr[k] = dict(cls=st["cls"], width_m=st["w"], length_m=round(float(s[-1])), max_grade_pct=round(100 * float(g.max()), 1),
                 max_cut_m=round(float((nat - z).max()), 2), max_fill_m=round(float((z - nat).max()), 2),
                 limit_pct={"main": 5, "lane": 19, "path": None}[st["cls"]])
CHK["street_grades"] = gr
tall = [(b["id"], b["model_id"], b["role"]) for b in T.B if CAT[b["model_id"]]["tall"]]
CHK["counts"] = dict(buildings=n, enterable=sum(CAT[b["model_id"]]["enterable"] for b in T.B), garrison=sum(b["garrison"] for b in T.B),
                     tall=tall, by_role=dict(collections.Counter(b["role"] for b in T.B)),
                     families=dict(collections.Counter(CAT[b["model_id"]]["family"] for b in T.B)))
# K0-style read checks
groups = collections.Counter(b["pad_group"] for b in T.B)
CHK["blocks"] = dict(share_in_shared_pads_of_3plus=round(100 * sum(c for c in groups.values() if c >= 3) / n, 1),
                     pad_groups=len(groups), distinct_pad_levels=len(set(round(b["pad_z_m"], 1) for b in T.B)))
tg = unary_union([q.buffer(6) for q in T.polys if True] + [SQ] + [v["rib"] for k, v in STREETS.items() if not v.get("keep")]).buffer(4).buffer(-6)
twn = tg.difference(QUAY.buffer(60)) if not tg.is_empty else tg
CHK["town_ground_m2"] = dict(this=round(twn.area), v4=61302, limit=79700)
bld_area = sum(q.area for q, b in zip(T.polys, T.B) if b["role"] != "quay")
st_area = unary_union([v["rib"] for k, v in STREETS.items() if not v.get("keep")]).intersection(twn).area
CHK["building_to_street_area"] = round(bld_area / st_area, 2)
CHK["walls"] = dict(pieces=len(WALLS), total_m=round(6.94 * len(WALLS), 1))
sqdoors = sum(1 for b in T.B if b["role"] in ("square",))
sqc_ = np.array(SQ.centroid.coords[0]); sides = collections.Counter(); ndoor = 0
for b in T.B:
    m = CAT[b["model_id"]]; a = math.radians(b["door_bearing_deg"]); half = (m["depth_m"] if b["door_side"] in ("front", "back") else m["width_m"]) / 2
    p3 = Point(b["x"] + (half + 3) * math.sin(a), b["y"] + (half + 3) * math.cos(a))
    if p3.distance(SQ) < 4.5 and b["role"] != "landmark":
        ndoor += 1; v = np.array([b["x"], b["y"]]) - sqc_
        sides[["NE (sea)", "SE", "SW (main street)", "NW"][int(((math.degrees(math.atan2(v[0], v[1])) - 42 + 45) % 360) // 90)]] += 1
CHK["square"] = dict(area_m2=round(SQ.area), level_z=f"two terraces: upper {SQ_UP} m (main-street side), lower {SQ_LO} m (sea side), split {SQ_SPLIT_B} m into the slope frame; one flight of steps", natural_ground_under_square_m=[round(SQ_GMIN, 2), round(SQ_GMAX, 2)],
                     main_street_level_at_square=round(zs(STREETS["M"], *W(160, 30)), 2), landmark="ND07 on the square",
                     doors_on_or_within_4_5m_of_square=ndoor, sides_with_doors=dict(sides))

# ------------------------------------------------------------------ outputs
streets_out = []
for k, st in STREETS.items():
    streets_out.append(dict(id=k, name=st["name"], **{"class": st["cls"]}, width_m=st["w"],
                            points=[[round(x, 2), round(y, 2)] for x, y in st["pts"]],
                            points_z=[round(float(v), 2) for v in st["z"]] if st["z"] is not None else None))
sqz = SQZ
comps = [dict(name_or_role="market on the upper terrace of the square (e.g. Crystal Carts, whole comp)", x=round(W(158, 36)[0], 2), y=round(W(158, 36)[1], 2), yaw_deg=42.0, footprint_m=[9.5, 9.4], pad_z_m=SQ_UP),
         dict(name_or_role="third square comp on the upper terrace: a covered market hall or cargo stack group (whole comp, your pick)", x=round(W(176, 38)[0], 2), y=round(W(176, 38)[1], 2), yaw_deg=42.0, footprint_m=[10.0, 10.0], pad_z_m=SQ_UP),
         dict(name_or_role="second square comp on the lower terrace: a covered stall or fountain group (whole comp, your pick)", x=round(W(156, 54)[0], 2), y=round(W(156, 54)[1], 2), yaw_deg=42.0, footprint_m=[8.0, 8.0], pad_z_m=SQ_LO),
         next(dict(c, name_or_role=c["name_or_role"] + " (kept from v4)") for c in V4["comps"] if "quay" in c["name_or_role"])]
landmark = next(b for b in T.B if b["role"] == "landmark")
layout = {
    "town": "Perys", "version": "v5 Kernel K5 (PROPOSED)",
    "frame": V4["frame"], "fixed_points": V4["fixed_points"],
    "town_ground": {"polygon": [[round(x, 1), round(y, 1)] for x, y in (twn if twn.geom_type == "Polygon" else max(twn.geoms, key=lambda g: g.area)).exterior.coords],
                    "area_m2": round(twn.area)},
    "streets": streets_out,
    "buildings": [{k: v for k, v in b.items()} for b in T.B],
    "square": {"polygon": [[round(x, 2), round(y, 2)] for x, y in SQ.exterior.coords], "landmark_building_id": landmark["id"],
               "level_z_m": {"upper_terrace": SQ_UP, "lower_terrace": SQ_LO}, "open_side": "north-east, toward the sea (a terrace edge)"},
    "walls": [{"model_id": w["model_id"], "points": w["points"]} for w in WALLS],
    "comps": comps,
    "notes": ["PROPOSED by Kernel K5. Every number in checks.json is measured by tools/perys_v5.py on height_perys_natural_1m.npy.",
              "Blocks: buildings with the same pad_group share one flat pad at the street level of the block's middle door.",
              "The harbour road HR is v4's, unchanged; its grade is reported, not designed by us.",
              "Lamps are yours (not placed)."],
}
json.dump(layout, open(OUT + "/perys_layout.json", "w"), indent=1)
json.dump(CHK, open(OUT + "/checks.json", "w"), indent=1)
print(json.dumps({k: CHK[k] for k in ("counts", "pad_cut_fill_m", "overlaps", "model_share", "door_check", "blocks", "town_ground_m2", "building_to_street_area", "walls", "square")}, indent=0)[:3500])
print({k: (v["max_grade_pct"], v["max_cut_m"], v["max_fill_m"]) for k, v in gr.items()})
print(CHK["straight_runs_m"])

# ------------------------------------------------------------------ plan PNG
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon as MP, Patch
from matplotlib.lines import Line2D
FAMC = {"naboo_dome": "#e9c98f", "white_or_pale_house": "#f7f5ef", "scifi": "#6c7fa3", "industrial": "#9aa3a8"}

def draw(ax, xlim, ylim, label_ids=False):
    xs = np.arange(X0, X0 + H.shape[1]); ys = np.arange(Y0, Y0 + H.shape[0])
    ax.contourf(xs, ys, H, levels=np.arange(-20, 120, 2), cmap="YlOrBr", alpha=0.35)
    ax.contour(xs, ys, H, levels=np.arange(0, 120, 2), colors="#8a7a60", linewidths=0.3)
    ax.contour(xs, ys, H, levels=np.arange(0, 120, 10), colors="#5a4a30", linewidths=0.8)
    ax.contour(xs, ys, H, levels=[0], colors="#1f5f8b", linewidths=2)
    for k, st in STREETS.items():
        fc = {"main": "#d8d2c4", "lane": "#e6dfcf", "path": "#efe9dc"}[st["cls"]]
        ax.add_patch(MP(np.array(st["rib"].exterior.coords), fc=fc, ec="#6b6252", lw=0.6, ls="-" if st["cls"] != "path" else ":"))
    ax.add_patch(MP(np.array(SQ.exterior.coords), fc="#f3e6c4", ec="#7b2cbf", lw=1.6, hatch=".."))
    ax.add_patch(MP(np.array(QUAY.exterior.coords), fc="#d9e8f0", ec="#1f5f8b", lw=1.2))
    for c in comps:
        w_, d_ = c["footprint_m"]; a = math.radians(c["yaw_deg"])
        ex = np.array([math.cos(a), -math.sin(a)]); ez = np.array([math.sin(a), math.cos(a)]); cc = np.array([c["x"], c["y"]])
        ax.add_patch(MP(np.array([cc + w_ / 2 * ex + d_ / 2 * ez, cc - w_ / 2 * ex + d_ / 2 * ez, cc - w_ / 2 * ex - d_ / 2 * ez, cc + w_ / 2 * ex - d_ / 2 * ez]),
                        fc="none", ec="#d63384", lw=1.4, ls="--"))
    for wl in WALLS:
        p = np.array(wl["points"]); ax.plot(p[:, 0], p[:, 1], color="#5a1f12", lw=3)
    for b, q in zip(T.B, T.polys):
        m = CAT[b["model_id"]]
        ax.add_patch(MP(np.array(q.exterior.coords), fc=FAMC[m["family"]], ec="#d7263d" if b["garrison"] else "#222",
                        lw=2.0 if b["garrison"] else 0.6))
        a = math.radians(b["door_bearing_deg"]); half = (m["depth_m"] if b["door_side"] in ("front", "back") else m["width_m"]) / 2
        dx, dy = b["x"] + half * math.sin(a), b["y"] + half * math.cos(a)
        ax.plot([dx, dx + 2.2 * math.sin(a)], [dy, dy + 2.2 * math.cos(a)], color="#0b6e4f", lw=1.6)
        if m["tall"]: ax.plot(b["x"], b["y"], marker="^", ms=7, color="k")
        if label_ids: ax.text(b["x"], b["y"], b["id"][1:], fontsize=5, ha="center", va="center", clip_on=True)
    lmb = next(b for b in T.B if b["role"] == "landmark"); ax.plot(lmb["x"], lmb["y"], "*", ms=18, color="#ffd23f", mec="k")
    ax.set_xlim(*xlim); ax.set_ylim(*ylim); ax.set_aspect("equal")
    ax.plot(5087.3, 3408.5, "o", ms=10, mfc="none", mec="#d7263d", mew=2)

fig = plt.figure(figsize=(18, 13), dpi=110)
ax = fig.add_axes([0.04, 0.06, 0.62, 0.86])
xl = (5050, 5450); yl = (3150, 3500)
draw(ax, xl, yl, label_ids=True)
ax.plot([xl[1] - 120, xl[1] - 20], [yl[0] + 12, yl[0] + 12], "k-", lw=4); ax.text(xl[1] - 70, yl[0] + 17, "100 m", ha="center", fontsize=10, weight="bold")
ax.annotate("", xy=(xl[1] - 15, yl[1] - 10), xytext=(xl[1] - 15, yl[1] - 45), arrowprops=dict(facecolor="k", width=4, headwidth=12))
ax.text(xl[1] - 15, yl[1] - 58, "N", ha="center", fontsize=12, weight="bold")
ax.text(5092, 3414, "NW road port (59.4 m)", fontsize=9, color="#d7263d", weight="bold")
ax.set_xlabel("x east (m, map frame)"); ax.set_ylabel("y north (m, map frame)")
ax2 = fig.add_axes([0.69, 0.62, 0.30, 0.30])
draw(ax2, (5590, 5750), (3500, 3620)); ax2.set_title("quay group (same frame; apron 2.2 m)", fontsize=10)
ax3 = fig.add_axes([0.69, 0.27, 0.30, 0.32])
cx, cy = SQ.centroid.coords[0]
draw(ax3, (cx - 70, cx + 70), (cy - 55, cy + 55), label_ids=True); ax3.set_title(f"the square: upper terrace {SQ_UP} m, lower {SQ_LO} m; landmark and ring", fontsize=10)
lax = fig.add_axes([0.69, 0.02, 0.30, 0.24]); lax.axis("off")
hand = [Patch(fc=FAMC[f], ec="#222", label=f.replace("_", " ")) for f in FAMC] + [
    Patch(fc="none", ec="#d7263d", lw=2, label="garrison (enterable)"), Line2D([], [], color="#0b6e4f", lw=2, label="door (tick points out of the door)"),
    Line2D([], [], ls="", marker="^", color="k", label="tall piece (> 14 m)"), Line2D([], [], ls="", marker="*", ms=14, color="#ffd23f", mec="k", label="landmark (ND07)"),
    Patch(fc="#f3e6c4", ec="#7b2cbf", hatch="..", label="square (open side to the sea)"), Patch(fc="none", ec="#d63384", ls="--", label="comp footprint"),
    Line2D([], [], color="#5a1f12", lw=3, label="retaining wall (WL01 runs)"), Patch(fc="#d8d2c4", ec="#6b6252", label="main street / lane / path")]
ax.legend(handles=hand, loc="lower left", fontsize=8.5, framealpha=0.92)
c = CHK
lax.text(0, 0.05, (f"MEASURED on the natural ground:\nbuildings {c['counts']['buildings']}, garrison {c['counts']['garrison']} (enterable {c['counts']['enterable']})\n"
                  f"pad cut/fill: median {c['pad_cut_fill_m']['median']} m, max {c['pad_cut_fill_m']['max']} m\n"
                  f"overlaps: {c['overlaps']['building_pairs']} pairs, {c['overlaps']['building_vs_street']} into streets\n"
                  f"largest model share {c['model_share']['largest'][1]} % ({c['model_share']['largest'][0]})\n"
                  f"doors off a street/square/quay: {c['door_check']['fail']}\n"
                  f"main street max grade {c['street_grades']['M']['max_grade_pct']} %"), fontsize=9.5, family="monospace", va="bottom")
fig.text(0.04, 0.955, "Perys v5 (Kernel K5, PROPOSED): real catalogue models on block pads, natural ground", fontsize=15, weight="bold")
fig.savefig(OUT + "/perys_plan.png", dpi=110); plt.close(fig)
