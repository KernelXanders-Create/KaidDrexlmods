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
    key="oyra_v2", town="Oyra", version="K6 v2 (graded with the 11 Nov grader) PROPOSED", seed=7,
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
    ],
    notes=["PROPOSED by Kernel K6, Oyra, under the 5 m grid rule (10 Nov late note).",
           "As your review asked, the cliff-edge row sits on the real break of slope in the window's south-west corner and the town faces south over the lagoon (about 100 m below).",
           "The rim is flat (130-131 m), so the rim street and both its rows are nearly one level; the lanes behind step down the gentle back-slope, one level per segment.",
           "Two look-out stairs (dead ends on purpose) are not drawn as streets, since they are steeper than the 31 degree bank: build them as stair pieces from the rim street at about (11636, 12338) and (11862, 12252) to the cliff edge.",
           "Roads out: the rim path (west-north-west), the crest road (south-east) and the north road (to Oyra Head) are yours to join at the street ends.",
           "Lamps are yours."],
)
CFG["pool_main"] = ["SF01", "SF08", "SF15", "SF16", "IN01", "IN02", "WH01", "WH02", "WH03", "WH04", "WH09", "WH11", "WH12", "WH21", "WH23", "WH07", "WH08",
                    "ND03", "ND01", "ND02", "ND05", "WH24", "WH22", "WH19", "WH18"]
CFG["pool_lane"] = ["WH01", "WH04", "WH03", "WH11", "WH12", "WH08", "WH24", "ND01", "ND02", "ND03", "ND04", "WH06", "WH17", "WH19", "WH22",
                    "WH23", "WH18", "WH05", "WH02", "WH07", "WH14", "WH15", "WH10", "WH09", "WH21"]


def build(T):
    from gtown import standard_build
    rows = [("R", T.cfg["pool_main"], "main", 0.4, 16.6)] + [(k, T.cfg["pool_lane"], "lane", 0.0, 16.6) for k in ("U", "V")]
    standard_build(T, "R", 36.0, 12.0, (11712, 12326), "down", ("ND07", "front"), ["IN01", "IN02", "SF15", "SF16", "SF01", "SF08", "WH09", "WH19", "WH03"], rows,
                   comps=[("CIS checkpoint or market group on the rim square (whole comp, your pick)", -9.0, 0.0, (9.5, 9.4))], open_side="south-west, over the cliff to the lagoon")
