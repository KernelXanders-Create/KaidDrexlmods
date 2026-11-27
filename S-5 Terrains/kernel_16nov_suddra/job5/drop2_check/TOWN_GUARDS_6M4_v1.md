# 6-M4 Cauldron Apron Town: seats for the FOB and the two guns — v1

Run on 2026-11-27, on ground pack v10, against the op 6 plan in `approaches36/run_a4/op6`. This follows call 27 B (HUMAN): one CIS Small Rectangle FOB with GPs and two CIS Heavy Gun Position + AA (UD), one gun by each of the town's two roads. The roads are set by T1 and T2 in `TOWN_JOINS_6M4_v1.md`.

Script: `town64/town64_guards.py`. Output: `town64/town64_guards_v1.json`. Numbers are MEASURED unless marked otherwise.

## Rules used

- Pad edge at least 10 m from the +0.3 m water line. This is checked on the 5 m grid points.
- The pad is levelled to the middle of the ground under it, with a change of no more than 4 m.
- Pad edge at least 3 m from any road edge. Roads are 7 m wide, and the T2 stub is taken as 7 m (ASSUMED).
- Pads at least 12 m apart.
- **"By the road":** the pad edge is within 25 m of that road's edge (ASSUMED).
- **Guns:** 300 m clear of other pads along the bearing, and no ground above the muzzle within 150 m. The muzzle is the pad level + 2.0 m (ASSUMED, as in the ops 3-4 checks).
- **Search:** pads tried every 5 m and every 15° of yaw.
- **Which spot is kept:**
  - the FOB, and then the SSW gun, nearest the stub's landing end. The SSW gun must be on the stub's other side from the FOB;
  - the N gun nearest where the N road leaves the town's rise, at (13776, 11376).

## Seats

| Member | Comp (size) | Seat | Yaw | Pad level | Ground under it | Change | From road edge | From town point |
|---|---|---|---|---|---|---|---|---|
| FOB | Small Rectangle FOB with GPs (90 × 58 m) | (13570, 11055) | 30° | +0.64 m | +0.37 to +0.91 m | 0.27 m | 5.7 m (SSW stub) | 148 m |
| SSW gun | Heavy Gun Position + AA (UD) (60 × 82 m) | (13500, 11130) | 45° | +0.78 m | +0.65 to +0.90 m | 0.12 m | 3.1 m (SSW stub) | 122 m |
| N gun | Heavy Gun Position + AA (UD) (60 × 82 m) | (13726, 11266) | 135° | +0.67 m | +0.41 to +0.94 m | 0.27 m | 3.9 m (6-M4 → 6-11) | 142 m |

## Gun facing

| Gun | Bearing | Why | 300 m clear | Highest ground within 150 m, against the muzzle |
|---|---|---|---|---|
| SSW gun | 214° | The T2 stub's line, toward 6-M3 Tank Laager (JOB_5 decision 28) | Yes | 1.89 m below |
| N gun | 0° | The designed N approach, past 6-06 (JOB_5 decision 28) | Yes | 1.90 m below |
| N gun, other bearing | 45° | Along the planned N road (T1), which leaves the town to the NE | Yes | 1.90 m below |

The N gun passes on either bearing.

## Reading (AI)

- **Area:** the three pads cover about 1.5 ha, about 11 % of the town's 13.2 ha rise. Room for about 80 buildings remains to be checked when the houses are laid out (NOT MEASURED).
- **The N gun is inside the town:** it is 121 m short of where the N road leaves the rise. Nearer the edge, the rise is too narrow to keep a pad 10 m clear of the water.
- **Firing lines:** on 0°, the N gun's line crosses the north part of the town, which reaches about 260 m beyond the gun. On 45° it runs along the road out of town. No houses are placed yet, so whether houses block either line is NOT MEASURED.
- **The FOB:** it is about 80 m from the K1 landing top, on the south edge, facing 6-M3 across the water, as call 27 asks.

## Decisions (Kernel)

| # | Finding | Answer | source |
|---|---|---|---|
| G1 | The N gun passes facing on both 0° (designed N approach) and 45° (along the N road); on 0° its line crosses the town's north part | b 45°, along the planned N road (T1) as it leaves the town to the NE, toward 6-11 | HUMAN |

The seats of the FOB, the SSW gun and the N gun stand as in the tables above. The bearings are SSW gun 214° and N gun 45°.
