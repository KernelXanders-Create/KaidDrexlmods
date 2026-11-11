# KERNEL_RETURN_11NOV_C_JOB3_v1: briefings for ops 1 and 2 (Saturday 14 Nov)

| File | What it is |
|---|---|
| `OP1_BLACK_STRAND_v2.md` | Op 1 (13:00 US Eastern): player briefing, 5-line Zeus brief, opening line, and the results Zeus records for op 2. |
| `OP2_AIRFIELD_TERRACE_v2.md` | Op 2 (20:00 US Eastern): player briefing, 5-line Zeus brief, and 5 history lines keyed to how op 1 ended. |

I did job 3 first: it is the only job with a date this week. Jobs 1 and 2 (ground plans for ops 3-8, then the towns on the map) come next, starting with ops 3 and 4.

## What I changed from your drafts
- **Site names, counts, sizes and every measured figure are kept.**
- **Your dagger lines are replaced:**
  - the op 1 and op 2 "smaller positions" lines are rewritten from `pads_op1.json` / `pads_op2.json`, so each claim is now checked (below);
  - the op 2 Summit Crater history line is replaced;
  - the op 1 opening line is replaced.
- **Where I invented a line, it is marked †:**
  - the op 1 opening line;
  - op 2's Ash Field Depot history line ("the same freighters").
- **"Optional" is gone:** the op 1 opening line is now just "Opening line". Nothing in either file is called optional.
- **Checked against your bans:**
  - CIS battle droids only (no other unit types named);
  - no scripted artillery (the mortars and the cliff guns fire only at a Zeus's hand);
  - no recon smoke;
  - no jammer objectives (the comms array and the Radar Point are a squad position and a destructible site, not jammers);
  - no LZs, no order.
- **Op 1 now ends with four results for Zeus to record.** Op 2's history lines are keyed to those four.

## Checked against the pads files (MEASURED)
- **Counts:** op 1 has 19 sites (17 pads plus Perys and the air-only sensor stack) and 10 squad positions. Op 2 has 18 sites and 15 positions. Both match your drafts.
- **Op 1 squad positions:** each one stands where your draft says.
  - **Heavy guns:** A1-01 and A1-02 behind the bunker line (189 m and 100 m); A1-04 by the gun pits (237 m); A1-05 by the turret bunkers (290 m); A1-06 by the West Cove landers (381 m); A1-10 by the North Strand AA (324 m).
  - **Summit AA platform:** A1-07, 188 m from the summit flak.
  - **Comms array:** A1-03, 301 m from the fuel farm.
  - **Checkpoints:** A1-09 on the Perys road, 371 m from the v4 square; A1-11 on the crater road, 115 m from the Crater Road Checkpoint.
  - Distances here are to the nearest pad. They differ a little from your 115-381 m (for example, A1-09 is 643 m from the nearest pad but guards Perys), so the briefing uses your figures.
- **Op 2 squad positions:**
  - **Claus forts:** A2-04, 216 m from the West Terrace AA, and A2-13, 400 m from the East Terrace AA.
  - **Star bastions:** A2-09, 405 m from the airbase, and A2-02, 295 m from the cliff stair.
  - **Gun Keep:** A2-12, 257 m from the fuel farm.
  - All 15 positions are 120-405 m from their nearest site, as your draft says.

## Things I noticed in the data (for you to check, not changed in the briefings)
1. **Several built pieces differ from the purpose map's library picks.** The names players see stay right, but some site descriptions may not match what is built:

   | Site | Built as | Purpose map pick |
   |---|---|---|
   | Geothermal Plant (op 1) | CIS Chemical Plant | Large Power Facility |
   | North Strand AA (op 1) | Mixed AA Platform | Covered AA Base |
   | Shield Pylon Ridge (op 1) | Flower Tower | — |
   | Lighthouse Cape (op 1) | Medium FOB | — |
   | Rib Turret Bunkers (op 1) | Small Citadel | — |
   | East Terrace AA (op 2) | Flower Tower 2 AA | — |
   | Revetment Bunkers (op 2) | Small Citadel | — |
   | Wreck Cove (op 2) | Medium FOB | Falling Lander Fixed |
   | Radar Point (op 2) | Comms Array | Giant Radar Dish |

   The last two matter most. **Radar Point is built as a comms array, not a radar dish**, so the briefing's "blinds the airbase's early warning" needs a dish players can see, or the line changes. **Wreck Cove is built as a Medium FOB, not the Falling Lander**; your Zeus line 4 still describes the falling lander, so check it is placed.
2. **The Claus fort ramps:** your first question (the 0.52 / 0.96 / 0.40 m ramp joints) is exactly the risk at A2-04 and A2-13. Op 2's Zeus line 3 now asks for a walk test before the op, and says what to tell players if it fails.

## Not done in this zip
- Jobs 1 and 2, and the three spare-hour questions. Jobs 1 and 2 are next.
