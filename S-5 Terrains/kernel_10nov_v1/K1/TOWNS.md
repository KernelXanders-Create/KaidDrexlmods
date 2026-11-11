# K1 town plans: six hand-made towns for Islands "Ember Caldera" (PROPOSED)

Plans for Miran's look, not build files. North up, metres. Each town has a PNG and a JSON in `towns/`.

## At a glance (MEASURED by tools/make_towns.py)

| Town | Op | Site | Size | Buildings | In blocks | sci-fi / white cube / Naboo dome | Garrison | Longest straight run (main / lanes) | Extent |
|---|---|---|---|---|---|---|---|---|---|
| Causeway Foot | 4 | 4-M3 | platoon | 96 | 94.8 % | 24 / 58 / 14 | 13 | 48.0 / 33.6 m | 228 x 127 m |
| Kamar Village | 6 | 6-01 | two-squad | 82 | 93.9 % | 25 / 44 / 13 | 11 | 42.1 / 73.1 m | 194 x 177 m |
| Kastro Quay | 5 | 5-M3 | platoon | 108 | 96.3 % | 38 / 56 / 14 | 13 | 53.8 / 62.2 m | 204 x 208 m |
| Lantern Quay | 5 | 5-09 | squad | 66 | 93.9 % | 15 / 40 / 11 | 10 | 68.1 / 71.9 m | 131 x 176 m |
| Oyra | 7 | 7-M2 | platoon | 106 | 92.5 % | 22 / 69 / 15 | 13 | 75.7 / 48.0 m | 121 x 258 m |
| Sound Head | 3 | 3-M3 | platoon | 104 | 96.2 % | 33 / 59 / 12 | 13 | 59.9 / 50.4 m | 198 x 164 m |

Checks per town (all PASS, see `tools/checks.txt`): 60-110 buildings; at least 75 % in blocks; main street 6-8 m; lanes 4-6 m; no straight run over 80 m on the main street or lanes; garrison 10-15; uneven frontages (cv at least 0.2).

## Causeway Foot (op 4, site 4-M3, platoon)

**Role in its op.** Main objective (platoon) of op 4 and the FOB for op 6. The road town where the north causeway lands on Ember Crescent: the only vehicle road onto the crescent runs through it. The garrison holds the causeway gate, the square at the fork and the upper road toward the monastery; the fuel point 560 m west-south-west (4-07) and the AA 710 m north-east (4-08) support it.

