"""Re-pass of the BUILT ops 1 and 2: keep everything that passes, fix what fails (12 Nov rules, measured on the build-4 grid).
Fixes: a road for any vehicle site without one; stubs where a road stops short of its pad; squad pads re-seated where they overlap a pad
or sit within 3 m of a road edge; long straights given a gentle side-to-side wave; a main road re-held to 10 %.
Usage: python3 repass12.py <op 1|2> <out dir>"""
import sys, os, json, math, collections
import numpy as np
from shapely.geometry import Polygon, LineString, Point
from shapely.ops import unary_union
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "../job1/tools"))
import world, planner
from planner import rect

OP = int(sys.argv[1]); OUT = sys.argv[2]; os.makedirs(OUT, exist_ok=True)
PK = world.PACK; H = world.H()
OBJ = {s["id"]: s for s in world.objectives()["sites"]}
BOX = {1: (800, 8300, 300, 5200), 2: (11400, 18200, 800, 4400)}[OP]
P = planner.Plan(BOX); P.band_range = 99.0; P.steep = 0.8; P.repair_to = 3.6
log = []

PADS = []
for f in ("pads_op1", "pads_op2"):
    for p in json.load(open(os.path.join(PK, "ops_1_2", f + ".json")))["pads"]:
        hx = p.get("hx") or p.get("hu"); hy = p.get("hy") or (p.get("hv") / 2 if p.get("hv") else None)
        if BOX[0] - 300 < p["x"] < BOX[1] + 300 and BOX[2] - 300 < p["y"] < BOX[3] + 300:
            PADS.append(dict(p, hx=hx, hy=hy, yaw=p.get("yaw", 0.0), key=f"{p['site']}@{p['x']:.0f},{p['y']:.0f}"))
ROADS = [dict(r, idx=i) for i, r in enumerate(json.load(open(os.path.join(PK, "ground", "roads_ops_1_2.json"))))
         if r["kind"] in ("dirt", "main") and f"(ao{OP})" in r.get("src", "")]


def poly(p, grow=0.0): return Polygon(rect(p["x"], p["y"], p["hx"], p["hy"], p["yaw"], grow))


