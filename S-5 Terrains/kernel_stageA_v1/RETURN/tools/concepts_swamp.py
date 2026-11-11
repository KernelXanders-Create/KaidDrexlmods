"""Swamp (2nd Company): three PROPOSED concepts. Same row format as islands.

Arma has one sea level (0 m), so every swamp sits on land at about +0.2 to
+3 m with water cut below 0 m. Map edges rise so no open sea is visible.
"""
import numpy as np
import terrain_lib as T
from terrain_lib import X, Y

ROAD = dict(color="#3b2a1a", lw=1.6, ls="-", label="proposed AI road (gentle, clear lane)")
RAIL = dict(color="#222222", lw=2.2, ls=(0, (6, 2)), label="rail embankment (vehicle lane)")
TRENCH = dict(color="#6b3e1f", lw=2.0, ls=(0, (2, 1.5)), label="trench belt (objects, PROPOSED)")
BOARD = dict(color="#7a5c2e", lw=1.4, ls=(0, (1, 1.5)), label="boardwalk (normal objects, 04)")


def _bump(H, bump, eps=0.05):
    """Raise terrain to `bump` only where the bump exists (keeps water elsewhere)."""
    H[:] = np.where(bump > eps, np.maximum(H, bump), H)


def _teardrops(H, seed, n, region, rx_rng, ry_rng, h_rng, tail=1.6, avoid=None):
    """Tree islands (hammocks) shaped like teardrops, tails downstream (south)."""
    rng = np.random.default_rng(seed)
    WX, WY = T.warp(seed, 90, 500)
    x0, y0, x1, y1 = region
    placed = []
    for _ in range(n):
        cx, cy = rng.uniform(x0, x1), rng.uniform(y0, y1)
        if avoid is not None and avoid(cx, cy):
            continue
        rx, ry, h = rng.uniform(*rx_rng), rng.uniform(*ry_rng), rng.uniform(*h_rng)
        u, v = (WX - cx) / rx, (WY - cy) / ry
        v = np.where(v < 0, v / tail, v)
        d = np.hypot(u, v)
        np.maximum(H, h * T.smoothstep(1.0, 0.55, d), out=H, where=d < 1.0)
        placed.append((cx, cy))
    return placed


