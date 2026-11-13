# KERNEL_RETURN_11NOV_C_OPS_1_2_REPASS_v2: ops 1 and 2, re-pass of what is built

**v2 changes two things from v1 (your answers):**
- 2-10 is re-seated beside the net;
- the Perys roads come in on the main street M (each stops 25 m out on M's line, and M is extended 25 m to meet them).

Op 2's files are unchanged from v1.

**One rule break is left,** op 1's `1-06-through` piece (a 164 m straight across the depot's floor). See the first lines of `OPS_1_2_REPASS_NOTES.md`. Everything else the audit found is fixed in `op1_repass.json` / `op2_repass.json`, with its numbers.

| File | What it is |
|---|---|
| `OPS_1_2_REPASS_NOTES.md` | The rule breaks left, the audit, every change with its numbers, the pads to check, and how to apply. |
| `audit_ops_1_2.json` | The audit of your built ops 1-2 on the build-4 grid: pads, every road's grade (point to point, 10 m, 20 m), straights, clearance, the net. |
| `op1_repass.json`, `op2_repass.json` | The fixes: re-seated pads (old and new), new roads and stubs, roads re-drawn (whole, levels to the millimetre), roads re-ended on Perys v7, pads off level. |
| `op1_repass.png`, `op2_repass.png` | Each op over a hillshade: your roads kept (grey), re-drawn (orange), new (red), re-ended on Perys (purple), re-seated pads (blue), pad points off level (magenta x), the Perys v7 houses (yellow). |
| `tools/` | `audit12.py` and `repass12.py`, with the planner they use (`world.py`, `planner.py`). |
