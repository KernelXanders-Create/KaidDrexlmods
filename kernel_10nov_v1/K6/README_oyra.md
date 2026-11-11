# KERNEL_RETURN_K6_oyra: Oyra on the real ground, under the 5 m grid rule (PROPOSED)

| File | What it is |
|---|---|
| `oyra_layout.json` | Layout in your return schema (map frame). Streets carry `points_z` and their level `segments`. 119 buildings with `pad_group`, `pad_z_m`, door side and bearing, `cut_m` / `fill_m`. Also the square (one level), a comp and notes. |
| `oyra_plan.png` | Plan: north up, 100 m scale bar, map coordinates, the 5 m height grid, street levels (blue numbers), doors and garrison. The inset shows the rim square on the cliff edge. |
| `oyra_checks.json` | Every self-check number, as data. |
| `tools/town_grid.py`, `tools/run_town.py`, `tools/oyra.py` | The engine (unchanged since Kamar Village) and this town's hand design, to read as text. |

**Tile used:** `towns6/oyra/height_1m.npy` (11570..12270, 12150..12850). There is no shore window: the lagoon cliff is inside this tile, and I didn't move the town onto the cliff face itself.

**Where the site moved:**
- About 260 m south-west of the K1 point (11920, 12500), onto the real break of slope in the window's south-west corner, as your review asked. The buildings span x 11592-11968 and y 12198-12475 (MEASURED).
- The rim square is at about (11712, 12316).
- The town now faces south-west over the lagoon instead of west over a cliff that isn't there.

## The ground (MEASURED)
- **A flat rim at 129.75-130.75 m** runs west-north-west to east-south-east, about 100 m deep.
- **On its south-west side** the ground drops about 100 m to the lagoon (the dense contours; your flag: median 35° near the sea point).
- **Behind it** a gentle back-slope (5-10 %) falls north-east toward the K1 point.
- No part of the town stands on the cliff face. The cliff-edge row stands on the flat rim, at its edge.

## Layout
- **The rim street (main, 6.5 m):**
  - runs about 30 m inside the cliff edge, along the whole rim (about 380 m);
  - four level segments, all within 1 m of each other (129.75-130.75 m), so it reads as one level;
  - its south row is the cliff-edge row, looking over the lagoon.
- **Two lanes behind it, about 45-55 m apart, with rows on both sides:**
  - the upper lane (128-130.75 m);
  - the back lane (121.75-125.75 m), which steps down the back-slope.
- **Four ramp cross lanes** link the three streets at their levels.
- **Two look-out stairs** (paths) run from the rim street to the cliff edge: dead ends on purpose, as in K1.
- **The rim square:**
  - one level (129.75 m), 40 x 14 m;
  - on the cliff side of the rim street, open to the lagoon (south-west);
  - the landmark is SF02 (20.5 m, sci-fi), standing in for the Narrows Signal Lantern;
  - one ring building (WH09, west end) and a CIS checkpoint or market comp.
- **Roads out:** the rim path (west-north-west, to the Narrows batteries), the crest road (south-east, to the Chora) and the north road (to Oyra Head). I've labelled where each meets the town; they are yours to join.

## Self-check (MEASURED by `tools/town_grid.py` on the site tile)
| Check | Result | Pass? |
|---|---|---|
| Grid points (every 5 m) claimed by two pad levels | **0** | pass |
| Pads at different levels closer than 14 m (17 m at 45°) | **0** (closest 15.3 m) | pass |
| Pad cut or fill | median 1.31 m, max 3.59 m. **1 near the limit:** B001, the landmark on the square (fill 3.59). None over 4.0. | pass, 1 listed |
| Overlaps; footprint into a street | 0; 0 | pass |
| Corner houses within 2 m of a cross street | 0 | pass |
| Doors: 3 m out lands on a street or the square | 119 of 119; door level within 0.75 m for all | pass |
| Lane ends vs the level of the street they join | 0 mismatches over 0.3 m | pass |
| Straight runs (m) | streets 74-77; cross lanes 46-59; look-out stairs 36-39 | pass |
| Grades: rim street | 6.3 % on its drops, 0.0 % average | pass |
| Grades: lanes | up to 15.6 % | pass |
| Grades: cross lanes | 0-13 % | pass |
| Grades: look-out stairs | 21-37 % average | they are stairs |
| Street cut / fill | at most 0.9 m / 1.8 m | pass |
| Largest model / twin group | WH19 10.1 %; ND01-size domes 10.1 %; WH11 + WH24 8.4 %; 27 models | pass (12 % cap) |
| Buildings / garrison | **119 / 55** (88 enterable) | pass (top of 40-55) |
| Sci-fi share | 12 of 119 (10 %), mostly on the rim street | |
| Tall pieces | 1: the landmark, on the square | pass |
| Pad levels | 12 | |

## What is weak, honestly
- **The square is small (40 x 14 m) with one ring building.** The rim between the street and the cliff edge is about 30 m, so a deeper square would sit on the cliff's top slope. Its other sides are the rim street's own row.
- **119 buildings is more than K1's 106.** The flat rim simply allows it. Trim the back lane's north row if you want fewer.
- **The CIS garrison halls (IN01 / IN02) didn't fit beside the square.** The ring there is mostly blocked by the rim street's clearance. The sci-fi read sits on the rim street's row instead.
- **The look-out stairs end at the cliff edge as dead ends.** I didn't draw any platform pieces; those are yours.

## Open questions
1. **Is about 120 buildings right for a platoon objective,** or should I trim to about 100 (drop the back lane's north row)?
2. **Would you like a larger rim square** (about 40 x 22 m) with near-limit pads at its cliff edge (3.5-4 m fill)?
3. **The three roads out:** join them at the labelled street ends, or should I draw them?
