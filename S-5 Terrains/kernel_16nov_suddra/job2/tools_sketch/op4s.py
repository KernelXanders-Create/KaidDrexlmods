"""Op 4 The Drain on the K3 A sketch ground (dry run until drop 2). Comps from DECISIONS.md (JOB_2).
The AI never crosses water: one net per bank; the three crossings are GAPS between the banks' crossing ends (POINT_TARGETS)."""
import world, sizes
R = {s["id"]: s for s in world.objectives()["sites"]}
BOX = (3800, 14400, 5400, 10400)
NAME = "The Drain (sketch)"
HG = "CIS Heavy Gun Position + AA (UD)"; SC = "CIS Small Checkpoint with GPs"; TR = "CIS Basic Trenchline with GPs"; RF = "CIS Small Rectangle FOB with GPs"
SPEC = [
 ("4-F", ["CIS Turbolaser Tower with GPs"], 300),          # the Danger Dam (owner: placed as built) is the crossing itself (GAPS); its lock tower stands on the south bank
 ("4-M1", ["town outline (about 80 buildings)", SC, HG, SC, HG], 500),
 ("4-M3", ["CIS Metal Trench Line with GPs", TR, TR, RF], 450), ("4-M4", ["CIS Landing Position with GPs"], 400),     # 4-M3: call 4A
 ("4-01", ["CIS Big Radio Tower with GPs"], 300), ("4-02", ["Tukata Turret Bunker", RF], 300), ("4-03", [TR, TR, RF], 400),     # 4-02: call 4A
 ("4-04", ["CIS Fuel Depot with GPs", HG], 350), ("4-05", ["CIS Powerbank Facility with GPs"], 400), ("4-06", [SC, HG], 300),
 ("4-07", ["Medium Covered AA Base with GPs"], 400), ("4-08", ["[Burnzy] CIS Arti-base + Flower Tower 2"], 400),
 ("4-09", ["Zavala CIS Outpost with GPs"], 350), ("4-10", ["CIS Vehicle Depot with GPs (D)"], 400), ("4-11", ["Small Wall with Bunker", RF], 300),     # call 4A
 ("4-12", ["Claus - Small Radar"], 300),
]
SITES = sizes.sites(SPEC, R)
# call 14A: the village's two road gates stand where its two roads reach the foot of the mound: east (to 4-M3, decision 46) and NNW (to 4-09)
SITES = [(t[0], t[1], t[2], t[3], t[4], t[5], {"4-M1.2": (5440.0, 7800.0), "4-M1.4": (5110.0, 8030.0), "4-M1.3": (4960.0, 7880.0), "4-M1.5": (5330.0, 7660.0)}.get(t[0], t[6]), t[7], t[8]) for t in SITES]
# 4-M2 Drain Rail Bridge: a gate at each end of the 3AS bridge (decision 8): the Pcannon checkpoint and the gun position on the south bank, the TKTA on the north bank
SITES += [("4-M2", "Drain Rail Bridge (south gate)", "CIS Double Pcannon Checkpoint with GPs", 35.5, 25.5, sizes.size("CIS Double Pcannon Checkpoint with GPs")[2], (8200, 6930), 250, False),
          ("4-M2.2", "Drain Rail Bridge (gun position)", HG, 29.9, 40.8, sizes.size(HG)[2], (8320, 6900), 300, False),
          ("4-M2.3", "Drain Rail Bridge (north gate)", "TKTA Checkpoint Fixed (Mono)", 30.0, 20.0, sizes.size("TKTA Checkpoint Fixed (Mono)")[2], (8200, 7290), 250, False)]
POINT_TARGETS = {"rail bridge S": (8200.0, 6990.0), "rail bridge N": (8200.0, 7235.0), "dam S": (10393.0, 7140.0), "dam N": (10393.0, 7320.0),
                 "armour causeway S": (10293.0, 7140.0), "armour causeway N": (10293.0, 7330.0),     # call 6A + decision 47: west of the Danger Dam
                 "village east road": (5600.0, 7800.0), "village NNW road": (4900.0, 8450.0)}     # decision 46 / call 14A: the east road reaches the village from 4-M3
POINT_TARGETS.update({
                 "causeway S": (7583.0, 7020.0), "causeway N": (7583.0, 7185.0)})
SOUTH = ["4-F", "4-M2", "4-M2.2", "4-M4", "4-01", "4-04", "4-04.2", "4-05", "4-07", "rail bridge S", "dam S", "causeway S", "armour causeway S"]
NETS = {"south bank": SOUTH, "north bank": [s[0] for s in SITES if s[0] not in SOUTH and s[0] not in ("4-M3", "4-12")] + ["rail bridge N", "dam N", "causeway N", "armour causeway N", "village east road", "village NNW road"]}
ROOT = {"south bank": "4-04", "north bank": "4-M3"}
# the village's two roads: the east road first (from 4-M3's net to the village), then the village, then 4-09 (the NNW road)
_N = NETS["north bank"]; _first = ["village east road", "4-M1", "village NNW road", "4-09"]
NETS["north bank"] = _first + [x for x in _N if x not in _first]
NETS["south bank"].remove("4-04")
GAPS = [dict(at=(8200, 7110), label="the Drain Rail Bridge (3AS, armour 7.5 m): span between the rail bridge's south and north ends"),
        dict(at=(10393, 7230), label="the Drain Locks: the Danger Dam, placed as built (its crest's AI use NOT MEASURED)"),
        dict(at=(10293, 7235), label="the armour causeway west of the dam (7.5 m clear, its own AI road line; call 6A, decision 47)"),
        dict(at=(7583, 7100), label="the Plank Road causeway (truck 3.1 m, crest +1.0 m) between its south and north ends")]
APPROACHES = {"4-F Drain Locks": ["SW past 4-04 (215 deg)", "W along the bank from 4-M2 once it falls (269 deg)"],
              "4-M1 Peat Cutters' Village": ["SSE past 4-07 (150 deg)", "NNW past 4-09 (336 deg)"],
              "4-M2 Drain Rail Bridge": ["SSW past 4-01 to the south gate (190 deg)", "over the 4-06 causeway to the north gate (309 deg)"],
              "4-M3 Central Salient": ["SSW past 4-11 from the Rail Bridge (214 deg)", "WSW from the 4-06 causeway (238 deg)"],
              "4-M4 Barge Quay": ["WSW past 4-05 (250 deg)", "by player boat through the lock once 4-F falls"]}

# decision 43: checkpoints are seated astride a road of the net after the net is built
ASTRIDE = ("4-06", "4-M1.2", "4-M1.4", "4-M2", "4-M2.3")

# route at 13 % so the cut-grid reading (bands of joining roads overlap at junctions) stays under the 14 % rule
NET_GRADE = 0.13

# call 5B: the trenches of 4-03 and 4-M3 stand on breastworks at +2.5 m or more
SITE_KW = {"4-03": dict(z_floor=2.5), "4-03.2": dict(z_floor=2.5), "4-M3": dict(z_floor=2.5), "4-M3.2": dict(z_floor=2.5), "4-M3.3": dict(z_floor=2.5)}

# call 14A: each village gate stands on the road it guards
ASTRIDE_ROAD = {"4-M1.2": "village east road", "4-M1.4": "village NNW road"}
