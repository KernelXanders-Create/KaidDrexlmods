# Ops 5-6 planner run on the drop 2 ground — v3 (third and fourth passes)

Run on 2026-11-26. This round follows Kernel's answers P1-P7 in `PLANNER_OPS56_v1.md`:
- the ground is pack v7 (`build_pack_drop2_v7.py`), which adds the 6-05 apron (P1) and the 5-M2.3 / 5-M2.5 fills (P2);
- the 5-02 and 5-12 roads route at 14 % per step (P4, P5), and the 5-M2 tunnel holdout is a foot link (P3);
- 5-02, 5-M2.5 and 5-12 try every pad edge, and 5-12's road search reaches over the whole map;
- the 6-03 junction may step up to 0.7 m, standing in for the ramp piece (P7).

The third pass of op 5 reached the 2-hour limit before it wrote any output. Kernel chose to split it (answer P8 below), so op 5 ran as two jobs:
- `op5e.py`: every op 5 site except 5-12;
- `op5f.py`: 5-12 alone, with its road allowed to join anywhere on the part 1 roads.

Outputs:
- op 6: `planner_ops56_v3/op6`;
- op 5: `planner_ops56_v4/op5_main` and `op5_512`.

All numbers are MEASURED unless marked otherwise.

## Op 6, third pass (14 min)

| Check | Result |
|---|---|
| Sites | Every site the plan puts on the net is on it. That includes **6-03**, by the road 6-03 → 6-05: 4,303 m long, worst grade 9.6 %, with a 0.67 m step at the junction |
| Roads | 17 roads, 32.4 km. Worst grade 12.8 % |
| One net | Reads FAIL only because of 6-M3, which has a vehicle approach but is off the net by decision (roads R2). The op 6 net is one piece with no site unreached |
| Other checks | Pass |

## Op 5 part 1, every site except 5-12 (33 min)

| Check | Result |
|---|---|
| Pads | Every pad has a spot. 5-M2.3 is on its fill, 4 m from its layout seat; 5-M2.5 is on its fill, 1 m from its layout seat (P2 worked) |
| Roads | 19 roads, 24.4 km. Worst grade 12.8 %. The trunk from the op 5 start to 5-M1 is 3.0 km |
| Long road | 5-03 → 5-F.3 is still 11.5 km. The run picked the same join as before (P6) |
| Not reached | **5-02** at (1400, 12000) and **5-M2.5** at (3385, 12520). Even with every edge tried, the log shows no try for either: the router found no path at all |
| Off the net by decision | 5-M2 (foot link, P3); 5-M4, 5-05 and 5-04 (roads R2); 5-13 (ground check f4) |
| Other checks | Pass |

5-M2.5 sits 20.8 m from 5-M2.2, which is on the net (from the pad spacing check).

## Op 5 part 2, 5-12 alone (76 min)

| Check | Result |
|---|---|
| Pad | 5-12 at (600, 11000), pad level +3.5 m |
| Roads | **None.** The router now finds paths to the part 1 roads and pads, so the 14 % grade and the whole-map search worked. Every try was rejected: |
| Rejected tries | At the junction, with steps of 0.55-1.41 m. The best tries were: 5-03 → 5-F.3 road (0.55 m step, grade 12.5 %), 5-F.3 → 5-M1.2 road (0.55 m, 12.9 %), and 5-F pad (0.56 m, 12.9 %). Some tries also clashed with 5-12's own pad |
| Road length | NOT MEASURED (the log does not give the length of rejected tries) |

## Op 5 part 2, 5-12 re-run with the narrowed search (P12, 7 min)

