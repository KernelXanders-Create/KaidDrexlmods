"""Perys v6 (second pass under the 5 m grid rule), PROPOSED.
Same idea as K5 v5: the diagonal main street from the NW road port, the landmark on
a one-level square open to the sea, the quay group. New: each street segment and
its two facing rows are ONE level; parallel streets 47 m apart so back-to-back rows
at different levels stand 14-17 m apart; levels change only in 16 m gaps where the
cross lanes meet the streets; cross lanes run in two pinned pieces."""
import json, math
import numpy as np
from shapely.geometry import Polygon, box
PACK = "/tmp/claude-0/-home-user-KaidDrexlmods/68d91108-852d-5f8a-b84e-f7c6d8824e63/scratchpad/handoff_10nov_b/KERNEL_HANDOFF_20261110b"
V4 = json.load(open(PACK + "/perys/perys_v4_layout.json"))

P0 = np.array([5087.3, 3408.5]); CU = np.array([math.sin(math.radians(132)), math.cos(math.radians(132))]); DU = np.array([math.sin(math.radians(42)), math.cos(math.radians(42))])
def W(a, b): return tuple(np.round(P0 + a * CU + b * DU, 2))
def WL(ab): return [W(a, b) for a, b in ab]

M_AB = [(0, 0), (30, 10), (62, 8), (96, 20), (128, 17), (160, 28), (184, 24), (206, 33), (228, 36), (252, 47), (278, 58), (302, 62)]
U_AB = [(14, -40), (44, -37), (78, -36), (110, -28), (140, -29), (166, -20), (190, -21), (214, -12), (240, -8), (266, 4), (292, 12), (318, 14)]
U2_AB = [(40, -87), (72, -82), (104, -77), (136, -80), (164, -70), (192, -70), (222, -60), (252, -54)]
KW_AB = [(28, 56), (62, 55), (96, 67), (118, 64)]
KE_AB = [(198, 79), (226, 83), (252, 94), (280, 105), (306, 109), (326, 120)]
SQ_AB = [(138, 30), (182, 34), (186, 52), (140, 50)]
QUAY = box(5632, 3546, 5722, 3584); QUAY_Z = 2.2
HR = next(s for s in V4["streets"] if s["id"] == "HR")

def cross(id_, ab, a_from, a_to, name):
    pts = WL(ab); L = sum(math.dist(p, q) for p, q in zip(pts[:-1], pts[1:]))
    return dict(id=id_, cls="lane", w=4.5, rows="none", name=name, pin_start=a_from, pin_end=a_to, ramp=True, pts=pts, smooth=True)

CFG = dict(
    key="perys_v6", town="Perys", version="v6 (Kernel second pass, 5 m grid rule) PROPOSED", seed=21,
    tile=PACK + "/perys/height_perys_natural_1m.npy", tile_origin=(4880, 2950), ground_label="natural ground",
    target_n=84, garrison_range=(40, 52), square=True,
    view=((5040, 5460), (3150, 3520)),
    inset=dict(view=((5560, 5760), (3500, 3640)), title="quay group (apron 2.2 m)"),
    title="Perys v6 (Kernel K5 second pass, PROPOSED): one level per terrace, 5 m grid rule, real models",
    labels={"NW road port (59.4 m)": (5092, 3414)},
    streets=[
        dict(id="M", cls="main", w=8.0, rows="both", name="Odos Perys (main street, AI road)", pin_start=59.4, pts=WL(M_AB),
             gaps_at=[W(62, 8), W(100, 19), W(206, 33), W(262, 51)], drop_grade=0.12),
        dict(id="U", cls="lane", w=5.0, rows="both", name="Ano Rouga (upper lane)", pts=WL(U_AB),
             gaps_at=[W(60, -36), W(110, -28), W(210, -13), W(266, 4)]),
        dict(id="U2", cls="lane", w=5.0, rows="both", name="Pano Rouga (top lane)", pts=WL(U2_AB), gaps_at=[W(120, -77), W(210, -63)]),
        cross("CT1", [(120, -77), (116, -60), (112, -44), (110, -28)], "U2", "U", "top link 1"),
        cross("CT2", [(210, -63), (214, -46), (208, -28), (210, -13)], "U2", "U", "top link 2"),
        dict(id="KW", cls="lane", w=5.0, rows="both", name="Kato Rouga west (lower lane)", pts=WL(KW_AB), gaps_at=[W(62, 55)]),
        dict(id="KE", cls="lane", w=5.0, rows="both", name="Kato Rouga east (lower lane)", pts=WL(KE_AB), gaps_at=[W(254, 96)]),
        cross("CU1", [(60, -36), (64, -20), (62, -6), (62, 8)], "U", "M", "cross lane 1 (upper)"),
        cross("CM1", [(62, 8), (60, 24), (64, 40), (62, 55)], "M", "KW", "cross lane 1 (lower)"),
        cross("CU2", [(110, -28), (104, -10), (100, 4), (100, 19)], "U", "M", "cross lane 2 (upper)"),
        cross("CM2", [(100, 19), (96, 36), (98, 52), (96, 67)], "M", "KW", "cross lane 2 (lower)"),
        cross("CU3", [(210, -13), (204, 4), (208, 20), (206, 33)], "U", "M", "cross lane 3 (upper)"),
        cross("CM3", [(206, 33), (194, 46), (212, 60), (198, 79)], "M", "KE", "cross lane 3 (lower)"),
        cross("CU4", [(266, 4), (260, 20), (264, 36), (262, 51)], "U", "M", "cross lane 4 (upper)"),
        cross("CM4", [(262, 51), (256, 68), (258, 82), (254, 96)], "M", "KE", "cross lane 4 (lower)"),
        dict(id="HL", cls="lane", w=5.0, rows="none", name="harbour link (to the v4 harbour road)", pin_start="KW", ramp=True,
             pts=WL([(62, 55), (60, 76), (58, 96)]) + [tuple(HR["points"][0])]),
        dict(id="HR", cls="path", out_cls="main", w=HR["width_m"], name="harbour road (v4 HR, unchanged; graded by your tools)", pts=[tuple(p) for p in HR["points"]], smooth=False),
    ],
    notes=["PROPOSED by Kernel, Perys second pass under the 5 m grid rule (10 Nov late note).",
           "Each street segment and the two rows facing it are one level (one pad_group per row run). Levels change only across 16 m gaps placed where the cross lanes meet the street; cross lanes run in two pieces pinned to the levels of the streets they join.",
           "Parallel streets are about 47 m apart, so back-to-back rows at different levels stand at least 14 m (17 m diagonal) apart; the strip between them is the bank hidden behind the rows.",
           "The square is one level, at the main street's level; the landmark (ND07) stands on it; its sea side is open.",
           "HR is your v4 harbour road, unchanged (written here as class main; graded by your tools, not by us). Lamps are yours."],
)
CFG["pool_main"] = ["SF01", "SF08", "SF15", "SF16", "WH01", "WH02", "WH03", "WH04", "WH09", "WH11", "WH21", "WH23", "WH12", "WH07", "WH08",
                    "ND03", "ND05", "ND01", "ND02", "WH24", "WH22", "WH19", "WH18"]
