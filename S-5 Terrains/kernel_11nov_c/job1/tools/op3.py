"""Op 3, The Sound: site list for the planner. Sizes are pad half-sizes (hx, hy) in metres.
KNOWN = the same composition's pad in pads_op1 / pads_op2; ASSUMED = no pad of that composition exists yet (named nearest kin)."""

BOX = (0, 9500, 6800, 13600)
PLAN_KW = dict(band_range=10.0, steep=1.0, repair_to=3.6)     # as ops 5-8 (re-pass): every road is still measured against 14 % and 4 m

# id, name, composition, hx, hy, size evidence, rough x, y (None = purpose map), search radius, water mode, priority
SITES = [
    ("3-F", "Sound Gate: south headland keep", "NEW 2: Sound fortress kit (keep)", 20.0, 20.0, "ASSUMED: no pad of the new kit exists; the south headland has only a 21 m shelf beside the ring islet at the mouth, which takes a 40 x 40 m keep (a sea work: may stand at the water's edge)", (3880, 10820), 120, "beach"),
    ("3-F-N", "Sound Gate: north headland keep", "NEW 2: Sound fortress kit (keep)", 30.0, 30.0, "ASSUMED, as the south keep, on the north headland point", (3510, 11150), 160, "beach"),
    ("3-M1", "South Notch Keep", "NEW 2: Sound fortress kit (keep + wall)", 40.0, 55.0, "ASSUMED: keep and wall across the gully, 80 x 110 m", None, 450, False),
    ("3-M2", "West Notch Keep", "NEW 2: Sound fortress kit (keep + wall)", 35.0, 45.0, "ASSUMED: 70 x 90 m", None, 450, False),
    ("3-M4", "Summit AA", "CIS Heavy AD Tower with GPs", 46.4, 44.0, "ASSUMED: as the CIS Flower Tower (1-11)", None, 400, False),
    ("3-01", "Cliff Galleries", "Royal Tunnel Holdout 1 (Mono)", 30.0, 25.0, "ASSUMED: tunnel mouth pad 60 x 50 m on the cliff top", None, 350, False),
    ("3-02", "Terrace Farms Post", "CIS Outpost with GPs (D)", 30.0, 30.0, "ASSUMED: 60 x 60 m", None, 350, False),
    ("3-03", "South Cape Landers", "CIS Landing Position with GPs", 44.5, 67.0, "KNOWN: 1-02 / 2-06", None, 500, "beach"),
    ("3-04", "Notch Road Checkpoint", "CIS Heavy Checkpoint with GPs", 32.9, 49.5, "ASSUMED: as the CIS Double Checkpoint (2-07)", None, 350, False),
    ("3-06", "Shoal Pillboxes", "Small Wall with Bunker", 20.0, 12.0, "ASSUMED: 40 x 24 m on the tephra bank", None, 250, "beach"),
    ("3-07", "Shoal Wreck Fort", "Falling Lander Unarmed", 40.0, 40.0, "ASSUMED: 80 x 80 m on the bar", None, 250, "beach"),
    ("3-08", "Peak Relay Dish", "Giant Comms Antenna Array", 40.0, 40.0, "ASSUMED: twice the CIS Comms Array's short side", None, 400, False),
    ("3-09", "Sound Rim Guns", "CIS AAT Turbolaster Base with GPs", 45.0, 45.0, "ASSUMED: 90 x 90 m", None, 400, False),
    ("3-10", "North Cove Outpost", "Zavala CIS Outpost with GPs", 30.0, 30.0, "ASSUMED: 60 x 60 m", None, 400, False),
    ("3-11", "West Cliff Battery", "CIS Small Artillery Base with GPs", 63.8, 31.4, "KNOWN: 1-M3", None, 400, False),
    ("3-12", "Ridge Stair Tower", "CIS Guard Tower with GPs", 15.0, 15.0, "ASSUMED: 30 x 30 m", None, 350, False),
    ("3-13", "Sound Fuel Depot", "CIS Fuel Depot with GPs", 43.6, 32.3, "KNOWN: 1-12", None, 400, False),
    ("3-14", "Inland Ramp Depot", "CIS Elevated Ramp Depot with GPs", 60.6, 39.5, "ASSUMED: as the CIS Elevated Landing Pad Construction (2-01)", None, 400, False),
    ("3-15", "Ash Middle Comms", "CIS Comms Array with GPs", 20.1, 46.3, "KNOWN: A1-03 / 2-08", None, 400, False),
    ("3-16", "Ash South Gun Line", "CIS Turbolaser Tower with GPs", 27.5, 30.1, "KNOWN: 2-09", None, 400, False),
]

