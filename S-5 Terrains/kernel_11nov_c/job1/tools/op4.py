"""Op 4, Cinder Road: site list, trunk, nets, squad anchors and approaches for the planner (pad half-sizes in metres)."""
NAME = "Cinder Road"
BOX = (12300, 19400, 3000, 10350)

SITES = [
    ("4-F", "Cinder Cone Fort", "CIS Flower Fortress with GPs", 60.0, 60.0, "ASSUMED: no pad of this composition exists; 120 x 120 m on the crater's west rim, with the crater floor as its inner yard (the CIS Flower Tower is 93 x 88 m)", (16390, 7460), 150, False),
    ("4-M1", "Mole Rock Gate", "CIS Double Pcannon Checkpoint with GPs", 35.5, 25.5, "KNOWN: 1-14 / A1-11 (a through-comp: the trunk runs through it)", None, 300, False),
    ("4-M2", "Cone Flank Batteries (artillery base)", "[Burnzy] CIS Arti-base", 63.8, 31.4, "ASSUMED: as the CIS Small Artillery Base (1-M3)", None, 400, False),
    ("4-M2-T", "Cone Flank Batteries (tower)", "CIS Flower Tower 2 AA (Mono)", 46.5, 50.5, "KNOWN: 2-M4", (17250, 7300), 350, False),
    ("4-M4", "Skerry AA Platform", "CIS Mixed AA Platform with GPs", 50.7, 46.4, "KNOWN: A1-07 / A2-08", None, 300, False),
    ("4-01", "North Causeway Gun", "CIS Guard Tower (PCannon) with GPS", 15.0, 15.0, "ASSUMED: 30 x 30 m beside the trunk on the north causeway", None, 300, False),
    ("4-02", "Cone Quarry", "41st Quarry", 50.0, 40.0, "ASSUMED: 100 x 80 m of pits", None, 350, False),
    ("4-03", "Lava Flow Trench", "CIS Basic Trenchline with GPs", 57.0, 30.2, "KNOWN: 2-12", (16150, 7250), 260, False),
    ("4-04", "South Foot Depot", "CIS Medium Logistics Base with GPs", 50.0, 40.0, "ASSUMED: between Supply Base Small_1 (82 x 65 m) and the Medium FOB (78 x 149 m)", None, 350, False),
    ("4-05", "Skerry Bunkers", "Tukata Turret Bunker", 25.0, 25.0, "ASSUMED: 50 x 50 m (your 1-05 with this pick was built as a Small Citadel, 148 x 153 m)", None, 300, False),
    ("4-06", "Flat Pillboxes", "Small Wall with Bunker", 45.1, 29.1, "KNOWN as built: your 1-09 with this pick is a Small Rectangle FOB, 90 x 58 m", None, 300, False),
    ("4-07", "Crescent Foot Fuel", "CIS Fuel Depot with GPs", 43.6, 32.3, "KNOWN: 1-12", None, 350, False),
    ("4-08", "Causeway Foot AA", "Tukata Air Defense Tower with GPs", 30.0, 30.0, "ASSUMED: 60 x 60 m", None, 350, False),
    ("4-09", "South Arm Road Checkpoint", "Tukata Checkpoint with GPs", 28.4, 34.4, "ASSUMED: as the CIS Small Checkpoint (A2-05)", None, 350, False),
    ("4-10", "East Slope Comms", "CIS Comms Array with GPs", 20.1, 46.3, "KNOWN: A1-03 / 2-08", None, 350, False),
    ("4-11", "Steam Vent Bores", "CIS Powerbank Facility with GPs", 60.0, 50.0, "REDUCED: the composition's own pad (2-14) is 192 x 166 m and nothing that big holds 4 m on the cone's north skirt; a 120 x 100 m pad fits (needs a smaller cut of the facility)", (16850, 7900), 250, False),
    ("4-12", "Black Beach Landers", "CIS Big Lander FOB with GPs", 60.0, 80.0, "ASSUMED: 120 x 160 m; a beach work (may come to the water's edge)", None, 400, "beach"),
]

TOWNS = {"4-M3": dict(name="Causeway Foot", layout="../../../kernel_10nov_v1/K6_repass/causeway_foot_v2/causeway_foot_v2_layout.json",
                      entry=(14300.0, 8176.0), entry_z=1.5,
                      exits={"west (south-arm road)": (13849.0, 8133.0, 12.31), "north (slope road)": (14165.0, 8442.0, 36.67)})}

