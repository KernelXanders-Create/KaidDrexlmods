"""Build the six K1 town plans: PNG + JSON + checks.

Run from the K1 folder:  python3 tools/make_towns.py
Needs: numpy, matplotlib, shapely. Deterministic (fixed seeds).
"""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
ROOT = os.path.dirname(HERE)

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon as MPoly
from matplotlib.lines import Line2D
from matplotlib.patches import Patch
from shapely.geometry import Polygon, MultiPolygon

from town_lib import Town
import towns as TW

FAM_COL = {"sci-fi": "#5b6f8f", "white cube": "#f4f1ea", "Naboo dome": "#e9c98f"}
H_EDGE = {"low": 0.6, "mid": 1.1, "tall": 2.0}
GARRISON_K = {"platoon": 13, "two_squad": 11, "squad": 10}


def coords(poly):
    return [[round(x, 1), round(y, 1)] for x, y in poly.exterior.coords[:-1]]


def build(fn, seed):
    spec = fn()
    lo, hi = spec["target"]
    for attempt in range(12):
        t = Town(spec, seed + attempt * 101)
        # pack the main street first (the dense core), then the lanes
        order = sorted([s for s in t.streets if s["kind"] != "road"], key=lambda s: 0 if s["kind"] == "main" else 1)
        for st in order:
            core = st["kind"] == "main"
            for side in (1, -1):
                t.pack_frontage(st, side, fr=(7, 15) if core else (6, 12), dp=(10, 17) if core else (8, 14),
                                back_p=0.55 if core else 0.35, gap_p=0.10 if core else 0.15)
        t.pack_infill()
        t.pack_fringe(spec["fringe"])
        if len(t.buildings) >= lo:
            break
    t.trim_to(hi)
    t.cut_unbuilt_lanes()
    t.tag()
    t.pick_garrison(GARRISON_K[spec["size"]], spec["approaches"])
    return spec, t


