# Grade: Sound Head

town_grader 1.0 (11 Nov 2026). Layout `sound_head_v2_layout`. Version string in the layout: K6 v2 (graded with the 11 Nov grader) PROPOSED.

**Seated as drawn: 27 of 27.** Refused: 0.

Refusal causes (our grading agent's categories): none.

Seated by role: landmark 1, square 1, main 6, lane 19.

## Checks

| Check | Rule | Result | Status |
|---|---|---|---|
| buildings seated | every building must be seated as drawn | 27 of 27 | PASS |
| refusals by kind | first failed test per refused building | none | PASS |
| pad-pad clash | two pads at different levels may not share a grid point (all buildings, order-free) | 0 pairs of pad groups, 0 shared points | PASS |
| pad-street / ramp / lane clash | no pad point may sit on a street, lane, path or square point at another level (all buildings, order-free) | 0 buildings, 0 grid points | PASS |
| street-street clash | grid points two streets both claim at different levels; the earlier street keeps its level there, so the later one gets a step. A few at a junction where a ramp meets a level street are normal; dozens mean two streets run over each other at different levels (report) | none | REPORT |
| square | one level; every point within 4.0 m of natural ground; no street point at another level; 31 deg bank to everything else | level 33.00 m, cut/fill max 2.94 m, 0 points meet streets at another level ; ok | PASS |
| pad cut / fill (true grid) | every pad point within 4.0 m of the natural ground; aim for 2.5 m (all buildings as drawn) | median 3.20 m, max 3.94 m, 27 over 2.5 m, 0 over 4.0 m  | PASS |
| ground solvable | 31 deg cones between all fixed points must meet (seated set) | 0 infeasible grid points | PASS |
| door threshold vs ground 1 m out | pad (= floor = threshold) within 5 cm of the graded surface 1 m out of the door (seated) | max 0.000 m; 0 fail  | PASS |
| door threshold vs street surface | pad within 5 cm of its street's level at the door's station, for doors within 12 m of the centre line (seated) | 25 checked, 0 fail ; 0 doors more than 12 m from their street (listed in result.json) | PASS |
| wall below ground | highest ground 0.25 m outside the walls minus the floor <= 0.3 m (seated) | max 0.00 m; 0 fail  | PASS |
| overlaps | no two footprint boxes overlap (whole layout as drawn) | 0 pairs ; closest gap 0.129 m | PASS |
| in a street ribbon (own street) | footprint >= half-width + 0.2 m from its own street's centre line (whole layout) | 0 buildings  | PASS |
| corner clearance (other streets) | footprint >= half-width + 1.0 m from every other street's centre line (whole layout) | 0 buildings  | PASS |
| back-to-back gap (31 deg bank) | pads at different levels need at least |dz| / 0.6 m between their grid points (first failure per building) | 0 buildings refused  | PASS |
| banks facing streets | a graded bank over 1.5 m seen from a main street or lane edge, before any building (seated set; report) | 27 runs, 463 stations (by street: {'M': 8, 'T11': 5, 'T23': 8, 'T47': 4, 'T59': 2}) | REPORT |
| straight runs | no main street or lane straight for more than 80 m (within 1.0 m of its chord) | longest main street or lane: T47 30.0 m; roads and paths (report): none | PASS |
| street grades | main streets under 5 % (8 % average, 12 % on a short drop), lanes under 19 %, paths are stairs (report) | {'M': 12.1, 'T11': 0.0, 'T23': 0.0, 'T47': 3.2, 'T59': 0.0} | REPORT |
| model / twin share (drawn) | any one model <= 15 %, any one twin group (colour variants of one house) <= 12 % | largest model SF03 4 = 14.8 %, largest twin group SF03 4 = 14.8 % | PASS |
| model / twin share (seated) | any one model <= 15 %, any one twin group (colour variants of one house) <= 12 % (the check is on the town as drawn; the seated share is a report) | largest model SF03 4 = 14.8 %, largest twin group SF03 4 = 14.8 % | REPORT |
| lamps | lamp positions, if given | none given (we place lamps ourselves) | n/a |
| comp seat and height | a whole comp needs its own level pad (every grid point of its rectangle at its pad_z_m, the same tests as a building pad, after the buildings), clear of seated buildings and of every carriageway | [('gate square: market or cargo group (whole comp, your pick)', 'level 33.0: its pad would seat: cut/fill 2.71'), ('quay comp: boat slips / cargo pad (whole comp, your pick)', 'level 3.0: its pad would seat: cut/fill 3.58')] | PASS |

## Buildings (in your file's order; grade_order = the order the grader seats them)

| id | model | street | role | pad z | seated | why |
|---|---|---|---|---|---|---|
| B001 | ND06 | SQ | landmark | 33.00 | yes | seated |
| B002 | SF03 | SQ | square | 33.00 | yes | seated |
| B003 | SF03 | M | main | 37.00 | yes | seated |
| B004 | SF03 | M | main | 37.00 | yes | seated |
| B005 | SF03 | M | main | 37.00 | yes | seated |
| B006 | ND01 | M | main | 37.00 | yes | seated |
| B010 | ND01 | M | main | 37.00 | yes | seated |
| B011 | ND03 | M | main | 36.50 | yes | seated |
| B012 | ND02 | T11 | lane | 12.75 | yes | seated |
| B014 | WH03 | T11 | lane | 12.75 | yes | seated |
| B017 | WH19 | T11 | lane | 12.75 | yes | seated |
| B019 | ND03 | T23 | lane | 25.00 | yes | seated |
| B020 | WH19 | T23 | lane | 25.00 | yes | seated |
| B021 | ND03 | T23 | lane | 25.00 | yes | seated |
| B022 | WH17 | T23 | lane | 25.00 | yes | seated |
| B023 | WH19 | T23 | lane | 25.00 | yes | seated |
| B024 | ND03 | T23 | lane | 25.00 | yes | seated |
| B026 | WH03 | T23 | lane | 25.00 | yes | seated |
| B028 | WH03 | T23 | lane | 25.00 | yes | seated |
| B030 | WH06 | T47 | lane | 49.00 | yes | seated |
| B031 | WH03 | T47 | lane | 49.00 | yes | seated |
| B032 | WH17 | T47 | lane | 49.00 | yes | seated |
| B034 | WH19 | T47 | lane | 49.00 | yes | seated |
| B035 | WH06 | T47 | lane | 49.00 | yes | seated |
| B039 | WH06 | T59 | lane | 60.75 | yes | seated |
| B041 | WH06 | T59 | lane | 60.75 | yes | seated |
| B042 | WH17 | T59 | lane | 60.75 | yes | seated |

## Streets

| street | class | width | grid points fixed | points already held by an earlier street at another level | max grade % |
|---|---|---|---|---|---|
| M | main | 7.0 | 193 | 0 | 12.1 |
| T11 | lane | 4.5 | 76 | 0 | 0.0 |
| T23 | lane | 4.5 | 148 | 0 | 0.0 |
| T47 | lane | 4.5 | 168 | 0 | 3.2 |
| T59 | lane | 4.5 | 83 | 0 | 0.0 |

Files: `plan.png` (every clashing cell drawn), `buildings.csv`, `result.json` (everything, with the grid points).
