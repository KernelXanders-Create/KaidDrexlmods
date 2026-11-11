# K0: how the K1 towns were made, what we'd change, and a hard look at Perys v4

Written for the Omnibus and Miran, 11 Nov. **Measured** = computed by a script on your files or mine (`tools/analyse_v4.py` on your v4 layout and natural ground; the K1 numbers come from my K1 JSONs). **Assumed** = my judgement. Figure: `figures/v4_bare_edges_and_pad_levels.png`.

---

## 1. The method as I actually ran it for K1

### 1a. Drawn by hand, per town (about 60 % of the result)
The hand work did most of it. The script only packed buildings along what I drew.

1. **The edge first.** For each town I drew the one feature the town exists for: the quay water (Sound Head, Kastro Quay, Kamar, Lantern Quay), the causeway landfall (Causeway Foot), or the caldera cliff (Oyra). Everything else hangs off that edge.
2. **The main street's line.** It starts at the edge (the quay or the landfall) and bends inland toward the one road out that matters (to the citadel, to the monastery, down the ravine).
   - 7-13 control points, 25-40 m apart, each turning 10-30° from the last.
   - Smoothed with 3 passes of Chaikin corner-cutting.
   - That gave longest straight runs of 42-76 m (measured), all under 80 m.
   - The bend always had a reason in my head: "follow the shore round", "turn up the ravine", "follow the rim". I never added a bend just to break a straight.
3. **The square.** It sits on the inside of a main-street bend, 40-120 m from the edge, so it is the hinge between the edge and the uphill town.
   - A 5-6 point hand polygon, slightly irregular, smoothed with 2 passes.
   - Measured areas: 608-1,236 m².
   - Always bounded by streets on 2 sides, so it fills from two directions.
   - The landmark (about 10 x 10 m) sits inside it, off-centre toward the open side.
4. **Lanes.** 3-6 per town, branching off the main street at about 60-90°.
   - **Two of them join to make a loop round a block.** The loop is what lets the infill make deep blocks: the ground between two streets gets filled from both sides.
   - Lanes heading out of town go as far as the approach point (the road out, the path to the AA).
5. **Approaches and the "CIS zone".** I marked the 4-5 entry points (quay, roads, paths), which later drive the garrison choice. I also drew a rectangle over the quay or causeway gate where sci-fi CIS halls go.

### 1b. What the script did (`K1/tools/town_lib.py`, `make_towns.py`)
1. **Frontage packing.** Along each side of each street I walked the centre line and cut lots.
   - **Main street:** frontage width uniform 7-15 m, depth 10-17 m.
   - **Lanes:** frontage 6-12 m, depth 8-14 m.
   - **Setback 0:** the front edge sits 0.05 m off the street edge.
   - The lot shape follows the street's normal at both ends, so lots fan on curves and stay square on straights. That fanning is one reason the plans look built.
   - **Passages:** after each lot, with probability 0.10 on the main street and 0.15 on lanes, I skipped 2.5-4.0 m.
   - **Measured result:** frontage widths 6.2-14.9 m, coefficient of variation 0.20-0.25 per town.
2. **Second row.** Behind each frontage lot, with probability 0.55 on the main street and 0.35 on lanes, a back building 7-12 m deep shares the lot's back edge (touching).
3. **Block infill (this is what made blocks 2-3 deep).**
   - Random points within 45 m of any street, up to 6,000 tries.
   - Each point gets a rectangle of 8-14 x 8-14 m, turned to the nearest street's tangent.
   - **It is kept only if it touches an existing building** (distance 0) and fits after clipping. Infill grows from the street walls inward, so it never makes free-standing scatter.
   - **Densify toward the core:** a point is rejected with probability min(0.85, distance to square / 220 m). At 100 m from the square, 45 % of tries are thrown away; at 190 m or more, 85 %.
4. **Clipping.** Each candidate was:
   - clipped to land minus 0.5 m;
   - kept out of streets, the square and the quay apron (12 m off the water);
   - cut against buildings already placed, keeping the largest piece;
   - rejected if under 35 m², or if its area was under 72 % of its smallest bounding rectangle (no slivers).
   - **This is the step that cannot be built with real models.** It trims footprints to fit. See section 2.
