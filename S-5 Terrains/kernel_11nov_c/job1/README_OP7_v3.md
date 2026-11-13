# KERNEL_RETURN_11NOV_C_JOB1_OP7_v3: op 7 (The Rim), ground plan, re-pass

**One rule fails: rule 3, for 7-M1 Skaros Rock Keep (as before) and 7-03 Crest Road Checkpoint.** Read the first lines of `op7_notes.md`.

Every other rule passes, measured your way (`tools/verify.py`): 0 of 15 roads over 14 %, every pad within 4 m, junction steps at most 0.29 m. One net on Ember Crescent reaches the Chora, Oyra, the Narrows and Oyra Head, and is joined to op 6 v2's net.

| File | What it is |
|---|---|
| `op7_plan.json` | The plan, with Oyra's `street_extensions`, `edits_to_other_ops_roads` (one level landing on op 6 v2's road), roads, foot links and moves. |
| `op7_plan.png` | The plan over a hillshade; your built Oyra Head road and the op 4 / op 6 roads dashed. |
| `op7_checks.json` | Each rule with numbers. |
| `op7_notes.md` | The failing rule, the net, your built road (item 10), Oyra (item 15), built sizes and roads. |
| `tools/` | The planner and `verify.py`. |

**New since op 6 v2:**
- **Towns:** a town joins the net 15 m out on its street's line (the street extended).
- **Pieces:** parts of one net that grew apart (each joined to a different existing road) are joined by a road where one holds.
