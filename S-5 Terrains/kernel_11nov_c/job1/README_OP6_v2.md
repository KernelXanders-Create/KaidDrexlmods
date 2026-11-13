# KERNEL_RETURN_11NOV_C_JOB1_OP6_v2: op 6 (Prophet Massif and Signal Isle), ground plan, re-pass

**One rule fails: rule 3.**
- **The link to op 4:** the massif's net reaches op 4's net only by a road that breaks 4 m (5.01 m at 7 grid points, over 582 m of its 2,895 m), so it needs a cutting, a retaining wall or a ramp there.
- **Four sites have no road:** 6-M3, 6-07, 6-04 and 6-14.

Read the first lines of `op6_notes.md`. Every other rule passes, measured your way (`tools/verify.py`).

**Item 11 is answered:** each coastal work has a pier at the water and a lift (or stair) up its cliff, with top, foot and pier points (`shore_links`).

| File | What it is |
|---|---|
| `op6_plan.json` | The plan, with `links_to_existing_net` (the best link road and its failing stretch), `shore_links`, `edits_to_other_ops_roads` (none this time), Kamar Village, roads, foot links and moves. |
| `op6_plan.png` | The plan over a hillshade; op 4's pads and roads hatched and dashed; the link GAP. |
| `op6_checks.json` | Each rule with numbers. |
| `op6_notes.md` | The failing rule, item 11, Kamar Village, built sizes, foot paths and roads. |
| `tools/` | The planner and `verify.py`. |

**New since op 5 v2:**
- **Coastal works:** each gets a shore link (pier, plus a stair or lift).
- **A link to another op's net** is tried on its own. If no road holds, the best try is kept with the stretch where it breaks.
- **A join on another op's road** may give that road a level landing. Any such change is listed as an edit to that road; op 6 makes none.
