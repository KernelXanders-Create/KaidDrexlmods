# KERNEL_RETURN_11NOV_C_JOB1_OP3_v2: op 3 (The Sound), ground plan, re-pass

**No rule fails.** Every rule reads PASS in `op3_checks.json`, and `tools/verify.py` measures it the way your 12 Nov sheet does (grades on the handed-over points, pads by polygon to the corners): 0 roads over 14 % and every pad within 4 m. Read the first lines of `op3_notes.md`.

| File | What it is |
|---|---|
| `op3_plan.json` | The plan. **Sites** (with `design_xy`, `moved_m` from the design point and `moved_from_rough_m`), squad positions, the town (Sound Head), roads (points every 4.5 m with `points_z` to the millimetre; `landings_for_joins` where a later road joins), foot links, approaches, shores, the gate line. |
| `op3_plan.png` | The plan over a hillshade of your build-4 ground. |
| `op3_checks.json` | Each rule with numbers. The grade rule now reports point to point, 10 m and 20 m. |
| `op3_notes.md` | The three least-sure things, moves, sizes, stairs, approaches, squads, shores and roads. |
| `tools/` | The planner (`world.py`, `planner.py`, `run_op.py`, `op3.py`) and `verify.py`, the independent check: `python3 verify.py op3_plan.json`. |

## What changed from v1 (your 12 Nov sheet)
- **Item 1 (grades):** after the straight-run wave, the points are spaced evenly again; the grade is held, checked and repaired between each pair of points; levels are given to the millimetre.
- **Item 5 (pads):** the pad grid now reaches a rotated pad's corners, both for the 4 m test and for the spacing to other pads.
- **Item 9 (junctions):** a road joins only on the earlier road's own level. A road built in this op gets a level landing where another joins it.
- **Item 12 (moves):** measured from the design point.
- **Also:**
  - your built ops 1-2 roads are fixed ground (none falls in op 3's box);
  - town houses are kept 3 m from road edges, measured from your grader's footprints;
  - your built pad size is tried first for every composition that has one;
  - a road whose smoothing breaks 4 m is drawn again with lighter smoothing.

Ops 4-8 follow, each as its own new zip.
