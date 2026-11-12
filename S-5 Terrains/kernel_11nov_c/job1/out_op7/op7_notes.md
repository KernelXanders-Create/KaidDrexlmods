# Op 7: The Rim, ground plan notes (Kernel, PROPOSED)

**One rule fails: rule 3 ("one connected net per island for sites with a vehicle approach"), for 7-M1 Skaros Rock Keep only.**
- The purpose map gives the keep a vehicle approach, but it stands on a 22 m ledge at the lagoon. The ground above rises 130 m at 40-60 %, so no 7 m road holds 14 % with 4 m cut / fill.
- The keep has a stair instead: 310 m long with 132 m of rise, from the ledge (12430, 11330, 21.75) up to the Chora-Oyra road at (12700, 11482, 153.6).
- **To pass rule 3, one of these is needed:**
  - a ramp or lift cut into the cliff;
  - a vehicle approach by water only (landing craft on the lagoon);
  - dropping "vehicles" from the keep's approaches in the purpose map.

Every other rule passes (`op7_checks.json`). Every other Ember Crescent site, and Oyra, is on ONE net, joined to op 6's west climb road. So the Chora is linked by road to the Prophet Monastery FOB, as the purpose map wants.

## The three things I am least sure of
1. **Skaros Rock Keep** (above).
2. **The Rim Chora has no town layout yet.**
   - 7-F is a hand-made town plus CIS Gloamport Star Bastion with GPs. The town is not one of the seven K6 towns, so the plan seats only the bastion: an ASSUMED 120 x 120 m pad at 241 m, 40 m from its point, 1.93 m of change.
   - **The Chora's houses must still fit round it.** In this plan, three roads and one pad are within 500 m of the bastion:
     - the road to the Chora Lower Terraces (7-13), 153 m;
     - the road to the AA Umbrella (7-M4), 513 m;
     - the road to the Skala Path Head (7-02), 310 m;
     - the AA platform A7-03.

     A Chora layout would pin these down, or move them.
3. **The road to Oyra is long, and the coast has few beaches.**
   - **The rim road:** the road from the Chora to Oyra runs 2.5 km along the lagoon rim and enters Oyra at the west end of its rim street.
     - It passes 14 m from the town's south row of buildings.
     - The east end, where the K6 notes put the crest road, gave no road within 4 m.
   - **Oyra Head's north tip has no landing shore on the 5 m grid.** The landers (7-05) sit at 125 m, and the bunkers (7-11) at 161 m. Boats reach the Coral Shelf shores west of the head (about 80 m stretches at y 15570-15950) and the Ash Crescent shores.

## Oyra (job 2)
- **Where it is:**
  - **purpose map:** (11920, 12500);
  - **K6 v2 layout centre:** (11785, 12344), on the cliff-top rim (130-131 m) over the lagoon;
  - **offset:** 206 m.
  - **I'd keep the layout:** its cliff-edge row is on the real break of slope, as your review asked.
- **Road join:** the rim street's west end, (11592, 12378) at 130.75 m, leaving west-north-west.
  - **How it was chosen:** the planner tried all five street ends the K6 notes name. The road from the Chora reached this one.
  - **The other street ends are join points on the net:** the North Rim Trench (7-06) joins at one, 171 m away. Through it come the Narrows East Battery and the north road to Oyra Head.
  - **Clearance:** the closest building centre is 14 m from a road edge, beyond the street ends.
- **Garrison:** 55 of its 106 buildings, platoon weight, matching its role as a main.
- **Squad positions guarding it:**
  - A7-05, on the rim road between the Chora and Oyra;
  - A7-06, over the Narrows from the east cliff.
- **Shore / quay:** none. Oyra is a cliff town about 100 m over the lagoon. The K6 layout's two look-out stairs from the rim street (about (11636, 12338) and (11862, 12252)) go to the cliff edge, not to the water.

