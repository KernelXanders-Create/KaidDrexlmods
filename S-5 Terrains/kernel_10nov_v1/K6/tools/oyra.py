"""Oyra (7-M2, op 7) on the real ground: K6 config (PROPOSED).
As your review asked: the cliff-edge row moves onto the real break of slope (the south-west
corner of the window) and the town turns to face south over the lagoon. The ground there is
a flat rim at 130-131 m running WNW-ESE, about 100 m deep, with a 100 m drop to the lagoon on
its south-west side and a gentle back-slope (5-10 %) falling north-east. The rim street runs
about 22 m inside the edge (its south row stands on the edge); two lanes follow behind it,
about 45 m apart; the rim square sits on the edge, open to the lagoon."""
import math
import numpy as np
from shapely.geometry import Polygon, LineString, Point
PACK = "/tmp/claude-0/-home-user-KaidDrexlmods/68d91108-852d-5f8a-b84e-f7c6d8824e63/scratchpad/handoff_10nov_b/KERNEL_HANDOFF_20261110b"


def bend(pts, amp=4.0):
    out = [pts[0]]
    for i in range(1, len(pts) - 1):
        a, b = np.array(pts[i - 1], float), np.array(pts[i + 1], float); t = (b - a) / np.linalg.norm(b - a); n = np.array([-t[1], t[0]])
        out.append(tuple(np.round(np.array(pts[i]) + n * amp * (1 if i % 2 else -1), 1)))
    return out + [pts[-1]]


def ramp(id_, pts, a, b, name, w=4.5):
    return dict(id=id_, cls="lane", w=w, rows="none", name=name, pin_start=a, pin_end=b, ramp=True, pts=pts, smooth=True)


R_PTS = [(11592, 12378), (11634, 12342), (11682, 12332), (11732, 12322), (11782, 12304), (11830, 12280), (11862, 12256), (11888, 12222), (11906, 12190)]
U_PTS = [(11600, 12428), (11650, 12408), (11700, 12392), (11750, 12380), (11800, 12366), (11850, 12346), (11890, 12320), (11926, 12290), (11950, 12256)]
V_PTS = [(11640, 12470), (11690, 12450), (11740, 12432), (11790, 12420), (11840, 12404), (11886, 12384), (11930, 12356), (11966, 12324)]

CFG = dict(
    key="oyra", town="Oyra", version="K6 (grid rule) PROPOSED", seed=7,
    tile=PACK + "/towns6/oyra/height_1m.npy", tile_origin=(11570, 12150), ground_label="site tile (as built today)",
    target_n=100, garrison_range=(40, 55), square=True,
    view=((11570, 12000), (12150, 12500)),
    inset=dict(view=((11690, 11800), (12260, 12340)), title="the rim square on the cliff edge (one level)"),
    title="Oyra (op 7, 7-M2), K6 PROPOSED: the rim town on the real break of slope, facing south over the lagoon, 5 m grid rule",
    labels={"the lagoon (100 m below)": (11640, 12200), "rim path (to the Narrows batteries)": (11575, 12392), "crest road (to the Chora)": (11905, 12172),
            "north road (to Oyra Head)": (11930, 12470)},
    streets=[
        dict(id="R", cls="main", w=6.5, rows="both", name="rim street (main, 6.5 m)", pts=bend(R_PTS, 6.0), adaptive=True, gap=16, drop_grade=0.12),
        dict(id="U", cls="lane", w=5.0, rows="both", name="upper lane", pts=bend(U_PTS, 5.5), adaptive=True),
        dict(id="V", cls="lane", w=5.0, rows="both", name="back lane", pts=bend(V_PTS, 6.5), adaptive=True),
        ramp("C1", [(11655, 12328), (11662, 12350), (11666, 12376), (11668, 12402)], "R", "U", "cross lane 1"),
        ramp("C2", [(11805, 12286), (11812, 12310), (11816, 12336), (11818, 12360)], "R", "U", "cross lane 2"),
        ramp("C3", [(11700, 12392), (11708, 12410), (11714, 12428), (11716, 12441)], "U", "V", "cross lane 3"),
        ramp("C4", [(11870, 12332), (11878, 12350), (11884, 12368), (11888, 12384)], "U", "V", "cross lane 4"),
        dict(id="LO1", cls="path", w=3.0, name="look-out stair to the cliff edge (dead end on purpose)", pts=[(11636, 12338), (11626, 12322), (11614, 12306)], smooth=False),
        dict(id="LO2", cls="path", w=3.0, name="look-out stair to the cliff edge (dead end on purpose)", pts=[(11862, 12252), (11848, 12240), (11834, 12230)], smooth=False),
    ],
    notes=["PROPOSED by Kernel K6, Oyra, under the 5 m grid rule (10 Nov late note).",
           "As your review asked, the cliff-edge row sits on the real break of slope in the window's south-west corner and the town faces south over the lagoon (about 100 m below).",
           "The rim is flat (130-131 m), so the rim street and both its rows are nearly one level; the lanes behind step down the gentle back-slope, one level per segment.",
           "Look-out stairs at two lane ends reach the cliff edge (dead ends on purpose).",
           "Roads out: the rim path (west-north-west), the crest road (south-east) and the north road (to Oyra Head) are yours to join at the street ends.",
           "Lamps are yours."],
)
CFG["pool_main"] = ["SF01", "SF08", "SF15", "SF16", "IN01", "IN02", "WH01", "WH02", "WH03", "WH04", "WH09", "WH11", "WH12", "WH21", "WH23", "WH07", "WH08",
                    "ND03", "ND01", "ND02", "ND05", "WH24", "WH22", "WH19", "WH18"]