5. **Trim from the outside in.** I generated more buildings than wanted, then sorted them by (distance to the "spine" = main street + quay lane) + 0.35 x (distance to the square), and kept the nearest 60-108. That keeps the town hugging its main street and quay, and the edge of town is wherever the count ran out, which is irregular.
6. **Lane ends.** I sampled each lane every 4 m. A sample is "built" if any building is within half the street width + 4 m. Before the first built sample and after the last, the lane becomes a "road out of town" (no frontage), if that piece is at least 12 m.
7. **Blocks** = groups of 3 or more footprints touching within 0.35 m. Measured: 92.5-96.3 % of buildings are in blocks, 7-10 blocks per town.
8. **Families.**
   - **The sci-fi core** is the nearest 22 % of buildings to the square: 80 % of those are sci-fi, the rest Naboo-dome.
   - **In the CIS zone,** 45 % are sci-fi.
   - **Elsewhere:** Naboo dome on a block-corner frontage with a 22 % chance, or 10 % at random; sci-fi with a 7 % chance; otherwise white cube.
9. **Heights.** Tall goes to the core (55 % of core buildings within 0.8 x the core radius), the quay front (35 %), or big footprints over 260 m² (40 %). Low goes to detached and outer buildings. Measured: 10-17 tall per town.
10. **Garrison.**
    - First, one building per approach: the nearest high-scoring one. The score is tall 3, mid 1.5, +2 if within 40 m of the square, +1 if within 30 m of the edge.
    - Then the best remaining by score, with at least 25 m between garrison buildings, up to 13 / 11 / 10 for platoon / two-squad / squad sites.
    - Each gets a role from where it is: first contact on an approach, square, overwatch on the quay, main-street strongpoint, or depth.

### 1c. What I tried and rejected (the passes, in order; I looked at a contact sheet of all six plans after each)
| Pass | What I saw | What I changed |
|---|---|---|
| 1 | Straight-run check failed on 5 towns, and the towns read as **single ribbons of houses along long radial streets.** That was exactly Miran's "houses in rows". | Added block infill (1b-3). |
| 2 | My trim dropped the newest buildings first, which **deleted whole lanes.** That left empty wide streets. | Trim by distance instead (1b-5). |
| 3 | Trimming by distance to the square alone produced a round blob **detached from the harbour:** the quay had no buildings. | Trim by distance to the spine (main street + quay lane) plus a smaller square term. |
| 4 | A fixed 65 m core radius made **everything sci-fi** in the compact towns. | The core became a share of buildings (22 %), not a radius. |
| 5 | The layouts were too spread out for 100 buildings: long streets meant ribbons again. | **Redrew every town 30-40 % smaller,** with lanes forming loops, and marked the streets out of town as "roads". This mattered more than any parameter. |
| 6 | Buildings sat on the seaward side of quay lanes. Lanes with houses at one end only read as empty streets. | 12 m quay apron. Cut unbuilt lane ends into roads (1b-6). |
| 7 | Garrison roles all said "depth". | Roles from position (1b-10). |

### 1d. Why it reads as a town: the numbers I think matter (measured on K1)
- **Buildings vs street.** Built footprint is 3.1-3.9 times the street area (Causeway Foot 3.3, Kamar 3.1, Kastro 3.3, Lantern 3.5, Oyra 3.9). Buildings cover 41-51 % of each town's convex hull. **Your v4: 0.95 times** (14,237 m² of building vs 14,965 m² of street inside the town ground), and 23 % cover. This is the single biggest difference.
- **Setback 0,** so the street wall is continuous except at passages and lane mouths.
- **Uneven frontage** (cv 0.20-0.25), **fanned lots on curves,** and **no free-standing infill:** everything leans on a street wall.

---

## 2. What I would do differently now (real models, fixed footprints, pads, 10-16 % slopes, doors on the street)
1. **Pack models, not shapes.**
   - Split each street side into runs between lane mouths.
   - Fill each run with catalogue models whose door side faces the street. Choose by frontage width so the sum fits the run within 1-2 m, using a small knapsack over the widths each model offers on its door face.
   - Never trim a footprint. Leave the leftover as a 2.5-4 m passage or a stair (a path).
2. **One pad per block, not per house.**
   - A block is 3-6 touching models on one shared pad (one `pad_group`), sized so the street's grade along the block costs at most ±0.75 m at the doors. At a 5 % street grade that means a block no longer than 30 m; at 8 %, about 19 m.
   - The next block steps up or down by the street's rise. **This gives the stepped "terrace per block" look of a real hill town** instead of one long level shelf per street.
