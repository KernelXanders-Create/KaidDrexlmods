# Islands concept A: Pillar Reach (PROPOSED)

**Pitch:** A drowned karst sea of towers, lagoons and hidden basins. The biggest island is a ring of limestone towers around a dry bowl, and the CIS have a droid foundry inside it.

## Setting
An original tropical ocean world in the Scarif mould: white sand, turquoise lagoons, jungle-capped towers. It is not canon Scarif, because the famous base there is Imperial-era. A tropical palette (bright sun, green and turquoise) is the opposite of Blackfen's violet night.

## Landform story
A limestone plateau sank and the sea flooded it. Rain dissolved the rock along cracks, leaving:
- towers (the Mushroom Field and the north karst field);
- **hongs**: cave chambers whose roofs fell in, now open lagoons inside tower islands (the Twin Hongs);
- one huge collapsed cave system, **the Crown**: a ring of towers 250-390 m high around a dry bowl (doline floor at about +25 m), with three natural notches in the ring.

Waves cut an undercut notch at the waterline, which makes the "mushroom" islets. Sand gathers on the lee sides into beaches and one long **sandbar** linking Landing Key to Market Isle. A fringing reef wraps the Crown's south shore.

## Signature set piece: the Crown
From the sea, the Crown looks like a wild jungle massif. Inside the ring sits a CIS droid foundry: multi-level halls built against the inner cliffs, with walls plugging the three notches. Walls in notches of a continuous cliff were a loved feature on our past maps, and this puts them on a ring around a hidden bowl.

**How players find it** (recon payoffs, no forced order):
1. Traffic logs at the Gun Tower summit (op 3).
2. Power pylons across the reef from the Hongs (op 4).
3. An exhaust plume rising from the bowl, visible from the Gun Tower ridge.

**Ways in (5):**
1. The south notch gate (the vehicle way).
2. The west notch wall.
3. The east cliff lift.
4. Ring gallery tunnels.
5. An air drop into the bowl once the rim AA is down.

All of them are above ground: the interiors are shells set into the ring (04: no underground).

## Op flow (6 ops, 3 weekends). Front: south-west to north-east.
| Op | Start | Area | Main objectives | End state | Front moves |
|---|---|---|---|---|---|
| 1 Beachhead | Fleet offshore, SW | Landing Key + south lagoon | Reef Battery, Landing Key Village (P), Burrow Knoll tunnels, Shore AA | Key held | FOB on Landing Key |
| 2 The Lagoon | Landing Key FOB | Mushroom Field, sandbar, Market Isle south | Pillar Stilt Town (P), Great Pillar Hollow, Market Port (P), Harbour Mole Battery | Lagoon and port held | FOB to Market Port |
| 3 Western Guns | Market Port | Gun Tower Isle + Wreck Reef | Ridge AA North (P), Cliff Gallery, Frigate Hulk (P), Summit Signal Station (intel) | West AA silent; air lanes open | FOB stays; air FARP on the ridge |
| 4 Hongs and Crown Shore | Market Port | Twin Hongs, cays, Crown south beach | Hong Boat Pens, East Hong tunnels, Crown South Beach (P), Reef Obstacle Line | Second beach assault succeeds | FOB on the Crown south beach |
| 5 The Ring | Crown beach FOB | Outer ring of the Crown | South Notch Gate (P), West Notch Wall, Ring Gallery Tunnels (P), Rim AA | Two or more ways into the bowl open | FOB at the south notch |
| 6 Into the Crown | South notch | The bowl and foundry | Foundry Main Hall (P), Assembly Line Hall (P), Service Tunnel Maze (P), Generator Core | Foundry destroyed | End of run |

Each op has 11-12 sites, mixing squad, two-squad and platoon sites, with 1 air-prep, 0-1 air-only and at least 1 tunnel site (MEASURED by `tools/make_all.py`; see `tools/out/validation_all.txt`). Every op has extra main objectives, so command can bypass 1-3 of them.