# =================================================================== A
def swamp_A():
    """The Mire Line: Mimban-style shell-cratered peat bog with eskers."""
    H = 0.65 + 0.3 * T.fbm(301, 1500, 3) + 0.2 * T.fbm(302, 250, 3)
    rng = np.random.default_rng(303)
    # Bog pools and kettle lakes (below 0)
    for _ in range(90):
        x, y = rng.uniform(500, 15500), rng.uniform(1800, 14200)
        T.set_blob(H, x, y, rng.uniform(40, 240), rng.uniform(-1.6, -0.5), soft=60, seed=0, mode="min")
    for (x, y, r) in [(2200, 6600, 450), (4600, 9000, 380), (13800, 4200, 420), (6000, 12000, 300)]:
        T.set_blob(H, x, y, r, -1.6, soft=120, seed=1, mode="min")
    # Eskers: winding gravel ridges NW-SE (the only firm high ground in the bog)
    eskers = [T.chaikin([(1200, 15000), (2200, 12600), (3100, 10600), (3400, 8200), (4600, 5600), (5600, 3100)]),
              T.chaikin([(5600, 14400), (6600, 12600), (8800, 10600), (10400, 8600), (12200, 6500)]),
              T.chaikin([(10200, 15300), (12400, 13600), (13600, 12000), (15500, 10200)])]
    for k, e in enumerate(eskers):
        T.raise_line(H, e, 110, 9 + 3 * k, soft=110)
    # The Drain: sluggish channel W-E (boats, hovers)
    drain = T.chaikin([(0, 7300), (2600, 6900), (5200, 7400), (7600, 7000), (10600, 7300), (13200, 6900), (16000, 7200)])
    T.carve_line(H, drain, 70, 1.8, soft=40)
    # Shell craters over the old front
    H += T.crater_field(304, 900, (1000, 3000, 15000, 14200), (20, 60), 1.8)
    # The Cauldron: orbital-strike crater, raised rim, flooded floor
    d = np.hypot(X - 11000, Y - 11000) * (1 + 0.06 * T.noise(305, 300))
    _bump(H, 12 * T.smoothstep(700, 470, d))
    H[:] = np.where(d < 430, -1.5 + 0.4 * T.noise(306, 80), H)
    # Moraines framing the map: Republic lines south, CIS highland north
    H += 14 * T.smoothstep(1700, 0, Y + 300 * T.noise(307, 900)) + 32 * T.smoothstep(14200, 16000, Y + 400 * T.noise(308, 900))
    rail = T.chaikin([(1800, 0), (4200, 2000), (5600, 2800), (7600, 6000), (9200, 9000), (11400, 13000), (12000, 16000)])
    T.raise_line(H, rail, 30, 3.0, soft=40)
    trenches = [T.chaikin([(500, 4300), (3000, 4700), (5200, 4200), (8000, 4000), (10400, 4900), (12500, 4400), (15500, 4800)]),
                T.chaikin([(1200, 8800), (4200, 8300), (6600, 8200), (9000, 8700), (11400, 8100), (14600, 8600)]),
                T.chaikin([(600, 13100), (3600, 12700), (6400, 13400), (9600, 13600), (13000, 13100), (15400, 13500)])]
    roads = [eskers[0], eskers[1], T.chaikin([(8000, 0), (8100, 2600), (7800, 5200), (7600, 7000), (8600, 9400), (9600, 13600), (8400, 15400)])]
    lines = [(rail, RAIL)] + [(r, ROAD) for r in roads] + [(t, TRENCH) for t in trenches]
    labels = [("Republic lines (south moraine)", 8000, 600), ("CIS moraine", 3000, 15600), ("the Drain", 1400, 7700),
              ("The Cauldron", 11000, 12000), ("esker", 2500, 11500), ("esker", 9600, 9600), ("crater field", 13800, 5600)]
    crossings = [("The Drain (main crossing at bridge)", (7600, 6600), (7600, 7400), "bridge; or wade/swim"),
                 ("Kettle lake west", (1700, 6600), (2700, 6600), "boat/hover; walk round"),
                 ("Cauldron floor", (10600, 11000), (11400, 11000), "stilt decks over flooded floor"),
                 ("Bog between eskers (sample)", (4000, 7800), (8400, 9800), "wade pools, walk the firm ground")]
    S, Tt, P = "s", "t", "p"
    ops = [
        dict(op=1, name="Over the Top", start=(8000, 1200), rows=[
            ("First Trench Belt West", "outpost", P, 4.5, 4.4, "Platoon trench system: dugouts, saps, MG posts", "t"),
            ("First Trench Belt East", "outpost", P, 11.5, 4.6, "Second half of the line; a bypass option", "t"),
            ("Pillbox Knoll", "outpost", Tt, 8.0, 4.0, "Concrete knoll that sees both belts", ""),
            ("Wire Mill Ruin", "other", S, 6.3, 3.4, "Ruin with cover in no man's land", ""),
            ("Dugout Galleries", "tunnel", Tt, 9.6, 4.9, "Covered galleries: tight, dark, into a command room", "it"),
            ("Droid Gun Line", "air_prep", Tt, 8.8, 5.8, "Guns are targets only (Zeus fires); pilots soften them", ""),
            ("Esker Observation Post", "outpost", S, 3.2, 5.2, "Sees the whole first belt", ""),
            ("Rail Halt", "other", Tt, 5.6, 2.8, "Railhead for Republic armour", "v"),
            ("Crater Field Snipers", "outpost", S, 13.0, 3.6, "Snipers in the craters", ""),
            ("Field Hospital Ruin", "other", S, 10.6, 3.2, "Rescue captured clones", "i"),
            ("AA Pit", "AA", Tt, 7.0, 5.4, "Grounds LAATs over the first belt", ""),
            ("Observation Blimp Tether", "air_only", S, 12.5, 6.2, "Spots for the gun line", ""),
        ]),
        dict(op=2, name="The Drain", start=(8000, 4300), rows=[
            ("Drain Bridge", "bridge", Tt, 7.6, 7.0, "Only tank crossing of the Drain", "v"),
            ("Drain Lock and Pumphouse", "other", Tt, 10.6, 7.2, "Powers the second belt's shields", "w"),
            ("Peat Cutters' Village", "town", P, 5.0, 7.6, "Sci-fi village on piles; FOB site for op 3", "i"),
            ("Barge Quay", "other", S, 12.6, 7.1, "CIS supply barges", "w"),
            ("Second Trench Belt", "outpost", P, 9.0, 8.6, "Main line north of the Drain", "t"),
            ("Sap-head Bunkers", "outpost", S, 6.6, 8.2, "Forward bunkers", ""),
            ("Duckboard Maze", "tunnel", Tt, 11.4, 8.2, "Covered trench maze into a dugout hall", "it"),
            ("Esker Battery", "battery", Tt, 3.6, 8.4, "Guns on the esker hit the village and bridge", ""),
            ("Fuel Dump", "air_prep", Tt, 13.6, 8.4, "Fuels the walker park", ""),
            ("Kettle Lake Outpost", "outpost", S, 2.2, 7.2, "Covers the west flank", ""),
            ("Signal Tower", "other", S, 8.0, 6.4, "Intel: second belt layout", ""),
            ("AA Halftrack Park", "AA", Tt, 14.0, 6.0, "Mobile AA", ""),
        ]),
        dict(op=3, name="Esker Road", start=(5000, 7600), rows=[
            ("Esker Fort North", "outpost", P, 3.0, 11.4, "Fort on the esker crest", ""),
            ("Gravel Pit Bunkers", "outpost", Tt, 2.0, 10.0, "Pits as cover", ""),
            ("Esker Rail Cutting", "other", Tt, 4.4, 10.6, "Rail cut through the esker; vehicle way", "v"),
            ("Moss Chapel Ruin", "other", S, 5.8, 10.2, "Ruin; intel cache", ""),
            ("Bog Pool Pillboxes", "outpost", S, 6.6, 11.6, "Pillboxes between pools", ""),
            ("Esker Dugouts", "tunnel", Tt, 3.4, 12.6, "Tunnel shells in the esker side", "it"),
            ("West AA Battery", "AA", Tt, 1.6, 12.8, "Covers the west", ""),
            ("Walker Park", "air_prep", Tt, 5.0, 12.4, "Walkers would counterattack the eskers", ""),
            ("Hamlet of Stakes", "town", Tt, 1.8, 8.6, "Pile village", "i"),
            ("Kettle Ferry", "other", S, 4.6, 9.0, "Ferry across the kettle lake", "w"),
            ("Esker Beacon", "air_only", S, 2.6, 14.6, "Guides CIS reinforcements", ""),
        ]),
        dict(op=4, name="The Cauldron", start=(9000, 8800), rows=[
            ("Cauldron Refinery", "facility", P, 11.0, 11.0, "Fuel refinery on stilts in the flooded crater", "wit"),
            ("Rim Bunker Ring", "outpost", P, 10.4, 10.6, "Bunkers round the rim", ""),
            ("Terrace Stair Batteries", "battery", Tt, 11.5, 11.5, "Guns on the inner terraces", ""),
            ("Rim Tunnels", "tunnel", P, 11.5, 10.5, "Shells in the rim spoil", "it"),
            ("Spoil Heap Snipers", "outpost", S, 12.4, 11.6, "High spoil heaps", ""),
            ("Pipeline Pumping Station", "other", Tt, 9.6, 12.0, "Pipes fuel north to the moraine", ""),
            ("Tank Laager", "outpost", Tt, 12.8, 10.0, "CIS tanks", "v"),
            ("Refinery Flare Stacks", "air_prep", Tt, 11.0, 11.3, "Tall stacks: pilots soften them", "w"),
            ("Ruined Mining Town", "town", Tt, 13.6, 11.2, "Town on the crater apron", "i"),
            ("Cauldron AA Pits", "AA", S, 10.2, 11.6, "Covers the crater", ""),
            ("Gas Holder", "air_only", S, 8.8, 10.6, "Feeds the refinery", ""),
        ]),
        dict(op=5, name="Third Line", start=(10500, 10500), rows=[
            ("Third Belt West", "outpost", P, 6.4, 13.4, "Last trench line, west half", "t"),
            ("Third Belt East", "outpost", P, 13.0, 13.2, "Last trench line, east half", "t"),
            ("Command Dugout", "tunnel", P, 9.6, 13.6, "Deep dugout shell with map rooms", "it"),
            ("Rail Junction", "other", Tt, 11.4, 13.0, "Rail into the moraine", "v"),
            ("Mud Fort", "outpost", Tt, 8.0, 12.6, "Earth fort", ""),
            ("Bog Bridge", "bridge", S, 14.4, 12.4, "Vehicle bridge on the east", "v"),
            ("Field Gun Battery", "battery", Tt, 9.0, 14.4, "Guns are targets only", ""),
            ("Droid Reserve Camp", "air_prep", Tt, 12.0, 14.4, "Reserve for counterattacks", ""),
            ("Signal Tower North", "other", S, 7.2, 14.6, "Intel for op 6", ""),
            ("Wrecked Walker Strongpoint", "outpost", S, 10.6, 12.4, "Dead walker as a bunker", ""),
            ("AA Belt", "AA", Tt, 14.2, 14.0, "Covers the moraine approach", ""),
        ]),
        dict(op=6, name="Moraine Citadel", start=(9600, 13600), rows=[
            ("Moraine Citadel", "facility", P, 8.4, 15.4, "CIS HQ built into the moraine", "it"),
            ("Citadel Gate Wall", "facility", Tt, 8.0, 14.9, "Wall and gate (starts closed)", "v"),
            ("Hangar Bunkers", "facility", Tt, 10.6, 15.3, "Gunship bunkers", "i"),
            ("Moraine Battery", "battery", Tt, 6.4, 15.3, "Guns on the moraine", ""),
            ("Moraine Gallery Maze", "tunnel", P, 9.4, 15.6, "Maze between the halls", "it"),
            ("Supply Railhead", "other", Tt, 12.0, 15.2, "Rail end", "v"),
            ("Comms Mast", "other", S, 7.2, 15.7, "Calls the fleet", ""),
            ("Fuel Tanks", "air_prep", Tt, 13.4, 15.4, "Pilots soften them", ""),
            ("Water Tower Snipers", "outpost", S, 5.2, 15.2, "Overwatch", ""),
            ("Prisoner Pens", "other", Tt, 11.2, 14.8, "Rescue clones", ""),
            ("Orbital Uplink Dish", "air_only", S, 14.6, 15.6, "Air-only kill", ""),
        ]),
    ]
    return dict(H=H, labels=labels, islands=[], crossings=crossings, ops=ops, lines=lines, min_h=0.2)


