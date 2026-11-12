"""Op 8, The Caldera Yard: site list, net, squad anchors and approaches for the planner (pad half-sizes in metres)."""
NAME = "The Caldera Yard"
BOX = (7000, 14500, 5800, 12000)
VIEW = (7000, 14500, 5800, 12000)
LEGEND_LOC = "upper left"
PLAN_KW = dict(band_range=10.0, steep=1.0, repair_to=3.6)     # as ops 5-7; every road is still held to 14 % and 4 m

# id, name, composition, hx, hy, size evidence, rough x, y (None = purpose map), search radius, water mode
SITES = [
    ("8-F", "Caldera Yard + Rim Foundry", "NEW 1: the Yard (capstone inside the Rim Foundry)", 140.0, 190.0,
     "MEASURED ground: your build-4 grid already has a flat shelf at 3.5 m here, 298 x 450 m (101,600 m2); a 280 x 380 m pad fits inside it (the purpose map's 'about 400 x 300 m'); a harbour work (dry dock and slipways reach the lagoon)", None, 200, "beach"),
    ("8-M1", "Breach Dam (east abutment and gate house)", "CIS Fortress Dam with GPs", 40.0, 30.0,
     "ASSUMED: the dam spans the breach (see the dam line); this is its east abutment and gate house, 80 x 60 m, on the south arm's tip (a harbour work)", (9265, 8570), 250, "beach"),
    ("8-M2", "Kameni Shield Generator", "Destructable Shield Generator and its shield template", 30.0, 30.0, "ASSUMED: 60 x 60 m", None, 350, False),
    ("8-M3", "South Arm Gun Line", "CIS AAT Turbolaster Base with GPs", 45.0, 45.0, "ASSUMED: 90 x 90 m (as op 3's Sound Rim Guns)", None, 300, False),
    ("8-M4", "Yard Power Plant", "CIS Large Power Facility with GPs", 70.0, 50.0, "ASSUMED: 140 x 100 m (as op 5's Ridge Power Station)", None, 300, False),
    ("8-01", "Dam West Tower", "Tukata Defense Tower Turbolaser", 20.0, 20.0, "ASSUMED: 40 x 40 m", None, 300, False),
    ("8-02", "Dam East Bunkers", "CIS Small Wall (Bunker) with GPs", 45.1, 29.1, "KNOWN as built: your 1-09 (Small Wall with Bunker) is a Small Rectangle FOB, 90 x 58 m", None, 300, False),
    ("8-03", "Inner Shore Fuel Quay", "CIS Large Fuel Depot with GPs", 80.0, 60.0, "REDUCED: the composition's own pad (2-xx) is 248 x 261 m and the inner shore takes no more than 160 x 120 m; a harbour work", None, 300, "beach"),
    ("8-04", "Crater Wall Depot", "CIS Depot (Fixed) with GPs (D)", 40.0, 30.0, "ASSUMED: 80 x 60 m (as op 6's Signal Isle Depot); on the inner shore (a harbour work)", None, 300, "beach"),
    ("8-05", "Kameni Vent Bunkers", "Tukata Turret Bunker", 25.0, 25.0, "ASSUMED: 50 x 50 m", None, 300, False),
    ("8-08", "South Arm Road Tower", "CIS Flower Tower with GPs", 46.4, 44.0, "KNOWN: 1-11", None, 300, False),
    ("8-09", "Akrotar Cape AA", "CIS Medium AA Base with GPs", 98.5, 96.4, "KNOWN: 2-M3", None, 400, False),
    ("8-10", "Inner Shore Road Gate", "CIS Double Checkpoint with GPs", 32.9, 49.5, "KNOWN: 2-07; on the inner shore road (a harbour work)", None, 300, "beach"),
    ("8-12", "Dry Dock Pump House", "Supply Outpost Version 2", 41.0, 32.5, "KNOWN: 82 x 65 m (the pad op 3 found); beside the Yard (a harbour work)", None, 300, "beach"),
    ("8-13", "South Crest AA", "Medium Covered AA Base with GPs", 60.0, 55.0, "ASSUMED: 120 x 110 m (a little under the Medium AA Base, 2-M3)", None, 300, False),
    ("8-14", "Akrotar Dig (sheds and ramp depot)", "CIS Elevated Ramp Depot with GPs", 60.6, 39.5, "ASSUMED: as the CIS Elevated Landing Pad Construction (2-01)", None, 300, False),
    ("8-14-T", "Akrotar Dig (the temple dig)", "Temple Run V4", 40.0, 30.0, "ASSUMED: 80 x 60 m of dig beside the sheds", (9750, 6850), 300, False),
    ("8-15", "Ash Crest Gun Line", "CIS Small Artillery Base with GPs", 63.8, 31.4, "KNOWN: 1-M3", None, 300, False),
    ("8-16", "Ash Outer Depot", "Supply Base Small_1", 41.0, 32.5, "KNOWN: 82 x 65 m", None, 300, "beach"),
]

