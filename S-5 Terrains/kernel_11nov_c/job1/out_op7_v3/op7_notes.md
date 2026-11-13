# Op 7: The Rim, ground plan notes, v3 (Kernel, PROPOSED)

**One rule fails: rule 3, for two sites with a vehicle approach and no road.**
- **7-M1 Skaros Rock Keep:** as in v1-v2, on a 22 m lagoon ledge under a 130 m climb of 40-60 % ground. It has a stair: 347 m long with 127 m of rise, up to the Chora-Oyra road at (12699, 11549, 148.0).
  - **Your built size (item 6):** your built Gun Keep pad (A2-12, 128 x 196 m) holds 4 m nowhere within 600 m of the keep's point. So the keep stays 80 x 80 m on the ledge (1.9 m of change), which needs a trimmed composition.
  - **Item 4 (the shore road to the Yard):** the keep's ledge is on the inner shore with the Yard. Its shore road (about 1.3 km at 3 m) belongs with op 8's ramp, so it is drawn in op 8 v2.
- **7-03 Crest Road Checkpoint:** at a true 14 %, every road to it breaks 4 m (4.2-4.6 m) or meets the net at a 1.2-3.6 m step. A 526 m path joins it to the net below.

Everything else passes (`op7_checks.json`, and `tools/verify.py` measured your way):
- 0 of 15 roads over 14 %;
- every pad within 4 m (worst 3.71 m, the Chora bastion);
- junction steps at most 0.29 m;
- nearest house wall 7.4 m from a road edge.

## The net
- **One net on Ember Crescent** reaches the Chora, Oyra, the Narrows and Oyra Head: 15 dirt roads, 11.6 km. It is joined to op 6 v2's net.
- **The join to op 6:** where the AA Umbrella's road (7-M4) meets op 6's road from the checkpoint to the monastery (6-02 to 6-F), that road gets a 50 m level landing at (14424, 11123), level 300.67 m. It is listed in `edits_to_other_ops_roads` as an edit to op 6 v2's road.
- **How it came together:** the run first grew two pieces, the Chora-Oyra side and the Oyra Head-Narrows side, each joined to an existing road. A 707 m road now joins them. It leaves the crest road 80 m out from Oyra and runs round the town's north side to the North Rim Trench (7-06).

## Your built road at Oyra Head (item 10)
- **Fixed ground:** your ops 1-2 road file's road from the Oyra Head Landers to the Windmill Flak (`7-05-7-14`) is now fixed ground in this op. No road of mine runs beside it or crosses its band.
- **How it joins:**
  - the Windmill Flak (7-14) joins it by a 66 m spur;
  - the Oyra Head Radar (7-04) joins it by a 500 m road;
  - both meet it at 0.15-0.29 m steps, within the 0.3 m I allow.
- **The Landers (7-05):** they join the net through the North Rim Trench (7-06), not your road.

## Oyra (job 2, item 15)
- **The crest road** comes in at the rim street's east end. It stops 15 m out on the street's line, at (11919, 12183), level 130.75 m; those 15 m are the street extended (Oyra street work). Its edge keeps 16 m from every house wall.
- **The north road:** the joining road above passes 141 m from the back lane's west end (the K6 notes' "north road" port) and serves the same way north. A short stub to that street end is yours if you want the port used.
- **The look-out stairs** (stair pieces; their tops are on the rim street; the cliff faces south-west over the lagoon):

  | Stair | Top | Cliff edge | Foot at the water |
  |---|---|---|---|
  | west | (11636, 12338), 129.9 m | (11629, 12325), 126.9 m | (11464, 12039), at the lagoon |
  | east | (11862, 12252), 130.0 m | (11847, 12226), 125.7 m | (11702, 11975), 1.9 m |

  Each is a 125-130 m drop from the cliff edge to the water. As look-outs they need only reach the edge, a few metres down.

## Your built sizes (item 6)
| Site | Composition | Result |
|---|---|---|
| 7-F Rim Chora bastion | CIS Gloamport Star Bastion | Your built A2-02 pad, 149 x 150 m, at 238.5 m (3.71 m of change). |
| 7-M1 Skaros Rock Keep | CIS Gloamport Gun Keep | Your built pad does not fit; see the first lines. |
| 7-07 Chora Power Bank | CIS Powerbank Facility | Your built 192 x 166 m pad holds 4 m nowhere within 960 m. It keeps 120 x 100 m (a trimmed composition). |

## Roads
- **Size:** 15 dirt roads (7 m), 11.6 km.
- **Measured on the handed-over points:** grade at most 13.8 %. Cut/fill at most 3.91 m. Longest straight 135 m. Nothing within 3 m of a road edge (closest pad 7.7 m).
- **Moves are from the design point** (item 12):
  - 7-12 Crew Barracks: 583 m;
  - 7-06 North Rim Trench: 417 m;
  - 7-02 Skala Path Head: 286 m;
  - 7-13 Chora Lower Terraces: 193 m.

  The reasons are as in v2.
