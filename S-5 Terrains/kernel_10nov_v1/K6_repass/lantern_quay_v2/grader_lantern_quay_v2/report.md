# Grade: Lantern Quay Hamlet

town_grader 1.0 (11 Nov 2026). Layout `lantern_quay_v2_layout`. Version string in the layout: K6 v2 (graded with the 11 Nov grader) PROPOSED.

**Seated as drawn: 51 of 51.** Refused: 0.

Refusal causes (our grading agent's categories): none.

Seated by role: landmark 1, quay 8, main 11, lane 31.

## Checks

| Check | Rule | Result | Status |
|---|---|---|---|
| buildings seated | every building must be seated as drawn | 51 of 51 | PASS |
| refusals by kind | first failed test per refused building | none | PASS |
| pad-pad clash | two pads at different levels may not share a grid point (all buildings, order-free) | 0 pairs of pad groups, 0 shared points | PASS |
| pad-street / ramp / lane clash | no pad point may sit on a street, lane, path or square point at another level (all buildings, order-free) | 0 buildings, 0 grid points | PASS |
| street-street clash | grid points two streets both claim at different levels; the earlier street keeps its level there, so the later one gets a step. A few at a junction where a ramp meets a level street are normal; dozens mean two streets run over each other at different levels (report) | none | REPORT |
| square | one level; every point within 4.0 m of natural ground; no street point at another level; 31 deg bank to everything else | level 75.25 m, cut/fill max 2.72 m, 0 points meet streets at another level ; ok | PASS |
| pad cut / fill (true grid) | every pad point within 4.0 m of the natural ground; aim for 2.5 m (all buildings as drawn) | median 2.63 m, max 3.62 m, 30 over 2.5 m, 0 over 4.0 m  | PASS |
| ground solvable | 31 deg cones between all fixed points must meet (seated set) | 0 infeasible grid points | PASS |
| door threshold vs ground 1 m out | pad (= floor = threshold) within 5 cm of the graded surface 1 m out of the door (seated) | max 0.000 m; 0 fail  | PASS |
| door threshold vs street surface | pad within 5 cm of its street's level at the door's station, for doors within 12 m of the centre line (seated) | 50 checked, 0 fail ; 0 doors more than 12 m from their street (listed in result.json) | PASS |
| wall below ground | highest ground 0.25 m outside the walls minus the floor <= 0.3 m (seated) | max 0.00 m; 0 fail  | PASS |
| overlaps | no two footprint boxes overlap (whole layout as drawn) | 0 pairs ; closest gap 0.004 m | PASS |
| in a street ribbon (own street) | footprint >= half-width + 0.2 m from its own street's centre line (whole layout) | 0 buildings  | PASS |
| corner clearance (other streets) | footprint >= half-width + 1.0 m from every other street's centre line (whole layout) | 0 buildings  | PASS |
| back-to-back gap (31 deg bank) | pads at different levels need at least |dz| / 0.6 m between their grid points (first failure per building) | 0 buildings refused  | PASS |
| banks facing streets | a graded bank over 1.5 m seen from a main street or lane edge, before any building (seated set; report) | 23 runs, 493 stations (by street: {'Q': 4, 'T58': 3, 'T66': 5, 'T74': 3, 'T82': 5, 'T90': 3}) | REPORT |
| straight runs | no main street or lane straight for more than 80 m (within 1.0 m of its chord) | longest main street or lane: T58 59.3 m; roads and paths (report): none | PASS |
| street grades | main streets under 5 % (8 % average, 12 % on a short drop), lanes under 19 %, paths are stairs (report) | {'T58': 3.3, 'T66': 4.8, 'T74': 3.3, 'T82': 4.8, 'T90': 0.0, 'Q': 11.0} | REPORT |
| model / twin share (drawn) | any one model <= 15 %, any one twin group (colour variants of one house) <= 12 % | largest model ND03 7 = 13.7 %, largest twin group ND03 7 = 13.7 % | PASS |
| model / twin share (seated) | any one model <= 15 %, any one twin group (colour variants of one house) <= 12 % (the check is on the town as drawn; the seated share is a report) | largest model ND03 7 = 13.7 %, largest twin group ND03 7 = 13.7 % | REPORT |
| lamps | lamp positions, if given | none given (we place lamps ourselves) | n/a |
| comp seat and height | whole comps with a footprint, if given | none given with a footprint (roles only) | n/a |

## Buildings (in your file's order; grade_order = the order the grader seats them)

| id | model | street | role | pad z | seated | why |
|---|---|---|---|---|---|---|
| B001 | SF03 | SQ | landmark | 75.25 | yes | seated |
| B002 | ND02 | T74 | main | 75.75 | yes | seated |
| B003 | SF15 | T74 | main | 75.75 | yes | seated |
| B004 | WH04 | T74 | main | 75.75 | yes | seated |
| B005 | WH03 | T74 | main | 75.25 | yes | seated |
| B006 | WH23 | T74 | main | 75.25 | yes | seated |
| B007 | ND01 | T74 | main | 75.25 | yes | seated |
| B008 | ND01 | T74 | main | 75.25 | yes | seated |
| B009 | WH19 | T74 | main | 75.25 | yes | seated |
| B010 | WH03 | T74 | main | 75.25 | yes | seated |
| B011 | ND02 | T74 | main | 75.25 | yes | seated |
| B012 | ND02 | T74 | main | 75.25 | yes | seated |
| B013 | ND03 | T66 | lane | 67.50 | yes | seated |
| B014 | WH06 | T66 | lane | 67.50 | yes | seated |
| B015 | ND01 | T66 | lane | 67.50 | yes | seated |
| B016 | ND03 | T66 | lane | 67.50 | yes | seated |
| B017 | WH19 | T66 | lane | 67.50 | yes | seated |
| B019 | WH06 | T66 | lane | 67.50 | yes | seated |
| B020 | WH03 | T82 | lane | 83.25 | yes | seated |
| B021 | WH12 | T82 | lane | 83.25 | yes | seated |
| B022 | WH01 | T82 | lane | 83.25 | yes | seated |
| B023 | ND03 | T82 | lane | 83.25 | yes | seated |
| B024 | WH22 | T82 | lane | 83.25 | yes | seated |
| B025 | WH02 | T82 | lane | 83.25 | yes | seated |
| B026 | WH14 | T82 | lane | 83.25 | yes | seated |
| B027 | ND03 | T82 | lane | 83.25 | yes | seated |
| B028 | WH03 | T82 | lane | 83.25 | yes | seated |
| B029 | ND04 | T82 | lane | 83.25 | yes | seated |
| B030 | WH18 | T82 | lane | 82.50 | yes | seated |
| B031 | WH18 | T58 | lane | 59.75 | yes | seated |
| B032 | ND03 | T58 | lane | 59.75 | yes | seated |
| B033 | WH01 | T90 | lane | 91.25 | yes | seated |
| B034 | WH12 | T90 | lane | 91.25 | yes | seated |
| B035 | ND04 | T90 | lane | 91.25 | yes | seated |
| B036 | WH09 | T90 | lane | 91.25 | yes | seated |
| B037 | WH11 | T90 | lane | 91.25 | yes | seated |
| B038 | WH19 | T90 | lane | 91.25 | yes | seated |
| B039 | WH03 | T90 | lane | 91.25 | yes | seated |
| B040 | WH12 | T90 | lane | 91.25 | yes | seated |
| B041 | WH03 | T90 | lane | 91.25 | yes | seated |
| B042 | WH15 | T90 | lane | 91.25 | yes | seated |
| B043 | WH11 | T90 | lane | 91.25 | yes | seated |
| B044 | ND03 | T90 | lane | 91.25 | yes | seated |
| B045 | SF13 | Q | quay | 3.00 | yes | seated |
| B046 | SF13 | Q | quay | 3.00 | yes | seated |
| B047 | WH12 | Q | quay | 4.50 | yes | seated |
| B048 | ND03 | Q | quay | 4.50 | yes | seated |
| B049 | WH11 | Q | quay | 4.50 | yes | seated |
| B050 | SF15 | Q | quay | 6.25 | yes | seated |
| B051 | WH03 | Q | quay | 6.25 | yes | seated |
| B052 | WH11 | Q | quay | 6.25 | yes | seated |

## Streets

| street | class | width | grid points fixed | points already held by an earlier street at another level | max grade % |
|---|---|---|---|---|---|
| T58 | lane | 5.0 | 79 | 0 | 3.3 |
| T66 | lane | 5.0 | 127 | 0 | 4.8 |
| T74 | lane | 5.0 | 153 | 0 | 3.3 |
| T82 | lane | 5.0 | 166 | 0 | 4.8 |
| T90 | lane | 5.0 | 146 | 0 | 0.0 |
| Q | lane | 5.0 | 145 | 0 | 11.0 |

Files: `plan.png` (every clashing cell drawn), `buildings.csv`, `result.json` (everything, with the grid points).
