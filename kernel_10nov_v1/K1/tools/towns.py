"""The six K1 towns, hand-designed (PROPOSED). Local metres, x east, y north.

World anchors are the site positions in reference/objectives_v2.json (MEASURED
there on the purpose-map sketch). Everything else is ASSUMED design.
"""
from shapely.geometry import Polygon, LineString, box

from town_lib import smooth

EXT = 330


def _land(sea_pts, extra_void=None):
    sea = Polygon(smooth(sea_pts + [sea_pts[0]], 3)).buffer(0)
    land = box(-EXT, -EXT, EXT, EXT).difference(sea)
    if extra_void is not None:
        land = land.difference(extra_void)
    return land, sea


def sound_head():
    # The Sound's head bay opens to the east; cliffs on both sides of the inlet.
    land, sea = _land([(340, -150), (240, -112), (165, -84), (112, -52), (88, -10), (92, 34), (112, 66),
                       (170, 98), (250, 124), (340, 140)])
    return dict(
        key="sound_head", name="Sound Head", site="3-M3", op=3, size="platoon", world_xy=[2550, 10550],
        land=land, sea=sea, edge_kind="harbour", core_r=65,
        streets=[
            dict(id="M", kind="main", width=7.0, pts=[(86, 8), (60, 14), (36, 26), (10, 30), (-14, 22), (-36, 30), (-58, 46), (-74, 70)]),
            dict(id="Q", kind="lane", width=6.0, pts=[(82, -44), (80, -18), (82, 12), (90, 40), (108, 62)]),
            dict(id="L1", kind="lane", width=5.0, pts=[(36, 26), (40, -2), (30, -28), (10, -44), (-14, -48)]),
            dict(id="L2", kind="lane", width=5.0, pts=[(10, 30), (14, 56), (4, 80), (-12, 100)]),
            dict(id="L3", kind="lane", width=4.5, pts=[(-14, 22), (-24, -4), (-14, -28), (-14, -48)]),
            dict(id="L4", kind="lane", width=4.5, pts=[(-58, 46), (-34, 64), (-12, 70), (4, 80)]),
            dict(id="R1", kind="road", width=6.0, pts=[(-14, -48), (-40, -80), (-70, -110), (-110, -140)]),
            dict(id="R2", kind="road", width=4.5, pts=[(-12, 100), (-24, 130), (-30, 160)]),
            dict(id="R3", kind="road", width=4.5, pts=[(-74, 70), (-110, 82), (-150, 92), (-185, 96)]),
        ],
        square=[(-30, 40), (-8, 38), (4, 46), (2, 60), (-16, 62), (-32, 54)],
        landmark=dict(name="Boatyard Control Spire", footprint=[(-20, 46), (-10, 46), (-10, 56), (-20, 56)],
                      note="sci-fi spire with a lit crown; the CIS boatyard's traffic control for the west rim, seen from the Sound mouth"),
        approaches=[("Quay (boats up the Sound)", (85, 0)), ("SW road (fuel depot, Notch road)", (-110, -140)),
                    ("NW path (Summit AA)", (-30, 160)), ("W lane (terrace farms)", (-185, 96)), ("Square", (-15, 51))],
        cis_zone=Polygon([(66, -60), (120, -60), (120, 70), (66, 70)]),
        role=("Main objective (platoon) of op 3 and the next FOB. The CIS boatyard town at the head of the Sound: "
              "crews and spares for the west-rim boats, the slips 450 m east-south-east (3-05), the fuel depot 670 m "
              "south-west (3-13). The garrison holds the quay front, the square under the control spire and the two "
              "upper lanes that look down the inlet."),
        approach_text=("From the sea: up the Sound once the gate is blown (op 3 final), or by LAAT; the quay is the "
                       "town's front door. From the road: the Notch road from the south-west past the fuel depot. "
                       "From the hill: the path down from the Summit AA (north-west) and the farm lane from the west."),
        target=(92, 104), fringe=6,
    )


