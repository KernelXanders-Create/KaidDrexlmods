# Swamp concept B: The Glow (PROPOSED)

**Pitch:** A bright Felucia "river of grass". Open sawgrass sloughs, teardrop hammocks topped with giant fungi, a limestone ridge forest, and a giant fallen fungal stalk lying across the main slough with a CIS bio-lab inside its hollow trunk.

## Setting
**Felucia**, a canon Clone Wars Republic-vs-CIS battle world. The palette is saturated and warm: orange, teal and magenta fungi, gold grass, bright humid daylight, low bright haze instead of dark fog. Blackfen is dark and blue-violet; this is bright and warm.

## Landform story
1. A flat **limestone shelf** tilts gently south, so water sheets slowly across it: the **sloughs**, very shallow (about -0.4 to -0.6 m) and branching.
2. Wherever the rock sits a little higher, peat and trees build **hammocks** (+1.4 to +3.2 m). The flow shapes them into **teardrops** with tails pointing downstream.
3. A **limestone ridge** (up to about +12 m) in the west carries the giant fungus forest.
4. A **northern rise** (about +20 m) holds the CIS citadel.
5. Limestone dissolves, so **cenotes** (sinkholes, about -8 m) pock the shelf.
6. The sloughs drain into a **south lake** (about -1.6 m).
7. An old Republic **canal road** (a levee with a canal beside it) runs north-south on the east side.
8. Decades ago a titanic fungal stalk fell across the main slough: the **Felled Titan**.

## Signature set piece: the Felled Titan
A fallen stalk about 2.8 km long and tens of metres thick lies across the main slough. Its root plate is a fort on the west hammock and its crown a fort on the east. Inside the **hollow trunk** is a CIS bio-lab: tight bores opening into big chambers.

- It's a natural bridge: infantry cross on top, and the trunk is an interior.
- It's visible from everywhere in the open grass, so recon sees it big.
- Build: scaled tree, root and rock kitbash, plus a lab interior comp. **This is a build risk:** it needs a test that the shapes read as a single stalk. It is the most "new asset" piece of the six concepts.

## Op flow (6 ops, 3 weekends). Front: south to north, with two flank options.
| Op | Start | Area | Main objectives | End state | Front moves |
|---|---|---|---|---|---|
| 1 Edge of the Grass | South lake (hover, boat, LAAT) | South sloughs and hammocks | Gladeside Village (P), Lakeshore Hover Pens, Heron Hammock Fort, Cenote Rim Shells | Lakeshore held | FOB in Gladeside |
| 2 Canal Road | East hammocks | East canal road | Canal Lock Fort (P), Ranger Station (retake), Levee Bunker Galleries, Canal Bridge | Vehicle route north open | FOB at the ranger station |
| 3 Spore Ridge | Gladeside | West ridge forest | Spore Works South Lab (P), Ridge Road Fort (P), Root Cellar Maze, Ridge Gun Battery | West ridge held | FOB on the ridge |
| 4 The Felled Titan | Centre | The Titan and main slough | Titan Hollow Trunk (P), West Root Fort (P), Crown East, Slough Hover Pens | Titan lab destroyed | FOB at the Titan crown |
| 5 Hammock Archipelago | Titan | North-central hammocks | Big Hammock Fort (P), Cenote Ring Tunnels, Spore Works North Lab | Approaches to the rise clear | FOB on the big hammock |
| 6 Spore Citadel | Big hammock | North rise | Citadel Main Lab (P), Culture Vat Halls (P), Root Tunnel Maze (P), Gate Wall | Citadel destroyed | End of run |

**Branching:** ops 2 (east, vehicles) and 3 (west, forest) can run in either order, and op 4 is reachable from either.

## Movement
- **Infantry:** wade the sloughs (about -0.4 to -0.6 m on the sketch) almost anywhere, which is slow and exposed. They hop hammock to hammock and choose routes by cover.
- **Hovers:** the main vehicle in the grass, if the modset's hovers work over shallow water (Q list).
- **Boats:** the main slough's channel (about -1.8 m, 40 m wide), the south lake and the canal.
- **Tanks:** the canal road (east), the ridge road (west) and the north road. These are the AI lanes on the sketch.
- **Boardwalks:** two (normal objects; 04).
- **Depths:** see the MEASURED table below.

<!-- AUTO-MEASURED START -->
**MEASURED on the sketch height field** (16 m cells; built by `tools/make_all.py`; the sketch is itself ASSUMED design):

| Island (sketch) | Area km² |
|---|---|
| **All land above 0 m** | **201.6** |

| Gap / route | Line length m | Water along it m | Deepest m | Shallowest m | Crossed by |
|---|---|---|---|---|---|
| Main slough at the Titan | 3015 | 1812 | -1.8 | -0.0 | Titan bridge; or wade 0.4-0.6 m; boat channel 1.8 m |
| Main slough, south | 3600 | 2384 | -1.8 | -0.0 | wade; hover; boat channel |
| East branch slough | 2400 | 1304 | -0.5 | -0.0 | wade; hover |
| South lake | 2800 | 2800 | -1.8 | -1.6 | boat / hover only |
| Canal beside canal road | 600 | 80 | -2.0 | -0.4 | bridges; swim |

Objective sites: 66 over 6 ops (squad 22, two-squad 34, platoon 10). Highest point 22 m; deepest -8 m.
<!-- AUTO-MEASURED END -->

## Why it's distinct from Blackfen (needs 2 of 5; this has all 5)
1. **Palette:** bright and warm, not dark violet.
2. **Vegetation:** sawgrass and giant fungi, not dark swamp forest.
3. **Water:** sheet-flow sloughs and open grass, not channels.
4. **Set piece:** the Felled Titan.
5. **Op flow:** hammock-hopping with east and west flank choices.

**vs B islands and the other swamps:** the only concept with long open sight lines over grass, and the only one whose landmark is organic.

## Biggest risk
**Open grass plus AI sight.** 04 says AI see through foliage differently from players. Tall sawgrass may hide players from players but not from AI, or the other way round. If the grass hides nothing from AI, wading players get shot from 600 m (ASSUMED).

**Early check:** test the grass-clutter AI sight (RISKS B1) on a test tile before Stage B, and decide the grass height and density with Miran.

## Rough build cost (ASSUMED)
- **New comps:** 2 (the Titan, and the citadel lab). That is at the house-rule limit of 1-2 new comps per map.
- **Reused:** stilt villages, canal lock, levee bunkers.
- **Terrain:** simple heightmap, but heavy clutter and satellite work for the grass to read at distance.
- **Effort:** medium-high, mostly in the Titan.
