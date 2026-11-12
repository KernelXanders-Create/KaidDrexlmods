"""Op ground planner (11 Nov C, job 1): place pads, route roads, place squad positions, find landing shores, check the rules.

Rules (from 00_START_HERE_11NOV_C.md), as this tool applies them:
 1. 5 m grid: a pad fixes every grid point under its footprint + 1.5 m to one level; pads at different levels need 14 m between
    footprints (17 m on the diagonal; this tool uses 17 m everywhere, the safe side). A road fixes every grid point within
    half its width + 3.5 m.
 2. A pad changes the ground by at most 4.0 m anywhere under it (footprint + 1.5 m).
 3. Roads: main <= 10 %, dirt <= 14 %; <= 4 m cut or fill (every grid point the road fixes); one connected net per island for
    the sites with a vehicle approach; no straight run over 150 m; nothing built within 3 m of a road edge.
 4. No pad within 12 m of another; no pad edge in water or within 10 m of the +0.3 m line unless harbour / beach work.
 5. Final and the four mains at least 400 m apart.
"""
import math, heapq, json
import numpy as np
from scipy import ndimage
from scipy.spatial import cKDTree
import world

C = 5.0
SEP = 17.0          # footprint to footprint between pads (different levels; 12 m rule is inside this)
ROAD_CLEAR = 3.0    # nothing built within 3 m of a road edge
CUT = 4.0


def rect(cx, cy, hx, hy, yaw, grow=0.0):
    """corners of a pad rectangle: hx along the pad's local x (east at yaw 0), hy along local y (north at yaw 0); yaw clockwise from north"""
    a = math.radians(yaw); ex = np.array([math.cos(a), -math.sin(a)]); ey = np.array([math.sin(a), math.cos(a)])
    c = np.array([cx, cy]); hx, hy = hx + grow, hy + grow
    return np.array([c - hx * ex - hy * ey, c + hx * ex - hy * ey, c + hx * ex + hy * ey, c - hx * ex + hy * ey])


def offsets(hx, hy, yaw, grow):
    """grid offsets (dj, di) of every grid point inside the grown rectangle, for a centre on a grid point"""
    R = math.hypot(hx + grow, hy + grow) + C          # the window reaches a rotated pad's corners (was max(hx, hy): corners were missed)
    n = int(math.ceil(R / C))
    dj, di = np.mgrid[-n:n + 1, -n:n + 1]
    X, Y = di * C, dj * C
    a = math.radians(yaw); ex = (math.cos(a), -math.sin(a)); ey = (math.sin(a), math.cos(a))
    u = X * ex[0] + Y * ex[1]; v = X * ey[0] + Y * ey[1]
    m = (np.abs(u) <= hx + grow + 1e-6) & (np.abs(v) <= hy + grow + 1e-6)
    return dj[m], di[m]



def nearest_on_line(P, pts, R, step=0.25):
    """for each point: distance to the polyline P, the index k of the segment it falls on and t along it (0..1);
    the line is sampled every `step` m and searched with a k-d tree (distance error under 0.01 m at the band edge)"""
    P = np.asarray(P, float); seg = np.diff(P, axis=0); Ls = np.hypot(*seg.T)
    ks, ts = [], []
    for k in range(len(seg)):
        m = max(1, int(math.ceil(Ls[k] / step))); t = np.arange(m) / m; ks.append(np.full(m, k)); ts.append(t)
    ks.append(np.array([len(seg) - 1])); ts.append(np.array([1.0]))
    ks = np.concatenate(ks); ts = np.concatenate(ts)
    S = P[ks] + seg[ks] * ts[:, None]
    d, i = cKDTree(S).query(pts, distance_upper_bound=R + step)
    ok = np.isfinite(d); i = np.where(ok, i, 0)
    return np.where(ok, d, 1e9), ks[i], ts[i]

