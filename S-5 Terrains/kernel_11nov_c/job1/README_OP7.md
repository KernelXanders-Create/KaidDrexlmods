# KERNEL_RETURN_11NOV_C_JOB1_OP7_v2: op 7 (The Rim), ground plan

**v2 changes one thing from v1:** the Ash Crescent shores in `op7_notes.md`. The 547 m, 503 m, 148 m and 80 m stretches are on Kameni, not Ash Crescent. The plan, checks and image are unchanged.

**One rule fails: rule 3, for 7-M1 Skaros Rock Keep only.** It stands on a 22 m lagoon ledge under a 130 m climb of 40-60 % ground, so it has a stair, not a road. Every other rule passes. Every other vehicle site and Oyra are on one net, joined to op 6's road to the Prophet Monastery. Read the first lines of `op7_notes.md`.

| File | What it is |
|---|---|
| `op7_plan.json` | The plan. **Sites:** id, name, composition, centre x / y, yaw, pad half-sizes hx / hy, pad level z, cut and fill, entrance bearing and point, rough point, metres moved, size evidence. **Squad positions:** the same, plus what each guards. **Town:** Oyra, tied to its K6 v2 layout, with its purpose-map point, the offset and the road port used. **Roads:** points every 4.5 m with `points_z`, kind, the two things each links, grade, cut/fill. **Also:** the other ops' roads this net joins, the keep's stair (top and bottom), approaches, landing shores, the moves. |
| `op7_plan.png` | The plan over a hillshade of your build-4 ground (5 m grid): pads by role, roads, the stair, landing shores, entrances, op 4 and op 6 pads (hatched) and roads (grey dashed), red dotted lines from each purpose-map point to its final pad, and a red X at Oyra's purpose-map point. |
| `op7_checks.json` | Each rule with numbers: status, worst case, where. |
| `op7_notes.md` | The failing rule, the three least-sure things, Oyra (job 2), the Rim Chora (no layout yet), moves, sizes, approaches, squad positions, shores and roads. |
| `tools/` | The planner, to read as text. `world.py` loads your 5 m grid, `planner.py` places pads, routes roads and finds shores, and `run_op.py` runs one op. `op7.py` is this op's site list, town (with its five road ports), the op 4 and op 6 plans it joins, net order, squad anchors, approaches and router settings. |

## Tools changed since op 6
- **An op can load other ops' finished plans** (`EXTERNAL_PLANS`). Their pads in the box are blocked, and their roads are fixed ground that a new road may join. Rule 3 counts their roads as one existing net.
- **New join points:** a pad's free edges, and a joined town's other street ends.
- **Town buildings:** the building check exempts the last 25 m at any of a town's street ends, not only the first one used.

Ops 3-6 (already sent) stand as sent.

## How it was made
1. **Every site:** the planner searched around the purpose map's rough point, at every 15° of yaw, for the pad that changes the 5 m grid least. The rules stay hard throughout: 4.0 m of change, 17 m from pads at other levels, 10 m from the +0.3 m line. Search starts small and widens only if nothing fits.
2. **Roads:**
   - **Routing:** the net grows from op 4's and op 6's roads, and each site joins the nearest level part of the net by a search on the 5 m grid. The search avoids water, pads and the town (with their band and clearance), side slopes over 50 % and cliff edges.
   - **Profile:** each road's profile is held to 14 % and repaired until every grid point it fixes is within 4 m of the ground. Each end has a 16 m level landing at the pad's or junction's level.
3. **Squad positions:** placed with the same rules near anchors on the approaches.
4. **Shores:** found on the grid as water-edge points with gentle ground behind.
5. **Checks:** each rule measured on the result.

Job 2's last towns and op 8 are not in this zip. Op 8 comes next.
