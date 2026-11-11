"""Sketch-terrain helpers for Kernel Stage A (PROPOSED concept sketches only).

These build a coarse height field (default 1000 x 1000 cells at 16 m for a
16 x 16 km map) from hand-placed landform features. The output is for
CHOOSING between concepts. It is not a Stage B heightmap.

Coordinates: metres from the south-west corner, x east, y north.
Array layout: H[row, col] with row 0 = SOUTH edge (we flip only when plotting).
"""
import math
from functools import lru_cache
import numpy as np
from scipy import ndimage

SIZE_M = 16000.0
N = 1000                      # cells per side (16 m cells)
CELL = SIZE_M / N

_yy, _xx = np.mgrid[0:N, 0:N]
X = (_xx + 0.5) * CELL        # metres east
Y = (_yy + 0.5) * CELL        # metres north


# ---------------------------------------------------------------- noise
def noise(seed, scale_m, amp=1.0):
    """Non-periodic smooth noise: Gaussian-filtered white noise, ~unit std."""
    return _noise_unit(int(seed), float(scale_m)) * amp


@lru_cache(maxsize=256)
def _noise_unit(seed, scale_m):
    rng = np.random.default_rng(seed)
    f = ndimage.gaussian_filter(rng.standard_normal((N, N)), scale_m / CELL,
                                mode="reflect")
    f /= (f.std() + 1e-9)
    f.setflags(write=False)
    return f


def fbm(seed, base_m=2000.0, octaves=5, gain=0.5):
    out = np.zeros((N, N))
    amp, scale, tot = 1.0, base_m, 0.0
    for o in range(octaves):
        out += noise(seed * 97 + o, max(scale, CELL), amp)
        tot += amp
        amp *= gain
        scale *= 0.5
    return out / tot


def warp(seed, strength_m=400.0, scale_m=1500.0):
    """Return warped coordinates (WX, WY) for organic, non-periodic shapes."""
    return (X + noise(seed, scale_m, strength_m) + noise(seed + 1, scale_m / 3, strength_m / 3),
            Y + noise(seed + 2, scale_m, strength_m) + noise(seed + 3, scale_m / 3, strength_m / 3))


def smoothstep(e0, e1, x):
    t = np.clip((x - e0) / (e1 - e0 + 1e-9), 0, 1)
    return t * t * (3 - 2 * t)


# ---------------------------------------------------------------- shapes
def coast_dist(cx, cy, rx, ry, ang_deg=0.0, seed=0, wstr=300.0, wscale=1200.0):
    """Approx signed distance (m) to an organic ellipse edge, + inside."""
    wx, wy = warp(seed, wstr, wscale)
    wx = wx + noise(seed + 7, 250, wstr * 0.25)          # small coves and points
    wy = wy + noise(seed + 8, 250, wstr * 0.25)
    a = math.radians(ang_deg)
    dx, dy = wx - cx, wy - cy
    u = dx * math.cos(a) + dy * math.sin(a)
    v = -dx * math.sin(a) + dy * math.cos(a)
    d = np.sqrt((u / rx) ** 2 + (v / ry) ** 2)
    return (1.0 - d) * min(rx, ry), np.arctan2(dy, dx)


def shelf_profile(s, shelf_w=250.0, shelf_d=2.5, slope_w=900.0, floor=-40.0):
    """Underwater profile for s<0 (metres outside the shore).
    Every shore gets a shelf: 0 -> -shelf_d over shelf_w, then down to floor."""
    o = -s
    a = -shelf_d * smoothstep(0, shelf_w, o) ** 0.8
    b = (floor + shelf_d) * smoothstep(shelf_w, shelf_w + slope_w, o)
    return a + b


