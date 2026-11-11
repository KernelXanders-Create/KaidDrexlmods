# KERNEL_RETURN_K6_lantern_quay: Lantern Quay Hamlet on the real ground, under the 5 m grid rule (PROPOSED)

| File | What it is |
|---|---|
| `lantern_quay_layout.json` | Layout in your return schema (map frame). Streets carry `points_z` and their level `segments`. 64 buildings with `pad_group`, `pad_z_m`, door side and bearing, `cut_m` / `fill_m`. Also the square (one level), comps and notes. |
| `lantern_quay_plan.png` | Plan: north up, 100 m scale bar, map coordinates, the 5 m height grid, street levels (blue numbers), doors and garrison. The inset shows the quay row on the beach strip. |
| `lantern_quay_checks.json` | Every self-check number, as data. |
| `tools/town_grid.py`, `tools/run_town.py`, `tools/lantern_quay.py` | The engine (unchanged since Kastro Quay) and this town's hand design, to read as text. |

**Tile used:** `towns6/lantern_quay/height_1m.npy` (7050..7750, 16300..17000). There is no shore window; the shore is inside this tile.

**Where the site moved:**
- The hamlet now spans x 7260-7529 and y 16340-16677 (MEASURED).
- The quay row moves about 280 m south-south-west of the K1 point (7400, 16650), down to the real shore, as your review asked.
- The pocket square is at about (7391, 16533), 120 m south of the K1 point.
- The top terrace reaches the K1 point's level (91 m).

## The ground (MEASURED)
- **A beach strip, 20-40 m wide at 1-8 m,** runs along the shore.
- **Above it, a sea escarpment 25-40 m high,** too steep for buildings (35-100 %).
- **Above that, a 15-25 % slope** climbs north-east to the K1 site (84 m) and the beacon path.

## Layout
- **The quay row stands on the beach strip:**
  - 7 buildings (two SF15 sheds, WH01, WH11 x2, WH12 x2), at levels 3.0 / 4.5 / 6.25 m;
  - they stand on the seaward side of the quay lane, doors on the lane;
  - the quay apron (2.0 m, ASSUMED) and a boat-slip comp are at the west end.
- **A foot stair climbs the escarpment (QS):** 11 legs, 24.5 % average, stair-steep on its legs. No vehicle road is needed: the hamlet is boat and air only.
- **Six terraces on the contours above the escarpment,** at about 52, 60, 68, 75, 83 and 91 m, about 35 m apart.
  - At 20 % two facing rows can't share a level (the same finding as Sound Head), so **each terrace carries one row, on its uphill side**, at one level per segment.
  - The closest pads at different levels stand 17.3 m apart.
- **The stepped main street (6 m) is the middle spine:** 4 ramp pieces zig-zagging up the terraces at 11-15 %, each meeting its terraces at their level.
  - Two side spines (4.5 m) do the same at the west and east ends, at 11-18.5 %.
  - K1's "steep main street climbing to the pocket square" becomes this stepped street.
- **The pocket square:**
  - one level (75.25 m), 36 x 13 m, on the downhill side of the 75 m terrace where the main street arrives;
  - open to the sea (south-west);
  - the landmark is SF03 (12.5 m sci-fi tower), standing in for the Beacon Relay Mast;
  - a fish-market comp stands on it.
- **The beacon path leaves from the top terrace** toward 5-M4 (north-east). It is yours to draw.

## Self-check (MEASURED by `tools/town_grid.py` on the site tile)
| Check | Result | Pass? |
|---|---|---|
| Grid points (every 5 m) claimed by two pad levels | **0** | pass |
| Pads at different levels closer than 14 m (17 m at 45°) | **0** (closest 17.3 m) | pass |
| Pad cut or fill | median 1.98 m, max 3.61 m. **1 near the limit:** B001, the landmark (fill 3.61). None over 4.0. | pass, 1 listed |
| Overlaps; footprint into a street | 0; 0 | pass |
| Corner houses within 2 m of a cross street | 0 | pass |
| Doors: 3 m out lands on a street or the square | 64 of 64; door level within 0.75 m for all | pass |
| Lane ends vs the level of the street they join | 0 mismatches over 0.3 m | pass |
| Straight runs (m) | terraces 42-63; quay lane 60; spine pieces 48-80 | pass (< 80) |
| Grades: stepped main street | 11-15 % | **over the 8 % average for a main street**: it is a stepped foot street. Say if it must be called a lane. |
| Grades: terraces | 0-4.7 % (drops between level segments) | pass |
| Grades: side spines | up to 18.5 % | pass (< 19) |
| Grades: quay lane | up to 10.9 % | pass |
| Grades: quay stair | 24.5 % average | it is a stair |
| Street cut / fill | at most 3.2 m / 3.7 m | pass |
| Largest model / twin group | WH03 10.9 %; WH11 + WH24 10.9 %; 22 models | pass (12 % cap) |
| Buildings / garrison | **64 / 40** (45 enterable) | pass. Your review: "66 is fine". |
| Sci-fi share | 3 of 64 (the mast and two quay sheds) | low on purpose, as in K1 |
| Tall pieces | none (the mast stand-in is 12.5 m) | pass |
| Pad levels | 10 | |

## What is weak, honestly
- **The square has no ring buildings.** At 13 m deep it already needs 3.6 m of fill under the mast; ring pieces at its ends failed cut/fill or street clearance. It is framed by the 75 m terrace's row and the main street.
- **One row per terrace** reads more like terraced houses than the tight K1 blocks. On a 20 % slope that is what the grid rule allows.
- **The quay row is only 7 buildings,** and the beach strip is narrow. The escarpment toe leaves no room for a second row.
- **The quay stair is the only link** between the quay and the hamlet (foot only, about 100 m of climb with the legs).

## Open questions
1. **The stepped main street:** may a main street on a no-vehicle hamlet be a 6 m stepped street at 11-15 %, or should it be named a lane?
2. **A taller mast:** if you want it over 14 m, the square needs a deeper pad (about 4 m of fill).
3. **The beacon path to 5-M4:** draw it from the top terrace's east end (about 7520, 16550), or should I add it?
