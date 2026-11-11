"""Kamar Village (6-01, op 6) on the real ground: K6 config (PROPOSED).
The K1 site point (16850, 11600) sits on a 25-35 % slope. 150-200 m west lies a gentle upland
shoulder (240-258 m) with a shallow north-south hollow at x ~16640 between a low knob (257 m,
east) and the massif slope (west): the village goes there, along the hollow (the "ravine").
As your review asked, the quay is a separate small landing on the beach strip below the sea
cliff, reached by a path down. Ground: the site window and the shore window stitched together
(identical where they overlap)."""
import math
import numpy as np
from shapely.geometry import Polygon, LineString
from shapely.ops import substring
SCRATCH = "/tmp/claude-0/-home-user-KaidDrexlmods/68d91108-852d-5f8a-b84e-f7c6d8824e63/scratchpad"
PACK = SCRATCH + "/handoff_10nov_b/KERNEL_HANDOFF_20261110b"


def bend(pts, amp=4.0):
    out = [pts[0]]
    for i in range(1, len(pts) - 1):
        a, b = np.array(pts[i - 1], float), np.array(pts[i + 1], float); t = (b - a) / np.linalg.norm(b - a); n = np.array([-t[1], t[0]])
        out.append(tuple(np.round(np.array(pts[i]) + n * amp * (1 if i % 2 else -1), 1)))
    return out + [pts[-1]]


def ramp(id_, pts, a, b, name, w=4.5):
    return dict(id=id_, cls="lane", w=w, rows="none", name=name, pin_start=a, pin_end=b, ramp=True, pts=pts, smooth=True)


M_PTS = [(16648, 11506), (16642, 11540), (16638, 11576), (16640, 11612), (16642, 11648), (16640, 11684), (16644, 11720), (16652, 11756)]
E_PTS = [(16706, 11520), (16712, 11556), (16714, 11592), (16712, 11628), (16714, 11664), (16716, 11700), (16722, 11736)]
WL_PTS = [(16584, 11540), (16582, 11576), (16584, 11612), (16586, 11648), (16588, 11684), (16592, 11720)]
NL_PTS = [(16600, 11790), (16632, 11796), (16664, 11794), (16696, 11790), (16728, 11784)]
Q_PTS = [(17198, 11232), (17192, 11206), (17199, 11178), (17193, 11150), (17198, 11124)]
QUAY_Z = 2.0
_ql = LineString(Q_PTS)
QUAY = Polygon(list(substring(_ql, 30, 80).offset_curve(4.5).coords) + list(substring(_ql, 30, 80).offset_curve(13.0).coords)[::-1])

CFG = dict(
    key="kamar_village", town="Kamar Village", version="K6 (grid rule) PROPOSED", seed=21,
    tile=SCRATCH + "/kamar_merged/height_merged_1m.npy", tile_origin=(16500, 11103), ground_label="site + shore windows stitched (as built today)",
    target_n=60, garrison_range=(40, 55), square=True,
    view=((16540, 16800), (11480, 11830)),
    inset=dict(view=((17140, 17260), (11130, 11280)), title="the quay landing on the beach strip (about 650 m south-east, 2.0 m)"),
    title="Kamar Village (op 6, 6-01), K6 PROPOSED: the ravine village on the upland shoulder, quay landing on the beach, 5 m grid rule",
    labels={"ravine road (to the massif, west)": (16548, 11780), "path down to the quay (past the K1 site)": (16700, 11515)},
    streets=[
        dict(id="M", cls="main", w=6.5, rows="both", name="main street (6.5 m) along the hollow", pts=bend(M_PTS), adaptive=True, gap=16, drop_grade=0.12),
        dict(id="E", cls="lane", w=5.0, rows="both", name="knob lane (east)", pts=bend(E_PTS), adaptive=True),
        dict(id="WL", cls="lane", w=5.0, rows="both", name="massif lane (west)", pts=bend(WL_PTS), adaptive=True),
        dict(id="NL", cls="lane", w=5.0, name="north lane (over the bench edge)", rows="up", pts=bend(NL_PTS, 3.0), adaptive=True),
        ramp("C1", [(16640, 11620), (16660, 11624), (16684, 11622), (16712, 11628)], "M", "E", "cross lane east 1"),
        ramp("C3", [(16639, 11580), (16620, 11578), (16600, 11580), (16582, 11576)], "M", "WL", "cross lane west 1"),
        ramp("C5", [(16652, 11756), (16668, 11766), (16676, 11780), (16680, 11793)], "M", "NL", "lane to the north lane"),
        dict(id="EE", cls="lane", w=4.5, rows="up", name="east edge lane (over the slope down to the K1 site)", pts=bend([(16786, 11566), (16788, 11590), (16786, 11614), (16789, 11638), (16788, 11662), (16792, 11694)], 4.0), adaptive=True),
        ramp("C6", [(16714, 11664), (16740, 11666), (16766, 11664), (16789, 11662)], "E", "EE", "cross lane to the east edge lane"),
        dict(id="QP", cls="path", w=3.0, name="path down to the quay landing (ASSUMED line, past the K1 site; yours to route)", smooth=False,
             pts=[(16706, 11520), (16760, 11500), (16850, 11560), (16963, 11454), (17040, 11380), (17110, 11300), (17160, 11250), (17198, 11232)]),
        dict(id="QL", cls="lane", w=5.0, rows=-1, name="quay landing lane (the landing row stands at the cliff foot, doors to the sea)", pts=Q_PTS, adaptive=True, tol=1.5),
    ],
    notes=["PROPOSED by Kernel K6, Kamar Village, under the 5 m grid rule (10 Nov late note).",
           "The village moves about 190 m west of the K1 site point, from a 25-35 % slope onto the gentle upland shoulder (240-258 m); the main street runs along the shallow hollow between the knob and the massif.",
           "Each street segment and its two rows are one level; cross lanes are ramps meeting the streets at their levels.",
           "The quay is a separate small landing on the beach strip about 650 m south-east, at 2.0 m, reached by a path down the slope (ASSUMED line, yours to route).",
           "Lamps are yours."],
)
CFG["pool_main"] = ["WH01", "WH02", "WH03", "WH04", "WH09", "WH11", "WH12", "WH21", "WH23", "WH07", "WH08", "ND03", "ND05", "WH24", "WH10", "WH14", "WH22", "WH19", "WH18", "SF15", "SF16", "SF01", "SF08"]
CFG["pool_lane"] = ["WH01", "WH04", "WH03", "WH11", "WH12", "WH08", "WH24", "ND01", "ND03", "ND04", "WH06", "WH17", "WH19", "WH22",
                    "WH23", "WH18", "WH05", "WH02", "WH07", "WH14", "WH15", "WH10", "WH09", "WH21"]
