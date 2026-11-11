# Swamp concept B: The Glow (rev 2, PROPOSED)

**Pitch:** a bright Felucia "river of grass": sawgrass sloughs, teardrop hammocks, a giant-flora ridge and a giant fallen stalk lying across the main slough.

## Setting
**Felucia**, a canon Clone Wars Republic-vs-CIS battle world. The palette is warm and bright: orange, teal and magenta flora, gold grass and humid haze.

## What changed from Stage A (REV2 point: "the Titan as a scaled-rock kitbash can't be a roof or a walkable bridge")
- **The Titan is now terrain.** The fallen stalk is a land berm baked into the heightmap: about 2.8 km long, 40 m wide and about 4 m above the slough (MEASURED on the sketch build). It is dressed with simple rock and bark objects only.
  - It has **no roof and no interior.**
  - Because it is land, it is walkable and AI can use it. It is the only dry crossing of the main slough.
- **The lab moved out of the trunk** into a new Droid-Factory-class build at the Titan's west root plate: the Titan Root Lab, about 300 x 250 m. That is NEW 1.
- **The capstone sits in NEW 2,** the Spore Citadel on the north rise (the finale).
- **The 2-comp budget is full, so tunnels are library pieces only:** the Cenote Caves (PLAD Cave Base) and the Root Cellar Maze (Royal Tunnel Holdout). 2 tunnel sites.
- **Big Hammock Fort is no longer a draw** (REV2 asked for a story reason). The east-hammock final is now the Grass Sea Fort, a plain library site.

## Main draws and build budget
| Draw | Build | Week |
|---|---|---|
| D1 The Felled Titan | **NEW 1** (the root-plate lab) + terrain berm | 2 (op 4) |
| D2 The Spore Citadel | **NEW 2**, with the planet's **one capstone interior** inside | 4 (op 8) |
| D3 The Canal Lock | library cluster (CIS Fortress Dam as the lock) | 1 (op 2) |
| D4 The Spore Ridge Grove | library cluster (Small Citadel + Large Power Facility) | 2 (op 3) |
| D5 The Lake Hover Base | library cluster (landing pads, vehicle depot, covered AA) | 1 (op 1) |
| D6 The Cenote Caves | library cluster (PLAD Cave Base), with a story reason: the spore stores | 3 (op 6) |

- **New comps:** 2 of 2.
- **Towns (hand-made town work):** Gladeside Village, Fungal Hamlet, Hammock Hamlet North, Cenote Hamlet and Grove Hamlet.

