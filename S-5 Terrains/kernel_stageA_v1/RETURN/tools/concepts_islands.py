"""Islands (1st Company): three PROPOSED concepts.

Each builder returns the sketch height field plus labels, measured crossings
and the op/objective data. Objective rows:
  (name, kind, size s/t/p, x_km, y_km, reason, flags)
flags: i = interior, t = tunnels, w = sits on water (stilts/pier/wreck/deck),
       v = vehicle objective (needs a road or flat approach)
Positions are hand-placed on the sketch, then snapped to the nearest land
cell (unless flagged w). ASSUMED placements.
"""
import numpy as np
import terrain_lib as T
from terrain_lib import X, Y


def _base(seed, floor):
    return floor + 6 * T.fbm(seed, 3000, 3)


def _ring(H, cx, cy, R, width, height, seed, notches=(), notch_h=30.0, notch_w=160.0):
    """Ring ridge (crater rim / karst crown) with notches at given bearings."""
    wx, wy = T.warp(seed, 220, 900)
    d = np.hypot(wx - cx, wy - cy)
    ring = height * T.smoothstep(width, width * 0.25, np.abs(d - R)) * (1 + 0.2 * T.fbm(seed + 5, 500, 4))
    np.maximum(H, np.where(H > 0, ring, H), out=H)
    for b in notches:
        a = np.radians(90 - b)
        p0 = (cx + (R - width) * np.cos(a), cy + (R - width) * np.sin(a))
        p1 = (cx + (R + width) * np.cos(a), cy + (R + width) * np.sin(a))
        T.carve_line(H, [p0, p1], notch_w, -notch_h, soft=80)
    return d


