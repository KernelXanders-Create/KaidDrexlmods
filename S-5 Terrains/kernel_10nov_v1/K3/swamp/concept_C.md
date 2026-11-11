# Swamp concept C: River Country (rev 2, PROPOSED)

**Pitch:** riverine war on Rodia. One great meandering river with levee roads, oxbow lakes, a fuel refinery in an oxbow, a tiered Rodian river city, and a droid foundry on the headwater terrace.

## Setting
**Rodia**, a canon Clone Wars swamp world with Rodian towns. The palette is bright green and gold with clear water.

## What changed from Stage A (REV2 points: "the south-east row is empty", "the one bridge makes the river a wall for AI", "3 comps, over budget")
- **The south-east is filled.** A new draw, D6 South Bluff Quarry, and op 4 cover the south-east and south-centre. Squares C1 and D1 now carry 5 and 8 sites.
- **Four planned AI river crossings:**
  1. the Mouth Bridge (op 1);
  2. the City Bridge (op 3);
  3. the River Weir dam crest (op 5; library CIS Fortress Dam);
  4. the Headwater Bridge (op 7).

  These are vanilla or CUP road bridges plus the dam, with no 3AS bridge on an AI route (ASSUMED; your convoy test decides). Each bank still holds its own garrison, and reserves never need to cross.
- **Budget is back to 2 new comps:**
  - the Stilt Refinery is NEW 1;
  - the Headwater Foundry is NEW 2, with the capstone inside, so the finale has it;
  - the Rodian River City is now **hand-made town work** with library checkpoints and AA, not a comp.

## Main draws and build budget
| Draw | Build | Week |
|---|---|---|
| D1 The Stilt Refinery | **NEW 1**: Droid-Factory class, on stilts in the west oxbow | 1 (op 2) |
| D2 The Headwater Foundry | **NEW 2**, with the planet's **one capstone interior** inside | 4 (op 8) |
| D3 Rodian River City | town work + library cluster | 2 (op 3) |
| D4 The River Weir | library cluster (Fortress Dam) | 3 (op 5) |
| D5 The North Bluff Fort | library cluster (Small Citadel + artillery + AA) | 3 (op 6) |
| D6 The South Bluff Quarry | library cluster (Mining Complex + artillery) | 2 (op 4) |

- **New comps:** 2 of 2.
- **Tunnels:** 2 library sites, both roofed cuts: Levee Tunnels East (op 5) and Bluff Face Galleries (op 6).
- **Towns (hand-made town work):** Fishing Stilt Village, Neck Village, River City, Splay Town, Bayou Head Village and Plantation Stilt Town. This is the most town work of the three concepts.

