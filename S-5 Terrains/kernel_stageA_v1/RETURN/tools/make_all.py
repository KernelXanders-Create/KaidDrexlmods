"""Build all Stage A sketches, objective JSONs and measured stats.

Usage (from the RETURN folder):  python3 tools/make_all.py [islands|swamp|all]
Needs: numpy, scipy, matplotlib.  Deterministic (fixed seeds).
Writes: <map>/plan_X.png, <map>/objectives_<map>_X.json,
        tools/out/stats_<map>_X.md, tools/out/validation.txt
and fills the AUTO-MEASURED block inside <map>/concept_X.md if present.
"""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
ROOT = os.path.dirname(HERE)

import numpy as np
import terrain_lib as T
import plot_lib as PL

SIZE = {"s": "squad", "t": "two_squad", "p": "platoon"}
GARRISON = {"s": "4-8", "t": "8-15", "p": "15-30"}
RECON = {"s": 900, "t": 1600, "p": 2500}
WAYS = {"s": 2, "t": 3, "p": 4}
MARK_A, MARK_B = "<!-- AUTO-MEASURED START -->", "<!-- AUTO-MEASURED END -->"


def build_objectives(H, ops, min_h):
    out, problems = [], []
    for op in ops:
        objs = []
        for k, (name, kind, sz, xk, yk, reason, flags) in enumerate(op["rows"], 1):
            x, y = xk * 1000, yk * 1000
            snapped = 0.0
            if "w" not in flags:
                x, y, snapped = T.snap_to_land(H, x, y, min_h=min_h)
                if snapped < 0:
                    problems.append(f"op{op['op']} {name}: no land within 600 m")
            h = max(0.0, T.sample(H, x, y))
            recon = int(min(4500, RECON[sz] + 8 * h + (500 if kind == "facility" else 0)))
            ways = WAYS[sz] + (1 if kind == "facility" and sz == "p" else 0)
            notes = [f"garrison points ~{GARRISON[sz]} (ASSUMED)"]
            if "w" in flags:
                notes.append("on water: decks/stilts/piers must be NORMAL objects, not simple (04)")
            if "t" in flags:
                notes.append("tunnels are above-ground shells hidden in rock or berm (04: no underground)")
            if "v" in flags:
                notes.append("vehicle objective: needs a clear AI lane")
            if snapped > 0:
                notes.append(f"snapped {snapped:.0f} m to sketch land")
            objs.append(dict(id=f"{op['op']}-{k:02d}", name=name, xy=[int(round(x)), int(round(y))],
                             size=SIZE[sz], kind=kind, reason=reason, recon_visible_from_m=recon,
                             interior="i" in flags, tunnels="t" in flags or kind == "tunnel",
                             ways_in=ways, notes="; ".join(notes)))
        sx, sy = op["start"]
        if op["op"] > 1:                      # later ops start from taken ground
            sx, sy, _ = T.snap_to_land(H, sx, sy, min_h=min_h, max_m=900)
        out.append(dict(op=op["op"], name=op["name"], start=[int(sx), int(sy)],
                        objectives=objs))
    return out, problems


def validate(ops_json):
    lines = []
    for op in ops_json:
        o = op["objectives"]
        n = len(o)
        sizes = {x["size"] for x in o}
        ap = sum(x["kind"] == "air_prep" for x in o)
        ao = sum(x["kind"] == "air_only" for x in o)
        tun = sum(x["tunnels"] for x in o)
        ok = 10 <= n <= 20 and len(sizes) == 3 and 1 <= ap <= 2 and ao <= 2 and tun >= 1
        lines.append(f"  op{op['op']} {op['name']}: {n} sites, sizes={sorted(sizes)}, air_prep={ap}, "
                     f"air_only={ao}, tunnel sites={tun} -> {'PASS' if ok else 'CHECK'}")
    return lines


