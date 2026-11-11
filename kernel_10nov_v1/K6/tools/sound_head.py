"""Sound Head (3-M3, op 3) on the real ground: K6 config (PROPOSED).
Ground: a bowl falling east to the Sound at 22-25 %. Terraces on the contours, one row
on the uphill side of each street; the gate square on the saddle at the bowl's
south-east lip; the quay on the narrow shore strip to the north-east."""
import math
import numpy as np
from shapely.geometry import Polygon, LineString, box
PACK = "/tmp/claude-0/-home-user-KaidDrexlmods/68d91108-852d-5f8a-b84e-f7c6d8824e63/scratchpad/handoff_10nov_b/KERNEL_HANDOFF_20261110b"

import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as _plt
from shapely.geometry import Polygon as _P

_H = np.load(PACK + "/towns6/sound_head/height_1m.npy"); _X0, _Y0 = 2200, 10200
BOWL = _P([(2470, 10470), (2560, 10470), (2610, 10478), (2648, 10500), (2675, 10512), (2660, 10560), (2632, 10640),
           (2622, 10708), (2560, 10712), (2470, 10712), (2440, 10600)])

def contour_street(level, region=BOWL, step=1):
    xs = np.arange(_X0, _X0 + _H.shape[1], step); ys = np.arange(_Y0, _Y0 + _H.shape[0], step)
    cs = _plt.contour(xs, ys, _H[::step, ::step], levels=[level]); _plt.close()
    best = None
    for seg in cs.allsegs[0]:
        ls = LineString(seg).intersection(region)
        parts = [ls] if ls.geom_type == "LineString" else list(getattr(ls, "geoms", []))
        for p_ in parts:
            if p_.geom_type == "LineString" and (best is None or p_.length > best.length): best = p_
    pts = list(best.coords)
    if pts[0][1] > pts[-1][1]: pts = pts[::-1]                 # run south to north
    keep = [pts[0]]
    for q in pts[1:]:
        if math.dist(q, keep[-1]) >= 12: keep.append(q)
    if math.dist(keep[-1], pts[-1]) > 3: keep.append(pts[-1])
    # gentle bends: push every other point 3.5 m across the contour (about 0.8 m of height on this slope)
    out = []
    for i, q in enumerate(keep):
        if 0 < i < len(keep) - 1 and i % 2 == 0:
            a, b = np.array(keep[i - 1]), np.array(keep[i + 1]); t = (b - a) / (np.linalg.norm(b - a) + 1e-9); n = np.array([-t[1], t[0]])
            q = tuple(np.array(q) + n * 3.5 * (1 if (i // 2) % 2 else -1))
        out.append(q)
    return out

# the gate square: long and narrow along the contour on the valley floor at the south-east lip
_c = np.array([2638.0, 10462.0]); _u = np.array([0.707, -0.707]); _v = np.array([0.707, 0.707])
SQ_PTS = [tuple(np.round(_c + a * 20 * _u + b * 8 * _v, 1)) for a, b in ((1, 1), (1, -1), (-1, -1), (-1, 1))]
QUAY = box(2637, 10657, 2670, 10684); QUAY_Z = 3.0

CFG = dict(
    key="sound_head", town="Sound Head", version="K6 (grid rule) PROPOSED", seed=5,
    tile=PACK + "/towns6/sound_head/height_1m.npy", tile_origin=(2200, 10200), ground_label="site tile (as built today)",
    target_n=90, garrison_range=(40, 50), square=True,
    view=((2420, 2720), (10410, 10760)),
    inset=dict(view=((2595, 2685), (10425, 10500)), title="the gate square on the valley floor (one level)"),
    title="Sound Head (op 3, 3-M3), K6 PROPOSED: contour terraces on the bowl, real models, 5 m grid rule",
    labels={"gate square (saddle)": (2600, 10425), "quay": (2672, 10660), "the Sound": (2690, 10740), "to the Notch road": (2660, 10418),
            "path to the Summit AA": (2440, 10725)},
    streets=[],
    notes=["PROPOSED by Kernel K6, Sound Head, under the 5 m grid rule (10 Nov late note).",
           "Each street is a terrace: level segments (blue numbers on the plan) with a row on its uphill side; levels change only across 16 m gaps.",
           "Stair paths (P1-P3) climb between terraces; they carry no buildings and follow the ground.",
           "The gate square sits on the saddle at the bowl's south-east lip, where the Notch road comes in; the quay is on the shore strip to the north-east.",
           "Lamps are yours."],
)

def build(T):
    sq = Polygon(SQ_PTS); T.SQ = sq
    x0, y0, x1, y1 = sq.bounds; xs, ys = np.meshgrid(np.arange(x0, x1), np.arange(y0, y1)); from shapely import contains_xy
    m = contains_xy(sq, xs, ys); sqz = round(float(T.G.zv(xs[m], ys[m]).mean()) * 4) / 4
    T.square_z = sqz
    # pin the main street to the square level at its start; recompute its levels
    T.streets["M"]["pin_start"] = sqz; T._levels(T.streets["M"]); pass
    T.extra_pads.append((sq.buffer(1.5), sqz)); T.extra_pads.append((QUAY.buffer(0.5), QUAY_Z))
    from town_grid import grid_points
    for gp in grid_points(sq.buffer(1.5)): T.claims[gp] = sqz
    for gp in grid_points(QUAY.buffer(0.5)): T.claims[gp] = QUAY_Z
    T.draw_polys = [(sq, "#f3e6c4", "#7b2cbf", "square"), (QUAY, "#d9e8f0", "#1f5f8b", "quay apron")]
    # landmark on the square
    T.pad += 1; T._pg = f"P{T.pad:03d}"
    lx, ly = tuple(np.array(sq.centroid.coords[0]) + 9 * np.array([0.707, -0.707])); T.add("ND06", lx, ly, 45.0, "front", sqz, "SQ", "landmark", T._pg)
    # square ring: west and north sides (doors into the square); the east side stays open toward the Sound
    c = np.array(sq.centroid.coords[0])
    P = SQ_PTS          # 0:(+u,+v) 1:(+u,-v) 2:(-u,-v) 3:(-u,+v); -v side is uphill (south-west)
    T.log.clear()
    for edge in ([P[2], P[1]], [P[3], P[2]], [P[1], P[0]]):
        T.pack_edge(edge, c, sqz, ["SF01", "SF08", "SF15", "SF16", "WH19", "ND03", "WH03", "ND01", "ND02", "WH11"], "square", allow_tall=False, cut_lim=3.2)
    print("RING", dict(T.log), "square level", sqz, "corners", P); T.log.clear()
    # terraces
    for k in ("M", "T14", "T21", "T28", "T42", "T49", "T56"):
        pool, role, sci = (T.cfg["pool_main"], "main", 0.5) if k == "M" else (T.cfg["pool_lane"], "lane", 0.12 if k in ("T14", "T21") else 0.0)
        for side in T.row_sides(T.streets[k]):
            T.pack_row(k, side, pool, role, max_depth=16.5, cut_lim=2.5, sci_first=sci)
    # quay group: on the apron's landward edge, doors onto the apron
    T.log.clear()
    T.pack_edge([(2638, 10658), (2638, 10683)], (2660, 10670), QUAY_Z, ["ND03", "WH19", "WH03", "WH11", "SF15", "SF16"], "quay", street_id="QY", cut_lim=3.5)
    T.pack_edge([(2640, 10657), (2668, 10657)], (2655, 10672), QUAY_Z, ["ND03", "WH19", "WH03", "WH11", "SF15"], "quay", street_id="QY", cut_lim=3.5)
    print("QUAY", dict(T.log))
    T.comps = [dict(name_or_role="gate square: market or cargo group (whole comp, your pick)", x=round(float(sq.centroid.x) - 6, 1), y=round(float(sq.centroid.y) + 6, 1), yaw_deg=45.0, footprint_m=[9.5, 9.4], pad_z_m=sqz),
               dict(name_or_role="quay comp: boat slips / cargo pad (whole comp, your pick)", x=2659.0, y=10672.0, yaw_deg=0.0, footprint_m=[16.0, 18.0], pad_z_m=QUAY_Z)]
    T.square_out = {"polygon": [list(p) for p in SQ_PTS], "level_z_m": sqz, "landmark_building_id": next(b["id"] for b in T.B if b["role"] == "landmark"),
                    "open_side": "east, toward the Sound"}

_levels = {14: "T14", 21: "T21", 28: "T28", 35: "M", 42: "T42", 49: "T49", 56: "T56"}
for lev, sid in _levels.items():
    pts = contour_street(lev)
    CFG["streets"].append(dict(id=sid, cls="main" if sid == "M" else "lane", w=7.0 if sid == "M" else 4.5, rows="up", smooth=True,
                               name=("main street (35 m contour)" if sid == "M" else f"terrace lane ({lev} m contour)"), pts=pts, seg=(30, 60)))
CFG["streets"] += [
    dict(id="QR", cls="path", w=3.5, rows="none", name="quay stair (foot only; boats serve the quay)",
         pts=[CFG["streets"][0]["pts"][-1], (2622, 10702), (2638, 10694), (2652, 10688)]),
    dict(id="P1", cls="path", w=3.0, name="south stair", pts=[(2500, 10520), (2530, 10530), (2560, 10524), (2592, 10536), (2622, 10530), (2652, 10546)]),
    dict(id="P2", cls="path", w=3.0, name="middle stair", pts=[(2472, 10604), (2502, 10612), (2532, 10606), (2562, 10614), (2592, 10608), (2626, 10616)]),
    dict(id="P3", cls="path", w=3.0, name="north stair", pts=[(2468, 10676), (2498, 10670), (2528, 10678), (2558, 10670), (2588, 10676), (2616, 10668), (2640, 10672)]),
]
CFG["pool_main"] = ["WH12", "WH02", "WH21", "WH23", "SF01", "SF08", "SF15", "SF16", "WH01", "WH03", "WH04", "WH11", "WH19", "ND01", "ND02", "ND03", "WH08", "WH24", "WH09"]
CFG["pool_lane"] = ["WH12", "WH02", "WH07", "WH09", "WH21", "WH22", "WH23", "WH18", "WH01", "WH03", "WH04", "WH08", "WH11", "WH19", "WH24", "ND01", "ND02", "ND03", "ND04", "WH06", "WH17", "WH14", "WH15", "WH05"]
