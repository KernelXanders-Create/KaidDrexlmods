# Ops 5-6 planner run on the drop 2 ground — v1

Run on 2026-11-26. The inputs were:
- the planner modules `op5d.py` / `op6d.py` (shared `op58d.py`), built from the job 5 sketch with Kernel's answers in `GROUND_CHECK_OPS58_v1.md`, `LAYOUT_OPS58_v1.md` and `ROADS_OPS58_v1.md`;
- pack v6 (`build_pack_drop2_v6.py`), which adds the ops 5-6 pad fills and the 4 causeways to the ops 3-4 ground; every ASSUMED fill is listed in `planner_ops56_v1/ground_requests_applied.json`;
- roads on dry ground only, searched over the whole map, with the same rules as ops 3-4.

Outputs are in `planner_ops56_v1/op5` and `op6` (plan json, checks json, png, log). All numbers are MEASURED unless marked otherwise.

## Op 6 (23 min)

| Check | Result |
|---|---|
| Pads | Every pad has a spot. The worst pad change is 6-05 at 3.47 m |
| Roads | 16 roads, 28.1 km. Worst grade 12.8 % |
| Not reached | **6-03** (Fuel Depot at (9600, 12000)). The router found paths to 6-05 and 6-M1, but rejected each one at the junction with the net, where the step in level was 0.67-1.6 m |
| Off the net by decision | 6-M3 and 6-M3.2 (roads R2), 6-F (ground check f3), and the op 6 start (roads R3) |
| Other checks | Pass |

## Op 5 (30 min)

| Check | Result |
|---|---|
| Pads | **No spot within 144 m: 5-M2.3** (Basic Trenchline, 114 × 60 m) and **5-M2.5** (Small Rectangle FOB). The worst pad change is 5-F.3 at 2.76 m |
| Roads | 18 roads, 24.4 km. Worst grade 12.8 %. The trunk from the op 5 start to 5-M1 is 3.0 km |
| Long road | 5-03 → 5-F.3 is 11.5 km against 3.7 km straight (3.1×) |
| Not reached | **5-M2** (the tunnel holdout: every road to it crossed its own pad). **5-12** and **5-02**: no route was found from the net |
| Off the net by decision | 5-M4, 5-05, 5-04 (roads R2), and 5-13 (ground check f4) |
| Other checks | Pass |

## Decisions (Kernel)

| # | Finding | Answer | source |
|---|---|---|---|
| P1 | 6-03 no road (junction steps 0.67-1.6 m) | a Ground request: level the ground at the 6-03 → 6-05 junction (0.67 m step) | HUMAN |
| P2 | 5-M2.3 (Trenchline) and 5-M2.5 (FOB) no pad within 144 m | a Ground requests: fill under both at their layout seats (3476, 12644) yaw 90 and (3386, 12521) | HUMAN |
| P3 | 5-M2 Royal Tunnel Holdout no road (routes cross its own pad) | a Foot link from the Turbolaser Tower, 17 m away | HUMAN |
| P4 | 5-02 no route (router about 10.4 % per step) | a Ease the router grade to 14 % per step for the 5-02 road only (still held to the 14 % rule) | HUMAN |
| P5 | 5-12 no route | a Ease the router grade to 14 % per step for the 5-12 road only | HUMAN |
| P6 | 5-03 → 5-F.3 11.5 km (3.1×) | c Let the re-run pick how 5-03 joins | HUMAN |
| P7 | 6-03 still no road after the P1 fill (second run: junction steps 0.67-1.39 m) | d Ramp piece at the junction, logged as a ramp spec | HUMAN |

### Ramp spec for 6-03 (P7)

| Item | Value | Tag |
|---|---|---|
| Where | The 6-03 road's junction at the west edge of 6-05, about (10105, 11825). 6-05 is at (10200, 11800), yaw 15, half-length 98.5 m | ASSUMED (the edge the best try used; the log gives no point) |
| Rise | 0.67 m (the smallest step of the rejected tries) | MEASURED |
| Length at 14 % | 4.8 m | MEASURED (from the rise) |
| Deck | 7 m, the road width | ASSUMED |
| Between | 6-03 (Fuel Depot, pad +1.0 m) and 6-05 (Medium AA Base, pad +3.75 m) | MEASURED |

With the ramp, the 6-03 road (about 0.6 km, worst grade 12.8 % on the tries) joins the net. The road line itself waits for the next planner run with the ramp allowed.
