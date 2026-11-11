"""Kastro Quay (5-M3, op 5) on the real ground: K6 config (PROPOSED).
Option (b) of your review: the whole town on the plateau, with a quay only.
Ground (shore window 4263..4963, 16423..17123): a nearly flat shelf at 115-140 m between the
acropolis slopes (west) and a 130 m sea cliff (east). Below the cliff, a small cove sheltered
by a low rock spit at 4800, 16740-16830 takes the quay apron; a cliff stair (and a cargo lift,
as a comp) links it to the port square on the cliff top."""
import math
import numpy as np
from shapely.geometry import Polygon, box
PACK = "/tmp/claude-0/-home-user-KaidDrexlmods/68d91108-852d-5f8a-b84e-f7c6d8824e63/scratchpad/handoff_10nov_b/KERNEL_HANDOFF_20261110b"


def bend(pts, amp=4.0):
    """push the inner points across the line by +-amp m, alternately, so no run is straight for more than about 75 m"""
    out = [pts[0]]
    for i in range(1, len(pts) - 1):
        a, b = np.array(pts[i - 1], float), np.array(pts[i + 1], float); t = (b - a) / np.linalg.norm(b - a); n = np.array([-t[1], t[0]])
        out.append(tuple(np.round(np.array(pts[i]) + n * amp * (1 if i % 2 else -1), 1)))
    return out + [pts[-1]]


def ramp(id_, pts, a, b, name, w=4.5):
    return dict(id=id_, cls="lane", w=w, rows="none", name=name, pin_start=a, pin_end=b, ramp=True, pts=pts, smooth=True)


M_PTS = [(4628, 16660), (4630, 16700), (4626, 16740), (4622, 16780), (4620, 16820), (4620, 16860), (4624, 16890), (4626, 16915), (4618, 16940),
         (4608, 16965), (4604, 16995), (4600, 17040)]
W_PTS = [(4586, 16636), (4574, 16680), (4570, 16720), (4568, 16760), (4568, 16800), (4570, 16840), (4574, 16880)]
BS_PTS = [(4586, 16636), (4556, 16640), (4524, 16648), (4496, 16660)]
B1_PTS = [(4496, 16660), (4490, 16690), (4488, 16720), (4488, 16752)]
SQ_PTS = [(4632, 16796), (4676, 16796), (4678, 16848), (4632, 16850)]
QUAY = box(4776, 16786, 4806, 16806); QUAY_Z = 2.0
STAIR = [(4676, 16822), (4700, 16832), (4712, 16816), (4724, 16836), (4736, 16818), (4746, 16838), (4756, 16816), (4764, 16834),
         (4772, 16814), (4780, 16826), (4788, 16806)]