def draw(spec, t, m, out):
    fig = plt.figure(figsize=(16, 13), dpi=110)
    ax = fig.add_axes([0.04, 0.05, 0.66, 0.86])
    ax.set_facecolor("#cdbb9a")                    # ground: ochre-red scoria (alien palette, not Earth tan)
    sea = spec["sea"]
    geoms = sea.geoms if isinstance(sea, MultiPolygon) else [sea]
    for g in geoms:
        if spec["edge_kind"] == "cliff":
            ax.add_patch(MPoly(np.array(g.exterior.coords), closed=True, fc="#1d3f66", ec="none"))
        else:
            ax.add_patch(MPoly(np.array(g.exterior.coords), closed=True, fc="#1f5f8b", ec="#0b2a4a", lw=1.5))
    if spec.get("edge_line") is not None:
        e = np.array(spec["edge_line"].coords)
        ax.plot(e[:, 0], e[:, 1], color="#5a1f12", lw=5)
        ax.plot(e[:, 0], e[:, 1], color="#c4572e", lw=2, ls=(0, (2, 2)))
    for st in t.streets:
        p = st["poly"]
        ax.add_patch(MPoly(np.array(p.exterior.coords), closed=True,
                           fc={"main": "#efe6d2", "lane": "#e4d9c0", "road": "#d9c79f"}[st["kind"]],
                           ec="#8a7a5a", lw=0.6, ls="-" if st["kind"] != "road" else (0, (3, 2))))
    ax.add_patch(MPoly(np.array(t.square.exterior.coords), closed=True, fc="#f3e9cf", ec="#6b5a3a", lw=1.2, hatch="..."))
    for b in t.blocks:
        ax.add_patch(MPoly(np.array(b["outline"].exterior.coords), closed=True, fill=False, ec="#7a2d1a", lw=1.0, ls="--"))
    for b in t.buildings:
        xy = np.array(b["poly"].exterior.coords)
        ax.add_patch(MPoly(xy, closed=True, fc=FAM_COL[b["family"]], ec="#222", lw=H_EDGE[b["height"]]))
        c = b["poly"].centroid
        if b["family"] == "Naboo dome":
            r = min(3.2, (b["poly"].area ** 0.5) / 4)
            ax.add_patch(plt.Circle((c.x, c.y), r, fc="#d9a443", ec="#6b4a12", lw=0.6))
        if b["height"] == "tall":
            ax.plot(c.x, c.y, marker="^", ms=4, color="#222")
        if b.get("garrison"):
            ax.add_patch(MPoly(xy, closed=True, fill=False, ec="#d7263d", lw=2.6))
            ax.text(c.x, c.y + 4, b["id"][1:], fontsize=7, color="#d7263d", weight="bold", ha="center")
    lm = Polygon(spec["landmark"]["footprint"])
    ax.add_patch(MPoly(np.array(lm.exterior.coords), closed=True, fc="#2a9df4", ec="#0b2a4a", lw=2))
    lc = lm.centroid
    ax.plot(lc.x, lc.y, marker="*", ms=22, color="#ffd23f", mec="#0b2a4a", zorder=6)
    ax.text(lc.x + 8, lc.y + 8, spec["landmark"]["name"], fontsize=9, weight="bold",
            bbox=dict(fc="white", ec="#0b2a4a", alpha=0.85, pad=1.5), zorder=7)
    allb = t.placed.union(t.square)
    for name, (x, y) in spec["approaches"]:
        if name.lower().startswith(("square", "rim square")):
            continue
        bx0, by0, bx1, by1 = allb.bounds
        x = min(max(x, bx0 - 60), bx1 + 60)      # approaches beyond the view sit on its edge
        y = min(max(y, by0 - 60), by1 + 60)
        ax.plot(x, y, marker="D", ms=9, color="#1b998b", mec="k", zorder=6)
        ax.text(x + 6, y - 10, name, fontsize=8, color="#0d4d45", weight="bold", clip_on=True,
                bbox=dict(fc="#ffffffcc", ec="none", pad=0.8), zorder=7)
    for st in t.streets:
        if st["kind"] == "main":
            c = np.array(st["line"].coords)
            ax.plot(c[:, 0], c[:, 1], color="#b5179e", lw=1.2, ls=(0, (6, 3)))
    ax.set_aspect("equal")
    minx, miny, maxx, maxy = allb.bounds
    pad = 75
    ax.set_xlim(minx - pad, maxx + pad)
    ax.set_ylim(miny - pad, maxy + pad)
    ax.set_xlabel("metres east (local frame)")
    ax.set_ylabel("metres north")
    x0, y0 = minx - pad + 15, miny - pad + 15
    ax.plot([x0, x0 + 50], [y0, y0], color="k", lw=5)
    ax.plot([x0, x0 + 25], [y0, y0], color="w", lw=2.5)
    ax.text(x0 + 25, y0 + 6, "50 m", ha="center", fontsize=10, weight="bold")
    ax.annotate("", xy=(maxx + pad - 15, maxy + pad - 10), xytext=(maxx + pad - 15, maxy + pad - 45),
                arrowprops=dict(facecolor="k", width=4, headwidth=12))
    ax.text(maxx + pad - 15, maxy + pad - 58, "N", ha="center", fontsize=13, weight="bold")
    fig.text(0.04, 0.965, f"{spec['name']} (op {spec['op']}, {spec['size'].replace('_', '-')} site {spec['site']}): town plan, PROPOSED",
             fontsize=16, weight="bold")
    fig.text(0.04, 0.94, "Hand-designed streets and edge; footprints packed along the frontages. North up. For Miran's look, not a build file.",
             fontsize=10)
    lax = fig.add_axes([0.72, 0.05, 0.27, 0.86]); lax.axis("off")
    hand = [Patch(fc=FAM_COL[f], ec="#222", label=f"{f}") for f in FAM_COL]
    hand += [Line2D([], [], ls="", marker="o", ms=8, mfc="#d9a443", mec="#6b4a12", label="dome on a Naboo-dome building"),
             Line2D([], [], ls="", marker="^", ms=7, color="#222", label="tall (edge weight = height class)"),
             Patch(fc="none", ec="#d7263d", lw=2.6, label="garrison building (number = id)"),
             Patch(fc="none", ec="#7a2d1a", ls="--", label="block outline (3+ touching)"),
             Patch(fc="#efe6d2", ec="#8a7a5a", label="main street"),
             Patch(fc="#e4d9c0", ec="#8a7a5a", label="lane"),
             Patch(fc="#d9c79f", ec="#8a7a5a", ls="--", label="road out of town (no frontage)"),
             Patch(fc="#f3e9cf", ec="#6b5a3a", hatch="...", label="square"),
             Line2D([], [], ls="", marker="*", ms=16, color="#ffd23f", mec="#0b2a4a", label="sci-fi landmark"),
             Line2D([], [], ls="", marker="D", ms=8, color="#1b998b", mec="k", label="approach / entry")]
    if spec["edge_kind"] == "cliff":
        hand.append(Line2D([], [], color="#5a1f12", lw=5, label="caldera cliff edge (~300 m drop)"))
    else:
        hand.append(Patch(fc="#1f5f8b", ec="#0b2a4a", label="harbour water"))
    lax.legend(handles=hand, loc="upper left", fontsize=9, title="Legend")
    fc = m["family_counts"]
    txt = (f"MEASURED on this plan:\n"
           f"buildings {m['buildings']}  (in blocks {m['in_blocks_pct']} %)\n"
           f"sci-fi {fc['sci-fi']} / white cube {fc['white cube']} / Naboo dome {fc['Naboo dome']}\n"
           f"low {m['height_counts']['low']} / mid {m['height_counts']['mid']} / tall {m['height_counts']['tall']}\n"
           f"frontages {m['frontage_width_m']['min']}-{m['frontage_width_m']['max']} m (cv {m['frontage_width_m']['cv']})\n"
           f"longest straight run: main {[s['max_straight_run_m'] for s in m['streets'] if s['kind']=='main'][0]} m, "
           f"any lane {max(s['max_straight_run_m'] for s in m['streets'] if s['kind']=='lane')} m\n"
           f"square {m['square_area_m2']} m²; garrison {m['garrison']} buildings\n"
           f"town extent {m['extent_m'][0]} x {m['extent_m'][1]} m\n\n"
           f"Ground colour = red-ochre scoria (alien palette).\n"
           f"Footprints are plan shapes, not asset picks.")
    lax.text(0, 0.0, txt, fontsize=9.5, family="monospace", va="bottom")
    fig.savefig(out, dpi=110)
    plt.close(fig)


