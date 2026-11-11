# Swamp concept A: The Mire Line (PROPOSED)

**Pitch:** A Mimban-style trench war across a shell-cratered peat bog. The front is literal: three trench belts, a flooded orbital-strike crater with a refinery in it, and a CIS citadel dug into the northern moraine.

## Setting
**Mimban**, a canon mud world. The palette is ochre and brown mud, grey-green sky, pale dead stumps, rust and smoke: a bleak daylight overcast. That is opposite to Blackfen's lush violet night.

## Landform story
1. Ice sheets left a flat **outwash plain** framed by two **moraines**: low hills south (Republic lines) and higher hills north (the CIS citadel).
2. Meltwater rivers under the ice left winding **eskers**, gravel ridges 9-15 m high (sketch) that are the only firm high ground across the bog.
3. Blocks of buried ice melted into **kettle lakes**.
4. Peat grew over everything, with countless bog pools.
5. Then the war came. Shelling cratered the middle of the plain, and an **orbital strike** blew a 1.4 km crater (the Cauldron), whose floor flooded below 0 m.
6. A sluggish drainage channel (**the Drain**) crosses west to east.
7. A **rail embankment** (+3 m) is the one straight-ish vehicle line.

## Signature set piece: the Cauldron
The crater has a raised rim (about +12 m) and a flooded floor (about -1.5 m). The CIS built a **fuel refinery on stilts** in the middle of it, with flare stacks visible for kilometres, terraced gun stairs on the inner wall, and tunnel shells in the rim spoil. It gives recon a big, readable target, and "a refinery rising out of the water" from the brief.

A second set piece is the **trench belts themselves**: three belts across the whole map, each a platoon-scale maze. We haven't done a trench map before.

## Op flow (6 ops, 3 weekends). Front: south to north, with branching.
| Op | Start | Area | Main objectives | End state | Front moves |
|---|---|---|---|---|---|
| 1 Over the Top | Republic lines (south moraine) | No man's land, first belt | First Trench Belt W and E (P, either or both), Pillbox Knoll, Dugout Galleries, Rail Halt | First belt broken | FOB at the first belt |
| 2 The Drain | First belt | The Drain and second belt (centre and east) | Drain Bridge (only tank crossing), Peat Cutters' Village (P), Second Trench Belt (P), Duckboard Maze | Drain crossed | FOB at the village or bridge |
| 3 Esker Road | Village | West eskers | Esker Fort North (P), Esker Rail Cutting, Esker Dugouts, Walker Park | West flank turned | FOB on the esker fort |
| 4 The Cauldron | Second belt | The crater | Cauldron Refinery (P), Rim Bunker Ring (P), Rim Tunnels (P), Tank Laager | Refinery destroyed | FOB on the crater rim |
| 5 Third Line | Cauldron rim | Third belt | Third Belt W and E (P), Command Dugout (P), Rail Junction | Last belt broken | FOB at the command dugout |
| 6 Moraine Citadel | Command dugout | North moraine | Moraine Citadel (P), Gallery Maze (P), Hangar Bunkers, Gate Wall | CIS HQ destroyed | End of run |

**Branching:** ops 3 (west) and 4 (centre-east) can run in either order. Each belt has W and E halves, so command can hit one and bypass the other.

## Movement
- **Water:** shallow and scattered. Bog pools and kettles run -0.5 to -1.6 m (sketch). The Drain is about -1.8 m (swim or hover; bridge for tanks). The Cauldron floor is about -1.5 m (stilt decks).
- **Infantry:** most ground is firm-ish peat (+0.3 to +1.2 m) peppered with craters. Infantry pick routes between pools. Craters and pools are the micro-terrain, so this concept satisfies the "not flat" rule hardest.
- **Vehicles:** tanks and walkers on the esker crests (AI roads), the rail embankment and the central plank road (the AI lanes on the sketch). Off-road through craters is possible but slow (ASSUMED; needs a test).
- **Hovers:** the Drain and the kettle lakes.
- **Boats:** barely needed. This is the least boat-dependent of the three.
- **Depths:** see the MEASURED table below.

<!-- AUTO-MEASURED START -->
**MEASURED on the sketch height field** (16 m cells; built by `tools/make_all.py`; the sketch is itself ASSUMED design):

| Island (sketch) | Area km² |
|---|---|
| **All land above 0 m** | **240.0** |

| Gap / route | Line length m | Water along it m | Deepest m | Shallowest m | Crossed by |
|---|---|---|---|---|---|
| The Drain (main crossing at bridge) | 800 | 112 | -3.4 | -0.2 | bridge; or wade/swim |
| Kettle lake west | 1000 | 808 | -1.6 | -0.1 | boat/hover; walk round |
| Cauldron floor | 800 | 800 | -1.9 | -1.1 | stilt decks over flooded floor |
| Bog between eskers (sample) | 4833 | 16 | -0.1 | -0.1 | wade pools, walk the firm ground |

Objective sites: 68 over 6 ops (squad 22, two-squad 33, platoon 13). Highest point 34 m; deepest -5 m.
<!-- AUTO-MEASURED END -->

## Why it's distinct from Blackfen (needs 2 of 5; this has all 5)
1. **Palette:** brown and ochre overcast, not violet night.
2. **Vegetation:** dead stumps and moss, almost no canopy, not lush swamp forest.
3. **Water:** scattered pools and one drain, not a delta channel maze.
4. **Set piece:** a crater refinery and trench belts.
5. **Op flow:** a line-breaking push, belt by belt.

**vs Aparra and Sarrak:** no forest or gorge, no desert. **vs B and C:** A is the most open and the most infantry-heavy, and its terrain is shaped by war.

## Biggest risk
**AI in craters and trenches.** 04 says droids stall after 100-200 m on rough ground, and craters are exactly that. This concept leans on static droid defence (trenches suit that) and counterattacks from communication trenches 250-400 m behind the belt. Trenches must be objects (Gruppe Adler Trenches is in the modset; whether its pieces suit static AI garrisons is ASSUMED, not checked).

**Early check:** in Stage B, put a B1 platoon in a 200 m trench piece and order a counterattack from 300 m across a crater field.

## Rough build cost (ASSUMED)
- **New comps:** 1 (the Cauldron refinery and rim).
- **Trench belts:** a big reusable comp kit (one belt segment repeated with variations, not copies; avoid "repetitive bands of the same objects").
- **Reused:** citadel walls, batteries, villages.
- **Terrain:** craters (scripted stamp) and eskers. Medium.
- **Risk to budget:** trench object count.
