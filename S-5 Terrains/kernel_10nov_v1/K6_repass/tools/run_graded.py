"""Run one town config through the grader-backed engine (11 Nov); write layout JSON, our plan PNG, and the 11 Nov grader's
report.md / plan.png / buildings.csv / result.json for that layout.
Usage: python3 run_graded.py <config module> <catalogue.json> <out dir>"""
import importlib, json, math, sys, os
import numpy as np
from shapely.geometry import Polygon, Point
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon as MP, Patch
from matplotlib.lines import Line2D
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from town_grid import Town, Ground
from gtown import GTown, streets_json, windows_for, SITES, FIXED, GRID5, TG

mod = importlib.import_module(sys.argv[1]); CAT = {b["model_id"]: b for b in json.load(open(sys.argv[2]))["buildings"]}; OUT = sys.argv[3]
os.makedirs(OUT, exist_ok=True)
cfg = mod.CFG; G = Ground(cfg["tile"], *cfg["tile_origin"])
cfg.setdefault("site", next(k for k in SITES if cfg["key"].startswith(k)))
T = GTown(cfg, CAT, G, seed=cfg.get("seed", 11)); T.build_streets()
mod.build(T)
if T.GT is None: T.init_grader()
# trim to the share rules (grader twin groups): drop the latest-placed lane / main house of an over-share group; removal keeps the rest valid
import collections as _co
while True:
    n_ = len(T.B); cm_ = _co.Counter(b["model_id"] for b in T.B); ct_ = _co.Counter(TG.TWIN[b["model_id"]] for b in T.B)
    over = [m for m, v in cm_.items() if v > 0.15 * n_] + [g for g, v in ct_.items() if "+" in g and v > 0.12 * n_]
    if not over: break
    cand_ = [i for i, b in enumerate(T.B) if (b["model_id"] in over or TG.TWIN[b["model_id"]] in over) and b["role"] != "landmark"]
    if not cand_: print("share over, nothing to trim:", over); break
    k_ = max(cand_)
    print("trim for share:", T.B[k_]["id"], T.B[k_]["model_id"]); del T.B[k_]; del T.P[k_]
    T.GT.acc = [o for o in T.GT.acc if o["kid"] in {b["id"] for b in T.B}]
T.comps = [T.seat_comp(c) if c.get("footprint_m") and c.get("pad_z_m") is not None else c for c in T.comps]
print("refused while placing:", dict(T.refused), "placed", len(T.B))
T.pick_garrison(*cfg["garrison_range"], cfg.get("garrison_prio", {"square": 0, "quay": 1, "main": 2, "lane": 3}))
CHK = T.checks()
FAMC = {"naboo_dome": "#e9c98f", "white_or_pale_house": "#f7f5ef", "scifi": "#6c7fa3", "industrial": "#9aa3a8"}

