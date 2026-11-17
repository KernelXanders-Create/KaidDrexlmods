# NEW 2 The Moraine Citadel (working name): outline v1

From decisions 13-17 in `DECISIONS.md` (HUMAN). Everything else here (sizes, small rooms, edges, GP numbers, counts) is my suggestion, marked AI or ASSUMED. Ground: the K3 sketch; the moraine's real shape is NOT MEASURED until drop 2.

## Where and what
- **Op and site:** op 8 The Moraine Citadel, the final 8-F, K3 point (8400, 15200); plays Sun 13 Dec (week 4).
- **Stake (K3):** the CIS front headquarters, powered by the Cauldron Refinery (op 6, NEW 1).
- **Win:** capture the CIS commander (a tactical droid or officer) in the Command Room before they escape to 8-12 Escape Pad (decision 15, HUMAN).

## Footprint and zones (decision 13, HUMAN; sizes AI)
| Zone | What | Size (AI) |
|---|---|---|
| T1 lower terrace | wall with a gate (starts closed), gun decks facing the south approach from 8-M1 Citadel Gate | 220 x 40 m |
| T2 middle terrace | wall, bunkers | 220 x 40 m |
| T3 top terrace | wall; the capstone's main blast door | 220 x 40 m |
| Capstone (core) | behind T3 on the crest bench, moraine ground shaped up around it, above the ground surface | about 50 x 30 m, 2 levels |
| Escape tunnel | from the capstone's east side to 8-12 Escape Pad (10000, 14400), built above ground inside a raised bank | about 1.8 km straight-line (MEASURED on K3 points: (8400, 15200) to (10000, 14400)); route NOT MEASURED |
Footprint: about 220 x 205 m including the crest bench (AI).

## Capstone interior (decisions 14-17, HUMAN; room detail AI)
- **Shell:** modular sci-fi corridor and room pieces (JM's Structures / Operation TREBUCHET; exact modules to confirm in the editor).
- **Levels:** 2, about 2,400 m2 of floor (1,320 on level 1, 1,080 on level 2), joined by three vanilla stairs (S1, S2, and the escape stair S3).

| Room | Level | Kind | Floor m2 | GPs | Task / role | source |
|---|---|---|---|---|---|---|
| R1 Entry Hall | 1 | big | 300 | 10 | the main door (E1) opens here | HUMAN (big room); AI (numbers) |
| R2 Guardroom | 1 | small | 60 | 3 | the west postern (E2) | AI |
| R3 Droid Works | 1 | big | 400 | 10 | droid assembly floor; heavy cover | HUMAN / AI |
| R4 Armoury | 1 | small | 80 | 3 | loop between R1 and R3 | AI |
| R5 Generator Room | 1 | small | 80 | 3 | the escape tunnel's foot (E3) | AI |
| R6 Shield Control | 2 | big | 300 | 10 | drop the Citadel's shields | HUMAN / AI |
| R7 Comms Room | 2 | small | 80 | 3 | junction of three routes | AI |
| R8 Officers' Quarters | 2 | small | 80 | 3 | a dead end | AI |
| R9 Command Room | 2 | big | 350 | 10 | the commander (win) | HUMAN / AI |
Passages (1-2 man, with junction GPs): about 400 m2 on level 1 (10 GPs), 270 m2 on level 2 (8 GPs).

**Connections (node graph in `NEW2_plan.png`, data in `NEW2_capstone_graph.json`):** R1-R2, R1-R3, R1-R4, R4-R3, R2-R3 (west loop), R3-R5, R1-S1-R6, R3-S2-R7, R6-R7, R6-R9, R7-R9, R7-R8 (dead end), R9-S3-R5 (the commander's escape).

| Check | Result | Tag |
|---|---|---|
| Routes between big rooms (simple paths up to 5 steps) | at least 7 for every pair (R1-R3 7, R1-R6 11, R1-R9 12, R3-R6 7, R3-R9 9, R6-R9 9) | MEASURED on the graph |
| GP density | level 1: 39 GPs / 1,320 m2 = 2.95 per 100 m2; level 2: 34 / 1,080 = 3.15 (need 1.2) | MEASURED on the AI numbers |
| Parts below ground | 0 (everything above the surface, inside raised ground) | by design |

**Entry points (decision 17, HUMAN):** E1 main blast door off T3 (south) into R1; E2 west postern into R2; E3 the escape tunnel from 8-12 into R5, enterable from the pad end once 8-12 is taken. All start closed. Dark only as a night mission; no filters.

## Estimated counts (ASSUMED)
| Part | Physical objects | GPs |
|---|---|---|
| Terraces T1-T3 (walls, gates, gun decks, bunkers, clutter) | about 350 | about 150 |
| Capstone (modules, doors, stairs, dressing at the unit's best-interior density) | about 600 | 73 |
| Escape tunnel | about 120 | 0 |
| Total | about 1,070 | about 223 |

## Landform it needs
- A south-facing moraine slope rising in three steps (each pad 4 m or less of change) over about 120 m, to a crest bench about 220 x 85 m.
- Ground raised around the capstone's walls to its roof line, so it reads as dug in while staying above the surface.
- A raised bank about 1.8 km long (straight-line) east to 8-12 for the escape tunnel, or a shorter tunnel ending in a covered run (to decide later).

## Risks
1. **The escape tunnel's length:** 1.8 km straight-line to 8-12 is far too long for one built tunnel; it likely becomes a short tunnel plus a covered or trench run. Flagged for the full spec.
2. **Stairs:** only vanilla stairs are trusted; the modular set's own stairs may fail.
3. **Module fit:** modular pieces must give 1-2 man passages without bare holes; joins need doors or wall pieces.
4. **Terraces on the real moraine:** NOT MEASURED until drop 2.
