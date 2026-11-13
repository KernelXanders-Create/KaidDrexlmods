# Op 8: The Caldera Yard, ground plan notes, v2 (Kernel, PROPOSED)

**One rule fails: rule 3 ("one connected net per island").** Two parts:
1. **The Yard's inner-shore net is not joined to the south arm's net,** and no road between them holds the rules anywhere.
   - **The two nets:**
     - inner shore: the Yard 8-F, the Dry Dock Pump House 8-12, the Inner Shore Road Gate 8-10, the Crater Wall Depot 8-04, the Inner Shore Fuel Quay 8-03, and op 7's Skaros keep;
     - south arm: joined to op 4 v2's net at Causeway Foot.
   - **The piece it needs (item 3):**
     - **Ramp:** from the fuel quay's edge on the inner shore, (11504, 8230), 5.3 m, up to the South Arm Gun Line's edge on the arm, (11045, 7795), 136.3 m.
     - **Size:** 131 m of rise, 632 m apart in a straight line, so at 14 % it is a 936 m zig-zag ramp road, 7 m deck, with its band held within 4 m of its own cut (retaining walls where the inner cliff is steeper).
     - **Where:** it is in `op8_plan.json` → `ramps_needed`, and marked GAP on the plan.
   - **The lowest step I measured in v1** (19.4 m, between the inner shore at (10005, 8305) and the arm at (9650, 8315), near the dam) would need a far smaller ramp. But no road within the rules reaches either end: the inner shore west of the fuel quay and the arm's tip are walled by the inner cliff. So that is only the better answer if you also cut a shore road along the inner shore from the quay to it (about 1.4 km).
2. **8-M4 Yard Power Plant** (on the rim, 341.8 m) has no road. Its v1 road (4.5 km from op 4's net) held 14 % only on average; at a true 14 % none holds.

Everything else passes (`op8_checks.json`, and `tools/verify.py` measured your way):
- 0 of 13 roads over 14 %;
- every pad within 4 m (worst 3.54 m, A8-10);
- junction steps 0;
- closest pad to a road edge 9.4 m.

## Item 4: the Skaros keep's shore road (done)
- **The road:** op 7's Skaros Rock Keep (7-M1, on its 22 m ledge) is joined to the Yard by a 1,474 m shore road along the inner shore. It holds 14 % at most, with 3.89 m of cut/fill, and ends level at both ends.
- **What it does:** it puts the keep on the Yard's net. Once the item 3 ramp exists, the keep is on the AI net too, which clears op 7's rule-3 failure for the keep.

## Item 13: the Yard
- **The pad:** 240 x 340 m at 3.0 m (2.21 m of change), centre (12835, 9815), yaw 15. It sits on your 3.5 m shelf (298 x 450 m).
- **Which edge meets the water:** the lagoon is 40 m off the pad's west side (340 m long) and 50 m off its east side (MEASURED from each side's midpoint outward); the north side is 185 m from the water and the south side is on dry ground.
  - The dry dock and the two slipway gantries belong on the west side, facing the open lagoon.
  - The Rim Foundry (with the capstone inside) belongs on the south-east, against the crater wall, where the rim path and the power plant are above it.
- **Would a second, foundry pad make the Yard bigger? No, in floor area. Measured on the shelf:**
  - **one pad (this plan):** 240 x 340 m = 81,600 m², with 2.21 m of change;
  - **two pads:** a 300 x 200 m Yard at 3.5 m, which sits on the shelf with 0.03 m of change, plus a foundry pad of up to 120 x 100 m at 3.75 m north of it (the next level allowed). Together that is 72,000 m².

  The two-pad layout fits the shelf almost exactly, with the foundry as its own level. The one-pad layout gives more floor.
- **The Yard's way in:** as in v1, by the inner-shore net (8-10 Inner Shore Road Gate) and, for vehicles from the AI net, only once the item 3 ramp exists. Foot: down the Skala path from op 7. Boats: across the lagoon once the dam gate opens.

## Your built sizes (item 6)
| Site | Result |
|---|---|
| 8-09 Akrotar Cape AA | Your built Medium AA Base, 197 x 193 m, at 17 m (3.51 m of change). |
| 8-08 South Arm Road Tower | Your built Flower Tower pad. |
| 8-03 Inner Shore Fuel Quay | Your built CIS Large Fuel Depot (2-M1, 248 x 261 m) holds 4 m nowhere on the inner shore. It keeps 160 x 120 m, which needs a trimmed composition. |
| 8-04 Crater Wall Depot | Your built CIS Depot (1-06, 134 x 248 m) does not fit the inner shore either. It keeps 80 x 60 m. |

## The dam
As in v1. The span is 354 m across water 41 m deep, from (9015, 8820) to (9265, 8570). The east gate house (8-M1) is 328 m from the design point (measured from the design point now, item 12), on a 23 m bench, joined to the arm's net by a 47 m road.

## Roads
- **Size:** 13 dirt roads (7 m), 11.1 km.
  - **South arm (8 roads):** joined to op 4 v2's net at op 4's checkpoint pad (4-09).
  - **Inner shore (5 roads):** including the Skaros shore road.
- **Measured on the handed-over points:** grade at most 13.8 %. Cut/fill at most 3.89 m. Longest straight 116 m. Junction steps 0. No edits to other ops' roads.
