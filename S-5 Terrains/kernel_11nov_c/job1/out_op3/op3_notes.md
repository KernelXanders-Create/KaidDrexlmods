# Op 3: The Sound, ground plan notes (Kernel, PROPOSED)

**No rule fails in this plan (`op3_checks.json`: every rule PASS; junction steps are reported).** The rule-3 pass depends on one reading of the rule (item 2 below): five sites have no road and are reached on foot or by boat.

## The three things I am least sure of
1. **The Sound fortress kit's sizes are guesses.** No pad of the new kit exists, so every keep pad is ASSUMED. The final's south keep only fits as a 40 x 40 m pad, on a 21 m shelf beside the ring islet at the mouth; nothing larger fits on that headland. If the kit's keep is bigger, the south keep has to sit on the cliff top 280 m south of the mouth (at 165 m) and the gate loses its south anchor.
   - North keep: 60 x 60 m.
   - South Notch Keep: 80 x 110 m.
   - West Notch Keep: 70 x 90 m.
2. **The road net reaches 14 of 19 sites; five cannot have a road under the rules.** They are both gate keeps (3-F, 3-F-N), the West Notch Keep (3-M2), the Cliff Galleries (3-01) and the Sound Rim Guns (3-09). Each stands on a low coastal shelf under cliffs 200-330 m high, where no 7 m road holds 14 % with 4 m of cut and fill. Sound Head itself sits in a crater whose walls rise 335 m in under 500 m.
   - **My reading of rule 3:** it binds the sites with a vehicle approach. The purpose map gives no op 3 site one ("foot / boat / air" everywhere). So the reached sites form ONE net per island, and the rest are foot, boat and air.
   - If you want vehicles at the Sound, these five need ramps or lifts, not roads.
3. **Junction steps.** Where a joining road meets the net, it ends on a 16 m level landing at the junction's level, and the earlier road keeps its level. The worst steps are on 5 of 11 roads: 1.3-2.5 m over 5-38 grid points (`op3_checks.json`). Your road builder may want a short ramp there. Your town grader treats the same thing (street-street) as a report, so I did too.

## Moved sites (rough point -> final pad)
| Site | Moved | Why |
|---|---|---|
| 3-M1 South Notch Keep | 277 m | The rough point is on the shore at 2.7 m. The keep now plugs the gully higher up, at 97.5 m, where an 80 x 110 m pad holds within 2 m. |
| 3-09 Sound Rim Guns | 184 m | The rough point's ground is too broken for a 90 x 90 m pad; the nearest seat is on the north-east shelf (3.93 m of change, the worst in the op). |
| 3-10 North Cove Outpost | 168 m | It needed flat ground above the cove. |
| 3-M4, 3-04, 3-11, 3-01, 3-F, 3-16, 3-12, 3-08, 3-03, 3-F-N | 14-64 m | Small seats. |
| 3-05 Sound Supply Slips | merged | The Sound's inner shore is a 30 m strip, and Sound Head's quay already fills it. The slips are now the town quay: a 33 x 27 m apron at 3.0 m, in the K6 Sound Head layout. "Supply Outpost Version 2" needs an 82 x 65 m pad, which does not fit anywhere on the Sound's shore. |
| 3-F Sound Gate | split | The site is the south keep. The north keep (3-F-N) is a new pad at the north headland point (3500, 11160). The gate is not a pad: it spans the water between them, from (3900, 10805) to (3510, 11130), about 510 m. |

## Composition sizes (pad half-sizes)
- **KNOWN** (the same composition is in your op 1-2 pads): 3-03, 3-11, 3-13, 3-15, 3-16.
- **ASSUMED from the nearest kin:**
  - 3-M4 as the CIS Flower Tower;
  - 3-04 as the Double Checkpoint;
  - 3-14 as the Elevated Landing Pad;
  - 3-08 as twice a Comms Array;
  - 3-06, 3-07, 3-09, 3-10, 3-01 and 3-02 at the sizes in `op3_plan.json` (`size_note` on each).
- I have no composition data, so **check these against the real compositions before building.**