def block_pad(p):
    c_ = rect(p["x"], p["y"], p["hx"] + 1.5, p["hy"] + 1.5, p["yaw"]); pol_ = Polygon(c_)
    P.add_area(p["key"], [tuple(q) for q in c_], None)
    gx_, gy_ = np.meshgrid(np.arange(int(min(c_[:, 0]) // 5), int(max(c_[:, 0]) // 5) + 2) * 5.0, np.arange(int(min(c_[:, 1]) // 5), int(max(c_[:, 1]) // 5) + 2) * 5.0)
    P.add_buildings(p["key"], [(a, b) for a, b in zip(gx_.ravel(), gy_.ravel()) if pol_.contains(Point(a, b))], r=0.0)
    J, I = np.nonzero(P.owner == p["key"]); P.fixed[J, I] = p["z"]


def as_road(r, pts=None, zs=None, rid=None):
    X = np.array(pts if pts is not None else r["points"], float)
    Z = zs if zs is not None else [round(world.z(x, y), 3) for x, y in X]
    return dict(id=rid or f"{r['link']}#{r['idx']}", kind=r["kind"], width_m=10.0 if r["kind"] == "main" else 7.0, links=r["link"].split("-through")[0].split("-", 2)[:2] if "-" in r["link"] else [r["link"]],
                points=[[round(float(x), 2), round(float(y), 2)] for x, y in X], points_z=[round(float(z), 3) for z in Z])


def straight(X, tol=1.0):
    X = np.array(X, float); best = 0.0; i = 0
    for j in range(2, len(X)):
        a, b = X[i], X[j]; ab = b - a; L = np.hypot(*ab)
        if L < 1e-6: continue
        q = X[i + 1:j] - a; d = np.abs(ab[0] * q[:, 1] - ab[1] * q[:, 0]) / L
        if (d > tol).any(): i = j - 1
        else: best = max(best, L)
    return best


def worst_grade(X, Z):
    X = np.array(X, float); Z = np.array(Z, float); sg = np.hypot(*np.diff(X, axis=0).T); s = np.r_[0, np.cumsum(sg)]; w = float((np.abs(np.diff(Z)) / np.maximum(sg, 1e-9)).max())
    for b in (10.0, 20.0):
        for i in range(len(s)):
            j = np.searchsorted(s, s[i] + b)
            if j < len(s): w = max(w, abs(Z[j] - Z[i]) / (s[j] - s[i]))
    return round(100 * w, 2)


# ---- fixed ground: every built pad and road of ops 1-2 in the box
RESEAT = []                     # squad pads that overlap a pad (< 12 m) or sit within 3 m of a road edge
built = [as_road(r) for r in ROADS]
for p in PADS:
    if not p["site"].startswith("A"): continue
    others = [q for q in PADS if q is not p and q["site"] != p["site"]]
    gap = min(poly(p).distance(poly(q)) for q in others) if others else 1e9
    rgap = min(poly(p).distance(LineString(r["points"]).buffer(r["width_m"] / 2)) for r in built) if built else 1e9
    if gap < 12.0 or rgap < 3.0: RESEAT.append(dict(key=p["key"], site=p["site"], pad_gap_m=round(gap, 1), road_gap_m=round(rgap, 1)))
reseat_keys = {x["key"] for x in RESEAT}
for p in PADS:
    if p["key"] not in reseat_keys: block_pad(p)
for r in built: P.commit_road(r)
P.roads = []

# ---- 1. squad pads re-seated (same composition and size, nearest seat that holds every rule)
moves = []
for x in RESEAT:
    p = next(q for q in PADS if q["key"] == x["key"])
    s = None
    for rad in (40, 80, 160):
        s = P.add_site(p["site"], "squad position", p["comp"], p["hx"], p["hy"], p["x"], p["y"], rad, size_note="your built pad, re-seated", step=5.0)
        if s: break
    if s is None: log.append(f"{p['site']}: no seat within 160 m"); continue
    moves.append(dict(site=p["site"], comp=p["comp"], why=f"{'overlaps a pad' if x['pad_gap_m'] < 12 else ''}{' and ' if x['pad_gap_m'] < 12 and x['road_gap_m'] < 3 else ''}{'within 3 m of a road edge' if x['road_gap_m'] < 3 else ''} (pad gap {x['pad_gap_m']} m, road gap {x['road_gap_m']} m)",
                      old=dict(x=p["x"], y=p["y"], z=p["z"], yaw=p["yaw"]), new=dict(x=s["x"], y=s["y"], z=s["z"], yaw=s["yaw"], max_change_m=s["max_change_m"]), moved_m=round(math.dist((p["x"], p["y"]), (s["x"], s["y"])), 1)))

# ---- 2. vehicle sites with no road, and roads that stop short of their pad
PM = open(os.path.join(PK, "design", "PURPOSE_MAP.md"), encoding="utf-8").read()
def vehicle(sid):
    ln = [l for l in PM.split("\n") if l.startswith(f"| {sid} |")]
    return bool(ln) and "vehicles" in ln[0].split("|")[-2]
new_roads = []
def level_nodes(r):
    X = np.array(r["points"], float); Z = np.array(r["points_z"], float); s_ = np.r_[0, np.cumsum(np.hypot(*np.diff(X, axis=0).T))]; out = []
    for k in range(0, len(X), 3):
        m = np.abs(s_ - s_[k]) <= 15.0
        if s_[k] >= 15 and s_[-1] - s_[k] >= 15 and np.ptp(Z[m]) <= 0.2: out.append((float(X[k, 0]), float(X[k, 1]), float(Z[k]), r["id"]))
    return out
def pad_edges(p, owner):
    a_ = math.radians(p["yaw"]); ex_ = np.array([math.cos(a_), -math.sin(a_)]); ey_ = np.array([math.sin(a_), math.cos(a_)]); out = []
    for v_, h_ in ((ex_, p["hx"]), (-ex_, p["hx"]), (ey_, p["hy"]), (-ey_, p["hy"])):
        q_ = np.array([p["x"], p["y"]]) + v_ * (h_ + 4.0); out.append((float(q_[0]), float(q_[1]), p["z"], owner, v_))
    return out
on_net = [p for p in PADS if not p["site"].startswith("A") and p.get("kind") != "pass profile" and min(poly(p).distance(LineString(r["points"])) for r in built) <= 15.0]
NODES = [n for r in built for n in level_nodes(r)] + [(e[0], e[1], e[2], e[3]) for p in on_net for e in pad_edges(p, p["key"])]     # only pads a road already serves
for p in PADS:
    if p["site"].startswith("A") or p["site"].split("-T")[0] not in OBJ or not vehicle(p["site"]): continue
    pol = poly(p)
    near = sorted((pol.distance(LineString(r["points"])), r["id"], r) for r in built)
    if near and near[0][0] <= 15.0: continue
    if p.get("kind") == "pass profile": log.append(f"{p['site']}: a pass-profile pad (its level runs along it); its road ends {near[0][0]:.0f} m off the pad's centre level edge: check the profile end"); continue
    if near and near[0][0] <= 60.0:               # a road that stops short: a stub routed from the pad's nearest edge to the road's end
        r = near[0][2]; ends = [(np.array(r["points"][0]), r["points_z"][0]), (np.array(r["points"][-1]), r["points_z"][-1])]; end, endz = min(ends, key=lambda e: pol.distance(Point(e[0])))
        stub = None
        for e in sorted(pad_edges(p, p["key"]), key=lambda q: math.dist(q[:2], end))[:3]:
            st_ = P.route(tuple(np.array(e[:2]) + e[4] * 8.0), tuple(end), za=p["z"], zb=endz, name=f"stub {p['site']}", kind="dirt", links=[p["site"], r["id"]], margin=300, pre=[tuple(np.array(e[:2]) - e[4] * 4.0)], own_ids=(p["key"],))
            if st_ and st_["max_cut_fill_m"] <= 4.0 and st_["max_grade_pct"] <= 14.05 and st_["clash_points"] == 0 and st_["in_water_points"] == 0: stub = st_; break
        if stub: new_roads.append(dict(stub, why=f"{r['id']} stops {near[0][0]:.0f} m short of the pad")); P.commit_road(stub)
        else: log.append(f"{p['site']}: {r['id']} stops {near[0][0]:.0f} m short; no stub holds the rules (level {p['z']} m at the pad, {endz} m at the road end)")
        continue
    done = None                                    # no road: join the net at its nearest level stretch or pad edge
    cand = sorted(NODES, key=lambda n: math.dist(n[:2], (p["x"], p["y"])))
    picked = []
    for n in cand:
        if all(math.dist(n[:2], q[:2]) > 150 for q in picked): picked.append(n)
        if len(picked) >= 8: break
    for margin in (900, 1500):
        for n in picked:
            for e in sorted(pad_edges(p, p["key"]), key=lambda q: math.dist(q[:2], n[:2]))[:2]:
                ep = np.array(e[:2]) - e[4] * 4.0
                r = P.route(tuple(np.array(e[:2]) + e[4] * 8.0), (n[0], n[1]), za=p["z"], zb=n[2], name=f"road {p['site']}", kind="dirt", links=[p["site"], n[3]], margin=margin, pre=[tuple(ep)], own_ids=(p["key"], n[3]))
                if r is None: continue
                if r["max_cut_fill_m"] <= 4.0 and r["max_grade_pct"] <= 14.05 and r["clash_points"] == 0 and r["in_water_points"] == 0 and r["junction_step_max_m"] <= 0.3:
                    done = r; break
                log.append(f"road {p['site']} -> {n[3]}: cut/fill {r['max_cut_fill_m']} m, clash {r['clash_points']}, junction {r['junction_step_max_m']} m")
            if done: break
        if done: break
    if done: new_roads.append(dict(done, why=f"{p['site']} has a vehicle approach and no road")); P.commit_road(done)
    else:
        log.append(f"{p['site']}: NO ROAD within the rules to its built seat (pad level {p['z']} m)")
        # the other answer: re-seat it (same composition, same built size) beside the net, as near its built seat as a road reaches
        alt = None
        for n in picked[:4]:
            s2 = P.add_site(p["site"] + " (re-seat)", p["site"], p["comp"], p["hx"], p["hy"], n[0], n[1], 250, size_note="your built size, re-seated beside the net", step=10.0)
            if not s2: continue
            for e in sorted(pad_edges(s2, s2["id"]), key=lambda q: math.dist(q[:2], n[:2]))[:2]:
                r = P.route(tuple(np.array(e[:2]) + e[4] * 8.0), (n[0], n[1]), za=s2["z"], zb=n[2], name=f"road {p['site']} (re-seat)", kind="dirt", links=[s2["id"], n[3]], margin=600,
                            pre=[tuple(np.array(e[:2]) - e[4] * 4.0)], own_ids=(s2["id"], n[3]))
                if r and r["max_cut_fill_m"] <= 4.0 and r["max_grade_pct"] <= 14.05 and r["clash_points"] == 0 and r["in_water_points"] == 0 and r["junction_step_max_m"] <= 0.3:
                    alt = (s2, r); break
            if alt: break
            P.sites.remove(s2)
        if alt:
            P.commit_road(alt[1])
            moves.append(dict(site=p["site"], comp=p["comp"], why="no road within the rules reaches its built seat on the knoll top; this seat beside the net does (a proposal: or build a ramp to the knoll)",
                              old=dict(x=p["x"], y=p["y"], z=p["z"], yaw=p["yaw"]), new=dict(x=alt[0]["x"], y=alt[0]["y"], z=alt[0]["z"], yaw=alt[0]["yaw"], max_change_m=alt[0]["max_change_m"]),
                              moved_m=round(math.dist((p["x"], p["y"]), (alt[0]["x"], alt[0]["y"])), 1)))
            new_roads.append(dict(alt[1], why=f"road to {p['site']}'s proposed new seat"))
        else: log.append(f"{p['site']}: no seat beside the net either (within 250 m of its four nearest join points)")

# ---- 2b. op 1: your built roads against the K6 Perys v7 houses (the built ground still has the v5 streets).
# A road that ends in Perys is cut where it reaches the town and routed to the nearest v7 street end at that street's level;
# a road that passes by is re-routed round the houses. Every house wall stays 3 m from a road edge.
perys = []
if OP == 1:
    sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "../../kernel_10nov_v1/K6/grader")); import town_grader as TG
    LP = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "../../kernel_10nov_v1/K6_repass/perys_v7/perys_v7_layout.json")))
    HSP = [Polygon(TG.footprint(TG.Model(b["model_id"]), TG.origin_from_centre(TG.Model(b["model_id"]), b["x"], b["y"], b["yaw_deg"]), b["yaw_deg"])) for b in LP["buildings"]]
    P.own_polys("Perys v7", HSP)
    # roads into Perys end on the main street M (owner's choice, 12 Nov): its west end first, then its east end
    PORTS = []
    for st in LP["streets"]:
        if st["id"] != "M": continue
        SP = np.array(st["points"], float)
        for k in (0, -1):                    # each end, with the street's outward direction there: a road comes in along the street's own line
            e_ = SP[k]; seq = SP if k == 0 else SP[::-1]
            q_ = next(p_ for p_ in seq[1:] if math.dist(p_, e_) > 2.0); d_ = (e_ - q_) / math.dist(e_, q_)
            PORTS.append((float(e_[0]), float(e_[1]), st["points_z"][k], f"{st['id']} {'west' if k == 0 else 'east'} end", d_))
    def hclear(pts, w): ln = LineString(pts).buffer(w / 2); return min(ln.distance(h) for h in HSP)
    for i_, r in enumerate(built):
        if hclear(r["points"], r["width_m"]) >= 3.0: continue
        X = np.array(r["points"], float); w = r["width_m"]
        near = [k for k in range(len(X)) if min(Point(X[k]).distance(h) for h in HSP) < 40.0]
        k0, k1 = max(0, min(near) - 4), min(len(X) - 1, max(near) + 4)
        P.uncommit(r); fix = None
        if k0 == 0 or k1 == len(X) - 1:            # the road ends in Perys: keep the outside part, end it on a v7 street
            keep_ = X[k1:] if k0 == 0 else X[:k0 + 1]; keepz = r["points_z"][k1:] if k0 == 0 else r["points_z"][:k0 + 1]
            c = keep_[0] if k0 == 0 else keep_[-1]; cz = keepz[0] if k0 == 0 else keepz[-1]
            for (px_, py_, pz_, pn_, d_) in PORTS:
                out_ = np.array([px_, py_]) + d_ * 25.0
                # the road stops 25 m out on M's own line; those 25 m are M extended (Perys street work, at M's end level), so the road itself keeps 3 m from every wall
                rr = P.route(tuple(c), tuple(out_), grade=0.14 if r["kind"] == "dirt" else 0.10, width=w, za=cz, zb=pz_, name=r["id"], kind=r["kind"], links=r["links"], margin=400)
                log.append(f"  {r['id']} to {pn_}: " + ("no path " + str(getattr(P, "last_fail", "")) if rr is None else f"cut/fill {rr['max_cut_fill_m']} m, clash {rr['clash_points']} {rr['clash_with']}, houses {hclear(rr['points'], w):.1f} m, grade {worst_grade(rr['points'], rr['points_z'])} %, from z {cz} to {pz_}"))
                if rr and rr["max_cut_fill_m"] <= 4.0 and rr["clash_points"] == 0 and hclear(rr["points"], w) >= 3.0 and worst_grade(rr["points"], rr["points_z"]) <= (14.05 if r["kind"] == "dirt" else 10.05):
                    pts_ = (list(rr["points"])[::-1] + keep_.tolist()[1:]) if k0 == 0 else (keep_.tolist()[:-1] + list(rr["points"]))
                    zz_ = (list(rr["points_z"])[::-1] + list(keepz)[1:]) if k0 == 0 else (list(keepz)[:-1] + list(rr["points_z"]))
                    fix = dict(r, points=pts_, points_z=zz_, ends_at=f"25 m out on the line of Perys v7 main street M at its {pn_.split()[1]} end: M extended 25 m from ({px_:.0f}, {py_:.0f}) to ({out_[0]:.0f}, {out_[1]:.0f}), level {pz_} m",
                               m_extension=dict(from_xy=[round(px_, 1), round(py_, 1)], to_xy=[round(float(out_[0]), 1), round(float(out_[1]), 1)], level_m=pz_, width_m=8.0,
                                                nearest_house_wall_m=round(LineString([(px_, py_), tuple(out_)]).buffer(4.0).distance(unary_union(HSP)), 2))); break
        else:                                       # the road passes by: re-route the stretch near the houses
            rr = P.route(tuple(X[k0]), tuple(X[k1]), grade=0.14 if r["kind"] == "dirt" else 0.10, width=w, za=r["points_z"][k0], zb=r["points_z"][k1], name=r["id"], kind=r["kind"], links=r["links"], margin=300)
            if rr and rr["max_cut_fill_m"] <= 4.0 and rr["clash_points"] == 0 and hclear(rr["points"], w) >= 3.0:
                fix = dict(r, points=X[:k0].tolist() + list(rr["points"]) + X[k1 + 1:].tolist(), points_z=list(r["points_z"][:k0]) + list(rr["points_z"]) + list(r["points_z"][k1 + 1:]), ends_at="re-routed round the houses")
        if fix:
            P.check_road(fix); P.recommit(fix); built[i_] = fix
            perys.append(dict(id=r["id"], kind=r["kind"], how=fix["ends_at"], m_extension=fix.get("m_extension"), house_clear_before_m=round(hclear(X, w), 2), house_clear_after_m=round(hclear(fix["points"], w), 2),
                              grade_after_pct=worst_grade(fix["points"], fix["points_z"]), max_cut_fill_m=fix["max_cut_fill_m"], points=fix["points"], points_z=fix["points_z"]))
        else:
            P.recommit(r); log.append(f"{r['id']}: crosses Perys v7 houses (clear {hclear(X, w):.1f} m); no re-route within the rules")

