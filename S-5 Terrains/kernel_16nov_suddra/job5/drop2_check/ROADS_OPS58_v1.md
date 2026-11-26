# Roads check: ops 5-8 sketch links on the drop 2 ground — v1

Run on 2026-11-26 with `roads58.py`. It checks the 69 links in `ops5_8_sketch.json`, which are AI links drawn on the K3 points before drop 2.

## Method

- **Ground:** the drop 2 heights resampled to 5 m, with the ops 3-4 fills (pack v5). It is checked on a 10 m lattice.
- **Water rule:** the same as the ops 3-4 router. Ground at or below +0.3 m counts as water, and a road keeps 10 m clear of it.
- **Grade:** no step steeper than 14 % over 10 m.
- **Endpoints:** a link end is snapped to free ground within 100 m.
- **Moves applied:** 5-05 at (5729, 10092) and 8-12 at (8400, 15500).
- **Op starts:** taken from the sketch.
- **Dry only:** this assumes the roads rule from ground check ops 3-4, finding 16 (dry ground only) also holds for ops 5-8. Kernel has not said yet.

## Dry islands (MEASURED)

One dry island of 97.4 km² holds most sites in every op. Every smaller piece below is ringed by water (checked with the water rule alone), not cut off by slope.

| Op | Island km² | Sites |
|---|---|---|
| 5 | main 97.4 | START, 5-F, 5-M1, 5-M2, 5-M3, 5-01, 5-02, 5-03, 5-06, 5-07, 5-08, 5-10, 5-11 |
| 5 | 0.1 | 5-M4, 5-05 |
| 5 | 0.1 | 5-04 |
| 5 | 0.7 | 5-09 |
| 5 | 3.1 | 5-12 |
| 5 | in water | 5-13 |
| 6 | main 97.4 | 6-M1, 6-M2, 6-M4, 6-01, 6-02, 6-03, 6-04, 6-05, 6-06, 6-08, 6-09, 6-10, 6-11 |
| 6 | 0.0 | START |
| 6 | in water | 6-F |
| 6 | 0.1 | 6-M3 |
| 6 | 0.0 | 6-07 |
| 6 | 0.0 | 6-12 |
| 7 | main 97.4 | START, 7-M1, 7-M2, 7-M3, 7-M4, 7-02, 7-03, 7-04, 7-05, 7-08, 7-09, 7-10, 7-11, 7-12 |
| 7 | 0.1 | 7-F |
| 7 | 0.0 | 7-01 |
| 7 | 0.0 | 7-06 |
| 7 | in water | 7-07 |
| 8 | main 97.4 | 8-F, 8-M1, 8-M2, 8-M3, 8-M4, 8-01, 8-02, 8-03, 8-04, 8-05, 8-06, 8-08, 8-09, 8-10, 8-11, 8-12 |
| 8 | 0.1 | START |
| 8 | 0.1 | 8-07 |

## Sketch links

