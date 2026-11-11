# KERNEL_RETURN_K6_kamar_village: Kamar Village on the real ground, under the 5 m grid rule (PROPOSED)

| File | What it is |
|---|---|
| `kamar_village_layout.json` | Layout in your return schema (map frame). Streets carry `points_z` and their level `segments`. 59 buildings with `pad_group`, `pad_z_m`, door side and bearing, `cut_m` / `fill_m`. Also the square (one level), comps and notes. |
| `kamar_village_plan.png` | Plan: north up, 100 m scale bar, map coordinates, the 5 m height grid, street levels (blue numbers), doors and garrison. The inset shows the quay landing on the beach strip. |
| `kamar_village_checks.json` | Every self-check number, as data. |
| `tools/town_grid.py`, `tools/run_town.py`, `tools/kamar_village.py` | The engine and this town's hand design, to read as text. **Engine fix:** the adaptive mode now stops cleanly when a drop gap runs past a street's end. Kastro Quay and Lantern Quay re-run identically. |

**Ground used:** the site window and the shore window, stitched into one height grid. They are identical where they overlap (MEASURED, max difference 0.0 m). The two corners that neither window covers take the nearest value. They are outside the town and the quay.

**Where the site moved:**
- **Village:** about 190 m west of the K1 point (16850, 11600). It spans x 16573-16793 and y 11500-11790 (MEASURED). The square is at about (16651, 11684).
- **Quay landing:** on the beach strip at about (17195, 11125-11235), about 650 m south-east of the village.

## Why the village moved west
- **The K1 point sits on a 25-35 % slope** (MEASURED: median 32 % around it). On that slope, two rows can't share a level and pads would need 4 m or more.
- **150-200 m west lies a gentle upland shoulder (240-258 m)** with a shallow north-south hollow at x ≈ 16640. The hollow runs between a low knob (257 m, east) and the massif slope (west).
- **The village sits along that hollow:** it is the "ravine village" of K1 on real ground. It keeps your "up at the site, on terraces" note, about 200 m from the point.

## Layout
- **Main street (6.5 m) along the hollow:**
  - 4 level segments: 246.0, 253.0, 248.0 and 243.75 m;
  - it drops at up to 12 % between them (0.9 % average).
- **Two parallel lanes** about 60-70 m either side, both with rows on both sides:
  - the knob lane (east), 247.75-256.75 m;
  - the massif lane (west), 251.5-259.5 m.
- **Two one-row lanes** at the edges of the shoulder:
  - an east edge lane over the slope toward the K1 point;
  - a north lane over the bench edge.
- **Ramp cross lanes** meet each street at its level.
- **The square:**
  - one level (248.0 m), on the east side of the main street's 248 m segment, open onto the main street;
  - about 17 x 34 m;
  - the landmark is SF02 (20.5 m, sci-fi), standing in for the Moisture Condenser Tower;
  - 4 ring buildings on its ends and its east side, plus a cistern or market comp.
- **The quay landing:**
  - 3 buildings (WH03, WH19 x2) at the cliff foot, on a short beach lane at 2.5-4.25 m, doors to the sea;
  - a 2.0 m apron (ASSUMED) with a slip and jetty comp;
  - the review asked for 3-5 buildings.
- **The path down to the quay (QP)** runs 646 m past the K1 point. It drops 245 m at 38 % average, steeper on the cliff. The line is ASSUMED, a foot path only, and yours to route (switchbacks).

## Self-check (MEASURED by `tools/town_grid.py` on the stitched ground)
| Check | Result | Pass? |
|---|---|---|
| Grid points (every 5 m) claimed by two pad levels | **0** | pass |
| Pads at different levels closer than 14 m (17 m at 45°) | **0** (closest 17.1 m) | pass |
| Pad cut or fill | median 1.88 m, max 2.50 m; none near the limit | pass |
| Overlaps; footprint into a street | 0; 0 | pass |
| Corner houses within 2 m of a cross street | 0 | pass |
| Doors: 3 m out lands on a street, the square or the quay | 59 of 59; door level within 0.75 m for all | pass |
| Lane ends vs the level of the street they join | 0 mismatches over 0.3 m | pass |
| Straight runs (m) | streets 27-68; quay lane 47 | pass |
| Grades: main street | 12.0 % on its drops, 0.9 % average | pass |
| Grades: lanes | up to 19.0 % | at the limit |
| Grades: cross lanes | 4-13 % | pass |
| Grades: quay path | 38 % average | it is a hill path (yours) |
| Street cut / fill | at most 2.3 m / 4.0 m (east edge lane, 4.02 m fill) | **fill at the 4 m line** |
| Largest model / twin group | ND03 11.9 %; WH11 + WH24 11.9 %; 22 models | pass (12 % cap) |
| Buildings / garrison | **59 / 40** (42 enterable) | garrison at the minimum |
| Tall pieces | 1: the landmark, on the square | pass |
| Pad levels | 14 | |

## What is weak, honestly
- **59 buildings, not K1's 82.** The shoulder is about 220 x 290 m and undulates by 15 m. Under one level per street segment only about a third of the main street is level frontage (three short segments), so most buildings stand on the lanes.
- **The garrison is exactly 40,** the bottom of your range.
- **The sci-fi read is thin:** 2 pieces (the tower stand-in and one block). The CIS billets K1 put on the quay are now three plain houses on the landing.
- **The quay is far:** 650 m and 245 m below, by a steep path. That is what the real coast gives (your flag: 79 % of the shore over 20°).

## Open questions
1. **Is the move about 190 m west to the shoulder acceptable,** or must the village stay on the K1 point's slope? There it would be one-row terraces like Sound Head, at about 40-50 buildings.
2. **The quay path:** should I draw a full switchback line, or will you route it?
3. **Better cove:** I saw none in the shore window. The beach strip at x 17185-17215, y 11120-11235 is its widest flat part (about 30 m at 1-3 m).
