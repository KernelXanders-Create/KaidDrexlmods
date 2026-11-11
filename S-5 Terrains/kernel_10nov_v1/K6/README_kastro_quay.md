# KERNEL_RETURN_K6_kastro_quay: Kastro Quay on the real ground, under the 5 m grid rule (PROPOSED)

| File | What it is |
|---|---|
| `kastro_quay_layout.json` | Layout in your return schema (map frame). Streets carry `points_z` and their level `segments`. 56 buildings with `pad_group`, `pad_z_m`, door side and bearing, `cut_m` / `fill_m`. Also the square (one level), comps (cargo lift head, square market, quay slips) and notes. |
| `kastro_quay_plan.png` | Plan: north up, 100 m scale bar, map coordinates, the 5 m height grid, street levels (blue numbers), doors and garrison. The inset shows the port square, the cliff stair and the quay. |
| `kastro_quay_checks.json` | Every self-check number, as data. |
| `tools/town_grid.py`, `tools/run_town.py`, `tools/kastro_quay.py` | The engine and this town's hand design, to read as text. **Engine change:** a new "adaptive" mode ends a level stretch of street where the ground under its frontage drifts more than ±1.5 m, and sizes each drop gap to the street's grade limit. Sound Head, Perys v6 and Causeway Foot don't use it, so their results are unchanged. |

**Window used:** the shore window `towns6/kastro_quay/shore_height_1m.npy` (4263..4963, 16423..17123).

**Where the site moved:** from the K1 point (about 4300, 16850, at 241 m) about 300 m east, onto the cliff-top plateau. The buildings span x 4480-4668 and y 16624-17035 (MEASURED). The port square is at about (4655, 16823).

## Option chosen: (b), the whole town on the plateau, with a quay only
- **The sea cliff is 130 m high and about 100 m wide in plan** (MEASURED: 136 m at x 4660 to 9 m at x 4790, on y 16825). A road down it at 12 % would need about 1.1 km of switchbacks, more than the whole window. So option (a)'s hamlet-plus-road can't be linked by a road here, and the shore strip has room for an apron but not a hamlet.
- **The quay:** a 30 x 20 m apron at 2.0 m (ASSUMED) in the small cove behind the low rock spit at x 4800, y 16740-16830.
  - It holds a boat-slip comp.
  - A foot-only cliff stair (QS, 11 zig-zag legs) climbs to the port square, alongside a cargo lift head (a comp, your pick).
  - There are no buildings on the apron.

## What the plateau really is
It is not flat. It is a low dome: a ridge at 133-137 m along x ≈ 4625, falling:
- west into an old crater bowl (floor 108 m);
- north into a shallow basin (117-121 m);
- east to the cliff edge.

There are rock knobs a few metres high on it. Only the ridge top is truly level (MEASURED: 132-137 m for 230 m along the main street's line). Everywhere else the ground under a 17 m-deep row moves 3-5 m, which is more than the 2.5 m pad target.

## Layout
- **Main street (7 m) along the ridge:**
  - levels 132.75, 135.5, 135.0 and 134.0 m;
  - it passes the port square on its east side;
  - it then drops (at up to 12 %) to the north basin at 122.25 and 121.0 m and ends at the north port.
- **Port square:**
  - It is one level (134.0 m), 46 x 54 m, on the cliff top.
  - Its east side is open to the Kastro Strait.
  - The landmark is SF02 (20.5 m), standing in for the Supply Port Control Spire.
  - The ring is SF08, SF13 and WH09 on its north side, plus a market comp and the cargo lift head.
- **Other streets:**
  - a west lane on the dome's west flank, 119-134 m, linked to the main street by two ramp lanes;
  - a basin lane to the east;
  - a lower quarter in the crater bowl (the bowl lane, 108.25 m), reached from the south port by the bowl lane south.
- **Road out:** the south road SL follows the ground (17 % average) and is yours to grade.

## Self-check (MEASURED by `tools/town_grid.py` on the shore window)
| Check | Result | Pass? |
|---|---|---|
| Grid points (every 5 m) claimed by two pad levels | **0** | pass |
| Pads at different levels closer than 14 m (17 m at 45°) | **0** (closest 16.0 m) | pass |
| Pad cut or fill | median 2.30 m, max 3.47 m. **24 of 56 are between 2.5 and 3.5 m** (listed in the checks file). None over 4.0. | pass, 24 listed |
| Overlaps; footprint into a street | 0; 0 | pass |
| Corner houses within 2 m of a cross street | 0 | pass |
| Doors: 3 m out lands on a street or the square | 56 of 56; door level within 0.75 m for all | pass |
| Lane ends vs the level of the street they join | 0 mismatches over 0.3 m | pass |
| Straight runs (m) | streets 35-70; cross lanes 53-59 | pass |
| Grades: main street | 12.0 % on its drops, 3.0 % average | pass |
| Grades: lanes | up to 19.0 % | at the limit |
| Grades: cross lanes | 10-13 % | pass |
| Grades: south road out | 17 % average, 52 % on one short stretch | **yours to grade** |
| Street cut / fill | at most 3.2 m / 4.1 m (main street, bowl lane) | **fill over 4 m on the bowl lane** |
| Largest model | ND01 12.5 % | pass (15 % rule) |
| Largest same-footprint group | the four 13.4 x 16.5 m prefab models SF01 / SF08 / SF15 / SF16, 12.5 % | **0.5 pt over my 12 % cap** (your cap names only WH11 + WH24, at 8.9 %) |
| Buildings / garrison | **56 / 40** (every enterable building is garrisoned) | garrison at the minimum |
| Tall pieces | 1: the landmark, on the square | pass |
| Pad levels | 12 (108.25 to 135.5 m) | |

## What is weak, honestly
- **56 buildings, half of K1's 108, and it reads as a scattered village, not a town.** The plateau is a dome with rock knobs. Under one level per street stretch, a 2.5 m pad target, a 3.5 m ceiling I allowed here, and 14 m between levels, only the ridge, the bowl floor and parts of the basin take rows.
- **24 pads need 2.5-3.5 m of cut or fill** (target 2.5). Your full grader reads up to 1.9 m more, so some may fail it.
- **The garrison is exactly 40,** the bottom of your range.
- **The quay has no buildings** and is reached only on foot or by the lift.
- **The road ports are ASSUMED.** The south road out is a 17 % climb as drawn, and the citadel road beyond it is yours.

## Open questions
1. **May the plateau be graded?** A real town on this dome would be cut into 3-4 broad terraces first. If your tools may flatten, for example, the ridge (about 134 m) and the north basin (about 120 m) as whole-quarter pads, this site could take about 100 buildings again. That is my main question for this town.
2. If not: **is a 56-building Kastro Quay acceptable,** or should the platoon objective move to a better site?
3. **The quay:** is a stair plus a cargo lift acceptable for the supply port's story, or do you want the switchback road of option (a) outside this window?
