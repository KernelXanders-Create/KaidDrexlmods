# Ops 3-4 planner re-run on the drop 2 ground — v4 (fourth pass)

Run on 2026-11-25. This pass applies Kernel's decisions 1-4 from `RERUN_OPS34_REAL_v2.md`:
- the ground is `suddra_drop2_pack_v4`, built by `build_pack_drop2_v4.py`; all of its ASSUMED fills are listed in `rerun_ops34_v4/ground_requests_applied.json`;
- the op modules are `op3r3.py`, `op4r2n.py` and `op4r2s.py`;
- the planner ramps the flattened stretch at an astride seat back to the road at 12 % (ASSUMED);
- op 4 is split by bank.

The third pass (`rerun_ops34_v3/`, op 3 only) is superseded by this one. All numbers are MEASURED unless marked otherwise.

## Op 3 (56 min): passes

| Check | Result |
|---|---|
| Grade | PASS, worst 12.8 % (the trunk step is gone) |
| Pads | Every pad has a spot. 3-03 sits on its fill at (15200, 3000). 3-10.3 is at (14000, 6535). 3-04.2 and 3-10.2 are about 200 m out |
| 3-M1.2 | Seated at its pin (13874, 5552), 0 m from its design point |
| Water line | PASS. Closest is 3-M2.2 at 12.5 m |
| One net | FAIL as accepted under v1 decision 1: 3-M2, 3-04, 3-04.2, 3-10, 3-10.2 and 3-10.3 are foot / boat / air links |
| Total road | 34.3 km over 21 roads |

## Op 4 south bank (36 min)

| Check | Result |
|---|---|
| Roads | 4-M4 → 4-04 14.3 km, 4-01 → 4-M4 3.0 km, 4-04.2 spur. Total 17.3 km |
| Pads | 4-F placed 203 m out (z +0.25). **4-07 (197 × 193 m): no spot within 300 m** |
| Not reached | 4-F, 4-M2.2, 4-05, and every crossing (south ends). Under decision 1 these are foot / boat / air links |
| Astride | Not used: this run seated north-bank checkpoints on a south road, which is a side effect of the split. Their seats come from the north run |

## Op 4 north bank (88 min)

| Check | Result |
|---|---|
| Roads | 10 roads, 15.9 km. Longest: 4-10 → 4-M3.3 at 7.6 km; rail bridge N → 4-06.2 at 3.7 km. Worst grade 12.8 % |
| Pads | 4-M1.5 placed 127 m out; 4-02.2 placed 165 m out (and now on the net) |
| Not reached | 4-M1, 4-M1.3, 4-M1.5, 4-09, 4-03 ×3, 4-08, the village roads, and the dam / causeway north ends. Under decision 1 these are foot / boat / air links |
| Astride seats | 4-M2 at (8401, 7842), 137 m from its pin. 4-M2.3 at (8177, 7326), 90 m out. 4-06 at (7250, 7766), 284 m out, with a 3.79 m pad change |
| Water line | **FAIL**: 4-M2.3 at 2.2 m, 4-M2 at 3.8 m, 4-06 at 5.9 m |

The fills changed the roads, so all three checkpoints seated off their filled spots. This is the same thing that happened to 3-M1.2 in the third pass. For 3-M1.2, filling and pinning it at the new seat fixed it.

## Decisions (Kernel)

| # | Question | Answer | source |
|---|---|---|---|