# ---- 3. straights over 150 m: the same line with a 2.5 m side-to-side wave (period 120 m); levels re-held to the grade on the grid
replaced = []
for r0, r in zip(ROADS, built):
    st = straight(r["points"]); lim = 0.10 if r["kind"] == "main" else 0.14
    g0 = worst_grade(r["points"], r["points_z"])
    if st <= 150.0 and g0 <= lim * 100 + 0.05: continue
    X = np.array(r["points"], float); s_ = np.r_[0, np.cumsum(np.hypot(*np.diff(X, axis=0).T))]; L = s_[-1]
    n = max(2, int(math.ceil(L / 4.5)) + 1); ss = np.linspace(0, L, n); Xr = np.c_[np.interp(ss, s_, X[:, 0]), np.interp(ss, s_, X[:, 1])]
    if st > 150.0:
        T = np.gradient(Xr, axis=0); T = T / (np.linalg.norm(T, axis=1)[:, None] + 1e-9); Nn = np.c_[-T[:, 1], T[:, 0]]
        Xr = Xr + Nn * (2.5 * np.sin(2 * np.pi * ss / 120.0) * np.clip(np.minimum(ss, L - ss) / 20.0, 0, 1))[:, None]
    P.uncommit(r)
    if "through" in r["id"]:     # a through-comp piece runs over the comp's own floor: keep the ground's levels under the waved line
        r2 = dict(r, points=[[round(float(x), 2), round(float(y), 2)] for x, y in Xr], points_z=[round(world.z(x, y), 3) for x, y in Xr]); P.check_road(r2)
        r2["clash_points"] = 0 if all(o.startswith(tuple(r["links"])) or o.startswith("R:") for o in r2.get("clash_with", [])) else r2["clash_points"]
    else:
        keep = P.chaikin; P.chaikin = 0
        r2 = P._road(Xr, lim, r["width_m"], r["points_z"][0], r["points_z"][-1], r["id"], r["kind"], r["links"])
        P.chaikin = keep
    ok = r2["max_cut_fill_m"] <= 4.0 and straight(r2["points"]) <= 150.0 and worst_grade(r2["points"], r2["points_z"]) <= lim * 100 + 0.05 and r2["clash_points"] == 0
    if ok:
        P.recommit(r2)
        replaced.append(dict(id=r["id"], kind=r["kind"], why=("straight %.0f m" % st if st > 150 else "") + (" grade %.1f %%" % g0 if g0 > lim * 100 + 0.05 else ""),
                             straight_before_m=round(st), straight_after_m=round(straight(r2["points"])), grade_before_pct=g0, grade_after_pct=worst_grade(r2["points"], r2["points_z"]),
                             max_cut_fill_vs_built_ground_m=r2["max_cut_fill_m"], points=r2["points"], points_z=r2["points_z"]))
    else:
        P.recommit(r); log.append(f"{r['id']}: no fix within the rules (cut/fill {r2['max_cut_fill_m']} m, straight {straight(r2['points']):.0f} m, grade {worst_grade(r2['points'], r2['points_z'])} %)")

