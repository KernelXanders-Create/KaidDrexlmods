# Op 6: Prophet Massif and Signal Isle, ground plan notes, v2 (Kernel, PROPOSED)

**One rule fails: rule 3 ("one connected net per island for sites with a vehicle approach").** Two parts:
1. **The massif's net does not reach op 4's net** (Causeway Foot) within the rules.
   - **The best road:** 2,895 m, from the Prophet Road Checkpoint (6-02, 304 m) down to op 4's road from 4-08 to Causeway Foot (62 m). It holds 14 % everywhere.
   - **Where it breaks:** cut/fill reaches 5.01 m at 7 grid points, between 137 m and 719 m along it.
   - **What it needs:** a cutting or retaining wall over that stretch, taking 1.0 m off the worst point, or a ramp there. The road is in `op6_plan.json` → `links_to_existing_net` (points and levels), and marked GAP on the plan.
   - **v1's link was not real either.** It came off op 4's East Slope Comms (4-10), which has no road in op 4 v2, and it held 14 % only on average.
2. **Four Ember Crescent sites with a vehicle approach have no road:** 6-M3 North Point Ferry Pens, 6-07 North Point Pillboxes, 6-04 Prophet Limestone Quarry and 6-14 Upper Spring Outpost. At a true 14 %, no road from the net to them holds 4 m. They have foot paths (below).

Everything else passes (`op6_checks.json`, and `tools/verify.py` measured your way):
- grades: 0 of 8 roads over 14 %;
- pads: every pad within 4 m. The monastery (6-F) is at 3.99 m, the closest to the cap.

## Item 11: the coastal works and their shores
Each coastal work stands on a cliff above the water. Measured from the pad edge facing the water to the last dry point before it:

| Site | Pad level | Drop to the water's edge | Horizontal run | Link | Pier at |
|---|---|---|---|---|---|
| 6-M3 North Point Ferry Pens | 221.0 m | 216 m | 346 m | lift | (15420, 12645) |
| 6-07 North Point Pillboxes | 240.8 m | 238 m | 425 m | lift | (16890, 12245) |
| 6-13 Kamar Landers | 158.8 m | 158 m | 364 m | lift | (16825, 10025) |
| 6-M2 Kamar Strand Bunker Line | 141.3 m | 140 m | 366 m | lift | (17220, 10915) |
| 6-05 Kamar Refuelling Base | 150.3 m | 149 m | 313 m | lift | (16910, 10060) |
| 6-08 Signal Isle Landing | 229.8 m | 226 m | 316 m | lift | (16680, 15350) |
| 6-11 North Cape AA | 274.0 m | 273 m | 536 m | lift | (17345, 17435) |
| 6-10 Kalam Rock Chapel | 2.5 m | 1.9 m | 11 m | stair | (18335, 16530) |

- **Each link** is a pier at the water (ASSUMED 30 x 8 m deck at +1.5 m, its outer end in at least 2 m of water) and a lift up the cliff face (ASSUMED 6 x 6 m shaft and head house), with a service stair beside it. A path runs from the pad edge to the lift head over the horizontal run.
- **Where the lift stands:** the plan gives the pad edge (top), the cliff foot (foot) and the pier. It does not place the lift on the cliff face to the metre; that is a pick on the real cliff.
- **My view:**
  - **Lift is right:** the ferry pens' and the Signal Isle Landing's purpose is the boat link, so a 216-226 m lift is what they need.
  - **No link needed:** the AA (6-11) and the pillboxes (6-07) are cliff-top works and could do without one.
  - **Lift or move:** the Kamar Strand works (6-M2, 6-05, 6-13) are 140-158 m up. They are better moved down to the strand if you can cut a shelf there, since nothing at the water's edge holds their pads within 4 m on this ground.
- `op6_plan.json` → `shore_links` has each top, foot and pier point.

## Kamar Village (job 2)
- **Road join:** the north lane's east end, (16728, 11784). Its road edge keeps 15.3 m from the nearest house wall (your grader's footprints, no exemption).
- **Unchanged from v1:** the garrison, the squad positions and the quay path.

## Your built sizes (item 6)
- **6-M4 Signal Ridge Comms:** now your built 1-13 pad (CIS Communications FOB), 88 x 104 m, at 320 m.
- **6-09 Signal Isle Depot:** your built CIS Depot pad (1-06, 134 x 248 m) holds 4 m nowhere within 720 m on Signal Isle. It keeps 80 x 60 m, which needs a trimmed composition.

## Foot paths for the unreached sites
| Site | To road | Straight | Rise |
|---|---|---|---|
| 6-M3 | 6-02 to 6-F | 783 m | 130 m |
| 6-04 | 6-02 to 6-F | 618 m | 134 m |
| 6-07 | 6-01 to 6-03 | 82 m | 7 m down (a short path) |
| 6-14 | 6-02 to 6-F | 244 m | 50 m |

## Roads
- **Size:** 8 dirt roads (7 m), 7.4 km, all on the massif, grown from the monastery.
- **Measured on the handed-over points:** grade at most 13.8 %. Cut/fill at most 3.89 m. Longest straight 81 m. Nothing within 3 m of a road edge (closest pad 16.5 m; closest house wall 15.3 m).
- **Junction steps:** 0, except where the bunker line's road (6-M2) meets the landers' road (6-13), at 0.66 m. That step came from a road added later; I report it.
- **Moves** are from the design point. The largest are 6-08 (990 m), 6-14 (781 m), 6-11 (683 m), 6-07 (630 m), 6-M3 (614 m), 6-F-T (555 m) and 6-03 (530 m). The reasons are as in v1.