def stats_md(name, H, d, ops_json):
    lab, areas = T.label_islands(H, 0.0)
    rows = ["| Island (sketch) | Area km² |", "|---|---|"]
    total_land = float((H > 0).mean() * 256)
    for nm, x, y in d["islands"]:
        x, y, _ = T.snap_to_land(H, x, y, min_h=0.1, max_m=900)
        r, c = int(y / T.CELL), int(x / T.CELL)
        L = lab[r, c]
        rows.append(f"| {nm} | {areas[L - 1]:.1f} |" if L > 0 else f"| {nm} | (label point in water) |")
    rows.append(f"| **All land above 0 m** | **{total_land:.1f}** |")
    cr = ["| Gap / route | Line length m | Water along it m | Deepest m | Shallowest m | Crossed by |",
          "|---|---|---|---|---|---|"]
    for nm, p0, p1, how in d["crossings"]:
        s = T.crossing_stats(H, p0, p1)
        cr.append(f"| {nm} | {s['length_m']} | {s['water_m']} | {s['deepest_m']} | {s['shallowest_m']} | {how} |")
    n_obj = sum(len(o["objectives"]) for o in ops_json)
    hist = {}
    for o in ops_json:
        for x in o["objectives"]:
            hist[x["size"]] = hist.get(x["size"], 0) + 1
    txt = [MARK_A,
           f"**MEASURED on the sketch height field** (16 m cells; built by `tools/make_all.py`; the sketch is itself ASSUMED design):",
           "", *rows, "", *cr, "",
           f"Objective sites: {n_obj} over {len(ops_json)} ops "
           f"(squad {hist.get('squad', 0)}, two-squad {hist.get('two_squad', 0)}, platoon {hist.get('platoon', 0)}). "
           f"Highest point {H.max():.0f} m; deepest {H.min():.0f} m.",
           MARK_B]
    return "\n".join(txt)


def run(map_name):
    if map_name == "islands":
        import concepts_islands as M
        bands = PL.ISLAND_BANDS
    else:
        import concepts_swamp as M
        bands = PL.SWAMP_BANDS
    os.makedirs(os.path.join(ROOT, map_name), exist_ok=True)
    os.makedirs(os.path.join(HERE, "out"), exist_ok=True)
    report = []
    for key, (title, fn) in M.CONCEPTS.items():
        d = fn()
        H = d["H"]
        ops_json, problems = build_objectives(H, d["ops"], d["min_h"])
        doc = {"map": map_name, "concept": key, "size_km": 16, "ops": ops_json,
               "measured_or_assumed": "ASSUMED: positions hand-placed on the sketch, then snapped to the nearest "
                                      "sketch land cell unless the site sits on water; recon distances, garrison "
                                      "counts and ways-in are ASSUMED rules of thumb (see tools/make_all.py)"}
        with open(os.path.join(ROOT, map_name, f"objectives_{map_name}_{key}.json"), "w") as f:
            json.dump(doc, f, indent=2)
        sub = f"PROPOSED concept {key}: {title}. 16 x 16 km, sea level 0 m. Sketch for choosing only; not approved, not a heightmap."
        PL.render(H, bands, ops_json, d["labels"], f"{map_name.capitalize()} concept {key}: {title} (PROPOSED)", sub,
                  os.path.join(ROOT, map_name, f"plan_{key}.png"), extra_lines=d.get("lines"))
        md = stats_md(title, H, d, ops_json)
        with open(os.path.join(HERE, "out", f"stats_{map_name}_{key}.md"), "w") as f:
            f.write(md + "\n")
        cpath = os.path.join(ROOT, map_name, f"concept_{key}.md")
        if os.path.exists(cpath):
            c = open(cpath).read()
            if MARK_A in c and MARK_B in c:
                c = c[:c.index(MARK_A)] + md + c[c.index(MARK_B) + len(MARK_B):]
                open(cpath, "w").write(c)
        report.append(f"{map_name} {key} ({title}):")
        report += validate(ops_json)
        report += [f"  PROBLEM {p}" for p in problems]
        print("\n".join(report[-(len(ops_json) + 1 + len(problems)):]))
    return report


if __name__ == "__main__":
    which = sys.argv[1] if len(sys.argv) > 1 else "all"
    rep = []
    for m in (["islands", "swamp"] if which == "all" else [which]):
        rep += run(m)
    vpath = os.path.join(HERE, "out", f"validation_{which}.txt")
    with open(vpath, "w") as f:
        f.write("House-rule checks per op (MEASURED by script on the JSON):\n"
                "10-20 sites, all three sizes, 1-2 air-prep, <=2 air-only, >=1 tunnel site.\n\n")
        f.write("\n".join(rep) + "\n")