# =================================================================== B
def swamp_B():
    """The Glow: Felucia-style sawgrass river of grass with fungal hammocks."""
    H = 0.3 + 0.12 * T.fbm(401, 1500, 3) + 0.06 * T.fbm(402, 200, 3)
    main = T.chaikin([(11500, 16000), (10800, 13500), (9200, 11500), (8100, 8600), (8300, 6000), (7400, 3500), (7800, 0)])
    branches = [T.chaikin([(4300, 15000), (5600, 12400), (7600, 9200)]),
                T.chaikin([(14500, 16000), (12600, 12200), (10600, 9000), (9000, 7000)]),
                T.chaikin([(8200, 5200), (6800, 2600), (5200, 0)]),
                T.chaikin([(8400, 4500), (11200, 2400), (13800, 0)])]
    T.carve_line(H, main, 1300, 0.55, soft=500)
    for b in branches:
        T.carve_line(H, b, 650, 0.45, soft=350)
    T.carve_line(H, [p for p in main], 40, 1.8, soft=20)        # deeper boat channel in the main slough
    # Western limestone ridge (giant fungus forest) and northern rise (citadel)
    ridge = T.chaikin([(2600, 1500), (3100, 5200), (2900, 9000), (3400, 12000), (3900, 14600)])
    dr = T.dist_to_polyline(ridge)
    _bump(H, 9 * T.smoothstep(1100, 150, dr) * (1 + 0.3 * T.fbm(404, 600, 3)))
    dn = np.hypot((X - 8800) / 1.6, Y - 16200)
    _bump(H, 20 * T.smoothstep(2000, 500, dn) * (1 + 0.2 * T.fbm(405, 500, 3)))
    # Hammocks: teardrop tree islands, tails downstream
    _teardrops(H, 406, 90, (4200, 1500, 15200, 14200), (60, 260), (120, 520), (1.4, 3.2))
    # Cenotes: small deep sinkholes (boats can't reach; swimmers can)
    rng = np.random.default_rng(407)
    for _ in range(14):
        T.set_blob(H, rng.uniform(1500, 14500), rng.uniform(1500, 14000), rng.uniform(40, 90), -8, soft=20, seed=0, mode="min")
    # Southern lake (open water; hover/boat staging)
    T.set_blob(H, 7200, 700, 1700, -1.6, soft=500, seed=408, mode="min")
    # Canal road on a levee, canal beside it (east side)
    canal_road = T.chaikin([(13800, 0), (13900, 4000), (13600, 8000), (13900, 12000), (14200, 16000)])
    T.raise_line(H, canal_road, 40, 2.6, soft=40)
    T.carve_line(H, T.offset_line(canal_road, -120), 50, 2.0, soft=20)
    ridge_road = T.offset_line(ridge, 150)
    titan = [(6700, 8500), (9500, 8800)]
    lines = [(canal_road, ROAD), (ridge_road, ROAD), (T.chaikin([(3600, 13200), (6000, 14400), (8800, 14800)]), ROAD),
             (titan, dict(color="#b5179e", lw=5, ls="-", label="the Felled Titan (set piece)")),
             (T.chaikin([(4800, 3300), (6200, 3000), (7600, 3400)]), BOARD),
             (T.chaikin([(9700, 9000), (10800, 10600), (11000, 11800)]), BOARD)]
    labels = [("spore ridge", 1500, 9000), ("main slough (the Glow)", 9800, 5200), ("south lake", 9300, 300),
              ("canal road", 15000, 6200), ("north rise", 11600, 15600), ("hammocks", 12000, 3000)]
    crossings = [("Main slough at the Titan", (6600, 8500), (9600, 8800), "Titan bridge; or wade 0.4-0.6 m; boat channel 1.8 m"),
                 ("Main slough, south", (6200, 4200), (9800, 4200), "wade; hover; boat channel"),
                 ("East branch slough", (9800, 10600), (12200, 10600), "wade; hover"),
                 ("South lake", (6000, 1200), (8800, 1200), "boat / hover only"),
                 ("Canal beside canal road", (13500, 6000), (14100, 6000), "bridges; swim")]
    S, Tt, P = "s", "t", "p"
    ops = [
        dict(op=1, name="Edge of the Grass", start=(8000, 600), rows=[
            ("Lakeshore Hover Pens", "other", Tt, 6.6, 2.0, "Droid hovers; take them to own the lake", "w"),
            ("Sawgrass Pillboxes", "outpost", S, 9.0, 2.8, "Pillboxes in open grass", "w"),
            ("Heron Hammock Fort", "outpost", Tt, 7.6, 3.4, "Fort on a big hammock", ""),
            ("Spore Sampler Station", "other", S, 10.6, 3.0, "Intel: what the labs make", ""),
            ("Gladeside Village", "town", P, 4.6, 3.2, "Sci-fi stilt village; FOB for op 3", "i"),
            ("Cenote Rim Shells", "tunnel", Tt, 5.8, 4.2, "Tunnel shells round a sinkhole", "it"),
            ("Hammock Gun Nest", "battery", Tt, 11.8, 4.2, "Guns hit the lake landing", ""),
            ("AA Hammock", "AA", Tt, 9.6, 4.8, "Grounds LAATs over the grass", ""),
            ("Droid Hover Park", "air_prep", Tt, 12.8, 2.6, "Pilots soften the hovers", ""),
            ("Canal Road Checkpoint", "outpost", S, 13.8, 3.8, "Gate on the canal road (starts closed)", "v"),
            ("Spore Balloon Tether", "air_only", S, 8.6, 5.6, "Spreads spores over the grass", ""),
        ]),
        dict(op=2, name="Canal Road", start=(12800, 3000), rows=[
            ("Canal Lock Fort", "outpost", P, 13.8, 6.4, "Fort on the lock: the vehicle route north", "v"),
            ("Pumping Station", "other", Tt, 14.4, 7.6, "Powers the east shields", ""),
            ("Levee Battery", "battery", Tt, 13.4, 8.6, "Guns cover the grass to the west", ""),
            ("Canal Barge Yard", "other", S, 14.2, 5.4, "Barges and boats", "w"),
            ("Levee Bunker Galleries", "tunnel", Tt, 13.9, 9.6, "Shells in the levee", "it"),
            ("Ranger Station", "outpost", Tt, 12.2, 7.2, "Old Republic post to retake", "i"),
            ("Fungus Farm Hammock", "other", S, 11.2, 6.4, "Food and spores", ""),
            ("Fuel Silos", "air_prep", Tt, 14.6, 10.4, "Pilots soften them", ""),
            ("Canal Bridge", "bridge", S, 13.6, 11.2, "Keeps the road open north", "v"),
            ("East Hammock Hamlet", "town", Tt, 11.6, 9.4, "Small hamlet", "i"),
            ("Levee AA Nest", "AA", S, 12.8, 10.6, "Covers the canal", ""),
        ]),
        dict(op=3, name="Spore Ridge", start=(4600, 3400), rows=[
            ("Ridge Road Fort", "outpost", P, 3.0, 6.4, "Fort on the ridge road", "v"),
            ("Giant Cap Grove", "outpost", S, 2.4, 7.8, "Snipers under giant caps", ""),
            ("Spore Works South Lab", "facility", P, 3.4, 8.8, "Bio-lab, multi-level", "i"),
            ("Ridge Gun Battery", "battery", Tt, 3.6, 10.0, "Guns cover the main slough", ""),
            ("Root Cellar Maze", "tunnel", Tt, 2.6, 9.4, "Maze in the root mass", "it"),
            ("Cenote Pump House", "other", S, 4.6, 7.2, "Water for the labs", ""),
            ("Ridge AA", "AA", Tt, 2.0, 10.8, "Covers the west", ""),
            ("Spore Silos", "air_prep", Tt, 4.0, 11.2, "Pilots soften them", ""),
            ("Fungal Hamlet", "town", Tt, 1.6, 5.6, "Hamlet in the caps", "i"),
            ("Glade Comms", "other", S, 5.0, 9.8, "Intel for the Titan", ""),
            ("Spore Venting Tower", "air_only", S, 1.2, 12.4, "Spore plume over the ridge", ""),
        ]),
        dict(op=4, name="The Felled Titan", start=(6000, 6000), rows=[
            ("Titan West Root Fort", "outpost", P, 6.4, 8.4, "Fort in the root plate", ""),
            ("Titan Hollow Trunk", "facility", P, 8.0, 8.6, "Lab inside the hollow trunk: halls and tight bores", "wit"),
            ("Titan Crown East", "outpost", Tt, 9.6, 8.9, "Fort in the fallen crown", ""),
            ("Slough Hover Pens", "other", Tt, 8.2, 7.2, "Hovers in the slough", "w"),
            ("Channel Pillboxes", "outpost", S, 7.4, 9.6, "Pillboxes on the boat channel", "w"),
            ("Tree Island Battery", "battery", Tt, 10.2, 10.0, "Guns cover the Titan", ""),
            ("Hammock Hamlet North", "town", Tt, 6.8, 10.8, "Hamlet", "i"),
            ("Titan AA Blisters", "air_prep", Tt, 8.6, 9.0, "Pilots soften the blisters", "w"),
            ("Fungus Light Tower", "other", S, 9.0, 7.6, "Comms", ""),
            ("Spore Pond Pumps", "other", S, 10.8, 7.8, "Feed the trunk lab", ""),
            ("Mid-slough AA", "AA", S, 7.0, 7.4, "Covers the slough", ""),
        ]),
        dict(op=5, name="Hammock Archipelago", start=(9600, 9000), rows=[
            ("Big Hammock Fort", "outpost", P, 9.6, 12.2, "Biggest hammock, ringed by grass", ""),
            ("Grass Sea Pillboxes", "outpost", S, 11.0, 11.8, "Pillboxes in the grass", "w"),
            ("Cenote Ring Tunnels", "tunnel", Tt, 8.4, 12.8, "Shells round a sinkhole", "it"),
            ("Hammock Battery", "battery", Tt, 10.8, 13.0, "Guns reach the north rise", ""),
            ("Stilt Supply Depot", "other", Tt, 12.4, 12.4, "Supplies for the citadel", "w"),
            ("Spore Works North Lab", "facility", Tt, 4.2, 13.0, "Second lab on the ridge", "i"),
            ("North Village Ruin", "town", Tt, 7.0, 13.4, "Ruined village", "i"),
            ("Hover Tank Park North", "air_prep", Tt, 12.6, 13.8, "Pilots soften it", ""),
            ("Ridge Comms", "other", S, 3.4, 12.6, "Intel", ""),
            ("AA Hammock North", "AA", Tt, 6.2, 12.0, "Covers the north grass", ""),
            ("Drone Hive Tower", "air_only", S, 14.0, 12.8, "Launches spore drones", ""),
        ]),
        dict(op=6, name="Spore Citadel", start=(9600, 12400), rows=[
            ("Citadel Main Lab", "facility", P, 8.2, 15.0, "The bio-lab heart: end of the run", "it"),
            ("Culture Vat Halls", "facility", P, 9.4, 15.2, "Big halls with staggered vats", "i"),
            ("Citadel Gate Wall", "facility", Tt, 8.6, 14.4, "Gate (starts closed)", "v"),
            ("Root Tunnel Maze", "tunnel", P, 7.2, 15.2, "Maze through giant roots", "it"),
            ("Citadel Battery", "battery", Tt, 10.6, 14.8, "Guns on the rise", ""),
            ("Spore Cannon Silos", "air_prep", Tt, 6.4, 14.6, "Pilots soften them", ""),
            ("Generator Cap", "other", Tt, 11.6, 15.4, "Power for the shield", ""),
            ("Landing Pad Ring", "other", S, 5.4, 15.4, "Escape pads", ""),
            ("Prisoner Pods", "other", Tt, 9.8, 14.2, "Rescue clones", ""),
            ("West Gate Bunkers", "outpost", S, 5.8, 14.2, "Second way in", ""),
            ("AA Cap Nest", "AA", S, 12.4, 14.6, "Covers the rise", ""),
        ]),
    ]
    return dict(H=H, labels=labels, islands=[], crossings=crossings, ops=ops, lines=lines, min_h=0.2)


