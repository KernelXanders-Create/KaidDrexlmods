# KERNEL_RETURN_K6_REPASS_ALL_v1: all seven towns, re-passed against your 11 Nov grader (PROPOSED)

**Every town reads "seated N of N" and "checks failed: none" on your grader.** I ran `grader/town_grader.py` from your pack, unchanged, with the 5 m files and the corners in your table (`--fixed perys_fixed.json` for Perys). Each run exits with code 0. First I confirmed my install: all five of your `--expect` runs print `MATCH`.

| Town | Folder | Seated (your grader) | Before (your grading / mine) | Garrison (enterable) | Square: level, landmark |
|---|---|---|---|---|---|
| Perys v7 | `perys_v7/` | **69 of 69**, checks failed: none | 39 of 98 | 40 (49) | 57.0 m, ND07 |
| Sound Head v2 | `sound_head_v2/` | **27 of 27**, checks failed: none | 4 of 61 | 15 (15) | 33.0 m, ND06 |
| Causeway Foot v2 | `causeway_foot_v2/` | **79 of 79**, checks failed: none | 25 of 82 | 40 (53) | 1.5 m, SF02 |
| Kastro Quay v2 | `kastro_quay_v2/` | **34 of 34**, checks failed: none | 16 of 56 | 25 (25) | 134.0 m, SF02 |
| Lantern Quay v2 | `lantern_quay_v2/` | **51 of 51**, checks failed: none | 21 of 64 (mine) | 33 (33) | 75.25 m, SF03 |
| Kamar Village v2 | `kamar_village_v2/` | **42 of 42**, checks failed: none | 17 of 59 (mine) | 28 (28) | 248.0 m, SF02 |
| Oyra v2 | `oyra_v2/` | **106 of 106**, checks failed: none | 42 of 119 (mine) | 55 (78) | 129.75 m, ND07 |

"Before": the first four are your 11 Nov grading of my returns. The last three are my own grading of the K6 returns you hadn't graded, run with your grader.

## What is in each town folder
- `<town>_layout.json`: the layout in your return schema. Every street has `points_z`; every building has `pad_z_m`, `street` and `role`; the square has one `level_z_m`.
- `grader_<town>/report.md`, `plan.png`, `buildings.csv`, `result.json`: your grader's own output for that layout, exactly as it wrote it.
- `<town>_plan.png`: my drawing of the same layout (streets with their levels, doors, garrison).

`tools/` holds the engine and the seven town files, to read as text:
- `town_grid.py`: the engine.
- `gtown.py`: the grader-backed placement (below).
- `run_graded.py`: lays out a town, then calls your grader on it.
- `diag.py`: finds the two fixed points behind any ungradable ground point.
- The seven town files.

## How I got every town to pass
**The engine now asks your grader before it places each building.** `gtown.py` imports `town_grader.py` and builds the ground your way:
- the grid from your 5 m file;
- every street's claim (half-width + 3.54 m, at its own level, stepping down on ramps);
- the square, in your order (your order at Perys).

Then, for each candidate house, it calls your own tests: overlap, ribbon (0.2 m own street, 1.0 m others), clash, cut/fill 4.0 m and the 31° bank, with your pad rule (1.5 m, rear 0.4 m for street rows). A house that fails is not drawn, and the engine tries the next model or spot.

Overlap, clash and bank are pairwise, and ribbon and cut/fill are per building. So a set that passes one by one in my order also passes in your order. Your grader confirms it on all seven.

**Changes in the designs:**
1. **Squares sit on one level stretch of their street,** at least 11 m clear of its ramps at both ends. Where a street's stretches were too short, I hold one level stretch around the square's site. Squares are smaller where the slope needs it, to stay within 4.0 m.
2. **Stairs are no longer drawn as streets.** A stair steeper than the 31° bank can't be graded ground, so the stair paths caused all the ungradable points. They are listed in each layout's `notes` with their ends and levels, to build as stair pieces:
   - Sound Head: three terrace stairs and the quay stair;
   - Lantern Quay: the escarpment stair, plus the stepped main street and side stairs;
   - Kastro Quay: the cliff stair, now a lift and stair, and the south road;
   - Kamar Village: the quay path;
   - Oyra: two look-out stairs.
3. **Terraces are spaced for the bank, and cross lanes get level landings.**
   - **Sound Head:** 12 m between terraces (11 / 23 / 35 / 47 / 59 m), about 50 m apart, with rows at most 12.5 m deep.
   - **Lantern Quay:** the terraces stop short of the escarpment, so the ground down to the quay lane can be graded.
   - **Kastro Quay:** its cross lane has 8 m level landings at each end.