# the town (3-M3 Sound Head) is the K6 v2 layout; its road joins at the gate square (the town's south-east lip)
TOWNS = {"3-M3": dict(name="Sound Head", layout="../../../kernel_10nov_v1/K6_repass/sound_head_v2/sound_head_v2_layout.json", entry=(2658.0, 10442.0), entry_z=33.0)}
NAME = "The Sound"

# the sea gate itself is not a pad: it spans the water between the two keeps
GATE = ((3900.0, 10805.0), (3510.0, 11130.0))

# road net on Sound Isle grows from the town's gate square; each site joins the nearest part of the net (dirt, 7 m)
NETS = {
    "Sound Isle": ["3-M4", "3-14", "3-08", "3-02", "3-M2", "3-11", "3-01", "3-F-N", "3-09", "3-10", "3-04", "3-12", "3-M1", "3-03", "3-F"],
    "Ash Crescent": ["3-15", "3-16"],
}
ROOT = {"Sound Isle": "3-13", "Ash Crescent": "3-15"}

# squad-size positions: (id, composition, hx, hy, anchor x, y, radius, what it guards)
SQUADS = [
    ("A3-01", "CIS Heavy Gun Position with GPs (D)", 30.1, 25.4, 3500, 8050, 250, "the South Notch beach and the gully mouth below the South Notch Keep"),
    ("A3-02", "CIS Heavy Gun Position with AA (D)", 29.8, 42.5, 2600, 7750, 300, "the South Cape beach and the landers (the FOB fallback)"),
    ("A3-03", "CIS Small Checkpoint with GPs", 28.4, 34.4, 3250, 8900, 300, "the Notch road near the Ridge Stair Tower's road junction"),
    ("A3-04", "CIS Heavy Gun Position + AA (UD)", 29.9, 40.8, 3550, 9500, 300, "the east beach under the Ridge Stair Tower"),
    ("A3-05", "CIS Heavy Gun Position with GPs (D)", 30.1, 25.4, 900, 9700, 300, "the west-coast approach to the West Notch"),
    ("A3-06", "CIS Mixed AA Platform with GPs", 50.7, 46.4, 1800, 10400, 350, "the air over the Sound head, between the fuel depot and the summit"),
    ("A3-07", "CIS Heavy Gun Position with AA (D)", 29.8, 42.5, 2350, 12500, 350, "the north cove beach, the back door"),
    ("A3-08", "CIS Small Checkpoint with GPs", 28.4, 34.4, 2900, 11200, 300, "the north shore shelf between the Cliff Galleries and the north gate keep (no road there: foot and boat)"),
    ("A3-09", "CIS Heavy Gun Position + AA (UD)", 29.9, 40.8, 4100, 10650, 300, "the Sound mouth from the south cliff, over the gate"),
    ("A3-10", "CIS Heavy Gun Position with GPs (D)", 30.1, 25.4, 8250, 9800, 300, "the Ash Crescent shore between the comms and the gun line"),
]

# two designed approaches per main (and the final); none is a landing zone and none sets an order
APPROACHES = {
    "3-F Sound Gate": ["by boat to the beach just east of the mouth (x 4140-4240, y 10840-10850) or onto the south keep's own shelf beside the ring islet",
                       "from the north cove beach along the north shore shelf to the north keep (3-F-N), then the gate's north end"],
    "3-M1 South Notch Keep": ["from the beach at x 3310-3430, y 7525-7565 (shore list), north along the coast and up the gully into the keep's wall",
                              "down the Notch road from the plateau (3-04 Notch Road Checkpoint), on the road net, with vehicles"],
    "3-M2 West Notch Keep": ["from the west-coast beach at x 510, y 10675-10730 (shore list), south along the coast and up the gully",
                             "on foot from the plateau: Terrace Farms Post (3-02) down the west slope to the keep's back"],
    "3-M3 Sound Head": ["by boat into the Sound to the town quay (under the gate's guns until 3-F falls)",
                        "on foot down the crater stair from the plateau road (see foot links)"],
    "3-M4 Summit AA": ["by road from the Inland Ramp Depot (3-14) and the Peak Relay Dish (3-08)", "by road from the Sound Fuel Depot (3-13)"],
}
BOAT_ONLY = ("3-06", "3-07")
