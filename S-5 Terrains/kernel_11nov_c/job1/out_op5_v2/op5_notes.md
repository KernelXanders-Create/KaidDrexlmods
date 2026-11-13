# Op 5: Acropolis Isle, ground plan notes, v2 (Kernel, PROPOSED)

**No rule fails in this plan (`op5_checks.json`: every rule PASS).** As in v1, the rule-3 pass rests on one reading: the purpose map gives no op 5 site a vehicle approach. So the three sites without a road (5-M2 Sea Cave Pens, 5-03 North Cape Battery, 5-04 Monastery Ledge) are reached by stair.

**Re-pass (your 12 Nov sheet):**
- **Item 1 (grades):** every road holds 14 % between each pair of points and over every 10 m and 20 m. `tools/verify.py`: 0 of 10 roads over (v1: 7 of 10).
- **Item 5 (pads):** counted to the corners. The worst is 3.62 m (5-02), and every pad agrees with `verify.py`.
- **Item 7 (Kastro Quay's houses):** measured from your grader's wall footprints, with no exemption. The nearest road edge is now 22 m from a house wall; in v1 it came within 0.5-0.9 m.
- **Item 9 (joins):** every junction step is 0.
- **Item 12 (moves):** from the design point.

## Kastro Quay: how the roads meet the town (job 2)
- **Where they come in:** both roads to the town, from the Ridge Power Station (5-05) and the East Bay Landers (5-14), come in at the north end of the main street M.
- **The extension:** each road stops 15 m out on M's own line, and those 15 m are M extended, at M's end level, 120.5 m. That is Kastro Quay street work.
  - It runs from (4600, 17040) to (4599, 17055).
  - The ground under it changes by at most 0.99 m.
- **Why:** roads keep off the town's outline and every house wall, and a street end inside the town cannot be reached by a 7 m road without passing its own row houses. This is the same answer as Perys in the ops 1-2 re-pass.
- **The other street ends:** B1 north (v1's join), M south, W south and N1 east are all offered as join points. M north gave the roads that hold every rule.
- **Garrison, squad positions and quay:** as in v1. 25 of 34 houses; A5-06, A5-08 and A5-07 guard its approaches; the quay apron is in the cove, below the cargo lift.
- **The purpose-map point vs the layout:** as in v1, 385 m apart. I'd keep the layout.

## The three things I am least sure of
1. **Kastro Quay's port still has no road to the sea** (as in v1). The quay is reached by lift. The Quay Fuel Depot (5-06) stays up the slope at 228 m, 559 m from its point.
2. **Three sites have no road,** joined by stairs:

   | Site | Bottom | Top (on road 5-08 to 5-F or 5-12 to 5-F) | Straight | Rise |
   |---|---|---|---|---|
   | 5-M2 Sea Cave Pens | (2300, 16100, 23) | (2042, 16631, 294.5) | 591 m | 272 m |
   | 5-03 North Cape Battery | (2900, 18540, 46.5) | (2286, 17548, 348.3) | 1167 m | 302 m |
   | 5-04 Monastery Ledge | (1690, 18230, 54.5) | (2286, 17548, 348.3) | 906 m | 294 m |

3. **Your built sizes (item 6):**
   - **5-02 West Cliff AA** (CIS Medium AA Base): your built 2-M3 pad (197 x 193 m) holds 4 m nowhere within 840 m. It keeps my 120 x 110 m, which needs a trimmed composition.
   - **5-13 Sensor Stack** (CIS Comms Array): your built pad does not fit the stack top. It keeps 30 x 30 m (air only).

## Roads
- **Size:** 10 dirt roads (7 m), 9.4 km. That is shorter than v1 (12.9 km): with the town's street ends offered, the net starts at M's north end.
- **Measured on the handed-over points:** grade at most 13.9 %. Cut/fill at most 4.0 m (5-05 to the town). Longest straight 126 m. Nothing within 3 m of a road edge (closest pad 14.3 m; closest house wall 22.4 m). Junction steps 0.
- **Pads:** the worst ground change is 3.62 m (5-02). Squad positions stand 126-676 m from their nearest site.

## Moves (from the purpose map's point)
| Site | Moved |
|---|---|
| 5-02 | 561 m |
| 5-06 | 559 m |
| 5-04 | 294 m |
| 5-14 | 117 m |
| 5-M1 | 91 m |
| 5-03 | 90 m |
| 5-05 | 82 m |
| others | 0-22 m |

The reasons are as in v1.