# =================================================================== A
def islands_A():
    H = _base(1, -45.0)
    rng = np.random.default_rng(101)
    # Landing Key: low limestone island, beaches S and E, three knolls
    T.island(H, 3200, 3000, 1600, 1000, 18, ang=15, seed=1, ramp=500)
    for (x, y, r, p) in [(2700, 3300, 180, 70), (3600, 2700, 150, 55), (3900, 3400, 120, 45)]:
        T.tower(H, x, y, r, p, seed=x)
    # Sandbar from Landing Key to Market Isle (wadeable, partly dry)
    T.raise_line(H, [(4400, 3600), (5000, 4600), (5500, 5500), (5900, 6200)], 170, -0.55)
    T.raise_line(H, [(4950, 4500), (5150, 4900)], 60, 0.4)
    # Mushroom Field: shallow lagoon with ~45 karst pillars
    T.set_blob(H, 8000, 3600, 2100, -4.5, soft=500, seed=5, mode="max")
    for k in range(46):
        x, y = rng.uniform(6000, 10200), rng.uniform(1800, 5400)
        T.tower(H, x, y, rng.uniform(40, 170), rng.uniform(18, 95), seed=1000 + k)
    # Market Isle: rolling island, port on the east side
    T.island(H, 6600, 7000, 1300, 900, 35, ang=-20, seed=3, ramp=700)
    # Gun Tower Isle: tall N-S karst ridge, cliffs west, beaches east
    T.island(H, 2600, 8800, 900, 2000, 190, ang=0, seed=4, ramp=420, cliff_dir=270, cliff_ramp=50)
    # Wreck Reef: wide reef flat with a sand motu
    T.set_blob(H, 4600, 12600, 1500, -0.7, soft=350, seed=6, mode="max")
    T.island(H, 4300, 12900, 320, 200, 3, seed=7, ramp=150, shelf_w=60)
    # Twin Hongs: two tower islands with enclosed lagoons (hongs)
    T.island(H, 11200, 5200, 750, 650, 20, seed=8, ramp=300)
    T.tower(H, 11200, 5200, 620, 135, seed=8)
    T.set_blob(H, 11250, 5250, 260, -2.0, soft=60, seed=9, mode="set")
    T.carve_line(H, [(11300, 5300), (11950, 5150)], 45, 1.6, soft=20)
    T.tower(H, 12700, 6500, 520, 110, seed=10)
    T.set_blob(H, 12720, 6520, 170, -1.8, soft=50, seed=11, mode="set")
    # The Crown: big karst massif, ring of towers around a dry doline floor
    T.island(H, 11800, 11200, 3300, 3100, 50, seed=12, ramp=1100, cliff_dir=45, cliff_ramp=80)
    d = _ring(H, 11800, 11800, 1500, 650, 320, seed=13, notches=(260, 190, 95))
    floor = 25 + 3 * T.fbm(14, 300, 3)
    t = T.smoothstep(1150, 950, d)
    H[:] = H * (1 - t) + floor * t
    T.set_blob(H, 11300, 7900, 900, -0.8, soft=250, seed=15, mode="max")    # fringing reef S
    # Stepping-stone cays between Market Isle and the Crown
    T.island(H, 8800, 8200, 420, 300, 12, seed=16, ramp=200)
    T.island(H, 9600, 9300, 300, 260, 8, seed=17, ramp=150)
    # North karst field (sight-line breakers)
    for k in range(26):
        x, y = rng.uniform(6200, 9600), rng.uniform(12600, 15600)
        T.tower(H, x, y, rng.uniform(60, 220), rng.uniform(40, 170), seed=2000 + k)
    # Outer east skerries
    for k in range(10):
        T.tower(H, rng.uniform(14200, 15600), rng.uniform(1500, 9000), rng.uniform(50, 140), rng.uniform(20, 70), seed=3000 + k)

    labels = [("Landing Key", 3200, 2500), ("Mushroom Field", 8100, 1500), ("Market Isle", 6400, 8100),
              ("Gun Tower Isle", 1500, 11200), ("Wreck Reef", 4600, 14300), ("Twin Hongs", 12000, 4200),
              ("The Crown", 13400, 14900), ("doline floor", 11800, 12100), ("north karst field", 7900, 15700),
              ("sandbar", 4300, 5000), ("cays", 9400, 8000)]
    islands = [("Landing Key", 3200, 3000), ("Market Isle", 6600, 7000), ("Gun Tower Isle", 2600, 8800),
               ("The Crown", 13000, 11800), ("Twin Hong W", 11200, 4700), ("Twin Hong E", 12700, 6200),
               ("Wreck Reef motu", 4300, 12900), ("Cay 1", 8800, 8200)]
    crossings = [
        ("Landing Key -> Market Isle (sandbar)", (4400, 3600), (5900, 6300), "wade the sandbar; boats either side"),
        ("Landing Key -> Gun Tower Isle", (2900, 4000), (2700, 6900), "boat / air"),
        ("Market Isle -> Gun Tower Isle", (5300, 7300), (3500, 8300), "boat / air"),
        ("Market Isle -> Twin Hongs", (7800, 6600), (10500, 5600), "boat / air"),
        ("Market Isle -> Crown via cays", (7800, 7600), (9900, 9600), "boat hop via cays / air"),
        ("Twin Hongs -> Crown south reef", (11500, 5900), (11500, 9300), "boat, then wade the reef flat"),
        ("Gun Tower Isle -> Wreck Reef", (2800, 10800), (4300, 11800), "boat, then wade the reef"),
    ]
    S, Tt, P = "s", "t", "p"
    ops = [
        dict(op=1, name="Beachhead", start=(1200, 1000), rows=[
            ("Reef Battery", "battery", Tt, 3.9, 2.4, "Its guns cover the south beach the platoon lands on", ""),
            ("Dune Line", "outpost", S, 2.6, 2.3, "First foothold; dunes and wrecks give beach cover", ""),
            ("Knoll Gun Nest", "battery", S, 2.7, 3.3, "High ground over both beaches", ""),
            ("Key Signal Mast", "other", S, 3.6, 2.8, "Intel: shows the Lagoon garrison layout for op 2", ""),
            ("Landing Key Village", "town", P, 3.3, 3.4, "Becomes the FOB and respawn for op 2", "i"),
            ("Burrow Knoll", "tunnel", Tt, 3.9, 3.4, "Tunnel shells link the knoll guns", "it"),
            ("Shore AA Pair", "AA", Tt, 2.2, 3.1, "Grounds LAATs on the west approach", ""),
            ("Tidal Fuel Depot", "other", S, 4.4, 3.0, "Fuel for droid gunboats in the lagoon", ""),
            ("Pillar Picket Towers", "outpost", Tt, 6.4, 2.4, "Spotters on pillars watch the whole lagoon", ""),
            ("Lagoon Gunboat Pens", "air_prep", Tt, 7.2, 2.8, "Gunboats would hit the beach; pilots soften them", "w"),
            ("Sandbar Bunker", "outpost", S, 4.8, 4.1, "Holds the wading route north", "w"),
            ("Offshore Sensor Platform", "air_only", S, 5.4, 1.4, "Blinds CIS to Navy movements for the run", "w"),
        ]),
        dict(op=2, name="The Lagoon", start=(3500, 3300), rows=[
            ("Sandbar Fort", "outpost", Tt, 5.5, 5.2, "Guards the wading route to Market Isle", "w"),
            ("Pillar Stilt Town", "town", P, 7.8, 3.7, "Lagoon town on stilts between pillars", "wi"),
            ("Pillar-top Gun Nests", "battery", S, 8.6, 4.4, "Guns on pillars reach Market harbour", ""),
            ("Great Pillar Hollow", "tunnel", Tt, 7.0, 4.6, "Tunnel shells through the biggest pillar", "it"),
            ("Drone Relay Pillar", "other", S, 9.4, 3.1, "Intel: maps CIS boat routes for op 4", ""),
            ("Floating Fuel Barge", "air_prep", Tt, 8.3, 2.6, "Feeds the lagoon gunboats", "w"),
            ("Market South Beach Line", "outpost", Tt, 6.4, 6.3, "Beach defences on Market Isle", ""),
            ("Harbour Mole Battery", "battery", Tt, 7.6, 7.2, "Covers the Market harbour entry", ""),
            ("Market Port", "town", P, 7.2, 6.9, "FOB and boat dock for ops 3 and 4", "iv"),
            ("Mine-laying Station", "other", S, 9.8, 4.3, "Take it and boats can use the lagoon safely", "w"),
            ("Cliff Shrine Lookout", "outpost", S, 5.8, 7.4, "Looks west over the gun island", ""),
            ("Pillar Sensor Spire", "air_only", S, 9.0, 5.2, "Spots LAAT traffic for the Crown", ""),
        ]),
        dict(op=3, name="Western Guns", start=(6200, 7600), rows=[
            ("East Beach Bunkers", "outpost", Tt, 3.2, 8.0, "Only beaches on the island; cover for the landing", ""),
            ("Ridge AA North", "AA", P, 2.5, 9.6, "Grounds air over the west; opens air lanes north", ""),
            ("Ridge AA South", "AA", Tt, 2.6, 7.9, "Covers Market Port from the air", ""),
            ("Cliff Gallery", "tunnel", Tt, 2.3, 8.7, "Galleries cut into the west cliff", "it"),
            ("Summit Signal Station", "other", S, 2.6, 8.8, "Intel: Crown traffic logs reveal the facility", ""),
            ("Fishing Hamlet", "town", Tt, 3.3, 9.3, "Civilians and a droid garrison", "i"),
            ("Ridge Landing Pad", "outpost", Tt, 3.1, 10.3, "CIS shuttles resupply the guns here", ""),
            ("Frigate Hulk", "outpost", P, 4.6, 12.6, "Salvaged hull guns cover the north channel", "wi"),
            ("Reef Motu Camp", "outpost", S, 4.3, 12.9, "Salvage crew camp", ""),
            ("Ridge Radar", "air_prep", S, 2.4, 10.4, "Cues the AA; pilots soften it first", ""),
            ("Wreck Beacon Tower", "air_only", S, 5.6, 12.0, "Guides CIS boats through the reef", "w"),
            ("Gun Isle Ammo Store", "other", S, 2.9, 7.3, "Destroy it and the ridge guns go quiet", ""),
        ]),
        dict(op=4, name="Hongs and Crown Shore", start=(7200, 6900), rows=[
            ("West Hong Gate Fort", "outpost", Tt, 10.7, 5.0, "Blocks the notch into the hong", ""),
            ("Hong Boat Pens", "other", Tt, 11.25, 5.25, "Droid boats hide in the hong", "w"),
            ("Hong Tower Battery", "battery", Tt, 11.5, 5.6, "Guns cover the Market-Crown water", ""),
            ("East Hong Pillar Tunnels", "tunnel", Tt, 12.7, 6.5, "Tunnel shells round the east hong", "it"),
            ("Reef Power Pylons", "other", S, 12.0, 7.3, "Cables run to the Crown: proves the facility", "w"),
            ("Cay Outpost", "outpost", S, 8.8, 8.2, "Stepping stone for boats", ""),
            ("Cay Relay", "other", S, 9.6, 9.3, "Relays Crown comms", ""),
            ("Crown South Beach Defences", "outpost", P, 11.0, 9.3, "The second beach assault; FOB site for op 5", ""),
            ("Reef Obstacle Line", "outpost", S, 11.6, 8.3, "Wading under fire across the reef flat", "w"),
            ("South Shield Projector", "air_prep", Tt, 12.4, 9.6, "Shields the beach guns until hit", ""),
            ("Coastal Research Station", "town", Tt, 10.2, 9.8, "Sci-fi station; intel on the bowl", "i"),
            ("Hong Comms Dish", "air_only", S, 13.0, 6.8, "Links the Crown to the CIS fleet", ""),
        ]),
        dict(op=5, name="The Ring", start=(11000, 9300), rows=[
            ("South Notch Gate", "facility", P, 11.6, 10.3, "Vehicle way into the bowl (gate starts closed)", "v"),
            ("West Notch Wall", "facility", Tt, 10.3, 11.8, "Wall plugs the west notch; second way in", ""),
            ("East Cliff Lift", "other", Tt, 13.3, 11.6, "Lift up the cliff: third way in", "i"),
            ("Ring Battery West", "battery", Tt, 10.4, 12.6, "Rim guns cover the west water", ""),
            ("Ring Battery North", "battery", Tt, 11.8, 13.3, "Rim guns cover the north docks", ""),
            ("Rim AA Nest", "AA", Tt, 12.9, 12.6, "Stops LAAT drops into the bowl", ""),
            ("Ring Gallery Tunnels", "tunnel", P, 12.8, 10.9, "Galleries in the ring: fourth way in", "it"),
            ("Jungle Workers' Town", "town", Tt, 10.3, 10.4, "Facility staff housing", "i"),
            ("North Shore Docks", "other", Tt, 12.0, 14.3, "Supply docks; cut them to starve the bowl", "w"),
            ("Doline Exhaust Stacks", "air_prep", Tt, 11.8, 11.0, "Visible plume; pilots soften the stacks", ""),
            ("Rim Observatory", "other", S, 11.0, 13.1, "Overlooks the whole bowl for op 6", ""),
            ("Ring Sensor Mast", "air_only", S, 13.6, 12.4, "Early warning for the bowl", ""),
        ]),
        dict(op=6, name="Into the Crown", start=(11600, 10100), rows=[
            ("Foundry Main Hall", "facility", P, 11.8, 11.9, "The droid foundry: the run's end goal", "it"),
            ("Assembly Line Hall", "facility", P, 12.4, 11.4, "Multi-level hall built against the cliff", "i"),
            ("Generator Core", "facility", Tt, 11.2, 12.3, "Kills foundry power and shields", "i"),
            ("Cliff-cut Command Tier", "facility", Tt, 12.3, 12.6, "Command and intel; upper levels in the rock", "i"),
            ("Droid Barracks Shells", "other", Tt, 11.3, 11.4, "Reserve garrison; take it to stop counterattacks", "i"),
            ("Service Tunnel Maze", "tunnel", P, 12.0, 10.9, "Tight maze opening into the main hall", "it"),
            ("Ore Lift and Conveyor", "other", S, 11.0, 11.8, "Feeds the foundry", ""),
            ("Coolant Pumphouse", "other", S, 12.7, 12.0, "Overheats the foundry if taken", ""),
            ("Hangar Cut", "facility", Tt, 12.6, 11.0, "Gunship hangar in the cliff", "i"),
            ("Cooling Towers", "air_prep", S, 11.6, 12.8, "Tall target that marks the bowl from the air", ""),
            ("Rim Comms Array", "other", S, 11.4, 13.0, "Calls the fleet; cut it before the end", ""),
        ]),
    ]
    return dict(H=H, labels=labels, islands=islands, crossings=crossings, ops=ops, lines=[], min_h=0.4)