def island(H, cx, cy, rx, ry, peak, ang=0.0, seed=0, ramp=600.0,
           cliff_dir=None, cliff_ramp=60.0, rough=0.25, shelf_w=250.0,
           floor=-40.0, wstr=550.0):
    """Add an island (max-combine). cliff_dir: compass bearing (deg, 0=N)
    of the cliffed side; shores there rise fast (still with a shelf)."""
    s, theta = coast_dist(cx, cy, rx, ry, ang, seed, wstr)
    r = np.full_like(s, ramp)
    if cliff_dir is not None:
        bearing = (90 - np.degrees(theta)) % 360
        diff = np.abs(((bearing - cliff_dir) + 180) % 360 - 180)
        k = smoothstep(80, 20, diff)            # 1 facing the cliff side
        r = ramp * (1 - k) + cliff_ramp * k
    land = peak * smoothstep(0, r, s) ** 0.9 * (1 + rough * fbm(seed + 11, 900, 4))
    land = np.maximum(land, 0.3 * smoothstep(0, 40, s))
    sw = shelf_w * np.clip(1 + 0.7 * noise(seed + 20, 700), 0.35, 2.2)   # shelf width varies
    slope = 900 * np.clip(1 + 0.5 * noise(seed + 21, 1500), 0.4, 2)
    sea = shelf_profile(s, sw, 2.5, slope, floor)
    sea = np.where(-s < sw + slope * 1.3, sea, -1e4)     # no far-field effect
    h = np.where(s > 0, land, sea)
    np.maximum(H, h, out=H)
    return s


def tower(H, cx, cy, r, peak, seed=0):
    """Steep karst tower / sea stack (heightfield cannot undercut;
    mushroom undercuts must come from rock objects)."""
    d = np.hypot(X - cx, Y - cy)
    jitter = np.clip(1 + 0.15 * noise(seed, 60), 0.85, 1.15)
    t = smoothstep(r * 1.2 * jitter, r * 0.8 * jitter, d)
    sk = smoothstep(r * 2.5, r * 1.1, d)          # small rock shelf round the foot
    np.maximum(H, peak * t + (1 - t) * (-200 * (1 - sk) - 1.5 * sk), out=H)


def carve_line(H, pts, width, depth, soft=60.0, only_below=None):
    """Lower terrain to -depth along a polyline (channel/river/pass)."""
    d = dist_to_polyline(pts)
    t = smoothstep(width / 2 + soft, width / 2, d)
    target = -depth
    newh = H * (1 - t) + np.minimum(H, target) * t
    if only_below is not None:
        newh = np.where(H < only_below, newh, H)
    H[:] = newh


def raise_line(H, pts, width, height, soft=40.0):
    """Raise terrain to `height` along a polyline (sandbar, levee, causeway)."""
    d = dist_to_polyline(pts)
    t = smoothstep(width / 2 + soft, width / 2, d)
    H[:] = H * (1 - t) + np.maximum(H, height) * t


def set_blob(H, cx, cy, r, value, soft=150.0, seed=0, mode="max", wstr=120.0):
    """Blend toward a fixed value inside an organic disc (reef flat, lake)."""
    wx, wy = warp(seed, wstr, 600)
    d = np.hypot(wx - cx, wy - cy)
    t = smoothstep(r + soft, r, d)
    v = value if np.isscalar(value) else value
    if mode == "max":
        H[:] = H * (1 - t) + np.maximum(H, v) * t
    elif mode == "min":
        H[:] = H * (1 - t) + np.minimum(H, v) * t
    else:
        H[:] = H * (1 - t) + v * t
    return t


def dist_to_polyline(pts):
    d = np.full((N, N), 1e9)
    for (x0, y0), (x1, y1) in zip(pts[:-1], pts[1:]):
        vx, vy = x1 - x0, y1 - y0
        L2 = vx * vx + vy * vy + 1e-9
        t = np.clip(((X - x0) * vx + (Y - y0) * vy) / L2, 0, 1)
        d = np.minimum(d, np.hypot(X - (x0 + t * vx), Y - (y0 + t * vy)))
    return d


def meander(p0, p1, amp, wavelength, seed, n=60):
    """Non-periodic meander between two points (random-phase sum of sines)."""
    rng = np.random.default_rng(seed)
    p0, p1 = np.array(p0, float), np.array(p1, float)
    L = np.linalg.norm(p1 - p0)
    t = np.linspace(0, 1, n)
    base = p0[None] + (p1 - p0)[None] * t[:, None]
    nrm = np.array([-(p1 - p0)[1], (p1 - p0)[0]]) / L
    off = np.zeros(n)
    for k in range(4):
        wl = wavelength * rng.uniform(0.6, 1.6)
        off += amp * rng.uniform(0.3, 1.0) * np.sin(2 * np.pi * t * L / wl + rng.uniform(0, 6.28))
    off *= np.sin(np.pi * t) ** 0.3
    return [tuple(p) for p in base + nrm[None] * off[:, None]]


