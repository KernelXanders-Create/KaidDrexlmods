# KERNEL_RETURN_11NOV_C_JOB1_OP8_v2: op 8 (The Caldera Yard), ground plan, re-pass

**One rule fails: rule 3.**
- **The Yard's inner shore and the south arm:** no road joins them within the rules. The ramp road they need is given (item 3): 131 m of rise, a 936 m zig-zag at 14 %, 7 m deck, from the fuel quay up to the South Arm Gun Line.
- **8-M4 Yard Power Plant** has no road.

Read the first lines of `op8_notes.md`. Everything else passes your way (`tools/verify.py`).

**Also answered:**
- **Item 4:** op 7's Skaros keep is joined to the Yard by a 1,474 m shore road.
- **Item 13:** the Yard's layout. The dry dock goes on the west side, facing the lagoon, and the foundry in the south-east. A second, foundry pad on the shelf gives 72,000 m² against one pad's 81,600 m².

| File | What it is |
|---|---|
| `op8_plan.json` | The plan, with `ramps_needed` (the item 3 ramp), the dam line, roads, the Skaros shore road (`7-M1 (op 7)-8-F`), and moves from the design points. |
| `op8_plan.png` | The plan over a hillshade; the ramp GAP; the ops 4 / 6 / 7 pads and roads. |
| `op8_checks.json` | Each rule with numbers. |
| `op8_notes.md` | The failing rule and the ramp, item 4, item 13 (the Yard), built sizes, the dam and roads. |
| `tools/` | The planner and `verify.py`. |

**New since op 7 v3:** a net can be joined to another op's pad (the Skaros keep) or to a fixed point. Where two parts of a net cannot be joined by any road, the ramp between their nearest road points is given.

With this zip the re-pass of ops 3-8 is complete.
