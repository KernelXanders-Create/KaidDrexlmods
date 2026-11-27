# House fit: the 6-M4 town and the 5-13 hamlet — v1

Run on 2026-11-27, on ground pack v10. This checks whether the planned houses fit round the guard pads and streets:
- the 6-M4 town, about 80 buildings (call 27);
- the 5-13 hamlet, about 30 houses (call 28 A).

Script: `hamlet513/housefit.py`. Output: `hamlet513/housefit_v1.json`. Counts are MEASURED on the stated rules; the rules marked ASSUMED are mine.

## Rules

- **Plot:** a square of 20 m, or of 25 m to leave room for lanes. A house of about 14 m is the middle of the house sizes in the K6 grader, with 3 m all round it. Both plot sizes are ASSUMED.
- **Grid:** plots are laid on a grid, with every 5 m offset tried. The best count is kept.
- **A plot counts when:**
  - all of it is dry, +0.5 m or higher (the village form rule);
  - it is 5 m clear of the +0.3 m water line (ASSUMED);
  - it is 3 m clear of a road or street edge (the planner rule; 7 m roads);
  - it is 5 m clear of a guard pad (ASSUMED).
- **Town ground:**
  - 6-M4: its dry rise within 400 m of (13600, 11200), as in `TOWN_JOINS_6M4_v1.md`;
  - 5-13: its dry rise within 200 m of (1840, 9705) (200 m ASSUMED).
- **Pads and streets used:**
  - 6-M4: the FOB and both guns (`TOWN_GUARDS_6M4_v1.md`), the SSW stub, and the op 6 roads;
  - 5-13: both gates and the gun, both stubs, and the op 5 roads (`HAMLET_513_v1.md`).

## Result

| Town | Dry rise | Usable | Wanted | 20 m plots | 25 m plots |
|---|---|---|---|---|---|
| 6-M4 Cauldron Apron Town | 13.2 ha | 10.8 ha | about 80 | 179 | 105 |
| 5-13 Stake Hamlet | 6.7 ha | 5.0 ha | about 30 | 77 | 45 |

Both fit, even with 25 m plots. That is 1.3× the wanted count for 6-M4 and 1.5× for 5-13.

## Reading (AI)

- The grid count is a ceiling on a clean grid. A real layout with streets, a square and turned houses will hold fewer.
- Even so, the 25 m count leaves a margin over the wanted number in both towns.
- The house types for the Suddra towns are not chosen yet. A town of big houses (about 20 m or more) would need to be checked again.