# ---- 4. pads: the built level against the grid (footprint + 1.5 m); and Perys's houses against every road (op 1)
from matplotlib.path import Path
offlevel = []
for p in PADS:
    if p.get("kind") == "pass profile": continue
    c = rect(p["x"], p["y"], p["hx"], p["hy"], p["yaw"], 1.5)
    I, J = np.meshgrid(np.arange(int(c[:, 0].min() // 5) - 1, int(c[:, 0].max() // 5) + 2), np.arange(int(c[:, 1].min() // 5) - 1, int(c[:, 1].max() // 5) + 2))
    m = Path(c).contains_points(np.c_[I.ravel() * 5.0, J.ravel() * 5.0], radius=1e-6); dev = H[J.ravel()[m], I.ravel()[m]] - p["z"]
    if np.abs(dev).max() > 0.5:
        k = np.argmax(np.abs(dev))
        offlevel.append(dict(site=p["site"], comp=p["comp"], max_off_m=round(float(dev[k]), 2), at=[float(I.ravel()[m][k] * 5), float(J.ravel()[m][k] * 5)], points_over_0_5_m=int((np.abs(dev) > 0.5).sum()), of_points=int(m.sum())))
houses = []
if OP == 1:
    sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "../../kernel_10nov_v1/K6/grader")); import town_grader as TG
    L_ = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "../../kernel_10nov_v1/K6_repass/perys_v7/perys_v7_layout.json")))
    HS = [Polygon(TG.footprint(TG.Model(b["model_id"]), TG.origin_from_centre(TG.Model(b["model_id"]), b["x"], b["y"], b["yaw_deg"]), b["yaw_deg"])) for b in L_["buildings"]]
    for r in built + new_roads + [dict(x, width_m=10.0 if x["kind"] == "main" else 7.0) for x in replaced]:
        ln = LineString(r["points"]).buffer(r["width_m"] / 2); d = min(ln.distance(h) for h in HS)
        if d < 3.0: houses.append(dict(road=r["id"], nearest_house_wall_m=round(d, 2)))

