"""Grader-backed placement (11 Nov). A Town whose add() seats a building only if the 11 Nov town grader would seat it:
the grader's own street claims, square, pad rule (footprint + 1.5 m, rear 0.4 m for street rows), overlap, ribbon,
clash, cut/fill and 31 degree bank tests are called directly from grader/town_grader.py. All five tests are pairwise
(overlap, clash, bank) or per building (ribbon, cut/fill, window), so a set that passes them one by one in our order
also passes them in the grader's order."""
import os, sys, json, collections
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "grader"))
import town_grader as TG
from town_grid import Town

GRID5 = os.environ.get("GRID5_DIR", "/tmp/claude-0/-home-user-KaidDrexlmods/68d91108-852d-5f8a-b84e-f7c6d8824e63/scratchpad/handoff_11nov_grader/heights_5m")
SITES = {"perys": ("perys_natural_5m.npy", 4730, 2800), "sound_head": ("sound_head_natural_5m.npy", 2050, 10050),
         "causeway_foot": ("causeway_foot_natural_5m.npy", 13600, 7750), "kastro_quay": ("kastro_quay_natural_5m.npy", 3700, 16270),
         "lantern_quay": ("lantern_quay_natural_5m.npy", 6900, 16150), "kamar_village": ("kamar_village_natural_5m.npy", 16350, 10950),
         "oyra": ("oyra_natural_5m.npy", 11420, 12000)}
FIXED = {"perys": os.path.join(HERE, "..", "grader", "perys_fixed.json")}


def windows_for(site):
    f, x0, y0 = SITES[site]
    return [(np.load(os.path.join(GRID5, f)), x0, y0, 5)]


def streets_json(T):
    """the streets exactly as the layout file writes them (the grader must see the same lines and levels)"""
    out = []
    for k, st in T.streets.items():
        pts = st["pts"][::2] + [st["pts"][-1]]
        zs = list(st["z"][::2]) + [st["z"][-1]]
        out.append({"id": k, "name": st.get("name", k), "class": st.get("out_cls", st["cls"]), "width_m": st["w"],
                    "points": [[round(x, 2), round(y, 2)] for x, y in pts], "points_z": [round(float(v), 2) for v in zs],
                    "segments": [dict(s0_m=round(g["s0"], 1), s1_m=round(g["s1"], 1), level_m=g["z"]) for g in st["segments"]] if st["cls"] != "path" else None})
    return out


