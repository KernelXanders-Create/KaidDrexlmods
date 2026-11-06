# Swamp: engine risks and tests (PROPOSED)

I didn't run any Arma tests (no Arma 3 here), so every risk below is ASSUMED from 04_ENGINE_FACTS. The tests are proposals.

## Design stance on droids and water (all three concepts)
**Droids hold firm ground and don't cross water by choice.**
- Garrisons sit on hammocks, levees, eskers, trenches and stilt decks.
- Counterattacks spawn 250-400 m away, unseen, on the **same firm-ground patch**, from the enemy side.
- Droid boats and hovers are static targets or Zeus-driven, never AI assault waves.

## Shared risks
| # | Risk | Why it might break | Test (proposed) | Pass if |
|---|---|---|---|---|
| S1 | AI wading | 04: untested. Bog pools and sloughs are everywhere. | **Test W1** (as for islands): a B1 squad crosses 50 m at 0.5 / 1.0 / 1.5 m depth, 5 runs each. Add a run across 300 m of mixed peat and pools at +0.3 to -0.6 m. | They arrive at 0.5 m. Our designs keep AI paths on ground at +0.2 m or above. |
| S2 | Water level moving (tides or waves) | Land at +0.2 to +0.5 m floods if the level rises even 0.3 m. | **Test W3**: log the water height at a marker over 6 game hours, at 3 dates, on a swamp test tile. | Movement under about 0.2 m, or mission settings hold it. If not, raise all "firm" ground to +0.6 m or more. |
| S3 | Boardwalks and stilt decks | 04: AI fall through simple floors and walk through thin rails; mod deck patrols are unreliable. | **Test D1**: a B1 squad crosses a 100 m boardwalk, mod deck vs vanilla deck (04 test 3). | Static garrisons only on any failing piece. |
| S4 | Fog and AI sight | 04: fog is cheap for FPS but changes AI sight. | A fog sweep: an AI squad vs a player-proxy target at 100, 200 and 400 m, with fog 0.1 / 0.3 / 0.5. Log the detection range. | We pick fog values where AI and player sight roughly match. |
| S5 | Dense vegetation and FPS | Very dense stands cost FPS and AI checks. | FPS on a 500 m tile with the densest planned stand, 60 AI. | FPS within Miran's limit. Put the densest stands only on ridges and hammocks, never over whole AOs. |
| S6 | "Too flat" | Command has rejected flat ground before. | Micro-terrain pass on the Stage B heightmap (pools, banks, crater rims, hummocks). | Command's in-game look. |
| S7 | Distant read of very low relief | A swamp at +0 to +3 m has almost no shading at 2-6 km. The satellite texture does all the work. | Render and in-game look at 2, 4 and 6 km. | Water, grass and tree patterns read naturally, with no banding. |

## Concept A: The Mire Line
| # | Risk | Test or check | Fallback |
|---|---|---|---|
| A1 | AI stall in crater fields (04: 100-200 m marches) | Counterattack test: a B1 platoon moves 300 m across craters to a trench. | Counterattacks start in communication trenches 200-300 m behind. Craters only in no man's land. |
| A2 | Trench objects and AI pathing (Gruppe Adler Trenches pieces; suitability ASSUMED) | Garrison test: 20 B1s in a 200 m trench, then an order to move along it. | Static garrisons in trenches; patrols only on open ground. |
| A3 | Object count of three full trench belts | FPS test on one belt segment × 3. | Shorter belts with gaps (the gaps double as bypass options). |
| A4 | Refinery stilts in the crater (normal objects needed) | Test D1 on the refinery deck pieces. | Fewer decks; garrison on the rim instead. |

## Concept B: The Glow
| # | Risk | Test or check | Fallback |
|---|---|---|---|
| B1 | Grass clutter and AI sight: AI may see through tall grass, or not see players who can see each other | Sight test in 1.5 m sawgrass, AI vs player proxy, 50-400 m. | Shorter grass; hammock edges as the real cover. |
| B2 | Hovers over shallow water (mod-dependent; which hovers we have is unknown) | Drive each hover in the modset over -0.5 m and -1.8 m water. | Boats in channels only; tanks on roads only. |
| B3 | Felled Titan readability and walkability | Kitbash a 300 m slice: walk on top, AI garrison inside, look at 2 km. | Shorter Titan, or a fallen ancient Separatist pylon instead (the same role). |
| B4 | Cenotes at -8 m: players drown, AI walk in | Mark them clearly; put rails or rocks round the rims (normal objects). | Shallower cenotes (-3 m). |

## Concept C: River Country
| # | Risk | Test or check | Fallback |
|---|---|---|---|
| C1 | AI convoys on narrow levee roads with water either side | A 2 km levee convoy, 5 runs. | Wider levee crests (12 m or more); scripted path helper. |
| C2 | River as a wall: one bridge | Decide with Miran: is AI never crossing OK? | A second bridge or pontoon in op 5. |
| C3 | Refinery and city decks (normal objects; mod stairs fail per 04) | Test D1 plus a stair test for the city tiers. | Vanilla stairs and ramps as connectors. |
| C4 | Bluff guns with clear fire lines (house rule) vs AI sight over the floodplain | View test from the bluff edge. | Tree belts at the bluff foot. |
