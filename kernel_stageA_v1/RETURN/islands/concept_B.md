# Islands concept B: Ember Chain (PROPOSED)

**Pitch:** A cold volcanic island chain of black beaches, sea cliffs and a sound. At the end is a flooded volcano whose crater hides a CIS shipyard, and the only way in by sea is a dammed breach in the rim.

## Setting
An original volcanic ocean world with Ahch-To / Faroe / Azores looks: grey-green grass on steep slopes, black sand, white surf, low cloud on the peaks and steam vents. I use an original world rather than Ahch-To because Ahch-To is a sacred Jedi site and it shouldn't host a droid base. The palette (cool grey, green and black) is unlike Blackfen's violet, Aparra's orange autumn and Sarrak's tan desert.

## Landform story
The islands sit on a volcanic arc running south-west to north-east:
- **Black Strand:** an old, low **shield volcano**. Lava ran into the sea and froze into ribs that cross the black beach.
- **Stack Garden:** waves cut a rock platform and left **stacks and arches**.
- **Airfield Isle:** a raised **marine terrace**, flat-topped.
- **Fjord Isle:** tall (about 400-530 m on the sketch). A glacier once carved a **sound** through it, and sea cliffs ring it, cut by gullies (notches).
- **Pumice Shoals:** tephra ash washed into a wadeable bar.
- **The Caldera:** the youngest volcano blew its top off, and the sea flooded the crater through a **breach** on the south-west side (like Deception Island).
- **Causeways:** the Separatists linked the Airfield to the Caldera's south foot with causeways via a **cinder cone** islet.

## Signature set piece: the Caldera Yard
The flooded crater is about 3 km across and -30 m deep (sketch). It holds a CIS shipyard:
- a frigate in dry dock;
- slipway cranes over the water;
- a foundry built into the inner rim terraces;
- a dam with a gate across the breach.

Players see the steam and the rim but not the yard until they crest the rim or take the dam.

**Ways in (5):** the dam gate (boats, after op 5), the south flank tunnels, the rim road from the causeway town, the rim tunnel maze, and an air drop once the rim AA and shield pylons are down.

A second set piece is the **Fjord Isle cliff walls**: walls plug two gullies in a continuous sea cliff. We know that feature is loved.

## Op flow (6 ops, 3 weekends). Front: south-west, then branching north or east, meeting at the Caldera.
| Op | Start | Area | Main objectives | End state | Front moves |
|---|---|---|---|---|---|
| 1 Black Strand | Fleet offshore, south | Black Strand | Strand Bunker Line (P), Lava Rib Gun Pits, Lava Tube Shelters, Geothermal Plant | Island held | FOB in Ash Village |
| 2 Stacks and Airfield | Ash Village | Stack Garden + Airfield Isle | Arch Gate Fort, Airfield Runway (P), Hangar Row, AA West and East | Airfield held | FOB and air FARP on the airfield |
| 3 Fjord Fortress | Ash Village (north) | Fjord Isle | South and West Notch Walls (P), Sound Boom Gate, Sound Head Town (P), Cliff Galleries (P) | Sound open to boats | FOB at the sound head |
| 4 Shoals and Crags | Sound head | Pumice Shoals, Northern Crags, Caldera west flank | Shoal Pillboxes, Crag Research Station (P), Breach Watch Battery | West flank foothold | FOB on the shoals' east end |
| 5 Cinder Road and Breach | Airfield | Causeways, Cinder Cone, Caldera south foot, dam | Cinder Cone Fort (P), Breach Dam Gate (P), Dam Turbine Hall, South Flank Tunnels | Dam held, gate open | FOB at the Caldera foot town |
| 6 Inside the Caldera | South rim | Crater lake and yard | Dry Dock Alpha (P), Rim Foundry Shell (P), Rim Tunnel Maze (P), Shield Generator | Yard destroyed | End of run |