# =================================================================== B
def islands_B():
    H = _base(21, -60.0)
    rng = np.random.default_rng(202)
    # Black Strand: low shield volcano, long black beach on the south
    T.island(H, 2800, 2800, 2000, 1300, 120, ang=20, seed=21, ramp=1100, cliff_dir=330, cliff_ramp=80)
    for pts, w, h in [([(1900, 2500), (1750, 1850), (1580, 1500)], 45, 3.0),      # lava-flow ribs
                      ([(2750, 2450), (2820, 1800), (2680, 1400)], 75, 4.0),
                      ([(3550, 2650), (3720, 2000), (3980, 1650)], 55, 2.5)]:
        T.raise_line(H, pts, w, h, soft=30)
    # Stack Garden: sea stacks and arches on a wave-cut platform
    T.set_blob(H, 5900, 3300, 1100, -2.0, soft=500, seed=22, mode="max")
    for k in range(26):
        T.tower(H, rng.uniform(4800, 7000), rng.uniform(2200, 4400), rng.uniform(30, 95), rng.uniform(25, 75), seed=4000 + k)
    # Airfield Isle: raised marine terrace, flat top
    T.island(H, 9800, 3800, 1900, 1100, 30, ang=-10, seed=23, ramp=1500, cliff_dir=160, cliff_ramp=60)
    T.raise_line(H, [(9000, 3700), (10900, 4100)], 90, 18, soft=60)
    T.carve_line(H, [(9000, 3700), (10900, 4100)], 90, -18, soft=60)
    # Fjord Isle: tall island cut by a sound
    T.island(H, 5000, 7600, 2000, 1700, 420, seed=24, ramp=900, cliff_dir=250, cliff_ramp=70)
    T.carve_line(H, [(7000, 7000), (6200, 7150), (5600, 7450), (4800, 7900)], 230, 20, soft=90)
    # Pumice Shoals: tephra bar, wadeable, between Fjord Isle and the Caldera
    T.set_blob(H, 7600, 9000, 900, -0.8, soft=300, seed=25, mode="max")
    T.raise_line(H, [(6600, 8400), (7600, 9000), (8500, 9600)], 220, -0.6)
    # The Caldera: stratovolcano with a flooded caldera and a SW breach
    T.island(H, 11000, 11000, 3300, 3000, 120, seed=26, ramp=2000)
    wx, wy = T.warp(27, 250, 1200)
    d = np.hypot(wx - 11000, wy - 11200)
    cone = 640 * np.clip(1 - d / 3200, 0, 1) ** 1.25 * (1 + 0.15 * T.fbm(28, 600, 4))
    np.maximum(H, np.where(H > 0, cone, H), out=H)
    t = T.smoothstep(1650, 1450, d)
    H[:] = H * (1 - t) + (-30 + 5 * T.fbm(29, 400, 3)) * t
    terr = T.smoothstep(1750, 1650, d) * (1 - t)                 # shoreline terraces inside rim
    H[:] = H * (1 - terr) + np.minimum(H, 10) * terr
    T.carve_line(H, [(10050, 10250), (9300, 9700), (8500, 9200)], 260, 18, soft=100)
    # Cinder Cone islet and two causeways (old Separatist works)
    T.island(H, 10500, 6000, 500, 450, 90, seed=30, ramp=300)
    T.raise_line(H, [(10100, 4800), (10500, 5550)], 30, 2.0, soft=20)
    T.raise_line(H, [(10600, 6450), (10900, 7950)], 30, 2.0, soft=20)
    # Northern Crags
    T.island(H, 3800, 12800, 1300, 900, 260, seed=31, ramp=320, cliff_dir=0, cliff_ramp=50)
    for k in range(12):
        T.tower(H, rng.uniform(1800, 6000), rng.uniform(11200, 14800), rng.uniform(40, 110), rng.uniform(30, 120), seed=5000 + k)
    for k in range(8):
        T.tower(H, rng.uniform(13800, 15600), rng.uniform(3000, 8000), rng.uniform(60, 160), rng.uniform(30, 90), seed=6000 + k)

    labels = [("Black Strand", 2600, 4600), ("Stack Garden", 6000, 1700), ("Airfield Isle", 10000, 2300),
              ("Fjord Isle", 3600, 9900), ("the sound", 6700, 7500), ("Pumice Shoals", 7400, 10000),
              ("The Caldera", 13900, 14600), ("flooded caldera", 11000, 11300), ("Cinder Cone", 11500, 6000),
              ("Northern Crags", 3800, 14400), ("breach", 8600, 8800)]
    islands = [("Black Strand", 2800, 2800), ("Airfield Isle", 9800, 3800), ("Fjord Isle", 4500, 7200),
               ("The Caldera", 12500, 9000), ("Cinder Cone", 10500, 6000), ("Northern Crags", 3800, 12800)]
    crossings = [
        ("Black Strand -> Stack Garden", (4300, 2800), (5000, 3000), "wade/boat over the wave-cut platform"),
        ("Black Strand -> Fjord Isle", (3300, 4100), (4300, 6000), "boat / air"),
        ("Stack Garden -> Airfield Isle", (7000, 3300), (8100, 3600), "boat / air"),
        ("Airfield -> Cinder Cone (causeway)", (10100, 4800), (10500, 5550), "causeway: foot and vehicles"),
        ("Cinder Cone -> Caldera (causeway)", (10600, 6450), (10900, 7950), "causeway: foot and vehicles"),
        ("Fjord Isle -> Caldera (Pumice Shoals)", (6600, 8400), (8500, 9600), "wade the tephra bar"),
        ("Fjord Isle -> Northern Crags", (4200, 9400), (3900, 11800), "boat / air"),
        ("Breach channel (into caldera)", (8500, 9200), (10050, 10250), "boats only; dam gate"),
    ]
    S, Tt, P = "s", "t", "p"
    ops = [
        dict(op=1, name="Black Strand", start=(2500, 600), rows=[
            ("Strand Bunker Line", "outpost", P, 2.8, 1.8, "Covers the whole black beach", ""),
            ("Lava Rib Gun Pits", "battery", Tt, 2.0, 1.9, "Pits in the lava ribs enfilade the beach", ""),
            ("Lighthouse Station", "other", S, 4.3, 2.2, "Spots for the Stack Garden guns", ""),
            ("Ash Village", "town", Tt, 3.0, 2.8, "FOB site for op 2", "i"),
            ("Lava Tube Shelters", "tunnel", Tt, 2.4, 3.3, "Shells in the lava ridge, tight and dark", "it"),
            ("Summit Post", "outpost", S, 2.8, 3.4, "Sees the airfield; intel for op 2", ""),
            ("Cliff AA North", "AA", Tt, 2.2, 3.9, "Grounds air on the north cliffs", ""),
            ("Geothermal Plant", "other", Tt, 3.6, 3.3, "Powers the island shields", "i"),
            ("Droid Artillery Park", "air_prep", Tt, 1.6, 2.7, "Guns are targets only (Zeus fires); pilots soften them", ""),
            ("Sniper Stacks", "outpost", S, 5.2, 2.8, "Stacks overlook the beach flank", ""),
            ("Offshore Picket Platform", "air_only", S, 1.0, 4.2, "Warns the airfield of the fleet", "w"),
        ]),
        dict(op=2, name="Stacks and Airfield", start=(3000, 2800), rows=[
            ("Arch Gate Fort", "outpost", Tt, 5.9, 3.4, "Fort under a natural arch", ""),
            ("Stack-top Gun Nests", "battery", S, 6.5, 2.6, "Guns on stacks cover the boat water", ""),
            ("Stack Boat Pens", "other", Tt, 6.2, 3.9, "Droid boats; take them to free the water", "w"),
            ("Airfield Runway", "facility", P, 9.8, 3.9, "CIS fighters base here; take it and air arrives faster", "v"),
            ("Hangar Row", "facility", Tt, 10.4, 4.1, "Big halls with staggered cover", "i"),
            ("AA Battery West", "AA", Tt, 8.5, 3.6, "Covers the west approach", ""),
            ("AA Battery East", "AA", Tt, 11.2, 3.6, "Covers the causeway", ""),
            ("Fuel Farm", "other", S, 9.3, 3.3, "Fighters stay grounded without it", ""),
            ("Control Tower", "other", S, 10.0, 4.4, "Intel: CIS flight plans", "i"),
            ("Revetment Tunnels", "tunnel", Tt, 10.9, 3.2, "Covered ways between revetments", "it"),
            ("Parked Droid Fighters", "air_prep", Tt, 9.6, 3.5, "Pilots soften the flight line", ""),
            ("Workers' Camp", "town", S, 8.9, 4.5, "Small sci-fi camp", "i"),
        ]),
        dict(op=3, name="Fjord Fortress", start=(3200, 4200), rows=[
            ("South Notch Wall", "facility", P, 4.6, 6.0, "Wall plugs a cliff notch: the gate into the island", ""),
            ("West Notch Wall", "facility", Tt, 3.2, 7.6, "Second walled notch: another way in", ""),
            ("Sound Mouth Batteries", "battery", Tt, 6.6, 7.0, "Guns close the sound to boats", ""),
            ("Sound Boom Gate", "other", Tt, 6.2, 7.2, "Boom blocks boats until opened", "w"),
            ("Sound Head Town", "town", P, 4.8, 7.9, "Town at the head of the sound", "i"),
            ("Cliff Galleries", "tunnel", P, 5.6, 8.4, "Tunnel shells in the cliff", "it"),
            ("Summit AA", "AA", Tt, 5.0, 7.4, "Highest AA on the map", ""),
            ("Terrace Farms", "outpost", S, 4.0, 8.6, "Stepped fields, low walls for cover", ""),
            ("Cable Car Station", "other", S, 5.3, 6.6, "Fast way up the cliff once taken", ""),
            ("Sound Rim Guns", "air_prep", Tt, 5.9, 6.6, "Pilots soften the rim guns", ""),
            ("North Cove Landing", "outpost", S, 5.6, 9.3, "Back door from the north", ""),
            ("Peak Relay Dish", "air_only", S, 4.4, 7.0, "Links the fortress to the caldera", ""),
        ]),
        dict(op=4, name="Shoals and Crags", start=(4800, 8000), rows=[
            ("Shoal Pillboxes", "outpost", Tt, 7.6, 9.0, "Wading under fire across the shoals", "w"),
            ("Shoal Wreck Fort", "outpost", Tt, 7.0, 8.6, "Wrecked freighter on the bar", "w"),
            ("Crag Research Station", "town", P, 3.8, 12.8, "Sci-fi station on a crag", "i"),
            ("Crag Stair Fort", "outpost", Tt, 4.4, 13.4, "Fort on the cliff stair", ""),
            ("Crag Cave Shells", "tunnel", Tt, 3.4, 12.4, "Tight tunnel shells", "it"),
            ("Crag AA", "AA", S, 4.6, 12.2, "Covers the northern water", ""),
            ("Caldera West Outpost", "outpost", Tt, 8.6, 11.4, "Foothold on the caldera's west flank", ""),
            ("Breach Watch Battery", "battery", Tt, 8.9, 9.7, "Guns cover the breach channel", ""),
            ("Steam Vent Bores", "other", S, 8.2, 10.8, "Heat plumes hide CIS movement", ""),
            ("Flank Gun Line", "air_prep", Tt, 9.0, 12.4, "Pilots soften the flank guns", ""),
            ("Skerry Beacon", "air_only", S, 2.0, 11.4, "Guides CIS shipping", "w"),
        ]),
        dict(op=5, name="Cinder Road and Breach", start=(10000, 4600), rows=[
            ("Cinder Cone Fort", "outpost", P, 10.5, 6.0, "Fort on the cone between the causeways", ""),
            ("Causeway Checkpoint", "outpost", S, 10.3, 5.2, "Gate on the causeway (starts closed)", "v"),
            ("Causeway Bridge Gun", "battery", Tt, 10.7, 7.2, "Covers the second causeway", "v"),
            ("Caldera Foot Town", "town", Tt, 11.0, 8.3, "Town at the end of the causeway", "i"),
            ("Breach Dam Gate", "facility", P, 9.6, 10.0, "Dam closes the caldera to boats", "w"),
            ("Dam Turbine Hall", "facility", Tt, 9.4, 9.6, "Interior halls in the dam", "wi"),
            ("South Flank Tunnels", "tunnel", Tt, 11.8, 8.8, "Shells up the south flank", "it"),
            ("Rim AA South", "AA", Tt, 11.4, 9.4, "Stops drops onto the rim", ""),
            ("East Slope Comms", "other", S, 13.2, 10.6, "Intel on the shipyard", ""),
            ("Rim Shield Pylons", "air_prep", Tt, 12.4, 9.6, "Shields the yard until hit", ""),
            ("Lava Quarry", "outpost", S, 12.6, 8.4, "Quarry pits for cover", ""),
            ("Steam Plume Sensor", "air_only", S, 13.8, 12.0, "Early warning on the east", ""),
        ]),
        dict(op=6, name="Inside the Caldera", start=(11200, 9600), rows=[
            ("Dry Dock Alpha", "facility", P, 10.2, 12.4, "Frigate in dry dock: the run's end goal", "wi"),
            ("Slipway Cranes", "facility", Tt, 11.9, 12.5, "Crane decks over the water", "w"),
            ("Rim Foundry Shell", "facility", P, 12.6, 11.0, "Multi-level foundry built into the rim", "it"),
            ("Shield Generator", "facility", Tt, 11.0, 12.9, "Drops the yard's shield", "i"),
            ("Crater Wall Barracks", "other", Tt, 9.6, 11.3, "Reserve garrison", "i"),
            ("Rim Tunnel Maze", "tunnel", P, 12.3, 10.0, "Tight maze down from the rim", "it"),
            ("Floating Fuel Docks", "other", S, 11.0, 11.0, "Fuel for the yard", "w"),
            ("North Rim Command", "facility", Tt, 11.8, 13.0, "Command and intel", "i"),
            ("Unfinished Frigate Hull", "air_prep", Tt, 10.8, 11.6, "Big air target in the lake", "w"),
            ("Pump House", "other", S, 9.6, 12.2, "Floods the dry dock if taken", ""),
            ("Crane Gantry Bridge", "other", S, 12.6, 12.2, "Walkway between rim and docks", ""),
        ]),
    ]
    return dict(H=H, labels=labels, islands=islands, crossings=crossings, ops=ops, lines=[], min_h=0.4)


