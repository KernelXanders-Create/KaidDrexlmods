# KERNEL_RETURN_K6_sound_head: Sound Head on the real ground, under the 5 m grid rule (PROPOSED)

| File | What it is |
|---|---|
| `sound_head_layout.json` | Layout in your return schema (map frame). Streets carry `points_z` and their level `segments`; 61 buildings with `pad_group`, `pad_z_m`, door side and bearing, `cut_m` / `fill_m`; square, comps, notes. |
| `sound_head_plan.png` | Plan: north up, 100 m scale bar, map coordinates, the 5 m height grid, street levels (blue numbers), doors and garrison. The inset shows the gate square. |
| `sound_head_checks.json` | Every self-check number, as data. |
| `tools/town_grid.py`, `tools/run_town.py`, `tools/sound_head.py` | The grid-aware engine and this town's hand design, to read as text. |

**Tile used:** `towns6/sound_head/height_1m.npy` (2200..2900, 10200..10900). The shore window is almost the same, as your note says. The town stays at the site; nothing moves.

## How the grid rule shaped it
- **The ground is the inner face of a bowl falling east to the Sound at 22-25 %** (MEASURED; your review: median 13.9°). At that slope, two rows facing each other across a street can't share one level: the far pad edges would sit about 3.3 m off the ground.
- **So every street is a terrace with ONE row, on its uphill side,** at one level. Streets follow the real contours every 7 m: 14, 21, 28, 35 (main street), 42, 49 and 56 m, with gentle ±3.5 m bends so no run is straight over 80 m.
- **Terraces are about 29 m apart,** so pads on neighbouring terraces stand at least 15.2 m apart (MEASURED). The bank between them is hidden behind each row.
- **Levels change only across 16 m gaps** (MEASURED, by street): the main street drops at up to 12.0 % (average 1.3 %), and lanes up to 18.8 %.
- **Three stair paths** (P1-P3) climb between the terraces; they carry no buildings.
- **The gate square** sits on the valley floor at the bowl's south-east lip, where the Notch road comes in. It is one level (34.5 m), long and narrow along the contour (40 x 16 m), open to the north-east.
  - **The ring:** 6 buildings, mostly the small SF03 sci-fi tower, with doors in on the south-west and both ends.
  - **The landmark:** ND06 (30.5 m) stands on the square.
  - **The main street** starts at the square's level.
- **The quay** is on the only shore bench (2-5 m), level 3.0 m, reached by a stair. It is foot only; boats serve it, because an 11 m drop in about 50 m can't be a lane. It holds one building and one comp.

## Self-check (MEASURED by `tools/town_grid.py` on the site tile)
| Check | Result | Pass? |
|---|---|---|
| Grid points (every 5 m) claimed by two pad levels (buildings + the square + the quay + level street segments) | **0** | pass |
| Pads at different levels closer than 14 m (17 m at 45° to the grid) | **0** (closest 15.2 m) | pass |
| Pad cut or fill (footprint + 1.5 m, every 1 m) | median 2.34 m, max 3.50 m. **8 near the limit:** the square ring B001-B007 (2.78-3.22) and quay B061 (3.50). None over 4.0. | pass, 8 listed |
| Overlaps; footprint into a street | 0; 0 | pass |
| Corner houses within 2 m of a cross street | 0 | pass |
| Doors: 3 m out lands on a street, the square or the quay | 61 of 61; door level within 0.75 m of the street for all | pass |
| Lane ends vs the level of the street they join | the main street starts at the square's level; contour lanes end free | pass |
| Straight runs (m) | streets 35.3-43.5; stair paths 45.5-51.6 | pass |
| Grades | main 12.0 % on its drop (average 1.3 %); lanes up to 18.8 %; stair paths 22-31 % average (they are stairs) | pass |
| Street cut into the slope | at most 1.17 m | pass |
| Largest model / twin group | 11.5 % (SF03); WH11 + WH24 6.6 %; 17 models | pass (12 % cap) |
| Buildings / garrison | **61 / 31** (every enterable building is garrisoned) | see note |
| Tall pieces | 1: the landmark ND06, on the square | pass |
| Pad levels | 11 | |

## What is weak, honestly
- **61 buildings, not K1's 104, and a garrison of 31, not 40-55.** On a 24 % slope only the uphill side of each terrace can carry houses. Each extra terrace needs about 29 m of slope, and the bowl has room for seven. More buildings would need the 2.5 m cut/fill target relaxed, or the town moved to gentler ground (none within the window).
- **Street fill:** with the level set for its row, the street sits on fill: up to 4.2 m on the main street and 6.5 m on T49 at its steepest spot. Your rule fails a street that cuts more than 4 m; fill isn't covered, so tell me if 6.5 m is too much.
- **The square ring and the quay building need near-limit pads** (2.8-3.5 m). Your full grader reads up to 1.9 m more, so these 8 may fail it.
- **The quay has one building.** The shore bench is tiny and steep (your flag: median 24°).

## Open questions
1. **Reading of the rule.** "A block is one level, both rows of it": I read a "block" here as a street segment plus its rows. On this slope there is only one row, uphill. Is that the reading you meant?
2. **Is 61 buildings acceptable for this site,** or should the target cut/fill rise to 3.0 m to fit more?
3. **Is street fill above 4 m acceptable?**