CFG["pool_quay"] = ["SF15", "SF16", "WH09", "WH19", "WH03", "WH11", "WH01", "WH12"]


def build(T):
    from town_grid import grid_points
    # the square: on the east side of the main street, in the middle of the hollow
    L = T.streets["M"]["line"]; s0 = L.project(__import__("shapely").geometry.Point(16640, 11684))
    p = np.array(L.interpolate(s0).coords[0]); q = np.array(L.interpolate(s0 + 1).coords[0]); t = (q - p) / np.linalg.norm(q - p); n = np.array([t[1], -t[0]])  # east
    c = p + n * (3.25 + 1.0 + 8.0)
    SQ = [tuple(np.round(c + a * 17 * t + b * 8 * n, 1)) for a, b in ((-1, -1), (1, -1), (1, 1), (-1, 1))]
    sq = Polygon(SQ); T.SQ = sq; sqz = T.zst("M", *p); T.square_z = sqz
    T.extra_pads.append((sq.buffer(1.5), sqz)); T.extra_pads.append((QUAY.buffer(0.5), QUAY_Z))
    for gp in grid_points(sq.buffer(1.5)): T.claims[gp] = sqz
    for gp in grid_points(QUAY.buffer(0.5)): T.claims[gp] = QUAY_Z
    T.draw_polys = [(sq, "#f3e6c4", "#7b2cbf", "square"), (QUAY, "#d9e8f0", "#1f5f8b", "quay apron")]
    T.pad += 1; T._pg = f"P{T.pad:03d}"
    lm = c + 9 * t + 3.0 * n
    yaw = (math.degrees(math.atan2(-n[0], -n[1]))) % 360
    T.add("SF02", lm[0], lm[1], (yaw + 180) % 360, "back", sqz, "SQ", "landmark", T._pg)      # condenser tower stand-in; its door (back) faces the main street
    T.log.clear()
    for edge in ([SQ[0], SQ[3]], [SQ[1], SQ[2]], [SQ[3], SQ[2]]):     # both ends and the far (east) side; the main street side is open
        T.pack_edge(list(edge), c, sqz, ["WH09", "WH19", "WH03", "WH11", "ND03", "WH01", "SF15", "SF16", "SF01"], "square", allow_tall=False, cut_lim=2.5)
    print("RING", dict(T.log))
    for k in ("M", "E", "WL", "EE", "NL", "QL"):
        pool, role = (T.cfg["pool_quay"], "quay") if k == "QL" else ((T.cfg["pool_main"], "main") if k == "M" else (T.cfg["pool_lane"], "lane"))
        for side in T.row_sides(T.streets[k]):
            n0 = len(T.B); T.log.clear(); T.pack_row(k, side, pool, role, max_depth=16.6, cut_lim=2.5, sci_first=0.3 if k in ("M", "QL") else 0.0); print(k, side, len(T.B) - n0, dict(T.log))
    cm = c - 8 * t
    T.comps = [dict(name_or_role="water cistern or market stalls on the square (whole comp, your pick)", x=round(float(cm[0]), 1), y=round(float(cm[1]), 1), yaw_deg=round(yaw, 1), footprint_m=[9.5, 9.4], pad_z_m=sqz),
               dict(name_or_role="quay landing: boat slips and a small jetty (whole comp, your pick)", x=round(float(QUAY.centroid.x), 1), y=round(float(QUAY.centroid.y), 1), yaw_deg=0.0, footprint_m=[7.0, 40.0], pad_z_m=QUAY_Z)]
    T.square_out = {"polygon": [list(p_) for p_ in SQ], "level_z_m": sqz, "landmark_building_id": next(b["id"] for b in T.B if b["role"] == "landmark"),
                    "open_side": "west, onto the main street"}