def causeway_foot():
    land, sea = _land([(150, -340), (140, -200), (158, -110), (176, -40), (196, 40), (232, 128), (300, 196),
                       (340, 230), (340, -340)])
    cw = LineString([(176, -66), (240, -84), (340, -112)]).buffer(9, cap_style=2)
    land = land.union(cw)
    return dict(
        key="causeway_foot", name="Causeway Foot", site="4-M3", op=4, size="platoon", world_xy=[14100, 8250],
        land=land, sea=sea.difference(cw), edge_kind="harbour", core_r=60,
        streets=[
            dict(id="M", kind="main", width=8.0, pts=[(184, -68), (160, -52), (134, -50), (110, -34), (88, -32), (64, -18), (36, -14), (8, -24), (-20, -40), (-44, -62)]),
            dict(id="L1", kind="lane", width=6.0, pts=[(64, -18), (70, 12), (60, 40), (70, 68)]),
            dict(id="L2", kind="lane", width=5.0, pts=[(134, -50), (128, -14), (146, 14), (150, 44)]),
            dict(id="L3", kind="lane", width=4.5, pts=[(36, -14), (30, -46), (44, -76), (70, -92), (96, -90)]),
            dict(id="L4", kind="lane", width=4.5, pts=[(88, -32), (96, -62), (96, -90)]),
            dict(id="L5", kind="lane", width=4.5, pts=[(8, -24), (0, 10), (14, 36), (34, 52), (60, 40)]),
            dict(id="R1", kind="road", width=8.0, pts=[(300, -108), (240, -86), (184, -68)]),
            dict(id="R2", kind="road", width=8.0, pts=[(-44, -62), (-80, -84), (-130, -100), (-190, -112), (-262, -118)]),
            dict(id="R3", kind="road", width=6.0, pts=[(70, 68), (60, 110), (74, 150), (64, 196)]),
            dict(id="R4", kind="road", width=4.5, pts=[(96, -90), (104, -124), (100, -160)]),
        ],
        square=[(20, 0), (44, -2), (56, 10), (50, 28), (30, 34), (16, 20)],
        landmark=dict(name="Causeway Signal Pylon", footprint=[(26, 8), (38, 8), (38, 20), (26, 20)],
                      note="sci-fi toll and signal pylon at the causeway landfall; its beacon lights the road for CIS convoys"),
        approaches=[("Causeway (east-south-east)", (300, -108)), ("South-arm road (west)", (-262, -118)),
                    ("Slope road (north, to the monastery)", (64, 196)), ("Beach (south)", (100, -160)), ("Square", (32, 14))],
        cis_zone=Polygon([(110, -100), (200, -100), (200, -20), (110, -20)]),
        role=("Main objective (platoon) of op 4 and the FOB for op 6. The road town where the north causeway lands on "
              "Ember Crescent: the only vehicle road onto the crescent runs through it. The garrison holds the "
              "causeway gate, the square at the fork and the upper road toward the monastery; the fuel point "
              "560 m west-south-west (4-07) and the AA 710 m north-east (4-08) support it."),
        approach_text=("Vehicles and infantry come up the causeway from the Cinder Cone (east-south-east). Boats land "
                       "on the beach south of the town. From the west, the south-arm road (op 8's road) enters past "
                       "the checkpoint 1 km away. The main street is the AI road: 8 m, gentle bends, no steep turns."),
        target=(82, 96), fringe=6,
    )


