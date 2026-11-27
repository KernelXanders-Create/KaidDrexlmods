# Ops 5-6: reviewed approaches swapped into the modules and plan files — v1

Done on 2026-11-27. Until now, the op 5-6 planner modules took each main's and final's two approaches from the sketch, where they were still the AI drafts of v1. The reviewed list is `job5/ops5_6_approaches_v2.md`: all HUMAN, from JOB_5 decisions 14 and 21-28 and JOB_4 decision 3.

## What changed

- **New module `job2/tools_sketch/approaches56_v2.py`:** it holds the reviewed list, read from the v2 table, for the 10 mains and finals of ops 5-6.
- **The op modules:** `op5d.py` and `op6d.py` now set `APPROACHES` from it. Every module built on them takes the new list too: `op5e`-`op5h`, `op6e`, and `op5f`/`op5h`, which have no mains and stay empty.
- **The final plan files:** `planner_ops56_v4/op5_main` and `approaches36/run_a4/op6`. In each, the `approaches` list and rule 6 of the checks now carry the reviewed list. A note in `approaches_source` says it was swapped in after the run.

**No re-run is needed.** The planner only writes `APPROACHES` into the plan and the rule 6 note; it does not read them when routing (MEASURED from `run_op.py`). The approaches-on-roads check already used the v2 list, so its result, 22 / 10 / 7 / 1, does not change.

## Old drafts and the reviewed list

| Site | Old draft (AI) | Reviewed (HUMAN) | Bearing changed |
|---|---|---|---|
| 5-F | SSE via 5-M1 (166°); N via 5-M2, after it falls (14°) | SSE up the esker road via 5-M1 (166°); N down the esker from 5-M2 once it falls (14°) | No |
| 5-M1 | via 5-05 (90°); via 5-09 (225°) | E past 5-05 (81°); SW past 5-09 (225°) | 90° → 81° |
| 5-M2 | via 5-F (194°); via 5-08 (39°) | NNE past 5-08 (39°); E past 5-04 Walker Park (97°) | The 194° way from 5-F is gone (call 6C rule); a 97° way from 5-04 is added |
| 5-M3 | via 5-M2 (117°); via 5-02 (196°) | ESE from 5-M2 once it falls (117°); S past 5-02 (196°) | No |
| 5-M4 | via 5-05 (207°); via 5-03 (34°) | SW past 5-05 (219°); WSW from 5-M1 once it falls (252°) | Both |
| 6-F | SW over the rim past 6-M1 (225°); E from 6-M4 (86°) | The same, with the town's full name | No |
| 6-M1 | from the op start (180°); via 6-F (45°) | WSW from the start (243°); W past 6-04 Gas Holder (277°) | Both |
| 6-M2 | via 6-F (223°); via 6-02 (78°) | S past 6-01 (179°); ENE past 6-02 (78°) | The 223° way from 6-F is gone (call 6C rule); a 179° way from 6-01 is added |
| 6-M3 | via 6-12 (252°); via 6-M4 (34°) | WNW past 6-01 (288°); SE past 6-10 (122°) | Both |
| 6-M4 | via 6-M3 (214°); via 6-06 (0°) | SSW from 6-M3 once it falls (214°); N past 6-06 (0°) | No |

## Still carrying the old list

- `SUDDRA_KERNEL_RETURN_OPS36_DROP2_v1.zip`: its op 5 and op 6 plan files were copied before this swap. A v2 of the return zip would carry the reviewed list.
- `SUDDRA_KERNEL_SCRIPTS_OPS36_DROP2_v1.zip`: its `op5d.py` and `op6d.py` are from before this swap, and it has no `approaches56_v2.py`.
- The earlier, superseded op 5-6 outputs (`planner_ops56_v1`-`v3`, `v5`-`v9`) are left as they were run.
