# Ground check: ops 5-8 sketch points on the drop 2 ground — v1

Run on 2026-11-26. It checks the 69 sites of `job5/ops5_8_sketch.json` against `drop2/suddra_height_cm.npz` and `suddra_masks.npz`.

## Method

- **Good ground** means AI-dry, not water, and at or above +0.5 m (the same rule as the ops 3-4 check).
- **Main comp footprint:** the first comp of each site, at the site point, with yaw 0. Its size comes from the size table: KNOWN where it was built on Thirra, otherwise ASSUMED. There are no designed pads yet, so the layout and yaw are ASSUMED.
- **Site disc:** a circle around the point holding all the site's comps (their area × 1.5, at least 60 m radius). It reads how much good ground surrounds the site.
- **Moves applied first:**
  - 5-05 to (5400, 9700) (call 5A, HUMAN);
  - 8-12 to (8400, 15500) (SUD-R34 option (c), owner).
- **Not yet applied:** the call 26 B moves of 8-04, 8-07, 8-08 and 8-10 out of op 7's ground. No spots exist for them yet, so they are checked at their job 5 points.
- **Ownership:** ops 7-8 and the Citadel are Comedian's (pack 5). Their findings are listed for both sketches to agree.
- **Pad change:** a ground range of 8 m or less can be levelled to the middle within the 4 m pad-change rule.

Scripts: `pads58.py` (every site) and `spot58.py` (nearest good spots for one footprint). All numbers are MEASURED on the drop 2 grid unless marked otherwise.

## All sites

