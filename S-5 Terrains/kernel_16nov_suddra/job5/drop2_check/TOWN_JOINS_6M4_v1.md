# 6-M4 Cauldron Apron Town: where its two roads join — v1

Run on 2026-11-27. Under call 27 and JOB_5 decision 28, the town has two roads:
- one at its south-south-west edge, from 6-M3 Tank Laager;
- one at its north edge, from 6-06 NE Esker Fort.

The pack 5 answers left the join points and levels NOT MEASURED until the drop 2 ground. They are measured here on pack v7, against the op 6 plan in `planner_ops56_v3/op6`.

Script: `town64/town64.py`. Output: `town64/town64_v1.json`. Numbers are MEASURED unless marked otherwise.

## How it was measured

- The town is taken as the dry rise round its sketch point (13600, 11200): ground at +0.5 m or higher, joined to the point, within 400 m. The +0.5 m comes from the village form rule; the 400 m limit is ASSUMED.
- Each road joins where its approach bearing leaves that rise.

## The town's rise

| Item | Value |
|---|---|
| Ground at the point | +0.88 m |
| Rise area | 13.2 ha |
| Rise level | +0.50 to +2.04 m |
| Rise extent from the point | x −180 to +350 m, y −175 to +330 m |
| Room for about 80 buildings | 13.2 ha is about 1,650 m² per building. My reading is that it fits (AI; NOT MEASURED against a house layout) |

## The two joins

| Road | Join point | Ground at the join | Beyond the join | Nearest planned road |
|---|---|---|---|---|
| N, toward 6-06 (0°) | (13600, 11400), 200 m N of the point | +0.52 m | Wet from 225 m out. 380 m of the 1,200 m straight line to 6-06 is at or below +0.3 m | 6-M4 → 6-11, 127 m away. That road leaves the town NE at 41° and reaches 6-06 by way of 6-11 |
| SSW, toward 6-M3 (214°) | (13491, 11038), 195 m from the point | +0.53 m | Wet from 200 m out, 5 m past the join. 930 m of the 1,442 m line to 6-M3 is wet | None on this side. 6-M3 is off the net (roads R2) |

## Reading (AI)

- **The N road:** a straight road due north would cross 380 m of water. The planned dry road reaches 6-06 instead, leaving the town to the NE.
- **The SSW road:** this road can only run to the shore. 6-M3 is an island with no causeway, and the gap measured in roads R2 is 759 m.
- **Both joins:** both sit at +0.52-0.53 m, about 0.2 m above the +0.3 m water line, with water 5-25 m beyond. That is inside the 10 m pad clearance rule if a gate or gun position stands there.
- **The FOB and SSW gun position:** call 27 puts them on the south edge by the SSW road. Their spots are NOT MEASURED.

## Decisions (Kernel)

| # | Finding | Answer | source |
|---|---|---|---|
