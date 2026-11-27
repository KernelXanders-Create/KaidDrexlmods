# Ops 7-8 hand-off to Comedian — v1

Written on 2026-11-27, from Kernel's ops 3-6 work on the drop 2 ground. Ops 7-8 and the Citadel are Comedian's (pack 5). This note lists what that work leaves on or next to ops 7-8 ground, and what is still open between the two sketches.

Script: `handoff78/handoff78.py`. Output: `handoff78/handoff78_v1.json`. Numbers are MEASURED unless marked otherwise.

## 1. Ground

- **Latest ground pack: v10** (`build_pack_drop2_v10.py` and the pack builders before it). Each change is logged in the pack's `ground_requests_applied.json`.
- **No ground change lands on an ops 7-8 site.** The nearest changes are these:

| Change | Where | Nearest ops 7-8 site |
|---|---|---|
| 6-05 apron (planner P1) | (10200, 11800) | 7-02 Wrecked Walker Strongpoint, 539 m |
| 6-06 ground request (ops58 f6b) | (13600, 12400) | 7-05 Reserve Camp, 1,131 m |
| 6-M1 W causeway, with its line cut to 12 % (approaches A4) | West of 6-M1 Rim Bunker Ring (10400, 10400), 190-1,335 m out | It runs from the op 7 start, which is 6-M1's point |
| 6-07 causeway fill (roads R2) | (14450, 13430) | 7-05 Reserve Camp, 1,666 m |

## 2. The op 7 start

| Item | Value |
|---|---|
| Op 7 start | (10400, 10400), the 6-M1 point |
| Nearest op 6 road | 6-M1.2 → 6-M1, 25 m from the start at (10425, 10404), road level +0.75 m |

So op 7 starts on the op 6 road net.

## 3. Op 5 and op 6 roads near ops 7-8 sites

The final plans used are op 5 `planner_ops56_v4/op5_main` and op 6 `approaches36/run_a4/op6`.
- Where a site has a layout (`layout58_ops78_v1.json`), the distance is to the edge of its members.
- Where it has none, the distance is to its sketch point.
- "Band edge" means the distance less the 7 m the planner keeps clear of each side of a road's centre line.

The list keeps roads within 150 m of a member, or 300 m of a sketch point.

| Road (op) | Site | Measured to | Closest road point | Road level | Centre line | Band edge |
|---|---|---|---|---|---|---|
| 6-08 → 6-11 (6) | 8-02 Supply Railhead | sketch point | (12023, 15359) | +0.99 m | 47 m | 40 m |
| 6-02 → 6-M2 (6) | 7-M2 Rail Junction Yard | Medium Logistics Base | (11519, 13711) | +1.43 m | 70 m | 63 m |
| 6-02 → 6-M2 (6) | 7-M2 | Landing Position | (11628, 13906) | +0.40 m | 103 m | 96 m |
| 6-08 → 6-11 (6) | 8-04 Fuel Tanks | sketch point | (12902, 14926) | +11.94 m | 123 m | 116 m |
| 6-11 → 6-02 (6) | 7-05 Reserve Camp | sketch point | (12688, 13108) | +9.49 m | 144 m | 137 m |
| 6-02 → 6-M2 (6) | 7-M2 | Turbolaser Tower | (11558, 13797) | +0.39 m | 147 m | 140 m |
| 5-03 → 5-F.3 (5) | 8-05 Water Tower Overwatch | sketch point | (4987, 14643) | +1.44 m | 243 m | 236 m |
| 6-11 → 6-02 (6) | 7-10 Comms Mast | sketch point | (12254, 12290) | +8.05 m | 270 m | 263 m |
| 6-02 → 6-M2 (6) | 7-10 | sketch point | (12223, 12352) | +5.57 m | 270 m | 263 m |
| 6-08 → 6-11 (6) | 7-05 | sketch point | (12531, 13262) | +1.01 m | 276 m | 269 m |
| 5-03 → 5-F.3 (5) | 7-08 Moraine Spring Post | sketch point | (5865, 13725) | +8.31 m | 293 m | 286 m |

