# KERNEL_RETURN_11NOV_C_JOB1_OP5_v1: op 5 (Acropolis Isle), ground plan

**No rule fails.** Every rule in your sheet reads PASS in `op5_checks.json`; junction steps are reported. Read `op5_notes.md` first: it gives the three things I am least sure of, including the reading of rule 3 the PASS depends on (three sites are reached by stair, not road).

| File | What it is |
|---|---|
| `op5_plan.json` | The plan. **Sites:** id, name, composition, centre x / y, yaw, pad half-sizes hx / hy, pad level z, cut and fill, entrance bearing and point, rough point, metres moved, size evidence. **Squad positions:** the same, plus what each guards. **Towns:** Kastro Quay and Lantern Quay Hamlet, tied to their K6 v2 layouts, each with its purpose-map point and the offset. **Roads:** points every 4.5 m with `points_z`, kind, the two things each links, grade, cut/fill. **Also:** foot links (stair top and bottom), approaches, landing shores, the moves. |
| `op5_plan.png` | The plan over a hillshade of your build-4 ground (5 m grid): pads by role, roads, foot links, landing shores, entrances, red dotted lines from each purpose-map point to its final pad, and a red X at each town's purpose-map point. |
| `op5_checks.json` | Each rule with numbers: status, worst case, where. |
| `op5_notes.md` | The three least-sure things, both towns (job 2: road join, garrison, squad positions, quay; Kastro Quay shown at both points), moves, sizes, stairs, approaches, squad positions, shores and roads. |
| `tools/` | The planner, to read as text. `world.py` loads your 5 m grid, `planner.py` places pads, routes roads and finds shores, and `run_op.py` runs one op. `op5.py` is this op's site list, towns, net, squad anchors, approaches and router settings. |

## Tools changed since op 4
- **Town buildings are blocked for roads** (8 m round each centre). Rule 3's 3 m check now also tests town buildings, from the centre to the road edge, at 8 m or more.
- **Per-op router settings** (`PLAN_KW`). Op 5 loosens the band filter and the step limit for the island's steep flanks; every road is still measured against the 14 % and 4 m rules.
- **The plan shows each town's purpose-map point** and its offset from the layout.
- **A site with no road on its island gets a foot path to a town** on the same island (the beacon to Lantern Quay).

Op 4 (v1, already sent) was made before these changes. Measured with the new building check, its closest road comes 21 m from a Causeway Foot building centre, so it still passes. Op 4 v1 stands.

## How it was made
1. **Every site:** the planner searched around the purpose map's rough point, at every 15° of yaw, for the pad that changes the 5 m grid least. The rules stay hard throughout: 4.0 m of change, 17 m from pads at other levels, 10 m from the +0.3 m line. Search starts small and widens only if nothing fits.
2. **Roads:**
   - **Routing:** the Acropolis net grows from Kastro Quay's road port; each site joins the nearest level part of the net by a search on the 5 m grid. The search avoids water, pads and town buildings (with their band and clearance), side slopes over 50 % and cliff edges.
   - **Profile:** each road's profile is held to 14 % and repaired until every grid point it fixes is within 4 m of the ground. Each end has a 16 m level landing at the pad's or junction's level.
3. **Squad positions:** placed with the same rules near anchors on the approaches.
4. **Shores:** found on the grid as water-edge points with gentle ground behind.
5. **Checks:** each rule measured on the result.

Job 2's other towns and ops 6-8 are not in this zip. Op 6 comes next.
