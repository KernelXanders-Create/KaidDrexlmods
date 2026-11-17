# NEW 1 The Cauldron Refinery (working name): spec draft v1

Built from decisions 1-12 in `DECISIONS.md` (all HUMAN). Positions, sizes and counts I filled in are marked AI or ASSUMED. Ground is the K3 sketch until drop 2 (Thu 19 Nov): the crater's real shape, rim height and bed depth are NOT MEASURED. No engine tests were run.

## Purpose, stake, story
- **Op and site:** op 6 The Cauldron, the final 6-F, K3 point (11000, 11000); plays Sun 6 Dec (week 3).
- **Stake:** the Refinery powers the Moraine Citadel (op 8). Left standing, op 8 is harder. (decision 2, HUMAN)
- **Story players can read:** a pipeline runs north out of the east half's pump hall toward the Citadel; the pump hall holds the manifold; blowing it is the win and visibly cuts the line. (HUMAN; pipeline route AI)
- **Palette (the slot's ALIEN LAYER was blank; assumed):** Rust and Ivory: rust-red reeds along every yard and causeway edge, red-leaf trees on the rim, white mineral crust at the waterlines, milky water, tufa towers from scaled rocks in the water (never as decks or roofs), high amber haze and a low sun. (decision 1, HUMAN)
- **Lighting:** a day mission; no lights placed. (decision 12, HUMAN)

## Approaches (decision 3, HUMAN)
1. **SW, over the rim past 6-M1 Rim Bunker Ring (225 deg):** down the SW truck causeway to the west half's gate.
2. **East, from 6-M4 Cauldron Apron Town (86 deg):** along the east truck causeway to the east half's gate.
Plus boats: player boats to the boat-step pier on each half's south side.

## Zones (decision 4, HUMAN; layout AI: see `NEW1_plan.png`)
Origin: the crater centre; x east, y north; z above sea level.
| Zone | What is there | Levels |
|---|---|---|
| Outer works / approaches | two K8 truck causeways (SW: 85 m with one bend; east: 48 m), each a designed straight, 6 m crest, 3.1 m clear; a forecourt fill (12 x 25 m) before each gate | +1.0 m |
| West half (process) | a 40 x 40 m yard; a north deck with the **control room**; a south deck with the **twin flare stacks** (45 m); an inner deck to the link; a gun deck by the gate; the wall line with the gate and the sandy breach; a 25 m boat pier south | yard +0.5, decks +1.7 |
| East half (tank farm and pumps) | the same frame: north deck with the **pump hall** over the **manifold** and the pipeline north; south deck with **three tanks**; inner deck, gun deck, wall line, boat pier | same |
| Centre | a 30 x 30 m deck carrying the CIS Mixed AA Platform; K3 boardwalks 45 m to each half's inner deck | +1.7 |
| Key buildings (interior rooms) | control room (west): task: download the flow logs and shut the flare. Pump hall (east): task: plant charges on the manifold (the stake payoff) | +1.7 |

Each causeway grades down from +1.0 m to its half's yard at +0.5 m; the decks ring the yard and are reached by K4 ramps (1.2 m rise), so the yard is a courtyard overlooked from the decks (decision 8).

## Breaches and destructibles (decisions 6, 10, HUMAN)
| Defended part | Way in 1 | Way in 2 | Way in 3 |
|---|---|---|---|
| West half | causeway gate: 3AS CIS wall door v2, closed at start | destructible sandy CIS wall section, 12 m south of the gate, reached from the forecourt | boat-step pier on the south deck (players' boats) |
| East half | same | same | same |
| Centre deck | the west boardwalk | the east boardwalk | - |

| Set piece | Where | Payoff |
|---|---|---|
| Flare stack A falls | west south deck | the landmark comes down; seen from both approaches |
| Tank 2 burns | east south deck | a big fire in the tank farm |
| Pipeline-north manifold blows | east north deck, in the pump hall | cuts the Citadel's power (the stake) |

## Facing (HOUSE_RULES D) for every gun
| Gun comp | Guns | Bearing | Approach it faces | 300 m clear | No ground above muzzle within 150 m | source |
|---|---|---|---|---|---|---|
| West CIS Heavy Gun Position + AA (UD), gun deck at (-122.5, 12.5), +1.7 m | 5 | 270 | the SW causeway and the rim | NOT MEASURED | **likely FAIL**: the crater rim is about 50 m west, height NOT MEASURED | HUMAN (comp); AI (bearing) |
| East CIS Heavy Gun Position + AA (UD), (122.5, 12.5) | 5 | 90 | the east causeway | NOT MEASURED | **likely FAIL**: the rim is about 50 m east | same |
| CIS Mixed AA Platform, centre (0, 0) | 2 | AA, sky | the crater air space | NOT MEASURED | NOT MEASURED (rim about 150 m away) | same |

A crater rim inside 150 m of every gun is the main facing risk. If the rim stands above the muzzle at drop 2, the guns need a higher seat (a raised gun deck) or a bearing along a gap in the rim; that is a question for you once the ground is in.

## Access (HOUSE_RULES E) for every way in
| Way in | Step / rise | Connector | Check | Tag |
|---|---|---|---|---|
| Causeway gate (forecourt +1.0 to yard +0.5) | 0.5 m | gate in the wall line | at the 0.5 m limit | MEASURED from the levels |
| Yard to north, south, inner decks | 1.2 m | Land_RampConcrete_F | inside 1.08-1.40 m | MEASURED |
| Boat step to the boat pier | 1.2 m | Land_RampConcrete_F | inside the band | MEASURED |
| Centre deck from the halves | 0 m | K3 boardwalk, level | pass | MEASURED |
| Sandy wall section (forecourt +1.0 to yard +0.5) | 0.5 m | breach | at the limit | MEASURED |
| Gun comps and the AA platform on decks | their authored access, kept (rule 22) | - | built for ground, placed on a deck (rule 23): **flag** | UNSURE |
| Control room, pump hall | their own doors at deck level | - | NOT MEASURED (classes unknown) | UNSURE |

## How it reads
| From | What shows | Tag |
|---|---|---|
| 1 km | both flare stacks, the rooms and the tank tops over the rim; the gun decks | ASSUMED (rim height NOT MEASURED) |
| 2 km | the twin stacks over the rim | ASSUMED |
| 3 km | the twin stacks (45 m) as two thin verticals; beyond about 1.8 km only ground shape and colour show, so the stacks carry it | ASSUMED |

## Counts (from `NEW1_parts.json`)
| Count | Value | Tag |
|---|---|---|
| Physical objects | 1,010 (bar: 445) | ASSUMED: deck sections at 16 x 8 m, 3 m wall pieces, clutter recipes per zone; comps MEASURED |
| Garrison points | 251 (bar: 251) | comps MEASURED (2 x 31, 49); deck, yard, link and pier GPs AI; room GPs ASSUMED 16 each |
| Guns | 12 | MEASURED (size table) |
| Footprint | 350 x 300 m crater (K3); the build itself about 270 x 150 m | MEASURED from the plan |
| Pad levels | yards +0.5; forecourts and causeways +1.0; decks +1.7; bed -1.5 (ASSUMED) | - |
| Largest fill | yards 2.0 m, causeways 2.5 m (from a -1.5 m bed) | MEASURED from the levels; real bed NOT MEASURED |
| Mission file | about 1,000 objects; under the 6 MB limit at any plausible size per object | ASSUMED |

## Risks
1. **Facing:** the rim is within 150 m of every gun (above).
2. **Comps on decks:** the gun positions and the AA platform are built for ground; on a +1.7 m deck they break rule 23 unless a deck counts as their ground. Flagged.
3. **AI on decks** (W3) and **trucks on the causeways** (W4).
4. **The crater bed:** if it is deeper than -1.5 m, the yard and causeway fill grows past 4 m.
5. **GPs are at the bar exactly** (251); the room GPs are assumed.

## What to test first in the engine
1. W3 on the concrete pier deck at +1.7 m with the yard ramps.
2. A gun comp placed on a deck: does it settle and fire?
3. The flare stack fall and the manifold blow as scripted set pieces.

## Files
`NEW1_parts.json` (every structural part, clutter recipes per zone, GP list, dressing, counts), `NEW1_plan.png`, `NEW1_elevations.png`, `DECISIONS.md`.
