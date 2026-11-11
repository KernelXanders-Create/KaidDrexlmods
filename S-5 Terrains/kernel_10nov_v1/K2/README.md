# KERNEL_RETURN_10NOV_K2: briefing and story pack, Islands ops 3-8 (PROPOSED)

Job K2 from the 10 Nov work pack. Drafts for Zeus and command to edit, not final text.

## What is in this zip
| File | Op | Week |
|---|---|---|
| `ops/OP3_THE_SOUND.md` | 3 The Sound | 2 |
| `ops/OP4_CINDER_ROAD.md` | 4 Cinder Road | 2 |
| `ops/OP5_ACROPOLIS_ISLE.md` | 5 Acropolis Isle | 3 |
| `ops/OP6_PROPHET_MASSIF.md` | 6 Prophet Massif and Signal Isle | 3 |
| `ops/OP7_THE_RIM.md` | 7 The Rim | 4 |
| `ops/OP8_CALDERA_YARD.md` | 8 The Caldera Yard | 4 |

Each file has three parts:
1. **A one-page briefing** in a plain military voice: Situation, Mission, Command chooses, Getting there, After the op.
2. **A 5-line Zeus brief:** what the enemy holds, where the reserve comes from, and what must not happen.
3. **3-5 history lines,** picked by the result of the op before. Each line says which result it belongs to.

## How it follows the purpose map and house rules
- **Win rule:** the final plus any 2 of the 4 mains, taken from the purpose map. Every briefing lists the 4 mains and what each one gives, so command chooses.
- **No landing zones and no forced order** in any briefing. Where an op can be reached several ways (ops 7 and 8), all of them are listed and command picks.
- **Zeus lines carry the hard rules:**
  - droids never cross water;
  - reserves spawn 250-400 m out, unseen, on the enemy side of the same landmass;
  - guns are targets only, with no scripted artillery;
  - the AI budget is 1,200 alive. Each op's planned garrison, if every site filled at once, is quoted from the purpose map (855-1,005).
- **History lines are keyed to real stakes** in the purpose map. Examples: op 1's Vent Field Radio gives "first intel on the Yard", op 2's Control Tower gives "the Yard's frigate schedule", op 4's East Slope Comms gives "intel on the Yard's shifts". So taking or skipping a supporting site changes the next op's story.
- **Canon:** Clone Wars era, CIS droids only. No named enemy characters, no Imperial-era terms. The fleet ships named are the purpose map's Acclamator plus one Venator† mention; both are Clone Wars Republic ships.

## What I invented († in the files)
Everything else in the briefings is from PURPOSE_MAP.md v2 and objectives_v2.json. These are mine; cut any of them freely:
- **Op 3:**
  - the Acclamator landing boats at Perys overnight;
  - supply boats leaving the Sound every night.
- **Op 4:**
  - engineers sweeping the first causeway leg for mines;
  - frigate hulls moving every few days;
  - droid convoys fuelling on the cone;
  - the CIS pulling guns east to the cone.
- **Op 5:**
  - "that is why it is so heavily held";
  - frigate tugs using the Lantern Rock beacon.
- **Op 6:** the Yard's crews changing at the Rim Chora at dusk (a detail invented to dress the purpose map's "intel on the Yard's shifts").
- **Op 7:**
  - the Venators closing on the caldera;
  - the dusk shift change at the Chora, and half the garrison being on the Skala path.
- **Op 8:** "tonight".

## Not done
- No briefings for ops 1-2. The pack asked for ops 3-8.
- No mission timing, weather, radio frequencies or call signs. I left them out rather than invent them.
- No slide images or maps per briefing. The purpose map's plan_v2.png is the map to use.

## Open questions (with the default I used)
1. **Results to track.** The history lines need Zeus to record a few results per op: final taken, which mains fell, and 1-2 named supporting sites such as the Vent Field Radio, the Control Tower, the East Slope Comms and the Lantern Rock Beacon. **Default:** a short checklist per op is enough. Tell me if you want it as a JSON for the mission files.
2. **Ops that follow "any of" several earlier ops** (7 and 8) get lines for each possible source, and Zeus reads the ones that match. **Default:** read 3-5 lines that apply, not all.
3. **Signal Isle battery fire** is story only: it fires at the fleet, never at players. **Default:** yes, per the no-scripted-artillery rule.
4. **The Yard Power Plant also feeds the Kameni shield** (this is in the purpose map). **Default:** Zeus may drop the shield when the plant blows, but only by choice. The briefing lists the generator as the main way to drop it.

## Measured, assumed, unsure
- **Quoted as MEASURED in the purpose map:** distances and channel widths, site counts and planned garrisons.
- **ASSUMED in the purpose map:** boat and air times. I kept the purpose map's own labels.
- **My own:** the voice and wording of every briefing, the reserve directions in the Zeus briefs (read from the site layout, ASSUMED), and the † items.
- **Unsure:** whether your Zeus team wants the Zeus brief longer than 5 lines for the bigger ops (3 and 8 have 21 and 18 sites).
