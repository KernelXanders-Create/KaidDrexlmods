# KERNEL_RETURN_K5b_perys_v6: Perys second pass under the 5 m grid rule (PROPOSED)

| File | What it is |
|---|---|
| `perys_v6_layout.json` | Layout in your return schema (map frame). Streets carry `points_z` and their level `segments`. 98 buildings with `pad_group`, `pad_z_m`, door side and bearing, `cut_m` / `fill_m`. Also the square (one level), comps and notes. |
| `perys_v6_plan.png` | Plan: north up, 100 m scale bar, map coordinates, the 5 m height grid, street levels (blue numbers), doors and garrison. The inset shows the quay group. |
| `perys_v6_checks.json` | Every self-check number, as data. |
| `tools/town_grid.py`, `tools/run_town.py`, `tools/perys_v6.py` | The grid-aware engine (the same one as Sound Head, plus a "ramp" mode for link lanes) and this town's hand design, to read as text. |

**Ground used:** `perys/height_perys_natural_1m.npy` (natural ground). **Fixed points kept:** the NW road port at 59.4 m, the v4 harbour road HR (unchanged), the quay apron at 2.2 m, and the v4 quay comp.

**Why a second pass:** your grader found K5 v5 couldn't be built. 143 pairs of its 67 pad groups clashed on the 5 m grid, and only 5 of 104 pads were accepted. v6 is rebuilt around the grid rule from the start.

## How the grid rule shaped it
- **Perys is a 10-14 % slope falling north-east to the sea** (MEASURED). At that slope two rows can face each other across a street at one level. Each far pad edge sits within about 2.2 m of the ground.
- **Each level segment of a street is one block: the street plus both rows, at one level.** Every row run is one `pad_group`.
- **Five streets run along the slope**, each with rows on both sides:
  - U2: the new top lane;
  - U: the upper lane;
  - M: the main street from the NW road port;
  - KW and KE: the lower lanes.
- **The streets are about 47 m apart,** so the back walls of rows on neighbouring streets stand at least 14 m apart (17 m on the diagonal). MEASURED: the closest pair of pads at different levels is 16.1 m apart. The bank between them is hidden behind the rows.
- **Levels change only across 16 m gaps,** placed where a cross lane meets the street. Frontages are level: every door is within 0.75 m of its street.
- **Cross lanes are separate pieces,** one between each pair of neighbouring streets: CT1-2, CU1-4, CM1-4 and HL. Each runs as one ramp with a 3 m level landing at each end, meeting the street it joins at that street's level (all mismatches 0).
- **The square is one level (57.0 m), at the main street's level** on its north-east (downhill) side. It is open to the sea.
  - **The landmark:** ND07 stands on the square.
  - **The two comps:** a market and a hall or cargo group.
  - **The ring:** I tried to put one at the two ends of the square, but every building there failed cut/fill or street clearance, so the square has none.
- **The quay group stands on the 2.2 m apron, doors north:** IN01, SF15, IN02 and SF16.
- **HL links the lower lanes to your v4 harbour road HR.** HR itself is unchanged.

## Self-check (MEASURED by `tools/town_grid.py` on the natural tile)
| Check | Result | Pass? |
|---|---|---|
| Grid points (every 5 m) claimed by two pad levels (buildings + the square + the quay + level street segments) | **0** | pass |
| Pads at different levels closer than 14 m (17 m at 45°) | **0** (closest 16.1 m) | pass |
| Pad cut or fill (footprint + 1.5 m, every 1 m) | median 1.70 m, max 2.88 m. **1 near the limit:** B001, the landmark ND07 (fill 2.88). None over 4.0. | pass, 1 listed |
| Overlaps; footprint into a street | 0; 0 | pass |
| Corner houses within 2 m of a cross street | 0 | pass |
| Doors: 3 m out lands on a street, the square or the quay | 98 of 98; door level within 0.75 m of its street for all | pass |
| Lane ends vs the level of the street they join | 0 mismatches over 0.3 m | pass |
| Straight runs (m) | streets 53-78; cross lanes 20-50; your v4 HR 214 (not ours, unchanged) | pass (< 80) for v6 streets |
| Grades: main street | 12.0 % on its drops, 3.0 % average | pass |
| Grades: lanes | up to 19.0 % (U and KE) | at the limit |
| Grades: cross lanes | 9-17 % (CM3 16.7 %) | pass |
| Street cut into the slope | at most 1.41 m; street fill at most 2.57 m (KE) | pass |
| Largest model / twin group | ND03 9.2 %; WH11 + WH24 10.2 %; 28 models | pass (12 % cap) |
| Buildings / garrison | **98 / 52** (66 enterable) | pass (40-55) |
| Tall pieces | 1: the landmark, on the square | pass |
| Pad levels | 17 (2.2 to 67.0 m) | |

**Main street levels (from the port):** 59.4, 57.75, 57.0 (the square), 53.5, 50.0 m.

**Town ground (ASSUMED estimate):** about 43,000 m² of streets plus 6 m and building pads, or 64,000 m² as a convex hull. Both are under your 79,700 m² limit.

## Compared with v5
| | v5 (K5) | v6 |
|---|---|---|
| Buildings | 104 | 98 |
| Garrison | 40-55 | 52 |
| Grid clashes | 143 pairs (your grader) | 0 (our check) |
| Pad levels | 67 groups, most on their own level | 17 levels in 34 row groups |
| Streets | M, U, K, K2 | Same pattern plus a top lane U2; each street level by segment |
| Square | sloping, with a ring | one level, no ring |

## What is weak, honestly
- **Our grid check is our reading of your rule.** I can't run your grader. Please run it before you trust the 0.
- **U and KE reach 19.0 % on one drop each,** right at the lane limit.
- **The square has no ring.** At 57.0 m its NW and SE ends need too much cut/fill for the pieces in the ring list. The square is framed by the main street's rows, the landmark and the two comps instead.
- **The cross lanes run at 9-17 %,** which is steep for vehicles. They are foot and light-vehicle links; the AI road is M.
- **HR is your v4 road unchanged.** It reaches 30.8 % at its steepest point. I didn't grade it; it's yours.
- **The top lane U2 is new ground,** uphill of v5's town. It adds the buildings v5 had on rows that can't keep a level under the rule.

## Open questions
1. **Is the "block" reading right?** I read a block as one level segment of a street plus its two rows, cut by a gap at each cross lane.
2. **Is U2 (new ground uphill) acceptable,** or should the town stay inside v5's footprint at about 77 buildings?
3. **Should the square have a ring?** It would need a cut/fill target of about 3.5 m on its two ends, or shorter pieces than the list holds.
