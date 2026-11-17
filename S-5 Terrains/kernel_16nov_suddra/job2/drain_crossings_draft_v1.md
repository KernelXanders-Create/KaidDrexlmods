# Drain crossings, draft v1 (ops 3-4, JOB_2 first part)

Built from decisions 11-15 in `DECISIONS.md`. Ground is the K3 sketch until drop 2 (Thu 19 Nov). Every length, level and depth that needs the drop-2 heightmap is NOT MEASURED.

| Crossing | Site | xy (K3 point, km) | Kind | AI route | Clear width | Second way | Boats | Length | Deck / crest level | Depth below | source |
|---|---|---|---|---|---|---|---|---|---|---|---|
| Drain Locks dam crest | 4-F (CIS Fortress Dam with GPs) | (10.39, 7.14) | dam crest (library comp) | armour | 7.5 m | not needed (not 3AS) | through the lock channel beside the dam, once 4-F is taken (player boats only) | NOT MEASURED | NOT MEASURED | NOT MEASURED (Drain at -1.5 m or deeper) | HUMAN (kind, armour, boats); AI (rest) |
| Drain Rail Bridge | 4-M2 | (8.20, 7.10) | 3AS bridge | armour | 7.5 m | armour: the Locks crest, 2.2 km east (MEASURED on K3 points); trucks: also the Plank Road causeway, 782 m (MEASURED on K3 points) | under the deck, if the clearance holds (NOT MEASURED) | NOT MEASURED | NOT MEASURED | NOT MEASURED (Drain at -1.5 m or deeper) | HUMAN |
| Plank Road Bridge | 4-06 | (7.59, 7.59) | earth causeway with a plank-road surface (a designed straight) | trucks | 3.1 m | not needed (not 3AS) | cannot pass | NOT MEASURED | NOT MEASURED (at +0.5 m or higher, rule 37) | NOT MEASURED | HUMAN |

## Water
| Water body | Depth band | Note | source |
|---|---|---|---|
| The Drain, whole length | boat channel, -1.5 m or deeper | infantry must swim; AI cross only at the three crossings | HUMAN |
| Lock channel beside 4-F | boat channel, -1.5 m or deeper | scripted gate, shut until 4-F is taken, then open to player boats; no AI boats | HUMAN |

## Reaches (ASSUMED from the K3 point order, west to east)
1. West of the Plank Road causeway: closed to boats from the east.
2. Middle, from the causeway to the Locks: holds the Rail Bridge; boats reach it through the lock once 4-F is taken.
3. East of the Locks: the Barge Quay (4-M4, 12.39 km) reach.

## Open items
- **Fortress Dam crest:** is the CIS Fortress Dam's authored crest 7.5 m clear? NOT MEASURED. If it is narrower, the armour route over it fails rule 31; flag it (no invented access, rule 22).
- **Rail Bridge clearance:** the 3AS deck height over -1.5 m water, and whether boats fit under it. NOT MEASURED.
- **3AS deck under AI armour:** UNSURE until your convoy test. If it fails, armour crosses only at the Locks.
- **Lock gate script:** what opens it (4-F captured) is a mission item, not ground. Listed in the notes.
