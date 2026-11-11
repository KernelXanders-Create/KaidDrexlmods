# Swamp concept A: The Mire Line (rev 2, PROPOSED)

**Pitch:** a trench war across a cratered peat bog. It is no longer one line pushed belt by belt: it is a field of separate salients and strongholds that command chooses through. A gas refinery in a flooded strike crater and a citadel dug into the north moraine are the two new builds.

## Setting (REV2 point: "Mimban is mostly Imperial-era lore")
- **Default:** an original mud world. I've left it unnamed; Miran or command names it. The look stays the same: ochre mud, grey-green overcast sky, dead stumps, rust and smoke.
- **Option:** keep Mimban for the look and accept the era stretch. This is the same issue I raised with Scarif in Stage A (QUESTIONS Q2).

## What changed from Stage A (REV2 point: "belt-by-belt reads as lanes and a forced order")
- **The three map-wide trench belts are gone.** In their place are trench salients and redoubts on rises, eskers and crater rims, with open bog between them. Every op's sites form a branching network with 4 mains, so command takes the final plus any 2. No op has to follow another in a fixed line:
  - week 1: ops 1 and 2;
  - week 2: op 3 (after op 1) and op 4 (after 2 or 3);
  - week 3: op 5 (after 2 or 4) and op 6 (after 3 or 4);
  - week 4: op 7 (after 5 or 6), then op 8.
- **The front moves round the map, not up one axis:**
  - the south-centre and the south-west corner in week 1;
  - the south-east gas field and the centre in week 2;
  - the west esker and the east crater in week 3;
  - the north moraine in week 4.
- **No repeated band.** Each trench site uses a different library mix (Metal Trench Line, Basic Trenchline, Mrogg support-trench part, bunkers), and they are scattered.
- **Trenches are carved into the Stage B heightmap itself** where a comp needs a cut, plus library trench comps. There is no Deformer (REV2 rule 13).

## Main draws and build budget
| Draw | Build | Week |
|---|---|---|
| D1 The Cauldron Refinery | **NEW 1**: Droid-Factory-class refinery on stilts in a flooded strike crater (about 350 x 300 m). No mega set piece: the crater rim and spoil are terrain. | 3 (op 6) |
| D2 The Moraine Citadel | **NEW 2**, with the planet's **one capstone interior** inside | 4 (op 8) |
| D3 The Esker Redoubt | library cluster on the west esker | 3 (op 5) |
| D4 The Drain Locks | library cluster (CIS Fortress Dam as the lock) | 2 (op 4) |
| D5 The Peat-Gas Works | library cluster (Mining Complex + Large Fuel Depot) | 2 (op 3) |
| D6 The Old Listening Post | library cluster (Communications FOB + Giant Radar Dish), with a story reason: it is a lost Republic post | 1 (op 2) |

- **New comps:** 2 of 2.
- **Tunnels:** 3 library tunnel sites, all dugouts or roofed cuts: Dugout Command Post (op 1), Esker Dugouts (op 5) and Rim Spoil Galleries (op 6).
- **Towns (hand-made town work):** Stake Hamlet, Peat Cutters' Village, Cauldron Apron Town and Kesh Junction.
- **Interiors:** every interior other than the capstone is a library interior (`library_interior` in the JSON).

