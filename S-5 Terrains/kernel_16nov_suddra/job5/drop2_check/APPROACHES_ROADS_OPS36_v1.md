# Approaches on the planned roads, ops 3-6 — v1

Run on 2026-11-27. Every planner check reads "SEE NOTES" for rule 6 (two designed approaches per main and final). This check asks, for each designed approach: **does a planned road leave the site on that side?**

## How it was measured

Plans used:
- op 3: `job2/drop2_check/rerun_ops34_v4/op3`;
- op 4: `rerun_ops34_v5/op4_north` and `op4_south`;
- op 5: `job5/drop2_check/planner_ops56_v4/op5_main` (5-12 is not a main and is still running);
- op 6: `planner_ops56_v3/op6`.

Approaches used:
- ops 3-4: as in the plans (JOB_2 decisions 16-25 and call 6C), with 4-M1's first way replaced by JOB_2 decision 46;
- ops 5-6: the reviewed list in `job5/ops5_6_approaches_v2.md`. The op 5-6 plans still carry the older AI drafts from the sketch, so the plans themselves were not used for these.

The method:
- A bearing is taken from the site's centre toward where the approach comes from.
- A road counts as leaving the site if it passes within 15 m of any member's pad.
- The road's heading is read where it is 150 m out from the centre (ASSUMED). A short spur is followed onto the road it joins.
- "On that side" means the road leaves within 45° of the approach bearing (ASSUMED).
- 6-M4 has no pad, so its sketch point is used, with a 30 m reach (ASSUMED).

Script: `approaches36/approach36.py`. Full output: `approaches36/approaches36_v1.json`. Headings are MEASURED on the plans.

## Totals

Out of 40 approaches (20 sites × 2):

| Result | Count |
|---|---|
| A road on that side | 18 |
| A road at the site, but none on that side | 11 |
| No road at the site at all | 10 |
| Not a land way (4-M4's boat way through the lock) | 1 |

## No road at the site: by earlier decisions

These five sites have no road by an earlier decision. This reading is AI.

| Site | Decision |
|---|---|
| 4-F Drain Locks, 4-M1 Peat Cutters' Village | Ops 3-4 v1 decisions 1 and 7: foot / boat / air |
| 5-M4 Moss Abbey Ruin, 6-M3 Tank Laager | Roads R2: island, no causeway |
| 6-F Cauldron Refinery | Ground check f3: water by design |

## A road at the site, but none on the approach side

| Op | Site | Approach | Bearing | Nearest road leaving | Off by | Follows from |
|---|---|---|---|---|---|---|
| 3 | 3-F Peat-Gas Works | W along the pipeline road past 3-M2 | 297° | 3-F → 3-02 at 212° | 85° | — |
| 3 | 3-M2 Pipeline Pumping Station | W from the start | 273° | 3-M2.2 → 3-M1 at 222° | 51° | — |
| 3 | 3-M4 Gasworks Spur | NW along the pipeline road | 315° | 3-M4 → 3-M2.2 at 265° | 50° | — |
| 4 | 4-M2 Drain Rail Bridge | over the 4-06 causeway to the north gate | 309° | rail bridge N → 4-06.2 at 25° | 76° | — |
| 5 | 5-M1 Esker Road Gate | E past 5-05 | 81° | 5-09 → 5-M1 at 176° | 95° | 5-05 is off the net (roads R2) |
| 5 | 5-M2 Esker Dugouts | E past 5-04 | 97° | 5-M2.4 → 5-08 at 22° | 75° | 5-04 is off the net (roads R2) |
| 5 | 5-M3 North-west Battery | S past 5-02 | 196° | 5-M3 spur, 92° | 104° | 5-02 is foot / boat / air (P10) |
| 6 | 6-M1 Rim Bunker Ring | WSW from the start | 243° | 6-05 → 6-M1 at 327° | 84° | Op 6 starts by boat or air (roads R3) |
| 6 | 6-M1 Rim Bunker Ring | W past 6-04 | 277° | 6-05 → 6-M1 at 327° | 50° | — |
| 6 | 6-M2 Terrace Batteries | ENE past 6-02 | 78° | 6-M2 → 6-01 at 190° | 112° | The 6-02 road comes in from 236° after its 6 km detour (roads R6) |
| 6 | 6-M4 Cauldron Apron Town | SSW from 6-M3 once it falls | 214° | 6-M4 → 6-11 at 41° | 173° | 6-M3 is off the net (roads R2) |

- Five of these approaches have no earlier decision behind them (marked —): 3-F W, 3-M2 W, 3-M4 NW, 4-M2 north gate and 6-M1 W.
- Three of those five miss by only 50-51°, just past the ASSUMED 45° tolerance: 3-M2 W, 3-M4 NW and 6-M1 W.

## A road on the approach side

3-F SW; 3-M1 both; 3-M2 SW; 3-M3 both; 3-M4 E; 4-M2 SSW; 4-M3 both; 4-M4 WSW; 5-F both; 5-M1 SW; 5-M2 NNE; 5-M3 ESE; 6-M2 S; 6-M4 N.

## Decisions (Kernel)

| # | Finding | Answer | source |
|---|---|---|---|