**Branching:** ops 3-4 (west) and op 5 (east) can run in either order, because both reach the Caldera. That gives command a real choice without lanes.

## Movement
- **Infantry:** wades the wave-cut platform to the Stack Garden (about -2 m deep at worst, so a short swim) and the Pumice Shoals (about -0.6 m). Walks the causeways.
- **Vehicles:** the causeways (Airfield → Cinder Cone → Caldera foot) are this concept's tank route. These are the most vehicle-friendly islands of the three concepts.
- **Boats:** the sound (about -20 m; the boom gate starts closed), all island gaps, and into the caldera via the breach (-18 to -34 m) only after the dam gate opens.
- **Air:** cliffs and peaks make LZs scarce on Fjord Isle. The terraces, the airfield and the beaches are the natural ones.
- **Gap depths:** see the MEASURED table below.

<!-- AUTO-MEASURED START -->
**MEASURED on the sketch height field** (16 m cells; built by `tools/make_all.py`; the sketch is itself ASSUMED design):

| Island (sketch) | Area km² |
|---|---|
| Black Strand | 9.6 |
| Airfield Isle | 4.1 |
| Fjord Isle | 8.8 |
| The Caldera | 21.0 |
| Cinder Cone | 0.8 |
| Northern Crags | 3.6 |
| **All land above 0 m** | **49.0** |

| Gap / route | Line length m | Water along it m | Deepest m | Shallowest m | Crossed by |
|---|---|---|---|---|---|
| Black Strand -> Stack Garden | 728 | 536 | -2.0 | -0.0 | wade/boat over the wave-cut platform |
| Black Strand -> Fjord Isle | 2147 | 1402 | -27.1 | -0.0 | boat / air |
| Stack Garden -> Airfield Isle | 1140 | 586 | -9.9 | -0.1 | boat / air |
| Airfield -> Cinder Cone (causeway) | 850 | 0 | 0.0 | 0.0 | causeway: foot and vehicles |
| Cinder Cone -> Caldera (causeway) | 1530 | 0 | 0.0 | 0.0 | causeway: foot and vehicles |
| Fjord Isle -> Caldera (Pumice Shoals) | 2247 | 706 | -0.6 | -0.0 | wade the tephra bar |
| Fjord Isle -> Northern Crags | 2419 | 2403 | -59.7 | -0.0 | boat / air |
| Breach channel (into caldera) | 1872 | 1872 | -34.5 | -18.0 | boats only; dam gate |

Objective sites: 69 over 6 ops (squad 22, two-squad 36, platoon 11). Highest point 534 m; deepest -69 m.
<!-- AUTO-MEASURED END -->

## Why it's distinct
- **vs Blackfen:** cold daylight, black and green, big relief, open sea.
- **vs Aparra:** no forest canopy. Grass and rock, long views.
- **vs Sarrak:** wet and steep. It has a caldera, not canyons.
- **vs A and C:** B has fewer, bigger islands, real vehicle routes on causeways, and the highest relief. Its sight-line answer is bulk: tall islands block each other.

## Biggest risk
**Long sight lines.** Big bare islands and open sea mean a sniper on the Fjord Isle summit (about 500 m up) sees most of the map. Grass slopes are also exposed for infantry.

**Mitigations:**
- low cloud and haze on the peaks (mission weather);
- gullies and lava ribs as micro-terrain;
- the Caldera rim hides the yard;
- the Fjord Isle summit AA objective doubles as a "take the high ground" payoff.

**Early check:** in Stage B, render the view from the Fjord summit at our view distance, and test the haze settings in-game.

## Rough build cost (ASSUMED)
- **New comps:** 1 (the Caldera yard: dry dock, cranes, dam).
- **Reused:** airfield pieces, batteries, cliff walls (already in our library from earlier maps).
- **Terrain work:** cliff dressing on Fjord Isle and the rim (heavy), lava ribs and stacks (medium).
- **Effort:** medium-high.
