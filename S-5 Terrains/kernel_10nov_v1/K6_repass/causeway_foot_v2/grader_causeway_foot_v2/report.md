# Grade: Causeway Foot

town_grader 1.0 (11 Nov 2026). Layout `causeway_foot_v2_layout`. Version string in the layout: K6 v2 (graded with the 11 Nov grader) PROPOSED.

**Seated as drawn: 79 of 79.** Refused: 0.

Refusal causes (our grading agent's categories): none.

Seated by role: landmark 1, square 1, main 12, lane 65.

## Checks

| Check | Rule | Result | Status |
|---|---|---|---|
| buildings seated | every building must be seated as drawn | 79 of 79 | PASS |
| refusals by kind | first failed test per refused building | none | PASS |
| pad-pad clash | two pads at different levels may not share a grid point (all buildings, order-free) | 0 pairs of pad groups, 0 shared points | PASS |
| pad-street / ramp / lane clash | no pad point may sit on a street, lane, path or square point at another level (all buildings, order-free) | 0 buildings, 0 grid points | PASS |
| street-street clash | grid points two streets both claim at different levels; the earlier street keeps its level there, so the later one gets a step. A few at a junction where a ramp meets a level street are normal; dozens mean two streets run over each other at different levels (report) | {'R2': 16, 'C7': 25, 'C8': 30, 'LO': 3, 'C1': 23, 'C2': 19, 'C3': 21, 'C4': 27, 'C5': 25, 'C6': 13, 'R3': 15, 'R4': 9} | REPORT |
| square | one level; every point within 4.0 m of natural ground; no street point at another level; 31 deg bank to everything else | level 1.50 m, cut/fill max 2.00 m, 0 points meet streets at another level ; ok | PASS |
| pad cut / fill (true grid) | every pad point within 4.0 m of the natural ground; aim for 2.5 m (all buildings as drawn) | median 2.85 m, max 3.98 m, 52 over 2.5 m, 0 over 4.0 m  | PASS |
| ground solvable | 31 deg cones between all fixed points must meet (seated set) | 0 infeasible grid points | PASS |
| door threshold vs ground 1 m out | pad (= floor = threshold) within 5 cm of the graded surface 1 m out of the door (seated) | max 0.000 m; 0 fail  | PASS |
| door threshold vs street surface | pad within 5 cm of its street's level at the door's station, for doors within 12 m of the centre line (seated) | 77 checked, 0 fail ; 0 doors more than 12 m from their street (listed in result.json) | PASS |
| wall below ground | highest ground 0.25 m outside the walls minus the floor <= 0.3 m (seated) | max 0.00 m; 0 fail  | PASS |
| overlaps | no two footprint boxes overlap (whole layout as drawn) | 0 pairs ; closest gap 0.001 m | PASS |
| in a street ribbon (own street) | footprint >= half-width + 0.2 m from its own street's centre line (whole layout) | 0 buildings  | PASS |
| corner clearance (other streets) | footprint >= half-width + 1.0 m from every other street's centre line (whole layout) | 0 buildings  | PASS |
| back-to-back gap (31 deg bank) | pads at different levels need at least |dz| / 0.6 m between their grid points (first failure per building) | 0 buildings refused  | PASS |
| banks facing streets | a graded bank over 1.5 m seen from a main street or lane edge, before any building (seated set; report) | 42 runs, 233 stations (by street: {'C1': 1, 'C2': 1, 'C3': 1, 'C4': 1, 'C5': 2, 'C8': 2, 'LO': 1, 'M': 5, 'UA': 7, 'UB': 11, 'UC': 10}) | REPORT |
| straight runs | no main street or lane straight for more than 80 m (within 1.0 m of its chord) | longest main street or lane: R2 62.6 m; roads and paths (report): R3 39.3 m, R4 35.3 m | PASS |
| street grades | main streets under 5 % (8 % average, 12 % on a short drop), lanes under 19 %, paths are stairs (report) | {'M': 12.1, 'R2': 7.8, 'UA': 19.1, 'UB': 19.1, 'UC': 15.6, 'C7': 16.2, 'C8': 14.6, 'LO': 4.8, 'C1': 9.6, 'C2': 13.6, 'C3': 16.4, 'C4': 15.4, 'C5': 15.6, 'C6': 11.7, 'R3': 18.9, 'R4': 11.5} | REPORT |
| model / twin share (drawn) | any one model <= 15 %, any one twin group (colour variants of one house) <= 12 % | largest model ND03 9 = 11.4 %, largest twin group ND03 9 = 11.4 % | PASS |
| model / twin share (seated) | any one model <= 15 %, any one twin group (colour variants of one house) <= 12 % (the check is on the town as drawn; the seated share is a report) | largest model ND03 9 = 11.4 %, largest twin group ND03 9 = 11.4 % | REPORT |
| lamps | lamp positions, if given | none given (we place lamps ourselves) | n/a |
| comp seat and height | whole comps with a footprint, if given | none given with a footprint (roles only) | n/a |

## Buildings (in your file's order; grade_order = the order the grader seats them)

| id | model | street | role | pad z | seated | why |
|---|---|---|---|---|---|---|
| B001 | SF02 | SQ | landmark | 1.50 | yes | seated |
| B002 | SF01 | SQ | square | 1.50 | yes | seated |
| B003 | WH02 | M | main | 1.50 | yes | seated |
| B004 | WH23 | M | main | 7.50 | yes | seated |
| B005 | ND05 | M | main | 7.50 | yes | seated |
| B006 | ND03 | M | main | 12.00 | yes | seated |
| B007 | WH24 | M | main | 12.00 | yes | seated |
| B008 | ND01 | M | main | 12.00 | yes | seated |
| B009 | SF15 | M | main | 1.50 | yes | seated |
| B010 | ND01 | M | main | 1.50 | yes | seated |
| B011 | WH24 | M | main | 1.50 | yes | seated |
| B012 | WH01 | M | main | 1.50 | yes | seated |
| B013 | ND03 | M | main | 12.00 | yes | seated |
| B014 | WH19 | M | main | 12.00 | yes | seated |
| B015 | WH08 | UA | lane | 17.00 | yes | seated |
| B016 | WH06 | UA | lane | 17.00 | yes | seated |
| B017 | WH17 | UA | lane | 17.00 | yes | seated |
| B018 | WH19 | UA | lane | 17.00 | yes | seated |
| B019 | WH06 | UA | lane | 15.25 | yes | seated |
| B020 | WH05 | UA | lane | 15.25 | yes | seated |
| B021 | WH19 | UA | lane | 15.25 | yes | seated |
| B022 | ND01 | UA | lane | 15.25 | yes | seated |
| B023 | ND02 | UA | lane | 11.75 | yes | seated |
| B024 | WH18 | UA | lane | 11.75 | yes | seated |
| B025 | WH12 | UA | lane | 11.75 | yes | seated |
| B026 | WH14 | UA | lane | 11.75 | yes | seated |
| B027 | WH03 | UA | lane | 5.25 | yes | seated |
| B028 | WH11 | UA | lane | 5.25 | yes | seated |
| B029 | WH05 | UA | lane | 5.25 | yes | seated |
| B030 | WH22 | UA | lane | 5.25 | yes | seated |
| B031 | ND01 | UA | lane | 15.25 | yes | seated |
| B032 | ND01 | UA | lane | 15.25 | yes | seated |
| B033 | WH01 | UA | lane | 15.25 | yes | seated |
| B034 | WH05 | UA | lane | 15.25 | yes | seated |
| B035 | WH04 | UA | lane | 11.75 | yes | seated |
| B036 | ND02 | UA | lane | 11.75 | yes | seated |
| B037 | WH22 | UA | lane | 11.75 | yes | seated |
| B038 | WH11 | UA | lane | 11.75 | yes | seated |
| B039 | WH08 | UA | lane | 5.25 | yes | seated |
| B040 | WH19 | UA | lane | 5.25 | yes | seated |
| B041 | WH06 | UA | lane | 5.25 | yes | seated |
| B042 | WH11 | UA | lane | 5.25 | yes | seated |
| B043 | ND02 | UB | lane | 21.75 | yes | seated |
| B044 | ND01 | UB | lane | 21.75 | yes | seated |
| B045 | ND03 | UB | lane | 21.75 | yes | seated |
| B046 | WH15 | UB | lane | 21.75 | yes | seated |
| B047 | WH08 | UB | lane | 21.75 | yes | seated |
| B048 | WH05 | UB | lane | 21.75 | yes | seated |
| B049 | ND03 | UB | lane | 21.75 | yes | seated |
| B050 | WH24 | UB | lane | 21.75 | yes | seated |
| B051 | ND03 | UB | lane | 19.00 | yes | seated |
| B052 | WH12 | UB | lane | 19.00 | yes | seated |
| B053 | WH24 | UB | lane | 19.00 | yes | seated |
| B054 | ND03 | UB | lane | 13.00 | yes | seated |
| B055 | WH03 | UB | lane | 13.00 | yes | seated |
| B056 | WH24 | UB | lane | 13.00 | yes | seated |
| B057 | ND03 | UB | lane | 13.00 | yes | seated |
| B058 | WH06 | UB | lane | 21.75 | yes | seated |
| B059 | WH18 | UB | lane | 19.00 | yes | seated |
| B060 | WH17 | UB | lane | 19.00 | yes | seated |
| B061 | WH19 | UB | lane | 19.00 | yes | seated |
| B062 | WH24 | UB | lane | 13.00 | yes | seated |
| B063 | ND03 | UB | lane | 13.00 | yes | seated |
| B064 | WH04 | UC | lane | 27.75 | yes | seated |
| B065 | WH17 | UC | lane | 27.75 | yes | seated |
| B066 | WH06 | UC | lane | 27.75 | yes | seated |
| B067 | SF16 | UC | lane | 27.75 | yes | seated |
| B068 | WH02 | UC | lane | 27.75 | yes | seated |
| B069 | WH01 | UC | lane | 27.75 | yes | seated |
| B070 | ND03 | UC | lane | 26.75 | yes | seated |
| B071 | WH12 | UC | lane | 26.75 | yes | seated |
| B072 | WH17 | UC | lane | 26.75 | yes | seated |
| B073 | WH19 | UC | lane | 24.25 | yes | seated |
| B074 | WH03 | UC | lane | 24.25 | yes | seated |
| B075 | WH19 | UC | lane | 27.75 | yes | seated |
| B076 | WH03 | UC | lane | 24.25 | yes | seated |
| B077 | WH22 | LO | lane | 7.75 | yes | seated |
| B078 | WH01 | LO | lane | 7.75 | yes | seated |
| B079 | SF15 | LO | lane | 7.00 | yes | seated |

## Streets

| street | class | width | grid points fixed | points already held by an earlier street at another level | max grade % |
|---|---|---|---|---|---|
| M | main | 8.0 | 236 | 0 | 12.1 |
| R2 | main | 8.0 | 187 | 16 | 7.8 |
| UA | lane | 5.0 | 243 | 0 | 19.1 |
| UB | lane | 5.0 | 227 | 0 | 19.1 |
| UC | lane | 5.0 | 182 | 0 | 15.6 |
| C7 | lane | 6.0 | 24 | 25 | 16.2 |
| C8 | lane | 4.5 | 26 | 30 | 14.6 |
| LO | lane | 5.0 | 72 | 3 | 4.8 |
| C1 | lane | 4.5 | 15 | 23 | 9.6 |
| C2 | lane | 6.0 | 26 | 19 | 13.6 |
| C3 | lane | 4.5 | 26 | 21 | 16.4 |
| C4 | lane | 6.0 | 21 | 27 | 15.4 |
| C5 | lane | 4.5 | 19 | 25 | 15.6 |
| C6 | lane | 4.5 | 20 | 13 | 11.7 |
| R3 | road | 6.0 | 46 | 15 | 18.9 |
| R4 | road | 4.5 | 60 | 9 | 11.5 |

Files: `plan.png` (every clashing cell drawn), `buildings.csv`, `result.json` (everything, with the grid points).