| Op | Link | Straight m | Result | Dry m | × straight |
|---|---|---|---|---|---|
| 5 | START – 5-05 | 2352 | NO DRY PATH (within 80 km) |  |  |
| 5 | 5-05 – 5-M4 | 129 | dry path | 143 | 1.11 |
| 5 | 5-M4 – 5-03 | 1442 | NO DRY PATH (within 80 km) |  |  |
| 5 | 5-03 – 5-10 | 1414 | dry path | 1607 | 1.14 |
| 5 | 5-10 – 5-04 | 1844 | NO DRY PATH (within 80 km) |  |  |
| 5 | 5-04 – 5-08 | 1442 | NO DRY PATH (within 80 km) |  |  |
| 5 | 5-08 – 5-M2 | 1281 | dry path | 1689 | 1.32 |
| 5 | 5-08 – 5-11 | 1456 | dry path | 4465 | 3.07 |
| 5 | 5-M2 – 5-F | 1649 | dry path | 12488 | 7.57 |
| 5 | 5-F – 5-01 | 1414 | dry path | 2540 | 1.8 |
| 5 | 5-01 – 5-13 | 1077 | end not on free ground within 100 m |  |  |
| 5 | 5-13 – 5-09 | 1000 | end not on free ground within 100 m |  |  |
| 5 | 5-09 – 5-M1 | 1414 | NO DRY PATH (within 80 km) |  |  |
| 5 | 5-01 – 5-12 | 1720 | NO DRY PATH (within 80 km) |  |  |
| 5 | 5-12 – 5-02 | 1281 | NO DRY PATH (within 80 km) |  |  |
| 5 | 5-02 – 5-M3 | 1456 | dry path | 1885 | 1.29 |
| 5 | 5-M3 – 5-06 | 1562 | dry path | 1802 | 1.15 |
| 5 | 5-M3 – 5-07 | 1612 | dry path | 1929 | 1.2 |
| 6 | START – 6-12 | 2683 | NO DRY PATH (within 80 km) |  |  |
| 6 | 6-12 – 6-01 | 800 | NO DRY PATH (within 80 km) |  |  |
| 6 | 6-01 – 6-F | 849 | end not on free ground within 100 m |  |  |
| 6 | 6-F – 6-M1 | 849 | end not on free ground within 100 m |  |  |
| 6 | 6-F – 6-M2 | 849 | end not on free ground within 100 m |  |  |
| 6 | 6-M2 – 6-02 | 843 | dry path | 6282 | 7.45 |
| 6 | 6-M2 – 6-09 | 966 | dry path | 1894 | 1.96 |
| 6 | 6-09 – 6-05 | 1000 | dry path | 3336 | 3.34 |
| 6 | 6-05 – 6-03 | 632 | dry path | 9660 | 15.28 |
| 6 | 6-01 – 6-M3 | 1265 | NO DRY PATH (within 80 km) |  |  |
| 6 | 6-02 – 6-M4 | 1342 | dry path | 4808 | 3.58 |
| 6 | 6-M4 – 6-06 | 1200 | dry path | 1388 | 1.16 |
| 6 | 6-06 – 6-07 | 1414 | NO DRY PATH (within 80 km) |  |  |
| 6 | 6-07 – 6-08 | 1562 | NO DRY PATH (within 80 km) |  |  |
| 6 | 6-M4 – 6-11 | 1566 | dry path | 2005 | 1.28 |
| 6 | 6-M1 – 6-04 | 1612 | dry path | 2331 | 1.45 |
| 6 | 6-M3 – 6-10 | 1887 | NO DRY PATH (within 80 km) |  |  |
| 7 | START – 7-02 | 1942 | dry path | 2117 | 1.09 |
| 7 | 7-02 – 7-12 | 608 | dry path | 9549 | 15.71 |
| 7 | 7-02 – 7-07 | 671 | end not on free ground within 100 m |  |  |
| 7 | 7-07 – 7-F | 600 | end not on free ground within 100 m |  |  |
| 7 | 7-F – 7-M2 | 1000 | NO DRY PATH (within 80 km) |  |  |
| 7 | 7-12 – 7-09 | 1000 | dry path | 1090 | 1.09 |
| 7 | 7-12 – 7-01 | 1020 | NO DRY PATH (within 80 km) |  |  |
| 7 | 7-01 – 7-M1 | 1114 | NO DRY PATH (within 80 km) |  |  |
| 7 | 7-M2 – 7-M4 | 1131 | dry path | 3589 | 3.17 |
| 7 | 7-M2 – 7-04 | 1170 | dry path | 1414 | 1.21 |
| 7 | 7-09 – 7-03 | 1217 | dry path | 3585 | 2.95 |
| 7 | 7-07 – 7-10 | 1456 | end not on free ground within 100 m |  |  |
| 7 | 7-10 – 7-05 | 1281 | dry path | 1979 | 1.54 |
| 7 | 7-M1 – 7-06 | 1711 | NO DRY PATH (within 80 km) |  |  |
| 7 | 7-06 – 7-08 | 1265 | NO DRY PATH (within 80 km) |  |  |
| 7 | 7-08 – 7-M3 | 1000 | dry path | 1951 | 1.95 |
| 7 | 7-M4 – 7-11 | 1789 | dry path | 1931 | 1.08 |
| 8 | START – 8-10 | 943 | NO DRY PATH (within 80 km) |  |  |
| 8 | 8-10 – 8-08 | 500 | dry path | 487 | 0.97 |
| 8 | 8-10 – 8-12 | 2280 | dry path | 3098 | 1.36 |
| 8 | 8-08 – 8-07 | 900 | NO DRY PATH (within 80 km) |  |  |
| 8 | 8-07 – 8-M1 | 985 | NO DRY PATH (within 80 km) |  |  |
| 8 | 8-M1 – 8-11 | 600 | dry path | 895 | 1.49 |
| 8 | 8-M1 – 8-F | 721 | dry path | 766 | 1.06 |
| 8 | 8-F – 8-09 | 721 | dry path | 766 | 1.06 |
| 8 | 8-12 – 8-M2 | 2010 | dry path | 2083 | 1.04 |
| 8 | 8-M2 – 8-M4 | 894 | dry path | 966 | 1.08 |
| 8 | 8-11 – 8-03 | 1118 | dry path | 1183 | 1.06 |
| 8 | 8-03 – 8-M3 | 854 | dry path | 924 | 1.08 |
| 8 | 8-M3 – 8-01 | 894 | dry path | 966 | 1.08 |
| 8 | 8-01 – 8-05 | 849 | dry path | 925 | 1.09 |
| 8 | 8-M2 – 8-06 | 1265 | dry path | 1366 | 1.08 |
| 8 | 8-06 – 8-02 | 500 | dry path | 729 | 1.46 |
| 8 | 8-02 – 8-04 | 1077 | dry path | 1233 | 1.14 |

Note: the links were drawn as minimum-spanning links on the K3 points. Several now join the main island to a small one, so they fail even where another main-island link would work.

## Decisions (Kernel)

