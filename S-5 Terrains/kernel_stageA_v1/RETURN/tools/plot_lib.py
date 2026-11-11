"""Plan-view sketch renderer (PROPOSED concept sketches, for choosing only)."""
import json
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap, BoundaryNorm, LightSource
from matplotlib.patches import Patch, Polygon
from matplotlib.lines import Line2D
from scipy.spatial import ConvexHull

import terrain_lib as T

ISLAND_BANDS = [  # (upper bound m, colour, label)
    (-15, "#0b2a4a", "deep water (< -15 m): air only"),
    (-3, "#1f5f8b", "boat water (-15 to -3 m)"),
    (-1.3, "#3f9cc4", "shallow, swim (-3 to -1.3 m)"),
    (0, "#8fd6d6", "reef / wade (-1.3 to 0 m)"),
    (3, "#efe2b0", "beach / flat (0 to 3 m)"),
    (25, "#9cc77a", "low land (3 to 25 m)"),
    (80, "#5f9c4f", "hills (25 to 80 m)"),
    (200, "#7e8a52", "high ground (80 to 200 m)"),
    (400, "#8c7556", "crags (200 to 400 m)"),
    (9999, "#e9e3da", "peaks (> 400 m)"),
]

SWAMP_BANDS = [
    (-1.3, "#1d4f6e", "channel, swim or boat (< -1.3 m)"),
    (-0.5, "#3d86a8", "deep wade (-1.3 to -0.5 m)"),
    (0, "#86c2c4", "shallow wade / slough (-0.5 to 0 m)"),
    (0.5, "#a7a777", "wet ground, mud (0 to 0.5 m)"),
    (1.5, "#9cbf6e", "firm ground (0.5 to 1.5 m)"),
    (3, "#6c9f4a", "hammock / levee (1.5 to 3 m)"),
    (10, "#7d8a4b", "rise (3 to 10 m)"),
    (30, "#9a8460", "ridge (10 to 30 m)"),
    (9999, "#d9d0c0", "hills (> 30 m)"),
]

SIZE_DOT = {"squad": 70, "two_squad": 170, "platoon": 340}
OP_COLOURS = ["#d7263d", "#f49d37", "#7b2cbf", "#1b998b", "#2e294e", "#c5d86d"]


def ao_polygon(pts, buffer_m=450.0):
    ring = []
    for x, y in pts:
        for a in np.linspace(0, 2 * np.pi, 16, endpoint=False):
            ring.append((x + buffer_m * np.cos(a), y + buffer_m * np.sin(a)))
    ring = np.array(ring)
    hull = ConvexHull(ring)
    return ring[hull.vertices]


