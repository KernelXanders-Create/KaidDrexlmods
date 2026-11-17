"""Op 3 The Peat-Gas Fields on the K3 A sketch ground (dry run until drop 2). Comps from DECISIONS.md (JOB_2)."""
import world, sizes
R = {s["id"]: s for s in world.objectives()["sites"]}
BOX = (9200, 16000, 0, 8600)
NAME = "The Peat-Gas Fields (sketch)"
HG = "CIS Heavy Gun Position + AA (UD)"; SC = "CIS Small Checkpoint with GPs"; TR = "CIS Basic Trenchline with GPs"; RF = "CIS Small Rectangle FOB with GPs"
SPEC = [
 ("3-F", ["CIS Mining Complex with GPs", "CIS Large Fuel Depot with GPs", "flare-stack field"], 500),
 ("3-M1", ["CIS Flower Fortress with GPs"], 400),
 ("3-M2", ["CIS Large Power Facility with GPs", HG, "TKTA Checkpoint Fixed (Mono)", RF], 450),
 ("3-M3", ["[Burnzy] CIS Arti-base + Flower Tower 2"], 400),
 ("3-M4", ["CIS Medium Logistics Base with GPs", HG], 400),
 ("3-01", ["CIS Fuel Depot with GPs"], 350), ("3-02", ["CIS Depot (Fixed) with GPs (D)"], 400), ("3-03", ["CIS Medium AA Base with GPs"], 400),
 ("3-04", ["Small Wall with Bunker"], 300), ("3-05", [SC, HG], 300), ("3-06", ["CIS Fuel Depot with GPs"], 350),
 ("3-07", ["Zavala CIS Outpost with GPs"], 350), ("3-08", ["CIS Medium Logistics Base with GPs"], 400), ("3-09", ["Giant Radar Dish"], 350),
 ("3-10", [TR, TR, RF], 400), ("3-11", ["Claus - Small Radar"], 300), ("3-12", [SC, HG], 300),
]
SITES = sizes.sites(SPEC, R)
NETS = {"op 3": [s[0] for s in SITES if s[0] != "3-M2" and s[0] != "3-11"]}
ROOT = {"op 3": "3-M2"}
APPROACHES = {"3-F Peat-Gas Works": ["W along the pipeline road past 3-M2 (297 deg)", "SW past 3-M4 / 3-02 (243 deg)"],
              "3-M1 Kettle East Fort": ["WSW past 3-12 (253 deg)", "S from 3-F once it falls (188 deg)"],
              "3-M2 Pipeline Pumping Station": ["W from the start (273 deg)", "SW past 3-05 (235 deg)"],
              "3-M3 East Crater Battery": ["SW past 3-M1 (220 deg)", "WSW past 3-07 (256 deg)"],
              "3-M4 Gasworks Spur": ["NW past 3-05 (315 deg)", "E from 3-02 once it falls (72 deg)"]}