**Approaches.** Vehicles and infantry come up the causeway from the Cinder Cone (east-south-east). Boats land on the beach south of the town. From the west, the south-arm road (op 8's road) enters past the checkpoint 1 km away. The main street is the AI road: 8 m, gentle bends, no steep turns.

**Look.** Road town at the causeway landfall. The sci-fi core is the toll and signal pylon on the square, with the CIS gatehouse halls at the causeway end. White cubes line the bends of the 8 m main street, and domed corner houses sit at the fork. Black lava sand on the beach below.

**Plan (MEASURED on the plan).**
- Main street: 8.0 m wide, about ? m long, bent (longest straight run 48.0 m).
- 5 lanes, 4.5-6.0 m wide. Roads and paths out of town carry no frontage.
- Square: 985 m², with the sci-fi landmark **Causeway Signal Pylon**: sci-fi toll and signal pylon at the causeway landfall; its beacon lights the road for CIS convoys.
- 96 buildings, 94.8 % of them in 8 touching blocks. Street frontages are 6.2-14.7 m wide (spread cv 0.22, so not evenly spaced).
- Heights: low 35 / mid 46 / tall 15.

**Garrison (13 buildings).**

- H002 (tall, Naboo dome): holds the square and covers the landmark
- H007 (mid, white cube): main-street strongpoint (south-west of the square)
- H008 (mid, white cube): main-street strongpoint (south-east of the square)
- H011 (tall, sci-fi): depth position in the south-east blocks
- H016 (mid, white cube): main-street strongpoint (south-east of the square)
- H032 (tall, sci-fi): depth position in the west blocks
- H064 (tall, sci-fi): depth position in the north-east blocks
- H072 (mid, white cube): depth position in the west blocks
- H081 (tall, white cube): first contact: covers the Causeway (east-south-east) entry
- H084 (mid, Naboo dome): first contact: covers the Beach (south) entry
- H086 (mid, white cube): depth position in the east blocks
- H088 (mid, white cube): first contact: covers the South-arm road (west) entry
- H095 (tall, Naboo dome): first contact: covers the Slope road (north, to the monastery) entry

## Kamar Village (op 6, site 6-01, two-squad)

**Role in its op.** Supporting site (two-squad) in op 6. The beach village under the Prophet Massif: billets for the Kamar Strand garrison, and its quay is the boat landing for Signal Isle runs. The garrison holds the quay front and the houses over the beach lane, which look down on the Strand Bunker Line (6-M2) 700 m south.

**Approaches.** From the sea: the quay cove or the black beach to the south. From the land: up the beach lane from Kamar Strand, or down the ravine road from the massif (west).

**Look.** Ravine village above the black Kamar Strand. The sci-fi core is the Moisture Condenser Tower and the CIS billets on the quay. White cubes stack up the ravine bends, with domes on the corner houses. The pale limestone of the Prophet Massif rises behind.

**Plan (MEASURED on the plan).**
- Main street: 6.5 m wide, about 195 m long, bent (longest straight run 42.1 m).
- 5 lanes, 4.5-5.0 m wide. Roads and paths out of town carry no frontage.
- Square: 608 m², with the sci-fi landmark **Moisture Condenser Tower**: sci-fi condenser tower, the village's water; tall enough to read from Kamar Strand.
- 82 buildings, 93.9 % of them in 8 touching blocks. Street frontages are 6.5-14.8 m wide (spread cv 0.22, so not evenly spaced).
- Heights: low 22 / mid 48 / tall 12.

**Garrison (11 buildings).**

- H001 (tall, sci-fi): main-street strongpoint (west of the square)
- H014 (mid, sci-fi): main-street strongpoint (south-east of the square)
- H017 (mid, white cube): main-street strongpoint (south of the square)
- H028 (tall, sci-fi): first contact: covers the Quay cove (boats) entry
- H042 (tall, white cube): overwatch on the quay (east side)
- H049 (mid, white cube): first contact: covers the Ravine road (west, up the massif) entry
- H054 (mid, white cube): main-street strongpoint (south-west of the square)
- H056 (mid, white cube): first contact: covers the Lower lane (south-west) entry
- H057 (tall, sci-fi): holds the square and covers the landmark
- H074 (mid, white cube): first contact: covers the Beach lane (Kamar Strand, south) entry
- H080 (tall, sci-fi): depth position in the north-west blocks

## Kastro Quay (op 5, site 5-M3, platoon)

**Role in its op.** Main objective (platoon) of op 5 and the FOB for op 7's boat route. The lower town under the acropolis and the CIS supply port of the north: supply boats for the Yard load here. The garrison holds the quay and mole, the quay square under the port spire and the main street's upper bends toward the citadel.

**Approaches.** From the sea: boats across the Kastro Strait into the bay; the mole and quay are the front. From the island: down the citadel road from the west, along the ridge lane from the power station (south-west) or the north lane from the fuel depot and the east-bay landers.

**Look.** The biggest town in this pack. A harbour lower town: sci-fi warehouses and the Supply Port Control Spire on the quay square. White cube terraces climb the main street toward the acropolis, and domes cluster where the lanes leave the main street. The white pumice cliffs of Acropolis Isle are behind.

**Plan (MEASURED on the plan).**
- Main street: 7.0 m wide, about 184 m long, bent (longest straight run 53.8 m).
- 6 lanes, 4.5-6.0 m wide. Roads and paths out of town carry no frontage.
- Square: 820 m², with the sci-fi landmark **Supply Port Control Spire**: sci-fi port spire on the quay square: CIS cargo control for the north, its crown visible from the Kastro Strait.
- 108 buildings, 96.3 % of them in 9 touching blocks. Street frontages are 6.2-14.9 m wide (spread cv 0.25, so not evenly spaced).
- Heights: low 31 / mid 60 / tall 17.

**Garrison (13 buildings).**

- H006 (tall, Naboo dome): first contact: covers the Quay and mole (boats) entry
- H009 (tall, white cube): overwatch on the quay (south side)
- H014 (mid, white cube): main-street strongpoint (north of the square)
- H023 (tall, sci-fi): holds the square and covers the landmark
- H030 (mid, white cube): main-street strongpoint (north-west of the square)
- H046 (tall, sci-fi): overwatch on the quay (south side)
- H049 (tall, sci-fi): overwatch on the quay (north side)
- H065 (mid, sci-fi): depth position in the south-west blocks
- H081 (mid, white cube): first contact: covers the South lane entry
- H084 (mid, sci-fi): first contact: covers the North lane (fuel depot, east bay) entry
- H085 (mid, white cube): first contact: covers the Ridge lane (south-west, power station) entry
- H087 (mid, white cube): depth position in the west blocks
- H107 (mid, Naboo dome): first contact: covers the Citadel road (west, uphill) entry

## Lantern Quay (op 5, site 5-09, squad)

**Role in its op.** Supporting site (squad) in op 5. The beacon keepers' fishing hamlet on Lantern Rock; its quay is the only boat landing, so it is how players reach the Lantern Rock Beacon (5-M4) 460 m north-east. The garrison is a small picket in the quay front and the houses round the little square.

**Approaches.** Only by boat or air (Lantern Rock is 2.3 km off Acropolis Isle). Boats land at the quay; the main street climbs from it to the square and on to the beacon path.

**Look.** A small, tight fishing hamlet. One quay row, then a steep main street with the Beacon Relay Mast on a pocket square. Mostly white cubes with blue-green alien scrub between them. The sci-fi share is lower here on purpose (a civilian hamlet); the mast and the quay sheds carry the sci-fi read.

**Plan (MEASURED on the plan).**
- Main street: 6.0 m wide, about 187 m long, bent (longest straight run 68.1 m).
- 3 lanes, 4.0-5.0 m wide. Roads and paths out of town carry no frontage.
- Square: 685 m², with the sci-fi landmark **Beacon Relay Mast**: sci-fi relay mast that repeats the Lantern Rock beacon down to the quay.
- 66 buildings, 93.9 % of them in 7 touching blocks. Street frontages are 6.2-14.8 m wide (spread cv 0.2, so not evenly spaced).
- Heights: low 15 / mid 41 / tall 10.

**Garrison (10 buildings).**

- H001 (tall, Naboo dome): main-street strongpoint (north-east of the square)
- H004 (tall, sci-fi): depth position in the north-west blocks
- H010 (mid, white cube): main-street strongpoint (south-west of the square)
- H013 (mid, Naboo dome): main-street strongpoint (north of the square)
- H015 (tall, sci-fi): holds the square and covers the landmark
- H027 (tall, white cube): first contact: covers the Quay (boats) entry
- H031 (mid, white cube): depth position in the south blocks
- H050 (tall, white cube): overwatch on the quay (south side)
- H057 (mid, Naboo dome): first contact: covers the Beacon path (north-east) entry
- H060 (mid, sci-fi): first contact: covers the West shore lane entry

## Oyra (op 7, site 7-M2, platoon)

**Role in its op.** Main objective (platoon) of op 7. The north rim cliff town and the garrison of the North Narrows: the two Narrows batteries (7-M3 and its pair) are manned from here, and the rim trench (7-06) 580 m south-west links it to the Chora. The garrison holds the rim square under the signal lantern, the cliff-edge houses that overlook the Narrows and the two road entries.

**Approaches.** The lagoon side is a 300 m cliff: no way up except the lanes' end stairs, which are dead ends on purpose (look-outs, not routes). Players come along the crest road from the south-east (from the Chora or the monastery), down the north road from the Oyra Head landing, or along the rim from the Narrows batteries.

**Look.** Rim town on the caldera's inner cliff. White cubes and Naboo domes pour over the cliff edge toward the lagoon (the Santorini teacher, not a copy). The sci-fi core is the rim square with the Narrows Signal Lantern, CIS garrison halls beside it, and cliff-edge look-outs at the ends of the lanes. The town faces the lagoon and the North Narrows.

**Plan (MEASURED on the plan).**
- Main street: 6.5 m wide, about ? m long, bent (longest straight run 75.7 m).
- 6 lanes, 4.5-5.0 m wide. Roads and paths out of town carry no frontage.
- Square: 1236 m², with the sci-fi landmark **Narrows Signal Lantern**: sci-fi signal spire on the rim square, lighting the North Narrows for Yard traffic; seen from the lagoon and the Narrows.
- 106 buildings, 92.5 % of them in 8 touching blocks. Street frontages are 7.1-14.8 m wide (spread cv 0.22, so not evenly spaced).
- Heights: low 32 / mid 64 / tall 10.

**Garrison (13 buildings).**

- H003 (tall, sci-fi): main-street strongpoint (east of the square)
- H006 (tall, sci-fi): main-street strongpoint (south-east of the square)
- H015 (mid, white cube): main-street strongpoint (north-east of the square)
- H016 (mid, white cube): main-street strongpoint (south-east of the square)
- H030 (tall, sci-fi): holds the square and covers the landmark
- H034 (mid, white cube): main-street strongpoint (east of the square)
- H051 (tall, Naboo dome): overwatch on the cliff edge (south side)
- H082 (mid, white cube): first contact: covers the North road (Oyra Head landing) entry
- H085 (mid, white cube): first contact: covers the Rim path (Narrows batteries, west-north-west) entry
- H086 (mid, white cube): overwatch on the cliff edge (north side)
- H092 (mid, white cube): first contact: covers the Crest road (south-east, from the Chora and the monastery) entry
- H102 (mid, white cube): overwatch on the cliff edge (south side)
- H106 (mid, white cube): first contact: covers the East lane (outer slope) entry

## Sound Head (op 3, site 3-M3, platoon)

**Role in its op.** Main objective (platoon) of op 3 and the next FOB. The CIS boatyard town at the head of the Sound: crews and spares for the west-rim boats, the slips 450 m east-south-east (3-05), the fuel depot 670 m south-west (3-13). The garrison holds the quay front, the square under the control spire and the two upper lanes that look down the inlet.

**Approaches.** From the sea: up the Sound once the gate is blown (op 3 final), or by LAAT; the quay is the town's front door. From the road: the Notch road from the south-west past the fuel depot. From the hill: the path down from the Summit AA (north-west) and the farm lane from the west.

**Look.** Boatyard town. The quay front and the square are the sci-fi core: grey CIS slipway halls and the Boatyard Control Spire. Behind them, white cubes climb the slope in stepped blocks, and Naboo domes mark corners and the lane heads. The inlet's red-and-black banded cliffs frame the town from the sea.

**Plan (MEASURED on the plan).**
- Main street: 7.0 m wide, about 178 m long, bent (longest straight run 59.9 m).
- 5 lanes, 4.5-6.0 m wide. Roads and paths out of town carry no frontage.
- Square: 635 m², with the sci-fi landmark **Boatyard Control Spire**: sci-fi spire with a lit crown; the CIS boatyard's traffic control for the west rim, seen from the Sound mouth.
- 104 buildings, 96.2 % of them in 10 touching blocks. Street frontages are 7.1-14.5 m wide (spread cv 0.21, so not evenly spaced).
- Heights: low 26 / mid 64 / tall 14.

**Garrison (13 buildings).**

- H001 (tall, sci-fi): main-street strongpoint (south-west of the square)
- H006 (tall, sci-fi): main-street strongpoint (west of the square)
- H020 (tall, sci-fi): main-street strongpoint (east of the square)
- H042 (mid, white cube): first contact: covers the SW road (fuel depot, Notch road) entry
- H047 (mid, white cube): main-street strongpoint (south-east of the square)
- H053 (tall, white cube): first contact: covers the Quay (boats up the Sound) entry
- H054 (tall, sci-fi): holds the square and covers the landmark
- H064 (tall, sci-fi): overwatch on the quay (east side)
- H077 (mid, white cube): overwatch on the quay (east side)
- H084 (mid, sci-fi): depth position in the east blocks
- H085 (mid, sci-fi): first contact: covers the W lane (terrace farms) entry
- H090 (mid, sci-fi): overwatch on the quay (south-east side)
- H091 (mid, white cube): first contact: covers the NW path (Summit AA) entry

