"""Ops 5-6 designed approaches, reviewed list v2 (job5/ops5_6_approaches_v2.md, all HUMAN: JOB_5 decisions 14 and 21-28, JOB_4 decision 3).
Replaces the AI drafts the op 5-6 modules read from the sketch. Used only for the plan files and rule 6 of the checks; it does not change routing."""
APPROACHES_V2 = {
 "5-F Esker Redoubt": [
  "SSE up the esker road via 5-M1 (166 deg)",
  "N down the esker from 5-M2 once it falls (14 deg)"
 ],
 "5-M1 Esker Road Gate": [
  "E past 5-05 Kettle North Trench (81 deg)",
  "SW past 5-09 West Fuel Dump (225 deg)"
 ],
 "5-M2 Esker Dugouts": [
  "NNE past 5-08 Stake Causeway Checkpoint (39 deg)",
  "E past 5-04 Walker Park (97 deg)"
 ],
 "5-M3 North-west Battery": [
  "ESE from 5-M2 once it falls (117 deg)",
  "S past 5-02 West Esker AA (196 deg)"
 ],
 "5-M4 Moss Abbey Ruin": [
  "SW past 5-05 (219 deg)",
  "WSW from 5-M1 once it falls (252 deg)"
 ],
 "6-F Cauldron Refinery": [
  "SW over the rim past 6-M1 (225 deg)",
  "E from 6-M4 Cauldron Apron Town (86 deg)"
 ],
 "6-M1 Rim Bunker Ring": [
  "WSW from the start (243 deg)",
  "W past 6-04 Gas Holder (277 deg)"
 ],
 "6-M2 Terrace Batteries": [
  "S past 6-01 Rim Spoil Galleries (179 deg)",
  "ENE past 6-02 Spoil Heap Snipers (78 deg)"
 ],
 "6-M3 Tank Laager": [
  "WNW past 6-01 (288 deg)",
  "SE past 6-10 Crater Lip Pillboxes (122 deg)"
 ],
 "6-M4 Cauldron Apron Town": [
  "SSW from 6-M3 once it falls (214 deg)",
  "N past 6-06 NE Esker Fort (0 deg)"
 ]
}
DECISIONS_V2 = {
 "5-F Esker Redoubt": "J5-14",
 "5-M1 Esker Road Gate": "J5-21 (draft kept)",
 "5-M2 Esker Dugouts": "J5-22",
 "5-M3 North-west Battery": "J5-23 (draft kept)",
 "5-M4 Moss Abbey Ruin": "J5-24",
 "6-F Cauldron Refinery": "JOB_4 decision 3",
 "6-M1 Rim Bunker Ring": "J5-25",
 "6-M2 Terrace Batteries": "J5-26",
 "6-M3 Tank Laager": "J5-27",
 "6-M4 Cauldron Apron Town": "J5-28 (draft kept)"
}
def for_op(op): return {k: v for k, v in APPROACHES_V2.items() if k.startswith(f"{op}-")}
