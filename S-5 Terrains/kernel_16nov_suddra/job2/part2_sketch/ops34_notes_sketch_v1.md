# Ops 3-4 notes, sketch dry run v1

**What this is:** the full JOB_2 part 2 run on the K3 A sketch ground (16 m cells from hand-placed landforms, resampled to 5 m), as the pack asks until drop 2 (decision of 17 Nov: full dry run). The method, data structure and checks are now proven end to end; on drop 2 it is a re-run. Every level and distance here is a sketch number.

## What the run found (and what you decided)
- **3-09 and 3-10 stood north of the Drain** (664 m and 599 m), out of op 3's reach. Moved south (decision 42).
- **4-06 Plank Road Bridge is 503 m north of the Drain**; kept, the causeway crosses due south (decision 41).
- **At the Rail Bridge the K3 sketch has no water:** its rail embankment closes the Drain at x 8.2 km (MEASURED: the 245 m line between the bridge ends never goes below 0 m). The 3AS bridge spans dry ground on the sketch; drop 2 decides.
- **One op 3 road (lowest +0.39 m) and three op 4 roads (+0.34-0.42 m) dipped under +0.5 m**; raised to +0.5 m (fill 0.16 m at most).

## The rule still failing: S12 (checkpoints astride their road)
The planner joins every road to a pad's edge; no road runs through a checkpoint's passage. 8 checkpoints fail (3 in op 3, 5 in op 4). The fix is a planner change: route the road through the checkpoint pad along its axis. Not done yet; it comes before the drop-2 run.

## Changed by me in the planner (copied from the 11 Nov C tools)
- Pads keep 15 m (on the grid) off the +0.3 m line, so footprint edges hold 10 m.
- Every road bend is eased to a 12 m radius or more.
- A Suddra check after the run: AI roads raised to +0.5 m; grades, bends, cut / fill re-measured; and a cut-grid check measured your way (R1-R7).

## Pad sizes
Comps you built on Thirra use your built pad sizes (KNOWN). Others are ASSUMED, each with its basis in the plan.

## Not measured on the sketch
Recon distances and "out of sight" for reserves (no vegetation); gate axes (comps' authored gates); ops 1-2 sites, AOs and their 400 m and reserve checks (drop 2); the Fortress Dam's crest width.

## The three things I am least sure of
1. Whether the drop-2 Drain matches the K3 line at the three crossings (it moved 4-06's crossing 500 m already).
2. The ASSUMED pad sizes for the 15 comps without a built pad (and the village outline).
3. The gun bearings: drafted (AI) from the designed approaches, not yet reviewed by you.
