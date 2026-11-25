# The three Drain crossings (24 Nov 2026)

The centre lines are exactly as given in your part-1 return (metres, Arma frame). Everything under "measured" is MEASURED: samples every about 2 m along the given line; height bilinear on the 4 m grid; water = the `water` mask on the nearest cell; water width = length of the line where the mask is set. Full detail, including parallel lines 75 m and 150 m either side, is in `DRAIN_CROSSINGS.json`.

| Crossing | Centre line (from, to) | Length | Water on the line | Lowest ground on the line | Bank ground (40 m before / after the water) | Depth bands on the line |
|---|---|---|---|---|---|---|
| Plank Road | (7628, 6792) to (7681, 7326) | 536.6 m | **84.1 m**, one run, from 228.3 m along the line | -2.14 m | south mean +1.35 m (max +1.60); north mean +1.31 m (max +1.60) | 12.0 m deep (2), 72.1 m boat (3) |
| Rail Bridge | (8241, 6907) to (8213, 7450) | 543.7 m | **80.3 m**, one run, from 232.7 m along the line | -2.14 m | south mean +1.31 m (max +1.60); north mean +1.28 m (max +1.60) | 80.3 m boat (3) |
| Drain Locks | (10415, 6932) to (10350, 7474) | 545.9 m | **0 m: the line is dry** | +0.71 m (lowest) | the line runs on +0.71 to +0.82 m ground, with a crest of up to +1.31 m between 200 m and 350 m along it | none |

## Per crossing
- **Plank Road.** The water run is 84.1 m on the line (the line is about 5.7 degrees off the north, so a little wider than the 69 m Drain width the ground build marks across the stream). Highest ground inside the water is -0.13 m. The first dry sample on each bank is low (+0.17 m south, -0.03 m north) and the ground rises to about +1.3 m within 40 m. 82 % of the line is in the AI-dry mask; 438.5 m of it is in the net core.
- **Rail Bridge.** 80.3 m of water, all in the boat band; the first dry samples are +0.47 m (south) and +1.10 m (north), the banks +1.3 m on average. 85 % of the line is AI-dry; 437.4 m is net core. The rail embankment (+4.4 m, mask `rail`) runs close by; the line itself reaches only +1.6 m.
- **Drain Locks.** **On our ground the Drain is closed here.** The whole line is dry and 100 % AI-dry. Along an east-west row through the dam centre (y = 7205) the dry crest runs from x = 10360 to x = 10404 (**about 44 m wide**) at +1.28 to +1.31 m, with water on both sides at -2.15 m (west) and -2.06 m (east). The `designed_straights` layer marks the dam crest (value 3) on 136 m of the line. So your lock channel is a new water request, as the part-1 return said. Water lies 75 to 150 m west of the line along its length (a pool at about -2.7 m), and in patches east of it (see the JSON).

## Cautions
- The ground-build crossing marks (centres 7656.8 / 7061.0, 8228.7 / 7180.5, 10384.2 / 7204.7) are the AI crossing points of the build; they lie on or near your lines.
- Heights at the edge of a water run are at or just under 0 m because our shores shelve into the water; "bank" heights above are therefore given as means over 40 m, not only the first cell.
