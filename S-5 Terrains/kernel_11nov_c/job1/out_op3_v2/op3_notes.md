# Op 3: The Sound, ground plan notes, v2 (Kernel, PROPOSED)

**No rule fails in this plan (`op3_checks.json`: every rule PASS).** As in v1, the rule-3 pass rests on one reading of the rule: the purpose map gives no op 3 site a vehicle approach, so the six sites without a road are reached on foot or by boat (item 2).

**Re-pass (your 12 Nov sheet):**
- **Grades (item 1):** every road now holds 14 % between each pair of points it hands over, and over every 10 m and 20 m along them. Measured with your method by `tools/verify.py`: 0 of 10 roads are over; the steepest is 13.9 % point to point. In v1, 8 of 11 roads were over.
- **Pads (item 5):** the planner's pad count now reaches rotated corners, and `verify.py`'s polygon count agrees with the plan on every pad. The worst is 3.93 m (3-09).
- **Joins (item 9):** no road meets another at a step. Where a road joins one this op built, that road gets a level landing there. Every junction step is 0.

## The three things I am least sure of
1. **The Sound fortress kit's sizes are still guesses.** No pad of the new kit exists and none is in your built pads. Sizes are as in v1:
   - south keep 40 x 40 m (the only size its 21 m shelf holds);
   - north keep 60 x 60 m;
   - South Notch Keep 80 x 110 m;
   - West Notch Keep 70 x 90 m.
2. **The road net now reaches 10 of 16 Sound Isle sites; six have no road.**
   - **Also in v1:** the two gate keeps (3-F, 3-F-N), the West Notch Keep (3-M2), the Cliff Galleries (3-01) and the Sound Rim Guns (3-09). Each is on a low coastal shelf under cliffs of 200-330 m.
   - **New in v2:** the North Cove Outpost (3-10, at 18 m). Its v1 road held 14 % only on average; at a true 14 %, no road down to the cove stays within 4 m.
   - All six, and Sound Head, are joined by stairs (below). If you want vehicles at the Sound, they need ramps or lifts.
3. **The roads are long switchbacks.** At a true 14 %, the climbs from the 200 m plateau to the summit (370 m) need long hairpin runs. The net is 13.0 km for 10 roads (v1: 19.8 km for 11, but steeper than it said).
   - **Where smoothing broke 4 m:** on two roads, 3-02 to 3-13 and 3-04 to 3-13, the usual corner smoothing cut the hairpins enough to leave the road over 4 m of cut. Those two are drawn with one smoothing pass instead of three, so their hairpins are tighter.

## Moves, measured from the purpose map's point (item 12)
| Site | Moved | Why |
|---|---|---|
| 3-F-N north keep | 502 m from 3-F's point | Not a move: the gate site is the south keep, and the north keep is a second pad at the north headland. |
| 3-M1 South Notch Keep | 277 m | Up the gully to 97.5 m. The point is on the shore at 2.7 m. |
| 3-09 Sound Rim Guns | 184 m | The point's ground is too broken. |
| 3-10 North Cove Outpost | 168 m | Flat ground above the cove. |
| 3-04, 3-M4, 3-F, 3-11, 3-01, 3-16, 3-12, 3-08, 3-03 | 14-64 m | Small seats. |
| 3-05 Sound Supply Slips | merged | Into Sound Head's quay, as in v1. |

Every move is now measured from your design point, not from my rough point. Where they differ, both are in `op3_plan.json` (`moved_m`, `moved_from_rough_m`).

## Composition sizes
- **KNOWN** (your built pads of the same composition): 3-03, 3-11, 3-13, 3-15, 3-16.
- **ASSUMED:** all others, with the basis in `size_note`. The planner now tries your built pad first for every composition it finds in `pads_op1` / `pads_op2`. None of op 3's assumed compositions is there.

## Foot links (stairs or paths, not graded ground)
| Site | Bottom (x, y, z) | Top (x, y, z) on road | Straight | Rise |
|---|---|---|---|---|
| 3-M3 Sound Head (gate square) | 2658, 10442, 33.0 | 2281, 10008, 380.5 (3-04 to 3-13) | 575 m | 347.5 m |
| 3-F south keep | 3900, 10785, 23.25 | 3382, 9257, 220.5 (3-12 to 3-04) | 1613 m | 197.2 m |
| 3-F-N north keep | 3500, 11160, 17.0 | 2155, 10925, 369.5 (3-M4 to 3-13) | 1366 m | 352.5 m |
| 3-M2 West Notch Keep | 660, 10000, 31.25 | 1312, 9616, 227.9 (3-02 to 3-13) | 756 m | 196.7 m |
| 3-01 Cliff Galleries | 3200, 11250, 43.25 | 2152, 10934, 369.5 (3-M4 to 3-13) | 1094 m | 326.2 m |
| 3-09 Sound Rim Guns | 3670, 11820, 25.25 | 2128, 11026, 369.5 (3-08 to 3-M4) | 1735 m | 344.2 m |
| 3-10 North Cove Outpost | 2860, 12800, 18.25 | 1969, 11418, 338.5 (3-08 to 3-M4) | 1645 m | 320.2 m |

- **The tops are the nearest road points reached over land in a straight line.** They are not the shortest stairs: v1's were shorter because v1 had roads nearer the coast.
- **The 10 Nov catalogue has no stair or ramp piece,** so I can't name one. Each link is a zig-zag stair of 200-350 m rise.

## Approaches
Unchanged from v1 (`op3.py`, and `approaches` in `op3_plan.json`). The vehicle approaches still all run on the Sound Isle net: 3-M1 by road from 3-04, and 3-M4 by road from 3-14, 3-08 and 3-13.

## Squad-size positions (10)
- **Placement:** placed as in v1, with pads now counted to their corners. The worst ground change is 3.53 m (A3-09).
- **Distance:** they stand 76-637 m from their nearest site.

## Shores a boat can land on
There are 16 stretches (MEASURED). The longest:
- Ash Crescent east, 302 m;
- east of the Sound mouth, 210 m and 100 m;
- Ash Crescent's lagoon side, 151 m;
- Sound Isle south-west, 149 m;
- the South Notch, 126 m.

## Roads
- **Size:** 10 dirt roads (7 m), 13.0 km.
  - **Sound Isle:** one net from the Sound Fuel Depot (3-13) to 3-M4, 3-14, 3-08, 3-02, 3-11, 3-04, 3-12, 3-M1 and 3-03.
  - **Ash Crescent:** 3-15 to 3-16.
- **Measured on the handed-over points:** grade at most 13.9 %. Cut/fill at most 3.97 m. Longest straight 117 m. Nothing within 3 m of a road edge (closest pad 18 m). Junction steps 0.
- **Not on any road:** no built ops 1-2 road and no town house is near this net.