CFG["pool_lane"] = ["WH01", "WH04", "WH03", "WH11", "WH12", "WH08", "WH24", "ND01", "ND02", "ND03", "ND04", "WH06", "WH17", "WH19", "WH22",
                    "WH23", "WH18", "WH05", "WH02", "WH07", "WH14", "WH15", "WH10", "WH09", "WH21"]


def build(T):
    from town_grid import grid_points
    L = T.streets["R"]["line"]; s0 = L.project(Point(11712, 12326))
    p = np.array(L.interpolate(s0).coords[0]); q = np.array(L.interpolate(s0 + 1).coords[0]); t = (q - p) / np.linalg.norm(q - p); n = np.array([t[1], -t[0]])
    if T.G.z(*(p + n * 25)) > T.G.z(*(p - n * 25)): n = -n          # n points toward the cliff (downhill)
    c = p + n * (3.25 + 1.0 + 7.0)
    SQ = [tuple(np.round(c + a * 20 * t + b * 7 * n, 1)) for a, b in ((-1, -1), (1, -1), (1, 1), (-1, 1))]
    sq = Polygon(SQ); T.SQ = sq; sqz = T.zst("R", *p); T.square_z = sqz
    T.extra_pads.append((sq.buffer(1.5), sqz))
    for gp in grid_points(sq.buffer(1.5)): T.claims[gp] = sqz
    T.draw_polys = [(sq, "#f3e6c4", "#7b2cbf", "square")]
    T.pad += 1; T._pg = f"P{T.pad:03d}"
    lm = c + 10 * t + 2.2 * n
    yaw = (math.degrees(math.atan2(-n[0], -n[1]))) % 360
    T.add("SF02", lm[0], lm[1], (yaw + 180) % 360, "back", sqz, "SQ", "landmark", T._pg)      # Narrows Signal Lantern stand-in; door toward the rim street
    T.log.clear()
    for edge in ([SQ[0], SQ[3]], [SQ[1], SQ[2]]):       # both ends; the cliff side stays open to the lagoon
        T.pack_edge(list(edge), c, sqz, ["IN01", "IN02", "SF15", "SF16", "SF01", "SF08", "WH09", "WH19", "WH03"], "square", allow_tall=False, cut_lim=2.5)
    print("RING", dict(T.log))
    for k in ("R", "U", "V"):
        pool, role, sci = (T.cfg["pool_main"], "main", 0.4) if k == "R" else (T.cfg["pool_lane"], "lane", 0.0)
        for side in T.row_sides(T.streets[k]):
            n0 = len(T.B); T.log.clear(); T.pack_row(k, side, pool, role, max_depth=16.6, cut_lim=2.5, sci_first=sci); print(k, side, len(T.B) - n0, dict(T.log))
    cm = c - 9 * t
    T.comps = [dict(name_or_role="CIS checkpoint or market group on the rim square (whole comp, your pick)", x=round(float(cm[0]), 1), y=round(float(cm[1]), 1), yaw_deg=round(yaw, 1), footprint_m=[9.5, 9.4], pad_z_m=sqz)]
    T.square_out = {"polygon": [list(p_) for p_ in SQ], "level_z_m": sqz, "landmark_building_id": next(b["id"] for b in T.B if b["role"] == "landmark"),
                    "open_side": "south-west, over the cliff to the lagoon"}
