# KERNEL_RETURN_11NOV_C_JOB1_OP6_v1: op 6 (Prophet Massif and Signal Isle), ground plan

**No rule fails.** Every rule in your sheet reads PASS in `op6_checks.json`; junction steps are reported. Every vehicle site and Kamar Village are on one net, joined to op 4's. Read `op6_notes.md` first. Its first item: the cliff coast puts the ferry pens, the landers and the Signal Isle Landing high above the water.

| File | What it is |
|---|---|
| `op6_plan.json` | The plan. **Sites:** id, name, composition, centre x / y, yaw, pad half-sizes hx / hy, pad level z, cut and fill, entrance bearing and point, rough point, metres moved, size evidence. **Squad positions:** the same, plus what each guards. **Town:** Kamar Village, tied to its K6 v2 layout, with its purpose-map point, the offset and the road port used. **Roads:** points every 4.5 m with `points_z`, kind, the two things each links, grade, cut/fill. **Also:** approaches, landing shores, the moves. |
| `op6_plan.png` | The plan over a hillshade of your build-4 ground (5 m grid): pads by role, roads, landing shores, entrances, op 4's 4-10 pad (hatched, the net's root), red dotted lines from each purpose-map point to its final pad, and a red X at the village's purpose-map point. |
| `op6_checks.json` | Each rule with numbers: status, worst case, where. |
| `op6_notes.md` | The three least-sure things, Kamar Village (job 2), moves, sizes, approaches, squad positions, shores and roads. |
| `tools/` | The planner, to read as text. `world.py` loads your 5 m grid, `planner.py` places pads, routes roads and finds shores, and `run_op.py` runs one op. `op6.py` is this op's site list, town (with its five road ports), op 4's root pad, net order, squad anchors, approaches and router settings. |

## Tools changed since op 5
- **A net can grow from another op's pad** (`EXTERNAL_PADS`). That pad is blocked for this op's pads and roads.
- **A town can join a net** at any of several road ports (street ends). The rule-3 check now covers towns with a vehicle approach.
- **Roads keep off a town's whole outline,** not only its buildings, except at the town's own road port.
- **Sites can be seated after the roads** (`LATE_SITES`), beside them, then joined by a spur.
- **Join points stay 40 m from a pad's own landing** (roads joining there had touched the pad).
- **The profile repair target is a per-op setting.**
- **Road bands are measured with a k-d tree.** Same results to 0.03 m (checked by re-running op 5), and long roads are several times faster.

Ops 3-5 (already sent) stand as sent: these changes only add options or speed.

## How it was made
1. **Every site:** the planner searched around the purpose map's rough point, at every 15° of yaw, for the pad that changes the 5 m grid least. The rules stay hard throughout: 4.0 m of change, 17 m from pads at other levels, 10 m from the +0.3 m line. Search starts small and widens only if nothing fits.
2. **Roads:**
   - **Routing:** the net grows from op 4's 4-10 pad. It climbs to the east upland first, then spreads, and each site joins the nearest level part of the net by a search on the 5 m grid. The search avoids water, pads and the village (with their band and clearance), side slopes over 50 % and cliff edges.
   - **Profile:** each road's profile is held to 14 % and repaired until every grid point it fixes is within 4 m of the ground. Each end has a 16 m level landing at the pad's or junction's level.
3. **Squad positions:** placed with the same rules near anchors on the approaches.
4. **Shores:** found on the grid as water-edge points with gentle ground behind.
5. **Checks:** each rule measured on the result.

Job 2's remaining towns and ops 7-8 are not in this zip. Op 7 comes next.
