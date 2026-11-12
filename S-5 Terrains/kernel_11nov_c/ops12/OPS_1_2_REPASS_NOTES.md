# Ops 1 and 2: re-pass of what is built, v2 (Kernel, PROPOSED)

**v2 (your 12 Nov answers):**
- **2-10:** the re-seat beside the net is taken.
- **Perys:** the roads into it now meet the main street M, not the CT1 lane.

**One rule break is left after this re-pass:** op 1's through-comp piece `1-06-through` (rule 3, straight 164 m). It runs across the 1-06 depot's floor; the 2.5 m wave would need 4.4 m of cut, so it is left as built. If a run across a comp's own floor counts, it needs a ramp-free bend inside the comp.

**Op 2, 2-10 Munitions Store (your choice, re-seat):** no road within the rules reaches its built knoll-top seat (147.9 m). It is re-seated beside the net at (15615, 1590), 83.8 m, yaw 165, with your built 79 x 62 m pad (1.94 m of change). A 313 m road (13.8 %, 2.88 m cut/fill) joins it to the net on the net's own level.

Everything else below is fixed, or is a check for your build.

**How I measured:** your built ops 1-2 pads and roads on the build-4 grid. Ops 1-2 are cut into it, so a road's level is the grid under its centreline. Same method as the ops 3-8 re-pass:
- grade between points and over every 10 m and 20 m;
- pads counted to their corners;
- road edges against pads (3 m) and house walls (3 m, your grader's footprints);
- straights within 1 m of the chord.

The full audit is in `audit_ops_1_2.json` (`audit12.py`). The fixes are in `opN_repass.json` (`repass12.py`).

## What the audit found (before any fix)
| | Op 1 | Op 2 |
|---|---|---|
| Roads (dirt + main) | 48, 40.7 km | 40, 22.2 km |
| Over the grade on the points | 1 (the main road `1-M2-1-14`, 10.1 %; limit 10 %) | 0 |
| Straight runs over 150 m | 5 | 6 (worst `2-F-2-M2`, 340 m) |
| Road edge within 3 m of a pad | 0 | 2 (A2-08, A2-09) |
| Pads within 12 m of each other | 0 | 1 (A2-03 overlaps 2-M3 by 35 m²) |
| Vehicle sites with no road | 0 | 2 (2-05: both roads stop 21 m short; 2-10: no road, 495 m away; now re-seated, see above) |
| Roads within 3 m of a Perys v7 house wall | 5 (`1-F-1-M2`, `1-01-1-F`, `1-F-1-15`, `1-M2-1-04`, `1-F-1-04`; 0.0 m, they run through houses) | — |
| Net per island | one | one |
| Mains 400 m apart | yes | yes |

Your dirt roads hold 14 % everywhere on the grid: the grade fault was mine, in ops 3-8, not yours.

## What the re-pass changes (each with its numbers)
**Op 1**
- **Main road `1-M2-1-14`:** re-held to 10 % on its own line: 9.86 % at most, 2.15 m of cut/fill against the built ground.
- **Four straights** (`1-M1-1-12` 196 m, `1-M1-1-11` 160 m, `1-03-1-13` 185 m, `1-11-1-15` 248 m): given a 2.5 m side-to-side wave (120 m period). Now 63-72 m at most, grade at most 13.8 %, cut/fill at most 3.0 m against the built ground.
- **Perys v7** (your K6 second pass, not yet built) stands where the built ground still has the v5 streets. Five built roads ran through its houses.
  - **Four now come in on the line of the main street M** (your choice). Each road stops 25 m out on M's line, and those 25 m are M extended, at M's own end level and width (8 m). That is Perys street work.
    - **West end:** `1-F-1-M2` and `1-F-1-04`. M extended from (5087, 3409) to (5064, 3419), level 59.4 m: 1.2 m of ground change.
    - **East end:** `1-01-1-F` and `1-F-1-15`. M extended from (5353, 3253) to (5374, 3239), level 50.0 m: 3.84 m of ground change.
    - The two roads at each end meet there.
  - **Why the extension, not the road, runs into the street end:** M's own row houses stand 0.2-0.3 m from M's edge (normal for a street row), and the walls nearest each end of M are 4.4-5.3 m from the end point. A 7 m road run into the very end would pass 0.9 m (west) or 1.8 m (east) from them.
    - So the roads stop on the extension and keep 13-18 m from every house wall, with no exemption.
    - The extension itself has walls 0.4 m (west) and 1.3 m (east) from its edge, as M's own rows do.
  - **One road goes round the houses:** `1-M2-1-04`, 20 m from the nearest wall.
  - **The five roads:** grades at most 13.82 %; cut/fill at most 3.84 m. The two east-end roads climb to M's east end at 50.0 m.
  - Each extension is in `op1_repass.json` → `perys_roads_reended` → `m_extension`.

**Op 2**
- **Squad pads re-seated** (same composition and size):

  | Pad | Problem | Change |
  |---|---|---|
  | A2-03 | overlapped 2-M3 | 2.0 m away, yaw 0 |
  | A2-08 | 2.1 m from a road edge | same place, turned to yaw 0 |
  | A2-09 | 2.2 m from a road edge | 2.9 m away, yaw 15 |

  Each now keeps 12 m from pads and 3 m from road edges; ground change at most 1.9 m.
- **2-05 Workers' Camp:** a 95 m stub from the pad to the end of `2-05-2-06` (13.8 %, 3.96 m cut/fill). It meets that road at a 0.4 m step; I would accept that, but flag it against item 9's 0.3 m.
- **2-10:** re-seated, with its road (top of this note).
- **Five straights** (`2-F-2-M2` 340 m, `2-M4-2-02` 165 m, `2-M4-2-12` 156 m, `2-01-2-07` 152 m, and the two `2-M3-through` pieces 169 m and 157 m): waved. Now 58-85 m, grade at most 13.8 %, cut/fill at most 1.97 m.
- **2-04 TKTA Checkpoint** is a pass-profile pad. Its road (`2-04-through`) ends 16 m from the pad's centre-level edge. On a profile pad that may be right (the low end), so I did not add a stub. Check it against the profile's end level.

## Pads that are not level on the grid (a check for your build)
- **What this is:** grid points under footprint + 1.5 m that differ from the pad's own level by more than 0.5 m. These are corners or rim points, not a rule break, but a comp set there floats or sinks by that much.
- **Op 1:** 1-04 (-1.23 m, 3 points), A1-06 (+1.16 m, 3), 1-05 (-0.96 m, 2), A1-09 (+0.92 m, 2), 1-01 (-0.88 m, 6), 1-13 (-0.74 m, 2), 1-02 (-0.69 m), 1-06 (-0.58 m), 1-M2 (+0.58 m), 1-M1 (-0.70 m and -0.51 m), A1-03 (+0.51 m).
- **Op 2:** 2-13 (+0.93 m), A2-04 (-0.90 m, 7 points), 2-05 (+0.84 m), 2-F (+0.64 m), 2-M1 (-0.64 m), A2-11 (+0.62 m), 2-02 (+0.58 m).
- **Where:** `opN_repass.json` → `pads_off_level` gives the worst point of each. The plans mark them with a magenta x.

## How to apply
- **Roads:** `opN_repass.json` gives every changed road whole (`points` and `points_z` to the millimetre): `roads_replaced`, `perys_roads_reended` and `new_roads`.
- **Pads:** `squad_pads_reseated` gives each moved pad's old and new centre, level and yaw.
- **Everything not listed is unchanged.**
