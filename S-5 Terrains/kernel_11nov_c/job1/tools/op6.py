"""Op 6, Prophet Massif and Signal Isle: site list, town, net, squad anchors and approaches for the planner (pad half-sizes in metres)."""
NAME = "Prophet Massif and Signal Isle"
BOX = (13300, 19600, 9000, 18300)
VIEW = (13300, 19600, 9000, 18300)
PLAN_KW = dict(band_range=10.0, steep=1.0, repair_to=3.6)      # as op 5, and the profile repair aims at 3.6 m: the massif's flanks are steep; every road is still held to 14 % and 4 m

# id, name, composition, hx, hy, size evidence, rough x, y (None = purpose map), search radius, water mode
SITES = [
    ("6-F", "Prophet Monastery (citadel)", "CIS Small Citadel with GPs", 74.2, 76.6, "KNOWN: 1-xx / 2-xx (CIS Small Citadel, op 1-2 pads)", None, 300, False),
    ("6-F-T", "Prophet Monastery (sensor crown)", "Giant Comms Antenna Array", 40.0, 40.0, "ASSUMED: 80 x 80 m (as op 3's Peak Relay Dish); a second pad of the final, beside the citadel", (15550, 11400), 300, False),
    ("6-M1", "Signal Isle Turbolaser Battery", "CIS Turbolaser Battery with GPs", 50.0, 40.0, "ASSUMED: 100 x 80 m (the Turbolaser Tower is 55 x 60 m)", None, 300, False),
    ("6-M2", "Kamar Strand Bunker Line", "CIS Basic Trenchline with GPs + Tukata Turret Bunker", 57.0, 30.2, "KNOWN for the trenchline (2-12); the turret bunker is set into the line", None, 300, False),
    ("6-M3", "North Point Ferry Pens", "Supply Outpost Version 2", 41.0, 32.5, "KNOWN: 82 x 65 m (the pad op 3 found for this composition)", None, 300, False),
    ("6-M4", "Signal Ridge Comms", "CIS Communications FOB with GPs", 50.0, 40.0, "ASSUMED: 100 x 80 m", None, 300, False),
    ("6-02", "Prophet Road Checkpoint", "CIS Small Checkpoint with GPs", 28.4, 34.4, "KNOWN: A2-05", None, 300, False),
    ("6-03", "Massif AA", "CIS Heavy AA Tower w Interior GPs", 46.4, 44.0, "ASSUMED: as the CIS Flower Tower (1-11)", None, 300, False),
    ("6-04", "Prophet Limestone Quarry", "CIS Mining Complex with GPs", 60.0, 45.0, "ASSUMED: 120 x 90 m of terraced dig (160 x 120 m found no seat within 840 m)", None, 400, False),
    ("6-05", "Kamar Refuelling Base", "TKTA Refueling Base (Mono, Fixed)", 43.6, 32.3, "ASSUMED: as the CIS Fuel Depot (1-12)", None, 300, False),
    ("6-06", "East Slope Gun Line", "CIS Small Artillery Base with GPs", 63.8, 31.4, "KNOWN: 1-M3", None, 300, False),
    ("6-07", "North Point Pillboxes", "Small Wall with Bunker", 45.1, 29.1, "KNOWN as built: your 1-09 with this pick is a Small Rectangle FOB, 90 x 58 m", None, 300, False),
    ("6-08", "Signal Isle Landing", "CIS Landing Position with GPs", 44.5, 67.0, "KNOWN: 1-02 / 2-06 (a beach work)", None, 500, "beach"),
    ("6-09", "Signal Isle Depot", "CIS Depot (Fixed) with GPs (D)", 40.0, 30.0, "ASSUMED: 80 x 60 m", None, 300, False),
    ("6-10", "Kalam Rock Chapel", "TKTA Tower with Interior (Mono)", 15.0, 15.0, "ASSUMED: 30 x 30 m on the east rock (a cliff work: may come to the water's edge)", None, 250, "beach"),
    ("6-11", "North Cape AA", "CIS AA Tooth Fixed with GPs", 25.0, 25.0, "ASSUMED: 50 x 50 m", None, 300, False),
    ("6-12", "Deep-Sea Sensor Stack", "Giant Radar Dish", 15.0, 15.0, "REDUCED / ASSUMED: the stack top takes about 30 x 30 m (the dish and a ring of guns); air only", None, 120, "beach"),
    ("6-13", "Kamar Landers", "CIS Lander Base Fixed with GPs (D)", 44.5, 67.0, "ASSUMED: as the CIS Landing Position (1-02); a beach work", None, 300, "beach"),
    ("6-14", "Upper Spring Outpost", "Zavala CIS Outpost with GPs", 30.0, 30.0, "ASSUMED: 60 x 60 m (as op 3's Zavala outpost); seated beside the west climb road below the spring (the spring's own ridge at 385 m takes no road)", (14680, 11450), 150, False),
]