def to_json(spec, t, m):
    blocks = [dict(id=b["id"], outline=coords(b["outline"]), building_ids=[t.buildings[i]["id"] for i in b["members"]])
              for b in t.blocks]
    blds = []
    for b in t.buildings:
        blds.append(dict(id=b["id"], footprint=coords(b["poly"]), height_class=b["height"], family=b["family"],
                         block=b["block"], on_street=b["street"] if b["frontage"] else None,
                         frontage_at_street_edge=bool(b["frontage"]),
                         garrison=bool(b.get("garrison")), garrison_role=b.get("garrison")))
    gar = [b["id"] for b in t.buildings if b.get("garrison")]
    return {
        "town": spec["name"], "site_id": spec["site"], "op": spec["op"], "size": spec["size"],
        "status": "PROPOSED plan for Miran's look; not a build file",
        "frame": {"units": "metres", "axes": "x east, y north (north up)", "origin": "local town centre",
                  "world_anchor_xy_m": spec["world_xy"],
                  "anchor_note": "site position from objectives_v2.json (20 x 20 km map, SW origin); the local origin "
                                 "is placed on it by eye, ASSUMED"},
        "role_in_op": spec["role"], "approaches_text": spec["approach_text"],
        "approaches": [dict(name=n, xy=[x, y]) for n, (x, y) in spec["approaches"]],
        "edge": {"kind": spec["edge_kind"],
                 "water_or_drop_outline": [coords(g) for g in (spec["sea"].geoms if isinstance(spec["sea"], MultiPolygon) else [spec["sea"]])]},
        "streets": [dict(id=s["id"], kind=s["kind"], width_m=s["width"],
                         centreline=[[round(x, 1), round(y, 1)] for x, y in s["line"].coords]) for s in t.streets],
        "square": {"outline": coords(t.square), "area_m2": round(t.square.area)},
        "landmark": dict(name=spec["landmark"]["name"], family="sci-fi", height_class="tall",
                         footprint=[list(p) for p in spec["landmark"]["footprint"]], note=spec["landmark"]["note"]),
        "blocks": blocks,
        "buildings": blds,
        "garrison": {"count": len(gar), "building_ids": gar,
                     "note": "Each garrison building has a role (the approach or feature it covers). Garrison rings "
                             "50-150 m out are op-level, not in this file."},
        "measured": m,
        "measured_or_assumed": "MEASURED: every number under 'measured' (computed by tools/make_towns.py on this plan). "
                               "ASSUMED: all positions, shapes, families and heights (design).",
    }


def main():
    os.makedirs(os.path.join(ROOT, "towns"), exist_ok=True)
    rows = []
    for k, fn in enumerate(TW.TOWNS):
        spec, t = build(fn, 1000 + 17 * k)
        m = t.measures()
        out = os.path.join(ROOT, "towns", spec["key"])
        draw(spec, t, m, out + "_plan.png")
        with open(out + "_plan.json", "w") as f:
            json.dump(to_json(spec, t, m), f, indent=1)
        main_run = [s["max_straight_run_m"] for s in m["streets"] if s["kind"] == "main"][0]
        lane_run = max(s["max_straight_run_m"] for s in m["streets"] if s["kind"] == "lane")
        road_run = max([s["max_straight_run_m"] for s in m["streets"] if s["kind"] == "road"] or [0])
        mw = [s["width_m"] for s in m["streets"] if s["kind"] == "main"][0]
        lw = [s["width_m"] for s in m["streets"] if s["kind"] == "lane"]
        checks = {
            "60-110 buildings": 60 <= m["buildings"] <= 110,
            "~80% in blocks (>=75)": m["in_blocks_pct"] >= 75,
            "main street 6-8 m": 6 <= mw <= 8,
            "lanes 4-6 m": all(4 <= w <= 6 for w in lw),
            "no straight run > 80 m": max(main_run, lane_run) <= 80,
            "garrison 10-15": 10 <= m["garrison"] <= 15,
            "uneven frontages (cv >= 0.2)": m["frontage_width_m"]["cv"] >= 0.2,
        }
        rows.append((spec["name"], m, checks))
        print(spec["name"], m["buildings"], m["in_blocks_pct"], m["family_counts"], "main run", main_run, "lane run", lane_run,
              "road run", road_run, "garrison", m["garrison"], "FAIL:" if not all(checks.values()) else "PASS",
              [k for k, v in checks.items() if not v])
    with open(os.path.join(HERE, "checks.txt"), "w") as f:
        f.write("K1 town checks (MEASURED by tools/make_towns.py)\n\n")
        for name, m, checks in rows:
            f.write(f"{name}: " + ", ".join(f"{k} {'PASS' if v else 'FAIL'}" for k, v in checks.items()) + "\n")


if __name__ == "__main__":
    main()
