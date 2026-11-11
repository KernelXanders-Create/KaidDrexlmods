# Islands: engine risks and tests (PROPOSED)

I didn't run any Arma tests (I have no Arma 3 in this environment), so every risk below is ASSUMED from 04_ENGINE_FACTS and general Arma behaviour. The tests are proposals for your team.

## Design stance on droids and water (all three concepts)
**Droids never need to cross water.** Each island's garrison defends its own island, and counterattacks spawn 250-400 m away, unseen, on the **same landmass**, from the enemy side (house rule).

- Droid boats and gunboats are **static targets** (air-prep or objectives), never AI-driven assault craft.
- Zeus can drive a boat by hand if the mission wants one.
- Where a concept has wading flats (A sandbar, B shoals, C reef), the droids hold **fixed** positions on the flat (pillboxes, wrecks, stilt forts). They don't wade across it.

## Shared risks
| # | Risk | Why it might break | Test (proposed) | Pass if |
|---|---|---|---|---|
| S1 | AI wading or swimming | 04 says it's untested. AI may stall, drown or path badly in water. | **Test W1:** a B1 squad ordered across 50 m of water at 0.5 / 1.0 / 1.5 m depth, 5 runs each, on our modset (droid units FST_Droid_B1_*). Record arrive, stall or drown, and the time taken. | Arrive 5/5 at 0.5 m. We design so it doesn't matter at 1.0 m or deeper. |
| S2 | AI boat crews and landings | Our Navy may want AI-crewed troop boats. | **Test W2:** an AI boat crew lands a squad on a sand beach, 5 runs; then again on a reef flat. | 4/5 clean landings, or we drop AI boats and keep them player and Zeus only. |
| S3 | Tides or waves change the water level | Wading flats at -0.3 to -1.2 m and beaches at +0.3 m are sensitive to even about 0.3 m of change. | **Test W3:** in the terrain test build, log the water height at a marker every 10 min over 6 game hours, at 3 dates. Also test the wave settings in the mission. | The water moves less than about 0.2 m, or we set mission weather and time to hold it. |
| S4 | Distant read of coasts | 04: past about 1.8 km only the terrain and satellite texture render. Reef colours, beaches and shelves must read in the satellite texture. | Render a test tile and look in-game from 2, 4 and 6 km. | Shelves and reefs read as natural, with no hard rings or bands. |
| S5 | Simple-object decks | 04: AI fall through simple-object floors. Piers, stilt towns and wreck decks are everywhere. | **Test D1:** a B1 squad patrolling a 100 m pier built from a mod deck vs a vanilla deck (04 test 3). | We keep static garrisons only on any deck that fails patrols. |
| S6 | Sea-level views | Long sight lines across open water. | Run a view-distance and fog test per concept from the highest point. | We agree a haze value Miran likes. |
| S7 | Vehicles to islands | Getting armour onto an island needs landing craft or sling loads. | Test a sling load with a LAAT/c (or what our mods have) and a landing-craft ramp onto sand. | At least one way works, or we keep armour to the islands it starts on. |

## Concept A: Pillar Reach
| # | Risk | Test or check | Fallback |
|---|---|---|---|
| A1 | Hundreds of towers mean heavy dressing and FPS cost. Towers can look like blobs at 4 m terrain cells. | A 1 km² test tile with 10 towers: FPS, object count, look at 0.5, 2 and 4 km. | Fewer, bigger towers. Bake more shape into the terrain. Rock objects as simple objects (04). |
| A2 | Undercut "mushroom" islets can't be made in the heightmap. | Kitbash test: scaled rocks forming an overhang; check AI and players don't fall through the gap. | Skip the undercut and use a steep tower with a rock skirt. |
| A3 | The bowl interior's multi-level halls rely on mod stairs (04: many fail). | Use vanilla concrete ramps or stairs in garrison connectors; test a squad climb. | Single-level halls with ramps. |
| A4 | AI near steep tower bases may flip or stall (04: 100-200 m marches). | Spawn counterattacks on open ground 250-400 m away, not round towers. | Static garrisons on towers. |

## Concept B: Ember Chain
| # | Risk | Test or check | Fallback |
|---|---|---|---|
| B1 | AI convoys on the causeways: 04 says convoys leave the road on switchbacks. The causeways are straight and flat, which is good. The Caldera rim road is steep. | AI convoy test on a 1.5 km causeway and a rim switchback. | No AI convoys on the rim road; scripted path helper. |
| B2 | Long sight lines from the 500 m summit. | View test (S6). | Lower the summit in Stage B; more cloud. |
| B3 | Boats inside the caldera need the dam gate to open (a scripted gate). | Gate test: a boat passes through an open gate object. | Air-only entry to the lake; foot entry via the dam. |
| B4 | Steep grass slopes (above about 35°) stall infantry and AI. | Slope walk test. | Terrace paths; stairs objects (vanilla). |

## Concept C: The Shallows
| # | Risk | Test or check | Fallback |
|---|---|---|---|
| C1 | Stilt towns and the hull's decks are the most deck-heavy concept: AI fall-through and patrols (04). | Test D1 plus a hull-deck garrison test. | Static garrisons only; vanilla floors in key rooms. |
| C2 | Wading belts with no cover mean slow players get massacred. | Mission dry-run: time a fireteam wading 400 m at -1 m. | More coral heads and wrecks; shorter belts. |
| C3 | Hull interior seen through panels: 04 says some sci-fi wall panels are see-through to AI. | Test the wall classes before the hull build. | Use tested classes only. |
| C4 | A very flat terrain may read as "too flat" (command feedback). | Micro-terrain pass on motus and flats (dunes, rubble ridges, pools). | Raise motus to +5 m dunes. |
