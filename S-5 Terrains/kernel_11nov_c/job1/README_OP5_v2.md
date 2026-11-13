# KERNEL_RETURN_11NOV_C_JOB1_OP5_v2: op 5 (Acropolis Isle), ground plan, re-pass

**No rule fails.** Every rule reads PASS in `op5_checks.json`. `tools/verify.py` measures it your way: 0 of 10 roads over 14 %, and every pad within 4 m.

**Kastro Quay:** the roads meet the town at its main street's north end, on a 15 m extension of M (Kastro Quay street work), and keep 22 m from every house wall. Read `op5_notes.md`.

| File | What it is |
|---|---|
| `op5_plan.json` | The plan: sites (with `design_xy`, `moved_m`), squad positions, the towns (Kastro Quay with its `street_extensions`, Lantern Quay), roads (levels to the millimetre), foot links, approaches, shores. |
| `op5_plan.png` | The plan over a hillshade of your build-4 ground. |
| `op5_checks.json` | Each rule with numbers. |
| `op5_notes.md` | The re-pass items, Kastro Quay, the least-sure things, roads and moves. |
| `tools/` | The planner and `verify.py`. |

**New since op 4 v2:** a road net that starts at a town starts 15 m out on the line of each of its street ends. The 15 m are the street extended, and roads keep 3 m from every house wall.
