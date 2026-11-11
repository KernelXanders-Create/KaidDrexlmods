# Swamp concept C: River Country (PROPOSED)

**Pitch:** Riverine war on Rodia. One great meandering river with levee roads, backswamp lakes, a fuel refinery rising out of an oxbow lake, a tiered Rodian river city, and a droid foundry on the headwater terrace. The Navy leads, and armour rides the levees.

## Setting
**Rodia**, a canon Clone Wars jungle-swamp world with Rodian towns. That gives real sci-fi river towns (HARD rule: 60 % or more sci-fi buildings) and a population worth saving. The palette is bright green and olive, golden morning haze, clear water and lilies. **Alternative skin:** Naboo lake country, if Miran prefers.

## Landform story
1. A big river meanders from the east terrace to the west across a wide floodplain between two **bluffs** (north about +35 m, south about +16 m).
2. Each flood drops silt on the banks, building **natural levees** about 2-3 m high right at the river and sloping into the **backswamp**, a low wet zone of lakes and pools at -0.8 to -1.0 m.
3. Old bends were cut off into **oxbow lakes** (about -2.2 m).
4. A **bayou** (a side channel, about -1.8 m) drains the north.
5. Rodians built on the only dry, continuous ground, the levees: roads, towns and a walled river **city** on a bend.
6. The CIS added a **stilt refinery** in the west oxbow and a **foundry** on the east terrace where the river enters.

## Signature set piece: the Stilt Refinery and the River City
**Stilt Refinery:** tanks and flare stacks stand on piles out in the oxbow lake, reached by pier causeways. It reads big from kilometres away (flares) and is surrounded by water, which makes a natural moat.

**Rodian River City:** a tiered city on a levee bend, with an undercity canal maze and the only vehicle bridge over the river. This is the "1 city-scale place".

## Op flow (6 ops, 3 weekends). Front: west to east, upstream, with north and south branches.
| Op | Start | Area | Main objectives | End state | Front moves |
|---|---|---|---|---|---|
| 1 River Mouth | West edge (boats, LAAT) | West reach | Levee Fort West (P), Ferry Landing, Levee Battery, Levee Bunker Galleries | Lower river held | FOB at the ferry landing |
| 2 The Oxbow | Ferry | West oxbow | Stilt Refinery (P), Refinery Pier Causeway, Neck Village, Pumphouse Tunnels | Refinery destroyed | FOB at the neck village |
| 3 Rodian River City | Neck village | City bend | City Levee Wall Gate (P), Market Tiers (P), Undercity Canal Shells (P), City Bridge | City liberated, bridge held | FOB in the city |
| 4 North Bluffs | City | North floodplain and bluffs | Bluff Fort (P), Bluff Face Galleries, Bayou Head Village, Bayou Bridge | North high ground held | FOB on the bluff |
| 5 Upper Bends | City | East bends | Second Oxbow Fort (P), Plantation Stilt Town (P), River Weir, Levee Tunnels East | River open to the terrace | FOB at the plantation |
| 6 Headwater Works | Plantation | East terrace | Foundry Terraces (P), Assembly Halls (P), Gallery Tunnel Maze (P), Terrace Gate | Foundry destroyed | End of run |

**Branching:** ops 4 and 5 can run in either order after the city falls. Op 4 is a flank that gives high-ground payoffs (the guns see the terrace).

## Movement
- **The river** (about -4.5 m, about 230 m wide on the sketch): boats only, plus swimming. No ford. The city bridge is the only vehicle crossing (ASSUMED: a second bridge or ferry may be needed; see the questions).
- **Levees:** continuous firm ground on both banks, so they carry the AI roads (gentle and flat). Tanks and walkers fight along them.
- **Backswamp:** wade pools and lakes (-0.8 to -1.0 m), plus hover and boat lakes.
- **Bayou:** about -1.8 m, a bridge for vehicles.
- **Bluffs:** about 16-35 m of relief gives real high ground and guns with clear lines of fire.
- **Depths:** see the MEASURED table below.

<!-- AUTO-MEASURED START -->
**MEASURED on the sketch height field** (16 m cells; built by `tools/make_all.py`; the sketch is itself ASSUMED design):

| Island (sketch) | Area km² |
|---|---|
| **All land above 0 m** | **224.3** |

| Gap / route | Line length m | Water along it m | Deepest m | Shallowest m | Crossed by |
|---|---|---|---|---|---|
| River at Rodian city (bridge) | 860 | 346 | -4.5 | -0.2 | bridge; boats; swim |
| River, west reach | 1300 | 361 | -4.5 | -0.1 | boat; swim (no ford) |
| Oxbow lake (refinery) | 1600 | 336 | -2.2 | -0.0 | piers; boat |
| Bayou | 1000 | 488 | -1.8 | -0.0 | bridge; wade/swim |
| Backswamp lake east | 2000 | 1904 | -1.0 | -0.1 | boat/hover; walk round |

Objective sites: 67 over 6 ops (squad 22, two-squad 34, platoon 11). Highest point 35 m; deepest -5 m.
<!-- AUTO-MEASURED END -->

## Why it's distinct from Blackfen (needs 2 of 5; this has 4)
1. **Palette:** bright green and gold.
2. **Water:** one big river with oxbows and lakes, not a delta maze.
3. **Set piece:** the stilt refinery and the river city.
4. **Op flow:** an upstream riverine push.

Vegetation (gallery jungle on the levees) is the closest point to Blackfen. Keep it lighter and greener.

**vs B and A:** C is the most vehicle and Navy friendly swamp, and the only one with a city.

## Biggest risk
**AI convoys on the levee roads, and the river splitting the map.**
- Levee roads are flat and gentle, which is good for 04 (convoys leave the road on switchbacks), but they're narrow with water on both sides. AI vehicles that leave the road drown.
- A single bridge makes the river a hard wall for AI.

**Early checks:** an AI convoy test on a 2 km levee road with water either side, and a decision on whether AI ever crosses the river. Proposed: **no**. Each bank has its own garrisons and counterattacks.

## Rough build cost (ASSUMED)
- **New comps:** 2 (the stilt refinery and the river city core). The foundry reuses facility pieces.
- **Reused:** stilt towns, levee bunkers, bridges.
- **Terrain:** the river, levees and oxbows are clean shapes. The backswamp needs micro-terrain.
- **Effort:** medium. The city is the biggest job.
