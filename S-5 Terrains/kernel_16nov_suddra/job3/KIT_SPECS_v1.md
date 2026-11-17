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
