# KERNEL_RETURN_K5: Perys v5 on the real ground with the real catalogue (PROPOSED)

## What is in this zip
| File | What it is |
|---|---|
| `perys_layout.json` | **The layout, in your return schema.** Map frame. Streets with `points_z`; 104 buildings (catalogue `model_id`, footprint centre, `yaw_deg`, `door_side`, `door_bearing_deg`, `pad_group`, `pad_z_m`, `garrison`, plus `cut_m` / `fill_m` / `street` / `role`); square and landmark; walls (none, see below); comps; town ground; notes. |
| `perys_plan.png` | The plan: north up, 100 m scale bar, map coordinates on the edges, doors marked (green ticks point out of each door), garrison outlined red. Insets show the quay group and the square. |
| `checks.json` | Every self-check number below, as data. |
| `k0_readchecks.json`, `k0_readchecks_figure.png` | My K0 read-checks run on v5 with the same script I used on v4, for a like-for-like comparison. |
| `tools/perys_v5.py`, `tools/k0_readchecks.py` | The scripts, to read as text (you don't need to run them). |

## The design in words
- **Main street (M, 8 m, the AI road)** starts exactly at the NW road port (5087.3, 3408.5) at 59.40 m. It runs south-east diagonally down the slope at up to 4.5 %, so its level steps down about 10 m over 311 m instead of sitting on one contour. Pads follow it down in many small steps: 53 distinct pad levels (v4 had 5).
- **Upper lane (U) and lower lanes (K, K2), 5 m,** run about 35 m and 49-77 m from the main street. That spacing fits **two rows back to back**: one row fronts the main street, the other fronts the lane. So blocks are two buildings deep and **every door is on a street** (104 of 104 pass the door check).
- **Four cross lanes (C1-C4)** and one stair path (UP) tie the lanes together.
- **The harbour link (HL)** runs from the lower lane down to the start of your v4 harbour road (HR), which I kept unchanged.
- **Blocks:** neighbouring houses in a block touch (0.08 m) on one shared pad: 67 pad groups for 104 buildings. A block ends when the street level at a door drifts more than 0.8 m from the pad. The next block steps on at 0.31 m (just over your 0.3 m minimum), with a 2.8-4.0 m passage every 4th block.
- **The square** sits on the main street's downhill side, about 1,630 m², open to the north-east (the sea).
  - **Two terraces:** upper at 55.4 m beside the main street, lower at 53.2 m toward the sea, with one flight of steps. (The natural ground under the square runs 51.5-57.0 m, so one level would need about 4 m of fill.)
  - **Landmark:** ND07, the 29 m Naboo tower, stands on the square.
  - **Doors face the square from 3 sides** (NW 3, SE 2, main-street side 2). The NE side stays open.
  - **Three comps:** a market and a covered hall on the upper terrace, a stall or fountain group on the lower, covering 15.5 %.
- **The main street and the square read sci-fi:** 12 of the main street's 27 buildings are sci-fi prefab modules, the square ring is sci-fi, and the landmark is on the square.
- **The quay group:** four low halls (IN01, SF15, IN02, SF16) on the apron's landward strip, x 5652-5710 and y 3547-3564, pad 2.2 m. Doors face north onto the quay. Your v4 landing-pad comp is kept where it was. Your harbour road ends inside the apron's west end, so the halls start at x 5652, clear of it.

## Self-check (all MEASURED by `tools/perys_v5.py` on `height_perys_natural_1m.npy` with your definitions)
| Check | Result | Pass? |
|---|---|---|
| Pad cut or fill (footprint + 1.5 m, sampled every 1 m) | median 1.86 m, max 3.14 m. **9 near the limit (2.5-4.0 m):** B008 2.94, B009 2.60, B012 3.14, B022 2.84, B023 2.63, B024 2.59, B026 2.54, B028 2.64, B087 2.54. **None over 4.0 m.** | pass (9 listed) |
| Overlaps: building pairs | 0 (buildings on different pads at least 0.3 m apart; on the same pad, touching only) | pass |
| Overlaps: footprint vs street ribbon | 0 | pass |
| Longest straight run per street (m) | M 71.7, U 79.5, K 49.4, K2 71.3, C1 41.8, C2 33.2, C3 43.5, C4 54.8, UP 36.4, HL 64.3. (HR is yours, unchanged, at 213.7.) | pass (U is close at 79.5) |
| Largest model share | 9.6 % (WH11 / ND03 / WH24 / WH19, 10 each); 26 distinct models | pass (under 15 %) |
| Door side (a point 3 m out from the door face lies on a street ribbon + 0.6 m, the square or the quay) | 104 of 104 | pass |
| Street grades on natural ground (max) | M 4.5 % (limit 5); lanes 3.1-15.8 % (limit 19); UP path 11.2 % | pass |
| Street cut into the slope (max along the centre line) | M 0.22 m, lanes 0.21-0.83 m (fill at most 1.89 m on M) | pass (limit 4 m) |
| Buildings | 104 (target 90-110): square 5, landmark 1, main street 27, lanes 67, quay 4 | pass |
| Garrison (enterable only) | 50 of 67 enterable | pass (40-55) |
| Tall pieces (over 14 m) | 1: the landmark ND07 on the square. None on a street edge or a shore. | pass |
| Blank wall over 15 m on a street edge | 0. SF09 was dropped (its 20 m blank left side faced a lane); no SF02 / SF05 / SF06 used. | pass |
| Retaining walls | **0 pieces.** No street edge without a building has a bank over 1.5 m within 3 m, because the streets sit within 0.8 m of the natural ground. | see note |
| Town ground | 33,161 m² (v4 61,302 m²; limit 79,700 m²). The town is denser, not bigger. | pass |
| Building footprint to street area (inside the town ground) | 2.09 (v4 0.95) | (K0 check) |

**K0 read-checks, v5 vs v4** (same script, `k0_readchecks.json`):

| Read-check | v5 | v4 |
|---|---|---|
| Lane street-wall continuity | 38-82 % | 0 % |
| Main street continuity | 65 % | MS 52 % |
| Frontage buildings set back over 1 m | 7.4 % | 51 % |
| Doors within 2° of square-on | 64 % | 93 % |
| Distinct pad levels | 53 | 5 |
| Landmark distance from the square | 0 m | 75 m |
| Square comp cover | 15.5 % | 7.9 % |
| Pads over 2.5 m of cut or fill | 8.7 % | 30 % |

**Still failing my own K0 thresholds** (honest):
- Touching groups of 3 or more: 48 % (target 70 %).
- Main-street continuity: 65 % (target 70 %).
- Cross lanes C1 (38 %) and C4 (44 %) are under 50 %.
- The upper lane runs about 35 m from the main street, which my rule 13 calls a "parallel band". It's the spacing that makes back-to-back blocks work, and I'd now set rule 13's lower bound at 40 m.

## What I could not check
- **Your full grading check.** Mine is the simple footprint + 1.5 m sample; you said yours reads up to 1.9 m more. The 9 near-limit pads are the ones to watch.
- **Door sides marked "assumed"** in the catalogue: all the sci-fi prefab modules (SF01/08/15/16) on the main street and square. I used them for the sci-fi read. If their door isn't on the back, they need turning 180°.
- **Lamps, and how the square's two terraces and steps are graded** (that's your tooling).
- **AI convoy behaviour** on the 8 m main street.
- **The harbour road's grade on natural ground** reads up to 30.7 % on short pieces (9.7 % average). That's your HR, graded by your tools, so I left it.

## Open questions
1. **Main-street grade.** I kept it under 5 % (your rule). With 6-8 % allowed (K0 question 1), the main street could cross more contours, and both the near-limit pads and the "parallel band" would shrink.
2. **Square comps:** I left roles and sizes (10 x 10, 9.5 x 9.4, 8 x 8 m) for you to pick real comps.
3. **Should the quay group sit on your harbour road's end** instead of next to it? Tell me if the apron's west end is free.

**Not done:** the K6 towns (next job), and any in-game look.
