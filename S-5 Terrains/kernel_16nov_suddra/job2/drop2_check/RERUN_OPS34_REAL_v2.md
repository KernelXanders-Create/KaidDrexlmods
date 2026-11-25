# Ops 3-4 planner re-run on the drop 2 ground — v2 (second pass)

Run on 2026-11-25. This pass applies Kernel's decisions 1-6 from `RERUN_OPS34_REAL_v1.md`:
- the pad pack is `suddra_drop2_pack_v2`, built by `build_pack_drop2_v2.py`; its ASSUMED fills are listed in `rerun_ops34_v2/ground_requests_applied.json`;
- the op modules are `tools_sketch/op3r2.py` and `op4r2.py`.

Op 3 outputs are in `rerun_ops34_v2/`. They are named `op32_*` because `run_op` takes the op number from the digits in the module name. All numbers are MEASURED unless marked otherwise.

## Op 4: not finished

Op 4 ran alongside op 3 and was **stopped at the 2-hour background limit** before it wrote any output. The first pass of op 4 took 96 min when run on its own. It has not been restarted.

## Op 3 (63 min)

| Check | Result | Compared with v1 |
|---|---|---|
| 300 m pad search (decisions 3-4) | 3-04.2 placed 197 m out at (12770, 4240), z +0.25. 3-10.2 placed 208 m out at (14170, 6430). **No spot for 3-03** (197 × 193 m) or **3-10.3** | v1: no spot for any of the 4 |
| Sites not on the road net | 3-04, 3-04.2, 3-10, 3-10.2 (no dry route); 3-M2 (trunk leg: no route) | Under decision 1 these are foot / boat / air links |
| Trunk 1-F → 3-M1 | 17,840 m, same line as v1 | — |
| Grade | **FAIL, worse**: a 19.4 % step at (13807, 5421) | v1: 16.7 % |
| 3-M1.2 shore gap | **FAIL**: 3.9 m from the +0.3 m line | v1: 1.8 m |
| 3-M1.2 seat | 408 m from its design point at (13838, 5447), z +1.42 | v1: 427 m at (13855, 5462) |
| Other checks | Pass | Same as v1 |

### Why the trunk step got worse

The step is not in the ground. When a checkpoint sits astride a road, the planner sets every road point within about 40 m of the pad to the pad's level (+1.42 m). Just past that point the road is back on its own profile (+0.55 m): a drop of 0.87 m in 4.5 m.

The apron and shore fill were placed around the v1 seat. This time the checkpoint seated 21 m away along the road, so the step fell outside the fill. The shore fill missed it the same way.

Any fill placed before the run can miss like this whenever the seat moves.

## Decisions (Kernel)

| # | Question | Answer | source |
|---|---|---|---|
