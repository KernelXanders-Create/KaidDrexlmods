# 5-13 Stake Hamlet: where it stands, and seats for its guards — v1

Run on 2026-11-27, on ground pack v10, against the op 5 plan in `planner_ops56_v4/op5_main`. This follows call 28 (HUMAN):
- **A:** a dry rise like the Mound camp, with about 30 houses;
- **B:** a TKTA Checkpoint Fixed (Mono) astride the SE road in from 5-09, a CIS Small Checkpoint with GPs astride the NNE road in from 5-01, and a CIS Heavy Gun Position + AA (UD) between the two gates, facing the op 5 start.

Scripts: `hamlet513/rise513.py`, `point513.py` and `guards513.py`. Their outputs are the `_v1.json` files beside them. Numbers are MEASURED unless marked otherwise. "Dry" means ground at +0.5 m or higher (the village form rule); "wet" means +0.3 m or lower.

## The sketch point is in water

- 5-13's sketch point (1600, 9000) has ground at +0.16 m, and none of the ground within 100 m is dry.
- The ground check (ops 5-8, decision 4) had called it water by design, for pile houses. Call 28 A then chose a dry rise.
- The dry rises within 1.2 km are in `hamlet513/rise513_v1.json`. The nearest big ones:
  - 38.3 ha to the NNE, 237 m away;
  - 55.1 ha to the SE, 485 m away.
- The near end of the NNE rise is a narrow tongue: within 300 m of the old point, nowhere on it is more than 34 m from its edge.

## The new point (H2 a)

| Item | Value |
|---|---|
| Point | (1840, 9705), 745 m from the sketch point |
| Ground | +3.58 m, 85 m inside the dry edge |
| Dry ground within 150 m | 5.3 ha |
| Nearest op 5 site | 5-01 Gravel Pit Bunkers II, 336 m |
| Nearest op 5 road | 5-01 → 5-F.3, 345 m away, with 90 m of wet ground on the straight line. The hamlet stays off the net (H3 c) |

## Street stubs to the shore (H3 c)

| Stub | Bearing | Length | Shore end | Faces |
|---|---|---|---|---|
| NNE | 31° | 112 m | (1898, 9801), ground +0.55 m | The 5-01 → 5-F.3 road, 233 m on, across 90 m of wet ground |
| SE | 123° | 200 m | (2008, 9596), ground +0.61 m | The 5-09 → 5-M1 road, about 1,030 m on, across about 400 m of wet ground |

Each stub is 7 m wide (ASSUMED) and runs from the point until the ground first drops below +0.5 m.

## Seats

| Member | Comp (size) | Seat | Yaw | Pad level | Ground under it | Change | Note |
|---|---|---|---|---|---|---|---|
| NNE gate | CIS Small Checkpoint with GPs (57 × 69 m, KNOWN) | (1875, 9763) | 31° | +2.70 m | +1.39 to +4.02 m | 1.31 m | Astride the NNE stub, 68 m out |
| SE gate | TKTA Checkpoint Fixed (Mono) (40 × 60 m, ASSUMED as in the ops 5-8 layout) | (1911, 9659) | 123° | +2.60 m | +1.43 to +3.78 m | 1.17 m | Astride the SE stub, 85 m out |
| Gun | CIS Heavy Gun Position + AA (UD) (60 × 82 m, KNOWN) | (1945, 9715) | 120° | +2.97 m | +2.02 to +3.92 m | 0.95 m | Between the gates, 105 m from the point |

| Gun | Bearing | Why | 300 m clear | Highest ground within 150 m, against the muzzle |
|---|---|---|---|---|
| Gun | 120° | Toward the op 5 start, (5200, 7800) (call 28 B) | Yes | 1.50 m below |

**Rules used:** as for the 6-M4 guards (`TOWN_GUARDS_6M4_v1.md`):
- pad edge at least 10 m from the +0.3 m line;
- pad levelled to the middle of its ground, change no more than 4 m;
- pads at least 12 m apart;
- the gun at least 3 m from the stub edges;
- the muzzle at pad level + 2.0 m (ASSUMED).

**How seats were chosen:**
- **The gates:** each is centred on its stub, with its long side along the stub (ASSUMED), and set as far out as the rules allow.
- **The gun:** searched every 5 m and 15° between the two stubs, and kept nearest the midpoint between the gates.

## Reading (AI)

- **Gates set back:** both gates stand well inside the shore ends. A gate further out would have its pad within 10 m of the water.
- **Room:** the three pads take about 1.1 ha of the 5.3 ha of dry ground within 150 m of the point. That leaves about 4 ha for about 30 houses, roughly 1,400 m² each. Whether they fit is NOT MEASURED until the houses are laid out.
- **Next to 5-01:** the hamlet now sits 336 m from 5-01. The 400 m spacing rule binds only finals and mains, and 5-13 is a supporting site.
- **Ways in:** with no roads, the two ways in from 5-01 and 5-09 are foot or wade ways across 90 m and about 400 m of wet ground.

## Decisions (Kernel)

| # | Finding | Answer | source |
|---|---|---|---|
| H1 | Call 28 A asks for a dry rise, but 5-13's point is in water (+0.16 m; nothing dry within 100 m) | a The NNE rise, 237 m away (38.3 ha, +0.5 to +5.6 m) | HUMAN |
| H2 | The near end of that rise is a narrow tongue; two spots have room | a North, (1840, 9705): 85 m inside the edge, 5.3 ha dry within 150 m | HUMAN |
| H3 | The call 28 gate roads don't exist (5-13 is off the net); the shortest ways to op 5 roads cross 90 m (NNE) and 400 m (SE) of wet ground | c No roads: each gate stands astride a street stub that ends at the shore | HUMAN |