4. **Share caps use your twin groups** (`TWIN` in your grader). After placement, the newest house of an over-share group is removed until every model is at most 15 % and every twin group at most 12 %.
5. **Comps:** a comp keeps its footprint and `pad_z_m` only if it seats by your comp test. Otherwise it stays a role with x, y, marked "(no level pad found here that the grader seats ...)". At Sound Head both comps seat; at Perys the quay comp seats. Everywhere else they are roles only.

## Town by town (all MEASURED by your grader unless marked)
- **Perys v7** (third pass): main street M, lanes U / U2 / KW / KE, cross lanes, the quay group on your 2.2 m apron, and your harbour road as built.
  - Square on M's level stretch at 57.0 m, 36 x 12 m, open to the sea; ND07 on it.
  - Pad cut/fill median 2.10 m, max 3.79 m.
  - Your v5 is in for Saturday; this one is for the record.
- **Sound Head v2:** five terraces, rows on the uphill side; gate square at 33.0 m (36 x 10 m); ND06 on it.
  - 27 buildings, 15 enterable. **The garrison can't reach 40 here:** on a 24 % slope your bank rule leaves room for five terraces with one shallow row each.
  - Cut/fill median 3.20 m, max 3.94 m.
- **Causeway Foot v2:** the 8 m AI main street (12.1 % on its drops), four contour lanes and the beach-side lane.
  - The only main-street stretch long enough for a one-level square is at the causeway landing. So the square moved there (1.5 m, 32 x 16 m), about 70 m east of the K1 fork; SF02 on it. ASSUMED: you may prefer it called the causeway gate square.
  - Cut/fill median 2.85 m, max 3.98 m (52 of 79 over 2.5 m).
- **Kastro Quay v2:** option (b), as before; the plateau-grading question is still open (below).
  - Square on the ridge (134.0 m); SF02 on it.
  - 34 buildings, 25 enterable. **Garrison 25.**
  - Cut/fill median 2.96 m, max 3.95 m.
- **Lantern Quay v2:**
  - five terraces (58-90 m) with one row each;
  - the quay row (8 buildings) on the beach strip;
  - square on the 74 m terrace's uphill side (75.25 m), with SF03.
  - **Garrison 33.**
- **Kamar Village v2:** the upland shoulder; main street along the hollow; square at 248.0 m with SF02; the quay landing with 3 houses. **Garrison 28.**
- **Oyra v2:** the flat rim; rim street, two lanes, square on the cliff side at 129.75 m with ND07 (the slimmer tower: SF02 ran over the cliff edge). 106 buildings, garrison 55. Cut/fill median 1.90 m.

## What is weak, honestly
- **Four towns are under the 40 garrison minimum:** Sound Head 15, Kastro Quay 25, Kamar Village 28, Lantern Quay 33. In each, every enterable building is garrisoned. The ground and your rules seat no more as these towns are laid out. More would need terrace grading (Kastro Quay), a gentler site (Sound Head), or more lanes on the K1 slope (Kamar Village, Lantern Quay). I'd rather ask than guess.
- **Cut/fill runs high:** most towns have a median of 2-3 m and many pads between 2.5 and 4.0 m. The engine now uses your 4.0 m limit directly; the 2.5 m aim is a report in your grader.
- **Squares have few or no ring buildings,** because with your rear-pad and clash rules ring houses rarely fit beside the landmark. The squares are framed by their streets' rows.
- **The stairs are notes, not drawn pieces.** You'll need to place them.
- **"Banks facing streets" and "street grades" are reports in your grader.** Some lanes and cross lanes are over 19 % on single drops: the grader lists them, and they don't count as failures.

## Open questions
1. **Garrisons under 40** (Sound Head, Kastro Quay, Kamar Village, Lantern Quay): accept them as they are, or say which lever to pull per town (grading, site, or more lanes)?
2. **Kastro Quay:** may the plateau be graded into broad terraces? That is still the main open question for that town.
3. **Causeway Foot:** is the square at the causeway landing acceptable, or should the main street hold a level stretch at the old fork? That would mean a longer level main street there and fewer houses on the climb.
4. **Stairs as pieces:** is a list of stair ends and levels in `notes` enough, or should I draw them in a separate `stairs` list in the layout?

## How to re-run
- **Grade a layout:**
  ```
  python grader/town_grader.py <town>/<town>_layout.json --grid5 heights_5m/<site>_natural_5m.npy X0 Y0 --out <folder>
  ```
  Use the corners from your table. For Perys, add `--fixed grader/perys_fixed.json`.
- **Re-make a town:**
  ```
  python3 tools/run_graded.py <town file> <catalogue.json> <out>
  ```
  Set `GRID5_DIR` to your `heights_5m` folder, and point `PACK` in the town files at your 10 Nov pack.
