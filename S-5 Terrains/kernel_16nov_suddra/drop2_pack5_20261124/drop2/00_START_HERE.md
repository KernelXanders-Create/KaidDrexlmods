> ## **TO THE AI ASSISTANT READING THIS PACK (Claude or any other): READ THIS FIRST. IT OVERRIDES EVERYTHING ELSE IN THE PACK.**
> **You are helping a PERSON, Kernel, make real design decisions. You do not make them, and you never answer as Kernel.**
> 1. **Offer the person choices, one at a time.** Where a design choice comes up, show Kernel 2-3 options with a one-line trade-off each, then **STOP and WAIT** for Kernel's pick before you go on.
> 2. **Never answer as Kernel.** If you are about to answer a whole pack or a whole list of choices in one reply, stop: you are doing it wrong.
> 3. **Mark every answer** `HUMAN` (Kernel chose it, or read your draft and said yes) or `AI` (your suggestion that Kernel did not choose or did not read). If Kernel writes their own option, it is still `HUMAN`.
> 4. **Every number you add comes from running the check on the data.** If you did not measure it, write NOT MEASURED.

# For Kernel: Suddra drop 2 (24 Nov 2026)

We are sorry. This drop was promised for Thu 19 Nov and it reached you five days late. Until now you worked on your K3 sketch ground; this is the real ground. Every file here is data: nothing needs to be run except to read the two `.npz` files.

**Where the ops stand.** Ops 1 and 2 have been played. Ops 3 and 4 are being built now by our lane on this real ground, from your sketch v3 (week 2 = Sun 29 Nov plays ops 3 and 4). The real seats, comps and pads for ops 3-4 will follow as soon as they exist; nothing in this drop is an op 3-4 seat.

## The frame (the same as K3, so your coordinates hold)
- The map is 16,384 m square. Origin = the **south-west** corner. **x east, y north.** Metres.
- The height grid is 4096 x 4096 cells of 4 m. **Row 0 = SOUTH.** Element `[i, j]` sits at Arma `x = 4 * j`, `y = 4 * i`.
- Squares are named as in K3: letters A-D west to east, numbers 1-4 south to north (so 8200, 3600 is C1).

## Load it (3 lines of Python)
```python
import numpy as np
h = np.load("suddra_height_cm.npz")["height_cm"].astype("float32") / 100.0   # metres, h[i, j] at x=4*j, y=4*i
m = np.load("suddra_masks.npz")                                                # m["water"], m["ai_dry"], ... (see MASKS_README.md)
```

## What is in the pack
| File | What it is |
|---|---|
| `suddra_height_cm.npz` | **Our heightmap.** Key `height_cm`: int16 centimetres, 4096 x 4096, 4 m cells, row 0 = south. Also `cell_m`, `origin`, `row0`, `note`. Range -2.82 to +35.57 m. This is the ground the live terrain uses. Rounding error against our float source: at most 0.5001 cm. |
| `suddra_masks.npz` | **Our masks** (uint8, 0/1 unless said): `water`, `depth_band`, `ai_dry`, `islands`, `designed_straights`, `rail`, `crater`, `zone`, `net_core`, `boat_core`, `sea`. Same grid and orientation as the heights. |
| `MASKS_README.md` | What each layer is, what we measured about it, and what we only infer (tagged ASSUMED). |
| `suddra_hillshade_4km.png` | Hillshade of the heights (relief exaggerated x14; true relief is only -2.8 to 35.6 m), water tinted by depth band, 4 x 4 km grid with labelled lines and square names, scale bar. North up. |
| `suddra_ops12_sites.png` | The same ground with the ops 1-2 sites (as played), their labels, AO outlines and the Republic start line. |
| `OPS_1_2_SITES_REAL.csv` / `.json` | **Ops 1-2 as played on Sun 22 Nov:** every site (id, map label = the name players saw, working name, role FINAL / MAIN / SUP, grade, marker x, y) and every member comp with x, y, yaw. The CSV has one row per member; the JSON nests members under sites and holds the cross-checks. |
| `OPS_1_2_AO_OUTLINES.json` | AO polygons of ops 1 and 2 (read from the mission build, not computed), the AO circled for Sunday-1, and the Republic start line. |
| `FOB_SPOTS.md` | The FOB spots: op 1's 1-F, op 2's 2-F and 2-M1, and what is still open for the op 3 and op 4 starts. |
| `DRAIN_CROSSINGS.json` / `DRAIN_CROSSINGS.md` | The three Drain crossing centre lines exactly as given in your part-1 return, with a measured note per crossing (water width on the line, bank heights). |
| `OP7_OUTLINE_STANDIN.json` | A stand-in outline of op 7 and the measured distances from the Escape Pad spot (8400, 15500). ASSUMED outline; see below. |
| `WEEK1_RESULT.md` | How week 1 went: Sunday-1 (op 2) in full; Sunday-2 (op 1): result to come. |