CFG = dict(
    key="kastro_quay_v2", town="Kastro Quay", version="K6 v2 (option b, graded with the 11 Nov grader) PROPOSED", seed=19,
    tile=PACK + "/towns6/kastro_quay/shore_height_1m.npy", tile_origin=(4263, 16423), ground_label="shore window (as built today)",
    target_n=62, garrison_range=(40, 55), square=True,
    view=((4440, 4830), (16610, 17070)),
    inset=dict(view=((4620, 4820), (16760, 16870)), title="port square, cliff stair and quay (apron 2.0 m)"),
    title="Kastro Quay (op 5, 5-M3), K6 PROPOSED: the town on the cliff-top plateau, quay in the cove below, 5 m grid rule",
    labels={"south port (to the citadel road)": (4590, 16622), "north port": (4570, 17058), "cove and quay": (4790, 16770), "Kastro Strait": (4810, 16700),
            "sea cliff (130 m)": (4730, 16900)},
    streets=[
        dict(id="M", cls="main", w=7.0, rows="both", name="main street (7 m): along the plateau ridge, past the port square, down to the north basin", pts=bend(M_PTS, 5.0), adaptive=True, hold=(4620, 16823, 26.0), gap=16, drop_grade=0.12),
        dict(id="W", cls="lane", w=5.0, rows="both", name="west lane (on the plateau's west flank)", pts=bend(W_PTS), adaptive=True),
        dict(id="N1", cls="lane", w=5.0, rows="both", name="basin lane", pin_start="M", pts=bend([(4606, 16975), (4630, 16979), (4652, 16975), (4672, 16979)], 2.0), adaptive=True),
        dict(id="BS", cls="lane", w=5.0, rows="both", name="bowl lane south (from the south port into the old crater)", pin_start="W", pts=bend(BS_PTS, 2.0), adaptive=True),
        dict(id="B1", cls="lane", w=5.0, rows="both", name="bowl lane (the lower quarter in the old crater)", pin_start="BS", pts=bend(B1_PTS, 3.0), adaptive=True),
        dict(ramp("C1", [(4569, 16800), (4586, 16794), (4603, 16786), (4619, 16778)], "W", "M", "cross lane (west lane to the main street)"), landing=8.0, keep_landings=True),
        ramp("C2", [(4574, 16880), (4588, 16904), (4604, 16924), (4618, 16940)], "W", "M", "cross lane north (west lane to the main street)"),
    ],
    notes=["PROPOSED by Kernel K6, Kastro Quay, option (b) of your review: the whole town on the cliff-top plateau, a quay only below.",
           "The plateau is nearly flat (115-140 m), so blocks are long and level; levels change only across 16 m gaps.",
           "The port square sits on the cliff top over the cove, open to the east (the Kastro Strait), with the port spire stand-in on it.",
           "The quay is a 30 x 20 m apron at 2.0 m in the cove behind the rock spit. The 130 m cliff cannot be graded ground (it is steeper than the 31 degree bank), so the link is a cargo lift and a stair as pieces (comps), not a street: lift head at about (4672, 16808) on the square, foot at the apron (4788, 16806).",
           "The south road out to the citadel road is yours to route: the 17 % climb south of the main street was not drawn as a street.",
           "The road ports at the main street's south and north ends are ASSUMED; the climb to the citadel road is yours to route.",
           "Lamps are yours."],
)
CFG["pool_main"] = ["SF01", "SF08", "SF15", "SF16", "IN01", "IN02", "IN03", "SF09", "SF13", "SF12", "WH01", "WH02", "WH03", "WH04", "WH09", "WH11", "WH21",
                    "WH23", "WH12", "WH07", "WH08", "ND03", "ND01", "ND02", "WH24", "WH22", "WH19", "WH18", "WH10", "WH05"]
CFG["pool_lane"] = ["WH01", "WH04", "WH03", "WH11", "WH12", "WH08", "ND01", "ND03", "ND02", "WH06", "WH17", "WH19", "WH22", "WH10", "WH09",
                    "WH23", "WH18", "WH05", "SF16", "SF15", "WH02", "WH07", "WH14", "WH15", "WH21"]


def build(T):
    from gtown import standard_build
    standard_build(T, "M", 28.0, 14.0, (4620, 16823), "down", ("SF02", "back"),
                   ["IN01", "IN02", "SF15", "SF16", "SF01", "SF08", "SF13", "SF09", "WH09", "WH19"],
                   [("M", T.cfg["pool_main"], "main", 0.5, 17.6)] + [(k, T.cfg["pool_lane"], "lane", 0.0, 17.6) for k in ("N1", "W", "BS", "B1")],
                   comps=[("market or cargo stack group on the square (whole comp, your pick)", -9.0, 0.0, (9.5, 9.4))],
                   open_side="east, over the cliff toward the Kastro Strait")
    T.comps.append(dict(name_or_role="cargo lift and stair pieces from the square down the cliff to the quay apron (your pick; not graded ground)", x=4672.0, y=16808.0))
    T.comps.append(dict(name_or_role="quay apron 30 x 20 m at 2.0 m: boat slips and cargo pad (whole comp, your pick)", x=4791.0, y=16796.0, yaw_deg=90.0, footprint_m=[18.0, 26.0], pad_z_m=QUAY_Z))