## The 8 ops (MEASURED from the data by `tools/make_k3.py`)
<!-- AUTO-OPTABLE START -->
| Op | Week | After (any of) | Start | Draw | Final | Mains (command picks any 2 + the final) | Supporting | Sizes s/t/p | Air-prep / air-only | Planned garrison | FOB after |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 River Mouth | 1 | opener | (0.5, 5.5) km | - | Levee Fort West (platoon) | Mouth Bridge (two-squad); Fishing Stilt Village (platoon); Levee Battery (two-squad); South Bluff AA (two-squad) | 12 | 10/5/2 | 1 / 1 | 720 | Levee Fort West |
| 2 The Oxbow | 1 | 1 | (1.6, 5.0) km | D1 Stilt Refinery | Stilt Refinery (platoon) | Neck Village (platoon); Oxbow Tank Farm (two-squad); Pipeline Gun Nests (two-squad); Levee Road Checkpoint (two-squad) | 12 | 9/6/2 | 1 / 1 | 745 | Neck Village |
| 3 Rodian River City | 2 | 2 | (6.6, 7.4) km | D3 River City Market Tiers | River City Market Tiers (platoon) | City Levee Gate (platoon); City Bridge (two-squad); Council Hall (two-squad); South Bank Battery (two-squad) | 12 | 9/6/2 | 1 / 1 | 745 | River City |
| 4 South Bluff Quarry | 2 | 2, 3 | (9.0, 6.2) km | D6 South Bluff Quarry | South Bluff Quarry (platoon) | Backswamp Lake Fort (platoon); Bluff Battery (two-squad); Quarry Rail Head (two-squad); Bluff Road Checkpoint (two-squad) | 12 | 9/6/2 | 1 / 1 | 745 | South Bluff Quarry |
| 5 The Weir | 3 | 3, 4 | (10.2, 7.6) km | D4 River Weir | River Weir (platoon) | Second Oxbow Fort (platoon); Levee Battery East (two-squad); Splay Town (two-squad); Weir Lock House (two-squad) | 12 | 9/6/2 | 1 / 1 | 745 | River Weir |
| 6 North Bluffs | 3 | 3 | (9.0, 7.8) km | D5 North Bluff Fort | North Bluff Fort (platoon) | Bluff Stair Battery (two-squad); Bluff Face Galleries (two-squad); Bayou Head Village (platoon); Bayou Bridge (two-squad) | 12 | 9/6/2 | 1 / 1 | 745 | North Bluff Fort |
| 7 Upper Bends | 4 | 5, 6 | (12.6, 9.8) km | - | Plantation Stilt Town (platoon) | Headwater Bridge (two-squad); Upper Levee Fort (platoon); Bend Battery (two-squad); North Lake Bunkers (two-squad) | 12 | 9/6/2 | 1 / 1 | 745 | Plantation Stilt Town |
| 8 Headwater Works | 4 | 7 | (13.2, 11.0) km | D2 Headwater Foundry | Headwater Foundry (platoon) | Assembly Yard (platoon); Terrace Gate Wall (two-squad); Foundry Battery (two-squad); Foundry Power Plant (two-squad) | 12 | 9/6/2 | 1 / 1 | 745 | end of run |
<!-- AUTO-OPTABLE END -->

All 8 ops pass the per-op checks (12 supporting each, a planned garrison of 720-745 if all filled). See `tools/out/checks.txt`.

**Choice:**
- op 4 (south bluff) follows 2 or 3;
- op 5 (weir) follows 3 or 4;
- op 6 (north bluffs) follows 3;
- op 7 follows 5 or 6;
- op 8 follows 7.

## Water and the AI (MEASURED on the sketch)
- **The sites sit on 2 main landmasses: the north bank (73) and the south bank (60).** The river splits them. The four crossings above are the only AI links between them.
- **3 sites stand on water:** the Stilt Refinery, its pier gate and the Fishing Stilt Village. The refinery is a new build; the other two are stilt and pier work, a known library gap.
- **Republic players:** Arma boats on the river (about -4.5 m) and the oxbow lakes. Armour runs on the levee roads.
- **Hovers are not relied on anywhere.**

## Coverage
All 16 squares carry sites, with 2-19 per square. The thinnest is B1, the south lake shore, at 2 sites. See COVERAGE.md.

## Recon
Every draw, final and main is seen from 1 km or more on at least 17 of 24 bearings in the terrain-only screening. Gallery jungle on the levees must keep sight corridors open to the draws.

## Fog
Golden morning river haze is a mood choice for missions.

## Why it's distinct from Blackfen
It differs on four counts:
1. **Palette:** bright green and gold.
2. **Water:** one big river with oxbows, not a delta maze.
3. **Set piece:** the stilt refinery and the river city.
4. **Op flow:** a riverine push up and across.

Vegetation (levee jungle) is the closest point to Blackfen. Keep it lighter and greener.

## Open points
- **AI convoys on narrow levees** with water on both sides need a test (Stage A RISKS C1).
- **Six towns** make this concept the biggest town workload.
- **The river splits the map:** the four bridges carry every AI move between banks. If one bridge class fails your test, that crossing drops to players only.
