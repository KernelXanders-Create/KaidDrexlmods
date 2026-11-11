# Op 4: Cinder Road, ground plan notes (Kernel, PROPOSED)

**No rule fails in this plan (`op4_checks.json`: every rule PASS; junction steps are reported), but the AI road cannot run through, as the purpose map wants.** On today's ground it breaks at two terrain steps that no road within your rules can climb:
1. **The south causeway head:** the 60 m wide causeway at 3.5 m meets the Terrace bench at 21-27 m within about 90 m (22 %), with no room on the strip for switchbacks. So op 4's net does not join op 2's net. (Marked GAP on the plan, at 15845, 4060.)
2. **The north causeway's cone end:** the causeway at 3.5 m meets the cone's north-west foot, which rises about 45 m within 100 m (44 %), and the cone's north shore has no low shelf to go round. So the cone and the north causeway are not joined by road. (GAP at 15720, 7845.)

Within each island the nets are connected and every vehicle site is on one:
- **Cinder Cone, Mole Rock and the south causeway:** the trunk over the south causeway, through the Mole Rock Gate and up to the fort, plus all cone sites.
- **Ember Crescent and the north causeway:** the trunk over the north causeway into Causeway Foot, plus 4-01, 4-07, 4-09, 4-08 and 4-10.

**To make the purpose map's single road** ("the fort is the gate of the only vehicle road onto Ember Crescent") work, both steps need your ramps, or a terrain change at the two causeway ends. I did not make terrain changes outside the rules.

## The three things I am least sure of
1. **The two gaps above.** Ramps at the causeway ends are the fix I'd suggest. Rule 3 passes because each island's net is whole, but the purpose map's intent (vehicles from the Airfield FARP to Ember Crescent) is not met until they're built.
2. **The fort is on the crater's west rim (127.5 m), not on the crater floor (106 m).**
   - The crater's inner wall falls 20-25 m at 30-58 %, so no road can reach the floor within the rules. The fort's 120 x 120 m pad on the rim holds within 1.72 m, and the crater floor becomes its inner yard.
   - The fort is the trunk's last stop on the cone. It could only be a through-gate again once the north gap is ramped.
   - Its size is ASSUMED: no pad of "CIS Flower Fortress with GPs" exists.
3. **All roads are 7 m dirt, not 10 m main.**
   - Mole Rock is a 30 m islet that the causeway crosses at sea level on both sides (22 m up and 26 m down within about 200 m), and the cone climb is 3.5 m to 127.5 m. Both need 14 %; a 10 % main road would need terrain cuts.
   - Your op 2 net is dirt too. Causeway Foot's own 8 m main street starts where the trunk ends.

## Moved or resized sites
| Site | Moved | Why |
|---|---|---|
| 4-03 Lava Flow Trench | 253 m, to the west rim (131 m) | The west flank's lava ribs are too steep for a road. From the rim it still overlooks the north causeway. |
| 4-11 Steam Vent Bores | 219 m, to the north-east skirt (27 m) beside the landers | The north-west skirt has no road access. **Pad reduced to 120 x 100 m:** the composition's known pad (2-14) is 192 x 166 m and does not fit anywhere on the north skirt within 4 m. |
| 4-06 Flat Pillboxes | 275 m | Moved along the south causeway to its cone end: the bank south of it is in the trunk's way. |
| 4-M4 Skerry AA Platform | 190 m | To flat ground on the skerry. |
| 4-M2-T Cone Flank Batteries tower | 166 m | The artillery base and the tower are two pads of one main, 400 m apart. |
| 4-12 Black Beach Landers | 133 m | A beach work, may come to the water's edge. |
| 4-10 East Slope Comms | 128 m | — |
| 4-07 | 71 m | — |
| 4-08 | 64 m | — |
| 4-02 | 50 m | — |
| 4-09 | 32 m | — |
| 4-04 | 28 m | — |

## Composition sizes
- **KNOWN** (same composition in your op 1-2 pads): 4-M1, 4-M2-T, 4-M4, 4-03, 4-07, 4-10.
- **KNOWN as built:** 4-06. Your 1-09, with the same pick, was built as a Small Rectangle FOB.
- **Reduced:** 4-11 (above).
- **ASSUMED:** 4-F, 4-M2 (artillery base), 4-01, 4-02, 4-04, 4-05, 4-08, 4-09, 4-12. The basis for each is `size_note` in `op4_plan.json`.

## Approaches (two per main and the final)
- **4-F Cinder Cone Fort:**
  - the trunk over the south causeway, through the Mole Rock Gate and up the cone's south side (vehicles);
  - from the north causeway or the north beach (the landers) up the cone's north-west side, on foot, or on the trunk once the north gap is ramped.
- **4-M1 Mole Rock Gate:**
  - along the south causeway (vehicles, on the trunk);
  - by boat to Mole Rock's shores (shores list: 506 m and 415 m north of the rock).
- **4-M2 Cone Flank Batteries:**
  - by boat to the cone's east shore;
  - along the cone's east flank road (vehicles).
- **4-M3 Causeway Foot:**
  - over the north causeway (vehicles, on the trunk);
  - by boat to the long beach south-west of the town (1.8 km), or down the slope road from the north.
- **4-M4 Skerry AA Platform:**
  - by boat to the skerry below the bunkers (4-05);
  - by air once its AA is suppressed (no LZ given).

## Squad-size positions (10)
| Position | Covers |
|---|---|
| A4-01 | the south causeway's south end |
| A4-02 | the south landfall on the cone |
| A4-03 | the cone's south-east flank |
| A4-04 | the air over the north causeway (AA platform) |
| A4-05 | the north causeway's cone end |
| A4-06 | the north causeway's town end |
| A4-07 | the north beach and the landers |
| A4-08 | the south-arm road west of Causeway Foot |
| A4-09 | the slope road above the town |
| A4-10 | the skerry channel |

They stand 112-1,124 m from their nearest site. A4-01 is 1.1 km from Mole Rock, because the causeway head has no site of its own.

## Shores a boat can land on
There are 19 stretches (MEASURED on the 5 m grid). The longest:
- the beach south-west of Causeway Foot, 1.8 km;
- both sides of the south causeway, 506, 415, 302 and 250 m;
- the cone's north beach, 280 m;
- the north causeway's sides, 111 m each.

## Roads
- **Size:** 17 dirt roads (7 m), 14.8 km in all.
- **Measured:** grade at most 14.0 %. Cut/fill at most 3.76 m over every grid point a road fixes. Longest straight 117 m. Nothing within 3 m of a road edge (closest 4.5 m).
- **Junction steps (reported):** up to 3.0 m. The worst are 4-04 joining at the fort's road (2.78 m over 300 points) and 4-11 joining at 4-04 (3.0 m).

## Job 2 note (Causeway Foot)
The trunk lands at the town's causeway end, at 1.5 m, which is the start level of the town's main street in the K6 v2 layout. The causeway deck is 3.5 m, so the last 60 m of the trunk drops 2 m. The town's other exits (south-arm road at 13849, 8133, 12.3 m; slope road at 14165, 8442, 36.7 m) carry the branches to 4-07 / 4-09 and 4-08 / 4-10.
