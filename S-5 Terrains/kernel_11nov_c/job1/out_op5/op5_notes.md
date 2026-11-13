# Op 5: Acropolis Isle, ground plan notes (Kernel, PROPOSED)

**No rule fails in this plan (`op5_checks.json`: every rule PASS; junction steps are reported).** As in op 3, the rule-3 pass depends on one reading of the rule:
- three Acropolis sites have no road and are reached on foot or by boat: 5-M2 Sea Cave Pens, 5-03 North Cape Battery and 5-04 Monastery Ledge;
- the purpose map gives no op 5 site a vehicle approach.

## The three things I am least sure of
1. **Kastro Quay's port has no road to the sea.**
   - The town (K6 v2) sits on the 115-140 m cliff-top plateau. Its quay is a 30 x 20 m apron at 2 m in the cove, linked by a cargo lift and a stair (pieces, at about (4672, 16808) to (4788, 16806)).
   - So the op's FOB unloads boats by lift.
   - **5-06 Quay Fuel Depot moved 559 m, up the slope north-west of the town (228 m), above the plateau.** The purpose map's point is on the cliff face at about 105 m, and no 87 x 65 m pad holds 4 m anywhere near the cove. Fuel for the boats would have to go down by the lift or a pipe.
   - If you want the depot at the water, it needs a cut shelf in the cliff (a terrain change), or it becomes the quay apron's own fuel point (a few tanks, not the composition).
