"""Causeway Foot (4-M3, op 4) on the real ground: K6 config (PROPOSED).
Ground: a gentle slope (8-15 %) falling south-south-east to the sea; the causeway lands
on the beach at the east end. Kept from K1: the 8 m AI main street from the causeway
landfall west to the south-arm road, the fork square where the slope road leaves for the
monastery, the causeway gatehouse halls. New for the grid rule: lanes on the contours
about 45 m apart, each street segment and its two rows one level, cross lanes as ramps."""
import math
import numpy as np
from shapely.geometry import Polygon
PACK = "/tmp/claude-0/-home-user-KaidDrexlmods/68d91108-852d-5f8a-b84e-f7c6d8824e63/scratchpad/handoff_10nov_b/KERNEL_HANDOFF_20261110b"

CAUSEWAY_END = (14286.0, 8181.0)          # K1's causeway landfall (ASSUMED until checked against your causeway road)
CAUSEWAY_Z = 1.5                          # ASSUMED deck level at the landfall (ground there 0.5 m)

M_PTS = [CAUSEWAY_END, (14262, 8193), (14236, 8203), (14210, 8213), (14182, 8222), (14154, 8231), (14126, 8236), (14098, 8231),
         (14072, 8218), (14050, 8202)]
UA_PTS = [(14030, 8236), (14058, 8254), (14088, 8270), (14118, 8280), (14148, 8282), (14178, 8280), (14208, 8274), (14238, 8266),
          (14268, 8254), (14300, 8240), (14330, 8230)]
UB_PTS = [(14060, 8300), (14092, 8316), (14124, 8326), (14156, 8330), (14188, 8330), (14220, 8322), (14252, 8314), (14284, 8302),
          (14316, 8290), (14346, 8282)]
UC_PTS = [(14070, 8352), (14100, 8365), (14132, 8375), (14164, 8378), (14196, 8376), (14228, 8368), (14260, 8358), (14292, 8346)]
LO_PTS = [(14036, 8160), (14064, 8172), (14092, 8182), (14120, 8187)]
R2_PTS = [(14050, 8202), (14026, 8170), (13998, 8159), (13965, 8150), (13929, 8142), (13887, 8136), (13849, 8133)]

# the fork square: on the downhill side of the main street, open to the beach (south)
_c0 = np.array([14182.0, 8222.0]); _u = np.array([math.sin(math.radians(108)), math.cos(math.radians(108))]); _v = np.array([math.sin(math.radians(198)), math.cos(math.radians(198))])
_c = _c0 + 15.0 * _v
SQ_PTS = [tuple(np.round(_c + a * 22 * _u + b * 9 * _v, 1)) for a, b in ((-1, -1), (1, -1), (1, 1), (-1, 1))]


def bend(pts, amp=4.0):
    """push the inner points across the line by +-amp m, alternately, so no run is straight for more than about 75 m"""
    out = [pts[0]]
    for i in range(1, len(pts) - 1):
        a, b = np.array(pts[i - 1], float), np.array(pts[i + 1], float); t = (b - a) / np.linalg.norm(b - a); n = np.array([-t[1], t[0]])
        out.append(tuple(np.round(np.array(pts[i]) + n * amp * (1 if i % 2 else -1), 1)))
    return out + [pts[-1]]


def ramp(id_, pts, a, b, name, w=4.5):
    return dict(id=id_, cls="lane", w=w, rows="none", name=name, pin_start=a, pin_end=b, ramp=True, pts=pts, smooth=True)