def draw(ax, xl, yl, ids=False):
    H = G.H; xs = np.arange(G.x0, G.x0 + H.shape[1]); ys = np.arange(G.y0, G.y0 + H.shape[0])
    ax.contourf(xs, ys, H, levels=np.arange(-20, 500, 2), cmap="YlOrBr", alpha=0.35)
    ax.contour(xs, ys, H, levels=np.arange(0, 500, 2), colors="#8a7a60", linewidths=0.3)
    ax.contour(xs, ys, H, levels=np.arange(0, 500, 10), colors="#5a4a30", linewidths=0.8)
    ax.contourf(xs, ys, H, levels=[-50, 0], colors=["#9cc3dc"])
    for gx in np.arange(math.ceil(xl[0] / 5) * 5, xl[1], 5): ax.axvline(gx, color="#000", lw=0.15, alpha=0.18)
    for gy in np.arange(math.ceil(yl[0] / 5) * 5, yl[1], 5): ax.axhline(gy, color="#000", lw=0.15, alpha=0.18)
    for poly, z in T.extra_pads:
        if poly.geom_type == "Polygon": ax.add_patch(MP(np.array(poly.exterior.coords), fc="none", ec="#1b998b", lw=0.4, ls=":"))
    for k, st in T.streets.items():
        fc = {"main": "#d8d2c4", "lane": "#e6dfcf", "path": "#f3efe6"}[st["cls"]]
        ax.add_patch(MP(np.array(st["rib"].exterior.coords), fc=fc, ec="#6b6252", lw=0.6, ls="-" if st["cls"] != "path" else ":"))
        for sg in st["segments"] if st["cls"] != "path" else []:
            p = st["line"].interpolate((sg["s0"] + sg["s1"]) / 2)
            if xl[0] < p.x < xl[1] and yl[0] < p.y < yl[1]:
                ax.text(p.x, p.y, f"{sg['z']:.1f}", fontsize=6.5, color="#0b4f6c", ha="center", va="center", clip_on=True,
                        bbox=dict(fc="#ffffffcc", ec="none", pad=0.4))
    for extra in getattr(T, "draw_polys", []):
        poly, fc, ec, lab = extra; ax.add_patch(MP(np.array(poly.exterior.coords), fc=fc, ec=ec, lw=1.4, hatch=".." if "square" in lab else None))
    for c in [c for c in T.comps if c.get("footprint_m") and "yaw_deg" in c]:
        w_, d_ = c["footprint_m"]; a = math.radians(c["yaw_deg"]); ex = np.array([math.cos(a), -math.sin(a)]); ez = np.array([math.sin(a), math.cos(a)]); cc = np.array([c["x"], c["y"]])
        ax.add_patch(MP(np.array([cc + w_ / 2 * ex + d_ / 2 * ez, cc - w_ / 2 * ex + d_ / 2 * ez, cc - w_ / 2 * ex - d_ / 2 * ez, cc + w_ / 2 * ex - d_ / 2 * ez]), fc="none", ec="#d63384", lw=1.3, ls="--"))
    for b, q in zip(T.B, T.P):
        m = T.CAT[b["model_id"]]
        ax.add_patch(MP(np.array(q.exterior.coords), fc=FAMC[m["family"]], ec="#d7263d" if b["garrison"] else "#222", lw=1.8 if b["garrison"] else 0.6))
        a = math.radians(b["door_bearing_deg"]); half = (m["depth_m"] if b["door_side"] in ("front", "back") else m["width_m"]) / 2
        dx, dy = b["x"] + half * math.sin(a), b["y"] + half * math.cos(a)
        ax.plot([dx, dx + 2.2 * math.sin(a)], [dy, dy + 2.2 * math.cos(a)], color="#0b6e4f", lw=1.5)
        if m["tall"]: ax.plot(b["x"], b["y"], marker="^", ms=7, color="k")
        if ids: ax.text(b["x"], b["y"], b["id"][1:], fontsize=5, ha="center", va="center", clip_on=True)
    lm = [b for b in T.B if b["role"] == "landmark"]
    if lm: ax.plot(lm[0]["x"], lm[0]["y"], "*", ms=16, color="#ffd23f", mec="k")
    ax.set_xlim(*xl); ax.set_ylim(*yl); ax.set_aspect("equal")

fig = plt.figure(figsize=(18, 13), dpi=110)
ax = fig.add_axes([0.04, 0.06, 0.62, 0.86]); xl, yl = cfg["view"]
draw(ax, xl, yl, ids=True)
ax.plot([xl[1] - 110, xl[1] - 10], [yl[0] + 10, yl[0] + 10], "k-", lw=4); ax.text(xl[1] - 60, yl[0] + 15, "100 m", ha="center", fontsize=10, weight="bold")
ax.annotate("", xy=(xl[1] - 12, yl[1] - 8), xytext=(xl[1] - 12, yl[1] - 40), arrowprops=dict(facecolor="k", width=4, headwidth=12))
ax.text(xl[1] - 12, yl[1] - 52, "N", ha="center", fontsize=12, weight="bold")
ax.set_xlabel("x east (m, map frame)"); ax.set_ylabel("y north (m, map frame)")
for lab, (x, y) in cfg.get("labels", {}).items(): ax.text(x, y, lab, fontsize=8.5, color="#7a1f0f", weight="bold", clip_on=True, bbox=dict(fc="#fff8", ec="none", pad=0.6))
if "inset" in cfg:
    ax2 = fig.add_axes([0.69, 0.50, 0.30, 0.42]); draw(ax2, *cfg["inset"]["view"], ids=True); ax2.set_title(cfg["inset"]["title"], fontsize=10)