## Foot links (stairs or paths, not graded ground): top and bottom points
| Site | Bottom (x, y, z) | Top (x, y, z) on road | Straight | Rise |
|---|---|---|---|---|
| 3-M3 Sound Head (gate square) | 2658, 10442, 33 | 2699, 9950, 368 (road 3-12-3-13) | 494 m | 335 m |
| 3-F south keep | 3900, 10785, 23 | 2878, 9871, 350 | 1371 m | 327 m |
| 3-F-N north keep | 3500, 11160, 17 | 3059, 11690, 256 | 690 m | 239 m |
| 3-01 Cliff Galleries | 3200, 11250, 43 | 3039, 11681, 260 | 460 m | 216 m |
| 3-09 Sound Rim Guns | 3670, 11820, 25 | 3098, 11733, 243 | 578 m | 218 m |
| 3-M2 West Notch Keep | 660, 10000, 31 | 1311, 9617, 229 | 755 m | 197 m |

**Catalogue piece:** the 10 Nov catalogue has no stair or ramp piece (52 buildings, 3 walls, 1 lamp), so I can't name one. Each link needs a zig-zag stair of about 200-335 m rise. The Sound Head crater stair (335 m) is the hard one; the town is otherwise reached by boat. The K6 Sound Head stairs listed in that layout's notes are the same case: one flight per 12 m terrace step.

## Approaches (two per main and the final; no landing zones, no order)
- **3-F Sound Gate:**
  - by boat to the beach just east of the mouth (x 4140-4240, y 10840-10850), or onto the south keep's shelf;
  - from the north cove beach along the north shore shelf to the north keep, then the gate's north end.
- **3-M1 South Notch Keep:**
  - from the beach at x 3310-3430, y 7525-7565, up the coast and the gully;
  - down the Notch road from 3-04, on the net, with vehicles.
- **3-M2 West Notch Keep:**
  - from the west-coast beach at x 510, y 10675-10730, along the coast and up the gully;
  - on foot from the plateau past the Terrace Farms Post (3-02).
- **3-M3 Sound Head:**
  - by boat into the Sound to the town quay;
  - on foot down the crater stair.
- **3-M4 Summit AA:**
  - by road from the Inland Ramp Depot (3-14) and the Peak Relay Dish (3-08);
  - by road from the Sound Fuel Depot (3-13).

## Squad-size positions (10)
**Compositions:** heavy gun positions, a mixed AA platform and small checkpoints, all KNOWN sizes. What each one covers:

| Position | Covers | Height |
|---|---|---|
| A3-01 | the South Notch beach and gully mouth | 88 m |
| A3-02 | the South Cape beach and the landers (the FOB fallback) | — |
| A3-03 | the Notch road junction | — |
| A3-04 | the east beach under the Ridge Stair Tower | — |
| A3-05 | the west-coast approach to the West Notch | — |
| A3-06 | the air over the Sound head (AA platform) | — |
| A3-07 | the north cove beach | — |
| A3-08 | the north shore shelf between the galleries and the north keep | — |
| A3-09 | the Sound mouth, from the south cliff over the gate | 166 m |
| A3-10 | the Ash Crescent shore between the comms and the gun line | — |

They stand 76-637 m from their nearest site.

## Shores a boat can land on
There are 16 stretches of at least 40 m where the ground rises at most 12 % over the first 30 m inland (`op3_plan.json` -> `shores`, MEASURED on the 5 m grid). Longest:
- Ash Crescent east, 302 m;
- east of the Sound mouth, 210 m and 100 m;
- Sound Isle south-west, 149 m;
- South Notch, 126 m;
- West Notch, 55 m;
- north cove, 46 m.

The Sound Head quay is a harbour, not a beach.

## Roads
- **Size:** 11 dirt roads (7 m), 19.8 km in all.
  - Sound Isle: one net from the Sound Fuel Depot (3-13) to 3-M4, 3-14, 3-08, 3-02, 3-11, 3-10, 3-04, 3-12, 3-M1 and 3-03.
  - Ash Crescent: 3-15 to 3-16.
- **Measured:** max grade 14.0 % everywhere (switchbacks). Max cut/fill 3.98 m over every grid point a road fixes (half-width + 3.5 m). Longest straight run 126 m. Nothing within 3 m of a road edge (closest 18 m).
- **No main roads:** there are no vehicle approaches in op 3 to need one.