def ground_from(LAY, windows, fixed=None):
    """the first half of town_grader.grade(): the grid, the streets and the square, fixed in the grader's order"""
    fixed = fixed or {}
    T = TG.Town(); T.lay = LAY
    T.streets, T.st_station, T.pads, T.pad_clash = [], {}, {}, {}
    over = {s["id"]: s for s in fixed.get("streets", [])}
    raw = [over.get(s["id"], s) for s in LAY["streets"]] + [s for s in fixed.get("streets", []) if s["id"] not in {x["id"] for x in LAY["streets"]}]
    T.fixed_pads = {p["id"]: p for p in fixed.get("pads", [])}
    xs = [p[0] for s in LAY["streets"] for p in s["points"]] + LAY.get("_extra_x", [])
    ys = [p[1] for s in LAY["streets"] for p in s["points"]] + LAY.get("_extra_y", [])
    if "window" in fixed:
        i0, i1, j0, j1 = fixed["window"]
    else:
        i0, i1 = int(min(xs) // 5) - TG.MARGIN_CELLS - 8, int(max(xs) // 5) + TG.MARGIN_CELLS + 9
        j0, j1 = int(min(ys) // 5) - TG.MARGIN_CELLS - 8, int(max(ys) // 5) + TG.MARGIN_CELLS + 9
    G = T.G = TG.Grid(i0, i1, j0, j1, windows)
    sts = [TG.street_from_json(s) for s in raw]; byid = {s.name: s for s in sts}
    sq = LAY.get("square") or {}
    has_sq = bool(sq.get("polygon")) and sq.get("level_z_m") is not None
    T.sq = np.array(sq["polygon"], float) if has_sq else None
    T.sqz = float(sq["level_z_m"]) if has_sq else None
    order = fixed.get("order")
    key = lambda s: TG.CLS_ORDER.get(s.cls, 4)
    if order is None:
        steps = [("street", s.name) for s in sorted(sts, key=key) if s.cls in ("main", "lane")] + [("square", None)] + \
                [("street", s.name) for s in sorted(sts, key=key) if s.cls not in ("main", "lane")] + [("pad", k) for k in T.fixed_pads]
    else:
        named = {x[1] for x in order if x[0] == "street"}; steps = []
        for kind, k in (tuple(x) for x in order):
            if kind == "street" and k not in byid: continue
            if kind == "pad" and k not in T.fixed_pads: continue
            if kind == "square":
                steps += [("street", s.name) for s in sorted(sts, key=key) if s.cls in ("main", "lane") and s.name not in named]
                steps.append(("square", None))
                steps += [("street", s.name) for s in sorted(sts, key=key) if s.cls not in ("main", "lane") and s.name not in named]
            else:
                steps.append((kind, k))
        if ("square", None) not in steps:
            steps += [("street", s.name) for s in sts if s.name not in named]
    for kind, k in steps:
        if kind == "street": TG.add_street(T, byid[k])
        elif kind == "square" and has_sq: TG.add_level_pad(T, "square", T.sq, T.sqz, "SQUARE", "square")
        elif kind == "pad":
            p = T.fixed_pads[k]; TG.add_level_pad(T, k, np.array(p["polygon"], float), float(p["level_z_m"]), k, "fixed pad")
    T.SN = {s.name: s for s in T.streets}
    T.acc = []
    return T


class GTown(Town):
    """Town whose add() asks the grader first. Call init_grader() after the streets (and the square) exist."""
    SETBACKS = (0.0, 0.4, 0.9, 1.5, 2.2, 3.0)

    def __init__(self, cfg, cat, ground, seed=11):
        super().__init__(cfg, cat, ground, seed)
        self.GT = None; self.refused = collections.Counter(); self.site = cfg["site"]

    def ok(self, poly, pz, own_street, yaw, cut_lim):          # all real tests are the grader's, in add()
        return True

    def init_grader(self):
        LAY = {"streets": streets_json(self)}
        if getattr(self, "SQ", None) is not None and getattr(self, "square_z", None) is not None:
            LAY["square"] = {"polygon": [list(map(float, p)) for p in list(self.SQ.exterior.coords)[:-1]], "level_z_m": float(self.square_z)}
        fx = json.load(open(FIXED[self.site])) if self.site in FIXED else None
        self.fixed = fx
        self.GT = ground_from(LAY, windows_for(self.site), fx)
        self.LAY_streets, self.LAY_square = LAY["streets"], LAY.get("square")

    def test(self, b):
        T = self.GT
        if T is None: self.init_grader(); T = self.GT
        o = TG.bobj(T, b, TG.REAR_DEFAULT)
        for x in T.acc:
            if abs(x["c"][0] - o["c"][0]) < 45 and abs(x["c"][1] - o["c"][1]) < 45 and TG.sat_pen(o["fp"], x["fp"]) > 0:
                return None, "overlap"
        for st in T.streets:
            lim = st.width / 2 + (0.2 if st.name == o["street"] else 1.0)
            if TG.seg_poly_dist(st, o["fp"]) < lim:
                return None, "ribbon"
        ok, why = T.G.feasible(o["V"], o["pad"])
        if not ok:
            return None, why.split(" ")[0] + (" bank" if why.startswith("bank") else "")
        return o, "ok"

    def add(self, mid, x, y, yaw, door, pz, street, role, pg):
        b = dict(id=f"B{len(self.B) + 1:03d}", model_id=mid, x=round(x, 2), y=round(y, 2), yaw_deg=round(yaw % 360, 2), door_side=door,
                 pad_z_m=round(pz, 2), street=street, role=role, pad_group=pg)
        o, why = self.test(b)
        if o is None:
            self.refused[why] += 1
            if role == "landmark" and not getattr(self, "_near", False):
                self._near = True
                try: return self.add_near(mid, x, y, yaw, door, pz, street, role, pg)
                finally: self._near = False
            return None
        self.GT.G.commit(o["V"], o["pad"], o["kid"], "pad"); self.GT.acc.append(o)
        return super().add(mid, x, y, yaw, door, pz, street, role, pg)

    def add_near(self, mid, x, y, yaw, door, pz, street, role, pg, r=6.0):
        """try the spot and then nearby spots (for landmarks and single pieces)"""
        for d in [k * 0.5 for k in range(1, int(r * 2) + 1)]:
            for ang in range(0, 360, 45):
                dx, dy = d * np.cos(np.radians(ang)), d * np.sin(np.radians(ang))
                b = self.add(mid, x + dx, y + dy, yaw, door, pz, street, role, pg)
                if b is not None: return b
        return None

    def seat_comp(self, c, tries=8.0):
        """a comp with a footprint seats like a pad (after the buildings), clear of buildings and carriageways; else it stays a role only"""
        G = self.GT.G
        w, d = c["footprint_m"][:2]; ex, ez = TG.axes(float(c.get("yaw_deg", 0.0)))
        for dd in [0.0] + [k * 0.5 for k in range(1, int(tries * 2) + 1)]:
            for ang in ((0,) if dd == 0 else range(0, 360, 30)):
                P0 = np.array([c["x"] + dd * np.cos(np.radians(ang)), c["y"] + dd * np.sin(np.radians(ang))])
                R = np.array([P0 + sx * w / 2 * ex + sz * d / 2 * ez for sx, sz in ((-1, -1), (1, -1), (1, 1), (-1, 1))])
                ok, why = G.feasible(G.cells_of_poly(R), float(c["pad_z_m"]))
                if not ok: continue
                if any(TG.sat_pen(R, b["fp"]) > 0 for b in self.GT.acc): continue
                if any(TG.seg_poly_dist(st, R) < st.width / 2 for st in self.GT.streets): continue
                return dict(c, x=round(float(P0[0]), 1), y=round(float(P0[1]), 1))
        cc = {k: v for k, v in c.items() if k not in ("footprint_m", "pad_z_m")}
        cc["name_or_role"] = cc.get("name_or_role", "comp") + " (no level pad found here that the grader seats: place it by hand, or leave it out)"
        return cc


def square_site(T, sid, length, depth, near=None, side="down", gap=1.0, margin=11.0):
    """a square on one level segment of street sid, clear of its ramps: the segment must run margin m past both ends.
    side: 'down' / 'up' (from the street, toward lower / higher ground) or +1 / -1. Returns (corners, level, centre, t, n)."""
    from shapely.geometry import Point
    st = T.streets[sid]; L = st["line"]; best = None
    s_near = L.project(Point(*near)) if near is not None else None
    for sg in st["segments"]:
        if sg["s1"] - sg["s0"] < length + 2 * margin: continue
        lo, hi = sg["s0"] + margin + length / 2, sg["s1"] - margin - length / 2
        s = (lo + hi) / 2 if s_near is None else min(max(s_near, lo), hi)
        score = 0 if s_near is None else abs(s - s_near)
        if best is None or score < best[0]: best = (score, s, sg["z"])
    if best is None: return None
    _, s, z = best
    p = np.array(L.interpolate(s).coords[0]); q = np.array(L.interpolate(min(s + 1, L.length)).coords[0]); t = (q - p) / np.linalg.norm(q - p)
    n = np.array([-t[1], t[0]])
    if side in ("down", "up"):
        down = T.G.z(*(p + n * 15)) < T.G.z(*(p - n * 15))
        if (side == "down") != down: n = -n
    elif side == -1: n = -n
    c = p + n * (st["w"] / 2 + gap + depth / 2)
    SQ = [tuple(np.round(c + a * length / 2 * t + b * depth / 2 * n, 1)) for a, b in ((-1, -1), (1, -1), (1, 1), (-1, 1))]
    return SQ, float(z), c, t, n


def standard_build(T, sq_street, length, depth, near, side, landmark, ring_pool, rows, ring_ends=True, comps=(), open_side="", quay=None, lm_along=0.3):
    """the shared K6 v2 build: a one-level square on a level stretch of sq_street, the landmark on it (door toward the street),
    a ring on the square's two ends, then the rows; comps as (name, along, across, footprint) in square axes."""
    from shapely.geometry import Polygon
    got = square_site(T, sq_street, length, depth, near=near, side=side)
    if got is None:
        SQ = None; T.SQ = None; T.square_z = None
    else:
        SQ, sqz, c, t, n = got
        T.SQ = Polygon(SQ); T.square_z = sqz
        T.draw_polys = [(T.SQ, "#f3e6c4", "#7b2cbf", "square")] + list(getattr(T, "draw_polys", []))[1:]
    T.init_grader()
    if SQ is not None:
        T.pad += 1; T._pg = f"P{T.pad:03d}"
        mid, door = landmark
        lm = c + lm_along * length / 2 * t
        yaw_door = (np.degrees(np.arctan2(-n[0], -n[1]))) % 360          # bearing from the square toward the street
        yaw = T.yaw_for(yaw_door, door)
        T.add(mid, lm[0], lm[1], yaw, door, sqz, "SQ", "landmark", T._pg)
        if ring_ends:
            for edge in ([SQ[3], SQ[0]], [SQ[1], SQ[2]]):
                T.pack_edge(list(edge), c, sqz, ring_pool, "square", allow_tall=False, cut_lim=4.0)
    if quay: quay(T)
    for k, pool, role, sci, md in rows:
        for sd in T.row_sides(T.streets[k]):
            T.pack_row(k, sd, pool, role, max_depth=md, cut_lim=4.0, sci_first=sci)
    T.comps = []
    if SQ is not None:
        for name, a, b, fp in comps:
            p = c + a * t + b * n
            T.comps.append(dict(name_or_role=name, x=round(float(p[0]), 1), y=round(float(p[1]), 1), yaw_deg=round(float(yaw_door), 1), footprint_m=list(fp), pad_z_m=sqz))
    lmk = [b["id"] for b in T.B if b["role"] == "landmark"]
    T.square_out = None if SQ is None else {"polygon": [list(p) for p in SQ], "level_z_m": sqz, "landmark_building_id": lmk[0] if lmk else None, "open_side": open_side}