def kastro_quay():
    land, sea = _land([(340, -230), (230, -190), (160, -150), (112, -92), (96, -24), (106, 48), (146, 108),
                       (208, 166), (290, 206), (340, 220)])
    mole = LineString([(106, 54), (160, 46), (206, 16), (236, -18)]).buffer(7, cap_style=2)
    land = land.union(mole)
    return dict(
        key="kastro_quay", name="Kastro Quay", site="5-M3", op=5, size="platoon", world_xy=[4200, 16850],
        land=land, sea=sea.difference(mole), edge_kind="harbour", core_r=70,
        streets=[
            dict(id="M", kind="main", width=7.0, pts=[(90, -2), (64, 4), (40, 18), (14, 22), (-10, 36), (-34, 32), (-56, 44), (-74, 66), (-90, 90)]),
            dict(id="Q", kind="lane", width=6.0, pts=[(100, -96), (92, -56), (90, -14), (94, 24), (108, 52), (132, 62)]),
            dict(id="L1", kind="lane", width=5.0, pts=[(40, 18), (32, -12), (14, -38), (-6, -56), (-8, -84)]),
            dict(id="L2", kind="lane", width=5.0, pts=[(14, 22), (22, 50), (14, 78), (26, 104)]),
            dict(id="L3", kind="lane", width=4.5, pts=[(-34, 32), (-40, 6), (-30, -20), (-6, -56)]),
            dict(id="L4", kind="lane", width=4.5, pts=[(52, 10), (48, -24), (40, -52), (60, -72), (94, -78)]),
            dict(id="L5", kind="lane", width=4.5, pts=[(-56, 44), (-38, 70), (-14, 80), (14, 78)]),
            dict(id="R1", kind="road", width=6.0, pts=[(-90, 90), (-120, 110), (-160, 128), (-214, 140)]),
            dict(id="R2", kind="road", width=4.5, pts=[(-8, -84), (-20, -120), (-24, -150)]),
            dict(id="R3", kind="road", width=4.5, pts=[(26, 104), (48, 118), (64, 124)]),
            dict(id="R4", kind="road", width=4.5, pts=[(-30, -20), (-60, -30), (-100, -30), (-150, -20), (-196, -26)]),
        ],
        square=[(62, -8), (85, -12), (86, -34), (76, -48), (60, -38), (56, -20)],
        landmark=dict(name="Supply Port Control Spire", footprint=[(68, -28), (78, -28), (78, -18), (68, -18)],
                      note="sci-fi port spire on the quay square: CIS cargo control for the north, its crown visible from the Kastro Strait"),
        approaches=[("Quay and mole (boats)", (90, 0)), ("Citadel road (west, uphill)", (-214, 140)),
                    ("Ridge lane (south-west, power station)", (-196, -26)), ("North lane (fuel depot, east bay)", (64, 124)),
                    ("South lane", (-24, -150)), ("Square", (72, -24))],
        cis_zone=Polygon([(60, -120), (130, -120), (130, 80), (60, 80)]),
        role=("Main objective (platoon) of op 5 and the FOB for op 7's boat route. The lower town under the acropolis "
              "and the CIS supply port of the north: supply boats for the Yard load here. The garrison holds the quay "
              "and mole, the quay square under the port spire and the main street's upper bends toward the citadel."),
        approach_text=("From the sea: boats across the Kastro Strait into the bay; the mole and quay are the front. "
                       "From the island: down the citadel road from the west, along the ridge lane from the power "
                       "station (south-west) or the north lane from the fuel depot and the east-bay landers."),
        target=(98, 108), fringe=6,
    )


