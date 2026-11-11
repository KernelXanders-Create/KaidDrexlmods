# Grade: Kastro Quay

town_grader 1.0 (11 Nov 2026). Layout `kastro_quay_v2_layout`. Version string in the layout: K6 v2 (option b, graded with the 11 Nov grader) PROPOSED.

**Seated as drawn: 34 of 34.** Refused: 0.

Refusal causes (our grading agent's categories): none.

Seated by role: landmark 1, main 13, lane 20.

## Checks

| Check | Rule | Result | Status |
|---|---|---|---|
| buildings seated | every building must be seated as drawn | 34 of 34 | PASS |
| refusals by kind | first failed test per refused building | none | PASS |
| pad-pad clash | two pads at different levels may not share a grid point (all buildings, order-free) | 0 pairs of pad groups, 0 shared points | PASS |
| pad-street / ramp / lane clash | no pad point may sit on a street, lane, path or square point at another level (all buildings, order-free) | 0 buildings, 0 grid points | PASS |
| street-street clash | grid points two streets both claim at different levels; the earlier street keeps its level there, so the later one gets a step. A few at a junction where a ramp meets a level street are normal; dozens mean two streets run over each other at different levels (report) | {'N1': 4, 'C1': 11, 'C2': 19} | REPORT |
| square | one level; every point within 4.0 m of natural ground; no street point at another level; 31 deg bank to everything else | level 134.00 m, cut/fill max 3.54 m, 0 points meet streets at another level ; ok | PASS |
| pad cut / fill (true grid) | every pad point within 4.0 m of the natural ground; aim for 2.5 m (all buildings as drawn) | median 2.96 m, max 3.95 m, 24 over 2.5 m, 0 over 4.0 m  | PASS |
| ground solvable | 31 deg cones between all fixed points must meet (seated set) | 0 infeasible grid points | PASS |
| door threshold vs ground 1 m out | pad (= floor = threshold) within 5 cm of the graded surface 1 m out of the door (seated) | max 0.000 m; 0 fail  | PASS |
| door threshold vs street surface | pad within 5 cm of its street's level at the door's station, for doors within 12 m of the centre line (seated) | 33 checked, 0 fail ; 0 doors more than 12 m from their street (listed in result.json) | PASS |
| wall below ground | highest ground 0.25 m outside the walls minus the floor <= 0.3 m (seated) | max 0.00 m; 0 fail  | PASS |
| overlaps | no two footprint boxes overlap (whole layout as drawn) | 0 pairs ; closest gap 0.083 m | PASS |
| in a street ribbon (own street) | footprint >= half-width + 0.2 m from its own street's centre line (whole layout) | 0 buildings  | PASS |
| corner clearance (other streets) | footprint >= half-width + 1.0 m from every other street's centre line (whole layout) | 0 buildings  | PASS |
| back-to-back gap (31 deg bank) | pads at different levels need at least |dz| / 0.6 m between their grid points (first failure per building) | 0 buildings refused  | PASS |
| banks facing streets | a graded bank over 1.5 m seen from a main street or lane edge, before any building (seated set; report) | 19 runs, 186 stations (by street: {'B1': 1, 'BS': 2, 'C1': 1, 'C2': 1, 'M': 6, 'N1': 1, 'W': 7}) | REPORT |
| straight runs | no main street or lane straight for more than 80 m (within 1.0 m of its chord) | longest main street or lane: BS 65.8 m; roads and paths (report): none | PASS |
| street grades | main streets under 5 % (8 % average, 12 % on a short drop), lanes under 19 %, paths are stairs (report) | {'M': 12.1, 'W': 19.1, 'N1': 17.4, 'BS': 19.1, 'B1': 19.2, 'C1': 13.8, 'C2': 12.8} | REPORT |
| model / twin share (drawn) | any one model <= 15 %, any one twin group (colour variants of one house) <= 12 % | largest model ND02 4 = 11.8 %, largest twin group ND01+ND02 4 = 11.8 % | PASS |
| model / twin share (seated) | any one model <= 15 %, any one twin group (colour variants of one house) <= 12 % (the check is on the town as drawn; the seated share is a report) | largest model ND02 4 = 11.8 %, largest twin group ND01+ND02 4 = 11.8 % | REPORT |
| lamps | lamp positions, if given | none given (we place lamps ourselves) | n/a |
| comp seat and height | whole comps with a footprint, if given | none given with a footprint (roles only) | n/a |

## Buildings (in your file's order; grade_order = the order the grader seats them)

| id | model | street | role | pad z | seated | why |
|---|---|---|---|---|---|---|
| B001 | SF02 | SQ | landmark | 134.00 | yes | seated |
| B002 | WH03 | M | main | 135.50 | yes | seated |
| B003 | WH09 | M | main | 134.00 | yes | seated |
| B004 | ND02 | M | main | 134.00 | yes | seated |
| B005 | SF15 | M | main | 121.75 | yes | seated |
| B006 | WH11 | M | main | 121.75 | yes | seated |
| B007 | ND02 | M | main | 132.75 | yes | seated |
| B008 | SF15 | M | main | 135.50 | yes | seated |
| B009 | WH03 | M | main | 135.50 | yes | seated |
| B010 | WH11 | M | main | 134.00 | yes | seated |
| B011 | SF13 | M | main | 134.00 | yes | seated |
| B012 | SF16 | M | main | 134.00 | yes | seated |
| B013 | ND03 | M | main | 121.75 | yes | seated |
| B014 | WH12 | M | main | 121.75 | yes | seated |
| B015 | WH17 | N1 | lane | 121.75 | yes | seated |
| B016 | ND02 | N1 | lane | 121.75 | yes | seated |
| B017 | WH09 | N1 | lane | 119.00 | yes | seated |
| B018 | ND02 | W | lane | 119.25 | yes | seated |
| B019 | WH19 | W | lane | 119.25 | yes | seated |
| B021 | WH17 | W | lane | 129.75 | yes | seated |
| B022 | WH08 | W | lane | 129.75 | yes | seated |
| B023 | WH18 | W | lane | 134.25 | yes | seated |
| B026 | ND03 | W | lane | 119.25 | yes | seated |
| B027 | WH10 | W | lane | 129.75 | yes | seated |
| B028 | WH09 | W | lane | 134.25 | yes | seated |
| B029 | WH22 | BS | lane | 122.00 | yes | seated |
| B030 | WH18 | BS | lane | 122.00 | yes | seated |
| B031 | ND03 | BS | lane | 122.00 | yes | seated |
| B032 | WH22 | BS | lane | 115.75 | yes | seated |
| B033 | WH11 | BS | lane | 115.75 | yes | seated |
| B034 | WH18 | B1 | lane | 108.25 | yes | seated |
| B035 | SF15 | B1 | lane | 108.25 | yes | seated |
| B036 | WH03 | B1 | lane | 108.25 | yes | seated |
| B037 | WH11 | B1 | lane | 108.25 | yes | seated |

## Streets

| street | class | width | grid points fixed | points already held by an earlier street at another level | max grade % |
|---|---|---|---|---|---|
| M | main | 7.0 | 321 | 0 | 12.1 |
| W | lane | 5.0 | 192 | 0 | 19.1 |
| N1 | lane | 5.0 | 44 | 4 | 17.4 |
| BS | lane | 5.0 | 66 | 0 | 19.1 |
| B1 | lane | 5.0 | 65 | 0 | 19.2 |
| C1 | lane | 4.5 | 29 | 11 | 13.8 |
| C2 | lane | 4.5 | 41 | 19 | 12.8 |

Files: `plan.png` (every clashing cell drawn), `buildings.csv`, `result.json` (everything, with the grid points).
