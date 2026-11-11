# Grade: Kamar Village

town_grader 1.0 (11 Nov 2026). Layout `kamar_village_v2_layout`. Version string in the layout: K6 v2 (graded with the 11 Nov grader) PROPOSED.

**Seated as drawn: 42 of 42.** Refused: 0.

Refusal causes (our grading agent's categories): none.

Seated by role: landmark 1, quay 3, main 6, lane 32.

## Checks

| Check | Rule | Result | Status |
|---|---|---|---|
| buildings seated | every building must be seated as drawn | 42 of 42 | PASS |
| refusals by kind | first failed test per refused building | none | PASS |
| pad-pad clash | two pads at different levels may not share a grid point (all buildings, order-free) | 0 pairs of pad groups, 0 shared points | PASS |
| pad-street / ramp / lane clash | no pad point may sit on a street, lane, path or square point at another level (all buildings, order-free) | 0 buildings, 0 grid points | PASS |
| street-street clash | grid points two streets both claim at different levels; the earlier street keeps its level there, so the later one gets a step. A few at a junction where a ramp meets a level street are normal; dozens mean two streets run over each other at different levels (report) | {'C1': 18, 'C3': 9, 'C5': 14, 'C6': 10} | REPORT |
| square | one level; every point within 4.0 m of natural ground; no street point at another level; 31 deg bank to everything else | level 248.00 m, cut/fill max 1.66 m, 0 points meet streets at another level ; ok | PASS |
| pad cut / fill (true grid) | every pad point within 4.0 m of the natural ground; aim for 2.5 m (all buildings as drawn) | median 2.76 m, max 3.98 m, 26 over 2.5 m, 0 over 4.0 m  | PASS |
| ground solvable | 31 deg cones between all fixed points must meet (seated set) | 0 infeasible grid points | PASS |
| door threshold vs ground 1 m out | pad (= floor = threshold) within 5 cm of the graded surface 1 m out of the door (seated) | max 0.000 m; 0 fail  | PASS |
| door threshold vs street surface | pad within 5 cm of its street's level at the door's station, for doors within 12 m of the centre line (seated) | 41 checked, 0 fail ; 0 doors more than 12 m from their street (listed in result.json) | PASS |
| wall below ground | highest ground 0.25 m outside the walls minus the floor <= 0.3 m (seated) | max 0.01 m; 0 fail  | PASS |
| overlaps | no two footprint boxes overlap (whole layout as drawn) | 0 pairs ; closest gap 0.068 m | PASS |
| in a street ribbon (own street) | footprint >= half-width + 0.2 m from its own street's centre line (whole layout) | 0 buildings  | PASS |
| corner clearance (other streets) | footprint >= half-width + 1.0 m from every other street's centre line (whole layout) | 0 buildings  | PASS |
| back-to-back gap (31 deg bank) | pads at different levels need at least |dz| / 0.6 m between their grid points (first failure per building) | 0 buildings refused  | PASS |
| banks facing streets | a graded bank over 1.5 m seen from a main street or lane edge, before any building (seated set; report) | 25 runs, 198 stations (by street: {'C3': 1, 'C5': 1, 'C6': 1, 'E': 3, 'EE': 7, 'M': 1, 'NL': 2, 'QL': 3, 'WL': 6}) | REPORT |
| straight runs | no main street or lane straight for more than 80 m (within 1.0 m of its chord) | longest main street or lane: C6 57.4 m; roads and paths (report): none | PASS |
| street grades | main streets under 5 % (8 % average, 12 % on a short drop), lanes under 19 %, paths are stairs (report) | {'M': 12.0, 'E': 19.1, 'WL': 19.0, 'NL': 15.7, 'C1': 4.3, 'C3': 12.9, 'C5': 10.9, 'EE': 18.9, 'C6': 10.1, 'QL': 11.1} | REPORT |
| model / twin share (drawn) | any one model <= 15 %, any one twin group (colour variants of one house) <= 12 % | largest model ND03 5 = 11.9 %, largest twin group ND03 5 = 11.9 % | PASS |
| model / twin share (seated) | any one model <= 15 %, any one twin group (colour variants of one house) <= 12 % (the check is on the town as drawn; the seated share is a report) | largest model ND03 5 = 11.9 %, largest twin group ND03 5 = 11.9 % | REPORT |
| lamps | lamp positions, if given | none given (we place lamps ourselves) | n/a |
| comp seat and height | whole comps with a footprint, if given | none given with a footprint (roles only) | n/a |

## Buildings (in your file's order; grade_order = the order the grader seats them)

| id | model | street | role | pad z | seated | why |
|---|---|---|---|---|---|---|
| B001 | SF02 | SQ | landmark | 248.00 | yes | seated |
| B002 | WH03 | M | main | 253.00 | yes | seated |
| B003 | SF16 | M | main | 248.00 | yes | seated |
| B004 | SF08 | M | main | 248.00 | yes | seated |
| B005 | ND03 | M | main | 253.00 | yes | seated |
| B006 | WH24 | M | main | 253.00 | yes | seated |
| B007 | WH11 | M | main | 248.00 | yes | seated |
| B008 | WH24 | E | lane | 256.75 | yes | seated |
| B009 | WH19 | E | lane | 256.75 | yes | seated |
| B010 | WH24 | E | lane | 252.25 | yes | seated |
| B011 | WH19 | E | lane | 252.25 | yes | seated |
| B012 | WH01 | E | lane | 247.75 | yes | seated |
| B013 | WH11 | E | lane | 248.00 | yes | seated |
| B014 | WH23 | E | lane | 256.75 | yes | seated |
| B015 | WH17 | E | lane | 256.75 | yes | seated |
| B016 | WH08 | E | lane | 256.75 | yes | seated |
| B018 | WH03 | WL | lane | 259.50 | yes | seated |
| B019 | WH12 | WL | lane | 259.50 | yes | seated |
| B021 | WH06 | WL | lane | 257.00 | yes | seated |
| B022 | WH12 | WL | lane | 257.00 | yes | seated |
| B023 | WH14 | WL | lane | 257.00 | yes | seated |
| B024 | WH02 | WL | lane | 251.50 | yes | seated |
| B025 | WH17 | WL | lane | 251.50 | yes | seated |
| B026 | WH06 | WL | lane | 259.50 | yes | seated |
| B027 | ND01 | WL | lane | 259.50 | yes | seated |
| B028 | WH02 | WL | lane | 257.00 | yes | seated |
| B029 | ND03 | WL | lane | 257.00 | yes | seated |
| B030 | ND01 | WL | lane | 251.50 | yes | seated |
| B031 | ND03 | WL | lane | 251.50 | yes | seated |
| B032 | ND03 | WL | lane | 251.50 | yes | seated |
| B033 | WH17 | EE | lane | 242.25 | yes | seated |
| B034 | WH05 | EE | lane | 245.25 | yes | seated |
| B035 | ND03 | EE | lane | 245.25 | yes | seated |
| B036 | ND04 | EE | lane | 245.25 | yes | seated |
| B037 | WH01 | EE | lane | 245.25 | yes | seated |
| B038 | WH19 | NL | lane | 236.50 | yes | seated |
| B039 | WH17 | NL | lane | 236.50 | yes | seated |
| B040 | ND01 | NL | lane | 236.50 | yes | seated |
| B041 | ND01 | NL | lane | 239.00 | yes | seated |
| B042 | SF15 | QL | quay | 2.50 | yes | seated |
| B043 | WH03 | QL | quay | 2.50 | yes | seated |
| B044 | WH19 | QL | quay | 2.50 | yes | seated |

## Streets

| street | class | width | grid points fixed | points already held by an earlier street at another level | max grade % |
|---|---|---|---|---|---|
| M | main | 6.5 | 206 | 0 | 12.0 |
| E | lane | 5.0 | 158 | 0 | 19.1 |
| WL | lane | 5.0 | 134 | 0 | 19.0 |
| NL | lane | 5.0 | 107 | 0 | 15.7 |
| C1 | lane | 4.5 | 43 | 18 | 4.3 |
| C3 | lane | 4.5 | 28 | 9 | 12.9 |
| C5 | lane | 4.5 | 20 | 14 | 10.9 |
| EE | lane | 4.5 | 102 | 0 | 18.9 |
| C6 | lane | 4.5 | 38 | 10 | 10.1 |
| QL | lane | 5.0 | 87 | 0 | 11.1 |

Files: `plan.png` (every clashing cell drawn), `buildings.csv`, `result.json` (everything, with the grid points).
