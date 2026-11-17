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

## K8 AI crossings: two road bridges, a causeway in two widths, the dam crest

| Crossing | Part | Clear width | Level | Boats | AI road line | Second way | Tag | source |
|---|---|---|---|---|---|---|---|---|
| Road bridge 1 | 3AS bridge piece (class to confirm) | 3.1 m truck / 7.5 m armour (deck width NOT MEASURED) | deck top about +3.5 m | 3.0 m clearance under the deck | centre line over the deck and both approaches | required on any AI route (rule 31) | class UNSURE; AI on deck UNSURE (test W4) | HUMAN |
| Road bridge 2 (fallback) | vanilla or CUP road bridge (class to confirm) | same | same | same | same | not required | UNSURE | HUMAN |
| Causeway, truck | earth fill, 6 m crest, 16 m toe | 3.1 m | crest +1.0 m (2.5 m of fill from -1.5 m) | cannot pass | centre line on the crest, level +1.0 m | not required | toe MEASURED from the section; side slope 1:2 AI | HUMAN (width, level); AI (slope) |
| Causeway, armour | earth fill, 12 m crest, 22 m toe | 7.5 m | +1.0 m | cannot pass | same | not required | same | same |
| Dam crest | CIS Fortress Dam with GPs (library comp) | 7.5 m needed on armour routes; crest width NOT MEASURED | as the comp is built | by a lock channel where a site chooses one | along the crest, authored access kept (rule 22) | not required | NOT MEASURED | HUMAN (Drain picks) |

- **Bridge approaches:** about 3.0 m of climb from a +0.5 m bank to the +3.5 m deck: 30 m at 10 % each end (MEASURED from the levels; 10 % is the main-road limit, a dirt road may use 14 %, about 21 m). Deck thickness 0.5 m is ASSUMED until the piece is measured.
- **Each causeway is a designed straight** (listed in a site's `ground_requests.designed_straights` with its ends and reason).
- **Risks and first tests:** W4 (a truck and a tracked vehicle over 1 km of causeway and over each bridge, 5 runs) decides whether the 3AS deck can carry AI; W2 checks that the live boats fit under 3.0 m.
- Drawing: `kit_K8.png` (causeway cross-sections; bridge side view). Data: `kit_K8.json`.

## K1 Boat landing (ground-only beach)

| # | Section | Value | Tag | source |
|---|---|---|---|---|
| 1 | For | the shore points players land on; FOB boats; Refinery landings (op 6) | - | HUMAN (kind) |
| 2 | Parts | none: graded ground only | - | HUMAN |
| 3 | Layout | `kit_K1.png`: 12 m run at 1:6 from -1.5 m to +0.5 m; waterline 9 m up from the toe; 12 m wide | run and waterline MEASURED from the levels; width AI | HUMAN / AI |
| 4 | Walkables | ground only; no simple or normal objects | - | - |
| 5 | Garrison points | 0 (a site covering a landing brings its own) | - | - |
| 6 | Ways in | boats beach on the wet slope; infantry walk up 1:6 (about 9.5 deg) | slope MEASURED from 1:6 | - |
| 7 | Built-for ground | a water ground request at each use: bank graded -1.5 to +0.5 m over 12 m; boat channel at -1.5 m at the toe | - | HUMAN |
| 8 | Facing | no guns | - | - |
| 9 | Size | 0 objects, 0 GPs, sci-fi share n/a | MEASURED | - |
| 10 | Risks and first test | boats may not beach cleanly at 1:6 (W2); the landing is open ground, so its cover comes from the site around it | UNSURE | AI |
