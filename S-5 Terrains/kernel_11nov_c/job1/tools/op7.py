"""Op 7, The Rim: site list, town, net, squad anchors and approaches for the planner (pad half-sizes in metres)."""
NAME = "The Rim"
BOX = (9000, 15200, 9500, 17500)
VIEW = (9000, 15200, 9500, 17500)
LEGEND_LOC = "lower left"
PLAN_KW = dict(band_range=99.0, steep=0.8, repair_to=3.6)     # re-pass: as ops 3-6 v2

# id, name, composition, hx, hy, size evidence, rough x, y (None = purpose map), search radius, water mode
SITES = [
    ("7-F", "Rim Chora: the kastro", "CIS Gloamport Star Bastion with GPs", 60.0, 60.0, "ASSUMED: 120 x 120 m (a star bastion); the Chora's houses are a hand-made town with no layout yet (not in K6), to be laid out round it", None, 250, False),
    ("7-M1", "Skaros Rock Keep", "CIS Gloamport Gun Keep with GPs", 40.0, 40.0, "ASSUMED: 80 x 80 m on the castle rock (a sea work: may stand at the water's edge)", None, 250, "beach"),
    ("7-M3", "Narrows East Battery (artillery base)", "[Burnzy] CIS Arti-base", 63.8, 31.4, "ASSUMED: as the CIS Small Artillery Base (1-M3)", None, 350, False),
    ("7-M3-T", "Narrows East Battery (tower)", "Flower Tower 2", 46.5, 50.5, "KNOWN: 2-M4 (CIS Flower Tower 2 AA)", (11250, 12900), 300, False),
    ("7-M4", "Chora AA Umbrella", "CIS Heavy AD Tower with GPs", 46.4, 44.0, "ASSUMED: as the CIS Flower Tower (1-11)", None, 300, False),
    ("7-01", "Narrows West Battery", "CIS Turbolaser Tower with GPs", 27.5, 30.1, "KNOWN: 2-09", None, 300, False),
    ("7-02", "Skala Path Head", "TKTA Checkpoint Fixed (Mono)", 24.0, 39.0, "KNOWN: 2-04 (a pass-profile pad 48 x 78 m; here seated level); on the cliff top where the Skala path starts down (the purpose map's point is on the cliff face)", (13000, 10750), 150, False),
    ("7-03", "Crest Road Checkpoint", "CIS Medium Checkpoint 3 with GPs", 30.0, 40.0, "ASSUMED: 60 x 80 m (a little over the Small Checkpoint, A2-05)", None, 300, False),
    ("7-04", "Oyra Head Radar", "Giant Radar Dish", 40.0, 40.0, "ASSUMED: 80 x 80 m", None, 300, False),
    ("7-05", "Oyra Head Landers", "CIS Fortified Lander (Backdoor) with GPs", 40.0, 60.0, "ASSUMED: 80 x 120 m; a beach work", None, 350, "beach"),
    ("7-06", "North Rim Trench", "CIS Metal Trench Line with GPs", 21.7, 75.1, "KNOWN: op 1 pads; on the rim between Oyra and the Narrows (the purpose map's point, south-west of the town, is boxed in by the cliff and the town)", (11400, 12500), 200, False),
    ("7-07", "Chora Power Bank", "CIS Powerbank Facility with GPs", 60.0, 50.0, "REDUCED: the composition's own pad (2-14) is 192 x 166 m and no seat for it holds 4 m within 960 m; a 120 x 100 m pad (as op 4's 4-11; needs a smaller cut of the facility)", None, 400, False),
    ("7-08", "Ash North Ridge Post", "Zavala CIS Outpost with GPs", 30.0, 30.0, "ASSUMED: 60 x 60 m (as op 3's Zavala outpost)", None, 300, False),
    ("7-11", "Oyra Head Beach Bunkers", "Tukata Turret Bunker", 25.0, 25.0, "ASSUMED: 50 x 50 m", None, 300, False),
    ("7-12", "Crew Barracks", "CIS Medium Logistics Base with GPs", 50.0, 40.0, "ASSUMED: between Supply Base Small_1 (82 x 65 m) and the Medium FOB (78 x 149 m)", None, 300, False),
    ("7-13", "Chora Lower Terraces", "Tukata Checkpoint Fixed with GPs", 28.4, 34.4, "ASSUMED: as the CIS Small Checkpoint (A2-05)", None, 300, False),
    ("7-14", "Oyra Head Windmill Flak", "CIS Minimal AA Flak Cannon with GPs", 20.0, 20.0, "ASSUMED: 40 x 40 m; the windmills are dressing in a row beside it (not a pad)", None, 300, False),
    ("7-15", "North Skerry Sensor", "Claus - Small Radar", 15.0, 15.0, "ASSUMED: 30 x 30 m on the stack top; air only", None, 120, "beach"),
]

