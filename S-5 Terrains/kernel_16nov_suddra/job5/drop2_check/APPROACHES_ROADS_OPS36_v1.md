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

## A2 ground check: 3-F west side (ground v5, MEASURED)

- **The line checked:** the straight line from 3-F (13200, 2600) to 3-M2 (11645, 3390). It is 1,744 m long, at a bearing of 297°.
- **Wet ground:** 1,290 m of it is at or below +0.3 m, in one main stretch from 175 m to 1,215 m out, going down to −2.72 m. Lines 150 m either side are just as wet, with 1,020 m and 1,270 m of wet ground.
- **Slope:** not the cause. On the centre line the worst 10 m grade is 10.6 %.
- **Pads:** none in the way.
- **Reading (AI):** a road on the W side would have to cross about 1 km of water. Under ops 3-4 v1 decision 1, roads stay on dry ground only, so that decision is why no road leaves 3-F on the W side.

## A3 causeways on the three wet sides (MEASURED, method ASSUMED)

How this was measured (script `approaches36/causeway36.py`, output `approaches36/causeway36_v1.jsonl`):
- Each line runs straight from the site's centre to the place the approach comes from.
- Ground at or below +0.3 m is wet.
- Each wet stretch is filled to +0.75 m, 50 m wide (the ops 5-6 causeway size).
- Stretches less than 50 m apart are joined into one piece.
- Fill is counted under the deck only, with no side slopes.

The line ends and the deck size are ASSUMED. The ground is pack v5 for op 3 and v7 for op 6.

| Approach | Line | Causeway (pieces) | Fill | Deepest fill | Worst dry-ground grade on the line |
|---|---|---|---|---|---|
| 3-M2 W from the start | 3,451 m to 1-F (8200, 3600), 273° | **2,265 m** in 5 pieces; the longest is 925 m, down to −2.23 m | 124,640 m³ | 2.98 m | 9.1 % |
| 3-M4 NW past 3-05 | 1,273 m to 3-05 (10300, 2500), 315° | 705 m in 3 pieces; the longest is 595 m | 23,633 m³ | 1.23 m | 7.6 % |
| 6-M1 W past 6-04 | 1,612 m to 6-04 (8800, 10600), 277° | 635 m in 5 pieces; the longest is 270 m | 21,339 m³ | 1.02 m | **16.2 %** (over the 14 % rule; a road there would need a cut) |

For scale: the four ops 5-6 causeways cross gaps of 20-50 m (roads R2).

- 3-05's point comes from the objectives file. 3-05 is not in the drop 2 op 3 plan.
- 3-M2's line ends at 1-F. A causeway that joined a nearer op 3 road would be shorter (NOT MEASURED).

## Decisions (Kernel)

| # | Finding | Answer | source |
|---|---|---|---|
| A1 | Tolerance for "a road on the approach side" (3-M2 W, 3-M4 NW and 6-M1 W miss by 50-51°) | a Keep 45°: the three stay as findings | HUMAN |
| A2 | 3-F W approach (297°): no road on that side; the line to 3-M2 is about 1 km of water | a Boat / wade way: the W approach stays a water way, no road | HUMAN |
| A3 | 3-M2 W, 3-M4 NW and 6-M1 W: approach sides wet | b Causeways: measure them before any re-run | HUMAN |
| A4 | Causeways on the three wet sides (3-M2 W 2,265 m; 3-M4 NW 705 m; 6-M1 W 635 m, with dry ground to 16.2 %) | a All three: ground requests in pack v8, with a cut to 12 % on the 6-M1 line; re-run ops 3 and 6 | HUMAN |