def lantern_quay():
    land, sea = _land([(-340, 50), (-220, 46), (-150, 26), (-104, -14), (-64, -60), (-20, -70), (24, -78),
                       (90, -62), (160, -78), (240, -100), (340, -120), (340, -340), (-340, -340)])
    return dict(
        key="lantern_quay", name="Lantern Quay", site="5-09", op=5, size="squad", world_xy=[7400, 16650],
        land=land, sea=sea, edge_kind="harbour", core_r=45,
        streets=[
            dict(id="M", kind="main", width=6.0, pts=[(-14, -58), (-8, -28), (10, 0), (28, 30), (24, 64), (38, 98), (36, 130)]),
            dict(id="Q", kind="lane", width=5.0, pts=[(-96, -26), (-62, -44), (-24, -54), (20, -58), (64, -48), (98, -50)]),
            dict(id="L1", kind="lane", width=4.5, pts=[(10, 0), (-26, 14), (-58, 8), (-92, 22)]),
            dict(id="L2", kind="lane", width=4.0, pts=[(28, 30), (62, 40), (94, 30)]),
        ],
        square=[(12, 6), (34, 12), (42, 30), (30, 44), (14, 34)],
        landmark=dict(name="Beacon Relay Mast", footprint=[(24, 20), (32, 20), (32, 28), (24, 28)],
                      note="sci-fi relay mast that repeats the Lantern Rock beacon down to the quay"),
        approaches=[("Quay (boats)", (-14, -58)), ("Beacon path (north-east)", (36, 130)),
                    ("West shore lane", (-96, -26)), ("Square", (28, 26))],
        cis_zone=None,
        role=("Supporting site (squad) in op 5. The beacon keepers' fishing hamlet on Lantern Rock; its quay is the "
              "only boat landing, so it is how players reach the Lantern Rock Beacon (5-M4) 460 m north-east. The "
              "garrison is a small picket in the quay front and the houses round the little square."),
        approach_text=("Only by boat or air (Lantern Rock is 2.3 km off Acropolis Isle). Boats land at the quay; "
                       "the main street climbs from it to the square and on to the beacon path."),
        target=(60, 66), fringe=6,
    )


def kamar_village():
    land, sea = _land([(190, -340), (160, -170), (128, -70), (114, 0), (126, 36), (150, 46), (138, 80),
                       (162, 150), (196, 340), (340, 340), (340, -340)])
    return dict(
        key="kamar_village", name="Kamar Village", site="6-01", op=6, size="two_squad", world_xy=[16850, 11600],
        land=land, sea=sea, edge_kind="harbour", core_r=55,
        streets=[
            dict(id="M", kind="main", width=6.5, pts=[(106, 16), (80, 22), (54, 12), (28, 18), (4, 32), (-18, 52), (-34, 76), (-44, 104)]),
            dict(id="Q", kind="lane", width=5.0, pts=[(102, -50), (104, -14), (108, 20), (118, 52)]),
            dict(id="L1", kind="lane", width=5.0, pts=[(80, 22), (86, -8), (80, -40), (90, -70)]),
            dict(id="L2", kind="lane", width=4.5, pts=[(54, 12), (44, -16), (24, -36), (-2, -44)]),
            dict(id="L3", kind="lane", width=4.5, pts=[(4, 32), (-12, 8), (-14, -20), (-2, -44)]),
            dict(id="L4", kind="lane", width=4.5, pts=[(-18, 52), (2, 78), (26, 82), (40, 64), (54, 40)]),
            dict(id="R1", kind="road", width=5.0, pts=[(-44, 104), (-66, 124), (-104, 140)]),
            dict(id="R2", kind="road", width=5.0, pts=[(90, -70), (104, -110), (114, -150)]),
        ],
        square=[(14, 40), (36, 32), (46, 42), (36, 58), (20, 60), (10, 50)],
        landmark=dict(name="Moisture Condenser Tower", footprint=[(24, 42), (34, 42), (34, 52), (24, 52)],
                      note="sci-fi condenser tower, the village's water; tall enough to read from Kamar Strand"),
        approaches=[("Quay cove (boats)", (106, 16)), ("Beach lane (Kamar Strand, south)", (114, -150)),
                    ("Ravine road (west, up the massif)", (-104, 140)), ("Lower lane (south-west)", (-2, -44)),
                    ("Square", (29, 47))],
        cis_zone=Polygon([(90, -40), (130, -40), (130, 60), (90, 60)]),
        role=("Supporting site (two-squad) in op 6. The beach village under the Prophet Massif: billets for the Kamar "
              "Strand garrison, and its quay is the boat landing for Signal Isle runs. The garrison holds the quay "
              "front and the houses over the beach lane, which look down on the Strand Bunker Line (6-M2) 700 m south."),
        approach_text=("From the sea: the quay cove or the black beach to the south. From the land: up the beach lane "
                       "from Kamar Strand, or down the ravine road from the massif (west)."),
        target=(70, 82), fringe=5,
    )


