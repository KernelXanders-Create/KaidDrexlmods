"""Op 4 The Drain on the K3 A sketch ground (dry run until drop 2). Comps from DECISIONS.md (JOB_2).
The AI never crosses water: one net per bank; the three crossings are GAPS between the banks' crossing ends (POINT_TARGETS)."""
import world, sizes
R = {s["id"]: s for s in world.objectives()["sites"]}
BOX = (3800, 14400, 5400, 10400)
NAME = "The Drain (sketch)"
HG = "CIS Heavy Gun Position + AA (UD)"; SC = "CIS Small Checkpoint with GPs"; TR = "CIS Basic Trenchline with GPs"; RF = "CIS Small Rectangle FOB with GPs"
SPEC = [
 ("4-F", ["CIS Turbolaser Tower with GPs"], 300),          # the CIS Fortress Dam is the crossing itself (GAPS); its lock tower stands on the south bank
 ("4-M1", ["town outline (about 80 buildings)", SC, HG, SC, HG], 500),
 ("4-M3", ["CIS Metal Trench Line with GPs"], 400), ("4-M4", ["CIS Landing Position with GPs"], 400),
 ("4-01", ["CIS Big Radio Tower with GPs"], 300), ("4-02", ["Tukata Turret Bunker"], 300), ("4-03", [TR, TR, RF], 400),
 ("4-04", ["CIS Fuel Depot with GPs", HG], 350), ("4-05", ["CIS Powerbank Facility with GPs"], 400), ("4-06", [SC, HG], 300),
 ("4-07", ["Medium Covered AA Base with GPs"], 400), ("4-08", ["[Burnzy] CIS Arti-base + Flower Tower 2"], 400),
 ("4-09", ["Zavala CIS Outpost with GPs"], 350), ("4-10", ["CIS Vehicle Depot with GPs (D)"], 400), ("4-11", ["Small Wall with Bunker"], 300),
 ("4-12", ["Claus - Small Radar"], 300),
]
SITES = sizes.sites(SPEC, R)
# 4-M2 Drain Rail Bridge: a gate at each end of the 3AS bridge (decision 8): the Pcannon checkpoint and the gun position on the south bank, the TKTA on the north bank
SITES += [("4-M2", "Drain Rail Bridge (south gate)", "CIS Double Pcannon Checkpoint with GPs", 35.5, 25.5, sizes.size("CIS Double Pcannon Checkpoint with GPs")[2], (8200, 6930), 250, False),
          ("4-M2.2", "Drain Rail Bridge (gun position)", HG, 29.9, 40.8, sizes.size(HG)[2], (8320, 6900), 300, False),
          ("4-M2.3", "Drain Rail Bridge (north gate)", "TKTA Checkpoint Fixed (Mono)", 30.0, 20.0, sizes.size("TKTA Checkpoint Fixed (Mono)")[2], (8200, 7290), 250, False)]
POINT_TARGETS = {"rail bridge S": (8200.0, 6990.0), "rail bridge N": (8200.0, 7235.0), "dam S": (10393.0, 7140.0), "dam N": (10393.0, 7320.0),
                 "causeway S": (7583.0, 7020.0), "causeway N": (7583.0, 7185.0)}
SOUTH = ["4-F", "4-M2", "4-M2.2", "4-M4", "4-01", "4-04", "4-04.2", "4-05", "4-07", "rail bridge S", "dam S", "causeway S"]
NETS = {"south bank": SOUTH, "north bank": [s[0] for s in SITES if s[0] not in SOUTH and s[0] not in ("4-M3", "4-12")] + ["rail bridge N", "dam N", "causeway N"]}
ROOT = {"south bank": "4-04", "north bank": "4-M3"}
NETS["south bank"].remove("4-04")
GAPS = [dict(at=(8200, 7110), label="the Drain Rail Bridge (3AS, armour 7.5 m): span between the rail bridge's south and north ends"),
        dict(at=(10393, 7230), label="the Drain Locks dam crest (CIS Fortress Dam, armour 7.5 m) between the dam's south and north ends"),
        dict(at=(7583, 7100), label="the Plank Road causeway (truck 3.1 m, crest +1.0 m) between its south and north ends")]
APPROACHES = {"4-F Drain Locks": ["SW past 4-04 (215 deg)", "W along the bank from 4-M2 once it falls (269 deg)"],
              "4-M1 Peat Cutters' Village": ["SSE past 4-07 (150 deg)", "NNW past 4-09 (336 deg)"],
              "4-M2 Drain Rail Bridge": ["SSW past 4-01 to the south gate (190 deg)", "over the 4-06 causeway to the north gate (309 deg)"],
              "4-M3 Central Salient": ["SSW past 4-11 from the Rail Bridge (214 deg)", "WSW from the 4-06 causeway (238 deg)"],
              "4-M4 Barge Quay": ["WSW past 4-05 (250 deg)", "by player boat through the lock once 4-F falls"]}
