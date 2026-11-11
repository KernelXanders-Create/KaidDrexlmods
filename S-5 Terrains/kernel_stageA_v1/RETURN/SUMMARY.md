# Kernel Stage A: summary for Miran

Everything here is **PROPOSED**. The sketches are for choosing, not for approval, and nothing goes in game without your look.

## Islands (1st Company): pick one
- **A Pillar Reach:** a drowned karst sea of tower islets and lagoons. The big island is a ring of towers around a hidden bowl with a droid foundry inside, walls plug its notches. Best at: the "wild island hides a facility" feel, beach landings, and broken sight lines (hundreds of towers). Risk: tower dressing cost and the distant read of towers.
- **B Ember Chain:** a cold volcanic chain of black beaches, sea cliffs and a sound, ending in a flooded caldera with a CIS shipyard behind a dammed breach. Best at: vehicle routes (causeways), cliff walls in notches, and a west-or-east branching front. Risk: long sight lines from 500 m peaks.
- **C The Shallows:** an atoll with wading reef flats, stilt towns over the lagoon, and an overgrown "ridge" that is really a crashed Separatist capital ship turned foundry (Mon Cala). Best at: wading and Navy play, and a unique set piece. Risk: flat and exposed, and the most stilt decks (AI fall-through risk).

**My recommendation: A**, because it's the closest to the brief's feel, with several distinct islands and a hidden-facility payoff. B is a strong second if you want more vehicles.

## Swamp (2nd Company): pick one
- **A The Mire Line:** a Mimban trench war across a cratered peat bog: three trench belts, a flooded orbital crater with a stilt refinery, and a moraine citadel. Best at: an AI-friendly static defence and a visible front. It differs from Blackfen on all 5 counts. Risk: AI stalling in craters, and trench object count.
- **B The Glow:** a bright Felucia "river of grass" with fungal hammocks and a giant fallen stalk (the Felled Titan) lying across the main slough, with a lab inside its trunk. Best at: a striking look and route choice. Risk: grass versus AI sight, and the Titan is a new build.
- **C River Country:** Rodia. One great river with levee roads, a stilt refinery in an oxbow, a tiered river city and a foundry upstream. Best at: Navy and armour, and a real city. Risk: AI convoys on narrow levees, and the river splitting the map.

**My recommendation: A.** It is the most distinct from Blackfen and the least dependent on AI in water. C if command wants vehicles and the Navy.

## Questions that change the design (defaults in QUESTIONS.md)
1. Can droids ever cross water? (Default: never.)
2. 6 ops or 4? (Default: 6.)
3. Which boats, landing craft and hovers does the modset really have?
4. Does our sea level move (tides)? Test before Stage B.
5. Is a trench war right for 2nd Company? (Swamp A.)

## What I measured vs assumed
**MEASURED** (computed by `tools/make_all.py` on the sketch height fields):
- island areas;
- gap lengths and min/max depths along sample lines;
- objective counts and size mix per op;
- house-rule checks per op (10-20 sites, all three sizes, 1-2 air-prep, at most 2 air-only, at least 1 tunnel site). All 36 ops pass (`tools/out/validation_all.txt`).

**ASSUMED:**
- all landform layouts and sketch heights (hand-placed design, not real data);
- objective positions (hand-placed, then snapped to sketch land);
- recon distances, garrison counts and ways-in (rules of thumb);
- build costs;
- mod contents (I only had mod names);
- every engine behaviour. **No Arma tests were run** (no Arma 3 available here). TESTS.md is therefore omitted, and the tests are proposed in each RISKS.md.

Reference links were written from memory and not re-checked this session.