# ---------------------------------------------------------------- sampling
def sample(H, x, y):
    c = int(np.clip(x / CELL, 0, N - 1))
    r = int(np.clip(y / CELL, 0, N - 1))
    return float(H[r, c])


def line_profile(H, p0, p1, step=8.0):
    L = math.hypot(p1[0] - p0[0], p1[1] - p0[1])
    n = max(2, int(L / step))
    xs = np.linspace(p0[0], p1[0], n)
    ys = np.linspace(p0[1], p1[1], n)
    return L, np.array([sample(H, x, y) for x, y in zip(xs, ys)])


def crossing_stats(H, p0, p1):
    """MEASURED on the sketch: total line length, water length, min/max depth."""
    L, prof = line_profile(H, p0, p1)
    wet = prof < 0
    water_len = L * wet.mean()
    if wet.any():
        return dict(length_m=round(L), water_m=round(water_len),
                    deepest_m=round(float(prof[wet].min()), 1),
                    shallowest_m=round(float(prof[wet].max()), 1))
    return dict(length_m=round(L), water_m=0, deepest_m=0.0, shallowest_m=0.0)


def label_islands(H, level=0.0, min_area_km2=0.05):
    lab, n = ndimage.label(H > level)
    areas = ndimage.sum(np.ones_like(H), lab, range(1, n + 1)) * CELL * CELL / 1e6
    return lab, areas


def snap_to_land(H, x, y, min_h=0.3, max_m=600.0):
    """Move a point to the nearest cell with H >= min_h within max_m."""
    if sample(H, x, y) >= min_h:
        return x, y, 0.0
    r = int(max_m / CELL)
    c0, r0 = int(x / CELL), int(y / CELL)
    rs, cs = slice(max(0, r0 - r), min(N, r0 + r + 1)), slice(max(0, c0 - r), min(N, c0 + r + 1))
    sub = H[rs, cs]
    ys, xs = np.nonzero(sub >= min_h)
    if len(xs) == 0:
        return x, y, -1.0
    gx = (xs + cs.start + 0.5) * CELL
    gy = (ys + rs.start + 0.5) * CELL
    d = np.hypot(gx - x, gy - y)
    i = int(np.argmin(d))
    return float(gx[i]), float(gy[i]), float(d[i])


def chaikin(pts, it=3):
    """Smooth a hand-drawn polyline (keeps ends)."""
    p = np.array(pts, float)
    for _ in range(it):
        q = [p[0]]
        for a, b in zip(p[:-1], p[1:]):
            q += [0.75 * a + 0.25 * b, 0.25 * a + 0.75 * b]
        q.append(p[-1])
        p = np.array(q)
    return [tuple(x) for x in p]


def offset_line(pts, off):
    """Parallel polyline at `off` metres to the left of travel."""
    p = np.array(pts, float)
    d = np.gradient(p, axis=0)
    n = np.stack([-d[:, 1], d[:, 0]], 1)
    n /= np.linalg.norm(n, axis=1, keepdims=True) + 1e-9
    return [tuple(x) for x in p + n * off]


def crater_field(seed, count, region, r_range=(16, 48), depth=1.8):
    """Shell-crater field as a height DELTA (bowl + low rim), via scattered
    stamps. region = (x0, y0, x1, y1) in metres."""
    from scipy.signal import fftconvolve
    rng = np.random.default_rng(seed)
    out = np.zeros((N, N))
    x0, y0, x1, y1 = region
    for rc in np.linspace(r_range[0], r_range[1], 4):
        imp = np.zeros((N, N))
        k = count // 4
        xs = rng.uniform(x0, x1, k) / CELL
        ys = rng.uniform(y0, y1, k) / CELL
        imp[ys.astype(int).clip(0, N - 1), xs.astype(int).clip(0, N - 1)] = rng.uniform(0.6, 1.2, k)
        R = int(rc * 2.2 / CELL) + 2
        gy, gx = np.mgrid[-R:R + 1, -R:R + 1] * CELL
        dd = np.hypot(gx, gy) / rc
        kern = -depth * np.clip(1 - dd ** 2, 0, None) + 0.5 * depth * np.exp(-((dd - 1.15) / 0.25) ** 2)
        out += fftconvolve(imp, kern, mode="same")
    return out