CFG["pool_lane"] = ["WH01", "WH04", "WH03", "WH11", "WH12", "WH08", "WH24", "ND01", "ND02", "ND03", "ND04", "WH06", "WH17", "WH19", "WH22",
                    "WH23", "WH18", "WH05", "SF16", "SF15", "WH02", "WH07"]


def build(T):
    from shapely import contains_xy
    from town_grid import grid_points
    sq = Polygon(WL(SQ_AB)); T.SQ = sq
    sqz = T.zst("M", *W(162, 28)); T.square_z = sqz
    T.extra_pads.append((sq.buffer(1.5), sqz)); T.extra_pads.append((QUAY.buffer(0.5), QUAY_Z))
    for gp in grid_points(sq.buffer(1.5)): T.claims[gp] = sqz
    for gp in grid_points(QUAY.buffer(0.5)): T.claims[gp] = QUAY_Z
    T.draw_polys = [(sq, "#f3e6c4", "#7b2cbf", "square"), (QUAY, "#d9e8f0", "#1f5f8b", "quay apron")]
    c = np.array(sq.centroid.coords[0])
    T.pad += 1; T._pg = f"P{T.pad:03d}"
    lm = W(152, 40); T.add("ND07", lm[0], lm[1], 222.0, "front", sqz, "SQ", "landmark", T._pg)
    T.log.clear()
    for edge in ([W(138, 30), W(140, 50)], [W(182, 34), W(186, 52)]):          # the two ends; the sea side stays open
        T.pack_edge(edge, c, sqz, ["SF01", "SF08", "SF15", "SF16", "SF17", "SF06", "WH09", "WH02", "ND03"], "square", allow_tall=True, cut_lim=2.5)
    print("RING", dict(T.log)); T.log.clear()
    for k in ("M", "U", "KW", "KE", "U2"):
        pool, role, sci = (T.cfg["pool_main"], "main", 0.55) if k == "M" else (T.cfg["pool_lane"], "lane", 0.0)
        for side in T.row_sides(T.streets[k]):
            T.pack_row(k, side, pool, role, max_depth=16.6, cut_lim=2.5, sci_first=sci)
    T.pack_edge([(5652, 3565), (5718, 3565)], (5677, 3580), QUAY_Z, ["IN01", "SF15", "IN02", "SF16", "IN03"], "quay", street_id="QY", cut_lim=2.5)
    print("QUAY+ROWS", dict(T.log))
    T.comps = [dict(name_or_role="market on the square (e.g. Crystal Carts, whole comp)", x=W(168, 42)[0], y=W(168, 42)[1], yaw_deg=42.0, footprint_m=[9.5, 9.4], pad_z_m=sqz),
               dict(name_or_role="covered hall or cargo stack group on the square (whole comp, your pick)", x=W(178, 44)[0], y=W(178, 44)[1], yaw_deg=42.0, footprint_m=[8.0, 8.0], pad_z_m=sqz),
               next(dict(cc, name_or_role=cc["name_or_role"] + " (kept from v4)") for cc in V4["comps"] if "quay" in cc["name_or_role"])]
    T.square_out = {"polygon": [list(p) for p in WL(SQ_AB)], "level_z_m": sqz,
                    "landmark_building_id": next(b["id"] for b in T.B if b["role"] == "landmark"), "open_side": "north-east, toward the sea"}