CFG = dict(
    key="causeway_foot_v2", town="Causeway Foot", version="K6 v2 (graded with the 11 Nov grader) PROPOSED", seed=8,
    tile=PACK + "/towns6/causeway_foot/height_1m.npy", tile_origin=(13750, 7900), ground_label="site tile (as built today)",
    target_n=82, garrison_range=(40, 55), square=True,
    view=((13990, 14370), (8110, 8420)),
    inset=dict(view=((14130, 14240), (8170, 8250)), title="the fork square (one level)"),
    title="Causeway Foot (op 4, 4-M3), K6 PROPOSED: the causeway road town on the real ground, 5 m grid rule",
    labels={"causeway (to the Cinder Cone)": (14290, 8170), "to the south-arm road": (13995, 8150), "slope road to the monastery": (14176, 8412),
            "beach": (14200, 8128)},
    streets=[
        dict(id="M", cls="main", w=8.0, rows="both", name="main street (AI road, 8 m)", pin_start=CAUSEWAY_Z, pts=bend(M_PTS, 4.0),
             adaptive=True, tol=1.6, maxlen=64, minlen=14, gap=16, drop_grade=0.12),
        dict(id="UA", cls="lane", w=5.0, rows="both", name="upper lane", pts=bend(UA_PTS), gaps_at=[(14090, 8271), (14168, 8281), (14250, 8261)]),
        dict(id="UB", cls="lane", w=5.0, rows="both", name="top lane", pts=bend(UB_PTS), gaps_at=[(14168, 8330), (14256, 8313)]),
        dict(id="UC", cls="lane", w=5.0, rows="both", name="crest lane", pts=bend(UC_PTS), gaps_at=[(14166, 8378), (14232, 8367)]),
        ramp("C7", [(14168, 8330), (14164, 8346), (14163, 8362), (14166, 8378)], "UB", "UC", "slope road, upper piece", w=6.0),
        ramp("C8", [(14256, 8313), (14238, 8330), (14234, 8350), (14232, 8367)], "UB", "UC", "east top cross lane"),
        dict(id="LO", cls="lane", w=5.0, rows="both", name="lower lane (beach side)", pts=LO_PTS),
        ramp("C1", [(14080, 8222), (14084, 8240), (14088, 8256), (14090, 8271)], "M", "UA", "west cross lane"),
        ramp("C2", [(14160, 8229), (14164, 8248), (14166, 8264), (14168, 8281)], "M", "UA", "slope road, lower piece (fork square to the upper lane)", w=6.0),
        ramp("C3", [(14230, 8205), (14238, 8224), (14244, 8242), (14250, 8261)], "M", "UA", "east cross lane"),
        ramp("C4", [(14168, 8281), (14164, 8298), (14166, 8314), (14168, 8330)], "UA", "UB", "slope road, middle piece", w=6.0),
        ramp("C5", [(14250, 8261), (14256, 8280), (14254, 8296), (14256, 8313)], "UA", "UB", "east upper cross lane"),
        ramp("C6", [(14098, 8231), (14104, 8214), (14112, 8200), (14120, 8187)], "M", "LO", "beach lane"),
        dict(id="R3", cls="path", out_cls="road", w=6.0, name="slope road to the monastery (out of town)", pts=[(14166, 8378), (14168, 8392), (14171, 8403), (14168, 8426), (14165, 8442)]),
        dict(id="R2", cls="path", out_cls="main", w=8.0, name="south-arm road (out of town, AI road)", pts=bend(R2_PTS, 3.0)),
        dict(id="R4", cls="path", out_cls="road", w=4.5, name="beach track", pts=[(14120, 8187), (14134, 8170), (14150, 8156), (14170, 8146), (14190, 8140)]),
    ],
    notes=["PROPOSED by Kernel K6, Causeway Foot, under the 5 m grid rule (10 Nov late note).",
           "The main street is the 8 m AI road from the causeway landfall to the south-arm road. Its level segments carry both rows; levels change only across 16 m gaps where a cross lane meets it, at up to 12 %.",
           "The fork square is one level, on the downhill side of the main street where the slope road leaves for the monastery; its south side stays open toward the beach.",
           "The causeway landfall point and its deck level (1.5 m) are ASSUMED from K1; check them against your causeway road.",
           "Lamps are yours."],
)
CFG["pool_main"] = ["SF01", "SF08", "SF15", "SF16", "IN01", "IN02", "IN03", "WH01", "WH02", "WH03", "WH04", "WH09", "WH11", "WH21", "WH23", "WH12",
                    "WH07", "WH08", "ND03", "ND05", "ND01", "ND02", "WH24", "WH22", "WH19", "WH18"]
CFG["pool_lane"] = ["WH01", "WH04", "WH03", "WH11", "WH12", "WH08", "WH24", "ND01", "ND02", "ND03", "ND04", "WH06", "WH17", "WH19", "WH22",
                    "WH23", "WH18", "WH05", "SF16", "SF15", "WH02", "WH07", "WH14", "WH15"]


def build(T):
    from gtown import square_site
    SQ, sqz, c, t, n = square_site(T, "M", 32.0, 16.0, near=(14182, 8222), side="down")
    sq = Polygon(SQ); T.SQ = sq; T.square_z = sqz
    T.draw_polys = [(sq, "#f3e6c4", "#7b2cbf", "square")]
    T.init_grader()
    # landmark: the causeway signal pylon (SF02, 20.5 m, stands in for it), on the square's east half, door toward the main street
    T.pad += 1; T._pg = f"P{T.pad:03d}"
    lm = c + 9 * t + 1.0 * n
    yaw = (np.degrees(np.arctan2(n[0], n[1]))) % 360
    T.add("SF02", lm[0], lm[1], yaw, "back", sqz, "SQ", "landmark", T._pg)
    for edge in ([SQ[3], SQ[0]], [SQ[1], SQ[2]]):       # the two ends; the beach side stays open
        T.pack_edge(list(edge), c, sqz, ["SF15", "SF16", "SF01", "SF08", "SF03", "WH09", "WH02", "ND03", "WH19", "WH11"], "square", allow_tall=False, cut_lim=4.0)
    for k in ("M", "UA", "UB", "UC", "LO"):
        pool, role, sci = (T.cfg["pool_main"], "main", 0.5) if k == "M" else (T.cfg["pool_lane"], "lane", 0.0)
        for side in T.row_sides(T.streets[k]):
            T.pack_row(k, side, pool, role, max_depth=17.0, cut_lim=4.0, sci_first=sci)
    cm = c - 8 * t
    T.comps = [dict(name_or_role="fork square: market or checkpoint group (whole comp, your pick)", x=round(float(cm[0]), 1), y=round(float(cm[1]), 1), yaw_deg=round(float(yaw), 1), footprint_m=[9.5, 9.4], pad_z_m=sqz)]
    lmk = [b["id"] for b in T.B if b["role"] == "landmark"]
    T.square_out = {"polygon": [list(p) for p in SQ], "level_z_m": sqz, "landmark_building_id": lmk[0] if lmk else None, "open_side": "south, toward the beach"}
