# SUDDRA_KERNEL_RETURN_JOB3: the water and stilt kit (draft v1)

Ten pieces specced from 25 decisions, all yours (`DECISIONS.md`, source HUMAN). Where I filled in a detail you did not choose (positions, spacing, sizes), the spec says AI.

**What blocks it from being final:**
- **Class names:** I could not see class names inside the mods. Every part names its mod or vanilla family and is marked "to confirm" (UNSURE). Only Land_RampConcrete_F (from the brief) and the library comps are named exactly.
- **No engine tests:** I have no Arma 3 with the live modset, so there is no `TESTS.md`. Every AI walk and drive claim is UNSURE until your W2-W5.
- **Row K-f fails:** five pieces (K2, K3, K4, K5, K8) have no true object count until the piece sizes are read in the editor; sci-fi share by volume is NOT MEASURED.

| Piece | In short |
|---|---|
| K1 boat landing | a graded beach, -1.5 to +0.5 m at 1:6, no objects |
| K2 pier 10 / 25 / 50 m | concrete, 4 m, deck +1.7 m, walls both sides, boat step at +0.5 m + ramp; the 50 m ends in an 8 x 8 m head with a CIS Turbolaser Tower |
| K3 boardwalk | the K2 deck as a walkway: 10 m segments, 8 x 8 m junction, end ramps |
| K4 stilt deck 15 / 30 m | concrete at +1.7 m, pillars, solid low walls, one ramp; small: sci-fi hut + 6 GPs; large: 12 GPs, centre clear for a comp |
| K5 stilt hut cluster | large K4 (2 huts) + 2 small K4s (1 hut each) on K3 links; 3 sci-fi + 1 real-world hut; 26 GPs |
| K6 boat pen | a sci-fi hangar over an 8 x 20 m slot at -1.5 m in a +2.5 m bank; ground walkway at +0.5 m, 4 GPs |
| K7 barges | vanilla wreck hulls (simple) with fuel tanks (NORMAL, burnable); not walkable |
| K8 crossings | 3AS bridge + vanilla/CUP fallback, 3.0 m boat clearance; causeway truck (6 m) and armour (12 m) at +1.0 m; Fortress Dam crest |
| K9 reed-mound AA nest | a CIS Heavy Gun Position + AA (UD) on a +1.5 m mound, ground ramp in |
| K10 pier checkpoint | a CIS Small Checkpoint with GPs astride a causeway road or on a widened pier |

| File | What it is |
|---|---|
| `KIT_SPECS_v1.md` | all ten pieces, sections 1-10 each |
| `kit_<piece>.json` | parts with positions relative to the piece origin, levels, normal / simple flags, GPs |
| `kit_<piece>.png` | plan (north up, scale bar) and side view |
| `JOB_3_checks.md` | rows K-a to K-f |
| `DECISIONS.md` | every choice, options shown and the pick |

**First tests I would run:** W3 (AI on the concrete pier deck at +1.7 m), W4 (the 3AS bridge under a truck and a tracked vehicle), then placing the K6 hangar over water and the K10 checkpoint's passage width in the editor.