def render(H, bands, ops, labels, title, subtitle, out_png, extra_lines=None):
    bounds = [-1e4] + [b[0] for b in bands]
    cmap = ListedColormap([b[1] for b in bands])
    norm = BoundaryNorm(bounds, cmap.N)
    ls = LightSource(azdeg=315, altdeg=40)
    rgb = cmap(norm(H))[..., :3]
    shade = ls.hillshade(np.flipud(H), vert_exag=3, dx=T.CELL, dy=T.CELL)
    shade = np.flipud(shade)
    land = (H > 0)[..., None]
    rgb = np.where(land, rgb * (0.55 + 0.45 * shade[..., None]), rgb * (0.85 + 0.15 * shade[..., None]))

    fig = plt.figure(figsize=(20, 16), dpi=100)
    ax = fig.add_axes([0.03, 0.04, 0.72, 0.9])
    ax.imshow(rgb, origin="lower", extent=[0, 16, 0, 16], interpolation="bilinear")
    for k in range(17):
        ax.axhline(k, color="k", lw=0.3, alpha=0.35)
        ax.axvline(k, color="k", lw=0.3, alpha=0.35)
    ax.set_xticks(range(0, 17)); ax.set_yticks(range(0, 17))
    ax.set_xlabel("km east"); ax.set_ylabel("km north")
    ax.set_xlim(0, 16); ax.set_ylim(0, 16)

    if extra_lines:
        for pts, style in extra_lines:
            a = np.array(pts) / 1000.0
            ax.plot(a[:, 0], a[:, 1], **style)

    for i, op in enumerate(ops):
        col = OP_COLOURS[i % len(OP_COLOURS)]
        pts = [o["xy"] for o in op["objectives"]]
        poly = ao_polygon(pts) / 1000.0
        ax.add_patch(Polygon(poly, closed=True, fill=False, ec=col, lw=2.2, ls="--"))
        cx, cy = poly[:, 0].mean(), poly[:, 1].max()
        ax.text(cx, min(cy + 0.15, 15.7), f"OP {op['op']}: {op['name']}", color=col,
                fontsize=10, ha="center", weight="bold",
                bbox=dict(fc="white", ec=col, alpha=0.8, pad=1.5))
        for o in op["objectives"]:
            ax.scatter(o["xy"][0] / 1000, o["xy"][1] / 1000, s=SIZE_DOT[o["size"]],
                       c=col, edgecolors="white", linewidths=1.0, zorder=5)
        sx, sy = op["start"]
        ax.scatter(sx / 1000, sy / 1000, marker="*", s=420, c=col, edgecolors="k", zorder=6)
        ax.text(sx / 1000 + 0.12, sy / 1000 - 0.25, f"S{op['op']}", color="k", fontsize=9, weight="bold", zorder=6)

    for name, x, y in labels:
        ax.text(x / 1000, y / 1000, name, fontsize=9, style="italic", ha="center",
                color="#111", bbox=dict(fc="#ffffffaa", ec="none", pad=0.8), zorder=4)

    # scale bar (2 km) and north arrow
    ax.plot([12.8, 14.8], [0.5, 0.5], color="k", lw=5)
    ax.plot([12.8, 13.8], [0.5, 0.5], color="w", lw=2.5)
    ax.text(13.8, 0.72, "2 km", ha="center", fontsize=11, weight="bold",
            bbox=dict(fc="white", ec="none", alpha=0.7, pad=1))
    ax.annotate("", xy=(15.3, 15.6), xytext=(15.3, 14.6),
                arrowprops=dict(facecolor="k", width=5, headwidth=14))
    ax.text(15.3, 14.35, "N", ha="center", fontsize=14, weight="bold")

    fig.text(0.03, 0.972, title, fontsize=17, weight="bold")
    fig.text(0.03, 0.950, subtitle, fontsize=10)

    lax = fig.add_axes([0.77, 0.04, 0.22, 0.9]); lax.axis("off")
    hand = [Patch(fc=b[1], ec="k", label=b[2]) for b in bands]
    hand += [Line2D([], [], ls="", marker="o", ms=s ** 0.5 / 1.6, mfc="grey", mec="w", label=f"{k.replace('_', '-')} objective")
             for k, s in SIZE_DOT.items()]
    hand += [Line2D([], [], ls="", marker="*", ms=16, mfc="grey", mec="k", label="op start (S#)"),
             Line2D([], [], ls="--", color="grey", lw=2, label="op AO outline")]
    if extra_lines:
        seen = set()
        for _, st in extra_lines:
            if st.get("label") and st["label"] not in seen:
                seen.add(st["label"])
                hand.append(Line2D([], [], color=st.get("color", "k"), ls=st.get("ls", "-"), lw=st.get("lw", 2), label=st["label"]))
    lax.legend(handles=hand, loc="upper left", fontsize=10, frameon=True, title="Legend (sketch, PROPOSED)")
    lax.text(0, 0.02, "Sketch height field: 16 m cells, hand-placed features + noise.\n"
             "For choosing a concept only. Not a heightmap.\n"
             "No lanes or suggested order are shown (house rule).\n"
             "Dot colour = op. Dot size = objective size.", fontsize=9, va="bottom")
    fig.savefig(out_png, dpi=100)
    plt.close(fig)
