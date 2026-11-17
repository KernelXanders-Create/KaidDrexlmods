# Suddra JOB_3 (water and stilt kit): decisions log

Each row is one design choice: what was asked, the options shown, the pick, and who chose it (HUMAN = Kernel; AI = suggestion not reviewed).

| # | date | question | options shown | pick | source |
|---|---|---|---|---|---|
| 1 | 17 Nov | K4 stilt deck: what the walkable deck is built from | (a) vanilla concrete pier sections; (b) Tanoa wooden pier platforms; (c) modset sci-fi plates (3AS / Legion / JM's) | (a): vanilla concrete pier sections, NORMAL objects. Exact class names to confirm in the editor (UNSURE); AI walk UNSURE until test W3. Sci-fi share comes from the pieces on the deck. | HUMAN |
| 2 | 17 Nov | K4 deck level and ground-level way in | (a) +1.0 m, a 0.5 m step from a +0.5 m bank; (b) +1.7 m, one vanilla concrete ramp (1.2 m rise); (c) +2.9 m, two ramps with a landing | (b): deck at +1.7 m above sea level; way in by one Land_RampConcrete_F, 1.2 m of rise from a +0.5 m bank (inside the 1.08-1.40 m band). Freeboard 1.7 m at calm sea (wave swing NOT MEASURED, test W5). | HUMAN |
| 3 | 17 Nov | K4: what stands under the deck (bed -1.5 m to deck +1.7 m) | (a) visible pillars every 5-7 m, simple objects; (b) the pier pieces' own legs only; (c) a fill mound, no stilts | (a): vanilla concrete or steel pillar pieces every 5-7 m under the deck edges, simple objects (not walked); boats and swimmers pass between. About 16 on a large deck (ASSUMED until laid out). | HUMAN |
| 4 | 17 Nov | K4 deck edges | (a) solid low walls (normal objects, about 1 m) all round, gaps only at the ramp and pier heads; (b) walls on the water sides only; (c) thin rails, edge GPs static-only | (a): normal-object low walls (sandbag or concrete barrier, about 1 m) along every edge, with gaps only at the ramp and at pier heads. Stops AI walking off; gives cover. Pieces to confirm in the editor (UNSURE). | HUMAN |