# =================================================================== C
def islands_C():
    H = _base(41, -50.0)
    cx, cy, rx, ry = 8000, 7600, 6200, 5600
    wx, wy = T.warp(42, 300, 1500)
    d = np.sqrt(((wx - cx) / rx) ** 2 + ((wy - cy) / ry) ** 2)
    dist_m = (d - 1.0) * min(rx, ry)                      # 0 on the ring line
    ringw = 380 + 120 * T.noise(43, 1500)
    flat = -0.6 + 0.25 * T.fbm(44, 300, 3)
    lagoon = -12 + 4 * T.fbm(45, 1500, 3)
    outside = T.shelf_profile(-(np.abs(dist_m) - ringw).clip(0), 120, 3, 700, -50)
    H[:] = np.where(dist_m < -ringw, np.maximum(lagoon, flat + (dist_m + ringw) / 60.0), H)
    H[:] = np.where(np.abs(dist_m) <= ringw, flat, H)
    H[:] = np.where(dist_m > ringw, np.maximum(outside, H), H)
    # Motus on the ring (sand islets), tangential
    motus = [(0, 1000, 330, 4), (25, 900, 300, 3.5), (55, 700, 260, 3), (-35, 900, 300, 3.5),
             (-60, 1100, 330, 4), (-90, 1300, 380, 4.5), (-120, 900, 300, 3.5), (-150, 700, 260, 3),
             (180, 1300, 380, 4), (160, 800, 280, 3), (140, 700, 250, 3), (105, 600, 240, 3)]
    for k, (ang, a, b, h) in enumerate(motus):
        r = np.radians(ang)
        px, py = cx + rx * np.cos(r), cy + ry * np.sin(r)
        T.island(H, px, py, a, b, h, ang=ang + 90, seed=50 + k, ramp=120, shelf_w=80, floor=-30.0, wstr=150)
    # Passes through the ring (boats only)
    passes = []
    for ang in (-10, -75, 170, 80):
        r = np.radians(ang)
        p0 = (cx + (rx - 900) * np.cos(r), cy + (ry - 900) * np.sin(r))
        p1 = (cx + (rx + 900) * np.cos(r), cy + (ry + 900) * np.sin(r))
        T.carve_line(H, [p0, p1], 240, 10, soft=80)
        passes.append((p0, p1))
    # Patch reefs in the lagoon (stilt towns stand on these)
    for (x, y, r) in [(8400, 5400, 350), (6600, 6200, 300), (9800, 6000, 250), (7400, 7000, 260),
                      (5800, 5000, 220), (10400, 7400, 230), (7700, 4600, 200), (9000, 6600, 180)]:
        T.set_blob(H, x, y, r, -0.9, soft=150, seed=x, mode="max")
    # Makatea: uplifted coral island, cliff rim, mined plateau inside
    s = T.island(H, 6200, 10600, 2600, 1800, 55, ang=10, seed=60, ramp=160, shelf_w=200, floor=-12)
    inner = T.smoothstep(250, 600, s)
    H[:] = np.where(inner > 0, H * (1 - inner) + (30 + 6 * T.fbm(61, 250, 4)) * inner, H)
    # The hull ridge: overgrown wreck berm running from makatea into the lagoon
    T.raise_line(H, [(8300, 10500), (9300, 11050), (10400, 11700)], 240, 42, soft=120)
    T.set_blob(H, 9500, 11000, 900, -0.7, soft=300, seed=62, mode="max")   # debris reef flat

    labels = [("East motus", 15000, 8600), ("South ring", 8000, 600), ("Lagoon", 8000, 5800),
              ("West ring", 900, 11000), ("Makatea", 4800, 12900), ("the hull", 10600, 12300),
              ("passes = boats only", 14200, 14800)]
    islands = [("Makatea + hull", 6200, 10600), ("East motu", cx + rx, cy), ("South motu", cx, cy - ry),
               ("West motu", cx - rx, cy)]
    crossings = [
        ("Reef walk: east motu -> south motu", (13800, 5000), (11200, 2700), "wade the reef flat"),
        ("East pass (along its axis)", passes[0][0], passes[0][1], "boats only"),
        ("South motu -> stilt town (lagoon)", (8000, 2400), (8400, 5200), "boat / hover / air"),
        ("Stilt town -> makatea", (8200, 5600), (6400, 8800), "boat / hover / air"),
        ("West motu -> makatea", (2400, 9000), (3800, 10400), "boat; reef flat then lagoon"),
        ("Makatea -> hull (debris flat)", (8300, 10200), (9600, 11000), "wade the debris flat / walk the berm"),
    ]
    S, Tt, P = "s", "t", "p"
    ops = [
        dict(op=1, name="East Motus", start=(15400, 7000), rows=[
            ("Motu Landing Line", "outpost", Tt, 14.3, 7.4, "Beach and palm-root cover", ""),
            ("Palm Grove Bunkers", "outpost", S, 14.1, 8.2, "Flanks the landing", ""),
            ("East Pass Battery", "battery", P, 14.0, 6.4, "Closes the east pass to the Navy", ""),
            ("Desalination Plant", "other", Tt, 14.2, 7.0, "Fresh water: the FOB needs it", "i"),
            ("Pass Fort", "outpost", Tt, 14.2, 5.8, "Fort on the reef beside the pass", "w"),
            ("Resort Motu", "town", Tt, 13.4, 10.3, "Sci-fi resort, now a droid billet", "i"),
            ("South Motu AA", "AA", Tt, 13.4, 4.9, "Grounds air over the east ring", ""),
            ("Coral Block Tunnels", "tunnel", Tt, 13.9, 8.9, "Shells in a coral-rubble berm", "it"),
            ("Gunboat Mooring", "air_prep", Tt, 12.8, 6.6, "Gunboats would hit the landing", "w"),
            ("Minefield Control", "other", S, 14.7, 5.2, "Clears the mines in the pass", "w"),
            ("Outer Sensor Platform", "air_only", S, 15.3, 9.6, "Blinds CIS to the fleet", "w"),
        ]),
        dict(op=2, name="The Reef Walk", start=(13600, 5000), rows=[
            ("Reef Pillbox Belt", "outpost", Tt, 11.9, 3.4, "Wading under fire, no hard cover but coral heads", "w"),
            ("Tide Wreck Fort", "outpost", Tt, 10.0, 2.4, "Old freighter on the reef", "wi"),
            ("Long Motu Village", "town", P, 8.0, 2.0, "Biggest motu town; FOB for op 3", "i"),
            ("South Pass Batteries", "battery", Tt, 9.2, 2.1, "Close the south pass", ""),
            ("Fish-farm Pens", "other", S, 8.8, 3.3, "Feeds the garrison", "w"),
            ("Motu Comms", "other", S, 6.6, 2.4, "Intel on the lagoon towns", ""),
            ("Coral Quarry Tunnels", "tunnel", Tt, 7.4, 2.2, "Shells in quarry spoil", "it"),
            ("SW Motu AA", "AA", Tt, 4.9, 2.8, "Covers the south lagoon", ""),
            ("Hover-tank Park", "air_prep", Tt, 11.1, 2.8, "Hovers would counterattack along the flat", ""),
            ("Reef Pumping Station", "other", S, 5.8, 2.4, "Powers the south motus", "w"),
            ("Drift Mine Tender", "air_only", S, 8.0, 0.8, "Lays mines in the passes", "w"),
        ]),
        dict(op=3, name="Lagoon Stilts", start=(8000, 2200), rows=[
            ("South Stilt Town", "town", P, 8.4, 5.4, "Big stilt town on a patch reef", "wi"),
            ("Stilt Market Ring", "town", Tt, 6.6, 6.2, "Ring of decks around a market", "wi"),
            ("Patch Reef Gun Platform", "battery", Tt, 9.8, 6.0, "Guns reach the makatea landing", "w"),
            ("Hover Pier", "other", Tt, 7.4, 7.0, "Droid hovers; take it to free the lagoon", "w"),
            ("Coral Garden Pillboxes", "outpost", S, 10.4, 7.4, "Pillboxes on a patch reef", "w"),
            ("Kelp Processing Barge", "other", S, 5.8, 5.0, "Fuel for the hover pier", "w"),
            ("Water Tower Comms", "other", S, 9.0, 6.6, "Intel on the hull", "w"),
            ("Habitat Dome Corridors", "tunnel", Tt, 6.4, 7.6, "Half-flooded dome: corridors open into halls", "wit"),
            ("Lagoon AA Barge", "air_prep", Tt, 8.0, 8.4, "Pilots soften the AA barge", "w"),
            ("Hull Watch Buoys", "other", S, 9.6, 8.6, "Spots for the hull guns", "w"),
            ("Stilt Clinic", "other", Tt, 7.7, 4.6, "Rescue Republic prisoners; they carry intel", "wi"),
        ]),
        dict(op=4, name="West Ring", start=(8200, 5400), rows=[
            ("West Motu Airstrip", "facility", P, 2.0, 7.8, "CIS air base; take it and air arrives faster", "v"),
            ("Hangar Revetments", "outpost", Tt, 2.2, 8.6, "Revetments as cover", ""),
            ("West Pass AA North", "AA", Tt, 2.5, 10.4, "Covers the makatea approach", ""),
            ("West Pass AA South", "AA", Tt, 2.4, 5.2, "Covers the lagoon", ""),
            ("Fuel Bladders", "other", S, 1.8, 7.0, "Fighters stay grounded without it", ""),
            ("Radar Dome", "other", S, 1.9, 9.3, "Cues all CIS AA", ""),
            ("Coral-berm Tunnels", "tunnel", Tt, 2.1, 6.3, "Shells in a storm berm", "it"),
            ("Lagoon Ferry Dock", "other", S, 3.0, 7.6, "Ferry to makatea", "w"),
            ("Droid Fighter Line", "air_prep", Tt, 2.3, 8.1, "Pilots soften the flight line", ""),
            ("Pass Boom Fort", "outpost", Tt, 1.9, 4.4, "Boom closes the west pass", "w"),
            ("Weather Station Spire", "air_only", S, 3.2, 12.6, "CIS forecasts for their boats", "w"),
        ]),
        dict(op=5, name="Makatea Cliffs", start=(2400, 9000), rows=[
            ("West Cliff Notch Wall", "facility", P, 3.7, 10.4, "Wall plugs the only west notch", ""),
            ("South Landing Stair", "outpost", Tt, 6.0, 8.9, "Stair up the south cliff", ""),
            ("Cliff Gun Galleries", "battery", Tt, 4.4, 11.6, "Galleries cover the west water", ""),
            ("Phosphate Railhead", "other", Tt, 5.6, 9.6, "Ore railway; vehicle way onto the plateau", "v"),
            ("Pinnacle Maze", "tunnel", P, 5.4, 10.8, "Mined coral pinnacles plus shells: a maze", "it"),
            ("Miners' Town", "town", P, 6.6, 10.2, "Sci-fi mining town; FOB for op 6", "i"),
            ("Plateau AA", "AA", Tt, 7.3, 11.6, "Covers the hull from the air", ""),
            ("Conveyor Pier", "other", S, 8.4, 9.4, "Loads ore into the hull", "w"),
            ("Ore Crusher Plant", "air_prep", Tt, 6.4, 11.4, "Tall plant; pilots soften it", ""),
            ("North Cliff Lookout", "outpost", S, 6.2, 12.2, "Sees the north side of the hull", ""),
            ("Hull Antenna Mast", "air_only", S, 9.5, 11.7, "Links the hull to the CIS fleet", ""),
        ]),
        dict(op=6, name="The Ship on the Reef", start=(6600, 10200), rows=[
            ("Bow Gate", "facility", P, 8.4, 10.6, "Gate in the bow, on the makatea (starts closed)", "i"),
            ("Keel Hangar", "facility", P, 9.3, 11.1, "Big hangar hall in the hull", "it"),
            ("Midships Foundry Deck", "facility", Tt, 9.8, 11.4, "The droid foundry: the run's end goal", "i"),
            ("Stern Reactor Hall", "facility", Tt, 10.3, 11.7, "Kills foundry power", "i"),
            ("Hull Breach Tunnels", "tunnel", P, 8.9, 10.9, "Tight decks opening into halls", "it"),
            ("Spine Turret Row", "battery", Tt, 9.5, 11.4, "Hull turrets cover the lagoon", ""),
            ("Debris Field Pillboxes", "outpost", S, 9.0, 10.3, "Wading through wreckage", "w"),
            ("Salvage Cranes", "other", S, 10.6, 11.3, "Crane decks on the reef", "w"),
            ("Hull AA Blisters", "air_prep", Tt, 9.9, 11.9, "Pilots soften the blisters", ""),
            ("Command Bridge Tower", "facility", Tt, 8.6, 10.9, "Command and intel, high in the bow", "i"),
            ("Escape Pod Bay", "other", S, 10.8, 11.9, "Stops CIS officers escaping", ""),
        ]),
    ]
    return dict(H=H, labels=labels, islands=islands, crossings=crossings, ops=ops, lines=[], min_h=0.4)


CONCEPTS = {"A": ("Pillar Reach", islands_A), "B": ("Ember Chain", islands_B), "C": ("The Shallows", islands_C)}
