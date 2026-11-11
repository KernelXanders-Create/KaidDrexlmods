"""K0: measure Perys v4 (their layout) on the natural ground. Read-only analysis."""
import json, math, sys, collections
import numpy as np
from shapely.geometry import Polygon, LineString, Point
from shapely.ops import unary_union

P = sys.argv[1]
L = json.load(open(sys.argv[3]))
C = {b["model_id"]: b for b in json.load(open(P + "/catalogue/buildings.json"))["buildings"]}
H = np.load(P + "/perys/height_perys_natural_1m.npy"); X0, Y0 = 4880, 2950

def h(x, y): return float(H[int(round(y - Y0)), int(round(x - X0))])

def foot(b):
    m = C[b["model_id"]]; a = math.radians(b["yaw_deg"])
    ex = np.array([math.cos(a), -math.sin(a)]); ez = np.array([math.sin(a), math.cos(a)])
    c = np.array([b["x"], b["y"]]); w, d = m["width_m"] / 2, m["depth_m"] / 2
    return Polygon([c + w * ex + d * ez, c - w * ex + d * ez, c - w * ex - d * ez, c + w * ex - d * ez])

B = L["buildings"]; F = [foot(b) for b in B]
S = {s["id"]: s for s in L["streets"]}
S = {k: v for k, v in S.items() if k != "HR"}
lines = {k: LineString(s["points"]) for k, s in S.items()}
ribbons = {k: lines[k].buffer(S[k]["width_m"] / 2, cap_style=2) for k in S}
out = {}
n = len(B)
# 1 gaps and touching blocks
gaps = []
adj = collections.defaultdict(set)
for i in range(n):
    dmin = min(F[i].distance(F[j]) for j in range(n) if j != i)
    gaps.append(dmin)
    for j in range(i + 1, n):
        if F[i].distance(F[j]) < 1.0:
            adj[i].add(j); adj[j].add(i)
seen = set(); comps = []
for i in range(n):
    if i in seen: continue
    st = [i]; g = []
    while st:
        k = st.pop()
        if k in seen: continue
        seen.add(k); g.append(k); st += list(adj[k])
    comps.append(g)
out["nearest_gap_m"] = dict(median=round(float(np.median(gaps)), 2), p25=round(float(np.percentile(gaps, 25)), 2), p75=round(float(np.percentile(gaps, 75)), 2))
out["touching_lt1m_share_in_groups_of_3plus"] = round(100 * sum(len(g) for g in comps if len(g) >= 3) / n, 1)
out["touching_groups_sizes"] = sorted([len(g) for g in comps if len(g) > 1], reverse=True)
# 2 alignment to street tangent and setback
devs, setbacks, per_street = [], collections.defaultdict(list), collections.defaultdict(list)
for b, f in zip(B, F):
    k = b.get("street")
    if k not in lines: continue
    ln = lines[k]; p = Point(b["x"], b["y"]); s = ln.project(p)
    q1, q2 = ln.interpolate(max(s - 2, 0)), ln.interpolate(min(s + 2, ln.length))
    tang = math.degrees(math.atan2(q2.x - q1.x, q2.y - q1.y)) % 180   # bearing of tangent
    door = (b.get("door_bearing_deg", b["yaw_deg"])) % 180
    dv = abs(((door - tang) % 180) - 90)         # 0 = door square to the street
    devs.append(dv)
    sb = f.distance(ribbons[k]); setbacks[k].append(sb)
    per_street[k].append((s, b))