# ---- outputs
out = dict(op=OP, ground="build-4 grid (ops 1-2 already cut in); road levels read off it", squad_pads_reseated=moves,
           new_roads=[dict(id=r["id"], why=r["why"], links=r["links"], length_m=r.get("length_m"), max_grade_pct=worst_grade(r["points"], r["points_z"]), max_cut_fill_m=r["max_cut_fill_m"],
                           junction_step_m=r["junction_step_max_m"], points=r["points"], points_z=r["points_z"]) for r in new_roads],
           roads_replaced=replaced, perys_roads_reended=perys, pads_off_level=offlevel, perys_houses_within_3_m_of_a_road=houses, log=log)
json.dump(out, open(os.path.join(OUT, f"op{OP}_repass.json"), "w"), indent=1, default=float)
print(json.dumps(dict(reseated=[(m["site"], m["moved_m"], m["why"]) for m in moves], new=[(r["id"], r["why"], r.get("length_m"), r["max_cut_fill_m"]) for r in new_roads],
                      replaced=[(r["id"], r["why"], r["straight_after_m"], r["grade_after_pct"], r["max_cut_fill_vs_built_ground_m"]) for r in replaced],
                      offlevel=[(o["site"], o["max_off_m"]) for o in offlevel], houses=houses, log=log), indent=0, default=float))

