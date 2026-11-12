# Op 4: Cinder Road, ground plan notes, v2 (Kernel, PROPOSED)

**One rule fails: rule 3 ("one connected net per island for sites with a vehicle approach").** Three sites with a vehicle approach have no road:
- **4-06 Flat Pillboxes:** on the south causeway at 3.25 m. Every road to it from the trunk meets the trunk at a 0.4-1.8 m step, and the strict rule (item 9) takes nothing over 0.3 m.
- **4-01 North Causeway Gun:** at 4.25 m. Roads to it break 4 m (4.3-6.2 m) or meet the net at a 0.8-1.5 m step.
- **4-10 East Slope Comms:** at 155 m. Its v1 road held 14 % only on average; at a true 14 %, every road to it breaks 4 m (4.1-9.0 m).

Everything else passes (`op4_checks.json`, and `tools/verify.py` measured your way): 0 of 16 roads over 14 %, and every pad within 4 m (worst 3.68 m).

## Item 2: the links to the airfield (your 12 Nov sheet)
**v1 was wrong to call the south link a 20 m step.** v2 starts the trunk on your built op 2 net, and both causeway ends are tried as real roads.
- **North causeway's cone end:** now a road. The trunk runs from the fort down to the north causeway (1,751 m, 13.9 % at most, 3.75 m cut/fill) and on over the causeway into Causeway Foot (1,539 m). The cone and Ember Crescent are joined by road.
- **South causeway head:** a road joins your net at the free edge of your built 2-07 pad (53.5 m). It runs 580 m to the terrace bench above the causeway, at (15830, 3690), 25.5 m.
  - **Why no road can finish it:** from there the ground falls 22 m to the causeway head at (15845, 4060), 3.5 m. On the ground: 25 m at y 3800, 11 m at y 3850, 3 m at y 3950. The causeway head is fenced by water on both sides, and no road holding 14 % and 4 m reaches it from any point on the terrace (tested from three starts, with and without the band filter).
  - **The ramp piece it needs:** 22 m of rise, at least 157 m long at 14 %, 7 m deck. Top (15830, 3690, 25.5); bottom (15845, 4060, 3.5); 370 m between them in a straight line, so the ramp can run straight down the terrace edge with room to spare. It is in `op4_plan.json` → `ramps_needed`, and marked GAP on the plan.
- **Once that ramp is built,** the AI road runs from the Airfield FARP over the south causeway, through the Mole Rock Gate, up to the fort, down to the north causeway and into Causeway Foot. That is the purpose map's single road.

## The three things I am least sure of
1. **The three unreached sites** (first lines). 4-06 and 4-01 sit beside the trunk on the causeways: a short ramp of 0.5-1.8 m where each joins would do. 4-10 needs a new seat lower on the slope, or your ramp.
2. **The south ramp** (item 2). Its foot lands on the causeway's widest part. Check it against your causeway's deck.
3. **Your built sizes moved two sites** (item 6):
   - **4-11 Steam Vent Bores** now has your built 2-14 pad, 192 x 166 m, instead of my reduced 120 x 100 m. That size fits only on the cone's north-east shoulder at 106 m, 770 m from the design point.
   - **4-M4 Skerry AA Platform** now has your built 1-04 pad, 96 x 87 m.

## What changed from v1 (the sheet's items)
- **Item 1 (grades):** held and measured point to point; 0 of 16 roads over (v1: 7 of 17).
- **Item 5 (pads):** counted to their corners. The fort (4-F, 120 x 120 m, ASSUMED) is now at 127.5 m with 1.72 m of change, on a seat that holds when counted your way.
- **Item 9 (joins):** every road ends on the earlier road's level. Where it joins a road of this op, that road gets a level landing (30-50 m) and the joining road ends on 20 m of level.
  - **One step remains:** where the 4-11 road meets the 4-03 road's band, 1.1 m over 4 grid points. The 4-03 road was added after 4-11's road was accepted, and its band touches 4-11's road there.
- **Item 12 (moves):** from the design point.
- **Built roads and pads:** your built ops 1-2 roads and pads are fixed ground in this op. The trunk starts on them.

## Moves (from the purpose map's point)
| Site | Moved | Why |
|---|---|---|
| 4-11 Steam Vent Bores | 770 m | Item 3: your built size. |
| 4-M2-T Cone Flank tower | 400 m | The second pad of a split main. |
| 4-06 Flat Pillboxes | 385 m | Onto the south causeway. |
| 4-03 Lava Flow Trench | 283 m | The west rim, as in v1. |
| 4-F Cinder Cone Fort | 214 m | The crater's west rim, as in v1. |
| 4-M4 Skerry AA Platform | 190 m | Flat ground on the skerry. |
| 4-10 East Slope Comms | 128 m | — |
| others | 0-71 m | — |

## Composition sizes
- **KNOWN (built):** 4-11 (2-14), 4-M4 (1-04).
- **KNOWN:** 4-M1, 4-M2-T, 4-03, 4-07, 4-10, and 4-06 as built.
- **ASSUMED:** 4-F, 4-M2, 4-01, 4-02, 4-04, 4-05, 4-08, 4-09, 4-12, with the basis in `size_note`. None of these compositions is in your built pads.

## Causeway Foot (job 2)
- **Road join:** the trunk ends at the town's causeway end, (14300, 8176), 1.5 m. Its road edge stays at least 13 m from any house wall (your grader's footprints).
- **Other branches:** 4-07, 4-09 and 4-08 join through the town's other exits, as in v1.

## Roads
- **Size:** 16 dirt roads (7 m), 12.5 km.
- **Measured on the handed-over points:** grade at most 13.9 %. Cut/fill at most 4.0 m (the fort climb). Longest straight 130 m. Nothing within 3 m of a road edge (closest pad 4.5 m, A4-05).
- **Squad positions:** they stand 130-1,124 m from their nearest site; A4-01 is again 1.1 km from Mole Rock, on the causeway head.