lax = fig.add_axes([0.69, 0.04, 0.30, 0.43]); lax.axis("off")
hand = [Patch(fc=FAMC[f], ec="#222", label=f.replace("_", " ")) for f in FAMC] + [
    Patch(fc="none", ec="#d7263d", lw=2, label="garrison (enterable)"), Line2D([], [], color="#0b6e4f", lw=2, label="door (tick points out)"),
    Line2D([], [], ls="", marker="^", color="k", label="tall piece (> 14 m)"), Line2D([], [], ls="", marker="*", ms=12, color="#ffd23f", mec="k", label="landmark"),
    Patch(fc="#f3e6c4", ec="#7b2cbf", hatch="..", label="square (one level)"), Patch(fc="none", ec="#d63384", ls="--", label="comp footprint"),
    Patch(fc="none", ec="#1b998b", ls=":", label="level street segment (pad)"), Patch(fc="#d8d2c4", ec="#6b6252", label="street (blue number = level, m)"),
    Line2D([], [], color="#000", lw=0.4, alpha=0.4, label="5 m height grid")]
lax.legend(handles=hand, loc="upper left", fontsize=8.5)
c = CHK
lax.text(0, 0.0, (f"MEASURED on the {cfg['ground_label']}:\nbuildings {c['counts']['buildings']}, garrison {c['counts']['garrison']} (enterable {c['counts']['enterable']}), pad levels {c['counts']['pad_levels']}\n"
                  f"grid points claimed by two levels: {c['grid_points_claimed_by_two_levels']}\n"
                  f"different-level pairs closer than 14-17 m: {c['different_level_pairs_closer_than_required']}\n"
                  f"pad cut/fill: median {c['pad_cut_fill_m']['median']} m, max {c['pad_cut_fill_m']['max']} m\n"
                  f"overlaps {c['overlaps']['building_pairs']}; into streets {c['overlaps']['building_vs_street']}; corners < 2 m {c['corner_houses_within_2m_of_a_cross_street']}\n"
                  f"doors off a street/square/quay: {c['door_check']['fail']}; largest twin group {c['model_share']['largest_twin_group'][1]} %"),
         fontsize=9, family="monospace", va="bottom")
fig.text(0.04, 0.955, cfg["title"], fontsize=15, weight="bold")
fig.savefig(os.path.join(OUT, cfg["key"] + "_plan.png"), dpi=110); plt.close(fig)
layout = {"town": cfg["town"], "version": cfg["version"],
          "frame": {"units": "metres", "x": "east", "y": "north", "origin": "map south-west corner", "yaw": "degrees clockwise from north"},
          "streets": T.LAY_streets,
          "buildings": T.B, "square": T.square_out, "walls": [], "comps": T.comps, "notes": cfg["notes"]}
if T.square_out and T.LAY_square: T.square_out = dict(T.square_out, polygon=T.LAY_square["polygon"], level_z_m=T.LAY_square["level_z_m"])
layout["square"] = T.square_out
json.dump(layout, open(os.path.join(OUT, cfg["key"] + "_layout.json"), "w"), indent=1)
_f, _x0, _y0 = SITES[cfg["site"]]
_args = [os.path.join(OUT, cfg["key"] + "_layout.json"), "--grid5", os.path.join(GRID5, _f), str(_x0), str(_y0), "--out", os.path.join(OUT, "grader_" + cfg["key"])]
if cfg["site"] in FIXED: _args += ["--fixed", FIXED[cfg["site"]]]
print("GRADER:", " ".join(_args)); _rc = TG.main(_args); print("grader exit code", _rc)
json.dump(CHK, open(os.path.join(OUT, cfg["key"] + "_checks.json"), "w"), indent=1)
print(json.dumps({k: CHK[k] for k in ("counts", "grid_points_claimed_by_two_levels", "different_level_pairs_closer_than_required", "closest_different_level_pair_m",
                                      "pad_cut_fill_m", "overlaps", "corner_houses_within_2m_of_a_cross_street", "model_share", "lane_end_level_mismatch_m")}, indent=0))
print({k: (v["max_grade_pct"], v["average_grade_pct"], v["max_cut_m"], v["max_fill_m"], v["segments"]) for k, v in CHK["street_grades"].items()})
print(CHK["straight_runs_m"], "door fails", CHK["door_check"]["fail"], CHK["door_check"]["door_level_off_street_over_0_75m"][:5])
print("rejects", dict(T.log))
