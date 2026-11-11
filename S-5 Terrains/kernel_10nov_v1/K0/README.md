# KERNEL_RETURN_K0: how K1 was made, and a hard look at Perys v4

| File | What it is |
|---|---|
| `K0_METHOD.md` | The answer to all six K0 questions: the K1 method with its exact parameters, what I'd change for real models and pads, a ranked critique of v4 (ten items, each with a fix and a measurable rule), which of your rules I'd loosen, a 15-check list, and the working loop |
| `figures/v4_bare_edges_and_pad_levels.png` | v4 over the natural ground. Red dots mark street edges with no building within 2 m; pads are coloured by level (5 levels for 93 buildings) |
| `tools/analyse_v4.py`, `tools/v4_measures.json` | The read-only script that measured v4 from your pack files, and its output. Read it as text; no need to run it |

**Headline (measured):**
- In K1, the building footprint is 3.1-3.9 times the street area, with 41-51 % ground cover. In v4 it is 0.95 times, with 23 % cover.
- v4 also has: 0 % street wall on every lane; 93 % of doors within 2° of square-on to their street; a median 0.72 m gap between houses; 5 pad levels; an empty square (7.9 % comp cover) with its landmark 75 m away.

**Not done:** three of the 15 checks (2, 7, 9) were not computed for v4. All thresholds are my judgement and should be calibrated on a town Miran likes.

**Questions:**
1. Can the main street climb at up to 8 % where it is not the AI convoy road? The critique and my K5 plan lean on this.
2. Are ND01 and ND02 visual twins in game? I assumed so (same size and look in the catalogue).
