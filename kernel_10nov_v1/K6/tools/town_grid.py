"""Grid-aware town engine for Kernel K5b / K6 (PROPOSED layouts).

Follows the 10 Nov late note: the terrain is a 5 m grid; a pad sets every grid
point under its footprint + 1.5 m. So:
  - a terrace (one street segment and the rows on both its sides) is ONE level;
  - pads at different levels keep 14 m (17 m at 45 degrees to the grid) apart, and
    never claim the same grid point;
  - streets are level along a segment's frontage and drop only across 14-17 m gaps
    (main <= 12 % on the drop, <= 8 % average; lanes <= 19 %);
  - lanes start / end at the level of the street they join;
  - a square is one level; corner houses keep 2 m clear of cross streets.
Hand-made per town (config): street lines, the square, the landmark, the quay.
"""
import json, math, collections
import numpy as np
from shapely.geometry import Polygon, LineString, Point, box
from shapely.ops import unary_union
from shapely import contains_xy

GRID = 5.0
TWIN_EXTRA = [("WH11", "WH24")]                 # one house in two colours (note, 10 Nov late)
DOOR_OVERRIDE = {"WH24": "left"}                 # its entrances are on the end stairs


class Ground:
    def __init__(self, path, x0, y0):
        self.H = np.load(path).astype(np.float64); self.x0, self.y0 = float(x0), float(y0)

    def z(self, x, y):
        return float(self.zv(np.array([x]), np.array([y]))[0])

    def zv(self, xs, ys):
        H = self.H; fx = np.clip(xs - self.x0, 0, H.shape[1] - 1.001); fy = np.clip(ys - self.y0, 0, H.shape[0] - 1.001)
        c0 = np.floor(fx).astype(int); r0 = np.floor(fy).astype(int); tx, ty = fx - c0, fy - r0
        a = H[r0, c0] * (1 - tx) + H[r0, c0 + 1] * tx; b = H[r0 + 1, c0] * (1 - tx) + H[r0 + 1, c0 + 1] * tx
        return a * (1 - ty) + b * ty

    def cutfill(self, poly, pz, step=1.0):
        g = poly.buffer(1.5, join_style=2); x0, y0, x1, y1 = g.bounds
        xs, ys = np.meshgrid(np.arange(math.floor(x0), math.ceil(x1) + 1, step), np.arange(math.floor(y0), math.ceil(y1) + 1, step))
        m = contains_xy(g, xs, ys)
        if not m.any(): return 0.0, 0.0
        v = self.zv(xs[m], ys[m]); return float(max(v.max() - pz, 0)), float(max(pz - v.min(), 0))


def chaikin(p, it=3):
    p = np.array(p, float)
    for _ in range(it):
        q = [p[0]]
        for u, v in zip(p[:-1], p[1:]): q += [0.75 * u + 0.25 * v, 0.25 * u + 0.75 * v]
        q.append(p[-1]); p = np.array(q)
    return p


def resample(line, step=2.0):
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


def grid_points(poly):
    x0, y0, x1, y1 = poly.bounds
    xs, ys = np.meshgrid(np.arange(math.ceil(x0 / GRID) * GRID, x1 + 0.01, GRID), np.arange(math.ceil(y0 / GRID) * GRID, y1 + 0.01, GRID))
    m = contains_xy(poly, xs, ys); return list(zip(np.round(xs[m], 1), np.round(ys[m], 1)))


def req_sep(yaw):
    a = yaw % 90.0; a = min(a, 90.0 - a)                 # 0 = lined up with the grid, 45 = diagonal
    return 14.0 + 3.0 * (a / 45.0)