| Site | Main comp | Size m (source) | Main: good % / water % / ground m | Site disc r m: good % / water % |
|---|---|---|---|---|
| 5-F | CIS Mini Fortress with GPs | 154 x 145 (KNOWN) | 100 / 0 / +0.90..+8.38 | 181: 98 / 2 |
| 5-M1 | CIS Small Checkpoint with GPs | 57 x 69 (KNOWN) | 100 / 0 / +0.81..+0.81 | 90: 100 / 0 |
| 5-M2 | Royal Tunnel Holdout 1 (Mono) | NOT MEASURED | NOT MEASURED (no size) | 126: 88 / 9 |
| 5-M3 | [Burnzy] CIS Arti-base + Flower Tower 2 | 140 x 120 (ASSUMED) | 100 / 0 / +0.97..+7.60 | 110: 100 / 0 |
| 5-M4 | CIS Outpost with GPs (D) | NOT MEASURED | NOT MEASURED (no size) | 60: 100 / 0 |
| 5-01 | Tukata Turret Bunker | 30 x 30 (ASSUMED) | 100 / 0 / +0.93..+0.93 | 60: 100 / 0 |
| 5-02 | CIS Medium AA Base with GPs | 197 x 193 (KNOWN) | 95 / 4 / -0.85..+1.24 | 165: 58 / 38 |
| 5-03 | Small Wall with Bunker | 40 x 24 (ASSUMED) | 100 / 0 / +0.90..+0.90 | 60: 100 / 0 |
| 5-04 | CIS Vehicle Depot with GPs (D) | 120 x 120 (ASSUMED) | 100 / 0 / +0.94..+1.12 | 102: 99 / 0 |
| 5-05 (moved) | CIS Basic Trenchline with GPs | 114 x 60 (KNOWN) | 0 / 0 / +0.21..+0.37 | 117: 2 / 1 |
| 5-06 | CIS Comms Array with GPs | 40 x 93 (KNOWN) | 100 / 0 / +1.09..+3.08 | 60: 100 / 0 |
| 5-07 | CIS Guard Tower with GPs | NOT MEASURED | NOT MEASURED (no size) | 60: 100 / 0 |
| 5-08 | CIS Small Checkpoint with GPs | 57 x 69 (KNOWN) | 100 / 0 / +0.89..+0.90 | 79: 97 / 0 |
| 5-09 | CIS Fuel Depot with GPs | 87 x 65 (KNOWN) | 100 / 0 / +1.00..+1.00 | 64: 100 / 0 |
| 5-10 | Zavala CIS Outpost with GPs | 60 x 60 (ASSUMED) | 100 / 0 / +0.96..+0.96 | 60: 100 / 0 |
| 5-11 | CIS Outpost with GPs (D) | NOT MEASURED | NOT MEASURED (no size) | 60: 100 / 0 |
| 5-12 | Claus - Small Radar | 30 x 30 (ASSUMED) | 100 / 0 / +3.36..+3.96 | 60: 100 / 0 |
| 6-F | NEW build 1 (centerpiece) | NOT MEASURED | NOT MEASURED (no size) | 60: 0 / 100 |
| 6-M1 | CIS Metal Trench Line with GPs | 43 x 150 (KNOWN) | 100 / 0 / +0.85..+0.85 | 84: 100 / 0 |
| 6-M2 | [Burnzy] CIS Arti-base + Flower Tower 2 | 140 x 120 (ASSUMED) | 100 / 0 / +0.81..+1.00 | 120: 95 / 0 |
| 6-M3 | CIS Vehicle Depot with GPs (D) | 120 x 120 (ASSUMED) | 100 / 0 / +0.81..+0.89 | 113: 99 / 0 |
| 6-M4 | hand-made town (town work, not a comp) | NOT MEASURED | NOT MEASURED (no size) | 60: 100 / 0 |
| 6-01 | Royal Tunnel Holdout 1 (Mono) | NOT MEASURED | NOT MEASURED (no size) | 60: 100 / 0 |
| 6-02 | Zavala CIS Outpost with GPs | 60 x 60 (ASSUMED) | 100 / 0 / +1.06..+1.06 | 60: 100 / 0 |
| 6-03 | CIS Powerbank Facility with GPs | 192 x 166 (KNOWN) | 69 / 11 / -1.68..+0.97 | 151: 40 / 42 |
| 6-04 | CIS Fuel Depot with GPs | 87 x 65 (KNOWN) | 100 / 0 / +5.87..+11.38 | 64: 100 / 0 |
| 6-05 | CIS Medium AA Base with GPs | 197 x 193 (KNOWN) | 99 / 0 / +0.37..+7.56 | 165: 80 / 1 |
| 6-06 | CIS Mini Fortress with GPs | 154 x 145 (KNOWN) | 97 / 1 / -1.63..+1.39 | 126: 77 / 11 |
| 6-07 | CIS Guard Tower with GPs | NOT MEASURED | NOT MEASURED (no size) | 60: 100 / 0 |
| 6-08 | CIS Depot (Fixed) with GPs (D) | 134 x 248 (KNOWN) | 100 / 0 / +0.66..+5.53 | 154: 100 / 0 |
| 6-09 | Destructable Shield Generator and its shield template | NOT MEASURED | NOT MEASURED (no size) | 60: 100 / 0 |
| 6-10 | Small Wall with Bunker | 40 x 24 (ASSUMED) | 100 / 0 / +1.04..+1.04 | 60: 100 / 0 |
| 6-11 | CIS Comms Array with GPs | 40 x 93 (KNOWN) | 100 / 0 / +0.78..+0.81 | 60: 100 / 0 |
| 6-12 | CIS Fuel Depot with GPs | 87 x 65 (KNOWN) | 100 / 0 / +0.91..+0.93 | 64: 100 / 0 |
| 7-F | hand-made town (town work, not a comp) | NOT MEASURED | NOT MEASURED (no size) | 60: 100 / 0 |
| 7-M1 | CIS Metal Trench Line with GPs | 43 x 150 (KNOWN) | 100 / 0 / +0.84..+0.84 | 84: 100 / 0 |
| 7-M2 | CIS Medium Logistics Base with GPs | 120 x 100 (ASSUMED) | 100 / 0 / +0.99..+1.10 | 140: 82 / 2 |
| 7-M3 | [Burnzy] CIS Arti-base + Flower Tower 2 | 140 x 120 (ASSUMED) | 100 / 0 / +0.67..+0.97 | 120: 97 / 1 |
| 7-M4 | CIS Double Pcannon Checkpoint with GPs | 71 x 51 (KNOWN) | 100 / 0 / +1.09..+1.82 | 88: 100 / 0 |
| 7-01 | Tukata Turret Bunker | 30 x 30 (ASSUMED) | 100 / 0 / +0.87..+0.87 | 60: 100 / 0 |
| 7-02 | Small Wall with Bunker | 40 x 24 (ASSUMED) | 0 / 23 / -0.22..+0.16 | 60: 0 / 48 |
| 7-03 | CIS Heavy AD Tower with GPs | NOT MEASURED | NOT MEASURED (no size) | 60: 100 / 0 |
| 7-04 | CIS Depot (Fixed) with GPs (D) | 134 x 248 (KNOWN) | 100 / 0 / +5.94..+14.97 | 154: 100 / 0 |
| 7-05 | CIS Medium Logistics Base with GPs | 120 x 100 (ASSUMED) | 100 / 0 / +0.89..+11.13 | 93: 100 / 0 |
| 7-06 | Small Wall with Bunker | 40 x 24 (ASSUMED) | 100 / 0 / +0.86..+0.86 | 60: 100 / 0 |
| 7-07 | CIS Fuel Depot with GPs | 87 x 65 (KNOWN) | 0 / 100 / -2.13..-1.18 | 64: 0 / 98 |
| 7-08 | Zavala CIS Outpost with GPs | 60 x 60 (ASSUMED) | 100 / 0 / +0.90..+0.90 | 60: 100 / 0 |
| 7-09 | CIS Guard Tower with GPs | NOT MEASURED | NOT MEASURED (no size) | 60: 100 / 0 |
| 7-10 | CIS Comms Array with GPs | 40 x 93 (KNOWN) | 100 / 0 / +1.10..+1.10 | 60: 100 / 0 |
| 7-11 | Claus - Small Radar | 30 x 30 (ASSUMED) | 100 / 0 / +1.04..+4.06 | 60: 100 / 0 |
| 7-12 | CIS Depot (Fixed) with GPs (D) | 134 x 248 (KNOWN) | 76 / 12 / -2.05..+1.03 | 154: 59 / 19 |
| 8-F | NEW build 2 (centerpiece) | NOT MEASURED | NOT MEASURED (no size) | 60: 100 / 0 |
| 8-M1 | CIS Double Pcannon Checkpoint with GPs | 71 x 51 (KNOWN) | 100 / 0 / +0.95..+0.95 | 88: 100 / 0 |
| 8-M2 | CIS Elevated Landing Pad Construction with GPs | 121 x 79 (KNOWN) | 100 / 0 / +19.59..+20.63 | 185: 100 / 0 |
| 8-M3 | [Burnzy] CIS Arti-base + Flower Tower 2 | 140 x 120 (ASSUMED) | 100 / 0 / +20.83..+25.82 | 120: 100 / 0 |
| 8-M4 | CIS Large Power Facility with GPs | 192 x 166 (ASSUMED) | 100 / 0 / +11.39..+29.30 | 151: 100 / 0 |
| 8-01 | Tukata Turret Bunker | 30 x 30 (ASSUMED) | 100 / 0 / +13.61..+15.24 | 60: 100 / 0 |
| 8-02 | CIS Medium Logistics Base with GPs | 120 x 100 (ASSUMED) | 100 / 0 / +0.97..+0.99 | 93: 100 / 0 |
| 8-03 | CIS Comms Array with GPs | 40 x 93 (KNOWN) | 100 / 0 / +29.45..+30.36 | 60: 100 / 0 |
| 8-04 | CIS Fuel Depot with GPs | 87 x 65 (KNOWN) | 100 / 0 / +12.79..+16.97 | 64: 100 / 0 |
| 8-05 | CIS Guard Tower with GPs | NOT MEASURED | NOT MEASURED (no size) | 60: 100 / 0 |
| 8-06 | CIS Medium AA Base with GPs | 197 x 193 (KNOWN) | 100 / 0 / -0.51..+3.29 | 165: 85 / 13 |
| 8-07 | CIS Basic Trenchline with GPs | 114 x 60 (KNOWN) | 86 / 0 / +0.20..+2.02 | 117: 36 / 19 |
| 8-08 | CIS Basic Trenchline with GPs | 114 x 60 (KNOWN) | 0 / 38 / -0.43..+0.41 | 117: 0 / 41 |
| 8-09 | Destructable Shield Generator and its shield template | NOT MEASURED | NOT MEASURED (no size) | 60: 100 / 0 |
| 8-10 | Giant Radar Dish | 80 x 80 (ASSUMED) | 68 / 0 / +0.40..+6.40 | 68: 62 / 0 |
| 8-11 | CIS Medium Logistics Base with GPs | 120 x 100 (ASSUMED) | 100 / 0 / +4.48..+8.20 | 93: 100 / 0 |
| 8-12 (moved) | CIS Elevated Landing Pad Construction with GPs | 121 x 79 (KNOWN) | 100 / 0 / +23.96..+27.11 | 83: 100 / 0 |
| 5-13 | hand-made town (town work, not a comp) | NOT MEASURED | NOT MEASURED (no size) | 60: 0 / 40 |