# the AI road trunk, south to north: from op 2's net at the causeway head, through the Mole Rock Gate and the cone fort, into Causeway Foot
TRUNK = [
    dict(stop=("xyz", (15845.0, 4060.0)), label="the south causeway's south end (3.5 m); the join up to op 2's net is a 20 m step that needs your ramp"),
    dict(stop=("site", "4-M1"), through=True, kind="dirt", width=7.0, grade=0.14),
    dict(stop=("site", "4-F"), through=False, kind="dirt", width=7.0, grade=0.14),
    dict(stop=("xyz", (15720.0, 7845.0)), label="the north causeway's cone end (3.5 m); the climb from here onto the cone is a 45 m step that needs your ramp"),
    dict(stop=("town", "4-M3"), kind="dirt", width=7.0, grade=0.14),
]

NETS = {"Cinder Cone, Mole Rock and the south causeway": ["4-04", "4-06", "4-02", "4-03", "4-11", "4-12", "4-M2", "4-M2-T"],
        "Ember Crescent and the north causeway": ["4-01", "4-07", "4-09", "4-08", "4-10"]}
ROOT = {k: "TRUNK" for k in NETS}

SQUADS = [
    ("A4-01", "CIS Small Checkpoint with GPs", 28.4, 34.4, 15950, 4300, 300, "the south causeway's head, between the Terrace and Mole Rock"),
    ("A4-02", "CIS Heavy Gun Position with GPs (D)", 30.1, 25.4, 16300, 6350, 250, "the south causeway landfall on the cone"),
    ("A4-03", "CIS Heavy Gun Position + AA (UD)", 29.9, 40.8, 17000, 6700, 300, "the cone's south-east flank and the sea toward the skerries"),
    ("A4-04", "CIS Mixed AA Platform with GPs", 50.7, 46.4, 16050, 7750, 300, "the air over the north causeway and the cone's west flank"),
    ("A4-05", "CIS Heavy Gun Position with AA (D)", 15700, 8050, 250, 250, "the north causeway's cone end"),
    ("A4-06", "CIS Heavy Gun Position with GPs (D)", 30.1, 25.4, 14650, 8150, 250, "the north causeway's landfall at Causeway Foot"),
    ("A4-07", "CIS Heavy Gun Position + AA (UD)", 29.9, 40.8, 16750, 8250, 300, "the cone's north beach and the landers"),
    ("A4-08", "CIS Small Checkpoint with GPs", 28.4, 34.4, 13450, 7850, 300, "the south-arm road west of Causeway Foot"),
    ("A4-09", "CIS Heavy Gun Position with AA (D)", 29.8, 42.5, 14450, 9100, 300, "the slope road above Causeway Foot, between the AA and the comms"),
    ("A4-10", "CIS Heavy Gun Position with GPs (D)", 30.1, 25.4, 18350, 7650, 300, "the skerry channel between the AA platform and the bunkers"),
]
SQUADS[4] = ("A4-05", "CIS Heavy Gun Position with AA (D)", 29.8, 42.5, 15700, 8050, 250, "the north causeway's cone end")

APPROACHES = {
    "4-F Cinder Cone Fort": ["by the trunk road over the south causeway, through the Mole Rock Gate and up the cone's south side (vehicles)",
                             "from the north causeway or the cone's north beach (the landers) up the cone's north-west side, on foot or on the trunk"],
    "4-M1 Mole Rock Gate": ["along the south causeway from the Airfield Terrace (vehicles, on the trunk)", "by boat to Mole Rock's own shore (see shores)"],
    "4-M2 Cone Flank Batteries": ["by boat to the cone's east shore below the batteries", "along the cone's east flank road from the South Foot Depot (vehicles)"],
    "4-M3 Causeway Foot": ["over the north causeway from the cone (vehicles, on the trunk)", "by boat to the beach south of the town, or down the slope road from the north"],
    "4-M4 Skerry AA Platform": ["by boat to the skerry's landing below the bunkers (4-05)", "by air once the platform's own AA is suppressed from the cone (no LZ given)"],
}
BOAT_ONLY = ("4-M4", "4-05")
VIEW = (12600, 19300, 3200, 10000)

# per-site search options: the fort keeps off the crater floor (no road can cross the crater's 20-25 m inner wall within the rules)
SITE_KW = {"4-F": dict(avoid=[(16620, 7360, 150)])}
