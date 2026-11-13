# KERNEL_RETURN_11NOV_C_JOB1_OP3_v1: op 3 (The Sound), ground plan

**No rule fails.** Every rule in your sheet reads PASS in `op3_checks.json`; junction steps are reported. Read `op3_notes.md` first: it gives the three things I am least sure of, including the reading of rule 3 the PASS depends on.

| File | What it is |
|---|---|
| `op3_plan.json` | The plan. **Sites:** id, name, composition, centre x / y, yaw, pad half-sizes hx / hy, pad level z, cut and fill, entrance bearing and point, rough point, metres moved, size evidence. **Squad positions:** the same, plus what each guards. **Town:** Sound Head, tied to the K6 v2 layout. **Roads:** points every 4.5 m with `points_z`, kind, the two things each links, grade, cut/fill. **Also:** foot links (stair top and bottom), approaches, landing shores, the sea gate line, the moves. |
| `op3_plan.png` | The plan over a hillshade of your build-4 ground (5 m grid): pads by role, roads, foot links, landing shores, the sea gate, entrances, and red dotted lines from each purpose-map point to its final pad. |
| `op3_checks.json` | Each rule with numbers: status, worst case, where. |
| `op3_notes.md` | The three least-sure things, the moves, sizes, stairs, approaches, squad positions, shores and roads. |
| `tools/` | The planner, to read as text. `world.py` loads your 5 m grid, `planner.py` places pads, routes roads and finds shores, and `run_op.py` runs one op. `op3.py` is this op's site list, nets, squad anchors and approaches. |

## How it was made
1. **Every site:** the planner searched around the purpose map's rough point, at every 15° of yaw, for the pad that changes the 5 m grid least. The rules stay hard throughout: 4.0 m of change, 17 m from pads at other levels, 10 m from the +0.3 m line. Search starts small and widens only if nothing fits.
2. **Roads:**
   - **Routing:** each net grows from one root; each site joins the nearest level part of the net by a search on the 5 m grid. The search avoids water, other pads (with their band and clearance), side slopes over 50 % and cliff edges.
   - **Profile:** each road's profile is held to 14 % and repaired until every grid point it fixes is within 4 m of the ground. Each end has a 16 m level landing at the pad's or junction's level.
3. **Squad positions:** placed with the same rules near anchors on the approaches.
4. **Shores:** found on the grid as water-edge points with gentle ground behind.
5. **Checks:** each rule measured on the result.

Job 2 (towns on the map) and ops 4-8 are not in this zip. Op 4 comes next.
