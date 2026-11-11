# Grade: Perys

town_grader 1.0 (11 Nov 2026). Layout `perys_v7_layout`. Version string in the layout: v7 (Kernel third pass, graded with the 11 Nov grader) PROPOSED.

**Seated as drawn: 69 of 69.** Refused: 0.

Refusal causes (our grading agent's categories): none.

Seated by role: landmark 1, square 1, quay 4, main 20, lane 43.

## Checks

| Check | Rule | Result | Status |
|---|---|---|---|
| buildings seated | every building must be seated as drawn | 69 of 69 | PASS |
| refusals by kind | first failed test per refused building | none | PASS |
| pad-pad clash | two pads at different levels may not share a grid point (all buildings, order-free) | 0 pairs of pad groups, 0 shared points | PASS |
| pad-street / ramp / lane clash | no pad point may sit on a street, lane, path or square point at another level (all buildings, order-free) | 0 buildings, 0 grid points | PASS |
| street-street clash | grid points two streets both claim at different levels; the earlier street keeps its level there, so the later one gets a step. A few at a junction where a ramp meets a level street are normal; dozens mean two streets run over each other at different levels (report) | {'CT1': 25, 'CT2': 27, 'CU1': 18, 'CU2': 23, 'CU3': 25, 'CU4': 22, 'CM1': 25, 'CM2': 19, 'CM3': 21, 'CM4': 25, 'HL': 14, 'HR': 33} | REPORT |
| square | one level; every point within 4.0 m of natural ground; no street point at another level; 31 deg bank to everything else | level 57.00 m, cut/fill max 3.71 m, 0 points meet streets at another level ; ok | PASS |
| fixed pad QUAY | a fixed level patch of ours (from --fixed) | level 2.20 m, cut/fill 2.93 m, ok | PASS |
| pad cut / fill (true grid) | every pad point within 4.0 m of the natural ground; aim for 2.5 m (all buildings as drawn) | median 2.10 m, max 3.79 m, 25 over 2.5 m, 0 over 4.0 m  | PASS |
| ground solvable | 31 deg cones between all fixed points must meet (seated set) | 0 infeasible grid points | PASS |
| door threshold vs ground 1 m out | pad (= floor = threshold) within 5 cm of the graded surface 1 m out of the door (seated) | max 0.000 m; 0 fail  | PASS |
| door threshold vs street surface | pad within 5 cm of its street's level at the door's station, for doors within 12 m of the centre line (seated) | 63 checked, 0 fail ; 0 doors more than 12 m from their street (listed in result.json) | PASS |
| wall below ground | highest ground 0.25 m outside the walls minus the floor <= 0.3 m (seated) | max 0.00 m; 0 fail  | PASS |
| overlaps | no two footprint boxes overlap (whole layout as drawn) | 0 pairs ; closest gap 0.006 m | PASS |
| in a street ribbon (own street) | footprint >= half-width + 0.2 m from its own street's centre line (whole layout) | 0 buildings  | PASS |
| corner clearance (other streets) | footprint >= half-width + 1.0 m from every other street's centre line (whole layout) | 0 buildings  | PASS |
| back-to-back gap (31 deg bank) | pads at different levels need at least |dz| / 0.6 m between their grid points (first failure per building) | 0 buildings refused  | PASS |
| banks facing streets | a graded bank over 1.5 m seen from a main street or lane edge, before any building (seated set; report) | 26 runs, 102 stations (by street: {'CM1': 1, 'CM2': 1, 'CM3': 1, 'CU2': 1, 'KE': 4, 'KW': 2, 'M': 9, 'U': 4, 'U2': 3}) | REPORT |
| straight runs | no main street or lane straight for more than 80 m (within 1.0 m of its chord) | longest main street or lane: U 73.7 m; roads and paths (report): HR 169.2 m | PASS |
| street grades | main streets under 5 % (8 % average, 12 % on a short drop), lanes under 19 %, paths are stairs (report) | {'M': 12.0, 'U': 19.1, 'U2': 14.0, 'KW': 7.8, 'KE': 19.1, 'CT1': 9.1, 'CT2': 9.5, 'CU1': 10.9, 'CU2': 11.9, 'CU3': 11.0, 'CU4': 11.5, 'CM1': 14.5, 'CM2': 12.7, 'CM3': 17.0, 'CM4': 15.9, 'HL': 10.3, 'HR': 11.4} | REPORT |
| model / twin share (drawn) | any one model <= 15 %, any one twin group (colour variants of one house) <= 12 % | largest model ND02 6 = 8.7 %, largest twin group ND01+ND02 8 = 11.6 % | PASS |
| model / twin share (seated) | any one model <= 15 %, any one twin group (colour variants of one house) <= 12 % (the check is on the town as drawn; the seated share is a report) | largest model ND02 6 = 8.7 %, largest twin group ND01+ND02 8 = 11.6 % | REPORT |
| lamps | lamp positions, if given | none given (we place lamps ourselves) | n/a |
| comp seat and height | a whole comp needs its own level pad (every grid point of its rectangle at its pad_z_m, the same tests as a building pad, after the buildings), clear of seated buildings and of every carriageway | [('Landing Pad Crap (the quay comp: a landing pad and crates) (kept from v4)', 'level 2.2: its pad would seat: cut/fill 3.50')] | PASS |

## Buildings (in your file's order; grade_order = the order the grader seats them)

| id | model | street | role | pad z | seated | why |
|---|---|---|---|---|---|---|
| B001 | ND07 | SQ | landmark | 57.00 | yes | seated |
| B002 | WH09 | SQ | square | 57.00 | yes | seated |
| B003 | ND05 | M | main | 59.40 | yes | seated |
| B004 | SF08 | M | main | 59.40 | yes | seated |
| B005 | WH08 | M | main | 59.40 | yes | seated |
| B006 | ND02 | M | main | 57.00 | yes | seated |
| B007 | SF08 | M | main | 57.00 | yes | seated |
| B008 | ND01 | M | main | 57.00 | yes | seated |
| B009 | ND02 | M | main | 53.50 | yes | seated |
| B010 | ND02 | M | main | 50.00 | yes | seated |
| B011 | ND01 | M | main | 50.00 | yes | seated |
| B012 | SF15 | M | main | 59.40 | yes | seated |
| B013 | ND05 | M | main | 59.40 | yes | seated |
| B014 | ND03 | M | main | 59.40 | yes | seated |
| B015 | ND02 | M | main | 57.75 | yes | seated |
| B016 | WH19 | M | main | 57.00 | yes | seated |
| B017 | SF01 | M | main | 57.00 | yes | seated |
| B018 | WH23 | M | main | 57.00 | yes | seated |
| B019 | ND02 | M | main | 57.00 | yes | seated |
| B020 | WH08 | M | main | 57.00 | yes | seated |
| B021 | WH12 | M | main | 57.00 | yes | seated |
| B022 | WH11 | M | main | 50.00 | yes | seated |
| B023 | ND03 | U | lane | 62.75 | yes | seated |
| B024 | ND02 | U | lane | 62.75 | yes | seated |
| B025 | WH06 | U | lane | 58.75 | yes | seated |
| B028 | WH07 | U | lane | 62.75 | yes | seated |
| B029 | WH02 | U | lane | 62.75 | yes | seated |
| B030 | ND03 | U | lane | 62.75 | yes | seated |
| B031 | WH12 | U | lane | 62.75 | yes | seated |
| B032 | SF15 | U | lane | 62.75 | yes | seated |
| B033 | WH03 | U | lane | 62.00 | yes | seated |
| B034 | WH17 | U | lane | 62.00 | yes | seated |
| B035 | WH11 | U | lane | 62.00 | yes | seated |
| B036 | WH12 | U | lane | 62.00 | yes | seated |
| B037 | WH24 | U | lane | 62.00 | yes | seated |
| B038 | WH12 | U | lane | 58.75 | yes | seated |
| B039 | WH17 | U | lane | 58.75 | yes | seated |
| B040 | WH07 | U | lane | 55.75 | yes | seated |
| B041 | ND03 | U | lane | 55.75 | yes | seated |
| B042 | WH11 | KW | lane | 53.25 | yes | seated |
| B043 | WH03 | KW | lane | 52.00 | yes | seated |
| B044 | WH05 | KW | lane | 52.00 | yes | seated |
| B045 | WH04 | KE | lane | 47.75 | yes | seated |
| B046 | SF16 | KE | lane | 47.75 | yes | seated |
| B047 | WH24 | KE | lane | 47.75 | yes | seated |
| B048 | SF16 | KE | lane | 42.25 | yes | seated |
| B049 | WH17 | KE | lane | 42.25 | yes | seated |
| B050 | WH08 | KE | lane | 42.25 | yes | seated |
| B051 | WH19 | KE | lane | 47.75 | yes | seated |
| B052 | WH19 | KE | lane | 42.25 | yes | seated |
| B053 | WH22 | KE | lane | 42.25 | yes | seated |
| B054 | ND03 | U2 | lane | 65.75 | yes | seated |
| B055 | WH17 | U2 | lane | 65.75 | yes | seated |
| B056 | WH03 | U2 | lane | 65.75 | yes | seated |
| B057 | WH17 | U2 | lane | 67.00 | yes | seated |
| B058 | WH08 | U2 | lane | 67.00 | yes | seated |
| B059 | ND04 | U2 | lane | 67.00 | yes | seated |
| B060 | WH04 | U2 | lane | 67.00 | yes | seated |
| B061 | WH05 | U2 | lane | 67.00 | yes | seated |
| B062 | WH12 | U2 | lane | 65.75 | yes | seated |
| B063 | WH05 | U2 | lane | 65.75 | yes | seated |
| B064 | WH19 | U2 | lane | 65.75 | yes | seated |
| B065 | WH06 | U2 | lane | 65.75 | yes | seated |
| B066 | ND03 | U2 | lane | 63.50 | yes | seated |
| B067 | WH12 | U2 | lane | 63.50 | yes | seated |
| B068 | IN01 | QY | quay | 2.20 | yes | seated |
| B069 | IN03 | QY | quay | 2.20 | yes | seated |
| B070 | IN01 | QY | quay | 2.20 | yes | seated |
| B071 | IN03 | QY | quay | 2.20 | yes | seated |

## Streets

| street | class | width | grid points fixed | points already held by an earlier street at another level | max grade % |
|---|---|---|---|---|---|
| M | main | 8.0 | 288 | 0 | 12.0 |
| U | lane | 5.0 | 248 | 0 | 19.1 |
| U2 | lane | 5.0 | 169 | 0 | 14.0 |
| KW | lane | 5.0 | 79 | 0 | 7.8 |
| KE | lane | 5.0 | 111 | 0 | 19.1 |
| CT1 | lane | 4.5 | 23 | 25 | 9.1 |
| CT2 | lane | 4.5 | 22 | 27 | 9.5 |
| CU1 | lane | 4.5 | 19 | 18 | 10.9 |
| CU2 | lane | 4.5 | 21 | 23 | 11.9 |
| CU3 | lane | 4.5 | 19 | 25 | 11.0 |
| CU4 | lane | 4.5 | 23 | 22 | 11.5 |
| CM1 | lane | 4.5 | 21 | 25 | 14.5 |
| CM2 | lane | 4.5 | 22 | 19 | 12.7 |
| CM3 | lane | 4.5 | 25 | 21 | 17.0 |
| CM4 | lane | 4.5 | 19 | 25 | 15.9 |
| HL | lane | 5.0 | 39 | 14 | 10.3 |
| HR | road | 7.0 | 354 | 33 | 11.4 |

Files: `plan.png` (every clashing cell drawn), `buildings.csv`, `result.json` (everything, with the grid points).