class Town:
    def __init__(self, cfg, cat, ground, seed=11):
        self.cfg, self.G, self.rng = cfg, ground, np.random.default_rng(seed)
        self.CAT = {k: dict(v) for k, v in cat.items()}
        for k, d in DOOR_OVERRIDE.items():
            if k in self.CAT: self.CAT[k]["door_side"] = d
        self.twin = {}
        for mid, m in self.CAT.items(): self.twin[mid] = f"{m['family']}|{m['width_m']}|{m['depth_m']}"
        for grp in TWIN_EXTRA:
            for mid in grp: self.twin[mid] = "+".join(grp)
        self.B, self.P = [], []                 # buildings, footprint polygons
        self.claims = {}                        # grid point -> level
        self.count, self.tcount = collections.Counter(), collections.Counter()
        self.pad = 0; self.log = collections.Counter()
        self.streets = {}

    # ------------------------------------------------------------------ streets
    def build_streets(self):
        cfg = self.cfg
        for sd in cfg["streets"]:
            line = LineString(chaikin(sd["pts"], 3)) if sd.get("smooth", True) else LineString(sd["pts"])
            pts = resample(line, 2.0); line = LineString(pts)
            s = np.array([0.0] + list(np.cumsum([math.dist(a, b) for a, b in zip(pts[:-1], pts[1:])])))
            self.streets[sd["id"]] = dict(sd, line=line, pts=pts, s=s, rib=line.buffer(sd["w"] / 2, cap_style=2))
        order = [sd["id"] for sd in cfg["streets"]]
        for k in order: self._levels(self.streets[k])
        self.RIBS = unary_union([v["rib"] for v in self.streets.values()])
        self.extra_pads = []
        for k, st in self.streets.items():                 # level street segments are pads too (their grid points are set flat)
            if st["cls"] == "path": continue
            for sg in st["segments"]:
                from shapely.ops import substring
                piece = substring(st["line"], sg["s0"], sg["s1"]).buffer(st["w"] / 2 + 0.5, cap_style=2)
                self.extra_pads.append((piece, sg["z"]))
                for gp in grid_points(piece):
                    if gp not in self.claims: self.claims[gp] = sg["z"]

    def _levels(self, st):
        """Split the street into level segments and drop gaps; segment level = mean ground of its terrace band."""
        if st["cls"] == "path":                             # stair paths follow the ground; no rows, no pads
            nat = self.G.zv(np.array([p[0] for p in st["pts"]]), np.array([p[1] for p in st["pts"]]))
            st["segments"] = [dict(s0=0.0, s1=st["line"].length, z=float(nat.mean()))]; st["z"] = nat; return
        L = st["line"].length; seg_rng = st.get("seg", (30, 48)); gap = st.get("gap", 16.0)
        g_drop = st.get("drop_grade", 0.12 if st["cls"] == "main" else 0.19)
        cuts, s = [], 0.0
        if st.get("ramp"):                                      # a link lane: short level landings at both ends, one graded ramp between
            cuts = [[0.0, 3.0], [L - 3.0, L]]
        elif st.get("gaps_at"):                                   # level changes only where cross lanes meet the street
            ss = sorted(st["line"].project(Point(*p)) for p in st["gaps_at"])
            edges = [0.0]
            for v in ss:
                if gap / 2 + 6 < v < L - gap / 2 - 6: edges += [v - gap / 2, v + gap / 2]
            edges.append(L)
            cuts = [[edges[i], edges[i + 1]] for i in range(0, len(edges), 2)]
        else:
            while s < L - 8:
                e = min(L, s + self.rng.uniform(*seg_rng))
                if L - e < 14: e = L
                cuts.append([s, e]); s = e + gap
        # pins: start / end levels from a fixed point or a parent street
        def band_level(a, b):
            ss = np.linspace(a, b, max(3, int((b - a) / 3)))
            vals = []
            for v in ss:
                p = np.array(st["line"].interpolate(v).coords[0]); q = np.array(st["line"].interpolate(min(v + 1, L)).coords[0])
                t = (q - p) / (np.linalg.norm(q - p) + 1e-9); n = np.array([-t[1], t[0]])
                sides = self.row_sides(st, p, n)
                if len(sides) != 1: offs = (-st["w"] / 2 - 6, 0, st["w"] / 2 + 6)
                else: offs = tuple(sides[0] * (st["w"] / 2 + d) for d in st.get("band", (2.0, 5.0, 8.0)))   # street + near half of the row
                for off in offs: vals.append(self.G.z(*(p + n * off)))
            return float(np.mean(vals))
        if st.get("adaptive"):                                  # end a level segment where its frontage band leaves +-tol of one level
            tol = st.get("tol", 1.5); maxlen = st.get("maxlen", 46.0); minlen = st.get("minlen", 12.0); cuts, s = [], 0.0
            def bvals(a, b):
                return [band_level(v, v) for v in np.arange(a, b + 0.01, 2.0)]
            prev = None                                          # (end of previous segment, its level)
            while s < L - 8:
                for _ in range(4):                               # move the start on until the drop from the last level fits the gap
                    e = min(L, s + minlen); vals = bvals(s, e)
                    while e + 2 <= L and e - s < maxlen:
                        nv = vals + bvals(e + 2, e + 2)
                        if max(nv) - min(nv) > 2 * tol: break
                        vals = nv; e += 2
                    if L - e < 14: e = L
                    lv = round(float(np.mean(vals)) * 4) / 4
                    if prev is None or abs(lv - prev[1]) / g_drop <= s - prev[0] + 0.01: break
                    s = prev[0] + abs(lv - prev[1]) / g_drop
                    if s >= L - 8: break
                if s >= L - 8: break
                cuts.append([s, e]); prev = (e, lv); s = e + gap
        lev = [round(band_level(a, b) * 4) / 4 for a, b in cuts]
        pin0 = self._pin(st, "start"); pin1 = self._pin(st, "end")
        if pin0 is not None: lev[0] = pin0
        if pin1 is not None: lev[-1] = pin1
        # merge segments whose levels are within 0.3 m (no gap needed)
        mc, ml = [cuts[0]], [lev[0]]
        for c, l in zip(cuts[1:], lev[1:]):
            if abs(l - ml[-1]) < 0.3 and not (pin1 is not None and c is cuts[-1]):
                mc[-1][1] = c[1]
            else:
                mc.append(c); ml.append(l)
        # widen a gap if its drop is too steep for the street class
        for i in range(1, len(mc)):
            need = abs(ml[i] - ml[i - 1]) / g_drop; have = mc[i][0] - mc[i - 1][1]
            if need > have:
                shift = need - have; mc[i][0] = min(mc[i][0] + shift, mc[i][1] - 6)
        st["segments"] = [dict(s0=a, s1=b, z=z) for (a, b), z in zip(mc, ml)]
        zs = np.empty(len(st["s"]))
        for i, v in enumerate(st["s"]):
            zs[i] = self._z_at(st, v)
        st["z"] = zs

    def row_sides(self, st, p=None, n=None):
        """Which side(s) of the street carry a row: 'both', 'up' (uphill side), 'down', or +1 / -1."""
        mode = st.get("rows", "both")
        if mode == "none": return []
        if mode == "both": return [1, -1]
        if mode in (1, -1): return [mode]
        if p is None:
            p = np.array(st["line"].interpolate(0.5, normalized=True).coords[0]); q = np.array(st["line"].interpolate(0.52, normalized=True).coords[0])
            t = (q - p) / (np.linalg.norm(q - p) + 1e-9); n = np.array([-t[1], t[0]])
        up = 1 if self.G.z(*(p + n * 12)) > self.G.z(*(p - n * 12)) else -1
        return [up] if mode == "up" else [-up]

    def _pin(self, st, which):
        p = st.get("pin_" + which)
        if p is None: return None
        if isinstance(p, (int, float)): return float(p)
        par = self.streets[p]; pt = st["line"].interpolate(0 if which == "start" else st["line"].length)
        return self._z_at(par, par["line"].project(pt))

    def _z_at(self, st, v):
        if st["cls"] == "path": return float(np.interp(v, st["s"], st["z"]))
        seg = st["segments"]
        for sg in seg:
            if sg["s0"] <= v <= sg["s1"]: return sg["z"]
        if v < seg[0]["s0"]: return seg[0]["z"]
        if v > seg[-1]["s1"]: return seg[-1]["z"]
        for a, b in zip(seg[:-1], seg[1:]):
            if a["s1"] < v < b["s0"]:
                t = (v - a["s1"]) / (b["s0"] - a["s1"]); return a["z"] + t * (b["z"] - a["z"])
        return seg[-1]["z"]

    def zst(self, k, x, y):
        st = self.streets[k]; return self._z_at(st, st["line"].project(Point(x, y)))

    # ------------------------------------------------------------------ buildings
    def dims(self, mid, door):
        m = self.CAT[mid]; return (m["width_m"], m["depth_m"]) if door in ("front", "back") else (m["depth_m"], m["width_m"])

    @staticmethod
    def yaw_for(bearing, door):
        return (bearing - {"front": 0, "right": 90, "back": 180, "left": 270}[door]) % 360

    def foot(self, mid, x, y, yaw):
        m = self.CAT[mid]; a = math.radians(yaw)
        ex = np.array([math.cos(a), -math.sin(a)]); ez = np.array([math.sin(a), math.cos(a)]); c = np.array([x, y])
        w, d = m["width_m"] / 2, m["depth_m"] / 2
        return Polygon([c + w * ex + d * ez, c - w * ex + d * ez, c - w * ex - d * ez, c + w * ex - d * ez])

    def allowed(self, mid):
        n = self.cfg["target_n"]
        return self.count[mid] + 1 <= 0.12 * n and self.tcount[self.twin[mid]] + 1 <= 0.12 * n

    def claim_ok(self, poly, pz):
        for gp in grid_points(poly.buffer(1.5, join_style=2)):
            z = self.claims.get(gp)
            if z is not None and abs(z - pz) > 0.01: return False
        return True

    def add_claims(self, poly, pz, margin=1.5):
        for gp in grid_points(poly.buffer(margin, join_style=2)): self.claims[gp] = pz

    def ok(self, poly, pz, own_street, yaw, cut_lim):
        L = self.log
        if poly.intersection(self.RIBS).area > 0.01:
            L["street"] += 1
            for k2, st2 in self.streets.items():
                if poly.intersection(st2["rib"]).area > 0.01: L["street:" + ("own" if k2 == own_street else st2["cls"])] += 1
            return False
        for k, st in self.streets.items():
            if k != own_street and poly.distance(st["rib"]) < 2.0: L["cross-street clearance"] += 1; return False
        if self.cfg.get("square") is not None and poly.distance(self.SQ) < (0.4 if own_street == "SQ" else 2.0): L["square"] += 1; return False
        for b, q in zip(self.B, self.P):
            if abs(b["pad_z_m"] - pz) < 0.01:
                if poly.intersection(q).area > 0.001 or (poly.distance(q) < 0.3 and b["pad_group"] != self._pg): L["building"] += 1; return False
            else:
                if poly.distance(q) < max(req_sep(yaw), req_sep(b["yaw_deg"])): L["level separation"] += 1; return False
        if not self.claim_ok(poly, pz): L["grid claim"] += 1; return False
        c, f = self.G.cutfill(poly, pz)
        if max(c, f) > cut_lim: L["cut/fill"] += 1; return False
        return True

    def add(self, mid, x, y, yaw, door, pz, street, role, pg):
        poly = self.foot(mid, x, y, yaw)
        b = dict(id=f"B{len(self.B) + 1:03d}", model_id=mid, x=round(x, 2), y=round(y, 2), yaw_deg=round(yaw % 360, 2),
                 door_side=door, garrison=False, pad_group=pg, pad_z_m=round(pz, 2),
                 door_bearing_deg=round((yaw + {"front": 0, "right": 90, "back": 180, "left": 270}[door]) % 360, 1),
                 street=street, role=role)
        self.B.append(b); self.P.append(poly); self.count[mid] += 1; self.tcount[self.twin[mid]] += 1
        self.add_claims(poly, pz); return b

    def pack_row(self, k, side, pool, role, max_depth=16.0, cut_lim=2.5, sci_first=0.0, jitter=2.5):
        """One row along one side of one street, segment by segment, at the segment's level."""
        st = self.streets[k]; line, w = st["line"], st["w"]
        for sg in st["segments"]:
            s = sg["s0"] + 1.0; nb = 0; self.pad += 1; self._pg = f"P{self.pad:03d}"; jit = self.rng.uniform(-jitter, jitter)
            while s < sg["s1"] - 4:
                cands = [m for m in pool if self.allowed(m)]; self.rng.shuffle(cands)
                if sci_first and self.rng.random() < sci_first: cands.sort(key=lambda mm: 0 if self.CAT[mm]["family"] == "scifi" else 1)
                placed = False
                for mid in cands[:12]:
                    m = self.CAT[mid]; door = m["door_side"]; fw, dp = self.dims(mid, door)
                    if dp > max_depth or m["tall"] or s + fw > sg["s1"] - 1: continue
                    smid = s + fw / 2
                    q0 = np.array(line.interpolate(max(smid - 3, 0)).coords[0]); q1 = np.array(line.interpolate(min(smid + 3, line.length)).coords[0])
                    t = (q1 - q0) / (np.linalg.norm(q1 - q0) + 1e-9); a = math.radians(jit)
                    t = np.array([math.cos(a) * t[0] - math.sin(a) * t[1], math.sin(a) * t[0] + math.cos(a) * t[1]])
                    n = np.array([-t[1], t[0]]) * side
                    door_pt = np.array(line.interpolate(smid).coords[0]) + n * (w / 2 + 0.35)
                    yaw = self.yaw_for(math.degrees(math.atan2(-n[0], -n[1])) % 360, door)
                    for extra in (0.0, 0.8, 1.6, 2.4):
                        cen = door_pt + n * (extra + dp / 2); poly = self.foot(mid, cen[0], cen[1], yaw)
                        if self.ok(poly, sg["z"], k, yaw, cut_lim):
                            self.add(mid, cen[0], cen[1], yaw, door, sg["z"], k, role, self._pg); placed = True; break
                    if placed:
                        s += fw + 0.08; nb += 1
                        if nb % 4 == 0: s += self.rng.uniform(2.8, 3.8)
                        break
                if not placed: s += 1.5

    def pack_edge(self, edge_pts, outward_ref, pz, pool, role, street_id="SQ", max_depth=20.0, cut_lim=2.5, allow_tall=False):
        """Buildings along a straight edge (square side, quay strip), doors toward outward_ref's opposite (into the space)."""
        line = LineString(edge_pts); L = line.length; s = 0.5; self.pad += 1; self._pg = f"P{self.pad:03d}"
        while s < L - 3:
            cands = [m for m in pool if self.allowed(m)]; self.rng.shuffle(cands); placed = False
            for mid in cands[:12]:
                m = self.CAT[mid]; door = m["door_side"]; fw, dp = self.dims(mid, door)
                if dp > max_depth or (m["tall"] and not allow_tall) or s + fw > L + 0.5: continue
                p0 = np.array(line.interpolate(s).coords[0]); p1 = np.array(line.interpolate(min(s + fw, L)).coords[0])
                t = (p1 - p0) / (np.linalg.norm(p1 - p0) + 1e-9); n = np.array([-t[1], t[0]])
                mid_pt = p0 + t * fw / 2
                if np.dot(n, np.array(outward_ref) - mid_pt) > 0: n = -n          # n points away from the space
                yaw = self.yaw_for(math.degrees(math.atan2(-n[0], -n[1])) % 360, door)
                cen = mid_pt + n * (dp / 2 + 0.45); poly = self.foot(mid, cen[0], cen[1], yaw)
                if self.ok(poly, pz, street_id, yaw, cut_lim):
                    self.add(mid, cen[0], cen[1], yaw, door, pz, street_id, role, self._pg); s += fw + 0.08; placed = True; break
            if not placed: s += 1.5

    # ------------------------------------------------------------------ checks
    def checks(self):
        C = {}; n = len(self.B)
        cf = []
        for b, q in zip(self.B, self.P):
            c, f = self.G.cutfill(q, b["pad_z_m"]); b["cut_m"], b["fill_m"] = round(c, 2), round(f, 2); cf.append(max(c, f))
        cf = np.array(cf)
        C["pad_cut_fill_m"] = dict(median=round(float(np.median(cf)), 2), max=round(float(cf.max()), 2), n_over_2_5=int((cf > 2.5).sum()),
                                   n_over_4=int((cf > 4).sum()), near_limit=[b["id"] for b, v in zip(self.B, cf) if 2.5 < v <= 4])
        # grid rule: recount from scratch (every 5 m point under footprint + 1.5 m, plus the square and quay pads)
        claims = collections.defaultdict(set)
        for b, q in zip(self.B, self.P):
            for gp in grid_points(q.buffer(1.5, join_style=2)): claims[gp].add(round(b["pad_z_m"], 2))
        for poly, z in self.extra_pads:
            for gp in grid_points(poly): claims[gp].add(round(z, 2))
        C["grid_points_claimed_by_two_levels"] = sum(1 for v in claims.values() if len(v) > 1)
        mins = []
        for i in range(n):
            for j in range(i + 1, n):
                if abs(self.B[i]["pad_z_m"] - self.B[j]["pad_z_m"]) > 0.01:
                    mins.append((self.P[i].distance(self.P[j]), max(req_sep(self.B[i]["yaw_deg"]), req_sep(self.B[j]["yaw_deg"]))))
        C["different_level_pairs_closer_than_required"] = sum(1 for d, r in mins if d < r - 0.01)
        C["closest_different_level_pair_m"] = round(min((d for d, r in mins), default=0), 2)
        ov = 0
        for i in range(n):
            for j in range(i + 1, n):
                a, b = self.P[i], self.P[j]
                if a.intersection(b).area > 0.01 or (self.B[i]["pad_group"] != self.B[j]["pad_group"] and a.distance(b) < 0.3): ov += 1
        C["overlaps"] = dict(building_pairs=ov, building_vs_street=sum(1 for q in self.P if q.intersection(self.RIBS).area > 0.01))
        cc = 0
        for b, q in zip(self.B, self.P):
            for k, st in self.streets.items():
                if k != b["street"] and q.distance(st["rib"]) < 2.0: cc += 1
        C["corner_houses_within_2m_of_a_cross_street"] = cc
        C["straight_runs_m"] = {k: round(max_run(v["line"]), 1) for k, v in self.streets.items()}
        cnt = collections.Counter(b["model_id"] for b in self.B); tw = collections.Counter(self.twin[b["model_id"]] for b in self.B)
        C["model_share"] = dict(largest_model=[cnt.most_common(1)[0][0], round(100 * cnt.most_common(1)[0][1] / n, 1)],
                                largest_twin_group=[tw.most_common(1)[0][0], round(100 * tw.most_common(1)[0][1] / n, 1)],
                                WH11_plus_WH24_pct=round(100 * (cnt["WH11"] + cnt["WH24"]) / n, 1), distinct_models=len(cnt))
        df = []; dl = []
        for b in self.B:
            m = self.CAT[b["model_id"]]; a = math.radians(b["door_bearing_deg"])
            half = (m["depth_m"] if b["door_side"] in ("front", "back") else m["width_m"]) / 2
            p = Point(b["x"] + (half + 3) * math.sin(a), b["y"] + (half + 3) * math.cos(a))
            ok = self.RIBS.buffer(0.6).contains(p) or any(sp.buffer(0.6).contains(p) for sp, _ in self.extra_pads)
            if not ok: df.append(b["id"])
            if b["street"] in self.streets:
                d = abs(self.zst(b["street"], p.x, p.y) - b["pad_z_m"])
                if d > 0.75: dl.append((b["id"], round(d, 2)))
        C["door_check"] = dict(ok=n - len(df), fail=len(df), fail_ids=df, door_level_off_street_over_0_75m=dl)
        gr = {}
        for k, st in self.streets.items():
            z = st["z"]; s = st["s"]; nat = self.G.zv(np.array([p[0] for p in st["pts"]]), np.array([p[1] for p in st["pts"]]))
            g = np.abs(np.diff(z)) / np.maximum(np.diff(s), 1e-6)
            avg = abs(z[-1] - z[0]) / max(s[-1], 1)
            gr[k] = dict(cls=st["cls"], width_m=st["w"], length_m=round(float(s[-1])), segments=len(st["segments"]),
                         max_grade_pct=round(100 * float(g.max()), 1), average_grade_pct=round(100 * avg, 1),
                         max_cut_m=round(float((nat - z).max()), 2), max_fill_m=round(float((z - nat).max()), 2))
        C["street_grades"] = gr
        jm = []
        for k, st in self.streets.items():
            for which in ("start", "end"):
                p = st.get("pin_" + which)
                if isinstance(p, str):
                    par = self.streets[p]; pt = st["line"].interpolate(0 if which == "start" else st["line"].length)
                    jm.append((k, which, p, round(abs(self._z_at(par, par["line"].project(pt)) - st["z"][0 if which == "start" else -1]), 2)))
        C["lane_end_level_mismatch_m"] = jm
        C["counts"] = dict(buildings=n, enterable=sum(self.CAT[b["model_id"]]["enterable"] for b in self.B),
                           garrison=sum(b["garrison"] for b in self.B), pad_levels=len(set(b["pad_z_m"] for b in self.B)),
                           tall=[(b["id"], b["model_id"], b["role"]) for b in self.B if self.CAT[b["model_id"]]["tall"]],
                           by_role=dict(collections.Counter(b["role"] for b in self.B)),
                           families=dict(collections.Counter(self.CAT[b["model_id"]]["family"] for b in self.B)))
        return C

    def pick_garrison(self, lo, hi, prio):
        ent = [b for b in self.B if self.CAT[b["model_id"]]["enterable"]]
        ent.sort(key=lambda b: (prio.get(b["role"], 5), self.rng.random())); sel = []
        for b in ent:
            if len(sel) >= hi: break
            if all(math.dist((b["x"], b["y"]), (g["x"], g["y"])) > 14 for g in sel) or b["role"] in ("square", "quay"): sel.append(b)
        for b in ent:
            if len(sel) >= lo: break
            if b not in sel: sel.append(b)
        for b in sel: b["garrison"] = True
