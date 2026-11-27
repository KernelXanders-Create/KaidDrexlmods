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
| 4 | 4-M2 Drain Rail Bridge | over the 4-06 causeway to the north gate | 309° | rail bridge N → 4-06.2 at 25° | 76° | The 4-06 causeway end has no road (ops 3-4 v1 decision 7; AI reading) |
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

## A4 re-runs on pack v8 (MEASURED)

Outputs: `approaches36/run_a4/op3` and `op6`. The approaches check was run again on these plans; its output is `approaches36/approaches36_v2.json`.

| Approach | Before | After |
|---|---|---|
| 3-M2 W from the start | no road on that side (51° off) | **road on that side.** The trunk from 1-F to 3-M2 now runs over the causeway: 3,429 m, worst grade 12.8 %. The road leaves 3-M2 20° off the approach bearing |
| 3-M4 NW past 3-05 | no road on that side (50° off) | **road on that side.** The new road from the causeway end is 1,241 m long, worst grade 1.5 %, and leaves 6° off |
| 6-M1 W past 6-04 | no road on that side (50° off) | **road on that side.** The new road from the causeway end is 1,409 m long, worst grade 13.8 %, and leaves 0° off. 6-M1's WSW approach, from the start, is now 34° off, so it also counts as on that side |

### Op 6 (15 min)

- 18 roads, 33.0 km.
- Every check passes except "one connected net". That fails only because of 6-M3 (roads R2).

### Op 3 (52 min): one setback

- **3-M1 lost its trunk.**
  - The trunk from 1-F to 3-M1 found a much shorter path this time: worst grade 9.9 %, inside a 500 m margin. The fourth pass needed 17.8 km.
  - That path was rejected at its start on the 1-F FOB point, with a 0.37 m junction step against the 0.3 m limit.
  - So 3-M1's own pad has no road. The planner gave a ramp spec instead (0.4 m rise).
  - 3-M1.3 is reached instead by a 14.6 km road from 3-M2.
- **Knock-on to 3-M1.2.** The checkpoint seated astride the 3-M2 trunk, 3,942 m from its pin. It is now only 4.2 m from the +0.3 m line, which fails the 10 m rule.
- **Other checks:**
  - "One connected net" fails, as accepted before: 3-04, 3-04.2, 3-10, 3-10.2 and 3-10.3 are foot / boat / air sites.
  - Everything else passes.
  - The worst grade is 12.8 %. The plan has 22 roads, 34.6 km.

## A5 re-run of op 3 (58 min, MEASURED)

Output: `approaches36/run_a5/op3`. Approaches re-checked in `approaches36/approaches36_v3.json`.

**Correction.** Under A4 I called the rejected 3-M1 trunk path "much shorter". That was my reading of its 500 m search margin, and it was wrong (AI, not measured). The trunk that now passes is 17,661 m long, about the same as the fourth pass (17.8 km).

| Item | Result |
|---|---|
| 1-F → 3-M1 trunk | On the net: 17,661 m, worst grade 12.8 %, with a 0.37 m step at its start on the 1-F FOB point (8300, 3780) |
| 3-M1.2 | Seated on that trunk 1 m from its pin (13874, 5552). Pad change 0.77 m |
| 3-M2 W and 3-M4 NW | Both still have a road on their side, 5° and 6° off the approach bearing |
| Approaches (op 3) | Every land approach has a road on its side except 3-F W, which is a water way by A2 |
| Roads | 23 roads, 35.0 km. Worst grade 13.8 % |
| One net | FAIL, as accepted before: 3-04, 3-04.2, 3-10, 3-10.2 and 3-10.3 are foot / boat / air |
| **Water line** | **FAIL: 3-M2.3** (Small Checkpoint) now sits astride the 3-M2 trunk on the causeway, at (11461, 3440). That is 41 m from its design point and **2.0 m** from the +0.3 m line. In the fourth pass it was on the 3-07 → 3-M2.4 road and passed |

### Ramp spec at the 1-F start of the 3-M1 trunk (A5)

| Item | Value | Tag |
|---|---|---|
| Where | The trunk's start on the 1-F FOB point, (8300, 3780), ground +0.32 m | MEASURED |
| Rise | 0.37 m | MEASURED |
| Length at 14 % | 2.6 m | MEASURED (from the rise) |
| Deck | 7 m, the road width | ASSUMED |

## A6 re-run of op 3 (58 min, MEASURED): passes

Output: `approaches36/run_a6/op3`, run on pack v9.
- **3-M2.3:** seated on the 3-M2 trunk 0 m from its pin, pad change 0.23 m.
- **3-M1.2:** seated 1 m from its pin.
- **Water line:** PASS. The closest pads are 3-M2.2 at 12.5 m and 3-M2 at 12.6 m.
- **Roads:** 23 roads, 35.0 km. Worst grade 13.8 %.
- **Other checks:** every one passes except "one connected net", the failure already accepted (3-04, 3-04.2, 3-10, 3-10.2 and 3-10.3 are foot / boat / air).

Final approaches check on these plans (op 3 `run_a6`, op 4 v5, op 5 v4 main, op 6 `run_a4`): `approaches36/approaches36_v4.json`. Of the 40 approaches:

| Result | Count |
|---|---|
| Road on that side | 22 |
| No road at the site | 10 |
| Road at the site, none on that side | 7 (3-F W, 4-M2 north gate, 5-M1 E, 5-M2 E, 5-M3 S, 6-M2 ENE, 6-M4 SSW) |
| Not a land way | 1 |

Every approach that still has no road on its side has a decision behind it: A2, roads R2 / R6, P10, T2 (6-M4's SSW shore stub and boat landing), or ops 3-4 v1 decisions 1 and 7.

## Decisions (Kernel)

| # | Finding | Answer | source |
|---|---|---|---|
| A1 | Tolerance for "a road on the approach side" (3-M2 W, 3-M4 NW and 6-M1 W miss by 50-51°) | a Keep 45°: the three stay as findings | HUMAN |
| A2 | 3-F W approach (297°): no road on that side; the line to 3-M2 is about 1 km of water | a Boat / wade way: the W approach stays a water way, no road | HUMAN |
| A3 | 3-M2 W, 3-M4 NW and 6-M1 W: approach sides wet | b Causeways: measure them before any re-run | HUMAN |
| A4 | Causeways on the three wet sides (3-M2 W 2,265 m; 3-M4 NW 705 m; 6-M1 W 635 m, with dry ground to 16.2 %) | a All three: ground requests in pack v8, with a cut to 12 % on the 6-M1 line; re-run ops 3 and 6 | HUMAN |
| A5 | Op 3: the 1-F → 3-M1 trunk rejected at its start (0.37 m junction step); 3-M1 off the net, 3-M1.2 seated 3,942 m away | a Ramp piece at the trunk's 1-F start (step up to 0.4 m, ramp spec logged); 3-M1.2 held to that trunk at its pin; re-run op 3 | HUMAN |
| A6 | 3-M2.3 seated on the 3-M2 trunk causeway, 2.0 m from the +0.3 m line | a Widen the causeway round the seat (pack v9: +0.75 m out to 30 m past the pad edge, 1,346 m³), pin 3-M2.3 there on the 3-M2 trunk, re-run op 3 | HUMAN |
