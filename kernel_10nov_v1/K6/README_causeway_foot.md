# KERNEL_RETURN_K6_causeway_foot: Causeway Foot on the real ground, under the 5 m grid rule (PROPOSED)

| File | What it is |
|---|---|
| `causeway_foot_layout.json` | Layout in your return schema (map frame). Streets carry `points_z` and their level `segments`. 82 buildings with `pad_group`, `pad_z_m`, door side and bearing, `cut_m` / `fill_m`. Also the square (one level), a comp and notes. |
| `causeway_foot_plan.png` | Plan: north up, 100 m scale bar, map coordinates, the 5 m height grid, street levels (blue numbers), doors and garrison. The inset shows the fork square. |
| `causeway_foot_checks.json` | Every self-check number, as data. |
| `tools/town_grid.py`, `tools/run_town.py`, `tools/causeway_foot.py` | The grid-aware engine (as for Sound Head and Perys v6) and this town's hand design, to read as text. |

**Tile used:** `towns6/causeway_foot/height_1m.npy` (13750..14450, 7900..8600). There is no shore window; none is needed, as the town already reaches the sea.

**Where the site moved:** nowhere. The K1 anchor (14100, 8250) stays. The buildings span x 14032-14336 and y 8152-8388 (MEASURED).

## Kept from K1 (your review: "keep almost everything")
- **The 8 m AI main street** runs from the causeway landfall at the east end, west past the fork square, to the south-arm road.
- **The fork square** is where the slope road leaves for the monastery.
- **The beach track** goes south to the beach.
- **The roads out of town** carry no frontage. They are the south-arm road (west), the slope road (north) and the beach track.

## How the grid rule shaped it
- **The ground is a gentle slope (8-15 %) falling south-south-east to the sea** (MEASURED). Two rows can face each other across a street at one level.
- **Five streets carry rows, both sides each.** Each level segment of a street and its two rows is one block at one level.
  - M: the main street.
  - UA, UB, UC: three lanes on the contours above it, about 45-50 m apart.
  - LO: a short lower lane on the beach side, west of the square.
- **The closest pads at different levels stand 15.3 m apart** (MEASURED).
- **The main street climbs from the causeway (1.5 m, ASSUMED deck level) to the south-arm road (12.25 m):**
  - six level segments: 1.5, 3.75, 6.0, 9.0, 11.5 and 12.25 m;
  - it drops only in 16 m gaps, at up to 12 %, with a 4.2 % average (fine for convoys).
- **Cross lanes are ramps between neighbouring streets,** each with 3 m level landings that meet the street at its level (all mismatches 0):
  - the slope road runs in three pieces (C2, C4, C7, 6 m wide) and then leaves north as R3;
  - C1, C3, C5 and C8 are lanes;
  - C6 leads to the lower lane and the beach track.
- **The fork square:**
  - It is one level (6.0 m), on the downhill side of the main street at the fork. It is 44 x 18 m.
  - Its south side stays open toward the beach.
  - The landmark is SF02 (20.5 m, sci-fi), standing in for K1's Causeway Signal Pylon.
  - There is one ring building (SF01, west end), plus a market or checkpoint comp.

## Self-check (MEASURED by `tools/town_grid.py` on the site tile)
| Check | Result | Pass? |
|---|---|---|
| Grid points (every 5 m) claimed by two pad levels (buildings + the square + level street segments) | **0** | pass |
| Pads at different levels closer than 14 m (17 m at 45°) | **0** (closest 15.3 m) | pass |
| Pad cut or fill (footprint + 1.5 m, every 1 m) | median 2.14 m, max 2.50 m; none near the limit | pass |
| Overlaps; footprint into a street | 0; 0 | pass |
| Corner houses within 2 m of a cross street | 0 | pass |
| Doors: 3 m out lands on a street or the square | 82 of 82; door level within 0.75 m of its street for all | pass |
| Lane ends vs the level of the street they join | 0 mismatches over 0.3 m | pass |
| Straight runs (m) | streets 61-73; cross lanes 33-60; roads out 41-77 | pass (< 80) |
| Grades: main street | 12.0 % on its drops, 4.2 % average | pass |
| Grades: lanes | up to 19.0 % on single drops (UA, UB) | at the limit |
| Grades: cross lanes | 10-16 % | pass |
| Grades: slope road out (R3) | 19 % (follows the ground) | |
| Street cut into the slope / street fill | at most 1.97 m / 3.36 m (UA) | pass |
| Largest model / twin group | WH19 11.0 %; ND01-size domes 11.0 %; WH11 + WH24 11.0 %; 24 models | pass (12 % cap) |
| Buildings / garrison | **82 / 46** (59 enterable) | pass (40-55) |
| Tall pieces | 1: the landmark, on the square | pass |
| Pad levels | 18 (1.5 to 27.75 m) | |

**Town ground (ASSUMED estimate):** about 42,000 m² of streets plus 6 m and building pads; 67,000 m² as a convex hull.

## What is weak, honestly
- **82 buildings, not K1's 96.** A different-level pad needs 14 m of clear ground around it, so the lanes have to sit about 45 m apart. That leaves room for four terraces between the beach and the crest.
- **The main street and the square read too little sci-fi:** 4 sci-fi pieces in 82. The sci-fi models are 13-17 m deep and fail the 2.5 m cut/fill target on most of the main street's frontage. Raising the sci-fi preference didn't change that. **The causeway gatehouse halls (IN01-IN03) didn't fit** for the same reason; two sci-fi pieces stand at the causeway end instead. Fixing this needs your call on a deeper cut/fill allowance there, or a flat gatehouse pad.
- **The square has only one ring building.** The east end is the landmark's; the slope falls too fast for a ring piece there. The square still has doors on its west and north sides (the main street's row).
- **The main street carries only 17 buildings.** It crosses the contours (it has to climb from the causeway), and its level segments are short.
- **Two lanes reach 19 % on one drop each,** right at the limit.

## Open questions
1. **The causeway landfall:** I kept K1's point (14286, 8181) and assumed a 1.5 m deck (the ground there is 0.5 m). Where does your causeway road actually land, and at what level?
2. **Gatehouse halls:** may the causeway end take a 3-3.5 m pad so the IN halls fit, or should a flat gatehouse pad be graded there?
3. **Is 82 buildings acceptable** in place of K1's 96?