K6 = "../../../kernel_10nov_v1/K6_repass/"
TOWNS = {"7-M2": dict(name="Oyra", layout=K6 + "oyra_v2/oyra_v2_layout.json", entry=(11906.0, 12190.0), entry_z=130.75,
                      # the K6 notes: the rim path (west-north-west), the crest road (south-east) and the north road (to Oyra Head) join at the street ends
                      ports=[(11906.0, 12190.0, 130.75, 120.0, "rim street, east end (crest road)"), (11950.0, 12256.0, 128.5, 110.0, "upper lane, east end"),
                             (11966.0, 12324.0, 122.5, 90.0, "back lane, east end"), (11640.0, 12470.0, 124.75, 0.0, "back lane, west end (north road)"),
                             (11592.0, 12378.0, 130.75, 290.0, "rim street, west end (rim path)")])}

# ops 4 and 6 are done: their pads here are blocked and their roads are the net this op joins (op 6's west climb passes 600 m east of the Chora)
EXTERNAL_PLANS = ["../out_op4_v2/op4_plan.json", "../out_op6_v2/op6_plan.json"]     # re-pass: the v2 plans
NETS = {"Ember Crescent": ["7-12", "7-03", "7-07", "7-M4", "7-F", "7-13", "7-02", "7-M1", "7-M2", "7-06", "7-M3", "7-M3-T", "7-11", "7-04", "7-14", "7-05"]}
ROOT = {"Ember Crescent": "EXTERNAL_ROADS"}

SQUADS = [
    ("A7-01", "CIS Small Checkpoint with GPs", 28.4, 34.4, 14000, 10450, 300, "the crest road between the Prophet Monastery (op 6) and the Chora"),
    ("A7-02", "CIS Heavy Gun Position with GPs (D)", 30.1, 25.4, 12650, 10950, 300, "the Skala path head and the lagoon shore below the Chora"),
    ("A7-03", "CIS Mixed AA Platform with GPs", 50.7, 46.4, 13300, 11350, 300, "the air over the Chora"),
    ("A7-04", "CIS Heavy Gun Position + AA (UD)", 29.9, 40.8, 12550, 11750, 300, "Skaros and the lagoon west of the Chora"),
    ("A7-05", "CIS Small Checkpoint with GPs", 28.4, 34.4, 12450, 12150, 300, "the rim road between the Chora and Oyra"),
    ("A7-06", "CIS Heavy Gun Position with AA (D)", 29.8, 42.5, 11400, 12950, 300, "the North Narrows from the east cliff"),
    ("A7-07", "CIS Heavy Gun Position with GPs (D)", 30.1, 25.4, 11600, 14100, 300, "Oyra Head's west shore and the Coral Shelf landfall"),
    ("A7-08", "CIS Heavy Gun Position + AA (UD)", 29.9, 40.8, 12650, 15100, 300, "Oyra Head's north tip and the sea toward the skerry"),
    ("A7-09", "CIS Heavy Gun Position with GPs (D)", 30.1, 25.4, 10000, 12900, 300, "Ash Crescent's north tip beach"),
    ("A7-10", "CIS Heavy Gun Position with AA (D)", 29.8, 42.5, 9900, 12300, 300, "the Ash north ridge and the Narrows channel"),
]

APPROACHES = {
    "7-F Rim Chora": ["along the crest road from the Prophet Monastery FOB (op 6), past the Crest Road Checkpoint (7-03) (vehicles)",
                      "the covered way up from Skaros through the Chora Lower Terraces (7-13), on foot"],
    "7-M1 Skaros Rock Keep": ["down the road from the Chora past the Skala Path Head (7-02) (vehicles)", "by boat on the lagoon to the rock once the Narrows are open"],
    "7-M2 Oyra": ["along the rim road from the Chora (vehicles)", "down the north road from Oyra Head, from the landers' beach (7-05)"],
    "7-M3 Narrows East Battery": ["along the rim road from Oyra past the North Rim Trench (7-06) (vehicles)", "by boat to the shore below the battery (shores list), then up on foot"],
    "7-M4 Chora AA Umbrella": ["by road from the Chora (vehicles)", "by road from the crest road past the Crew Barracks (7-12) and the Power Bank (7-07)"],
}
BOAT_ONLY = ("7-15",)

# re-pass: the Chora-Oyra part and the Oyra Head part (joined to your built road) are joined by a road where one holds
JOIN_PIECES = ("Ember Crescent",)
