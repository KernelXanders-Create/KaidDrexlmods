"""Lantern Quay Hamlet (5-09, op 5) on the real ground: K6 config (PROPOSED).
Ground: a 12-17 % slope falling south-west from the K1 site (84 m) to the top of a
25-40 m sea escarpment; a beach strip 20-40 m wide at its foot. As your review asked,
the quay row moves down to the real shore (the beach strip); a stair climbs the
escarpment; the hamlet above sits on contour terraces (both rows, one level per
segment) joined by the stepped main street (ramp pieces) up to the pocket square."""
import math
import numpy as np
from shapely.geometry import Polygon, LineString, box
from scipy.ndimage import gaussian_filter
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as _plt
PACK = "/tmp/claude-0/-home-user-KaidDrexlmods/68d91108-852d-5f8a-b84e-f7c6d8824e63/scratchpad/handoff_10nov_b/KERNEL_HANDOFF_20261110b"
_X0, _Y0 = 7050, 16300
_H = np.load(PACK + "/towns6/lantern_quay/height_1m.npy"); _HS = gaussian_filter(_H, 5)
SLOPE = Polygon([(7262, 16486), (7330, 16462), (7410, 16444), (7480, 16452), (7530, 16480), (7536, 16560), (7520, 16640),
                 (7450, 16676), (7350, 16676), (7280, 16630), (7250, 16560)])


