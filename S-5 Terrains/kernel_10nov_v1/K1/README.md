# KERNEL_RETURN_10NOV_K1: town plans for the six undesigned towns (PROPOSED)

Job K1 from the 10 Nov work pack. Islands "Ember Caldera", weeks 2-4. These are plans and data for Miran's look, not game files. Miran's in-game look decides.

## What is in this zip
| File | What it is |
|---|---|
| `README.md` | This page |
| `TOWNS.md` | One section per town: role in its op, approaches, look, measured plan numbers, the garrison list with each building's job |
| `towns/<town>_plan.png` | The plan drawing: north up, 50 m scale bar, metres, legend, measured box |
| `towns/<town>_plan.json` | The same plan as data: street centre lines, the square, the landmark, blocks, every building footprint with height class, family and garrison flag |
| `tools/` | The Python that made it (`make_towns.py`, `town_lib.py`, `towns.py`, `make_report.py`) and `checks.txt` |

| Town | Op | Site | Size | Buildings | Garrison |
|---|---|---|---|---|---|
| Sound Head | 3 | 3-M3 | platoon | 104 | 13 |
| Causeway Foot | 4 | 4-M3 | platoon | 96 | 13 |
| Kastro Quay | 5 | 5-M3 | platoon | 108 | 13 |
| Lantern Quay | 5 | 5-09 | squad | 66 | 10 |
| Kamar Village | 6 | 6-01 | two-squad | 82 | 11 |
| Oyra | 7 | 7-M2 | platoon | 106 | 13 |

Perys (op 1) and the Rim Chora (op 7) are yours, as the pack says, and are not touched.

## How the plans were made (so you can judge them)
- **By hand, per town:** the coast or cliff edge, the one bent main street, the lanes, the square, the landmark, the approaches, and where the sci-fi core sits (`tools/towns.py`).
- **By script:** packing building footprints along those hand-drawn frontages, so they touch, sit at the street edge and have uneven widths. Then filling the ground between streets so blocks are deep, not one house thick. Then trimming from the outside in, so each town keeps a dense core along its main street and quay.
- The script also turns any lane end with no houses into a "road out of town", so no empty wide street is left. It then checks every rule below and draws the plan.
- The builders still place every real asset by hand. The plan says where the mass, the street wall, the square and the garrison are.

**Answers to what failed last time** ("houses in rows, wide empty streets, no dense core"):
- **Rows:** 92-96 % of buildings sit in touching blocks, and blocks run 2-3 buildings deep around the core.
- **Wide empty streets:** the main street is 6.5-8 m and lanes are 4-6 m, frontages sit at the street edge, and unbuilt lane ends become paths.
- **No dense core:** each town's sci-fi core is the cluster round its square and quay, the nearest roughly 22 % of buildings plus the CIS quay zone.

## Checks (MEASURED by `tools/make_towns.py`; all six PASS, see `tools/checks.txt`)
- 60-110 buildings.
- At least 75 % of buildings in blocks (a block is 3 or more touching).
- One main street, 6-8 m wide; lanes 4-6 m.
- No straight run over 80 m on the main street or any lane. A run is measured as the longest piece of centre line that stays within 1.5 m of its chord. The worst result is Oyra's main street at 75.7 m. Some roads out of town are longer and straighter (up to 123 m at Causeway Foot's causeway); they have no frontage.
- Garrison of 10-15 buildings.
- Frontage widths are uneven: coefficient of variation 0.2 or more, measured 0.22-0.23, with widths 6-15 m. No houses at even spacing.
- A square with one sci-fi landmark; a harbour quay or cliff edge used on purpose. The quays keep a 12 m open apron along the water. Oyra's houses stand on the cliff edge.

## The look (words; the plans show families by colour)
- **White cube houses** are the body of each town (40-69 %).
- **Naboo domes** sit on corner and lane-head buildings (11-15 %).
- **A clear sci-fi core** (15-38 %): a sci-fi landmark on each square, plus CIS halls on the quay or gate. Lantern Quay is the lowest at 15 of 66, on purpose, because it is a civilian fishing hamlet.
- The ground in the drawings is red-ochre scoria, not Earth tan, which keeps it apart from Sarrak.
- Per-town look notes are in TOWNS.md. This follows the purpose map's direction: Malden white cubes, 3AS Naboo domes, banded red and black cliffs, blue and red-leaf scrub.

## Not done
- No terrain heights inside the towns. The plans are flat. Slopes, terraces and stairs need the Stage B heightmap; Oyra and Sound Head will be steep.
- No asset picks per footprint (which Malden house or which Naboo piece), and no interiors chosen. REV2 rule 6 says every interior other than the capstone is a library interior, so each garrison building should be an enterable library building.
- Perys and the Rim Chora (yours).
- No in-game check of any kind. Nothing here needs Arma.

## Open questions (with the default I used)
1. **Three sketch site points sit high above the water,** but their roles are harbour towns:
   - Sound Head: the site is at 384 m ground, 156 m from the coast.
   - Kastro Quay: 259 m ground, 567 m from the coast.
   - Kamar Village: 222 m ground, 544 m from the coast.

   This is MEASURED in `objectives_v2.json`.
   **Default:** I drew them as harbour towns at the water, so the site point moves down to the shore in Stage B. The other option is an upper town with a separate quay hamlet (more buildings, more work).
2. **Lantern Quay is a squad site,** but the pack asks for 60-110 buildings. **Default:** 66 buildings with 10 garrisoned; the rest are empty dressing. Say if you want it smaller (about 30-40).
3. **Town size.** The towns measure about 120-230 m by 130-260 m. I don't know your Aparra kit towns' footprint. **Default:** this size. Say if your kit towns are bigger or smaller and I'll scale.
4. **Sci-fi share.** The core runs 15-38 % sci-fi. Is that "clear" enough to not read as an Earth village? **Default:** yes, with the landmark and the CIS quay halls as the signal.
5. **Causeway Foot's 8 m main street is op 4's AI road** through a dense town. Street walls at the edge leave a clean 8 m lane with gentle bends (longest straight run 48 m), but AI convoys in towns are untested by me. **Default:** keep it, and flag for your convoy test.
6. **Oyra's cliff lanes end in look-outs, not routes** down the 300 m cliff. **Default:** dead ends on purpose. The Skala path to the Yard belongs to the Rim Chora, not Oyra.
7. **Local frame placement.** Each JSON's local origin is set on its site point by eye, ASSUMED. **Default:** you re-seat each plan on the Stage B coast.

## Measured, assumed, unsure
- **MEASURED** (by the scripts, on these plans): building counts, block share, family and height counts, frontage widths and spread, street widths and lengths, straight runs, square areas, extents, garrison counts. Also the source facts I read from `objectives_v2.json`: site positions, ground heights, coast distances and the nearby sites.
- **ASSUMED** (design): every shape, position and footprint, the family and height of each building, and the garrison choice.
- **Unsure:**
  - Whether the footprint sizes (about 40-250 m² each) match your Malden and Naboo pieces.
  - Whether 12 m quay aprons are wide enough for your quay pieces.
  - How the plans sit on real slopes.
