# JOB_3 checks (rows K-a to K-f)

Method: rows K-a, K-c and K-d were counted by reading every `kit_*.json` (each part's walked / simple flags, levels of walked parts, and any part named "rock"). The other rows were counted against `KIT_SPECS_v1.md`.

| Row | Check | Target | Result | Tag |
|---|---|---|---|---|
| K-a | walkable parts flagged simple | 0 | 0 | MEASURED (kit JSONs) |
| K-b | decks with no ground-level way in by a vanilla ramp or stair | 0 | 0: K4, K2, K3, K5 each have a Land_RampConcrete_F from a +0.5 m bank; K6 and K9 are entered over ground | MEASURED (specs) |
| K-c | lowest deck level above sea level | >= +0.8 m | +1.7 m (every deck). The K2 boat step at +0.5 m is walked but is a boat step, not a deck (decision 9) | MEASURED (kit JSONs) |
| K-d | rock models used as a deck, roof or bridge | 0 | 0 | MEASURED (kit JSONs) |
| K-e | crossings without their own AI road line, clear width or boat clearance stated | 0 | 0 missing as statements. Two values are NOT MEASURED: the 3AS / vanilla bridge deck widths and the Fortress Dam crest width (the required 3.1 / 7.5 m is stated; the pieces' actual widths are not) | MEASURED (specs) |
| K-f | pieces without object, GP and sci-fi share counts | 0 | **5 pieces lack a true object count**: K2, K3, K4, K5, K8 (deck, wall and pillar counts wait on piece sizes read in the editor). **Sci-fi share by volume is NOT MEASURED** for K4, K5, K10; K5 is 75 % by count. GP counts are given for all ten | MEASURED (specs) |
