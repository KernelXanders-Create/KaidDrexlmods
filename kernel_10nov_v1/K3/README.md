# KERNEL_RETURN_10NOV_K3: swamp concepts A / B / C at the 9 Nov targets (PROPOSED)

Job K3 from the 10 Nov pack: "Path 2" of REV2 for the swamp only. All three concepts are brought to sketch level and presented as A / B / C, with **no recommendation** (Miran picks).

## Pick one
- **A The Mire Line:** a trench war across a cratered peat bog. It is now a field of separate salients and strongholds, not belts.
  - **New builds:** a gas refinery in a flooded strike crater (week 3) and a citadel dug into the north moraine (week 4, with the capstone inside).
  - **Water:** almost all ground is one landmass, and the Drain has 3 AI crossings.
  - **Setting:** an original mud world (Mimban as an option).
- **B The Glow:** Felucia's "river of grass": sawgrass sloughs, teardrop hammocks and a giant-flora ridge.
  - **The Titan** is now a terrain berm across the main slough. It is the only dry crossing and is walkable by AI.
  - **New builds:** a lab at the Titan's root plate (week 2) and the Spore Citadel (week 4, with the capstone inside).
  - **Water:** the sloughs split the shelf into 9 landmasses that each hold their own garrison.
- **C River Country:** Rodia's great river with levee roads, oxbows, a tiered river city and bluffs north and south.
  - **New builds:** a stilt refinery in an oxbow (week 1) and the Headwater Foundry (week 4, with the capstone inside).
  - **Water:** the river is crossed by 4 AI crossings (3 bridges and a weir).
  - **Towns:** six, the most town work of the three.

## What is in this zip
| File | What it is |
|---|---|
| `README.md` | This page |
| `swamp/concept_A.md`, `concept_B.md`, `concept_C.md` | Each concept: setting, what changed and the REV2 point it fixes, draws and build budget, the 8-op table, water and AI, coverage, recon, fog, distinctness, open points |
| `swamp/plan_A.png`, `plan_B.png`, `plan_C.png` | 16 x 16 km plans: depth and height colours, the 4 x 4 km squares with site counts, all 8 op AOs and starts, draws (orange = new build, yellow = library cluster), AI roads and crossings. No lanes and no order are shown. |
| `swamp/objectives_swamp_A.json`, `_B.json`, `_C.json` | Every op and site as data: role, size, stake, library pick, draw, new_build, capstone, `interior` (capstone only) / `library_interior`, tunnel, air-prep, air-only, square, landmass, recon screening |
| `COVERAGE.md` | The sites per 4 x 4 km square for each concept, and the empty squares (none) |
| `DRAWS.md` | One table per concept: draw / square / new build or library / make-up / week / story reason / recon |
| `tools/` | Python: `make_k3.py`, `swamp_v2_data.py`, the Stage A terrain code (`concepts_swamp_v1.py`, `terrain_lib.py`) and `out/checks.txt` |

## Targets met (MEASURED by `tools/make_k3.py`; see `tools/out/checks.txt`)
| Target (REV2) | A | B | C |
|---|---|---|---|
| 8 ops over 4 weeks, all AOs planned now | yes | yes | yes |
| Per op: final + 4 mains + 12 supporting (12-16 asked) | yes, all 8 | yes, all 8 | yes, all 8 |
| All three sizes; a platoon site before the final | yes | yes | yes |
| 1-2 air-prep and up to 2 air-only per op | 1 / 1 | 1 / 1 | 1 / 1 |
| Planned garrison if every site filled at once (1,200 limit) | 745-855 | 745-805 | 720-745 |
| Main draws (4-6), spread over the weeks | 6 (weeks 1-4) | 6 (weeks 1-4) | 6 (weeks 1-4) |
| New-build centerpieces (1-2) / capstone interiors (exactly 1) | 2 / 1 | 2 / 1 | 2 / 1 |
| Tunnel sites (library only, biome fit) | 3 | 2 | 2 |
| Empty 4 x 4 km squares | none (5-18 sites each) | none (2-18) | none (2-19) |
| Draws and mains seen from 1 km or more (terrain-only screening) | all, on 14+ of 24 bearings | all, on 17+ | all, on 17+ |
| AI crosses water | never: 3 Drain crossings | never: Titan berm; 9 landmasses hold their own garrisons | never: 4 river crossings |
| Hovers relied on | no | no | no |
| Deformer | none; trench cuts go into the Stage B heightmap | none | none |

Each concept answers the point REV2 listed for it:
- **A:** the belts are broken into a network, and the lore question is answered.
- **B:** the Titan is now a terrain berm with a new root-plate lab, and the tunnels are library pieces.
- **C:** the south-east is filled, there are 4 river crossings, and the budget is 2 comps with the city as town work.

## Not done
- **No engine tests.** Every AI, bridge, convoy and grass-sight claim is ASSUMED.
- **No town plans for the swamp towns.** They are listed per concept as town work.
- **No Stage B heightmap, masks or renders.** The plans are 16 m sketch fields made from my Stage A terrain code.
- **No coverage per island,** which is not relevant for the swamp.
- **Library picks are names taken from the Islands purpose map.** Whether each one suits a swamp, and still loads, is for Compmaker to check.

## Open questions (with the default I used)
1. **A's world:** an original mud world, or Mimban despite the era? **Default:** original, unnamed (command names it).
2. **B's giant flora:** there is no fungal kit (REV2). **Default:** scaled Gliese plants, Rugosa coral and alien brush. This is B's biggest look risk.
3. **B's nine landmasses:** **Default:** each holds its own garrison. In Stage B, raised hammock trails would join the east side to the centre wherever Miran wants AI counterattacks to move.
4. **Bridges on AI routes (A and C):** **Default:** vanilla or CUP road bridges plus library dam crests, no 3AS bridges, all pending your convoy test.
5. **Garrison sizes** (squad 25, two-squad 50, platoon 110) are the Islands purpose map's ASSUMED figures. **Default:** same here.
6. **Map size:** **Default:** 16 x 16 km for all three swamps. The density targets are met without growing the map.

## Measured, assumed, unsure
- **MEASURED** by `make_k3.py` on the sketch data:
  - counts per op and per map;
  - sites per square and empty squares;
  - landmass ids and counts;
  - ground heights at sites;
  - the terrain-only recon screening: 24 bearings, 16 distances up to 4 km, eye 1.8 m.
- **ASSUMED:**
  - every position (hand-placed, then snapped to the nearest firm ground);
  - all landform shapes;
  - structure heights for the recon screening (6, 10 and 15 m; draws 30 m);
  - garrison sizes;
  - library suitability;
  - bridge classes.
- **Unsure:** recon is terrain only. Swamp trees and giant flora are not modelled, so Stage B dressing must keep sight corridors open to every draw.
