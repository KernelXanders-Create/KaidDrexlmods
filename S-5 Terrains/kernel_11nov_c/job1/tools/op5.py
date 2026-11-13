"""Op 5, Acropolis Isle: site list, towns, nets, squad anchors and approaches for the planner (pad half-sizes in metres)."""
NAME = "Acropolis Isle"
BOX = (0, 11000, 14300, 19400)
# the island's flanks are steeper than ops 3-4: the router's band filter is loosened from 7.6 to 10 m and its step limit from 0.8 to 1.0 of the grade; every road is still held to 4 m cut / fill and 14 %
PLAN_KW = dict(band_range=99.0, steep=0.8, repair_to=3.6)     # re-pass: as ops 3-4 v2
VIEW = (0, 11000, 14300, 19400)

# id, name, composition, hx, hy, size evidence, rough x, y (None = purpose map), search radius, water mode
SITES = [
    ("5-F", "Acropolis Citadel", "TKTA Citadel with Hangar (Mono, Fixed) + Le Temple 2", 80.0, 80.0, "ASSUMED: no pad of either composition exists; 160 x 160 m, a little over the CIS Small Citadel (148 x 153 m) to take Le Temple 2 inside the walls", None, 300, False),
    ("5-M1", "Windmill Ridge", "Lessu Outskirts + CIS Flak Crown with GPs (Appalachia)", 58.4, 54.0, "KNOWN for the Flak Crown (op 1 pads); the Lessu windmills are dressing strung along the spine either side of it (not a pad)", None, 300, False),
    ("5-M2", "Sea Cave Pens", "PLAD Cave Base with Escape", 40.0, 30.0, "ASSUMED: an 80 x 60 m apron at the cave mouth (a sea work: may stand at the water's edge); the cave itself is inside the cliff", None, 300, "beach"),
    ("5-M4", "Lantern Rock Beacon", "CIS Big Radio Tower with GPs", 30.0, 30.0, "ASSUMED: 60 x 60 m", None, 300, False),
    ("5-01", "Pumice Coast Bunker Line", "CIS Metal Trench Line with GPs", 21.7, 75.1, "KNOWN: op 1 pads", None, 300, False),
    ("5-02", "West Cliff AA", "CIS Medium AA Base with GPs", 60.0, 55.0, "REDUCED: the composition's own pad (2-M3) is 197 x 193 m and nothing that big holds 4 m on the west cliffs; a 120 x 110 m pad fits (needs a smaller cut of the base)", None, 400, False),
    ("5-03", "North Cape Battery", "CIS Turbolaser Tower with GPs", 27.5, 30.1, "KNOWN: 2-09", None, 300, False),
    ("5-04", "Monastery Ledge", "Zavala CIS Outpost Fixed with GPs", 30.0, 30.0, "ASSUMED: 60 x 60 m (as op 3's Zavala outpost)", None, 300, False),
    ("5-05", "Ridge Power Station", "CIS Large Power Facility with GPs", 70.0, 50.0, "ASSUMED: 140 x 100 m", None, 300, False),
    ("5-06", "Quay Fuel Depot", "CIS Fuel Depot with GPs", 43.6, 32.3, "KNOWN: 1-12", None, 300, False),
    ("5-07", "Citadel Gate Checkpoint", "TKTA Checkpoint Fixed (Mono)", 24.0, 39.0, "KNOWN: 2-04 (a pass-profile pad 48 x 78 m; here seated level)", None, 300, False),
    ("5-08", "Olive Terraces Post", "CIS Outpost with GPs (D)", 30.0, 30.0, "ASSUMED: 60 x 60 m", None, 300, False),
    ("5-10", "Coral Head Pillboxes", "Small Wall with Bunker", 20.0, 12.0, "ASSUMED: 40 x 24 m on a coral head (as op 3's shoal pillboxes)", None, 250, "beach"),
    ("5-11", "Coral Shelf Wreck", "2x Armed Landers Fixed", 40.0, 60.0, "ASSUMED: 80 x 120 m for two landers side by side on the reef", None, 300, "beach"),
    ("5-12", "Citadel Gun Park", "CIS Vehicle Depot with GPs (D)", 50.0, 40.0, "ASSUMED: 100 x 80 m", None, 300, False),
    ("5-13", "Kastro Strait Sensor Stack", "CIS Comms Array with GPs", 15.0, 15.0, "REDUCED: the Comms Array's pad (A1-03) is 40 x 93 m; the stack top only takes about 30 x 30 m (the array's mast and a ring of guns); air only", None, 120, "beach"),
    ("5-14", "East Bay Landers", "CIS Landing Position with GPs", 44.5, 67.0, "KNOWN: 1-02 / 2-06 (a beach work)", None, 350, "beach"),
]

