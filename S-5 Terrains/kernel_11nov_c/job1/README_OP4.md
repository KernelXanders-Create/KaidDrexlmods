# KERNEL_RETURN_11NOV_C_JOB1_OP4_v1: op 4 (Cinder Road), ground plan

**No rule fails, but the AI road breaks at two terrain steps (the south causeway head and the north causeway's cone end) that need your ramps. Read the first lines of `op4_notes.md`.**

| File | What it is |
|---|---|
| `op4_plan.json` | The plan. **Sites:** id, name, composition, centre x / y, yaw, pad half-sizes hx / hy, pad level z, cut and fill, entrance bearing and point, rough point, metres moved, size evidence. **Squad positions:** the same, plus what each guards. **Town:** Causeway Foot, tied to the K6 v2 layout. **Trunk breaks:** the two gaps. **Roads:** points every 4.5 m with `points_z`, kind, the two things each links, grade, cut/fill. **Also:** foot links, approaches, landing shores, the moves. |
| `op4_plan.png` | The plan over a hillshade of your build-4 ground (5 m grid): pads by role, roads, landing shores, the two GAPs (red X), entrances, and red dotted lines from each purpose-map point to its final pad. |
| `op4_checks.json` | Each rule with numbers: status, worst case, where. |
| `op4_notes.md` | The gaps, the three least-sure things, moves, sizes, approaches, squad positions, shores and roads. |
| `tools/` | The planner, to read as text. `world.py` loads your 5 m grid, `planner.py` places pads, routes roads and finds shores, and `run_op.py` runs one op. `op4.py` is this op's site list, trunk, nets, squad anchors and approaches. |

## Tools changed since op 3
- A trunk: an AI road through given stops, with through-comps.
- Trunk stops are placed before the other pads.
- A fix to the straight-run breaker, which had been cutting switchback corners.
- A check that the ground under a road's band varies by at most 7.6 m.
- Other pads stay blocked near road ends.

Op 3 (v1, already sent) was made with the earlier router. Re-run on this one, it reaches fewer sites (the band check is stricter on Sound Isle's slopes), so op 3 v1 stands; it passes every rule.

## How it was made
1. **Every site:** the planner searched around the purpose map's rough point, at every 15° of yaw, for the pad that changes the 5 m grid least. The rules stay hard throughout: 4.0 m of change, 17 m from pads at other levels, 10 m from the +0.3 m line. Search starts small and widens only if nothing fits.
2. **Trunk first:** the trunk's stops are placed first, then the trunk is routed, then the other sites are placed around it.
3. **Roads:**
   - **Routing:** each net grows from the trunk; each site joins the nearest level part of the net by a search on the 5 m grid. The search avoids water, other pads (with their band and clearance), side slopes over 50 % and cliff edges.
   - **Profile:** each road's profile is held to 14 % and repaired until every grid point it fixes is within 4 m of the ground. Each end has a 16 m level landing at the pad's or junction's level.
4. **Squad positions:** placed with the same rules near anchors on the approaches.
5. **Shores:** found on the grid as water-edge points with gentle ground behind.
6. **Checks:** each rule measured on the result.

Job 2 (towns on the map) and ops 5-8 are not in this zip. Ops 5 and 6 come next.
