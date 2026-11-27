# Suddra: Kernel's ops 3-6 return on the drop 2 ground — v1

Made on 2026-11-27. These are the final planner plans for ops 3, 4, 5 and 6 on the drop 2 ground, with their checks, the ground changes, and the docs that record every decision. The data and proposals are here; the scripts stay in the repository (`job2/tools_sketch`, `job2/drop2_check`, `job5/drop2_check`).

Every number is MEASURED unless marked ASSUMED or NOT MEASURED. Decisions are Kernel's (HUMAN) unless marked AI.

## The final plans (`plans/`)

| Op | Folder | Ground pack | Roads | Length | Worst road grade | Only check not passed |
|---|---|---|---|---|---|---|
| 3 | `op3` (op37) | v9 | 23 | 35.0 km | 13.8 % | One connected net: 3-04, 3-04.2, 3-10, 3-10.2 and 3-10.3 are foot / boat / air |
| 4 north | `op4_north` (op43) | v5 | 10 | 15.9 km | 12.8 % | One connected net: accepted under ops 3-4 v1 decision 1 |
| 4 south | `op4_south` (op43) | v5 | 4 | 31.9 km | 12.8 % | One connected net: accepted under ops 3-4 v1 decision 1 |
| 5 | `op5` | v7 | 19 | 24.4 km | 12.8 % | One connected net: 5-02, 5-M2.5 (P10) and 5-12 (P17) are foot / boat / air. 5-12 has no plan of its own |
| 6 | `op6` | v8 | 18 | 33.0 km | 13.8 % | One connected net: 6-M3 is off the net (roads R2) |

- Every other check passes. "Junction steps" is a report, not a pass/fail check.
- The one step over 0.3 m in each plan has a ramp spec:
  - op 3: 0.37 m on the 3-M1 trunk at 1-F (A5);
  - op 6: 0.66 m at the 6-03 junction (P7).
- Each folder has the plan, its checks, a map picture and the run log.

## Ground (`ground/`)

`ground_requests_applied_pack_v10.json` lists all 40 ground changes up to pack v10, in order. That covers:
- the ops 3-4 fills;
- the ops 5-6 requests;
- the causeways (A4) and the 3-M2 widening (A6);
- the P16 cut at 5-12's join. It is not used by any road, since 5-12 went off the net (P17).

Each later pack contains the earlier ones, so pack v10 holds every plan's ground. No change lands on an ops 7-8 site.

## Docs (`docs/`), with their decisions

| Doc | What it holds |
|---|---|
| `GROUND_CHECK_OPS34_v1.md` | Ops 3-4 ground check |
| `RERUN_OPS34_REAL_v1`, `v2`, `v4`, `v5` | Ops 3-4 planner re-runs and their decisions; v5 is the final for ops 3-4 |
| `PLANNER_OPS56_v1.md`, `v3.md` | Ops 5-6 planner runs, decisions P1-P17, and the 6-03 ramp spec |
| `APPROACHES_ROADS_OPS36_v1.md` | Do the planned roads serve each designed approach? Decisions A1-A6, including the A5 ramp spec |
| `TOWN_JOINS_6M4_v1.md` | Where the 6-M4 town's two roads join; decisions T1-T2 |
| `HANDOFF_OPS78_v1.md` | What ops 3-6 leave on or next to Comedian's ops 7-8 ground, and the open items between the two sketches |

## Approaches: final result (`checks/approaches36_v4.json`)

Of the 40 designed approaches for the 20 mains and finals of ops 3-6:

| Result | Count |
|---|---|
| A road leaves the site on that side | 22 |
| No road at the site | 10 (4-F, 4-M1, 5-M4, 6-F, 6-M3) |
| No road on that side, each by a decision | 7 |
| A boat way (4-M4) | 1 |

Other files in `checks/`: the causeway lines (`causeway36_v1.jsonl`), the 6-M4 town joins (`town64*_v1.json`) and the ops 7-8 hand-off measurements (`handoff78_v1.json`).

## Known gaps

- **Op 5-6 plan files:** they still carry the older AI-drafted approaches. The reviewed list is `job5/ops5_6_approaches_v2.md`, and the approaches check used that list.
- **6-M4:** the town's FOB and gun spots are NOT MEASURED.
- **Escape Pad (8-12):** its check against op 7's real outline is NOT MEASURED, because op 7 is not built.