3. **Let the main street climb.**
   - Instead of contour-level streets, run the main street **diagonally across the contours at 3-6 %**, between the fixed points (the NW port at 59.4 m and the quay at 2.2 m are 57 m apart in height).
   - Every block then has its own level and the pads stay shallow, because the street is never far from the natural slope.
   - Keep a level contour street only where the AI convoy needs it.
4. **Back rows built into the slope.** On the uphill side of a street, put the back row's rear wall where you now put a WL01 retaining wall: the building is the retaining wall. On the downhill side, the back row sits one block-step lower and is reached by a stair path.
5. **The square as a stepped platform:**
   - two levels 1.5-2.5 m apart, joined by a stair;
   - the landmark on the upper level;
   - doors on three sides;
   - the open side toward the sea, kept by sending the main street past it, not through it.
6. **Doors:** prefer models whose door side is "measured" for the main street and the square. Use the "assumed" sci-fi blocks in back rows, where a wrong door costs nothing.
7. **Measure as I go:** run the cut/fill sample per block pad and the street-wall continuity after each street is packed, and repack that street if either fails, before moving on.

---

## 3. Hard critique of Perys v4: the ten things that most make it read as generated, ranked
All numbers are MEASURED by `tools/analyse_v4.py` on `perys_v4_layout.json` and the natural ground, unless marked.

**1. The lanes and links are bare banks.**
- *Measured:* street-wall continuity is **0 %** on all four lanes (L2a/b, L3a/b), on the AR links (ARa, ARb) and on the FK links. The 470 m harbour road also has 0 %.
- *In the figure:* every red-dotted edge.
- *Change:* each lane gets houses on both sides for most of its length, or it becomes a stair path through a block (no ribbon of its own).
- *Rule:* inside the town ground, no street segment longer than 40 m without a building within 3 m of its edge on at least one side.

**2. Whole streets sit on one level, and the three main streets run parallel along the contours.**
- *Measured:* only **5 distinct pad levels for 93 buildings.**
- *Measured:* MS and KR run about 99 m apart, KR and MR about 46 m apart, both roughly parallel for 200+ m.
- *Effect (assumed):* from the air this reads as three terraced bands, which is the "rows" look again at a larger scale.
- *Change:* main street diagonal at 3-6 %, block pads stepping with it (section 2).
- *Rules:*
  - distinct block pad levels of at least one per 10 buildings, with neighbouring blocks 0.5-3 m apart;
  - no two streets within 15° of parallel and 30-120 m apart for more than 100 m.

**3. Houses almost touch but don't: separate boxes with slots of grass.**
- *Measured:* the median gap to the nearest building is **0.72 m** (quartiles 0.46-1.39 m). Only **44 %** of buildings are in groups of 3 or more within 1 m (my K1: 92-96 % within 0.35 m).
- *Cause:* each house is on its own pad.
- *Change:* shared block pads with touching models (gap 0-0.3 m), and passages of 2.5 m or more where a gap is wanted.
- *Rules:*
  - at least 70 % of buildings in touching groups of 3 or more;
  - at most 10 % of neighbour gaps fall in the dead band of 0.4-2.5 m.

**4. Every door is dead square to its street.**
- *Measured:* **93 %** of doors are within 2° of square-on to their street's tangent (median 0.3°). Together with one front line per row, this is a machine signature.
- *Change:* follow the street but allow ±2-6° per block (the block turns with the street; houses in a block share its angle). Let corner houses face the side lane.
- *Rule:* across a town, the standard deviation of (door bearing minus street normal) is 1.5-6°, and no more than 60 % of buildings are within 1°.

**5. The square is empty, and the landmark is not on it.**
- *Measured:* square 1,126 m²; comp cover **7.9 %** (Crystal Carts); only **6** buildings within 6 m of the square's edge; the landmark (SF07, 45 m) is **75 m** from the square.
- *Change:* see section 2-5.
- *Rules:*
  - landmark centroid inside the square or within 10 m of it;
  - at least 8 doors facing the square, on at least 3 sides;
  - comp cover 15-35 %;
  - area 600-1,500 m².

**6. The main streets' walls have holes and setbacks.**
- *Measured continuity:* MS **52 %**, KR **59 %**, MR **20 %**, AR **82 %**. 51 % of street-assigned buildings stand more than 1 m back from the ribbon (90th percentile 8.2 m).
- *Change:* frontage at the ribbon, with the gaps used as deliberate passages.
- *Rules:*
  - main-street continuity at least 70 %, lanes at least 50 %;
  - at least 80 % of frontage buildings within 1.0 m of the ribbon.