## Moved, resized or added sites
| Site | Moved | Why |
|---|---|---|
| 7-12 Crew Barracks | 581 m | South-east, to (14190, 10270) at 194.5 m, beside op 6's west climb road. It is the net's first link to op 6. |
| 7-13 Chora Lower Terraces | 193 m | Up beside the bastion at 244 m. The terraces' point is on the cliff. |
| 7-M4 Chora AA Umbrella | 146 m | — |
| 7-02 Skala Path Head | 130 m | Onto the cliff top at 262 m, where the Skala path starts down. The purpose map's point (124 m) is on the cliff face. |
| 7-11 Oyra Head Beach Bunkers | 113 m | — |
| 7-04 Oyra Head Radar | 100 m | — |
| 7-07 Chora Power Bank | 78 m | **Pad reduced to 120 x 100 m:** the composition's known pad (2-14) is 192 x 166 m, and none holds 4 m within 960 m. |
| 7-M1, 7-08, 7-M3-T, 7-F | 40-71 m | — |
| others | 0-10 m | — |
| 7-06 North Rim Trench | 5 m from its new rough point | The purpose map's point, south-west of Oyra, is boxed in by the cliff and the town, so I gave the trench a rough point on the rim between Oyra and the Narrows (11400, 12500). It now stands at 123 m. |
| 7-M3-T | added | The Narrows East Battery's Flower Tower 2 is its own pad, 250 m north-east of the artillery base. |

## Composition sizes
- **KNOWN** (same composition in your op 1-2 pads): 7-M3-T (Flower Tower 2), 7-01, 7-02 (seated level), 7-06.
- **Reduced:** 7-07 (above).
- **ASSUMED:** 7-F (bastion), 7-M1, 7-M3, 7-M4, 7-03, 7-04, 7-05, 7-08, 7-11, 7-12, 7-13, 7-14, 7-15. The basis for each is `size_note` in `op7_plan.json`.

## Approaches (two per main and the final)
- **7-F Rim Chora:**
  - along the crest road from the Prophet Monastery FOB (op 6), past the Crew Barracks (7-12) and the Crest Road Checkpoint (7-03) (vehicles);
  - the covered way up from Skaros through the Chora Lower Terraces (7-13), on foot (the keep's stair, then the terraces).
- **7-M1 Skaros Rock Keep:**
  - down the keep's stair from the Chora-Oyra road (on foot; there is no road, see the first line);
  - by boat on the lagoon once the Narrows are open.
- **7-M2 Oyra:**
  - along the rim road from the Chora (vehicles);
  - down the north road from Oyra Head, from the landers (7-05).
- **7-M3 Narrows East Battery:**
  - from Oyra past the North Rim Trench (7-06) (vehicles);
  - by boat to the Narrows shore below the battery, then up on foot.
- **7-M4 Chora AA Umbrella:**
  - by road from the Chora (vehicles);
  - by road from the crest road past the Power Bank (7-07).

## Squad-size positions (10)
| Position | Covers | Height / note |
|---|---|---|
| A7-01 | the crest road between the monastery (op 6) and the Chora | |
| A7-02 | the lagoon shore and the Skala path's foot | 4 m, a shore work, 11.9 m from the +0.3 m line |
| A7-03 | the air over the Chora (AA platform) | |
| A7-04 | Skaros and the lagoon west of the Chora | |
| A7-05 | the rim road between the Chora and Oyra | |
| A7-06 | the North Narrows from the east cliff | |
| A7-07 | Oyra Head's west shore and the Coral Shelf landfall | |
| A7-08 | Oyra Head's north tip and the sea toward the skerry | |
| A7-09 | Ash Crescent's north tip | 20 m |
| A7-10 | the Ash north ridge and the Narrows channel | 5 m |

They stand 130-859 m from their nearest site. A7-05, on the rim road, is 859 m from Oyra.

## Ash Crescent and the skerry
- **No road:** 7-01 Narrows West Battery (34 m) and 7-08 Ash North Ridge Post (106 m) are foot and boat sites on Ash Crescent, as the purpose map says.
- **Shores:** the two Ash Crescent stretches in the box are 547 m and 503 m, at its south end (y 9870-9945), and 148 m, 80 m and 53 m elsewhere along its shores.
- **7-15 North Skerry Sensor:** on its stack, air only.

## Roads
- **Size:** 15 dirt roads (7 m), 10.4 km in all. One net on Ember Crescent, joined to op 6's west climb road (`6-03-4-10`) by a 176 m road from the Crew Barracks.
- **Measured:** grade at most 14.0 %. Cut/fill at most 3.91 m over every grid point a road fixes. Longest straight 117 m. Nothing within 3 m of a road edge (closest pad 8.0 m; closest town building centre 14 m).
- **Junction steps (reported):** up to 2.84 m, where the Crew Barracks road meets op 6's road.
- **Pads:** the worst ground change is 3.65 m, at 7-08. 7-07 and A7-01 are also over 3.5 m.
- **No main roads:** the climbs need 14 %.