# =================================================================== C
def swamp_C():
    """River Country: Rodia-style meandering river, levees, oxbows, bluffs."""
    H = 0.35 + 0.3 * T.fbm(501, 1500, 3) + 0.12 * T.fbm(502, 200, 3)
    river = T.chaikin([(0, 3600), (1500, 4400), (2800, 3800), (4000, 4600), (4600, 6000), (5800, 6600), (7000, 6000),
                       (8200, 6600), (8600, 8000), (9800, 8800), (11200, 8400), (12400, 9400), (12800, 10800),
                       (14200, 11400), (16000, 11000)], 4)
    bayou = T.chaikin([(4200, 16000), (4600, 13500), (5200, 12200), (4800, 10000), (5000, 8200), (4700, 6100)], 3)
    # Natural levees: highest at the bank, fading into the backswamp
    dr = T.dist_to_polyline(river)
    _bump(H, np.where(dr < 1400, 0.4 + 2.4 * np.exp(-np.clip(dr - 110, 0, None) / 260), 0))
    db = T.dist_to_polyline(bayou)
    _bump(H, np.where(db < 500, 0.3 + 1.2 * np.exp(-np.clip(db - 45, 0, None) / 120), 0))
    # Backswamp lakes and pools
    rng = np.random.default_rng(503)
    for (x, y, r) in [(2200, 7600, 700), (10600, 4200, 900), (6800, 3200, 600), (11800, 12600, 500), (2600, 10800, 600)]:
        T.set_blob(H, x, y, r, -1.0, soft=300, seed=2, mode="min")
    for _ in range(60):
        T.set_blob(H, rng.uniform(300, 15700), rng.uniform(1800, 12800), rng.uniform(40, 200), -0.8, soft=60, seed=0, mode="min")
    # Oxbow lakes (old cut-off bends)
    def arc(cx, cy, r, a0, a1):
        a = np.radians(np.linspace(a0, a1, 40))
        return [(cx + r * np.cos(t), cy + r * np.sin(t)) for t in a]
    ox1, ox2 = arc(6400, 8700, 800, -40, 220), arc(10700, 6500, 650, 120, 380)
    for ox in (ox1, ox2):
        T.carve_line(H, ox, 170, 2.2, soft=60)
    T.carve_line(H, river, 230, 4.5, soft=60)
    T.carve_line(H, bayou, 90, 1.8, soft=40)
    # Bluffs: north and south terraces; east terrace highland (foundry)
    H += 34 * T.smoothstep(12900, 15300, Y + 500 * T.noise(504, 900))
    H += 16 * T.smoothstep(2000, 200, Y + 400 * T.noise(505, 900))
    dn = np.hypot(X - 14700, Y - 13700)
    _bump(H, 22 * T.smoothstep(2000, 900, dn) * (1 + 0.15 * T.fbm(506, 400, 3)))
    levee_n, levee_s = T.offset_line(river, 190), T.offset_line(river, -190)
    bluff_road = T.chaikin([(0, 13800), (4000, 13500), (8000, 14100), (11000, 13700), (13800, 13000), (16000, 13400)])
    lines = [(levee_n[::2], ROAD), (levee_s[::2], ROAD), (bluff_road, ROAD),
             (T.chaikin([(8500, 7400), (8800, 8300), (9000, 11000), (8700, 13800)]), ROAD),
             (T.chaikin([(6000, 7700), (6200, 8200)]), BOARD)]
    labels = [("the river", 1500, 3300), ("north bluffs", 3000, 15200), ("south bluff", 12500, 700),
              ("oxbow", 6400, 9700), ("oxbow", 10700, 5600), ("bayou", 4000, 11600), ("east terrace", 15000, 15500),
              ("backswamp", 10600, 3300)]
    crossings = [("River at Rodian city (bridge)", (8400, 7400), (9100, 7900), "bridge; boats; swim"),
                 ("River, west reach", (2800, 3200), (2800, 4500), "boat; swim (no ford)"),
                 ("Oxbow lake (refinery)", (5600, 8700), (7200, 8700), "piers; boat"),
                 ("Bayou", (4300, 10000), (5300, 10000), "bridge; wade/swim"),
                 ("Backswamp lake east", (9600, 4200), (11600, 4200), "boat/hover; walk round")]
    S, Tt, P = "s", "t", "p"
    ops = [
        dict(op=1, name="River Mouth", start=(500, 5500), rows=[
            ("Levee Fort West", "outpost", P, 1.6, 5.0, "Fort on the levee road", "v"),
            ("Ferry Landing", "other", Tt, 2.8, 4.4, "Ferry across the river", "w"),
            ("Fishing Stilt Village", "town", Tt, 1.2, 2.6, "Rodian stilt village", "wi"),
            ("Bayou Gunboat Pens", "air_prep", Tt, 2.2, 3.2, "Pilots soften the gunboats", "w"),
            ("Levee Battery", "battery", Tt, 4.2, 4.0, "Guns cover the river", ""),
            ("Backswamp Pillboxes", "outpost", S, 3.4, 6.0, "Pillboxes in the backswamp", ""),
            ("South Bluff AA", "AA", Tt, 3.0, 1.4, "Covers the river mouth", ""),
            ("Levee Bunker Galleries", "tunnel", Tt, 4.4, 5.2, "Shells in the levee", "it"),
            ("Pump Tower", "other", S, 0.8, 4.0, "Intel and water", ""),
            ("Cypress Hammock Snipers", "outpost", S, 2.0, 7.0, "Snipers in the trees", ""),
            ("Channel Marker Sensor", "air_only", S, 3.8, 3.0, "Guides CIS boats", "w"),
        ]),
        dict(op=2, name="The Oxbow", start=(4200, 5000), rows=[
            ("Stilt Refinery", "facility", P, 6.4, 8.7, "Fuel refinery rising out of the oxbow lake", "wit"),
            ("Refinery Pier Causeway", "bridge", Tt, 6.0, 8.0, "Pier causeway: the foot way in", "w"),
            ("Oxbow Tank Farm", "other", Tt, 7.2, 8.8, "Fuel tanks", ""),
            ("Levee Road Checkpoint", "outpost", S, 5.4, 6.4, "Gate on the levee road", "v"),
            ("Refinery Flare Stacks", "air_prep", Tt, 6.8, 9.2, "Pilots soften them", "w"),
            ("Pipeline Gun Nests", "battery", S, 5.2, 9.2, "Guns on the pipeline berm", ""),
            ("Neck Village", "town", Tt, 6.6, 7.4, "Village on the oxbow neck", "i"),
            ("Oxbow AA Barge", "AA", Tt, 5.8, 9.1, "AA on the lake", "w"),
            ("Pumphouse Tunnels", "tunnel", Tt, 7.4, 9.6, "Pipe galleries", "it"),
            ("Bayou Boat Dock", "other", S, 4.6, 8.4, "Boats up the bayou", "w"),
            ("Gas Flare Tower", "air_only", S, 7.8, 10.2, "Tall flare", ""),
        ]),
        dict(op=3, name="Rodian River City", start=(6600, 7400), rows=[
            ("City Levee Wall Gate", "facility", P, 8.4, 7.2, "Walled levee gate (starts closed)", "v"),
            ("River City Market Tiers", "town", P, 9.0, 7.6, "Tiered Rodian city on the levee", "i"),
            ("City Bridge", "bridge", Tt, 8.6, 7.9, "Only vehicle bridge over the river", "vw"),
            ("Harbour Quay", "other", Tt, 9.2, 6.8, "River harbour", "w"),
            ("Water Temple Tower", "other", S, 9.6, 7.9, "Tall landmark; intel", ""),
            ("Undercity Canal Shells", "tunnel", P, 8.9, 7.3, "Tight canal corridors into halls", "it"),
            ("Rooftop AA", "AA", Tt, 9.3, 7.2, "Covers the city", ""),
            ("South Bank Battery", "battery", Tt, 7.6, 5.6, "Guns cover the bridge", ""),
            ("Gunboat Moorings", "air_prep", Tt, 8.0, 6.2, "Pilots soften them", "w"),
            ("Council Hall", "other", Tt, 9.5, 7.4, "Rescue Rodian leaders", "i"),
            ("South Levee Pillboxes", "outpost", S, 8.8, 5.8, "Flank cover", ""),
            ("City Spire Relay", "air_only", S, 9.8, 7.0, "Links the city to the foundry", ""),
        ]),
        dict(op=4, name="North Bluffs", start=(9000, 7800), rows=[
            ("Bluff Fort", "outpost", P, 8.2, 13.2, "Fort on the bluff edge", ""),
            ("Bluff Stair Battery", "battery", Tt, 9.6, 13.4, "Guns look over the floodplain", ""),
            ("Bluff Face Galleries", "tunnel", Tt, 7.4, 13.2, "Shells cut into the bluff", "it"),
            ("Bayou Head Village", "town", Tt, 4.6, 13.4, "Village at the bayou head", "i"),
            ("Bluff AA", "AA", Tt, 10.8, 13.6, "Covers the north", ""),
            ("Backswamp Outposts", "outpost", S, 8.6, 10.8, "Outposts on hammocks", ""),
            ("Logging Camp", "other", Tt, 6.0, 11.8, "Timber and boats", ""),
            ("Bluff Gun Park", "air_prep", Tt, 11.6, 14.4, "Pilots soften it", ""),
            ("Comms Relay", "other", S, 9.0, 14.4, "Intel on the foundry", ""),
            ("Bayou Bridge", "bridge", S, 5.0, 12.2, "Road over the bayou", "v"),
            ("Bluff Sensor Mast", "air_only", S, 12.6, 13.6, "Early warning", ""),
        ]),
        dict(op=5, name="Upper Bends", start=(10000, 8600), rows=[
            ("Second Oxbow Fort", "outpost", P, 10.6, 6.5, "Fort inside the second oxbow", ""),
            ("Levee Battery East", "battery", Tt, 11.8, 8.6, "Guns cover the bends", ""),
            ("River Weir", "other", Tt, 12.6, 9.8, "Weir and lock", "w"),
            ("Splay Pillboxes", "outpost", S, 13.4, 8.2, "On the crevasse splay", ""),
            ("Plantation Stilt Town", "town", P, 13.2, 10.8, "Stilt town on the bend", "wi"),
            ("Levee Tunnels East", "tunnel", Tt, 12.2, 10.2, "Shells in the levee", "it"),
            ("Bluff Road Checkpoint", "outpost", S, 12.0, 5.4, "South bluff road", "v"),
            ("Hover Tank Park", "air_prep", Tt, 14.0, 9.6, "Pilots soften it", ""),
            ("Levee AA East", "AA", Tt, 11.2, 7.6, "Covers the bends", ""),
            ("Fuel Barges", "other", S, 14.6, 11.0, "Fuel for the foundry", "w"),
            ("Weir Control Tower", "air_only", S, 13.0, 9.2, "Air-only kill", ""),
        ]),
        dict(op=6, name="Headwater Works", start=(13200, 10800), rows=[
            ("Foundry Terraces", "facility", P, 14.4, 13.6, "Droid foundry on the east terrace: end of run", "it"),
            ("Assembly Halls", "facility", P, 15.0, 12.8, "Big halls with staggered cover", "i"),
            ("Terrace Gate Wall", "facility", Tt, 13.6, 12.6, "Gate (starts closed)", "v"),
            ("Gallery Tunnel Maze", "tunnel", P, 14.0, 14.4, "Maze between the halls", "it"),
            ("Foundry Battery", "battery", Tt, 12.8, 14.2, "Guns cover the bends", ""),
            ("River Intake Pumphouse", "other", Tt, 15.2, 11.4, "Cooling water for the foundry", "w"),
            ("Cooling Stacks", "air_prep", Tt, 15.4, 14.4, "Pilots soften them", ""),
            ("Workers' Stilts", "town", Tt, 12.4, 12.0, "Worker housing", "wi"),
            ("Shield Pylon", "other", S, 13.4, 13.8, "Drops the foundry shield", ""),
            ("AA Terrace Nest", "AA", S, 15.4, 13.6, "Covers the terrace", ""),
            ("Landing Pad", "other", S, 14.8, 15.2, "Escape pad", ""),
        ]),
    ]
    return dict(H=H, labels=labels, islands=[], crossings=crossings, ops=ops, lines=lines, min_h=0.2)


CONCEPTS = {"A": ("The Mire Line", swamp_A), "B": ("The Glow", swamp_B), "C": ("River Country", swamp_C)}
