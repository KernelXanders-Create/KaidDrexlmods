# Op 5 sites off the road net: their ways in — v1

Run on 2026-11-27. This covers the op 5 sites that are foot / boat / air:
- 5-02 and 5-M2.5 (P10);
- 5-12 (P17);
- the 5-13 hamlet (H3).

It measures how players and AI walk from each to the op 5 road net, and where the nearest boat water is.

Script: `offnet/offnet5.py`. Output: `offnet/offnet5_v1.json`. It uses the drop 2 masks and heights (`suddra_masks.npz`, `suddra_height_cm.npz`) and the op 5 plan (`planner_ops56_v4/op5_main`). Numbers are MEASURED unless marked otherwise.

## Method

- **Players' walk:** any cell that is not deep or boat water (depth bands 2 and 3) can be walked.
  - "Wade" means walking through depth band 1, the reed shallows.
  - "Low ground" means a cell that is neither water nor in the AI-walk mask.
- **AI walk:** only the drop 2 AI-walk mask (`ai_dry`).
- **Walks:** each is the shortest one, on an 8 m grid, from the pad edge to within 10 m of an op 5 road.
- **Boat:** the nearest cell of the boat network (`boat_core`).

## Result

| Site | Players' walk to the net | of it wading | of it low ground | AI walk to the net | Nearest boat water |
|---|---|---|---|---|---|
| 5-02 West Esker AA (1400, 12000) | 1,016 m to 5-03 → 5-F.3 | 676 m (lowest −0.74 m) | 124 m | **Yes**: 1,298 m, all on AI ground, to 5-03 → 5-F.3 at (2160, 12936) | 1,857 m |
| 5-M2.5 (3385, 12520) | 80 m to 5-M2.2 → 5-M2.4, all dry | 0 | 0 | **Yes**: the same 80 m | 56 m |
| 5-12 Small Radar (600, 11000) | 1,804 m to 5-01 → 5-F.3 at (2016, 10008) | 0 | 594 m (lowest +0.13 m) | **No** walk within 3.5 km | 1,106 m |
| 5-13 Stake Hamlet (1840, 9705) | 353 m to 5-01 → 5-F.3 at (2016, 9992) | 0 | 172 m (lowest +0.13 m) | **No** walk within 3.5 km | 648 m |

## Reading (AI)

- **5-02:** it has no road, but AI can walk it in by a 1.3 km dry way. Players have a shorter 1.0 km way that wades for about 680 m.
- **5-M2.5:** it is in practice on the net: its walk is 80 m of dry ground, a little longer than the 21 m pad-to-pad gap in P10.
- **5-12 and 5-13:** their AI are cut off from the net. Their droids stay where they are (X1, X2). Players can walk in to both without wading.

## Decisions (Kernel)

| # | Finding | Answer | source |
|---|---|---|---|
| X1 | 5-13: no AI walk to the net; players walk 353 m, 172 m of it on low ground | a Accept it: the hamlet's droids stay where they are; players walk in | HUMAN |
| X2 | 5-12: no AI walk to the net; players walk 1,804 m, 594 m of it on low ground | a Accept it: 5-12's droids stay where they are; players walk in (foot / boat / air, P17) | HUMAN |