| # | Finding | Answer | source |
|---|---|---|---|
| R1 | Do roads stay on dry ground only for ops 5-6? | b Dry only, plus a fill causeway (ground request) to each small island that needs a vehicle road | HUMAN |
| R2 | Which small islands get a fill causeway | Causeways for 5-09 (22 m), 6-07 (22 m), 6-12 (20 m), 5-12 (50 m). Not chosen: 5-M4 + 5-05, 5-04, the op 6 start, 6-M3 (foot / boat / air links under dry-only) | HUMAN |
| R3 | Op 6 start (10400, 7200) on a 0.02 km² island with no road | b Keep it: op 6 starts by boat or air | HUMAN |
| R4 | How to set the ops 5-6 road net | a Redraw as the shortest dry net on the drop 2 ground (with the 4 causeways), bring back long links | HUMAN |
| R5 | 5-12 via its 50 m causeway gives a 47.6 km road (5.7 km straight to 5-11) | a Keep the 50 m causeway and the 47.6 km road | HUMAN |
| R6 | Op 6 long links 6-09–6-03 (4.3×), 6-09–6-02 (2.9×), 6-06–6-02 (2.7×) | a Accept the detours as measured | HUMAN |

## Redrawn ops 5-6 net (R4, MEASURED; `net56.py`, output in `net56_v1.json`)

The net is a minimum spanning tree over the shortest dry paths between each op's sites, with Kernel's 4 causeways (R2) opened as 7 m fill strips. The causeway fill level is ASSUMED. Each path is in `net56_v1.json`, sampled every 50 m.

### Op 5: 15 on the net, 76.0 km

Off the net (foot / boat / air under R1-R3): 5-M4, 5-04, 5-05, 5-13

| Link | Dry m | Straight m | × |
|---|---|---|---|
| 5-11 – 5-12 | 47575 | 5657 | 8.41 |
| 5-M1 – START | 3179 | 2408 | 1.32 |
| 5-M2 – 5-08 | 1689 | 1281 | 1.32 |
| 5-02 – 5-M3 | 1885 | 1456 | 1.29 |
| 5-06 – 5-M3 | 1802 | 1562 | 1.15 |
| 5-03 – 5-10 | 1607 | 1414 | 1.14 |
| 5-10 – 5-08 | 3077 | 2720 | 1.13 |
| 5-M1 – 5-09 | 1546 | 1414 | 1.09 |
| 5-10 – 5-11 | 3381 | 3111 | 1.09 |
| 5-M1 – 5-01 | 1649 | 1523 | 1.08 |
| 5-M3 – 5-F | 2897 | 2683 | 1.08 |
| 5-M1 – 5-F | 1766 | 1649 | 1.07 |
| 5-06 – 5-07 | 1883 | 1811 | 1.04 |
| 5-07 – 5-11 | 2083 | 2010 | 1.04 |

Causeways (ground requests, R2): 5-09 22 m from (3020, 9120) to (3040, 9130), lowest ground +0.76; 5-12 50 m from (400, 9360) to (400, 9310), lowest ground +0.52

### Op 6: 15 on the net, 35.0 km

Off the net (foot / boat / air under R1-R3): 6-M3, 6-F; the op 6 start (boat / air, R3)

| Link | Dry m | Straight m | × |
|---|---|---|---|
| 6-09 – 6-03 | 6324 | 1456 | 4.34 |
| 6-09 – 6-02 | 4389 | 1523 | 2.88 |
| 6-06 – 6-02 | 3554 | 1342 | 2.65 |
| 6-09 – 6-M2 | 1894 | 966 | 1.96 |
| 6-04 – 6-M1 | 2331 | 1612 | 1.45 |
| 6-08 – 6-07 | 2150 | 1562 | 1.38 |
| 6-M4 – 6-07 | 3105 | 2417 | 1.28 |
| 6-11 – 6-M4 | 2005 | 1566 | 1.28 |
| 6-M1 – 6-05 | 1659 | 1414 | 1.17 |
| 6-M4 – 6-06 | 1388 | 1200 | 1.16 |
| 6-10 – 6-11 | 2893 | 2646 | 1.09 |
| 6-01 – 6-12 | 866 | 800 | 1.08 |
| 6-M2 – 6-01 | 1257 | 1224 | 1.03 |
| 6-01 – 6-M1 | 1225 | 1200 | 1.02 |

Causeways (ground requests, R2): 6-07 22 m from (14450, 13430) to (14430, 13440), lowest ground +0.64; 6-12 20 m from (11620, 9720) to (11620, 9740), lowest ground +0.68

The 5-12 causeway lands on a far lobe of the main island, so its road runs 47.6 km. Kernel kept it (R5). `cw512.py` measured two shorter routes in: an 819 m causeway toward 5-F and a 1,251 m causeway toward 5-01.

## Ops 7-8 (Comedian's)

The island table above lists them. 7-F Kesh Junction, which is also the op 8 start, sits on a 0.11 km² island. 7-01, 7-06 and 8-07 are on small islands, and 7-07 is in water. Passed to Comedian with the ground check findings.

## Not done

- Real road lines through the planner (grade per 10 / 20 m, cut / fill, approaches) for ops 5-6. This check only measures paths on a 10 m lattice.