out["door_square_to_street_deg"] = dict(median=round(float(np.median(devs)), 1), share_within_2deg=round(100 * np.mean(np.array(devs) < 2), 1))
allsb = [x for v in setbacks.values() for x in v]
out["setback_from_ribbon_m"] = dict(median=round(float(np.median(allsb)), 2), p90=round(float(np.percentile(allsb, 90)), 2), share_over_1m=round(100 * np.mean(np.array(allsb) > 1.0), 1))
# 3 street-wall continuity: share of each street's edge length that has a building within 2 m of the ribbon
cont = {}
for k, ln in lines.items():
    if S[k]["class"] == "path": continue
    hit = tot = 0
    nn = int(ln.length // 2)
    for side in (1, -1):
        off = ln.parallel_offset(S[k]["width_m"] / 2 + 1.5, "left" if side > 0 else "right")
        for i in range(nn):
            pt = off.interpolate(i / max(nn - 1, 1), normalized=True)
            tot += 1; hit += any(f.distance(pt) < 2.0 for f in F)
    cont[k] = (S[k]["class"], round(ln.length), round(100 * hit / tot))
out["street_wall_continuity_pct"] = cont
# 4 model shares and same-model neighbours
cnt = collections.Counter(b["model_id"] for b in B)
out["top_models"] = [(m, c, round(100 * c / n, 1)) for m, c in cnt.most_common(6)]
same_nb = 0
for i in range(n):
    j = min((j for j in range(n) if j != i), key=lambda j: F[i].distance(F[j]))
    same_nb += B[i]["model_id"][:2] == B[j]["model_id"][:2] and C[B[i]["model_id"]]["family"] == C[B[j]["model_id"]]["family"] and B[i]["model_id"] in ("ND01", "ND02") and B[j]["model_id"] in ("ND01", "ND02")
out["ND01_ND02_next_to_ND01_ND02"] = same_nb
fam = collections.Counter(C[b["model_id"]]["family"] for b in B)
out["families"] = dict(fam)
# 5 square
sq = Polygon(L["square"]["polygon"]); out["square_area_m2"] = round(sq.area)
comp_area = sum(c["footprint_m"][0] * c["footprint_m"][1] for c in L["comps"] if Point(c["x"], c["y"]).within(sq))
out["square_comp_cover_pct"] = round(100 * comp_area / sq.area, 1)
lm = next(f for b, f in zip(B, F) if b["id"] == L["square"]["landmark_building_id"])
sq = Polygon(L["square"]["polygon"])
out["landmark_distance_to_square_m"] = round(lm.distance(sq), 1)
near_sq = [b for b, f in zip(B, F) if f.distance(sq) < 6]
out["buildings_within_6m_of_square"] = len(near_sq)
# 6 cut/fill
cuts, fills = [], []
for b, f in zip(B, F):
    pz = b["pad_z_m"]; g = f.buffer(1.5, join_style=2)
    x0, y0, x1, y1 = g.bounds; vals = []
    for yy in range(int(y0), int(y1) + 1):
        for xx in range(int(x0), int(x1) + 1):
            if g.contains(Point(xx, yy)): vals.append(h(xx, yy))
    cuts.append(max(vals) - pz); fills.append(pz - min(vals))
cf = np.maximum(np.maximum(cuts, 0), np.maximum(fills, 0))
out["cut_or_fill_max_m"] = dict(median=round(float(np.median(cf)), 2), max=round(float(cf.max()), 2), share_over_2_5=round(100 * np.mean(cf > 2.5), 1))
pads = sorted(set(round(b["pad_z_m"], 1) for b in B)); out["distinct_pad_levels"] = len(pads)
# 7 walls
wl = sum(LineString(w["points"]).length for w in L["walls"]); out["retaining_wall_total_m"] = round(wl)
# 8 street widths vs building height (canyon ratio)
hh = [C[b["model_id"]]["height_m"] for b in B if not C[b["model_id"]]["tall"]]
out["median_low_building_height_m"] = round(float(np.median(hh)), 1)
# 9 parallel main streets: spacing between MS and KR and MR centrelines
def mean_sep(a, b):
    la, lb = lines[a], lines[b]; return round(float(np.median([lb.distance(la.interpolate(t, normalized=True)) for t in np.linspace(0.1, 0.9, 30)])), 1)
out["parallel_main_street_spacing_m"] = {f"{a}-{b}": mean_sep(a, b) for a, b in (("M", "U"), ("M", "K"), ("M", "K2")) if a in lines and b in lines}
# 10 rows field
out["row_field"] = dict(collections.Counter(b.get("row") for b in B))
out["street_field"] = dict(collections.Counter(b.get("street") for b in B))
json.dump(out, open(sys.argv[2], "w"), indent=1)
print(json.dumps(out, indent=1))

# ---- figure: v4 with bare street edges in red, pads coloured by level
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon as MP
fig, ax = plt.subplots(figsize=(12, 11), dpi=110)
xs = np.arange(X0, X0 + H.shape[1]); ys = np.arange(Y0, Y0 + H.shape[0])
ax.contour(xs, ys, H, levels=np.arange(0, 120, 2), colors="#999", linewidths=0.4)
ax.contour(xs, ys, H, levels=np.arange(0, 120, 10), colors="#555", linewidths=0.8)
for k, r in ribbons.items():
    ax.add_patch(MP(np.array(r.exterior.coords), fc="#cfcfcf", ec="#777", lw=0.5))
levels = sorted(set(round(b["pad_z_m"],1) for b in B)); cm = plt.get_cmap("viridis")
for b, f in zip(B, F):
    ax.add_patch(MP(np.array(f.exterior.coords), fc=cm(levels.index(round(b["pad_z_m"],1)) / max(len(levels) - 1, 1)), ec="k", lw=0.5))
for k, ln in lines.items():
    if S[k]["class"] == "path": continue
    for side in ("left", "right"):
        off = ln.parallel_offset(S[k]["width_m"] / 2 + 1.5, side)
        nn = int(off.length // 2)
        for i in range(nn):
            pt = off.interpolate(i / max(nn - 1, 1), normalized=True)
            if not any(f.distance(pt) < 2.0 for f in F):
                ax.plot(pt.x, pt.y, ".", color="#d7263d", ms=2.5)
ax.add_patch(MP(np.array(sq.exterior.coords), fc="none", ec="#7b2cbf", lw=2))
ax.plot(*lm.centroid.coords[0], "*", ms=18, color="#ffd23f", mec="k")
ax.annotate("landmark (ND07) on the square", lm.centroid.coords[0], xytext=(20, -30), textcoords="offset points", fontsize=9)
ax.set_xlim(5050, 5450); ax.set_ylim(3180, 3480); ax.set_aspect("equal")
ax.set_title("Perys v5 (Kernel K5) over natural ground, K0 read-checks\nred dots = street edge with no building within 2 m; pad colour = pad level (only %d levels for %d buildings)" % (len(levels), n), fontsize=10)
ax.plot([5330, 5430], [3190, 3190], "k-", lw=4); ax.text(5380, 3195, "100 m", ha="center")
ax.set_xlabel("x east (m, map frame)"); ax.set_ylabel("y north (m, map frame)")
fig.savefig(sys.argv[2].replace(".json", "_figure.png"), bbox_inches="tight"); print("figure ok")