def oyra():
    # The caldera's inner cliff (a ~300 m drop to the lagoon) runs down the west side.
    edge = [(-50, -340), (-96, -200), (-128, -96), (-146, 0), (-138, 96), (-104, 190), (-50, 280), (-20, 340)]
    void = Polygon(smooth(edge + [(-340, 340), (-340, -340)] + [edge[0]], 2)).buffer(0)
    land = box(-EXT, -EXT, EXT, EXT).difference(void)
    return dict(
        key="oyra", name="Oyra", site="7-M2", op=7, size="platoon", world_xy=[11920, 12500],
        land=land, sea=void, edge_kind="cliff", edge_line=LineString(smooth(edge, 2)), core_r=65,
        streets=[
            dict(id="M", kind="main", width=6.5, pts=[(40, -170), (14, -140), (-14, -118), (-36, -90), (-58, -66), (-68, -36), (-86, -10), (-90, 20), (-80, 48), (-88, 78), (-70, 104), (-56, 132), (-28, 150)]),
            dict(id="L1", kind="lane", width=4.5, pts=[(-36, -90), (-66, -100), (-96, -112), (-112, -124)]),
            dict(id="L2", kind="lane", width=4.5, pts=[(-86, -10), (-112, -20), (-134, -10)]),
            dict(id="L3", kind="lane", width=4.5, pts=[(-70, 104), (-96, 112), (-116, 132)]),
            dict(id="L4", kind="lane", width=5.0, pts=[(-58, -66), (-30, -56), (-4, -70), (26, -58)]),
            dict(id="L5", kind="lane", width=5.0, pts=[(-80, 48), (-50, 58), (-22, 46), (4, 60)]),
            dict(id="L6", kind="lane", width=4.5, pts=[(-14, -118), (-12, -88), (-4, -70)]),
            dict(id="L7", kind="lane", width=4.5, pts=[(-68, -36), (-42, -22), (-34, 6), (-46, 30), (-50, 58)]),
            dict(id="R1", kind="road", width=6.0, pts=[(40, -170), (76, -186), (104, -176), (140, -190)]),
            dict(id="R2", kind="road", width=5.0, pts=[(-28, 150), (-10, 180), (16, 214), (18, 256)]),
            dict(id="R3", kind="road", width=4.0, pts=[(-56, 132), (-80, 160), (-96, 190)]),
        ],
        square=[(-130, 30), (-104, 24), (-98, 44), (-104, 66), (-126, 70), (-138, 50)],
        landmark=dict(name="Narrows Signal Lantern", footprint=[(-126, 42), (-116, 42), (-116, 52), (-126, 52)],
                      note="sci-fi signal spire on the rim square, lighting the North Narrows for Yard traffic; seen from the lagoon and the Narrows"),
        approaches=[("Crest road (south-east, from the Chora and the monastery)", (140, -190)),
                    ("North road (Oyra Head landing)", (18, 256)), ("Rim path (Narrows batteries, west-north-west)", (-96, 190)),
                    ("East lane (outer slope)", (26, -58)), ("Rim square", (-121, 47))],
        cis_zone=None,
        role=("Main objective (platoon) of op 7. The north rim cliff town and the garrison of the North Narrows: the "
              "two Narrows batteries (7-M3 and its pair) are manned from here, and the rim trench (7-06) 580 m "
              "south-west links it to the Chora. The garrison holds the rim square under the signal lantern, the "
              "cliff-edge houses that overlook the Narrows and the two road entries."),
        approach_text=("The lagoon side is a 300 m cliff: no way up except the lanes' end stairs, which are dead ends "
                       "on purpose (look-outs, not routes). Players come along the crest road from the south-east (from "
                       "the Chora or the monastery), down the north road from the Oyra Head landing, or along the rim "
                       "from the Narrows batteries."),
        target=(96, 106), fringe=6,
    )


TOWNS = [sound_head, causeway_foot, kastro_quay, lantern_quay, kamar_village, oyra]
