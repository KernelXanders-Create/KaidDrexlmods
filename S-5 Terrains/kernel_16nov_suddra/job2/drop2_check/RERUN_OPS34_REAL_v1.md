# Ops 3-4 planner re-run on the drop 2 ground — v1

Run on 2026-11-25. The inputs were:
- drop 2 heights resampled to 5 m;
- the ground requests filled as ASSUMED levels (see `rerun_ops34_v1/ground_requests_applied.json`);
- Kernel's moves from `GROUND_CHECK_OPS34_v1.md` rows 1-15;
- roads on dry ground only (row 16), searched over the whole map with a 6,000 m margin.

Tools: `tools_sketch/op3r.py` and `op4r.py`. Outputs are in `rerun_ops34_v1/` (plan json, checks json, png, logs).
All numbers below are MEASURED from those outputs unless marked otherwise.

## Op 3 (54 min run)

| Check | Result |
|---|---|
| Pads not found (144 m search) | 3-03 (197 × 193 m), 3-04.2, 3-10.2, 3-10.3 |
| Sites not on the road net | 3-04, 3-10 (no dry route); 3-M2 (trunk leg from 1-F: no route) |
| Trunk 1-F → 3-M1 | 17,840 m long (straight line 5.5 km). It runs far south (y ≈ 1,040-1,100 at x 10,500-15,000) |
| Grade | **FAIL**: the trunk has one step of 16.7 % at (13824, 5436), 17.4 km along, near the 3-M1 end. Every other road is ≤ 12.8 % |
| Pad within 10 m of the +0.3 m line | **FAIL**: 3-M1.2 at 1.8 m |
| Astride seats | 3-M1.2 moved 427 m onto the trunk; 3-M2.3 moved 482 m onto 3-07 → 3-M2.4 |
| Total road | 34.2 km over 20 roads |
| Other checks | Pass (pad spacing, pad change ≤ 4 m, cut/fill ≤ 4 m, 150 m straights, 3 m road edge, final/mains 400 m) |

## Op 4 (96 min run)

| Check | Result |
|---|---|
| Pads not found (144 m search) | 4-F (55 × 60 m), 4-M1.5, 4-02.2, 4-07 (197 × 193 m) |
| South bank net | Two pieces: {4-04, 4-M4, 4-01, 4-04.2} and {4-M2}. Not reached: 4-M2.2, 4-05 |
| North bank net | One piece: {4-M3 ×4, 4-02, 4-06 ×2, 4-10, 4-11 ×2, 4-M2.3}. Not reached: 4-M1, 4-M1.3, 4-09, 4-03 ×3, 4-08 |
| Crossings (dam, causeways, rail bridge S) | No dry route to either bank's net, except rail bridge N |
| No seat | 4-M1.2, 4-M1.4 (their roads were never built) |
| Long roads | 4-M4 → 4-04: 14,337 m (straight 1.7 km). 4-10 → 4-M3.3: 7,556 m |
| Astride seats | 4-M2 moved **857 m** to the north bank's rail bridge road, off its south-bank design point. 4-M2.3 moved 62 m; 4-06 moved 11 m |
| Pad within 10 m of the +0.3 m line | **FAIL**: 4-06 at 1.4 m, 4-M2 at 4.2 m, 4-M2.3 at 5.7 m |
| Grade | Pass (worst 12.8 %) |
| Total road | 33.3 km over 12 roads |

## Reading

Dry-only routing finds routes only by going far around the wet ground: the op 3 trunk is about 3.2 × the straight line, and 4-M4 → 4-04 about 8.4 ×. In op 4 it still leaves 7 north-bank sites, 2 south-bank sites and every crossing off the net.

Before the next run, Kernel decides the questions below, one at a time.

## Decisions (Kernel)

| # | Question | Answer | source |
|---|---|---|---|
