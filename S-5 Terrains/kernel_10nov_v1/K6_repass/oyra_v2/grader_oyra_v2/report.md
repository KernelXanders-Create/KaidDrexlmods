# Grade: Oyra

town_grader 1.0 (11 Nov 2026). Layout `oyra_v2_layout`. Version string in the layout: K6 v2 (graded with the 11 Nov grader) PROPOSED.

**Seated as drawn: 106 of 106.** Refused: 0.

Refusal causes (our grading agent's categories): none.

Seated by role: landmark 1, main 40, lane 65.

## Checks

| Check | Rule | Result | Status |
|---|---|---|---|
| buildings seated | every building must be seated as drawn | 106 of 106 | PASS |
| refusals by kind | first failed test per refused building | none | PASS |
| pad-pad clash | two pads at different levels may not share a grid point (all buildings, order-free) | 0 pairs of pad groups, 0 shared points | PASS |
| pad-street / ramp / lane clash | no pad point may sit on a street, lane, path or square point at another level (all buildings, order-free) | 0 buildings, 0 grid points | PASS |
| street-street clash | grid points two streets both claim at different levels; the earlier street keeps its level there, so the later one gets a step. A few at a junction where a ramp meets a level street are normal; dozens mean two streets run over each other at different levels (report) | {'C2': 22, 'C3': 16, 'C4': 14} | REPORT |
| square | one level; every point within 4.0 m of natural ground; no street point at another level; 31 deg bank to everything else | level 129.75 m, cut/fill max 3.68 m, 0 points meet streets at another level ; ok | PASS |
| pad cut / fill (true grid) | every pad point within 4.0 m of the natural ground; aim for 2.5 m (all buildings as drawn) | median 1.90 m, max 3.94 m, 35 over 2.5 m, 0 over 4.0 m  | PASS |
| ground solvable | 31 deg cones between all fixed points must meet (seated set) | 0 infeasible grid points | PASS |
| door threshold vs ground 1 m out | pad (= floor = threshold) within 5 cm of the graded surface 1 m out of the door (seated) | max 0.000 m; 0 fail  | PASS |
| door threshold vs street surface | pad within 5 cm of its street's level at the door's station, for doors within 12 m of the centre line (seated) | 105 checked, 0 fail ; 0 doors more than 12 m from their street (listed in result.json) | PASS |
| wall below ground | highest ground 0.25 m outside the walls minus the floor <= 0.3 m (seated) | max 0.00 m; 0 fail  | PASS |
| overlaps | no two footprint boxes overlap (whole layout as drawn) | 0 pairs ; closest gap 0.000 m | PASS |
| in a street ribbon (own street) | footprint >= half-width + 0.2 m from its own street's centre line (whole layout) | 0 buildings  | PASS |
| corner clearance (other streets) | footprint >= half-width + 1.0 m from every other street's centre line (whole layout) | 0 buildings  | PASS |
| back-to-back gap (31 deg bank) | pads at different levels need at least |dz| / 0.6 m between their grid points (first failure per building) | 0 buildings refused  | PASS |
| banks facing streets | a graded bank over 1.5 m seen from a main street or lane edge, before any building (seated set; report) | 18 runs, 55 stations (by street: {'R': 7, 'U': 5, 'V': 6}) | REPORT |
| straight runs | no main street or lane straight for more than 80 m (within 1.0 m of its chord) | longest main street or lane: R 64.8 m; roads and paths (report): none | PASS |
| street grades | main streets under 5 % (8 % average, 12 % on a short drop), lanes under 19 %, paths are stairs (report) | {'R': 6.3, 'U': 7.8, 'V': 15.8, 'C1': 0.0, 'C2': 1.0, 'C3': 11.1, 'C4': 12.9} | REPORT |
| model / twin share (drawn) | any one model <= 15 %, any one twin group (colour variants of one house) <= 12 % | largest model ND03 11 = 10.4 %, largest twin group ND01+ND02 12 = 11.3 % | PASS |
| model / twin share (seated) | any one model <= 15 %, any one twin group (colour variants of one house) <= 12 % (the check is on the town as drawn; the seated share is a report) | largest model ND03 11 = 10.4 %, largest twin group ND01+ND02 12 = 11.3 % | REPORT |
| lamps | lamp positions, if given | none given (we place lamps ourselves) | n/a |
| comp seat and height | whole comps with a footprint, if given | none given with a footprint (roles only) | n/a |

## Buildings (in your file's order; grade_order = the order the grader seats them)

| id | model | street | role | pad z | seated | why |
|---|---|---|---|---|---|---|
| B001 | ND07 | SQ | landmark | 129.75 | yes | seated |
| B002 | WH07 | R | main | 130.75 | yes | seated |
| B003 | SF01 | R | main | 130.75 | yes | seated |
| B004 | ND03 | R | main | 130.75 | yes | seated |
| B005 | SF08 | R | main | 130.75 | yes | seated |
| B006 | SF16 | R | main | 130.75 | yes | seated |
| B007 | WH22 | R | main | 129.75 | yes | seated |
| B008 | SF16 | R | main | 129.75 | yes | seated |
| B009 | SF15 | R | main | 129.75 | yes | seated |
| B010 | SF08 | R | main | 129.75 | yes | seated |
| B011 | SF01 | R | main | 129.75 | yes | seated |
| B012 | WH18 | R | main | 129.75 | yes | seated |
| B013 | ND02 | R | main | 129.75 | yes | seated |
| B014 | SF16 | R | main | 130.25 | yes | seated |
| B015 | SF15 | R | main | 130.25 | yes | seated |
| B016 | SF16 | R | main | 130.75 | yes | seated |
| B017 | WH18 | R | main | 130.75 | yes | seated |
| B018 | WH19 | R | main | 130.75 | yes | seated |
| B019 | WH19 | R | main | 130.75 | yes | seated |
| B020 | ND02 | R | main | 130.75 | yes | seated |
| B021 | WH18 | R | main | 130.75 | yes | seated |
| B022 | WH18 | R | main | 130.75 | yes | seated |
| B023 | WH18 | R | main | 130.75 | yes | seated |
| B024 | WH03 | R | main | 130.75 | yes | seated |
| B025 | WH24 | R | main | 130.75 | yes | seated |
| B026 | WH07 | R | main | 130.75 | yes | seated |
| B027 | ND02 | R | main | 130.75 | yes | seated |
| B028 | ND01 | R | main | 129.75 | yes | seated |
| B029 | WH12 | R | main | 129.75 | yes | seated |
| B030 | ND01 | R | main | 129.75 | yes | seated |
| B031 | ND03 | R | main | 129.75 | yes | seated |
| B032 | WH19 | R | main | 129.75 | yes | seated |
| B033 | ND02 | R | main | 129.75 | yes | seated |
| B034 | WH19 | R | main | 129.75 | yes | seated |
| B035 | SF08 | R | main | 130.25 | yes | seated |
| B036 | WH11 | R | main | 130.25 | yes | seated |
| B037 | WH24 | R | main | 130.75 | yes | seated |
| B038 | WH12 | R | main | 130.75 | yes | seated |
| B039 | WH11 | R | main | 130.75 | yes | seated |
| B040 | ND03 | R | main | 130.75 | yes | seated |
| B041 | WH19 | R | main | 130.75 | yes | seated |
| B042 | WH18 | U | lane | 130.25 | yes | seated |
| B043 | WH09 | U | lane | 130.25 | yes | seated |
| B044 | ND03 | U | lane | 130.25 | yes | seated |
| B045 | WH04 | U | lane | 130.75 | yes | seated |
| B046 | WH11 | U | lane | 130.75 | yes | seated |
| B047 | WH01 | U | lane | 130.00 | yes | seated |
| B048 | WH12 | U | lane | 130.00 | yes | seated |
| B049 | WH08 | U | lane | 130.00 | yes | seated |
| B050 | WH02 | U | lane | 129.25 | yes | seated |
| B051 | WH09 | U | lane | 129.25 | yes | seated |
| B052 | WH01 | U | lane | 128.00 | yes | seated |
| B053 | ND02 | U | lane | 128.00 | yes | seated |
| B054 | WH08 | U | lane | 128.00 | yes | seated |
| B055 | WH23 | U | lane | 128.00 | yes | seated |
| B056 | WH06 | U | lane | 128.00 | yes | seated |
| B057 | ND02 | U | lane | 128.00 | yes | seated |
| B058 | WH15 | U | lane | 128.50 | yes | seated |
| B059 | ND02 | U | lane | 128.50 | yes | seated |
| B060 | WH10 | U | lane | 130.25 | yes | seated |
| B061 | ND03 | U | lane | 130.25 | yes | seated |
| B062 | WH11 | U | lane | 130.25 | yes | seated |
| B063 | ND02 | U | lane | 130.25 | yes | seated |
| B064 | WH03 | U | lane | 130.75 | yes | seated |
| B065 | WH15 | U | lane | 130.00 | yes | seated |
| B066 | WH12 | U | lane | 130.00 | yes | seated |
| B067 | WH17 | U | lane | 129.25 | yes | seated |
| B068 | ND02 | U | lane | 129.25 | yes | seated |
| B069 | ND02 | U | lane | 129.25 | yes | seated |
| B070 | WH15 | U | lane | 128.00 | yes | seated |
| B071 | WH17 | U | lane | 128.00 | yes | seated |
| B072 | WH01 | U | lane | 128.00 | yes | seated |
| B073 | WH09 | U | lane | 128.00 | yes | seated |
| B074 | ND04 | U | lane | 128.00 | yes | seated |
| B075 | WH15 | U | lane | 128.00 | yes | seated |
| B076 | WH23 | U | lane | 128.00 | yes | seated |
| B077 | WH11 | U | lane | 128.50 | yes | seated |
| B078 | WH08 | U | lane | 128.50 | yes | seated |
| B079 | WH17 | V | lane | 124.75 | yes | seated |
| B080 | WH14 | V | lane | 124.75 | yes | seated |
| B081 | WH12 | V | lane | 124.75 | yes | seated |
| B082 | WH17 | V | lane | 125.75 | yes | seated |
| B083 | WH23 | V | lane | 125.75 | yes | seated |
| B084 | ND03 | V | lane | 125.75 | yes | seated |
| B085 | WH24 | V | lane | 125.75 | yes | seated |
| B086 | WH05 | V | lane | 125.75 | yes | seated |
| B087 | WH18 | V | lane | 125.75 | yes | seated |
| B088 | WH09 | V | lane | 125.75 | yes | seated |
| B089 | WH11 | V | lane | 124.25 | yes | seated |
| B090 | WH14 | V | lane | 124.25 | yes | seated |
| B091 | WH17 | V | lane | 124.25 | yes | seated |
| B092 | WH03 | V | lane | 121.75 | yes | seated |
| B093 | WH08 | V | lane | 121.75 | yes | seated |
| B094 | WH17 | V | lane | 122.50 | yes | seated |
| B095 | WH11 | V | lane | 122.50 | yes | seated |
| B096 | WH03 | V | lane | 122.50 | yes | seated |
| B097 | WH03 | V | lane | 124.75 | yes | seated |
| B098 | WH14 | V | lane | 124.75 | yes | seated |
| B099 | ND03 | V | lane | 125.75 | yes | seated |
| B100 | WH17 | V | lane | 125.75 | yes | seated |
| B101 | WH23 | V | lane | 125.75 | yes | seated |
| B102 | ND03 | V | lane | 124.25 | yes | seated |
| B103 | ND03 | V | lane | 124.25 | yes | seated |
| B104 | ND03 | V | lane | 122.50 | yes | seated |
| B105 | ND03 | V | lane | 122.50 | yes | seated |
| B106 | WH14 | V | lane | 122.50 | yes | seated |

## Streets

| street | class | width | grid points fixed | points already held by an earlier street at another level | max grade % |
|---|---|---|---|---|---|
| R | main | 6.5 | 318 | 0 | 6.3 |
| U | lane | 5.0 | 317 | 0 | 7.8 |
| V | lane | 5.0 | 280 | 0 | 15.8 |
| C1 | lane | 4.5 | 36 | 0 | 0.0 |
| C2 | lane | 4.5 | 35 | 22 | 1.0 |
| C3 | lane | 4.5 | 23 | 16 | 11.1 |
| C4 | lane | 4.5 | 24 | 14 | 12.9 |

Files: `plan.png` (every clashing cell drawn), `buildings.csv`, `result.json` (everything, with the grid points).
