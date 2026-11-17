# Ops 3-4 self-check, sketch dry run v1 (K3 A sketch ground)

Every number below was measured on the plans in this folder (`op3_plan_sketch_v1.json`, `op4_plan_sketch_v1.json`) on the K3 A sketch ground (16 m cells resampled to 5 m). They are re-measured on drop 2. NOT MEASURED means the sketch cannot answer it.

## Op 3 The Peat-Gas Fields
| id | check | limit | result | tag |
|---|---|---|---|---|
| S1 | comps not a member of a named, graded site | 0 | 0 (every pad is a site's main or member) | MEASURED |
| S2 | sites under their floor on both counts | 0 | 0 measured under; 8 meet on GPs; 8 NOT MEASURED (comps not in the size table); 1 air-only | MEASURED |
| S3 | main smaller than the grade, members not bringing it up | 0 | 0 among measured sites; the 8 unmeasured NOT MEASURED | MEASURED / NOT MEASURED |
| S4 | multi-comp share | >= 1/3 | 6 of 17 | MEASURED |
| S5 | final / mains / supporting; grades; platoon before the final | 1 / 4 / 12; all three; yes | 1 / 4 / 12; 8 / 6 / 3; yes | MEASURED |
| S6 | closest final / main pair | >= 400 m | 1,562 m (3-M1 to 3-M3) | MEASURED |
| S7 | guns under 300 m clear | 0 | 0 of 7 gun comps (30 guns) | MEASURED (sketch; no ops 1-2 comps yet) |
| S8 | ground above the muzzle within 150 m | 0 | 0 (muzzle = pad + 2.0 m, ASSUMED) | MEASURED |
| S9 | gun line meets another comp within 300 m | 0 | 0 | MEASURED |
| S10 | sill step > 0.5 m | 0 | 0 (largest 0.0 m) | MEASURED |
| S11 | road end > 15 m from the gate / > 10 deg off the gate axis | 0 | road ends 4.0 m off the pad edge at most; the gate axis is NOT MEASURED (comps' authored gates unknown) | MEASURED / NOT MEASURED |
| S12 | checkpoints not astride their road | 0 | **3 of 3 FAIL**: the planner ends roads at pad edges; no road yet runs through a checkpoint's passage (3-05, 3-12, 3-M2's TKTA) | MEASURED |
| S13 | banned / superseded / filler; "(D)" listed | 0 / listed | 0; "(D)": 3-02 CIS Depot (Fixed) with GPs (D) | MEASURED |
| S14 | stake / reason; two approaches; recon | 0 | stakes and approaches all set; recon NOT MEASURED (no vegetation) | MEASURED / NOT MEASURED |
| S15 | garrison; alive split | <= 1,200 | 770 planned (K3, ASSUMED); split 700 / 200 / 300 | ASSUMED |
| S16 | pad cut / fill; spacing; waterline; below +0.5 | 0 each | 0 each: largest change 0.58 m; waterline 10 m held; lowest pad +0.5 m | MEASURED |
| R1 | bend radius under 12 m (10 m chords, every 1 m) | 0 | 0; tightest 15.0 m | MEASURED (cut grid) |
| R2-R4 | over 14 % point / 10 m / 20 m | 0 | 0; worst 3.4 / 2.7 / 2.1 % | MEASURED (cut grid) |
| R5 | stacked legs | 0 | 0 | MEASURED |
| R6 | junctions not on a 20 m level landing | 0 | 0 of 6 joins | MEASURED |
| R7 | longest straight; cut / fill | <= 150 m; <= 4 m | 112 m; 0.18 m | MEASURED |
| R8 | objects within 3 m of a road edge | 0 | 0 (planner rule 3) | MEASURED |
| R9 | water gaps not listed; 3AS without a second way; Wall Gates | 0 | 0 (op 3 crosses no water after decision 42) | MEASURED |
| M3 | lowest AI net point; unlisted water gaps | >= +0.5; 0 | +0.5 m (one road raised from +0.39 m); 0 | MEASURED |
| M4 | ops 1-2 sites without a reserve area | 0 | NOT MEASURED (ops 1-2 come in drop 2); op 3: 5 of 5 mains and final have one | MEASURED / NOT MEASURED |
| M5 | incised straights > 300 m not listed | 0 | 0 | MEASURED |
| M8 | 3AS bridges without a second way | 0 | 0 | MEASURED |

## Op 4 The Drain
| id | check | limit | result | tag |
|---|---|---|---|---|
| S1 | comps not a member of a site | 0 | 0 | MEASURED |
| S2 | under the floor on both counts | 0 | 0 measured under; 6 meet; 9 NOT MEASURED; 1 air-only; the village ASSUMED met | MEASURED |
| S3 | main smaller than the grade | 0 | 0 among measured | MEASURED |
| S4 | multi-comp share | >= 1/3 | 6 of 17 | MEASURED |
| S5 | final / mains / supporting; grades; platoon before the final | 1 / 4 / 12; all three; yes | 1 / 4 / 12; 7 / 7 / 3; yes | MEASURED |
| S6 | closest final / main pair | >= 400 m | 1,817 m (4-F to 4-M3) | MEASURED |
| S7-S9 | guns: clear 300 m; ground above muzzle in 150 m; comp in line | 0 / 0 / 0 | 0 / 0 / 0 over 8 gun comps (32 guns); each member faces the designed approach on its side | MEASURED (bearings AI) |
| S10 | sill step > 0.5 m | 0 | 0 | MEASURED |
| S11 | road end / gate axis | 0 | 4.0 m at most; gate axis NOT MEASURED | MEASURED / NOT MEASURED |
| S12 | checkpoints not astride their road | 0 | **5 of 5 FAIL** (4-06, 4-M1's two guards, 4-M2's two gates): roads end at pad edges | MEASURED |
| S13 | names; "(D)" listed | 0 / listed | 0; "(D)": 4-10 CIS Vehicle Depot with GPs (D) | MEASURED |
| S14 | stake / approaches / recon | 0 | set; recon NOT MEASURED | - |
| S15 | garrison; split | <= 1,200 | 885 planned (ASSUMED); 700 / 200 / 300 | ASSUMED |
| S16 | pads | 0 each | 0 each: largest change 0.56 m; lowest pad +0.5 m | MEASURED |
| R1 | bends under 12 m | 0 | 0; tightest 14.6 m | MEASURED (cut grid) |
| R2-R4 | over 14 % | 0 | 0; worst 13.8 / 13.5 / 10.7 % (4-03 to 4-M3) | MEASURED (cut grid) |
| R5 | stacked legs | 0 | 0 | MEASURED |
| R6 | junction landings | 0 | 0 of 9 joins | MEASURED |
| R7 | straight; cut / fill | <= 150 m; <= 4 m | 107 m; 0.84 m | MEASURED |
| R8 | objects within 3 m of a road edge | 0 | 0 | MEASURED |
| R9 | water gaps not listed; 3AS without a second way; Wall Gates | 0 | 0: the three gaps are the three listed crossings, each with its own road line; the 3AS Rail Bridge has two second ways | MEASURED |
| M3 | lowest AI net point | >= +0.5 | +0.5 m (three roads raised from +0.34-0.42 m) | MEASURED |
| M4 | ops 1-2 sites without a reserve area | 0 | NOT MEASURED (drop 2); op 4: 5 of 5 | - |
| M5 | incised straights > 300 m not listed | 0 | 0; the Plank Road causeway (165 m) is listed as a designed straight | MEASURED |
| M8 | 3AS without a second way | 0 | 0 | MEASURED |
