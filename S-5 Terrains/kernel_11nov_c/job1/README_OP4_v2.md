# KERNEL_RETURN_11NOV_C_JOB1_OP4_v2: op 4 (Cinder Road), ground plan, re-pass

**One rule fails: rule 3, for three sites (4-06, 4-01, 4-10).** Read the first lines of `op4_notes.md`.

**Item 2 is answered:**
- the north causeway's cone end is now a road;
- the south causeway head needs one ramp, 22 m of rise and at least 157 m at 14 %, 7 m wide (`ramps_needed`), from a terrace bench that a road joins to your built op 2 net.

| File | What it is |
|---|---|
| `op4_plan.json` | The plan: sites (with `design_xy`, `moved_m`), squad positions, Causeway Foot, roads (levels to the millimetre; `landings_for_joins`), the trunk (starting at your built 2-07 pad), `ramps_needed`, `trunk_breaks`, approaches, shores. |
| `op4_plan.png` | The plan over a hillshade of your build-4 ground. Your built ops 1-2 pads (hatched) and roads (grey dashed); the GAP at the south causeway head. |
| `op4_checks.json` | Each rule with numbers. |
| `op4_notes.md` | The failing rule, item 2, the least-sure things, the changes, moves, sizes, Causeway Foot and roads. |
| `tools/` | The planner and `verify.py`, the independent check: `python3 verify.py op4_plan.json`. |

## New since op 3 v2
- **Your built ops 1-2 pads are fixed ground,** and a road may join one at a free edge.
- **The trunk can start on your existing net.** Where a point cannot be reached, the road is taken to the nearest bench on dry ground, and the ramp for the rest is given (rise, length at 14 %, width, both ends).
- **Join landings:** a joining road ends on 20 m of level, and the road it joins gets a 50 m level landing (30 m where 50 m does not fit).