## The 8 ops (MEASURED from the data by `tools/make_k3.py`)
<!-- AUTO-OPTABLE START -->
| Op | Week | After (any of) | Start | Draw | Final | Mains (command picks any 2 + the final) | Supporting | Sizes s/t/p | Air-prep / air-only | Planned garrison | FOB after |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 Edge of the Grass | 1 | opener | (8.0, 0.6) km | D5 Lake Hover Base | Lake Hover Base (platoon) | Heron Hammock Fort (platoon); Lakeshore AA (two-squad); Gladeside Village (platoon); Hover Depot (two-squad) | 12 | 9/5/3 | 1 / 1 | 805 | Lake Hover Base |
| 2 Canal Road | 1 | 1 | (12.8, 1.2) km | D3 Canal Lock | Canal Lock (platoon) | Ranger Station (platoon); Levee Battery (two-squad); Pumping Station (two-squad); South Canal Checkpoint (two-squad) | 12 | 9/6/2 | 1 / 1 | 745 | Canal Lock |
| 3 Spore Ridge | 2 | 1 | (4.6, 3.2) km | D4 Spore Ridge Grove | Spore Ridge Grove (platoon) | Ridge Road Fort (platoon); Ridge Power Station (two-squad); Ridge Gun Battery (two-squad); Fungal Hamlet (two-squad) | 12 | 9/6/2 | 1 / 1 | 745 | Spore Ridge Grove |
| 4 The Felled Titan | 2 | 1, 3 | (4.6, 3.2) km | D1 Titan Root Lab | Titan Root Lab (platoon) | Titan Crown Fort (platoon); Mid-Titan Bunkers (two-squad); Slough Hover Pens (two-squad); Tree Island Battery (two-squad) | 12 | 9/6/2 | 1 / 1 | 745 | Titan root plate |
| 5 East Hammocks | 3 | 2, 4 | (12.2, 7.2) km | - | Grass Sea Fort (platoon) | Big Hammock Barracks (platoon); East Branch Bunkers (two-squad); Hammock Battery (two-squad); Stilt Supply Depot (two-squad) | 12 | 9/6/2 | 1 / 1 | 745 | Grass Sea Fort |
| 6 The Cenote Caves | 3 | 4, 5 | (12.4, 10.4) km | D6 Cenote Caves | Cenote Caves (platoon) | Cenote Ring Fort (platoon); North Branch Bunkers (two-squad); Cave Pump House (two-squad); North-east AA (two-squad) | 12 | 9/6/2 | 1 / 1 | 745 | Cenote Caves |
| 7 North-west Groves | 4 | 3, 4 | (3.2, 9.0) km | - | Spore Works North (platoon) | Root Cellar Maze (two-squad); North Ridge Fort (platoon); Grove Battery (two-squad); North-west AA (two-squad) | 12 | 9/6/2 | 1 / 1 | 745 | Spore Works North |
| 8 The Spore Citadel | 4 | 6, 7 | (9.6, 12.4) km | D2 Spore Citadel | Spore Citadel (platoon) | Culture Vat Halls (platoon); Citadel Gate Wall (two-squad); Citadel Battery (two-squad); Generator Cap (two-squad) | 12 | 9/6/2 | 1 / 1 | 745 | end of run |
<!-- AUTO-OPTABLE END -->

All 8 ops pass the per-op checks (12 supporting each, a planned garrison of 745-805 if all filled). See `tools/out/checks.txt`.

**Choice:** ops 2 (east canal) and 3 (west ridge) can run in either order. Op 4 follows 1 or 3, op 5 follows 2 or 4, op 6 follows 4 or 5, op 7 follows 3 or 4, and op 8 follows 6 or 7.

## Water and the AI (MEASURED on the sketch)
- **The sites fall on 9 separate landmasses.** The sloughs (about -0.4 to -0.6 m) cut the shelf into pieces:
  - the main west-and-centre landmass carries 89 sites, joined across the main slough by the Titan berm;
  - the east canal side carries 22 sites and the north-east 14;
  - six small hammocks carry 2-4 sites each.
- **AI never crosses water,** so each landmass holds its own garrison, and its reserves spawn on it.
- **Stage B fix (ASSUMED):** raised hammock trails, a few dry ground ridges in the grass, can join the east side to the centre where Miran wants AI counterattacks to move.
- **No water sites** (no stilt decks).
- **Republic players:** Arma boats on the boat channel (-1.8 m) and the south lake. Wading the sloughs is slow but allowed.
- **Hovers are not relied on anywhere** (REV2 rule 9).

## Coverage
All 16 squares carry sites, with 2-18 per square. The thinnest is D1, the south-east grass and canal start, at 2 sites. See COVERAGE.md.

## Recon
Every draw, final and main is seen from 1 km or more on at least 17 of 24 bearings in the terrain-only screening. The open grass makes this the easiest concept to read from far away. Giant flora must keep sight corridors open to the draws.

## Fog
Bright low haze over the grass is a mood choice for missions. It is not used to hide weak terrain.

## Why it's distinct from Blackfen
It differs on all five counts:
1. **Palette:** bright and warm.
2. **Vegetation:** sawgrass and giant flora.
3. **Water:** sheet-flow sloughs.
4. **Set piece:** the Titan berm.
5. **Op flow:** hammock-hopping with east and west choices.

## Open points
- **There is no fungal kit** (REV2). The giant flora would come from scaled Gliese plants, Rugosa coral and alien brush. Can that read as Felucia? This is the biggest look risk of the three concepts.
- **Grass and AI sight** need a test (Stage A RISKS B1).
- **Nine landmasses** mean more separate garrisons. Decide in Stage B where hammock trails should join them.
