# Op 8: The Caldera Yard, ground plan notes (Kernel, PROPOSED)

**One rule fails: rule 3 ("one connected net per island"). Ember Crescent has two road nets, and the Yard is on the one the AI road net does not reach.**
- **The arm net:** the south arm, Akrotar and the rim. It is joined to op 4's net at Causeway Foot (and through it to ops 6 and 7).
- **The inner shore net:** the Yard (8-F), the Dry Dock Pump House (8-12), the Inner Shore Road Gate (8-10), the Crater Wall Depot (8-04) and the Inner Shore Fuel Quay (8-03), on the strip of shore inside the crater.

**Why:** an inner cliff of 20-110 m runs right round the lagoon, and no 7 m road holds 14 % with 4 m cut / fill anywhere along it. Its side slopes run over 60 %, even with the router loosened as far as the rules allow (below).
- **The lowest step (MEASURED, marked GAP on the plan):** 19.4 m, between the inner shore at (10005, 8305), 10 m, and the south arm at (9650, 8315), 29.5 m. That is 355 m apart, about 5.5 % on average, but broken ground between them.
- **A ramp there joins the two nets** and makes the purpose map's "inner shore road from the south into the Yard" real. Until then, vehicles reach the Yard only by water.
- **Op 7 is on the same strip:** its Skaros Rock Keep (7-M1, op 7's failing site) is on this inner shore, about 1.6 km north of the Yard. An inner shore road from the Yard to Skaros, plus this one ramp, would clear the rule-3 failure in both ops.

Every other rule passes (`op8_checks.json`), and every Ember Crescent site is on one of the two nets.

## The three things I am least sure of
1. **The gap above.** I did not change terrain outside the rules. The ramp needs your hand.
2. **The Yard's size, and the dam.**
   - **The Yard:** your build-4 ground already has the Yard's shelf, a flat at exactly 3.5 m, 298 x 450 m across (101,600 m², MEASURED), but not rectangular. The largest pad that holds 4 m on it is 240 x 340 m (yaw 15°, level 3.0 m, 2.21 m of change), against the purpose map's "about 400 x 300 m". The Rim Foundry and the capstone sit inside it.
   - **The Breach Dam:** not a pad. It spans the breach at its narrowest (MEASURED): 354 m across water 41 m deep, from Ash Crescent's south tip at (9015, 8820) to the south arm at (9265, 8570). It is drawn as the dam line.
   - **The dam's gate house** (8-M1, the CIS Fortress Dam's ground works, an ASSUMED 80 x 60 m) stands at the east end on a 23 m bench, 160 m south of the span's end. So the crest road needs a 160 m approach from the span to the bastion.
   - **Ash Crescent has no road** (its sites are foot and boat in the purpose map). So the dam's crest road, "the only AI link between the two crescents", ends at Ash's south tip.
3. **Router settings and long roads.** The south arm's tip is broken ground. For op 8 I loosened:
   - the router's band filter to 14 m;
   - its side-slope limit to 0.6;
   - its cliff margin to 5 m.

   These only steer the search; every road is still measured at 14 % and 4 m (worst 3.66 m). Even so, two roads are long:
   - the Yard Power Plant on the rim (8-M4, 342 m) is joined by a 4.5 km road climbing from op 4's net at Causeway Foot;
   - the dam's east end, by a 2.0 km road from the South Crest AA.

## Moved, resized or added sites
| Site | Moved | Why |
|---|---|---|
| 8-08 South Arm Road Tower | 388 m | Onto the arm's outer slope at 33 m, beside the road from Causeway Foot. |
| 8-09 Akrotar Cape AA | 277 m | The full KNOWN pad (197 x 193 m) fits on the cape at 19 m. |
| 8-16 Ash Outer Depot | 177 m | To 60.5 m, above Ash's west beach. |
| 8-M1 Breach Dam gate house | 160 m | Item 2. |
| 8-01 Dam West Tower | 108 m | On Ash's south tip at 180 m, over the dam's west end. |
| 8-03 Inner Shore Fuel Quay | 0 m | **Pad reduced to 160 x 120 m:** the CIS Large Fuel Depot's own pad is 248 x 261 m, and the inner shore takes no more. |
| 8-14-T Akrotar Dig, temple | added | The Temple Run dig is its own pad beside the Elevated Ramp Depot's sheds (8-14). |
| others | 0-64 m | — |