## Findings

### Ops 5-6

| # | Site | Finding (MEASURED) | Nearest good spots for the main footprint |
|---|---|---|---|
| 1 | 5-05 Kettle North Trench (moved, call 5A) | At (5400, 9700) the trench (114 × 60 m) is 0 % good: ground +0.21..+0.37 m, below +0.5 but not water | (5400, 9420), 280 m S, ground +0.58..+0.97 (this is about the K3 point before the move); (5729, 10092), 512 m NE; (4376, 9700), 1,024 m W |
| 2 | 6-03 Pipeline Pump | The Powerbank Facility (192 × 166 m) is 69 % good with 11 % water; ground −1.68..+0.97 m | (10104, 11817), 536 m ESE, ground +0.59..+7.26; (10567, 13152), 1,504 m NE; (8399, 10992), 1,568 m SW |
| 3 | 6-F Cauldron Refinery (final) | The point is 100 % water, ground −1.64..−1.42 m. The stake is "the gas refinery on stilts in the flooded crater". NEW build, no size | Dry crater rim at about 520 m: (11512, 11090) E, (11000, 10480) S, (10504, 11181) W, ground +5..+13 |
| 4 | 5-13 Stake Hamlet | 0 % good, 43 % water, ground −0.95..+0.30 m. The stake is "pile-house hamlet". Town work, no size | (1975, 8553), 584 m SE; (1854, 9699), 744 m NNE; (710, 8843), 904 m W |
| 5 | Sloped pads | Within 8 m, so they can be levelled in place: 5-F 7.5 m range, 6-05 7.2 m, 5-M3 6.6 m, 6-04 5.5 m, 6-08 4.9 m | — |
| 6 | Wet ground round the site | The main footprint is good but the site disc is wet: 5-02 (58 % good, 38 % water), 6-06 (77 % / 11 %), 5-M2 (88 % / 9 %, no size). Other members may not fit beside the main | — |

### Ops 7-8 (Comedian's)

| # | Site | Finding (MEASURED) |
|---|---|---|
| 7 | 7-02 Wrecked Walker Strongpoint | 0 % good, 23 % water. Good spots at (10095, 12317), 96 m E, and (10080, 12161), 160 m SSE |
| 8 | 7-07 Fuel Siding | 100 % water. Good spot at (10784, 12446), 240 m SE |
| 9 | 7-12 Junction Field Hospital | Depot (134 × 248 m) is 76 % good, 12 % water |
| 10 | 7-04, 7-05, 8-M4 | Slope over 8 m: 7-04 9.0 m, 7-05 10.2 m, 8-M4 17.9 m |
| 11 | 8-07, 8-08, 8-10 | Wet or partly wet (86 %, 0 %, 68 % good). These sites move anyway under call 26 B |

## Decisions (Kernel)

| # | Finding | Answer | source |
|---|---|---|---|
