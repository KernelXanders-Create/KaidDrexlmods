# KERNEL_RETURN_11NOV_C_JOB1_OP8_v1: op 8 (The Caldera Yard), ground plan

**One rule fails: rule 3.** The Yard and the inner shore sites are on their own road net. An inner cliff of 20-110 m all round the lagoon keeps them from the south arm's net, which joins op 4's at Causeway Foot. The lowest step is marked GAP on the plan (19.4 m over 355 m, near the dam); a ramp there joins the nets. Every other rule passes. Read the first lines of `op8_notes.md`.

| File | What it is |
|---|---|
| `op8_plan.json` | The plan. **Sites:** id, name, composition, centre x / y, yaw, pad half-sizes hx / hy, pad level z, cut and fill, entrance bearing and point, rough point, metres moved, size evidence. **Squad positions:** the same, plus what each guards. **Roads:** points every 4.5 m with `points_z`, kind, the two things each links, grade, cut/fill. **Also:** the op 4 roads this net joins, the GAP (in `trunk_breaks`), the dam line (in `gate`), approaches, landing shores, the moves. |
| `op8_plan.png` | The plan over a hillshade of your build-4 ground (5 m grid): pads by role, roads, the dam line, the GAP (red X), landing shores, entrances, the pads and roads of ops 4, 6 and 7 (hatched and grey dashed), and red dotted lines from each purpose-map point to its final pad. |
| `op8_checks.json` | Each rule with numbers: status, worst case, where. |
| `op8_notes.md` | The failing rule and the GAP, the Yard's shelf and the dam, router settings, moves, sizes, approaches, squad positions, shores and roads. |
| `tools/` | The planner, to read as text. `world.py` loads your 5 m grid, `planner.py` places pads, routes roads and finds shores, and `run_op.py` runs one op. `op8.py` is this op's site list, dam line, GAP, the op 4, 6 and 7 plans it joins, the two nets, squad anchors, approaches and router settings. |

## Tools changed since op 7
- **Rule 3 is checked per island.** Nets named "<island>: <part>" must join up, so a second net on one island now FAILs, as it should. Every earlier op had at most one net per island, so ops 3-7 read the same.
- **Each road tries every nearby existing road,** not only the nearest few points of the net (the Yard Power Plant only joins op 4's net this way).
- **Known gaps can be marked** (`GAPS`), and the dam line has its own label.

Ops 3-7 (already sent) stand as sent. **One correction to op 7's notes** is in `KERNEL_RETURN_11NOV_C_JOB1_OP7_v2.zip`: the 547 m, 503 m, 148 m and 80 m shores I gave as Ash Crescent's are on Kameni, the lagoon islet.

## How it was made
1. **Every site:** the planner searched around the purpose map's rough point, at every 15° of yaw, for the pad that changes the 5 m grid least. The rules stay hard throughout: 4.0 m of change, 17 m from pads at other levels, 10 m from the +0.3 m line (harbour and beach works exempt). Search starts small and widens only if nothing fits.
2. **Roads:**
   - **Routing:** the arm net grows from op 4's, op 6's and op 7's roads; the inner shore net grows from the Yard. Each site joins the nearest level part of its net by a search on the 5 m grid. The search avoids water, pads (with their band and clearance), side slopes over 60 % and cliff edges.
   - **Profile:** each road's profile is held to 14 % and repaired until every grid point it fixes is within 4 m of the ground. Each end has a 16 m level landing at the pad's or junction's level.
3. **Squad positions:** placed with the same rules near anchors on the approaches.
4. **Shores:** found on the grid as water-edge points with gentle ground behind.
5. **Checks:** each rule measured on the result.

Job 1 is complete with this zip (ops 3-8). Job 2's tie-ins are in each op's notes (Sound Head op 3, Causeway Foot op 4, Kastro Quay and Lantern Quay op 5, Kamar Village op 6, Oyra op 7). Perys is op 1-2 ground, outside job 1's ops 3-8, so it was not tied in here. Next are the three spare-hour questions and the stair and comp-pad items.
