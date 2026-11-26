# Ops 3-4 planner re-run on the drop 2 ground — v5 (final for this round)

Run on 2026-11-25/26. This pass applies Kernel's decisions 1-2 from `RERUN_OPS34_REAL_v4.md`:
- the ground is `suddra_drop2_pack_v5`, built by `build_pack_drop2_v5.py`; every ASSUMED fill is listed in `rerun_ops34_v5/ground_requests_applied.json`;
- the op 4 modules are `op4r3n.py` and `op4r3s.py`, split by bank.

Op 3 was not re-run; its passing plan is the fourth pass in `rerun_ops34_v4/op3/`. All numbers are MEASURED unless marked otherwise.

## Where each op stands

| Op | Plan | Checks not passed |
|---|---|---|
| 3 | `rerun_ops34_v4/op3/` (21 roads, 34.3 km) | One connected net only, accepted under v1 decision 1 |
| 4 south | `rerun_ops34_v5/op4_south/` (4 roads, 31.9 km) | One connected net only, accepted under v1 decision 1 |
| 4 north | `rerun_ops34_v5/op4_north/` (10 roads, 15.9 km) | One connected net only, accepted under v1 decision 1 |

Every other rule passes in all three plans:
- pad spacing;
- pad change ≤ 4 m (worst: 4-06 at 3.79 m);
- grade ≤ 14 % (worst 12.8 %);
- cut / fill ≤ 4 m;
- no straight run over 150 m;
- 3 m road edge;
- 10 m from the +0.3 m line (closest: 4-06.2 and 4-M2.2 at 12.2 m);
- final / mains 400 m apart.

## Op 4 fifth pass details

- **4-07** sits on its fill at (6000, 6400), with a 0.25 m pad change. A new dry road, 4-07 → 4-01, joins it to the south net: 14.6 km, worst grade 12.2 %.
- **Pinned checkpoints:** 4-06 seated 0 m from its pin, 4-M2 1 m and 4-M2.3 5 m.
- **No seat:** 4-M1.2 and 4-M1.4, because their village roads have no dry route. They stay at their design points (v1 decision 8).

## Sites with no road (foot / boat / air links, v1 decisions 1 and 7)

- **Op 3:** 3-M2, 3-04, 3-04.2, 3-10, 3-10.2, 3-10.3.
- **Op 4 south:** 4-F, 4-M2.2, 4-05.
- **Op 4 north:** 4-M1, 4-M1.3, 4-M1.5, 4-09, 4-03 ×3, 4-08.
- **Crossings:** every crossing end except rail bridge N.

## Two plans for op 4

The op 4 plan is in two files, one per bank. The south file also lists astride seats for 4-06 and 4-M2.3 on a south road. Those come from splitting the run and are not used; the seats in the north file are the real ones.
