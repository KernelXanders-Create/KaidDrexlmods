"""K3: build the three swamp concepts at the 9 Nov targets.

Run from the K3 folder:  python3 tools/make_k3.py
Writes swamp/plan_X.png, swamp/objectives_swamp_X.json, tools/out/optable_X.md,
tools/out/checks.txt, COVERAGE.md, DRAWS.md and fills the AUTO block in each
swamp/concept_X.md. Deterministic.
"""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
ROOT = os.path.dirname(HERE)

import numpy as np
from scipy import ndimage
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap, BoundaryNorm, LightSource
from matplotlib.patches import Patch, Polygon
from matplotlib.lines import Line2D
from scipy.spatial import ConvexHull

import terrain_lib as T
import concepts_swamp_v1 as V1
from swamp_v2_data import CONCEPTS, LIB

SIZE = {"s": "squad", "t": "two_squad", "p": "platoon"}
GARR = {"s": 25, "t": 50, "p": 110}                       # ASSUMED, same as the Islands purpose map
TGT_H = {"s": 6.0, "t": 10.0, "p": 15.0}                  # ASSUMED structure height for recon screening
OPC = ["#d7263d", "#f49d37", "#7b2cbf", "#1b998b", "#2e294e", "#3a86ff", "#8a5a00", "#e5383b"]
BANDS = [(-1.3, "#1d4f6e", "channel, swim or boat (< -1.3 m)"), (-0.5, "#3d86a8", "deep wade (-1.3 to -0.5 m)"),
         (0, "#86c2c4", "shallow wade / slough (-0.5 to 0 m)"), (0.5, "#a7a777", "wet ground (0 to 0.5 m)"),
         (1.5, "#9cbf6e", "firm ground (0.5 to 1.5 m)"), (3, "#6c9f4a", "hammock / levee (1.5 to 3 m)"),
         (10, "#7d8a4b", "rise (3 to 10 m)"), (30, "#9a8460", "ridge / bluff (10 to 30 m)"), (9999, "#d9d0c0", "hills (> 30 m)")]
MARK_A, MARK_B = "<!-- AUTO-OPTABLE START -->", "<!-- AUTO-OPTABLE END -->"


def terrain(key):
    if key == "A":
        d = V1.swamp_A()
        lines = [l for l in d["lines"] if l[1].get("label", "").startswith(("rail", "proposed AI road"))]
    elif key == "B":
        d = V1.swamp_B()
        berm = [(6700, 8500), (8100, 8650), (9500, 8800)]
        T.raise_line(d["H"], berm, 40, 4.0, soft=25)          # the Titan as a land berm (terrain, not objects)
        lines = [l for l in d["lines"] if "Titan" not in l[1].get("label", "")]
        lines.append((berm, dict(color="#b5179e", lw=4, ls="-", label="Felled Titan berm (terrain, walkable, AI-passable)")))
    else:
        d = V1.swamp_C()
        lines = d["lines"]
    return d["H"], lines