def contour_street(level, region=SLOPE, spacing=24.0):
    xs = np.arange(_X0, _X0 + _H.shape[1]); ys = np.arange(_Y0, _Y0 + _H.shape[0])
    cs = _plt.contour(xs, ys, _HS, levels=[level]); _plt.close()
    best = None
    for seg in cs.allsegs[0]:
        ls = LineString(seg).intersection(region)
        for p_ in ([ls] if ls.geom_type == "LineString" else list(getattr(ls, "geoms", []))):
            if p_.geom_type == "LineString" and (best is None or p_.length > best.length): best = p_
    n = max(2, int(best.length // spacing))
    pts = [tuple(np.round(best.interpolate(i / n, normalized=True).coords[0], 1)) for i in range(n + 1)]
    if pts[0][0] > pts[-1][0]: pts = pts[::-1]                 # run west to east
    out = [pts[0]]                                            # gentle bends (+-3.5 m) so no run is straight over 80 m
    for i in range(1, len(pts) - 1):
        a, b = np.array(pts[i - 1]), np.array(pts[i + 1]); t = (b - a) / np.linalg.norm(b - a); nn = np.array([-t[1], t[0]])
        out.append(tuple(np.round(np.array(pts[i]) + nn * 3.5 * (1 if i % 2 else -1), 1)))
    return out + [pts[-1]]


def ramp(id_, pts, a, b, name, w=5.0, out_cls=None):
    d = dict(id=id_, cls="lane", w=w, rows="none", name=name, pin_start=a, pin_end=b, ramp=True, pts=pts, smooth=True)
    if out_cls: d["out_cls"] = out_cls
    return d


LEVELS = {"T50": 50, "T58": 58, "T66": 66, "T74": 74, "T82": 82, "T90": 90}
QUAY_Z = 2.0
Q_PTS = [(7296, 16396), (7330, 16381), (7366, 16378), (7400, 16359), (7436, 16358), (7470, 16343)]
_ql = LineString(Q_PTS)
from shapely.ops import substring as _sub
_qw = _sub(_ql, 0, 42)
QUAY = Polygon(list(_qw.offset_curve(-4.0).coords) + list(_qw.offset_curve(-16.0).coords)[::-1])
SPINES = [((7250, 16480), (7330, 16690)), ((7345, 16430), (7440, 16680)), ((7440, 16430), (7540, 16620))]

CFG = dict(
    key="lantern_quay", town="Lantern Quay Hamlet", version="K6 (grid rule) PROPOSED", seed=4,
    tile=PACK + "/towns6/lantern_quay/height_1m.npy", tile_origin=(_X0, _Y0), ground_label="site tile (as built today)",
    target_n=66, garrison_range=(40, 55), square=True,
    view=((7240, 7560), (16310, 16690)),
    inset=dict(view=((7280, 7490), (16320, 16420)), title="the quay row on the beach strip (quay apron 2.0 m)"),
    title="Lantern Quay Hamlet (op 5, 5-09), K6 PROPOSED: quay row on the real shore, terraces above the escarpment, 5 m grid rule",
    labels={"sea escarpment (25-40 m)": (7250, 16440), "beacon path (to 5-M4)": (7470, 16684), "quay": (7380, 16330)},
    streets=[],
    notes=["PROPOSED by Kernel K6, Lantern Quay Hamlet, under the 5 m grid rule (10 Nov late note).",
           "As your review asked, the quay row moves down to the real shore: the beach strip at the foot of the sea escarpment, about 280 m south-south-west of the K1 site point.",
           "The escarpment (25-40 m) is climbed by a stair; the hamlet above sits on contour terraces 7 m apart (both rows, one level per segment).",
           "The main street is stepped: ramp pieces between terraces, pinned to the levels they join, from the stair head up to the pocket square. Boats and air only, so no vehicle road is needed.",
           "Lamps are yours."],
)
for sid, lev in LEVELS.items():
    CFG["streets"].append(dict(id=sid, cls="lane", w=5.0, rows="up", name=f"terrace lane ({lev} m contour)", pts=contour_street(lev), adaptive=True, tol=1.5))
CFG["streets"] += [
    dict(id="Q", cls="lane", w=5.0, rows=-1, name="quay lane (the quay row stands on the beach, doors on the lane)", pts=Q_PTS, adaptive=True, tol=1.5, band=(2.0, 5.0, 8.0)),
]
CFG["pool_main"] = ["WH01", "WH02", "WH03", "WH04", "WH09", "WH11", "WH12", "WH21", "WH23", "WH07", "WH08", "ND03", "ND01", "ND02", "WH24", "WH22", "WH19", "WH18", "SF15", "SF16"]
CFG["pool_lane"] = ["WH01", "WH04", "WH03", "WH11", "WH12", "WH08", "WH24", "ND01", "ND02", "ND03", "ND04", "WH06", "WH17", "WH19", "WH22",
                    "WH23", "WH18", "WH05", "WH02", "WH07", "WH14", "WH15", "WH10", "WH09", "WH21"]
CFG["pool_quay"] = ["SF15", "SF16", "SF13", "WH09", "WH19", "WH03", "WH11", "WH01", "ND03", "WH21", "WH12"]


def _spine_pieces():
    """ramp pieces between neighbouring terraces where each spine line crosses them; the middle spine is the stepped main street"""
    lanes = [k for k in LEVELS]; out = []
    for si, (a, b) in enumerate(SPINES):
        sp = LineString([a, b]); hits = []
        for k in lanes:
            L = LineString([st for st in CFG["streets"] if st["id"] == k][0]["pts"]); x = L.intersection(sp)
            if not x.is_empty: hits.append((k, tuple(np.round(L.interpolate(L.project(x if x.geom_type == "Point" else x.geoms[0])).coords[0], 1))))
        lines = {k: LineString([st for st in CFG["streets"] if st["id"] == k][0]["pts"]) for k, _ in hits}
        for j, ((k0, p0), (k1, p1)) in enumerate(zip(hits[:-1], hits[1:])):
            L1 = lines[k1]; v = L1.project(LineString([p1, p1]).centroid if False else __import__("shapely").geometry.Point(p1))
            cand = [tuple(np.round(L1.interpolate(min(max(v + d, 4), L1.length - 4)).coords[0], 1)) for d in ((40, -40) if si != 1 else (30, -30))]
            p1 = max(cand, key=lambda q: math.dist(q, p0))
            hits[j + 1] = (k1, p1)
            m = ((p0[0] + p1[0]) / 2, (p0[1] + p1[1]) / 2)
            name = "stepped main street, piece" if si == 1 else f"stair lane {si + 1}"
            out.append(ramp(f"S{si + 1}{k0[1:]}", [p0, m, p1], k0, k1, f"{name} ({k0[1:]} to {k1[1:]} m)", w=6.0 if si == 1 else 4.5, out_cls=None))
    return out


CFG["streets"] += _spine_pieces()
_t50 = LineString([st for st in CFG["streets"] if st["id"] == "T50"][0]["pts"])
_head = tuple(np.round(_t50.interpolate(_t50.project(LineString(SPINES[1]).intersection(_t50))).coords[0], 1)) if not LineString(SPINES[1]).intersection(_t50).is_empty else _t50.coords[-1]
CFG["streets"].append(dict(id="QS", cls="path", w=3.5, name="quay stair up the escarpment (foot only)", smooth=False,
                           pts=[(7400, 16364), (7386, 16378), (7404, 16390), (7384, 16402), (7404, 16414), (7386, 16426), (7404, 16436), _head]))


def build(T):
    from town_grid import grid_points
    # the pocket square: on the downhill side of terrace T74, where the stepped main street arrives
    L = T.streets["T74"]["line"]; sp = LineString(SPINES[1]); x = L.intersection(sp); s0 = L.project(x if x.geom_type == "Point" else x.geoms[0]) + 16
    p = np.array(L.interpolate(s0).coords[0]); q = np.array(L.interpolate(s0 + 1).coords[0]); t = (q - p) / np.linalg.norm(q - p); n = np.array([-t[1], t[0]])
    if T.G.z(*(p + n * 10)) > T.G.z(*(p - n * 10)): n = -n                  # n points downhill
    c = p + n * (2.5 + 1.0 + 6.5)
    SQ = [tuple(np.round(c + a * 18 * t + b * 6.5 * n, 1)) for a, b in ((-1, -1), (1, -1), (1, 1), (-1, 1))]
    sq = Polygon(SQ); T.SQ = sq; sqz = T.zst("T74", *p); T.square_z = sqz
    T.extra_pads.append((sq.buffer(1.5), sqz)); T.extra_pads.append((QUAY.buffer(0.5), QUAY_Z))
    for gp in grid_points(sq.buffer(1.5)): T.claims[gp] = sqz
    for gp in grid_points(QUAY.buffer(0.5)): T.claims[gp] = QUAY_Z
    T.draw_polys = [(sq, "#f3e6c4", "#7b2cbf", "square"), (QUAY, "#d9e8f0", "#1f5f8b", "quay apron")]
    T.pad += 1; T._pg = f"P{T.pad:03d}"
    lm = c - 11 * t - 2.0 * n
    yaw = (math.degrees(math.atan2(-n[0], -n[1])) + 180) % 360        # door side (back) toward the lane... the tower is a mast; door into the square
    T.add("SF03", lm[0], lm[1], yaw, "back", sqz, "SQ", "landmark", T._pg)
    T.log.clear()
    for edge in ([SQ[0], SQ[3]], [SQ[1], SQ[2]]):     # the two ends; the downhill (sea) side stays open
        T.pack_edge(list(edge), c, sqz, ["WH09", "WH19", "WH03", "WH11", "ND03", "WH01", "SF15", "SF16"], "square", allow_tall=False, cut_lim=2.5)
    print("RING", dict(T.log))
    for k in ("T74", "T66", "T82", "T58", "T90", "T50", "Q"):
        pool, role = (T.cfg["pool_quay"], "quay") if k == "Q" else ((T.cfg["pool_main"], "main") if k == "T74" else (T.cfg["pool_lane"], "lane"))
        for side in T.row_sides(T.streets[k]):
            n0 = len(T.B); T.log.clear(); T.pack_row(k, side, pool, role, max_depth=16.6, cut_lim=2.5, sci_first=0.3 if k == "Q" else 0.0); print(k, side, len(T.B) - n0, dict(T.log))
    cm = c + 9 * t
    T.comps = [dict(name_or_role="fish market or net stalls on the square (whole comp, your pick)", x=round(float(cm[0]), 1), y=round(float(cm[1]), 1), yaw_deg=round(yaw, 1), footprint_m=[9.5, 9.4], pad_z_m=sqz),
               dict(name_or_role="quay: boat slips, fishing boats, net racks (whole comp, your pick)", x=round(float(QUAY.centroid.x), 1), y=round(float(QUAY.centroid.y), 1), yaw_deg=17.0, footprint_m=[34.0, 8.0], pad_z_m=QUAY_Z)]
    T.square_out = {"polygon": [list(p_) for p_ in SQ], "level_z_m": sqz, "landmark_building_id": next(b["id"] for b in T.B if b["role"] == "landmark"),
                    "open_side": "south-west, toward the sea"}
