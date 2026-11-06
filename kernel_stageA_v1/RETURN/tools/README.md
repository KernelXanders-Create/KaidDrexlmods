# tools/ (Kernel Stage A sketch tools, PROPOSED)

Rerun everything from the `RETURN/` folder:

    pip install numpy scipy matplotlib
    python3 tools/make_all.py all        # ~2-3 min; deterministic (fixed seeds)
    python3 tools/make_manifest.py       # rewrites RETURN_MANIFEST.md with sha256s

| File | What it is |
|---|---|
| terrain_lib.py | Sketch height-field primitives (noise, islands, towers, channels, levees, craters, sampling, snapping) |
| plot_lib.py | Plan-view renderer: colour bands, hillshade, 1 km grid, scale bar, north arrow, AO outlines, objective dots |
| concepts_islands.py | The three island concepts: landforms + op/objective data |
| concepts_swamp.py | The three swamp concepts: landforms + op/objective data |
| make_all.py | Builds PNGs + objective JSONs, measures areas/gaps, fills the AUTO-MEASURED blocks in concept_X.md, runs house-rule checks |
| make_manifest.py | Writes RETURN_MANIFEST.md |
| out/ | Generated stats and validation report (MEASURED on the sketches) |

Sketch grid: 1000 x 1000 cells at 16 m (not the Stage B 4 m heightmap).