class Plan:
    def __init__(self, box):
        self.H = world.H()
        self.box = box                                   # x0, x1, y0, y1 of the working window
        self.sites, self.roads, self.squads = [], [], []
        self.block = np.zeros(self.H.shape, bool)         # grid points no new pad footprint may cover (existing pads + SEP, roads + clearance)
        self.fixed = np.full(self.H.shape, np.nan)        # grid points fixed by pads / roads, at their level
        self.owner = np.full(self.H.shape, "", object)
        self.water = self.H <= 0.3
        self.cross_max = 0.5
        self.repair_to = 3.8                                    # the profile repair pulls each station's band to within this cut / fill
        self.steep = 0.8                                        # router step limit as a share of the grade (the profile pass holds the grade)
        self.band_range = 7.6                                   # the most the ground under a road band may vary (router filter only)
        self.balanced = False
        self.cliff_dilate = 2
        self.route_sigma = 1.5
        self.chaikin = 3

    # ----------------------------------------------------------------- pads
    def search(self, x, y, hx, hy, radius, step=10.0, yaws=range(0, 180, 15), water_ok=False, cap=3.6, prefer_low=True, avoid=(), pull=None):
        """best pad near (x, y): smallest score = distance + 60 m per metre of ground change over 2 m; all hard rules met"""
        H = self.H; best = None
        xs = np.arange(x - radius, x + radius + 1e-6, step); ys = np.arange(y - radius, y + radius + 1e-6, step)
        X, Y = np.meshgrid(xs, ys); keep = np.hypot(X - x, Y - y) <= radius
        X = np.round(X[keep] / C) * C; Y = np.round(Y[keep] / C) * C
        I = (X / C).astype(int); J = (Y / C).astype(int)
        wmask = ndimage.binary_dilation(self.water, iterations=2) if not water_ok else None     # +0.3 m line + 10 m
        for yaw in yaws:
            dj, di = offsets(hx, hy, yaw, 1.5)                   # pad points (footprint + 1.5 m)
            fj, fi = offsets(hx, hy, yaw, 0.0)                   # footprint points (spacing tests)
            ok = np.ones(len(X), bool)
            JJ = J[:, None] + dj[None, :]; II = I[:, None] + di[None, :]
            hz = H[JJ, II]
            lo, hi = hz.min(1), hz.max(1)
            lvl = (lo + hi) / 2; ch = (hi - lo) / 2
            ok &= ch <= cap
            ok &= ~self.block[J[:, None] + fj[None, :], I[:, None] + fi[None, :]].any(1)
            if not water_ok:
                ok &= ~wmask[JJ, II].any(1) & (lo > 0.3)
            elif water_ok == "beach":                            # a beach / harbour work: dry pad, may come to the water's edge
                ok &= H[JJ, II].min(1) > 0.3
            if not ok.any(): continue
            d = np.hypot(X - x, Y - y)
            score = d + 60.0 * np.maximum(0, ch - 2.0)
            if pull is not None: score = score + pull[2] * np.hypot(X - pull[0], Y - pull[1])
            for (ax, ay, ar) in avoid:
                score += np.where(np.hypot(X - ax, Y - ay) < ar, 1e6, 0)
            score[~ok] = np.inf
            k = int(np.argmin(score))
            if np.isfinite(score[k]) and (best is None or score[k] < best[0]):
                best = (float(score[k]), float(X[k]), float(Y[k]), yaw, round(float(lvl[k]) * 4) / 4, float(ch[k]))
        return best

    def add_site(self, sid, name, comp, hx, hy, x, y, radius, water_ok=False, size_note="", **kw):
        got = self.search(x, y, hx, hy, radius, water_ok=water_ok, **kw)
        if got is None:
            return None
        _, cx, cy, yaw, z, ch = got
        # re-measure the change at the rounded level
        dj, di = offsets(hx, hy, yaw, 1.5); J = int(cy / C) + dj; I = int(cx / C) + di
        hz = self.H[J, I]; cut = float(max(0, (hz - z).max())); fill = float(max(0, (z - hz).max()))
        s = dict(id=sid, name=name, comp=comp, x=cx, y=cy, yaw=yaw, hx=hx, hy=hy, z=z, cut_m=round(cut, 2), fill_m=round(fill, 2),
                 max_change_m=round(max(cut, fill), 2), moved_m=round(math.hypot(cx - x, cy - y)), rough=(x, y), size_note=size_note,
                 water_ok=water_ok, n_points=len(J))
        self.fixed[J, I] = z; self.owner[J, I] = sid
        # block: footprint dilated by SEP (+ half a cell for the 5 m sampling)
        fj, fi = offsets(hx, hy, yaw, SEP + 3.5); self.block[int(cy / C) + fj, int(cx / C) + fi] = True
        self.sites.append(s)
        return s

    def add_area(self, sid, poly_pts, z, grow=SEP, own=False):
        """a fixed area that is not a single pad (a town): its points are blocked for other pads"""
        from matplotlib.path import Path
        P = np.array(poly_pts); x0, y0 = P.min(0) - grow; x1, y1 = P.max(0) + grow
        I, J = np.meshgrid(np.arange(int(x0 / C), int(x1 / C) + 1), np.arange(int(y0 / C), int(y1 / C) + 1))
        from shapely.geometry import Polygon, Point
        pol = Polygon(P).buffer(grow)
        m = np.array([pol.contains(Point(i * C, j * C)) for i, j in zip(I.ravel(), J.ravel())])
        self.block[J.ravel()[m], I.ravel()[m]] = True
        if own:      # the area itself (not grown) is owned, so roads other than its own keep their band off it
            pol0 = Polygon(P); m0 = np.array([pol0.contains(Point(i * C, j * C)) for i, j in zip(I.ravel(), J.ravel())])
            jj, ii = J.ravel()[m0], I.ravel()[m0]; free = self.owner[jj, ii] == ""; self.owner[jj[free], ii[free]] = sid

    def add_buildings(self, sid, pts, r=8.0):
        """a town's buildings: each centre and the grid points within r metres are owned by the town, so roads keep their band off them"""
        for x, y in pts:
            n = int(math.ceil(r / C)); j0, i0 = int(round(y / C)), int(round(x / C))
            for dj in range(-n, n + 1):
                for di in range(-n, n + 1):
                    if math.hypot(dj * C, di * C) <= r and not self.owner[j0 + dj, i0 + di]: self.owner[j0 + dj, i0 + di] = sid

    # ----------------------------------------------------------------- roads
    def route(self, a, b, grade=0.14, width=7.0, za=None, zb=None, name="", kind="dirt", links=(), margin=450.0, cell=5.0, steep=None, pre=None, post=None, own_ids=()):
        """A* on a 10 m lattice (16 directions) inside the pair's box + margin, over smoothed natural ground; the grade limit is a
        hard limit per step (times `steep`, which the profile pass then absorbs with cut / fill); returns the road dict or None"""
        H = self.H; k = int(cell / C)
        if steep is None: steep = self.steep
        x0 = max(min(a[0], b[0]) - margin, self.box[0]); x1 = min(max(a[0], b[0]) + margin, self.box[1])
        y0 = max(min(a[1], b[1]) - margin, self.box[2]); y1 = min(max(a[1], b[1]) + margin, self.box[3])
        i0, i1, j0, j1 = int(x0 / C), int(x1 / C), int(y0 / C), int(y1 / C)
        Hs = ndimage.gaussian_filter(H[j0:j1 + 1, i0:i1 + 1], self.route_sigma)[::k, ::k]
        water = self.water[j0:j1 + 1, i0:i1 + 1]
        own = self.owner[j0:j1 + 1, i0:i1 + 1]
        padonly = np.vectorize(lambda o: bool(o) and not o.startswith("R:"))(own)
        band = int(math.ceil((width / 2 + 3.5 + ROAD_CLEAR) / C))
        wband = int(math.ceil((width / 2 + 3.5 + 1.0) / C))                 # the whole band stays on dry ground
        bad = ndimage.binary_dilation(water, iterations=max(2, wband)) | ndimage.binary_dilation(padonly, iterations=band)
        Hf = ndimage.gaussian_filter(H[j0:j1 + 1, i0:i1 + 1], 1.0); gy_, gx_ = np.gradient(Hf, C)
        sl_ = np.hypot(gx_, gy_)
        bad |= sl_ > self.cross_max                                 # side slope: the 7 m band would cut / fill too much
        if self.cliff_dilate: bad |= ndimage.binary_dilation(sl_ > 0.9, iterations=self.cliff_dilate)    # and keep the band off cliff edges
        Hr = H[j0:j1 + 1, i0:i1 + 1]; nb = int(math.ceil((width / 2 + 3.5) / C)) * 2 + 1
        bad |= (ndimage.maximum_filter(Hr, size=nb) - ndimage.minimum_filter(Hr, size=nb)) > self.band_range   # no single level holds the band within 4 m (the profile repair and the 4 m check still apply)
        bad = ndimage.maximum_filter(bad.astype(np.uint8), size=k)[::k, ::k].astype(bool)
        ny, nx = Hs.shape
        sa = (int(round((a[1] - j0 * C) / cell)), int(round((a[0] - i0 * C) / cell))); sb = (int(round((b[1] - j0 * C) / cell)), int(round((b[0] - i0 * C) / cell)))
        r_free = band // k + 2
        for (sj, si) in (sa, sb):
            bad[max(0, sj - r_free):sj + r_free + 1, max(0, si - r_free):si + r_free + 1] = False
        others = np.vectorize(lambda o: bool(o) and not o.startswith("R:") and o not in own_ids)(own)       # other pads stay blocked near the ends
        others = ndimage.binary_dilation(others, iterations=int(math.ceil((width / 2 + ROAD_CLEAR) / C)) + 1)
        bad |= ndimage.maximum_filter(others.astype(np.uint8), size=k)[::k, ::k].astype(bool)
        steps = [(dj, di) for dj in range(-2, 3) for di in range(-2, 3) if (dj, di) != (0, 0) and math.gcd(abs(dj), abs(di)) == 1]
        g = {sa: 0.0}; prev = {}; pq = [(0.0, sa)]; done = set()
        while pq:
            f, n = heapq.heappop(pq)
            if n == sb: break
            if n in done: continue
            done.add(n)
            for dj, di in steps:
                m = (n[0] + dj, n[1] + di)
                if not (1 <= m[0] < ny - 1 and 1 <= m[1] < nx - 1) or bad[m]: continue
                L = math.hypot(dj, di) * cell; dz = abs(Hs[m] - Hs[n]) / L
                if dz > grade * steep: continue
                ng = g[n] + L * (1 + 2.0 * max(0.0, dz - 0.6 * grade) / grade)
                if ng < g.get(m, 1e18):
                    g[m] = ng; prev[m] = n; heapq.heappush(pq, (ng + math.hypot(m[0] - sb[0], m[1] - sb[1]) * cell, m))
        if sb not in g: return None
        path = [sb]
        while path[-1] != sa: path.append(prev[path[-1]])
        path = path[::-1]
        P = np.array([(i0 * C + p[1] * cell, j0 * C + p[0] * cell) for p in path], float)
        P[0] = a; P[-1] = b
        if pre is not None: P = np.vstack([np.array(pre, float), P])        # a straight stub out of the pad before the route
        if post is not None: P = np.vstack([P, np.array(post, float)])      # and a straight stub into the pad after it
        return self._road(P, grade, width, za, zb, name, kind, links)

    def _road(self, P, grade, width, za, zb, name, kind, links):
        P = np.asarray(P, float)
        # smooth (Chaikin) and resample every 4.5 m
        for _ in range(self.chaikin):
            Q = [P[0]]
            for p, q in zip(P[:-1], P[1:]): Q += [0.75 * p + 0.25 * q, 0.25 * p + 0.75 * q]
            Q.append(P[-1]); P = np.array(Q)
        s = np.r_[0, np.cumsum(np.hypot(*np.diff(P, axis=0).T))]; L = s[-1]
        n = max(2, int(math.ceil(L / 4.5)) + 1); ss = np.linspace(0, L, n)
        P = np.c_[np.interp(ss, s, P[:, 0]), np.interp(ss, s, P[:, 1])]
        if L > 150 and straight_run(P, 1.0) > 140:          # break long straights: a gentle 2.5 m side-to-side wave (keeps switchbacks)
            T = np.gradient(P, axis=0); T = T / (np.linalg.norm(T, axis=1)[:, None] + 1e-9); Nn = np.c_[-T[:, 1], T[:, 0]]
            w = 2.5 * np.sin(2 * np.pi * ss / 120.0) * np.clip(np.minimum(ss, L - ss) / 20.0, 0, 1)
            P = P + Nn * w[:, None]
            s2 = np.r_[0, np.cumsum(np.hypot(*np.diff(P, axis=0).T))]; L = s2[-1]          # the wave bunches points on curves: space them evenly again
            n = max(2, int(math.ceil(L / 4.5)) + 1); ss = np.linspace(0, L, n)
            P = np.c_[np.interp(ss, s2, P[:, 0]), np.interp(ss, s2, P[:, 1])]
        gz = np.array([world.z(x, y) for x, y in P])
        # target level per station: the middle of the natural ground over the band points nearest to it (balances cut against fill)
        Rb = width / 2 + 3.5
        x0b, y0b = P.min(0) - Rb - C; x1b, y1b = P.max(0) + Rb + C
        Ib, Jb = np.meshgrid(np.arange(int(x0b / C), int(x1b / C) + 2), np.arange(int(y0b / C), int(y1b / C) + 2))
        pts = np.c_[(Ib * C).ravel(), (Jb * C).ravel()]; nat = self.H[Jb.ravel(), Ib.ravel()]
        bd, k_, t_ = nearest_on_line(P, pts, Rb); bk = np.where(t_ < 0.5, k_, k_ + 1)
        inb = bd <= Rb
        lo = np.full(n, np.inf); hi = np.full(n, -np.inf)
        np.minimum.at(lo, bk[inb], nat[inb]); np.maximum.at(hi, bk[inb], nat[inb])
        mid = np.where(np.isfinite(lo), (lo + hi) / 2, gz)
        zp = ndimage.uniform_filter1d(gz, 5, mode="nearest") if not self.balanced else ndimage.uniform_filter1d(mid, 3, mode="nearest")
        if za is not None: zp[0] = za
        if zb is not None: zp[-1] = zb
        ss = np.r_[0, np.cumsum(np.hypot(*np.diff(P, axis=0).T))]; L = ss[-1]       # distances along the points as handed over
        ds = np.diff(ss).mean(); seg = np.maximum(np.diff(ss), 1e-6)     # each segment's own length: the grade holds point to point
        land_a = (ss <= 16.0) if za is not None else np.zeros(n, bool)          # level landings: the band at a pad or junction keeps its level
        land_b = (ss >= L - 12.0) if zb is not None else np.zeros(n, bool)
        fixed = land_a | land_b
        if za is not None: zp[land_a] = za
        if zb is not None: zp[land_b] = zb
        for _ in range(200):                                  # grade limit: clamp toward the ground, never moving the landings
            old = zp.copy()
            for k in range(1, n):
                if not fixed[k]: zp[k] = min(max(zp[k], zp[k - 1] - grade * seg[k - 1]), zp[k - 1] + grade * seg[k - 1])
            for k in range(n - 2, -1, -1):
                if not fixed[k]: zp[k] = min(max(zp[k], zp[k + 1] - grade * seg[k]), zp[k + 1] + grade * seg[k])
            if np.abs(zp - old).max() < 1e-4: break
        # repair: where a station's band goes past 3.9 m of cut or fill, move that station toward its band (within the grade limit)
        for _ in range(80):
            dev = nat[inb] - zp[bk[inb]]
            dmax = np.full(n, -np.inf); dmin = np.full(n, np.inf)
            np.maximum.at(dmax, bk[inb], dev); np.minimum.at(dmin, bk[inb], dev)
            T_ = self.repair_to; up = np.where(np.isfinite(dmax) & (dmax > T_), dmax - T_, 0.0); dn = np.where(np.isfinite(dmin) & (dmin < -T_), dmin + T_, 0.0)
            shift = np.where(up > 0, np.where(dmin - up >= -T_, up, 0.5 * (up + dn)), dn)
            shift[fixed] = 0.0
            if np.abs(shift).max() < 0.01: break
            zp = zp + ndimage.uniform_filter1d(shift, 5, mode="nearest") * 1.2
            for _k in range(30):
                old = zp.copy()
                for k in range(1, n):
                    if not fixed[k]: zp[k] = min(max(zp[k], zp[k - 1] - grade * seg[k - 1]), zp[k - 1] + grade * seg[k - 1])
                for k in range(n - 2, -1, -1):
                    if not fixed[k]: zp[k] = min(max(zp[k], zp[k + 1] - grade * seg[k]), zp[k + 1] + grade * seg[k])
                if np.abs(zp - old).max() < 1e-4: break
        r = dict(id=name, kind=kind, width_m=width, links=list(links), points=[[round(float(x), 2), round(float(y), 2)] for x, y in P],
                 points_z=[round(float(v), 2) for v in zp], length_m=round(float(L)), max_grade_pct=round(float(np.max(np.abs(np.diff(zp)) / seg) * 100), 1))
        self.check_road(r)
        return r

    def band_points(self, r):
        """grid points the road fixes (within half width + 3.5 m), each with the road level at its nearest station"""
        P = np.array(r["points"]); Z = np.array(r["points_z"]); R = r["width_m"] / 2 + 3.5
        x0, y0 = P.min(0) - R - C; x1, y1 = P.max(0) + R + C
        I, J = np.meshgrid(np.arange(int(x0 / C), int(x1 / C) + 2), np.arange(int(y0 / C), int(y1 / C) + 2))
        X, Y = I * C, J * C; pts = np.c_[X.ravel(), Y.ravel()]
        best_d, k_, t_ = nearest_on_line(P, pts, R); best_z = Z[k_] + (Z[k_ + 1] - Z[k_]) * t_
        m = best_d <= R
        return J.ravel()[m], I.ravel()[m], best_z[m]

    def check_road(self, r):
        J, I, Z = self.band_points(r)
        nat = self.H[J, I]
        r["max_cut_fill_m"] = round(float(np.abs(Z - nat).max()), 2) if len(Z) else 0.0
        r["in_water_points"] = int((nat <= 0.0).sum())
        cur = self.fixed[J, I]; own = self.owner[J, I]
        clash = ~np.isnan(cur) & (np.abs(cur - Z) > 0.05)
        isroad = np.array([str(o).startswith("R:") for o in own], bool) if len(own) else np.zeros(0, bool)
        r["clash_points"] = int((clash & ~isroad).sum()); r["clash_with"] = sorted(set(own[clash & ~isroad].tolist()))
        r["junction_step_points"] = int((clash & isroad).sum())
        r["junction_step_max_m"] = round(float(np.abs(cur - Z)[clash & isroad].max()), 2) if (clash & isroad).any() else 0.0
        r["straight_max_m"] = straight_run(np.array(r["points"]))
        return r

    def commit_road(self, r):
        J, I, Z = self.band_points(r)
        free = np.isnan(self.fixed[J, I])
        self.fixed[J[free], I[free]] = Z[free]; self.owner[J[free], I[free]] = "R:" + r["id"]
        # block pads: band + 3 m clearance + SEP
        R = r["width_m"] / 2 + 3.5 + ROAD_CLEAR
        P = np.array(r["points"]); x0, y0 = P.min(0) - R - C; x1, y1 = P.max(0) + R + C
        I2, J2 = np.meshgrid(np.arange(int(x0 / C), int(x1 / C) + 2), np.arange(int(y0 / C), int(y1 / C) + 2))
        pts = np.c_[(I2 * C).ravel(), (J2 * C).ravel()]; dmin = np.full(len(pts), 1e9)
        for k in range(len(P) - 1):
            a, b = P[k], P[k + 1]; ab = b - a; t = np.clip(((pts - a) @ ab) / (ab @ ab + 1e-9), 0, 1)
            dmin = np.minimum(dmin, np.hypot(*(pts - (a + t[:, None] * ab)).T))
        m = dmin <= r["width_m"] / 2 + ROAD_CLEAR + 3.5 + 2.5          # + 2.5 m: pads are tested on 5 m grid points
        self.block[J2.ravel()[m], I2.ravel()[m]] = True
        self.roads.append(r)

    # ----------------------------------------------------------------- shores
    def shores(self, x0, x1, y0, y1, max_slope=0.12, min_len=40.0):
        """coast stretches a boat can land on: water-edge grid points whose ground rises at most max_slope over the first 30 m inland"""
        H = self.H; j0, j1, i0, i1 = int(y0 / C), int(y1 / C), int(x0 / C), int(x1 / C)
        h = H[j0:j1, i0:i1]; land = h > 0.3
        edge = land & ndimage.binary_dilation(~land) & (h < 3.0)
        gy, gx = np.gradient(ndimage.gaussian_filter(h, 2.0), C); sl = np.hypot(gx, gy)
        inland = ndimage.maximum_filter(np.where(land, sl, 0), size=7)
        good = edge & (inland <= max_slope)
        lab, n = ndimage.label(ndimage.binary_dilation(good, iterations=1), structure=np.ones((3, 3)))
        out = []
        for k in range(1, n + 1):
            jj, ii = np.nonzero((lab == k) & good)
            if len(jj) < 2: continue
            pts = np.c_[(ii + i0) * C, (jj + j0) * C]
            # length = longest extent
            d = np.hypot(*(pts[:, None, :] - pts[None, :, :]).transpose(2, 0, 1)) if len(pts) < 400 else None
            if d is not None:
                a, b = np.unravel_index(np.argmax(d), d.shape); L = d[a, b]; A, B = pts[a], pts[b]
            else:
                A, B = pts[0], pts[-1]; L = float(np.hypot(*(A - B)))
            if L >= min_len:
                out.append(dict(from_xy=[float(A[0]), float(A[1])], to_xy=[float(B[0]), float(B[1])], length_m=round(float(L)), points=len(pts),
                                mean_inland_slope_pct=round(float(inland[jj, ii].mean() * 100), 1)))
        return out


def straight_run(P, tol=1.0):
    best = 0.0; n = len(P); i = 0
    while i < n - 1:
        j = i + 1
        while j + 1 < n:
            a, b = P[i], P[j + 1]; ab = b - a; v = P[i:j + 2] - a
            if (np.abs(ab[0] * v[:, 1] - ab[1] * v[:, 0]) / (np.linalg.norm(ab) + 1e-9)).max() > tol: break
            j += 1
        best = max(best, float(np.linalg.norm(P[j] - P[i]))); i = max(i + 1, j - 1) if j - 1 > i else i + 1
    return round(best, 1)
