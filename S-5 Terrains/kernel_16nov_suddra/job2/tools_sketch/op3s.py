"""Op 3 The Peat-Gas Fields on the K3 A sketch ground (dry run until drop 2). Comps from DECISIONS.md (JOB_2)."""
import world, sizes
R = {s["id"]: s for s in world.objectives()["sites"]}
BOX = (7900, 16000, 0, 8600)
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
# decision 44: op 3's two entry roads from the 1-F FOB (8200, 3600): the pipeline road through 3-05's point to 3-M2,
# and the spur road through 3-12's point to 3-M1; the rest of the net grows from them
TRUNKS = [
    [dict(stop=("xyz", (8200.0, 3600.0)), name="1-F FOB", label="1-F FOB (op 1's final; its exact spot comes in drop 2)"),
     dict(stop=("xyz", (10300.0, 2500.0)), label="3-05 Pipeline Checkpoint's point", kind="dirt", width=7.0, grade=0.14),
     dict(stop=("site", "3-M2"), through=False, kind="dirt", width=7.0, grade=0.14)],
    [dict(stop=("xyz", (8300.0, 3780.0)), name="1-F FOB", label="1-F FOB, north exit (the FOB counts as one node: both entry roads leave it)"),
     dict(stop=("xyz", (11000.0, 4600.0)), label="3-12 Spur Bridge Gate's point", kind="dirt", width=7.0, grade=0.14),
     dict(stop=("site", "3-M1"), through=False, kind="dirt", width=7.0, grade=0.14)],
]
_ORDER = [s[0] for s in SITES if s[0] not in ("3-M2", "3-M1", "3-11")]
_ORDER = [x for x in _ORDER if not x.startswith("3-F")] + ["3-F", "3-F.2", "3-F.3"]     # the Works joins last, onto a fuller net (first, it hugged 3-M2's pad)
NETS = {"op 3": _ORDER}
ROOT = {"op 3": "TRUNK"}
APPROACHES = {"3-F Peat-Gas Works": ["W along the pipeline road past 3-M2 (297 deg)", "SW past 3-M4 / 3-02 (243 deg)"],
              "3-M1 Kettle East Fort": ["WSW past 3-12 (253 deg)", "S from 3-F once it falls (188 deg)"],
              "3-M2 Pipeline Pumping Station": ["W from the start (273 deg)", "SW past 3-05 (235 deg)"],
              "3-M3 East Crater Battery": ["SW past 3-M1 (220 deg)", "WSW past 3-07 (256 deg)"],
              "3-M4 Gasworks Spur": ["NW past 3-05 (315 deg)", "E from 3-02 once it falls (72 deg)"]}

# decision 43: checkpoints are seated astride a road of the net after the net is built
ASTRIDE = ("3-05", "3-12", "3-M2.3")

# route at 13 % so the cut-grid reading (bands of joining roads overlap at junctions) stays under the 14 % rule
NET_GRADE = 0.13
