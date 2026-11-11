"""Town-plan generator for Kernel K1 (PROPOSED plans, not game files).

Each town is HAND-DESIGNED: the coast or cliff, the bent main street, the lanes,
the square and the landmark are hand-placed in towns.py. This library only
packs building footprints along the street frontages (touching, at the street
edge, irregular widths), measures the result against the K1 rules and draws it.

Local frame: metres, origin near the town centre, x east, y north (north up).
"""
import math
import numpy as np
from shapely.geometry import LineString, Point, Polygon, box, MultiPolygon
from shapely.ops import unary_union, substring

FAMILIES = ("sci-fi", "white cube", "Naboo dome")


def smooth(pts, it=3):
    p = np.array(pts, float)
    for _ in range(it):
        q = [p[0]]
        for a, b in zip(p[:-1], p[1:]):
            q += [0.75 * a + 0.25 * b, 0.25 * a + 0.75 * b]
        q.append(p[-1])
        p = np.array(q)
    return p


def max_straight_run(line, tol=1.5, step=2.0):
    """Longest piece of the centre line that stays within `tol` m of its chord
    (MEASURED). A straight run is what the eye reads as a straight street."""
    L = line.length
    n = max(2, int(L / step))
    pts = np.array([line.interpolate(i * L / n).coords[0] for i in range(n + 1)])
    best = 0.0
    for i in range(len(pts) - 1):
        j = i + 1
        while j + 1 < len(pts):
            a, b = pts[i], pts[j + 1]
            ab = b - a
            v = pts[i:j + 2] - a
            d = np.abs(ab[0] * v[:, 1] - ab[1] * v[:, 0]) / (np.linalg.norm(ab) + 1e-9)
            if d.max() > tol:
                break
            j += 1
        best = max(best, float(np.linalg.norm(pts[j] - pts[i])))
    return best


def _frame(line, s):
    s = min(max(s, 0.01), line.length - 0.01)
    p = np.array(line.interpolate(s).coords[0])
    q = np.array(line.interpolate(min(s + 1.0, line.length)).coords[0])
    r = np.array(line.interpolate(max(s - 1.0, 0)).coords[0])
    t = q - r
    t /= np.linalg.norm(t) + 1e-9
    return p, t, np.array([-t[1], t[0]])


