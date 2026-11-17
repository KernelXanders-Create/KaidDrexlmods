# Ops 3-4 notes, sketch dry run v2

**What this is:** the full JOB_2 part 2 run on the K3 A sketch ground (16 m cells from hand-placed landforms, resampled to 5 m), as the pack asks until drop 2. Every level and distance is a sketch number; on drop 2 the same run repeats. v2 fixes the one rule v1 failed (S12, checkpoints astride their road). **Both ops now pass every measured rule.**

## Decisions taken from the run (all HUMAN, in `../DECISIONS.md`)
- **41:** 4-06 Plank Road Bridge stays 503 m north of the Drain; the causeway crosses due south.
- **42:** 3-09 and 3-10 moved south of the Drain (they were out of op 3's reach).
- **43:** every checkpoint is seated astride a road of its net, centred, passage along the road (the passage is ASSUMED to be the comp's local y axis).
- **44:** op 3 gets its two entry roads from the 1-F FOB: the pipeline road through 3-05's point to 3-M2, and the spur road through 3-12's point to 3-M1. Checkpoint moves accepted: 3-05 97 m, 3-12 168 m, 3-M2's TKTA 173 m, 4-M2's gates 57 and 63 m, 4-06 317 m, the village guards 308 and 366 m.
- **45:** the village NNW gun position faces 330 deg (it fired through the re-seated checkpoint at 336 deg).
- **46:** the village's second approach is now E along the north bank from the Plank Road causeway (91 deg), not SSE past 4-07: the SSE way starts south of the Drain, where there is no crossing. This replaces part of decision 22.

## What else the run found
- **The Rail Bridge crosses no water on the sketch:** the K3 rail embankment closes the Drain at x 8.2 km. Drop 2 decides.
- **Roads under +0.5 m** were raised to +0.5 m: five in op 3 (lowest +0.32 m, on the pipeline entry road), two in op 4 (+0.42-0.48 m).
- **The 1-F FOB** counts as one road node: both op 3 entry roads leave it, 200 m apart. Its real spot comes in drop 2.

## Changes in the planner (copied from the 11 Nov C tools)
- Pads keep 15 m (on the grid) off the +0.3 m line, so footprint edges hold 10 m.
- Every road bend is eased to a 12 m radius or more.
- Checkpoints are seated astride a road after the net is built; the road's band takes the pad's level.
- Several entry roads (trunk chains) per op; a named point (the FOB) is one node for all of them.
- Roads are routed at 13 % so the cut-grid reading (where joining roads' bands overlap) stays under 14 %.
- After the run: roads raised to +0.5 m; grades, bends, cut / fill re-measured; a cut-grid check measured your way (R1-R7).

## Not measured on the sketch
Recon distances and "out of sight" for reserves (no vegetation); gate axes and passage axes (comps' authored gates); ops 1-2 sites, AOs and their 400 m and reserve checks (drop 2); the Fortress Dam's crest width.

## The three things I am least sure of
1. Whether the drop-2 Drain matches the K3 line at the three crossings.
2. The ASSUMED pad sizes for the 15 comps without a built pad (and the village outline).
3. The gun bearings: drafted (AI) from the designed approaches except 4-M1.3 (yours).