TOWNS = {"6-01": dict(name="Kamar Village", layout="../../../kernel_10nov_v1/K6_repass/kamar_village_v2/kamar_village_v2_layout.json",
                      entry=(16648.0, 11506.0), entry_z=246.0,
                      # street ends at the village's edge, each with the bearing a road leaves it on (K6 v2 layout)
                      ports=[(16648.0, 11506.0, 246.0, 180.0, "main street, south end"), (16786.0, 11566.0, 242.25, 180.0, "east lane, south end"),
                             (16584.0, 11540.0, 259.5, 180.0, "west lane, south end"), (16600.0, 11790.0, 236.5, 270.0, "north lane, west end"),
                             (16728.0, 11784.0, 239.0, 90.0, "north lane, east end")])}

# op 4's East Slope Comms pad: the end of op 4's Ember Crescent net (its own road leaves the south edge); op 6's net grows from its free edges
EXTERNAL_PADS = [dict(id="4-10 (op 4 net)", x=14800.0, y=9370.0, hx=20.1, hy=46.3, yaw=0.0, z=155.25, used_entrance=(14800.0, 9319.7))]
# the net climbs the south slope to the east upland first (the west side is cut by ravines), then spreads over the upland and back west
NETS = {"Ember Crescent": ["6-06", "6-13", "6-05", "6-M2", "6-01", "6-03", "6-F-T", "6-F", "6-M3", "6-07", "6-04", "6-02", "6-14"]}
ROOT = {"Ember Crescent": "4-10 (op 4 net)"}

SQUADS = [
    ("A6-01", "CIS Heavy Gun Position with GPs (D)", 30.1, 25.4, 16700, 10150, 300, "the south end of Kamar Strand and the landers"),
    ("A6-02", "CIS Heavy Gun Position + AA (UD)", 29.9, 40.8, 17050, 11250, 300, "the north end of Kamar Strand and the village quay"),
    ("A6-03", "CIS Small Checkpoint with GPs", 28.4, 34.4, 14750, 9900, 300, "the road up from Causeway Foot (op 4's net)"),
    ("A6-04", "CIS Heavy Gun Position with GPs (D)", 30.1, 25.4, 15150, 10600, 300, "the west climb between the checkpoint and the spring"),
    ("A6-05", "CIS Mixed AA Platform with GPs", 50.7, 46.4, 15700, 11700, 300, "the air over the monastery"),
    ("A6-06", "CIS Heavy Gun Position with AA (D)", 29.8, 42.5, 16600, 12300, 300, "the north point beach and the ferry pens"),
    ("A6-07", "CIS Heavy Gun Position with GPs (D)", 30.1, 25.4, 16700, 15500, 300, "Signal Isle's south shore over the channel"),
    ("A6-08", "CIS Small Checkpoint with GPs", 28.4, 34.4, 15900, 16300, 300, "the path up from the Signal Isle Landing"),
    ("A6-09", "CIS Heavy Gun Position + AA (UD)", 29.9, 40.8, 17300, 17200, 450, "the north-east sky and the north cape"),
    ("A6-10", "CIS Heavy Gun Position with AA (D)", 29.8, 42.5, 18000, 16100, 300, "the east rock and the sea toward the sensor stack"),
]

APPROACHES = {
    "6-F Prophet Monastery": ["by road from Causeway Foot (op 4's net) up the west climb, past the Upper Spring Outpost (6-14) and the Prophet Road Checkpoint (6-02) (vehicles)",
                              "the covered climb up the quarry (6-04) from the north-west, on foot"],
    "6-M1 Signal Isle Turbolaser Battery": ["by boat to the Signal Isle Landing (6-08) beach, then up past the Signal Ridge Comms (6-M4)",
                                            "by boat or air to the north cape under the North Cape AA (6-11), then up the north slope"],
    "6-M2 Kamar Strand Bunker Line": ["by boat to the black beach of Kamar Strand (shores list)", "by road down from the massif past the refuelling base (6-05) (vehicles)"],
    "6-M3 North Point Ferry Pens": ["by road from the Massif AA (6-03) (vehicles)", "by boat to the north point beach under the pillboxes (6-07)"],
    "6-M4 Signal Ridge Comms": ["from the Signal Isle Landing (6-08) up the ridge", "by air once the North Cape AA (6-11) falls"],
}
BOAT_ONLY = ("6-12",)

# the spring outpost is seated after the roads, beside the west climb road (its own ridge takes no road)
LATE_SITES = ("6-14",)
JUNCTION_MAX_LATE = 3.6      # its spur may meet the climb road at a step up to 3.6 m (a reported item, not a rule; the road builder ramps it)