K6 = "../../../kernel_10nov_v1/K6_repass/"
TOWNS = {
    "5-M3": dict(name="Kastro Quay", layout=K6 + "kastro_quay_v2/kastro_quay_v2_layout.json",
                 entry=(4488.0, 16752.0), entry_z=108.25,
                 # its street ends (K6 v2 layout), each with the bearing a road leaves it on
                 ports=[(4488.0, 16752.0, 108.25, 355.0, "B1 north end"), (4628.0, 16660.0, 132.75, 180.0, "M south end"), (4600.0, 17040.0, 120.5, 355.0, "M north end"),
                        (4586.0, 16636.0, 122.0, 180.0, "W south end"), (4672.0, 16979.0, 119.0, 90.0, "N1 east end")]),          # street B1's north end, the town's west edge (the road port to the citadel road)
    "5-09": dict(name="Lantern Quay Hamlet", layout=K6 + "lantern_quay_v2/lantern_quay_v2_layout.json",
                 entry=(7533.3, 16542.3), entry_z=91.25),           # the top terrace's east end (foot only; no road on Lantern Rock)
}

# one net on Acropolis Isle, grown from Kastro Quay (the op's FOB); Lantern Rock, the reef and the stack have no road
NETS = {"Acropolis Isle": ["5-05", "5-M1", "5-07", "5-F", "5-12", "5-03", "5-08", "5-04", "5-02", "5-01", "5-06", "5-14", "5-M2"]}
ROOT = {"Acropolis Isle": "5-M3"}

SQUADS = [
    ("A5-01", "CIS Heavy Gun Position with GPs (D)", 30.1, 25.4, 3250, 15950, 300, "the pumice south beach below the bunker line"),
    ("A5-02", "CIS Heavy Gun Position + AA (UD)", 29.9, 40.8, 1750, 16250, 300, "the sea-cave mouths and the Kastro Strait crossing"),
    ("A5-03", "CIS Heavy Gun Position with GPs (D)", 30.1, 25.4, 1250, 16700, 300, "the west coast landing below the West Cliff AA"),
    ("A5-04", "CIS Heavy Gun Position with AA (D)", 29.8, 42.5, 2600, 18200, 300, "the citadel's north back slope, between the gun park and the cape battery"),
    ("A5-05", "CIS Mixed AA Platform with GPs", 50.7, 46.4, 3000, 17500, 300, "the air over the acropolis"),
    ("A5-06", "CIS Small Checkpoint with GPs", 28.4, 34.4, 4250, 16500, 300, "the road from Kastro Quay up to the power station"),
    ("A5-07", "CIS Heavy Gun Position + AA (UD)", 29.9, 40.8, 4300, 18250, 300, "the north-east bay beach and the landers"),
    ("A5-08", "CIS Small Checkpoint with GPs", 28.4, 34.4, 4250, 17350, 300, "the road north of Kastro Quay to the fuel depot and the bay"),
    ("A5-09", "CIS Heavy Gun Position with GPs (D)", 30.1, 25.4, 7650, 16450, 250, "Lantern Quay's landing and the hamlet stair"),
    ("A5-10", "CIS Heavy Gun Position with AA (D)", 29.8, 42.5, 7950, 17150, 250, "the Lantern channel and the head of the Coral Shelf"),
]

APPROACHES = {
    "5-F Acropolis Citadel": ["up the road from Kastro Quay past the power station, Windmill Ridge and the Citadel Gate (5-07)",
                              "the covered climb from the south-west: past the Olive Terraces Post (5-08) onto the summit's west side"],
    "5-M1 Windmill Ridge": ["from the pumice south beach, past (or through) the bunker line (5-01) and up the spine",
                            "along the ridge road from the Ridge Power Station (5-05)"],
    "5-M2 Sea Cave Pens": ["by boat across the Kastro Strait into the cave mouth", "from above: down from the Olive Terraces Post (5-08) on its road or the cliff path"],
    "5-M3 Kastro Quay": ["by boat to the quay apron in the cove, then the cargo lift and the stair up the cliff", "overland from the East Bay Landers (5-14) or along the road from the power station (5-05)"],
    "5-M4 Lantern Rock Beacon": ["by boat to Lantern Quay, then up the hamlet stairs to the beacon", "by boat or air to the rock's north and east shores (shores list), then up the slope on foot"],
}
BOAT_ONLY = ("5-10", "5-11", "5-13")