# plan image: the op over a hillshade; built roads grey, replaced roads orange, new roads red, re-seated pads blue
x0, x1, y0, y1 = BOX; h, hs = world.hillshade(x0, x1, y0, y1)
fig, ax = plt.subplots(figsize=(18, 12))
ax.imshow(hs, origin="lower", extent=(x0, x0 + 5 * (h.shape[1] - 1), y0, y0 + 5 * (h.shape[0] - 1)), cmap="gray", alpha=0.85)
X_ = np.linspace(x0, x0 + 5 * (h.shape[1] - 1), h.shape[1]); Y_ = np.linspace(y0, y0 + 5 * (h.shape[0] - 1), h.shape[0])
ax.contourf(X_, Y_, h, levels=[-500, 0.3], colors=["#a9cbe0"], alpha=0.8)
rep_ids = {r["id"] for r in replaced}
for r in built:
    q = np.array(r["points"]); ax.plot(q[:, 0], q[:, 1], color="#888888" if r["id"] not in rep_ids else "#cccccc", lw=1.6)
for r in replaced:
    q = np.array(r["points"]); ax.plot(q[:, 0], q[:, 1], color="#e08a00", lw=2.4)
for r in new_roads:
    q = np.array(r["points"]); ax.plot(q[:, 0], q[:, 1], color="#d62728", lw=2.8)