def square_of(x, y):
    c = "ABCD"[min(3, int(x // 4000))]
    r = min(4, int(y // 4000) + 1)
    return f"{c}{r}"


def recon(H, x, y, th):
    """Terrain-only screening (like the Islands purpose map): observers at 16
    distances on 24 bearings, eye 1.8 m, target top = ground + th.
    Returns max, median of per-bearing max, bearings seeing it from >=1 km and >=2 km."""
    dists = np.arange(250, 4001, 250)
    best = np.zeros(24)
    hs = T.sample(H, x, y) + th
    for b in range(24):
        a = 2 * np.pi * b / 24
        for dd in dists:
            ox, oy = x + dd * np.cos(a), y + dd * np.sin(a)
            if not (0 <= ox < T.SIZE_M and 0 <= oy < T.SIZE_M):
                continue
            n = max(2, int(dd / T.CELL))
            ts = np.linspace(0.0, 1.0, n)[1:-1]
            px = ox + (x - ox) * ts
            py = oy + (y - oy) * ts
            c = np.clip((px / T.CELL).astype(int), 0, T.N - 1)
            r = np.clip((py / T.CELL).astype(int), 0, T.N - 1)
            ground = np.maximum(H[r, c], 0.0)
            eye = max(T.sample(H, ox, oy), 0.0) + 1.8
            line = eye + (hs - eye) * ts
            if np.all(ground <= line):
                best[b] = max(best[b], dd)
    return int(best.max()), int(np.median(best)), int((best >= 1000).sum()), int((best >= 2000).sum())


def build(c):
    H, lines = terrain(c["key"])
    lab, _ = ndimage.label(H > 0)
    sites, problems, ops_out = [], [], []
    for op in c["ops"]:
        ids = []
        k = 0
        for line in op["rows"].strip().splitlines():
            name, role, sz, xk, yk, libc, flags, stake = [s.strip() for s in line.split("|")]
            fl = flags.split()
            x, y = float(xk) * 1000, float(yk) * 1000
            moved = 0.0
            if "w" not in fl:
                x, y, moved = T.snap_to_land(H, x, y, min_h=0.25, max_m=600)
                if moved < 0:
                    problems.append(f"op{op['op']} {name}: no firm ground within 600 m")
            if role == "F":
                sid = f"{op['op']}-F"
            elif role == "M":
                k += 1
                sid = f"{op['op']}-M{sum(1 for s in sites if s['op'] == op['op'] and s['role'] == 'main') + 1}"
            else:
                sid = f"{op['op']}-{sum(1 for s in sites if s['op'] == op['op'] and s['role'] == 'supporting') + 1:02d}"
            draw = next((f for f in fl if f.startswith("D")), None)
            th = 30.0 if (draw or "new" in fl) else TGT_H[sz]
            rmax, rmed, r1, r2 = recon(H, x, y, th)
            s = dict(id=sid, op=op["op"], name=name, role={"F": "FINAL", "M": "main", "S": "supporting"}[role],
                     size=SIZE[sz], xy=[int(x), int(y)], square=square_of(x, y), stake=stake,
                     library_pick=LIB[libc], draw=draw, new_build="new" in fl, capstone="cap" in fl,
                     interior="cap" in fl, library_interior="li" in fl, tunnel="tun" in fl,
                     air_prep="ap" in fl, air_only="ao" in fl, destructible="d" in fl, on_water="w" in fl,
                     vehicle="v" in fl, garrison_planned=GARR[sz], garrison_ring_m=[50, 150],
                     landmass=int(lab[int(y / T.CELL), int(x / T.CELL)]) if "w" not in fl else 0,
                     ground_m=round(T.sample(H, x, y), 1), snapped_m=round(max(moved, 0), 0),
                     recon_max_m=rmax, recon_median_m=rmax and rmed, recon_bearings_1km=r1, recon_bearings_2km=r2)
            sites.append(s)
            ids.append(sid)
        sx, sy = op["start"]
        ops_out.append(dict(op=op["op"], week=op["week"], name=op["name"], start=[sx, sy],
                            after_any_of=op["prereq"][0] if op["prereq"] else [], fob=op["fob"], site_ids=ids))
    return H, lines, sites, ops_out, problems


def checks(c, sites, ops_out):
    out, ok_all = [], True
    for op in ops_out:
        S = [s for s in sites if s["op"] == op["op"]]
        nf = sum(s["role"] == "FINAL" for s in S)
        nm = sum(s["role"] == "main" for s in S)
        ns = sum(s["role"] == "supporting" for s in S)
        sizes = {s["size"] for s in S}
        ap = sum(s["air_prep"] for s in S)
        ao = sum(s["air_only"] for s in S)
        plat_before = any(s["size"] == "platoon" and s["role"] != "FINAL" for s in S)
        garr = sum(s["garrison_planned"] for s in S)
        ok = nf == 1 and nm + ns >= 12 and 12 <= ns <= 16 and len(sizes) == 3 and 1 <= ap <= 2 and ao <= 2 and plat_before and garr <= 1200
        ok_all &= ok
        out.append(f"  op{op['op']} {op['name']}: final {nf}, mains {nm}, supporting {ns}, sizes {sorted(sizes)}, "
                   f"air-prep {ap}, air-only {ao}, platoon before final {plat_before}, planned garrison {garr} -> {'PASS' if ok else 'CHECK'}")
    draws = {s["draw"] for s in sites if s["draw"]}
    newb = {s["draw"] for s in sites if s["draw"] and s["new_build"]}
    caps = sum(s["capstone"] for s in sites)
    tun = sum(s["tunnel"] for s in sites)
    weak = [s for s in sites if (s["draw"] or s["role"] in ("FINAL", "main")) and s["recon_bearings_1km"] < 6]
    mapok = len(ops_out) == 8 and 4 <= len(draws) <= 6 and 1 <= len(newb) <= 2 and caps == 1 and 2 <= tun <= 3
    ok_all &= mapok
    out.append(f"  map: ops {len(ops_out)}, draws {len(draws)}, new-build centerpieces {len(newb)}, capstone interiors {caps}, "
               f"tunnel sites {tun} -> {'PASS' if mapok else 'CHECK'}")
    out.append(f"  recon (terrain-only screening): draws/finals/mains seen from >=1 km on fewer than 6 of 24 bearings: "
               f"{', '.join(s['id'] + ' ' + s['name'] for s in weak) if weak else 'none'}")
    return out, ok_all, weak


def coverage(sites):
    grid = {f"{c}{r}": [] for r in range(1, 5) for c in "ABCD"}
    for s in sites:
        grid[s["square"]].append(s)
    return grid


def ao_poly(pts, buf=450.0):
    ring = [(x + buf * np.cos(a), y + buf * np.sin(a)) for x, y in pts for a in np.linspace(0, 2 * np.pi, 16, endpoint=False)]
    ring = np.array(ring)
    return ring[ConvexHull(ring).vertices]


def plot(c, H, lines, sites, ops_out, grid, out):
    bounds = [-1e4] + [b[0] for b in BANDS]
    cmap = ListedColormap([b[1] for b in BANDS])
    norm = BoundaryNorm(bounds, cmap.N)
    shade = np.flipud(LightSource(315, 40).hillshade(np.flipud(H), vert_exag=6, dx=T.CELL, dy=T.CELL))
    rgb = cmap(norm(H))[..., :3] * (0.65 + 0.35 * shade[..., None])
    fig = plt.figure(figsize=(20, 16), dpi=100)
    ax = fig.add_axes([0.03, 0.04, 0.72, 0.9])
    ax.imshow(rgb, origin="lower", extent=[0, 16, 0, 16], interpolation="bilinear")
    for k in range(17):
        ax.axhline(k, color="k", lw=0.25, alpha=0.3)
        ax.axvline(k, color="k", lw=0.25, alpha=0.3)
    for k in (4, 8, 12):
        ax.axhline(k, color="w", lw=1.2, ls=":")
        ax.axvline(k, color="w", lw=1.2, ls=":")
    for sq, S in grid.items():
        cx, cy = "ABCD".index(sq[0]) * 4, (int(sq[1]) - 1) * 4
        ax.text(cx + 0.12, cy + 3.75, f"{sq}  {len(S)} sites", fontsize=9, color="w", weight="bold",
                bbox=dict(fc="#00000088", ec="none", pad=1))
    for pts, st in lines:
        a = np.array(pts) / 1000.0
        ax.plot(a[:, 0], a[:, 1], **{k: v for k, v in st.items() if k != "label"})
    for op in ops_out:
        col = OPC[op["op"] - 1]
        S = [s for s in sites if s["op"] == op["op"]]
        poly = ao_poly([s["xy"] for s in S]) / 1000.0
        ax.add_patch(Polygon(poly, closed=True, fill=False, ec=col, lw=2, ls="--"))
        ax.text(poly[:, 0].mean(), min(poly[:, 1].max() + 0.12, 15.75), f"OP {op['op']} (wk {op['week']}): {op['name']}",
                color=col, fontsize=9.5, ha="center", weight="bold", bbox=dict(fc="white", ec=col, alpha=0.85, pad=1.2))
        for s in S:
            sz = {"squad": 40, "two_squad": 95, "platoon": 190}[s["size"]]
            mk = "s" if s["air_prep"] else ("D" if s["air_only"] else "o")
            ax.scatter(s["xy"][0] / 1000, s["xy"][1] / 1000, s=sz, c=col, marker=mk,
                       edgecolors="white" if s["role"] == "supporting" else "k", linewidths=1.6 if s["role"] != "supporting" else 0.8, zorder=5)
            if s["draw"]:
                ax.scatter(s["xy"][0] / 1000, s["xy"][1] / 1000, s=900, marker="*",
                           c="#ff5a1f" if s["new_build"] else "#ffd23f", edgecolors="k", zorder=6)
                ax.text(s["xy"][0] / 1000 + 0.2, s["xy"][1] / 1000 - 0.35, f"{s['draw']} {s['name']}" + (" (NEW)" if s["new_build"] else ""),
                        fontsize=9, weight="bold", zorder=7, bbox=dict(fc="#fff8dc", ec="k", alpha=0.9, pad=1))
        sx, sy = op["start"]
        ax.scatter(sx / 1000, sy / 1000, marker="P", s=220, c=col, edgecolors="k", zorder=6)
        ax.text(sx / 1000 + 0.12, sy / 1000 + 0.12, f"S{op['op']}", fontsize=9, weight="bold", zorder=7)
    ax.plot([12.8, 14.8], [0.5, 0.5], color="k", lw=5)
    ax.plot([12.8, 13.8], [0.5, 0.5], color="w", lw=2.5)
    ax.text(13.8, 0.72, "2 km", ha="center", fontsize=11, weight="bold", bbox=dict(fc="white", ec="none", alpha=0.7, pad=1))
    ax.annotate("", xy=(15.4, 15.5), xytext=(15.4, 14.5), arrowprops=dict(facecolor="k", width=5, headwidth=14))
    ax.text(15.4, 14.25, "N", ha="center", fontsize=14, weight="bold")
    ax.set_xlim(0, 16); ax.set_ylim(0, 16); ax.set_xticks(range(17)); ax.set_yticks(range(17))
    ax.set_xlabel("km east"); ax.set_ylabel("km north")
    fig.text(0.03, 0.972, f"Swamp concept {c['key']}: {c['title']} (rev 2, PROPOSED)", fontsize=17, weight="bold")
    fig.text(0.03, 0.950, f"{c['setting']}. 16 x 16 km, water below 0 m. 8 ops / 4 weeks. Sketch for choosing; heights and positions ASSUMED, counts MEASURED.", fontsize=10)
    lax = fig.add_axes([0.765, 0.04, 0.23, 0.9]); lax.axis("off")
    hand = [Patch(fc=b[1], ec="k", label=b[2]) for b in BANDS]
    hand += [Line2D([], [], ls="", marker="o", ms=m, mfc="grey", mec="w", label=l) for m, l in ((6, "squad site"), (9, "two-squad site"), (13, "platoon site"))]
    hand += [Line2D([], [], ls="", marker="o", ms=10, mfc="grey", mec="k", mew=1.6, label="final / main (black ring)"),
             Line2D([], [], ls="", marker="s", ms=9, mfc="grey", mec="w", label="air-prep (populated from start)"),
             Line2D([], [], ls="", marker="D", ms=8, mfc="grey", mec="w", label="air-only"),
             Line2D([], [], ls="", marker="*", ms=20, mfc="#ff5a1f", mec="k", label="main draw, NEW build"),
             Line2D([], [], ls="", marker="*", ms=20, mfc="#ffd23f", mec="k", label="main draw, library cluster"),
             Line2D([], [], ls="", marker="P", ms=12, mfc="grey", mec="k", label="op start (S#)"),
             Line2D([], [], ls="--", color="grey", lw=2, label="op AO outline (no lanes, no order)")]
    seen = set()
    for _, st in lines:
        if st.get("label") and st["label"] not in seen:
            seen.add(st["label"])
            hand.append(Line2D([], [], color=st.get("color", "k"), ls=st.get("ls", "-"), lw=st.get("lw", 2), label=st["label"]))
    lax.legend(handles=hand, loc="upper left", fontsize=9, title="Legend (PROPOSED)")
    lax.text(0, 0.0, "White dotted lines: 4 x 4 km coverage squares\n(site count in each corner).\n"
             "AI never crosses water: every AI route uses\nland, a bridge or a dam crest.", fontsize=9, va="bottom")
    fig.savefig(out, dpi=100)
    plt.close(fig)


def optable(c, sites, ops_out):
    L = ["| Op | Week | After (any of) | Start | Draw | Final | Mains (command picks any 2 + the final) | Supporting | Sizes s/t/p | Air-prep / air-only | Planned garrison | FOB after |",
         "|---|---|---|---|---|---|---|---|---|---|---|---|"]
    for op in ops_out:
        S = [s for s in sites if s["op"] == op["op"]]
        fin = [s for s in S if s["role"] == "FINAL"][0]
        mains = [s for s in S if s["role"] == "main"]
        dr = next((f"{s['draw']} {s['name']}" for s in S if s["draw"]), "-")
        cnt = {k: sum(s["size"] == v for s in S) for k, v in SIZE.items()}
        L.append(f"| {op['op']} {op['name']} | {op['week']} | {', '.join(map(str, op['after_any_of'])) or 'opener'} | "
                 f"({op['start'][0] / 1000:.1f}, {op['start'][1] / 1000:.1f}) km | {dr} | {fin['name']} ({fin['size'].replace('_', '-')}) | "
                 f"{'; '.join(m['name'] + ' (' + m['size'].replace('_', '-') + ')' for m in mains)} | "
                 f"{sum(s['role'] == 'supporting' for s in S)} | {cnt['s']}/{cnt['t']}/{cnt['p']} | "
                 f"{sum(s['air_prep'] for s in S)} / {sum(s['air_only'] for s in S)} | {sum(s['garrison_planned'] for s in S)} | {op['fob']} |")
    return "\n".join(L)


def main():
    os.makedirs(os.path.join(ROOT, "swamp"), exist_ok=True)
    os.makedirs(os.path.join(HERE, "out"), exist_ok=True)
    rep = ["K3 checks (MEASURED by tools/make_k3.py on the sketch data)",
           "Per op: 1 final, mains + supporting >= 12, 12-16 supporting, all three sizes, 1-2 air-prep, <= 2 air-only,",
           "a platoon site before the final, planned garrison <= 1,200 if all filled at once (S 25 / 2S 50 / P 110 ASSUMED).",
           "Per map: 8 ops, 4-6 draws, 1-2 new-build centerpieces, exactly 1 capstone, 2-3 tunnel sites.", ""]
    cov_md = ["# COVERAGE: sites per 4 x 4 km square (K3, MEASURED on the sketch data)", "",
              "Columns A-D run west to east (4 km each), rows 1-4 south to north. Every site counts in the square it sits in.", ""]
    draws_md = ["# DRAWS: main draws per concept (K3, PROPOSED)", "",
                "Recon = terrain-only screening, MEASURED on the sketch: farthest seen / bearings (of 24) that see it from 1 km or more. "
                "Swamp trees are not modelled, so Stage B dressing must keep sight corridors open to each draw (ASSUMED).", ""]
    for key, c in CONCEPTS.items():
        H, lines, sites, ops_out, problems = build(c)
        chk, ok, weak = checks(c, sites, ops_out)
        grid = coverage(sites)
        rep += [f"Concept {key} {c['title']}:"] + chk + [f"  PROBLEM {p}" for p in problems] + [""]
        doc = {"map": "swamp", "concept": key, "title": c["title"], "revision": 2, "size_km": 16,
               "setting": c["setting"], "status": "PROPOSED sketch for choosing",
               "draws": [dict(id=k, name=v[0], build=v[1], make_up=v[2], story_reason=v[3]) for k, v in c["draws"].items()],
               "ops": ops_out, "sites": sites,
               "measured_or_assumed": "MEASURED by tools/make_k3.py on the sketch: counts, squares, landmass ids, ground heights, "
                                      "recon screening (terrain only). ASSUMED: every position (hand-placed, snapped to firm ground), "
                                      "garrison sizes (S 25 / 2S 50 / P 110), structure heights for recon (6/10/15 m, draws 30 m), "
                                      "library suitability."}
        with open(os.path.join(ROOT, "swamp", f"objectives_swamp_{key}.json"), "w") as f:
            json.dump(doc, f, indent=1)
        plot(c, H, lines, sites, ops_out, grid, os.path.join(ROOT, "swamp", f"plan_{key}.png"))
        tab = optable(c, sites, ops_out)
        open(os.path.join(HERE, "out", f"optable_{key}.md"), "w").write(tab + "\n")
        cpath = os.path.join(ROOT, "swamp", f"concept_{key}.md")
        if os.path.exists(cpath):
            s = open(cpath).read()
            if MARK_A in s:
                s = s[:s.index(MARK_A)] + MARK_A + "\n" + tab + "\n" + s[s.index(MARK_B):]
                open(cpath, "w").write(s)
        # coverage table
        cov_md += [f"## Concept {key}: {c['title']}", "", "| Row \\ Col | A (0-4 km) | B (4-8 km) | C (8-12 km) | D (12-16 km) |", "|---|---|---|---|---|"]
        for r in (4, 3, 2, 1):
            cells = []
            for col in "ABCD":
                S = grid[f"{col}{r}"]
                ops = sorted({s["op"] for s in S})
                cells.append(f"{len(S)} (ops {', '.join(map(str, ops))})" if S else "0 (see reason)")
            cov_md.append(f"| {r} ({(r - 1) * 4}-{r * 4} km) | " + " | ".join(cells) + " |")
        empty = [k for k, v in grid.items() if not v]
        cov_md += ["", f"Empty squares: {', '.join(empty) if empty else 'none'}. "
                       f"Fewest sites in one square: {min(len(v) for v in grid.values())}; most: {max(len(v) for v in grid.values())}.", ""]
        draws_md += [f"## Concept {key}: {c['title']}", "",
                     "| Draw | Area (square) | New build or library cluster | Make-up | Week(s) it serves | Story reason | Recon (max m / bearings >= 1 km) |",
                     "|---|---|---|---|---|---|---|"]
        for did, (nm, bld, make, why) in c["draws"].items():
            s = next(x for x in sites if x["draw"] == did)
            wk = next(o["week"] for o in ops_out if o["op"] == s["op"])
            draws_md.append(f"| {did} {nm} | {s["square"]} | {bld} | {make} | week {wk} (op {s['op']}) | {why} | {s['recon_max_m']} / {s['recon_bearings_1km']} of 24 |")
        draws_md.append("")
        print(f"{key}: {len(sites)} sites, ok={ok}, problems={problems}, weak recon={[w['id'] for w in weak]}")
    open(os.path.join(HERE, "out", "checks.txt"), "w").write("\n".join(rep) + "\n")
    open(os.path.join(ROOT, "COVERAGE.md"), "w").write("\n".join(cov_md) + "\n")
    open(os.path.join(ROOT, "DRAWS.md"), "w").write("\n".join(draws_md) + "\n")


if __name__ == "__main__":
    main()
