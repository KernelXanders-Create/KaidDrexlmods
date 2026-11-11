# Islands concept C: The Shallows (PROPOSED)

**Pitch:** An atoll world where the whole fight is in the shallows: wading reef flats under fire, stilt towns over the lagoon, and a "ridge" on the raised coral island that turns out to be an overgrown Separatist capital ship, now a droid foundry.

## Setting
**Mon Cala's outer shallows.** The CIS invasion of Mon Cala is canon Clone Wars, so it gives a reason for droids and a Republic ally to rescue. A Pabu-style stilt-town look fits the Mon Cal and Quarren fishing towns. The palette is bright turquoise, white sand, palms and coral pink, the furthest of the three concepts from Blackfen.

## Landform story
1. A ring reef grew round a sunken volcano: the **atoll**.
2. Storms piled coral rubble and sand into **motus** on the ring.
3. Tidal flow keeps **deep passes** open through the ring.
4. In the north-west the reef was **uplifted** into a makatea: a coral island with a cliff rim (about 50-65 m) and a hollow plateau. Miners strip-mined it into a field of **pinnacles**.
5. Decades ago a Separatist capital ship crashed along the makatea's east edge and onto the reef flat. Jungle and coral grew over it until it read as a **ridge**.
6. The CIS have now reoccupied the hull as a foundry.

## Signature set piece: the Ship on the Reef
From the sea it looks like an overgrown ridge. Up close it's a hull more than 2 km long:
- the bow gate sits on the makatea;
- the keel hangar and foundry deck are inside;
- the stern reactor hall stands on the reef;
- debris and pillboxes cover the wadeable debris flat around it.

**Engine fit:** the terrain carries a long berm (the "ridge"), so the distant read works when objects are culled past about 1.8 km. Up close, the hull comp sits on and against the berm, so the interiors are above ground.

**Ways in (5):** the bow gate (vehicles, from the makatea), the debris-flat wade, hull breach tunnels, the conveyor pier from the lagoon, and an air drop once the AA blisters are down.

A second set piece is the **Pinnacle Maze** on the makatea: a natural tunnel-like maze built with rock objects and shells.

## Op flow (6 ops, 3 weekends). Front: clockwise round the ring, then across the lagoon. Ops 2-4 can be reordered.
| Op | Start | Area | Main objectives | End state | Front moves |
|---|---|---|---|---|---|
| 1 East Motus | Fleet offshore, east | East ring motus, east pass | East Pass Battery (P), Pass Fort, Desalination Plant, Coral Block Tunnels | East pass open to the Navy | FOB on the east motu |
| 2 The Reef Walk | East motu | South ring | Reef Pillbox Belt (wade under fire), Tide Wreck Fort, Long Motu Village (P), South Pass Batteries | South ring held | FOB on Long Motu |
| 3 Lagoon Stilts | Long Motu | Lagoon patch reefs | South Stilt Town (P), Habitat Dome Corridors, Hover Pier, Stilt Clinic (rescue) | Lagoon held | FOB in the stilt town |
| 4 West Ring | Stilt town | West motus, airstrip | West Motu Airstrip (P), West Pass AA N and S, Radar Dome | CIS air gone | FARP on the airstrip |
| 5 Makatea Cliffs | West motu | Makatea | West Cliff Notch Wall (P), Pinnacle Maze (P), Miners' Town (P), Cliff Gun Galleries | Plateau held | FOB in the Miners' Town |
| 6 The Ship on the Reef | Miners' Town | The hull | Bow Gate (P), Keel Hangar (P), Hull Breach Tunnels (P), Midships Foundry | Foundry destroyed | End of run |

## Movement
- **Infantry:** wades a lot. Reef flats run about -0.3 to -1.2 m and the debris flat about -0.7 m (sketch).
- **Boats, hovers and air:** cross the lagoon (-5 to -16 m).
- **Passes:** boats only, about -10 m.
- **Vehicles:** almost none: the motus are small, and only the makatea plateau and the airstrip motu take them. This is the most infantry- and Navy-heavy concept.
- **Gap depths:** see the MEASURED table below.

<!-- AUTO-MEASURED START -->
**MEASURED on the sketch height field** (16 m cells; built by `tools/make_all.py`; the sketch is itself ASSUMED design):

| Island (sketch) | Area km² |
|---|---|
| Makatea + hull | 21.9 |
| East motu | 0.9 |
| South motu | 1.5 |
| West motu | 1.4 |
| **All land above 0 m** | **32.8** |

| Gap / route | Line length m | Water along it m | Deepest m | Shallowest m | Crossed by |
|---|---|---|---|---|---|
| Reef walk: east motu -> south motu | 3471 | 1355 | -1.2 | -0.0 | wade the reef flat |
| East pass (along its axis) | 1800 | 1800 | -14.9 | -10.0 | boats only |
| South motu -> stilt town (lagoon) | 2828 | 2692 | -10.9 | -0.0 | boat / hover / air |
| Stilt town -> makatea | 3672 | 3062 | -11.7 | -0.2 | boat / hover / air |
| West motu -> makatea | 1980 | 1050 | -1.5 | -0.0 | boat; reef flat then lagoon |
| Makatea -> hull (debris flat) | 1526 | 562 | -0.7 | -0.0 | wade the debris flat / walk the berm |

Objective sites: 66 over 6 ops (squad 21, two-squad 35, platoon 10). Highest point 67 m; deepest -50 m.
<!-- AUTO-MEASURED END -->

## Why it's distinct
- **vs Blackfen:** bright and flat-water, not a dark channel maze. Wading is the main movement, and the set piece is a crashed ship.
- **vs Aparra and Sarrak:** nothing alike.
- **vs A and B:** C is the lowest relief (highest point about 65 m, sketch), the most wading, the most stilt decks, and the only concept where the facility is a ship.

## Biggest risk
**Flat and exposed.** An atoll has long sight lines over water, and players wading at about 1 m depth are slow targets. Two engine risks follow:
- **Lots of stilt decks**, which must be normal objects (04: AI fall through simple floors; mod decks need tests).
- **Droid garrisons on decks:** static garrisons only, no patrols (04).

**Mitigations:**
- palms and coral-rubble berms as cover on the motus;
- coral heads and wreck debris as cover on the flats;
- sea haze;
- the makatea and hull block the north;
- wading belts no longer than about 400 m between pieces of cover (ASSUMED target).

**Early check:** test 2 (wading AI) and test 3 (deck patrols) in RISKS.md, before Stage B.

## Rough build cost (ASSUMED)
- **New comps:** 1 big one (the hull interior). The pinnacle maze reuses rock kitbash.
- **Reused:** stilt-town pieces in quantity, pass forts, airstrip.
- **Terrain work:** the simplest heightmap of the three. Reef micro-terrain and coral heads need care.
- **Effort:** low terrain, high comps (the hull is the biggest single new comp across all three concepts).