for r in perys:
    q = np.array(r["points"]); ax.plot(q[:, 0], q[:, 1], color="#7b2cbf", lw=2.6)
if OP == 1:
    for h in HSP: c = np.array(h.exterior.coords); ax.fill(c[:, 0], c[:, 1], fc="#f4d06f", ec="#8a6d00", lw=0.4)
    ax.text(5380, 3600, "Perys v7 (K6)", fontsize=8, weight="bold")
for p in PADS:
    c = rect(p["x"], p["y"], p["hx"], p["hy"], p["yaw"]); ax.fill(c[:, 0], c[:, 1], fc="#bbbbbb" if p["key"] in reseat_keys else "#555555", ec="k", lw=0.5, alpha=0.7)
    ax.text(p["x"] + p["hx"] + 8, p["y"], p["site"], fontsize=6.5)
for m in moves:
    s = next(q for q in P.sites if q["id"] in (m["site"], m["site"] + " (re-seat)")); c = rect(s["x"], s["y"], s["hx"], s["hy"], s["yaw"]); ax.fill(c[:, 0], c[:, 1], fc="#1f77b4", ec="k", lw=0.8)
    ax.annotate("", xy=(s["x"], s["y"]), xytext=(m["old"]["x"], m["old"]["y"]), arrowprops=dict(arrowstyle="->", color="#1f77b4"))
for o in offlevel: ax.plot(*o["at"], "mx", ms=8, mew=2)
from matplotlib.lines import Line2D
ax.legend(handles=[Line2D([], [], color="#888888", lw=2, label="your built road (kept)"), Line2D([], [], color="#e08a00", lw=2, label="road re-drawn (straight / grade)"),
                   Line2D([], [], color="#d62728", lw=2, label="new road or stub"), Line2D([], [], color="#7b2cbf", lw=2, label="road re-ended on a Perys v7 street / round its houses"), Line2D([], [], color="#1f77b4", lw=6, label="squad pad re-seated (arrow from the old seat)"),
                   Line2D([], [], color="m", marker="x", ls="", label="pad point off its level by > 0.5 m")], loc="upper left", fontsize=8)
ax.set_title(f"Op {OP} re-pass (Kernel, PROPOSED) on your build-4 ground"); ax.set_xlim(x0, x1); ax.set_ylim(y0, y1); ax.set_aspect("equal")
fig.savefig(os.path.join(OUT, f"op{OP}_repass.png"), dpi=90, bbox_inches="tight")