Output in `planner_ops56_v5/op5_512`. **No road.** The log has no tries at all: with the search margin cut from 16 km to 6 km, the router found no dry path to any of the three joins. The run with the 16 km margin did find paths to them, so the dry way round is longer than a 6 km box allows. The 6 km figure was ASSUMED by me; that assumption was wrong. (Roads R5 measured 5-12's kept road at 47.6 km.)

The 0.6 m ramp allowance (P9) was never tested, because no path reached a junction.

## Op 5 part 2, 5-12 re-run with three joins and the 16 km margin (P13)

Output in `planner_ops56_v6/op5_512` (log only). **Stopped at its own 115 min limit with no output.** The log has no tries at all. The two earlier 16 km runs behaved differently:
- the first, with every join and no ramp, finished in 76 min and logged 19 rejected tries;
- the second, with every join and the ramp, also stopped with no output.

Where the time goes is NOT MEASURED.

## Op 5 part 2, 5-12 without the ramp, repeated (P14, 73 min)

Output in `planner_ops56_v7/op5_512`. **It finished**, in 73 min, so the no-ramp setup still finishes as it did in the 76-min run.
- No road was built. All 34 tries were rejected at the junction.
- The smallest steps were 0.55 m (the 5-03 → 5-F.3 road, 12.5 % grade) and 0.56 m (the 5-F pad, 12.9 %), the same as before.
- The log gives the step but not where the junction is.

Reading (AI): the two runs that allowed a 0.6 m step both ran past 115 min. The one that allowed none finished in 73 min. So allowing the step is likely what makes those runs slow. The cause is NOT MEASURED.

## Op 5 part 2, 5-12 with each junction point logged (P15, 73 min)

Output in `planner_ops56_v8/op5_512` (module `op5h.py`, pack v7, no ramp). It finished in 73 min. **No road was built.** All 34 tries were again rejected at the junction, and the log now gives where each one joins and how long it is.

| Joins | Join point | Net level there | Best step | Grade | Road length |
|---|---|---|---|---|---|
| 5-03 → 5-F.3 road | (2733, 11760) | +0.66 m | 0.55 m | 12.5 % | 52,660 m |
| 5-F.3 → 5-M1.2 road | (3024, 10704) | +6.91 m | 0.55 m | 12.9 % | 53,830 m |
| 5-F pad | (2876, 10950) | +6.25 m | 0.56 m | 12.9 % | 53,479 m |
| 5-F.3 pad | (2914, 10796) | +5.75 m | 0.60 m | 13.1 % | 53,642 m |
| 5-03 → 5-F.3 road, second point | (2633, 12004) | +3.65 m | 0.63 m | 12.8 % | 52,372 m |
| 5-F.2 → 5-03 road | (2936, 11199) | +1.16 m | 0.89 m | 12.4 % | 53,251 m |
| 5-F.2 pad | (2931, 11160) | +2.75 m | 0.92 m | 12.7 % | 53,304 m |
| 5-01 → 5-F.3 road (4 points) | (2072-2429, 9853-9998) | +0.77 to +1.87 m | 0.99 m | 12.7-12.8 % | 55,495-55,907 m |
| 5-01 pad | (1981, 10000) | +1.0 m | 0.99 m | 12.7 % | 55,956 m |

- Every try is 52-56 km long. The best one, 52,660 m, is about 23 times the 2.3 km straight line from 5-12 (600, 11000) to its join. That length fits roads R5's 47.6 km kept road.
- The two best joins both have a 0.55 m step. One is on the low shore road at (2733, 11760), net level +0.66 m. The other is on the high road at (3024, 10704), net level +6.91 m.
- What the ground request would be: raising or lowering the ground under the last few metres of the 5-12 road by about 0.3 m would bring the step under the 0.3 m limit. That is AI reading: the size and length of the change are NOT MEASURED.

## Ramp spec for 6-03 (P7), corrected

| Item | Value | Tag |
|---|---|---|
| Where | The 6-03 road's junction at (10138, 11499). This replaces the v1 guess at about (10105, 11825) | MEASURED |
| Rise | 0.67 m | MEASURED |
| Length at 14 % | 4.8 m | MEASURED (from the rise) |
| Deck | 7 m, the road width | ASSUMED |
| Between | The 6-03 road (Fuel Depot, pad +1.0 m) and the net at 6-05 (Medium AA Base, pad +3.75 m) | MEASURED |

## Decisions (Kernel)

| # | Finding | Answer | source |
|---|---|---|---|
| P8 | Op 5 third pass stopped at the 2-hour limit | a Split off 5-12: the rest of op 5 as one job, then 5-12 alone joined to that net | HUMAN |
| P9 | 5-12 no road: every try rejected at the junction (steps 0.55-1.41 m) | a Ramp piece: allow up to a 0.6 m step at the 5-12 junction, logged as a ramp spec (about 3.9 m long at 14 %, ASSUMED until the re-run gives the step), then re-run 5-12 alone | HUMAN |
| P10 | 5-02 and 5-M2.5 no road (the router found no dry path to either, with every edge tried) | a Both foot / boat / air. 5-M2.5 gets a 21 m foot link to 5-M2.2 (like P3) | HUMAN |
| P11 | 5-03 → 5-F.3 still 11.5 km (3.1× the straight line) after P6 | a Accept it, like the long dry routes in ops 3-4 (v1 decision 1) | HUMAN |
| P12 | 5-12 re-run with the ramp stopped at the 2-hour limit (no output) | a Narrow the search: join only the 5-03 → 5-F.3 road, the 5-F.3 → 5-M1.2 road or the 5-F pad, with a 6 km margin, then re-run | HUMAN |
| P13 | 5-12 narrowed re-run: no path inside the 6 km margin (ASSUMED by me, too small) | a Keep the three joins, go back to the 16 km margin, stop at 115 min | HUMAN |
| P14 | 5-12 three-join run stopped at 115 min with no tries | d Re-run the 76-min setup without the ramp, then a ground request at the best junction | HUMAN |
| P15 | 5-12: where to put the junction ground request (the log gave no point) | a Log each try's junction point, re-run the no-ramp setup, then place the ground request at the measured junction | HUMAN |
| P16 | 5-12: the two best joins tie at a 0.55 m step | a Low shore road: the ground request goes at the 5-03 → 5-F.3 road join, (2733, 11760), net level +0.66 m | HUMAN |

## P16 ground request at the 5-12 join (pack v10)

Script `build_pack_drop2_v10.py` builds pack v10 = pack v9 plus this cut. Pack v9 only differs from v7 at ops 3 and 6, far from op 5.

| Item | Value | Tag |
|---|---|---|
| Where | The 5-03 → 5-F.3 road join, (2733, 11760), net level +0.66 m | MEASURED (P15 run) |
| Ground there before | +0.6 to +0.7 m at the join, rising to +1.2-1.4 m about 25-30 m inland (west). The water is 10-20 m to the east | MEASURED |
| Shape | Cut only. Within 40 m of the join, ground is held to no more than +0.66 m + 3 % of the distance (+1.86 m at 40 m). Ground is never raised, so the water line does not move | Reach and slope ASSUMED |
| Size | Largest cut 0.59 m. 33 grid cells changed, 209 m³ | MEASURED |

### Re-run of 5-12 on pack v10 (69 min)

Output in `planner_ops56_v9/op5_512` (module `op5h.py`, no ramp). **No road. The cut changed nothing**: all 34 tries are the same as on pack v7, with the same steps, joins and lengths. The best is still 0.55 m at (2733, 11760).

Why (MEASURED from the code, `planner.py` `check_road`):
- The junction step is not measured against the ground. It is the largest level difference over the grid points that both the new road's band (half width + 3.5 m, so 7 m) and the net road already fix.
- The 5-12 road ends at the net level (+0.66 m) at the join. The net road there is flat: +0.65 to +0.73 m over 100 m (MEASURED).
- On an external plan's road the planner gives no level landing. That landing (`relevel`) is only made for this op's own roads.

Reading (AI): the new road probably climbs at about 12.5 % in its last few metres, inside the shared band. 0.55 m at 12.5 % is 4.4 m. The new road's levels at the join are NOT MEASURED, because the log does not keep a rejected road's points.

Pack v10's cut stays in the ground log but did nothing for this run.