class Town:
    def __init__(self, spec, seed):
        self.spec = spec
        self.rng = np.random.default_rng(seed)
        self.land = spec["land"]
        self.streets = []
        for st in spec["streets"]:
            line = LineString(smooth(st["pts"], 3))
            self.streets.append(dict(st, line=line, poly=line.buffer(st["width"] / 2, cap_style=2, join_style=1)))
        self.street_union = unary_union([s["poly"] for s in self.streets])
        self.square = Polygon(smooth(spec["square"] + [spec["square"][0]], 2)).buffer(0)
        self.landmark = Polygon(spec["landmark"]["footprint"])
        apron = spec.get("sea", Polygon()).buffer(12.0 if spec.get("edge_kind") == "harbour" else 1.5)
        self.blocked = unary_union([self.street_union, self.square, apron])   # quay apron stays open
        self.buildings = []
        self.placed = Polygon()

    # ---------------------------------------------------------------- packing
    def _try_add(self, poly, info, min_area=35.0):
        if not poly.is_valid:
            poly = poly.buffer(0)
        poly = poly.intersection(self.land.buffer(-0.5))
        poly = poly.difference(self.blocked.buffer(0.15))
        if not self.placed.is_empty:
            poly = poly.difference(self.placed)
        if isinstance(poly, MultiPolygon):
            poly = max(poly.geoms, key=lambda g: g.area)
        if poly.is_empty or poly.area < min_area or not isinstance(poly, Polygon):
            return None
        if poly.area / (poly.minimum_rotated_rectangle.area + 1e-9) < 0.72:   # no slivers
            return None
        poly = poly.simplify(0.3)
        info = dict(info, poly=poly)
        self.buildings.append(info)
        self.placed = unary_union([self.placed, poly])
        return info

    def pack_frontage(self, st, side, fr=(6, 14), dp=(9, 16), back_p=0.45, gap_p=0.12):
        line, w = st["line"], st["width"]
        s = self.rng.uniform(0, 4)
        while s < line.length - 4:
            f = self.rng.uniform(*fr)
            d = self.rng.uniform(*dp)
            p0, t0, n0 = _frame(line, s)
            p1, t1, n1 = _frame(line, s + f)
            o = side * (w / 2 + 0.05)
            front0, front1 = p0 + n0 * o, p1 + n1 * o
            back0, back1 = p0 + n0 * side * (w / 2 + d), p1 + n1 * side * (w / 2 + d)
            poly = Polygon([front0, front1, back1, back0])
            b = self._try_add(poly, dict(street=st["id"], frontage=True, front_w=f))
            if b is not None and self.rng.random() < back_p:          # second building behind, touching
                d2 = self.rng.uniform(7, 12)
                bb0 = p0 + n0 * side * (w / 2 + d + d2)
                bb1 = p1 + n1 * side * (w / 2 + d + d2)
                self._try_add(Polygon([back0, back1, bb1, bb0]), dict(street=st["id"], frontage=False, front_w=None))
            s += f
            if self.rng.random() < gap_p:                              # stair passage
                s += self.rng.uniform(2.5, 4.0)

    def pack_fringe(self, n, band=(18, 55), size=(7, 11)):
        """A few detached houses on the edge (terraced plots), turned to face the street."""
        tries = 0
        added = 0
        hull = self.street_union.buffer(band[1]).difference(self.street_union.buffer(band[0]))
        minx, miny, maxx, maxy = hull.bounds
        while added < n and tries < 4000:
            tries += 1
            x, y = self.rng.uniform(minx, maxx), self.rng.uniform(miny, maxy)
            if not hull.contains(Point(x, y)):
                continue
            nearest = min(self.streets, key=lambda s: s["line"].distance(Point(x, y)))
            sp = nearest["line"].project(Point(x, y))
            _, t, _ = _frame(nearest["line"], sp)
            a, b = self.rng.uniform(*size), self.rng.uniform(*size)
            ang = math.atan2(t[1], t[0]) + self.rng.normal(0, 0.15)
            c, s_ = math.cos(ang), math.sin(ang)
            corners = [(x + c * u - s_ * v, y + s_ * u + c * v) for u, v in ((-a / 2, -b / 2), (a / 2, -b / 2), (a / 2, b / 2), (-a / 2, b / 2))]
            poly = Polygon(corners)
            if not self.placed.is_empty and poly.distance(self.placed) < 3.0:
                continue
            if self._try_add(poly, dict(street=None, frontage=False, front_w=None, detached=True), min_area=40):
                added += 1

    def pack_infill(self, reach=45.0, tries=6000, size=(8, 14)):
        """Fill the ground between streets (inside blocks) with buildings that
        touch their neighbours: this makes deep blocks and a dense core, not rows."""
        zone = self.street_union.buffer(reach).intersection(self.land.buffer(-0.5)).difference(self.blocked)
        minx, miny, maxx, maxy = zone.bounds
        sqc = self.square.centroid
        for _ in range(tries):
            x, y = self.rng.uniform(minx, maxx), self.rng.uniform(miny, maxy)
            p = Point(x, y)
            if not zone.contains(p) or (not self.placed.is_empty and self.placed.contains(p)):
                continue
            # denser near the square: accept far points less often
            if self.rng.random() < min(0.85, p.distance(sqc) / 220.0):
                continue
            nearest = min(self.streets, key=lambda st: st["line"].distance(p))
            _, t, _ = _frame(nearest["line"], nearest["line"].project(p))
            a, b = self.rng.uniform(*size), self.rng.uniform(*size)
            ang = math.atan2(t[1], t[0])
            c, s_ = math.cos(ang), math.sin(ang)
            poly = Polygon([(x + c * u - s_ * v, y + s_ * u + c * v)
                            for u, v in ((-a / 2, -b / 2), (a / 2, -b / 2), (a / 2, b / 2), (-a / 2, b / 2))])
            # infill must lean on something: touch an existing building
            if self.placed.is_empty or poly.distance(self.placed) > 0.01:
                continue
            self._try_add(poly, dict(street=None, frontage=False, front_w=None), min_area=40)

    def trim_to(self, target_max):
        """Drop the buildings farthest from the square until we are at the count:
        the town keeps a dense core and loses its outer ribbons."""
        sq = self.square
        spine = unary_union([s["line"] for s in self.streets if s["kind"] == "main" or s["id"] == "Q"])
        self.buildings.sort(key=lambda b: b["poly"].centroid.distance(spine) + 0.35 * b["poly"].centroid.distance(sq))
        self.buildings = self.buildings[:target_max]
        self.placed = unary_union([b["poly"] for b in self.buildings])

    def cut_unbuilt_lanes(self):
        """A lane with no houses on it reads as a wide empty street. Past its last
        lined frontage, a lane becomes a path out of town (kind 'road')."""
        new = []
        for st in self.streets:
            if st["kind"] not in ("lane", "main"):
                new.append(st)
                continue
            line = st["line"]
            n = max(2, int(line.length / 4))
            built = [self.placed.distance(line.interpolate(i * line.length / n)) < st["width"] / 2 + 4 for i in range(n + 1)]
            idx = [i for i, b in enumerate(built) if b]
            if not idx:
                st = dict(st, kind="road")
                new.append(st)
                continue
            a, b = idx[0] * line.length / n, idx[-1] * line.length / n
            for (s0, s1, kind, suf) in ((0, a, "road", "a"), (a, b, st["kind"], ""), (b, line.length, "road", "b")):
                if s1 - s0 < 12:
                    continue
                seg = substring(line, s0, s1)
                new.append(dict(st, id=st["id"] + suf, kind=kind, line=seg,
                                poly=seg.buffer(st["width"] / 2, cap_style=2, join_style=1)))
        self.streets = new
        self.street_union = unary_union([s["poly"] for s in self.streets])

    # ---------------------------------------------------------------- tagging
    def tag(self):
        sq = self.square
        sea = self.spec.get("sea", Polygon())
        edge = self.spec.get("edge_line")
        core_r = self.spec.get("core_r", 70)
        polys = [b["poly"] for b in self.buildings]
        # blocks = touching groups of 3+
        n = len(polys)
        parent = list(range(n))

        def find(i):
            while parent[i] != i:
                parent[i] = parent[parent[i]]
                i = parent[i]
            return i
        for i in range(n):
            for j in range(i + 1, n):
                if polys[i].distance(polys[j]) < 0.35:
                    parent[find(i)] = find(j)
        groups = {}
        for i in range(n):
            groups.setdefault(find(i), []).append(i)
        self.blocks = []
        bid = {}
        for g in groups.values():
            if len(g) >= 3:
                k = len(self.blocks) + 1
                outline = unary_union([polys[i].buffer(0.3) for i in g]).buffer(-0.3)
                if isinstance(outline, MultiPolygon):
                    outline = max(outline.geoms, key=lambda q: q.area)
                self.blocks.append(dict(id=f"B{k:02d}", members=g, outline=outline))
                for i in g:
                    bid[i] = f"B{k:02d}"
        dists = sorted(b["poly"].centroid.distance(sq) for b in self.buildings)
        core_cut = dists[int(len(dists) * self.spec.get("core_frac", 0.22))]
        core_r = core_cut
        for i, b in enumerate(self.buildings):
            c = b["poly"].centroid
            dsq = c.distance(sq)
            dsea = c.distance(sea) if not sea.is_empty else 1e9
            dedge = c.distance(edge) if edge is not None else 1e9
            b["block"] = bid.get(i)
            b["d_square"] = dsq
            b["d_sea"] = min(dsea, dedge)
            r = self.rng.random()
            if dsq <= core_cut or (self.spec.get("cis_zone") is not None and self.spec["cis_zone"].contains(c) and r < 0.45):
                fam = "sci-fi" if r < 0.8 else "Naboo dome"
            else:
                corner = b["frontage"] and b["block"] is not None and r < 0.22
                fam = "Naboo dome" if (corner or r < 0.10) else ("sci-fi" if r > 0.93 else "white cube")
            b["family"] = fam
            area = b["poly"].area
            h = self.rng.random()
            if (dsq < core_r * 0.8 and h < 0.55) or (b["d_sea"] < 25 and h < 0.35) or (area > 260 and h < 0.4):
                hc = "tall"
            elif b.get("detached") or h < 0.35:
                hc = "low"
            else:
                hc = "mid"
            b["height"] = hc
        for i, b in enumerate(self.buildings):
            b["id"] = f"H{i + 1:03d}"

    def pick_garrison(self, k, anchors):
        """Pick k buildings: tall/mid, spread out (25 m min), each covering a named anchor."""
        score = []
        for i, b in enumerate(self.buildings):
            s = {"tall": 3, "mid": 1.5, "low": 0}[b["height"]] + (2 if b["d_square"] < 40 else 0) + (1 if b["d_sea"] < 30 else 0)
            score.append(s + self.rng.random())
        chosen = []
        # one per anchor first (the building nearest each approach or feature, preferring high score)
        for name, (x, y) in anchors:
            cand = sorted(range(len(self.buildings)),
                          key=lambda i: self.buildings[i]["poly"].centroid.distance(Point(x, y)) - 6 * score[i])
            for i in cand:
                if i not in [c for c, _ in chosen] and all(self.buildings[i]["poly"].centroid.distance(self.buildings[c]["poly"].centroid) > 25 for c, _ in chosen):
                    chosen.append((i, name))
                    break
        for i in sorted(range(len(self.buildings)), key=lambda i: -score[i]):
            if len(chosen) >= k:
                break
            if i in [c for c, _ in chosen]:
                continue
            if all(self.buildings[i]["poly"].centroid.distance(self.buildings[c]["poly"].centroid) > 25 for c, _ in chosen):
                near = min(anchors, key=lambda a: self.buildings[i]["poly"].centroid.distance(Point(*a[1])))[0]
                chosen.append((i, f"depth position toward {near}"))
        edge_word = "quay" if self.spec.get("edge_kind") == "harbour" else "cliff edge"
        sqc = self.square.centroid
        for i, role in chosen[:k]:
            b = self.buildings[i]
            c = b["poly"].centroid
            dx, dy = c.x - sqc.x, c.y - sqc.y
            side = ["east", "north-east", "north", "north-west", "west", "south-west", "south", "south-east"][
                int(((math.degrees(math.atan2(dy, dx)) + 22.5) % 360) // 45)]
            if role in ("Square", "Rim square"):
                role = "holds the square and covers the landmark"
            elif not role.startswith("depth position"):
                role = f"first contact: covers the {role} entry"
            elif b["d_sea"] < 30:
                role = f"overwatch on the {edge_word} ({side} side)"
            elif b["street"] is not None and any(s["id"] == b["street"] and s["kind"] == "main" for s in self.streets):
                role = f"main-street strongpoint ({side} of the square)"
            else:
                role = f"depth position in the {side} blocks"
            b["garrison"] = role
            if self.buildings[i]["height"] == "low":
                self.buildings[i]["height"] = "mid"

    # ---------------------------------------------------------------- measures
    def measures(self):
        m = {}
        n = len(self.buildings)
        m["buildings"] = n
        m["in_blocks_pct"] = round(100 * sum(1 for b in self.buildings if b["block"]) / max(n, 1), 1)
        m["blocks"] = len(self.blocks)
        fam = {f: sum(1 for b in self.buildings if b["family"] == f) for f in FAMILIES}
        m["family_counts"] = fam
        m["height_counts"] = {h: sum(1 for b in self.buildings if b["height"] == h) for h in ("low", "mid", "tall")}
        fw = [b["front_w"] for b in self.buildings if b["front_w"]]
        m["frontage_width_m"] = dict(min=round(min(fw), 1), max=round(max(fw), 1), mean=round(float(np.mean(fw)), 1),
                                     cv=round(float(np.std(fw) / np.mean(fw)), 2))
        m["frontage_buildings"] = len(fw)
        m["streets"] = []
        for st in self.streets:
            m["streets"].append(dict(id=st["id"], kind=st["kind"], width_m=st["width"], length_m=round(st["line"].length),
                                     max_straight_run_m=round(max_straight_run(st["line"]), 1)))
        m["square_area_m2"] = round(self.square.area)
        m["garrison"] = sum(1 for b in self.buildings if b.get("garrison"))
        allb = unary_union([b["poly"] for b in self.buildings])
        minx, miny, maxx, maxy = allb.bounds
        m["extent_m"] = [round(maxx - minx), round(maxy - miny)]
        m["built_footprint_m2"] = round(allb.area)
        return m