Reading (AI):
- **Op 6 reaches into ops 7-8 ground by design.** 6-08 Supply Depot NE is at (13400, 14400).
- **8-02:** its sketch point is 47 m from the 6-08 → 6-11 road. 8-02 has no layout yet, so whether its pads clear the road is NOT MEASURED.
- **7-M2:** the 6-02 → 6-M2 road passes 63 m from its Logistics Base. That base's 120 × 100 m size is ASSUMED.
- **Shared roads:** where Comedian's roads would meet these op 5-6 roads, they can use them as fixed ground, the way 5-12 was tried (section 5).

## 4. Findings already passed to Comedian, still open

From `GROUND_CHECK_OPS58_v1.md` (findings 7-11, Kernel decision 7-11 a):

| Site | Finding |
|---|---|
| 7-02 | 0 % good ground, 23 % water. Good spots at (10095, 12317), 96 m E, and (10080, 12161), 160 m SSE |
| 7-07 Fuel Siding | 100 % water. Good spot at (10784, 12446), 240 m SE |
| 7-12 Junction Field Hospital | Depot is 76 % good, 12 % water |
| 7-04, 7-05, 8-M4 | Slope over 8 m: 9.0 m, 10.2 m and 17.9 m |
| 8-07, 8-08, 8-10 | Wet or partly wet. They move under call 26 B anyway |

From `ROADS_OPS58_v1.md`:
- **Islands:** 7-F Kesh Junction, which is also the op 8 start, sits on a 0.11 km² island. 7-01, 7-06 and 8-07 are on small islands, and 7-07 is in water.
- **No dry path within 80 km:**
  - 7-F – 7-M2, 7-12 – 7-01, 7-01 – 7-M1, 7-M1 – 7-06, 7-06 – 7-08;
  - op 8 start – 8-10, 8-08 – 8-07, 8-07 – 8-M1.

From `LAYOUT_OPS58_v1.md`:
- 7-M2's wrecked train and 7-03's Heavy AD Tower have no size, so neither is seated.
- Members more than 150 m from their point: 7-M2's Landing Position (360 m), 8-M2's Medium AA Base (160 m), and three at each of 8-07 and 8-08.

## 5. What the ops 3-6 runs learned, for Comedian's roads (planner `job2/tools_sketch/run_op.py`)

- **Run time:** a run that passes 2 hours is lost with no output. Split big ops (P8). Runs that allowed a 0.6 m junction step ran past 115 min, while the same runs with no step allowance finished in about 70 min (P14). The cause is NOT MEASURED.
- **Junction step:** this is the level gap between a new road and the road it joins, over the ground both of them hold (each road's band is 7 m either side of its centre line). It is not a gap to the ground, so lowering or raising the ground at a join does not fix it (P16, P17). Roads from another plan (`EXTERNAL_PLANS`) get no level landing at a join; this op's own roads do.
- **Options that helped:**
  - `TRUNKS`: forces a road along a set line;
  - `ASTRIDE_ROAD`: puts a checkpoint on a named road;
  - a per-leg `jmax`: allows a ramp piece on one trunk leg;
  - `SITE_GRADE`: lets a named road route at its own grade;
  - `ALL_EDGES`: tries every pad edge;
  - `JOIN_ONLY` with `EXTERNAL_PLANS` and `ROOT = "EXTERNAL_ROADS"`: joins another plan's net.
- **Wet ground:** the water line is +0.3 m. Causeways and fills were made at +0.75 m, 25 m half width (ASSUMED).

## 6. Open items between the two sketches

| Item | Owner | State |
|---|---|---|
| Comedian's call 28 (Kernel's call 20 B, the guns: the Citadel's lowest gun decks and AA stand cold in op 8 if the Refinery fell) | Comedian confirms or picks another | Waiting; due by Wed 2 Dec (calls pack 4) |
| Mound camp spot (op 4) | Comedian sets it | Waiting. Once it is set, Kernel sets the third gun's spot, bearing and facing check (pack 5) |
| Escape Pad 8-12 | Moved to (8400, 15500), the north spot (pack 5) | Its check against op 7's real outline is NOT MEASURED, because op 7 is not built |
| Names: 6-M4 town, 5-13 Stake Hamlet | Comedian names them (pack 5) | No name in the files here yet |
| 6-M4 town roads | Kernel, T1 / T2 | Set: N road is 6-M4 → 6-11; SSW is a shore stub with a K1 landing toward 6-M3 |