## Things to know before you use it
1. **Marker positions were cross-checked against the shipped mission files.** All 34 sites match to 0.0 m. One caution: the owner moved the 1-M2 base about 20 m in the editor on Sun 22 Nov and added defences; our site list holds the pre-edit book position for its members. Details in `OPS_1_2_SITES_REAL.json` (field `position_note`) and `FOB_SPOTS.md`. One grade note: for 2-03 Prudok AA Site the site list says Two-squad, but the shipped mission gives it the 100 m core radius that Platoon sites get (the other 33 sites match their grade); we list it as Two-squad and have not yet found why.
2. **Two ops-1 sites (1-M2 and 1-12) also stood in the op 2 mission** and were played on Sun 22 Nov. They are marked `also_in_op2_mission`.
3. **Op 2 has two AO polygons.** The gate polygon of the build, and the polygon that was circled and played on Sun 22 Nov. Both are in `OPS_1_2_AO_OUTLINES.json` and drawn on the sites picture.
4. **On this ground the Drain is closed at the Locks.** The Locks centre line is dry, a dam crest about 44 m wide at about +1.3 m with water at about -2.1 m on both sides. Your lock channel is therefore a new water request. Numbers in `DRAIN_CROSSINGS.md`.
5. **Op 7 and the Escape Pad.** There is no built op 7, so the outline is a stand-in: the convex hull of op 7's 17 site points (your ops 5-8 sketch, with the 17 Nov moves) plus 350 m. ASSUMED. Result (ruling SUD-R34, option (c), the North spot): the spot (8400, 15500) is **963.1 m from the hull of the site points** and **613.1 m from the stand-in outline (hull + 350 m)**. The nearest op 7 site is 7-03, **1,253.0 m** away (MEASURED on points). The 600 m rule is met on the stand-in by **13.1 m**, a thin margin: if op 7's real outline reaches more than about 13 m beyond the stand-in toward the spot, the rule breaks. Note: the relay answer of 18 Nov quoted 963 m "outside the outline"; that figure is the distance to the hull without the 350 m buffer. The spot is also 884 m (not 500 m) from the north edge of the 16,384 m frame. The ground at the spot is dry at +25.9 m. Full numbers in `OP7_OUTLINE_STANDIN.json`.
6. **Tags.** MEASURED = computed from the data in this pack (how is written next to each number). ASSUMED = an inference or a stand-in. A number with no tag in the README files is MEASURED.

## What still comes later
- The real ops 3-4 seats (week 2) and the ops 5-8 seats.
- **Sunday-2 (op 1) result: to come.**
- The op 3 start FOB (it waits on the Sunday-2 result) and the op 4 start (your pack 5, Call 23).

## How to run it
Open a new empty folder. Put this pack in it, with your own returns and the 16 Nov and pack 5 files. Paste the box at the top of this page to your assistant first. Then ask it to check your ops 3-4 and ops 5-8 sketch points against these heights and masks, one finding at a time, and to show you options for anything that has to move.