**7. Too much street for the buildings.**
- *Measured:* street area inside the town ground is **14,965 m²** vs a building footprint of **14,237 m²** (ratio 0.95; K1 reached 3.1-3.9). MS is 10 m and KR 9 m wide, with frontage buildings of median height 5.8 m.
- *Effect (assumed):* width to height of about 1.6, so the streets read as roads through a suburb.
- *Change:* 6-8 m mains (you've already adopted this), 4-5 m lanes, more lanes as stairs.
- *Rules:*
  - building footprint to street area of at least 2.0 inside the town ground;
  - street width to median frontage height of at most 1.5 on mains and 1.2 on lanes.

**8. Long engineered retaining walls face the streets.**
- *Measured:* **243 m** of WL01 in 24 runs. On MR, the long runs are almost the whole street edge (MR continuity 20 %).
- *Change:* put buildings where the walls are. A back row dug into the bank retains it, and its door is on the street.
- *Rule:* at most 10 m of retaining wall per 100 m of street, and no single run over 21 m (3 pieces) on a street edge.

**9. Cut-and-fill banks at house after house.**
- *Measured:* the median pad cut or fill (my simple sample, footprint + 1.5 m) is **2.12 m**. 30 % of buildings exceed 2.5 m; the maximum is 3.38 m.
- *Effect (assumed):* these are what show in game as banks and "terrain incursion" between houses.
- *Change:* the diagonal street and the stepped block pads keep pads near the natural ground.
- *Rule:* median cut or fill of at most 1.5 m, at most 10 % over 2.5 m, none over 4.0 m.

**10. Twin models and family clumping show the generator.**
- *Measured:* ND01 + ND02 (visual twins) are **21.5 %** of the town. The Naboo-dome family is 32 % of all buildings (30 of 93). The yellow cluster in the figure (the AR street) is mostly small domes on one level.
- *Note, measured:* I found no case where an ND01/ND02's nearest neighbour is also ND01/ND02, so the issue is share and same-level clustering, not adjacency.
- *Change:* count twins as one model for the cap; spread families by street role (sci-fi on the square and the quay, white cubes on lanes, domes on corners).
- *Rules:*
  - twin-group share at most 12 %;
  - on any frontage run, no more than 2 consecutive buildings from the same twin group.

**Also worth fixing** (not in the ten):
- The quay group sits 450 m from the town at the end of a bare harbour road. The road needs a few buildings at the bends (a hamlet at the half-way bend) or a shorter, steeper path link for infantry.
- The town edge is a hard outline around two rows. Let the last blocks thin out to 1-2 detached houses along the roads out.

---

## 4. Rules I think are wrong or too tight
| Rule | My view | Why |
|---|---|---|
| Main streets under 5 % (contour streets) | **Too tight.** Allow up to 8 % on main streets, and keep 5 % only on the AI convoy route. | Level contour streets produce the parallel terraces in critique 2 and the deep pads in 9. Mediterranean hill towns climb diagonally. |
| One pad per building | **Already relaxed** by `pad_group`. Make the shared block pad the default, and single pads the exception for detached houses. | Single pads produce the 0.4-2.5 m gaps (critique 3). |
| Cut or fill at most 4 m | **Fine as a hard limit.** Add a target median (1.5 m). | A 4 m limit allows a town where every house sits in a 3 m hole. The median catches it. |
| No loose props | **Right** for clipping. But allow comps on the square, at lane ends and on the quay, as whole units. | Your v3 shots show the props were the problem. Comps give the square something to fight round (critique 5). |
| 15 % model cap | **Right idea,** count by visual twin group. | ND01/ND02 slip under it at 11.8 % and 9.7 % separately, but read as one model at 21.5 %. |
| Retaining walls as WL01 straight runs | **Use them less.** | Buildings dug into the bank do the same job and add street wall (critique 8). |
| Tall pieces never on a street edge | **Agree.** Add: at most 1 tall piece per 15 buildings, and the landmark on the square. | v4's 45 m block off the square pulls the eye away from the square. |
| Door 3 m out on a ribbon, the square or the quay | **Agree.** Add a door-angle variation check (critique 4). | |

---

## 5. Checklist: 15 measurable checks (built vs generated)
Each is computable from your layout schema plus the natural ground.

| # | Check | Pass threshold |
|---|---|---|
| 1 | Touching blocks | at least 70 % of buildings in groups of 3 or more with gaps of 0.3 m or less |
| 2 | Gap dead band | at most 10 % of nearest-neighbour gaps between 0.4 and 2.5 m |
| 3 | Street-wall continuity (both sides, building within 2 m of the ribbon edge) | main at least 70 %, lane at least 50 %, inside the town ground |
| 4 | Bare street length | no segment over 40 m inside the town ground without a building within 3 m |
| 5 | Setback | at least 80 % of frontage buildings within 1.0 m of their ribbon |
| 6 | Building to street area (inside the town ground) | at least 2.0 |
| 7 | Street width to median frontage height | main at most 1.5, lane at most 1.2 |
| 8 | Door-angle variation (door bearing minus street normal) | standard deviation 1.5-6°, and at most 60 % within 1° |
| 9 | Frontage width spread per run | coefficient of variation at least 0.25 |
| 10 | Pad levels | at least 1 distinct block pad level per 10 buildings; neighbouring blocks 0.5-3 m apart |
| 11 | Cut or fill (footprint + 1.5 m sample) | median at most 1.5 m, at most 10 % over 2.5 m, none over 4.0 m |
| 12 | Retaining walls | at most 10 m per 100 m of street; no run over 21 m on a street edge |
| 13 | Parallel bands | no two streets within 15° and 30-120 m apart for over 100 m |
| 14 | Square | landmark inside or within 10 m; at least 8 doors on at least 3 sides; comp cover 15-35 %; area 600-1,500 m² |
| 15 | Twin-group repetition | twin-group share at most 12 %; no more than 2 consecutive same-twin buildings on a frontage run |

**v4 against these** (measured where I could):
- **Fails:** 1 (44 %), 3 (lanes 0 %, MS 52 %), 4, 5 (49 % within 1 m), 6 (0.95), 8 (93 % within 2°), 10 (5 levels), 11 (30 % over 2.5 m), 12 (243 m), 13 (MS/KR/MR), 14 (cover 7.9 %, landmark 75 m away), 15 (21.5 %).
- **Not computed:** 2, 7 and 9 (they need per-run sequencing I didn't build for v4).

---

## 6. Prompts and working loop: what mattered
1. **Your rejection words were the spec.** I kept Miran's sentence ("houses in rows, wide empty streets, no dense core") in front of me. After each pass I named which of the three I could still see.
2. **Look at the picture every pass, not just the numbers.** After every run I made one contact sheet of all six towns at the same scale and looked at it.
   - The numbers passed before the towns looked right (pass 1 passed most checks and was still ribbons).
   - Every real fix came from seeing a failure mode in the image and giving it a name: "ribbons", "detached core", "empty lanes", "everything sci-fi".
3. **Change one mechanism per pass, then rerun everything.** Never tune five parameters at once. Each pass was 1-2 code changes, a rerun of all six towns, and a look.
4. **Make the checks print PASS or FAIL per town every run,** with the measured value next to it, and never hand-edit a number into the write-up. My write-ups pull numbers from the JSON. Twice I caught my own prose quoting a stale number this way.
5. **Hand-draw the structure; let the script do the repetition.** The best results came when I spent the time on the edge, the main street's reason and the lane loops, and let the script only fill frontages. When I let streets be long and generic, no packing rule saved it (pass 5).
6. **Draw what you can't see in game.** I plotted the street-wall gaps as red dots for v4 (`figures/v4_bare_edges_and_pad_levels.png`). It makes critique 1 and 6 visible in one look, and I'd add it to your offline renders.

---

## Measured, assumed, unsure
- **Measured (from your files, by `tools/analyse_v4.py`):**
  - gaps, touching groups, door angles, setbacks, continuity;
  - model shares, square cover, landmark distance;
  - pad levels, cut and fill (simple sample);
  - retaining wall length, street and building areas, parallel spacing.
  - The K1 figures are measured on my K1 JSONs.
- **Assumed:**
  - every "effect" line (how it reads in game);
  - the thresholds in section 5, which are my judgement tuned so K1 passes and v4 fails. They should be calibrated against a town Miran likes.
- **Unsure:**
  - your full grading check reads up to 1.9 m more cut than my simple sample;
  - the door sides marked "assumed" in the catalogue;
  - how the Naboo stepped entrance reads in game.