## The 8 ops (MEASURED from the data by `tools/make_k3.py`)
<!-- AUTO-OPTABLE START -->
| Op | Week | After (any of) | Start | Draw | Final | Mains (command picks any 2 + the final) | Supporting | Sizes s/t/p | Air-prep / air-only | Planned garrison | FOB after |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 Over the Wire | 1 | opener | (8.0, 0.8) km | - | Wirefield Redoubt (platoon) | Pillbox Knoll (two-squad); Rail Halt (platoon); Crater Gun Pits (two-squad); Dugout Command Post (two-squad) | 12 | 8/7/2 | 1 / 1 | 770 | Wirefield Redoubt |
| 2 The Old Listening Post | 1 | 1 | (4.4, 0.9) km | D6 Old Listening Post | Old Listening Post (platoon) | West Esker South Fort (platoon); Kettle Pumphouse (two-squad); Dish Field (two-squad); South Moraine West Battery (two-squad) | 12 | 9/6/2 | 1 / 1 | 745 | Old Listening Post |
| 3 The Peat-Gas Fields | 2 | 1 | (8.2, 3.6) km | D5 Peat-Gas Works | Peat-Gas Works (platoon) | Kettle East Fort (platoon); Pipeline Pumping Station (two-squad); East Crater Battery (two-squad); Gasworks Spur (two-squad) | 12 | 8/7/2 | 1 / 1 | 770 | Peat-Gas Works |
| 4 The Drain | 2 | 2, 3 | (8.2, 3.6) km | D4 Drain Locks | Drain Locks (platoon) | Peat Cutters' Village (platoon); Drain Rail Bridge (two-squad); Central Salient (platoon); Barge Quay (two-squad) | 12 | 7/7/3 | 1 / 1 | 855 | Peat Cutters' Village |
| 5 Esker Road | 3 | 2, 4 | (5.2, 7.8) km | D3 Esker Redoubt | Esker Redoubt (platoon) | Esker Road Gate (two-squad); Esker Dugouts (two-squad); North-west Battery (two-squad); Moss Abbey Ruin (platoon) | 12 | 9/6/2 | 1 / 1 | 745 | Esker Redoubt |
| 6 The Cauldron | 3 | 3, 4 | (10.4, 7.2) km | D1 Cauldron Refinery | Cauldron Refinery (platoon) | Rim Bunker Ring (platoon); Terrace Batteries (two-squad); Tank Laager (two-squad); Cauldron Apron Town (platoon) | 12 | 8/6/3 | 1 / 1 | 830 | Cauldron rim |
| 7 Moraine Foot | 4 | 5, 6 | (10.4, 10.4) km | - | Kesh Junction (platoon) | Command Dugout Salient (platoon); Rail Junction Yard (two-squad); Moraine Outwork Battery (two-squad); Moraine Road Gate (two-squad) | 12 | 8/7/2 | 1 / 1 | 770 | Kesh Junction |
| 8 The Moraine Citadel | 4 | 7 | (10.6, 13.2) km | D2 Moraine Citadel | Moraine Citadel (platoon) | Citadel Gate (two-squad); Hangar Bunkers (platoon); Moraine Battery (two-squad); Citadel Power Plant (two-squad) | 12 | 8/7/2 | 1 / 1 | 770 | end of run |
<!-- AUTO-OPTABLE END -->

All 8 ops pass the per-op checks: 1 final, 4 mains, 12 supporting, all three sizes, 1 air-prep, 1 air-only, a platoon site before the final, and a planned garrison of 745-855 if every site filled at once (under 1,200). See `tools/out/checks.txt`.

## Water and the AI (MEASURED on the sketch)
- 135 of 136 sites sit on **one connected landmass**. The bog pools are scattered, not joined, so droids can walk everywhere except across the Drain.
- **The Drain is crossed at three planned AI points:** the Drain Locks dam crest (D4), the Drain Rail Bridge and the Plank Road Bridge. These are vanilla or CUP bridges, not 3AS (ASSUMED; your convoy test decides).
- Only one site stands on water: the Cauldron Refinery on stilts.
- **No hovers are needed,** and nothing depends on boats.

## Coverage
All 16 squares carry sites, with 5-18 per square. See COVERAGE.md.

## Recon
Every draw, final and main is seen from 1 km or more on at least 14 of 24 bearings in the terrain-only screening. This bog is open, and the dead-stump vegetation planned here hides little.

## Fog
Low ground mist in the crater field at dawn is a mood choice for missions. It is not needed to hide anything.

## Why it's still distinct from Blackfen
It differs on all five counts:
1. **Palette:** ochre and grey overcast, not violet night.
2. **Vegetation:** dead stumps and moss, not lush swamp forest.
3. **Water:** scattered pools and one drain, not a delta.
4. **Set piece:** a crater refinery and a moraine citadel.
5. **Op flow:** a field of salients.

## Open points
- The name of the world (above).
- How Gruppe Adler or library trench comps sit on a 4-5 m heightmap with carved cuts: Stage B work.
- Whether droids hold trench comps well as static garrisons: needs a test (Stage A RISKS A2).