## Movement
- **Infantry:** walks the islands. Wades the sandbar (about -0.5 m), the Wreck Reef flat (about -0.7 m) and the Crown's south reef (about -0.8 m).
- **Boats:** all the deep gaps (-4 to -40 m) and the lagoon (about -4.5 m between the pillars).
- **LAAT/air:** everywhere once the AA is down. The Gun Tower AA covers the west, the Hong comms dish the east, and the rim AA the bowl.
- **Vehicles:** only on Landing Key, Market Isle, the Crown's outer slopes and the bowl floor (via the south notch). Light vehicles cross by sling or landing craft (needs a test, see Q list).
- **Gap depths:** the table below is MEASURED on the sketch. Widths are along the straight sample line.

<!-- AUTO-MEASURED START -->
**MEASURED on the sketch height field** (16 m cells; built by `tools/make_all.py`; the sketch is itself ASSUMED design):

| Island (sketch) | Area km² |
|---|---|
| Landing Key | 5.5 |
| Market Isle | 8.9 |
| Gun Tower Isle | 8.2 |
| The Crown | 25.9 |
| Twin Hong W | 1.8 |
| Twin Hong E | 1.1 |
| Wreck Reef motu | 0.8 |
| Cay 1 | 0.2 |
| **All land above 0 m** | **57.2** |

| Gap / route | Line length m | Water along it m | Deepest m | Shallowest m | Crossed by |
|---|---|---|---|---|---|
| Landing Key -> Market Isle (sandbar) | 3089 | 1640 | -0.6 | -0.0 | wade the sandbar; boats either side |
| Landing Key -> Gun Tower Isle | 2907 | 2739 | -17.9 | -0.0 | boat / air |
| Market Isle -> Gun Tower Isle | 2059 | 328 | -0.3 | -0.0 | boat / air |
| Market Isle -> Twin Hongs | 2879 | 1700 | -26.9 | -0.0 | boat / air |
| Market Isle -> Crown via cays | 2900 | 2580 | -39.1 | -0.0 | boat hop via cays / air |
| Twin Hongs -> Crown south reef | 3400 | 2776 | -34.6 | -0.0 | boat, then wade the reef flat |
| Gun Tower Isle -> Wreck Reef | 1803 | 1779 | -23.6 | -0.2 | boat, then wade the reef |

Objective sites: 71 over 6 ops (squad 27, two-squad 33, platoon 11). Highest point 390 m; deepest -53 m.
<!-- AUTO-MEASURED END -->

Note: the sketch shows a shallow shelf (about -0.3 m) between Market Isle and Gun Tower Isle, which makes it a wadeable link. Keep it as a route, or deepen it to keep the islands separate? (QUESTIONS Q6)

## Why it's distinct
- **vs Blackfen:** daylight tropical palette, vertical rock in place of flat delta, and a front that hops island to island.
- **vs Aparra:** no temperate forest or gorge. Here the "gorge" is a ring of towers around a bowl.
- **vs Sarrak:** wet, green and vertical.
- **vs B and C:** A is the most vertical and has the most broken sight lines (hundreds of towers). B is cold volcanic with big single islands. C is flat reef and wading.

## Biggest risk
**Karst towers read as blobs at 2-6 km.** The undercut can't be done in the heightmap, and 4 m terrain cells soften steep towers. Steep faces need dense, seated cliff objects (a HARD house rule), and there are hundreds of towers.

**Early check:** in Stage B, build one 1 km² test tile with 10 towers at 4 m and look in-game at 0.5, 2 and 4 km. Count the objects per tower.

## Rough build cost (ASSUMED)
- **New comps:** 1 (the foundry bowl interior, a big one).
- **Reused:** stilt towns from library pieces, beach defences, batteries, AA sites.
- **Special terrain work:** the tower field (hundreds of rock clusters, the most dressing of the three concepts) and the ring notch walls.
- **Effort:** highest of the three for terrain dressing; medium for comps.