## Composition sizes
- **KNOWN** (same composition in your op 1-2 pads): 8-02 (as built), 8-08, 8-09, 8-10, 8-12 (82 x 65 m), 8-15, 8-16.
- **MEASURED ground:** 8-F (item 2).
- **Reduced:** 8-03 (above).
- **ASSUMED:** 8-M1, 8-M2, 8-M3, 8-M4, 8-01, 8-04, 8-05, 8-13, 8-14, 8-14-T. The basis for each is `size_note` in `op8_plan.json`.

## Approaches (two per main and the final)
- **8-F Caldera Yard:**
  - down the Skala path from the Rim Chora (op 7), on foot;
  - by boat across the lagoon once the dam gate opens.
  - The inner shore road from the south, through the Inner Shore Road Gate (8-10), only becomes a vehicle approach once the GAP ramp is built.
- **8-M1 Breach Dam:**
  - along the south arm road to the dam's east end (vehicles);
  - from Ash Crescent's south tip across the dam crest, on foot, or by boat to either end.
- **8-M2 Kameni Shield Generator** (104.5 m; Kameni has no road):
  - by boat to Kameni's north landing past the Vent Bunkers (8-05);
  - by boat to Kameni's south shores (547 m and 503 m, the longest in the op's lagoon).
- **8-M3 South Arm Gun Line:**
  - along the south arm road from Causeway Foot past the road tower (8-08) (vehicles);
  - up from the inner shore fuel quay (8-03), on foot.
- **8-M4 Yard Power Plant:**
  - by the 4.5 km road from op 4's net (vehicles);
  - up the cliff from the Dry Dock Pump House (8-12), on foot.

## Squad-size positions (10)
| Position | Covers | Height / note |
|---|---|---|
| A8-01 | the south arm road from Causeway Foot | |
| A8-02 | the inner shore road between the fuel quay and the depot | 2.3 m, on the inner shore |
| A8-03 | the air over the Yard, from the rim | 350 m |
| A8-04 | the inner shore north of the road gate and the Yard's south end | 3.3 m, 15.2 m from the +0.3 m line |
| A8-05 | the dam's east end | |
| A8-06 | the south crest between the AA and the gun line | |
| A8-07 | Akrotar's beaches | |
| A8-08 | Kameni's south shore | |
| A8-09 | the dam's west end on Ash Crescent | |
| A8-10 | Ash Crescent's west beach | |

They stand 211-849 m from their nearest site.

## Shores a boat can land on
There are 11 stretches (MEASURED on the 5 m grid):
- the south arm's outer coast below Causeway Foot, 1,887 m;
- Kameni: 547 m and 503 m on the south, 148 m on the east, 80 m on the west;
- Akrotar: 172 m and 52 m;
- Ash Crescent: 151 m and 53 m on the lagoon side.

The Yard and the inner shore quays are harbour works on the lagoon, not beaches.

## Roads
- **Size:** 13 dirt roads (7 m), 14.5 km in all.
  - **The arm net:** 9 roads, joined to op 4's roads (`4-09-4-07` and `4-07-4-M3`) at Causeway Foot.
  - **The inner shore net:** 4 roads, from the Yard south to the fuel quay.
- **None** on Kameni or Ash Crescent.
- **Measured:** grade at most 14.0 %. Cut/fill at most 3.66 m over every grid point a road fixes. Longest straight 116 m. Nothing within 3 m of a road edge (closest pad 9.3 m).
- **Junction steps (reported):** up to 2.05 m, where the road tower's road meets op 4's road.
- **Pads:** the worst ground change is 3.54 m (A8-10). Every other pad is under 3.5 m.
- **No main roads:** the climbs need 14 %.