# the dam itself is not a pad: it spans the breach at its narrowest (MEASURED: 354 m, 41 m deep), Ash Crescent's south tip to the south arm
GATE = ((9015.0, 8820.0), (9265.0, 8570.0))
GATE_LABEL = "Breach Dam (span)"

# ops 4, 6 and 7 are done: their pads here are blocked and their roads are the net this op joins
EXTERNAL_PLANS = ["../out_op4/op4_plan.json", "../out_op6/op6_plan.json", "../out_op7/op7_plan.json"]
NETS = {"Ember Crescent": ["8-08", "8-M3", "8-13", "8-02", "8-M1", "8-14", "8-14-T", "8-09", "8-03", "8-04", "8-10", "8-12", "8-F", "8-M4"]}
ROOT = {"Ember Crescent": "EXTERNAL_ROADS"}

SQUADS = [
    ("A8-01", "CIS Small Checkpoint with GPs", 28.4, 34.4, 12900, 7600, 300, "the south arm road from Causeway Foot"),
    ("A8-02", "CIS Heavy Gun Position with GPs (D)", 30.1, 25.4, 11800, 8350, 300, "the inner shore road between the fuel quay and the depot"),
    ("A8-03", "CIS Mixed AA Platform with GPs", 50.7, 46.4, 13400, 9600, 300, "the air over the Yard, from the rim"),
    ("A8-04", "CIS Heavy Gun Position + AA (UD)", 29.9, 40.8, 12500, 9300, 300, "the inner shore north of the road gate and the Yard's south end"),
    ("A8-05", "CIS Heavy Gun Position with AA (D)", 29.8, 42.5, 9500, 8150, 300, "the dam's east end"),
    ("A8-06", "CIS Heavy Gun Position with GPs (D)", 30.1, 25.4, 10600, 7700, 300, "the south crest between the AA and the gun line"),
    ("A8-07", "CIS Heavy Gun Position + AA (UD)", 29.9, 40.8, 9800, 6400, 300, "Akrotar's beaches"),
    ("A8-08", "CIS Heavy Gun Position with GPs (D)", 30.1, 25.4, 10100, 10250, 300, "Kameni's south shore"),
    ("A8-09", "CIS Heavy Gun Position with AA (D)", 29.8, 42.5, 8450, 9100, 300, "the dam's west end on Ash Crescent"),
    ("A8-10", "CIS Small Checkpoint with GPs", 28.4, 34.4, 7950, 10600, 300, "Ash Crescent's west beach"),
]

APPROACHES = {
    "8-F Caldera Yard": ["along the inner shore road from the south, through the Inner Shore Road Gate (8-10) (vehicles)",
                         "down the Skala path from the Rim Chora (op 7), on foot; or by boat across the lagoon once the dam gate opens"],
    "8-M1 Breach Dam": ["along the south arm road to the dam's east end (vehicles)", "from Ash Crescent's south tip across the dam crest on foot, or by boat to either end"],
    "8-M2 Kameni Shield Generator": ["by boat to Kameni's north landing past the Vent Bunkers (8-05)", "by boat to Kameni's south shore, or by air once the shield's AA falls"],
    "8-M3 South Arm Gun Line": ["along the south arm road from Causeway Foot past the South Arm Road Tower (8-08) (vehicles)", "up from the Inner Shore Fuel Quay (8-03)"],
    "8-M4 Yard Power Plant": ["by road from the rim (the op 4 and op 7 nets) (vehicles)", "up the cliff path from the Dry Dock Pump House (8-12), on foot"],
}
BOAT_ONLY = ()
