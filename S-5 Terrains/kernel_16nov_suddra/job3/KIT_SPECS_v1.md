# Suddra water and stilt kit, specs draft v1 (JOB_3)

Built from `DECISIONS.md`. No engine tests were run (no Arma 3 with the live modset here), so every walkable claim is UNSURE until your tests W1-W5. Class names I cannot see are marked "to confirm"; I name only classes given in the brief or the vanilla family I believe they belong to (UNSURE).

## K4 Stilt deck, small (15 x 15 m) and large (30 x 30 m)

| # | Section | Small | Large | Tag | source |
|---|---|---|---|---|---|
| 1 | For | a garrisoned stilt outpost | the base of the Cauldron Refinery's stilt sections (op 6, week 3); centre clear for a library comp | - | HUMAN |
| 2 | Parts | deck of vanilla concrete pier sections (Land_PierConcrete_01_* family, to confirm); 8 pillars, simple; low walls, normal; 1 Land_RampConcrete_F; 1 sci-fi prefab hut (3AS / Gliese / JM's, to confirm) | same deck, 20 pillars, walls, 1 ramp; no hut | classes UNSURE; counts MEASURED from `kit_K4.json` | HUMAN (parts); AI (counts from 6 m pillar spacing) |
| 3 | Layout | `kit_K4.png` plan + side view | same | - | AI |
| 4 | Walkables | deck, ramp, hut floor: all NORMAL. AI path: bank +0.5 m, up the ramp (1.2 m rise), onto the deck | deck and ramp, NORMAL; same path | AI walk UNSURE (test W3) | HUMAN |
| 5 | Garrison points | 6, along the inside of the low walls, all moving (walls stop the AI walking off) | 12, same | count HUMAN; positions AI | HUMAN / AI |
| 6 | Ways in | infantry and AI: one vanilla concrete ramp on the bank side, in a 4 m gap in the wall; no vehicles | same | gap width ASSUMED (ramp width NOT MEASURED) | HUMAN (ramp); AI (gap) |
| 7 | Built-for ground | bank at +0.5 m beside the deck for the ramp foot; bed at -1.5 m under the deck | same | - | HUMAN |
| 8 | Facing | no guns | no guns (a comp in the centre brings its own and is checked per site) | - | HUMAN |
| 9 | Size | 16 entries in `kit_K4.json` (deck and walls as one entry per run; true object count NOT MEASURED until piece sizes are read); 6 GPs | 27 entries; 12 GPs (+ the centre comp's) | MEASURED (entries) / NOT MEASURED (objects) | - |
| 10 | Risks and first test | (1) AI may not walk the concrete pier deck at +1.7 m: run W3 first; (2) wave swing eats freeboard: W5; (3) the pier sections' own deck height may not match +1.7 m without sinking them | same, plus: the centre comp must sit on the deck, not the sea bed | UNSURE | AI |

- **Levels:** deck +1.7 m above sea level (freeboard 1.7 m at calm sea), bed -1.5 m, bank +0.5 m. Rows K-b (way in by vanilla ramp: yes) and K-c (lowest deck +1.7 m, needs at least +0.8 m) pass on paper.
- **Sci-fi share:** small deck: the hut is the only sci-fi piece; share by volume NOT MEASURED. Large deck: none until a comp stands in the centre.

## K2 Pier / jetty: 10, 25 and 50 m (the 50 m with a turret head)

| # | Section | Value | Tag | source |
|---|---|---|---|---|
| 1 | For | quays (4-M4 Barge Quay in week 3 and later), Refinery pier gates (op 6), village piers (pile fringe) | - | AI (uses); HUMAN (kit) |
| 2 | Parts | deck of vanilla concrete pier sections (Land_PierConcrete_01_* family, to confirm), 4 m wide; pillars every 6 m both sides, simple; low walls both edges and the head end, normal; 1 Land_RampConcrete_F from the bank; a boat step at +0.5 m (normal platform, to confirm) beside the head with 1 Land_RampConcrete_F up to the deck. 50 m only: head widened to 8 x 8 m with one CIS Turbolaser Tower with GPs | classes UNSURE | HUMAN |
| 3 | Layout | `kit_K2.png` plan of all three + side view of the 50 m | - | AI |
| 4 | Walkables | deck, both ramps, boat step, widened head: all NORMAL. AI path: bank +0.5, ramp, deck +1.7 to the head | AI walk UNSURE (test W3) | HUMAN |
| 5 | Garrison points | 10 m: 1; 25 m: 2; 50 m: 5 on the deck + the turret's 30 = 35. Deck GPs one per 10 m, alternating sides, all moving | count and positions AI; turret GPs MEASURED (size table) | AI / HUMAN |
| 6 | Ways in | infantry and AI: the bank ramp; players from boats: the boat step and its ramp (1.2 m rise). No vehicles | - | HUMAN |
| 7 | Built-for ground | bank at +0.5 m at the root; bed -1.5 m along the pier | - | HUMAN |
| 8 | Facing | 50 m: the turret faces out along the pier's axis over open water; its 300 m / 150 m check is per site | NOT MEASURED | AI |
| 9 | Size | entries in `kit_K2.json`: 11 / 15 / 25 (deck and walls one entry per run; true object counts NOT MEASURED); turret 30 obj, 1 gun (MEASURED) | - | - |
| 10 | Risks and first test | (1) AI walk on the concrete deck: W3; (2) the boat step at +0.5 m is under the K-c +0.8 m deck minimum: it is a boat step, not a deck; wave swing may wash it (W5); (3) the turret on a pier deck: does it settle on the deck, not the bed? Check in the editor | UNSURE | AI |