2. **Three sites can't have a road, and the North Cape Battery sits low.**
   - **5-M2 Sea Cave Pens:** an apron at the cave mouth (23 m).
   - **5-03 North Cape Battery:** on a shelf at 46.5 m, 90 m from its point. The point itself (92 m) is on a slope too broken for a pad. From the shelf the guns cover the north sea, but they see the citadel's back slope from below, not from above.
   - **5-04 Monastery Ledge:** a cliff ledge at 54.5 m, 294 m from its point (the point's ground is broken). A cliff monastery fits there.
   - Each is under 270-300 m of steep ground that no 7 m road holds at 14 % with 4 m cut / fill, so each has a stair (below).
3. **The router was loosened for this island, and the roads are long.** Acropolis Isle's flanks are steeper than ops 3-4 (30-45 % over most of the island).
   - **Settings, set in `op5.py`:** I raised the router's band filter from 7.6 to 10 m, and its step limit from 0.8 to 1.0 of the grade. These only steer the search; the rules did not change.
   - **What still holds:** every road is held to 14 % and 4 m cut / fill and measured (worst 3.9 m).
   - **The cost:** long switchbacks. The town-to-power-station road is 3.1 km for a 118 m climb; the whole net is 12.9 km.
   - Without the change, the plateau under Kastro Quay is cut off from the rest of the island.

## Kastro Quay: the town and the purpose map's point (job 2, shown on the plan)
- **Where each is:**
  - **purpose map:** (4200, 16850), at 241 m, on the ridge's east flank;
  - **K6 v2 layout:** centre (4584, 16813), on the cliff-top plateau over the cove;
  - **offset:** 385 m (MEASURED; the pack's start note says about 300 m).
- **I'd keep the layout.**
  - The plateau is the only flat ground near the cove (blocks 115-140 m, level runs), and the cove is the only harbour on the east coast.
  - The purpose map's point is on a 30 % flank with no harbour below it.
  - The site's links (5-05 power station, 5-06 fuel, 5-14 landers) are all reached by road from the layout as it stands.
- **Road join:** street B1's north end, the town's west edge, at (4488, 16752), 108.25 m.
  - The road from the power station (5-05) comes in from the north-west, heading 146° on its last 25 m.
  - Its last 25 m meet the town's own street, and it keeps at least 24 m from any building centre beyond that.
  - The south road port in the layout (main street, 132.75 m) is above the 17 % climb the K6 notes left to me: a road to it ran through the town's west block, so I moved the join to B1.
- **Garrison:** 25 of the town's 34 buildings, against the op's other platoon sites (the citadel and the sea caves, both P).
- **Squad positions guarding it:**
  - A5-06, on the road to the power station;
  - A5-08, on the road north toward the fuel depot and the bay;
  - A5-07, over the east bay beach and the landers.
- **Shore / quay:** the quay apron in the cove (2 m), then the lift. The two east-bay beaches (247 m and 231 m) are 700-1,000 m north.

## Lantern Quay Hamlet (job 2)
- **Purpose map:** (7400, 16650). **Layout centre:** (7391, 16512). They are 138 m apart; I'd keep the layout (the quay row is on the real shore).
- **No road:** the hamlet is foot-only, and the purpose map says the AI cannot leave Lantern Rock.
- **Foot paths:** the beacon (5-M4, 126 m) is 487 m from the top terrace's east end (7533, 16542, 91.25 m), with a climb of 35 m.
- **Garrison:** 33 of its 51 buildings.
- **Squad positions:** A5-09 over the landing and the hamlet stair; A5-10 over the Lantern channel.
- **Shore / quay:** its own quay row at 3-6 m. Also beaches of 111 m on the rock's south-west side, and 118 m and 85 m on its north-east side.

## Moved, resized or merged sites
| Site | Moved | Why |
|---|---|---|
| 5-02 West Cliff AA | 561 m, up the west slope to 240 m | **Pad reduced to 120 x 110 m:** the composition's known pad (2-M3) is 197 x 193 m, and no seat for it holds 4 m on the west cliffs. The smaller pad fits only up the slope; from 240 m it still covers the western sea (the worst pad change in the op, 3.62 m). |
| 5-06 Quay Fuel Depot | 559 m | Item 1 above. |
| 5-04 Monastery Ledge | 294 m | Item 2 above. |
| 5-14 East Bay Landers | 112 m | To ground behind the bay beach (106 m; a beach work). |
| 5-03 North Cape Battery | 90 m | Item 2 above. |
| 5-M1 Windmill Ridge | 80 m | Along the spine. The Lessu windmills are dressing strung along the spine either side of the Flak Crown pad. |
| 5-05, 5-01, 5-08 | 20-32 m | Small seats. |
| 5-13 Kastro Strait Sensor Stack | 0 m | **Reduced to 30 x 30 m:** the stack top takes no more, so it holds the array's mast and a ring of guns, not the whole Comms Array (40 x 93 m). Air only. |

## Composition sizes
- **KNOWN** (same composition in your op 1-2 pads): 5-M1 (Flak Crown), 5-01, 5-03, 5-06, 5-07 (2-04, here seated level), 5-14.
- **Reduced:** 5-02, 5-13 (above).
- **ASSUMED:** 5-F, 5-M2, 5-M4, 5-04, 5-05, 5-08, 5-10, 5-11, 5-12. The basis for each is `size_note` in `op5_plan.json`.
- **5-F Acropolis Citadel:** 160 x 160 m at 369 m, holding within 3.18 m. It is a little over the CIS Small Citadel, to take Le Temple 2 inside the walls.

## Foot links (stairs or paths, not graded ground): top and bottom points
| Site | Bottom (x, y, z) | Top (x, y, z) | Straight | Rise |
|---|---|---|---|---|
| 5-M2 Sea Cave Pens | 2300, 16100, 23 | 2042, 16631, 294.5 (road 5-08 to 5-F) | 591 m | 272 m |
| 5-03 North Cape Battery | 2900, 18540, 46.5 | 3008, 17554, 348 (road 5-F to 5-07) | 992 m | 301 m |
| 5-04 Monastery Ledge | 1690, 18230, 54.5 | 2343, 17589, 348 (road 5-12 to 5-F) | 915 m | 294 m |
| 5-M4 Lantern Rock Beacon | 7700, 17000, 126 | 7533, 16542, 91 (Lantern Quay's top terrace) | 487 m | 35 m down |

**Catalogue piece:** as for op 3, the 10 Nov catalogue has no stair or ramp piece, so I can't name one. The three Acropolis stairs are zig-zags of about 270-300 m rise. The beacon path is a graded footpath (about 7 %), so it needs no piece.

## Approaches (two per main and the final)
- **5-F Acropolis Citadel:**
  - up the road from Kastro Quay, past the power station, Windmill Ridge and the Citadel Gate (5-07);
  - the covered climb from the south-west, past the Olive Terraces Post (5-08) onto the summit's west side.
- **5-M1 Windmill Ridge:**
  - from the pumice south beach, past the bunker line (5-01) and up the spine;
  - along the ridge road from the power station (5-05).
- **5-M2 Sea Cave Pens:**
  - by boat across the Kastro Strait into the cave mouth;
  - from above, down the stair from the Olive Terraces road.
- **5-M3 Kastro Quay:**
  - by boat to the quay apron in the cove, then the lift and stair;
  - overland from the East Bay Landers (5-14), or along the road from the power station.
- **5-M4 Lantern Rock Beacon:**
  - by boat to Lantern Quay, then up the hamlet stairs and the path;
  - by boat or air to the rock's north-east beaches (118 m and 85 m), then up the slope on foot.

## Squad-size positions (10)
| Position | Covers | Height |
|---|---|---|
| A5-01 | the pumice south beach below the bunker line | 183 m |
| A5-02 | the sea-cave mouths and the strait crossing | 3.5 m, a shore work, 12.6 m from the +0.3 m line |
| A5-03 | the west coast landing below the West Cliff AA | 248 m |
| A5-04 | the north back slope between the gun park and the cape battery | 94 m |
| A5-05 | the air over the acropolis (AA platform) | 339 m |
| A5-06 | the road from Kastro Quay to the power station | 210 m |
| A5-07 | the east bay beach and the landers | 68 m |
| A5-08 | the road north of Kastro Quay | 293 m |
| A5-09 | Lantern Quay's landing and the hamlet stair | 88 m |
| A5-10 | the Lantern channel and the head of the Coral Shelf | 159 m |

They stand 126-668 m from their nearest site.

## Shores a boat can land on
There are 24 stretches (MEASURED on the 5 m grid). The longest:
- the two east-bay beaches below the landers, 247 m and 231 m;
- the north shore, 161 m;
- the south-west point, 157 m;
- Lantern Rock: 118 m on the north-east and 111 m on the south-west.

**Sea works** (no shore needed; boat only):
- 5-10 and 5-11 on the Coral Shelf banks (4.25 m and 3.75 m);
- 5-13 on its stack (27.5 m; air only).

## Roads
- **Size:** one net on Acropolis Isle, grown from Kastro Quay. 10 dirt roads (7 m), 12.9 km in all, reaching 10 of 13 Acropolis sites and the town.
- **None** on Lantern Rock, the Coral Shelf or the stack.
- **Measured:** grade at most 14.0 %. Cut/fill at most 3.9 m over every grid point a road fixes. Longest straight 112 m. Nothing within 3 m of a road edge (closest pad 8.9 m; closest town building centre 23.8 m).
- **Junction steps (reported):** up to 2.14 m (5-14 joining the town road). The rest are 0.3-2.05 m.
- **No main roads:** there are no vehicle approaches in op 5 to need one. The climbs need 14 %.
