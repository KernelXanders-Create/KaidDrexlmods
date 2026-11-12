"""Run one op's ground plan: sites -> road nets -> squad positions -> shores -> checks -> opN_plan.json / .png / _checks.json.
Usage: python3 run_op.py op3 <out dir>"""
import sys, os, json, math, importlib, collections, time
import numpy as np
from shapely.geometry import Polygon, LineString, Point, MultiPoint
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
import world, planner
from planner import rect
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "../../../kernel_10nov_v1/K6/grader"))
import town_grader as TG       # house footprints exactly as your grader reads them

# built pads of ops 1-2: the measured size of every composition that already stands somewhere (tried first)
BUILT = {}
for f_ in ("pads_op1", "pads_op2"):
    for p_ in json.load(open(os.path.join(world.PACK, "ops_1_2", f_ + ".json")))["pads"]:
        if p_.get("hx") and p_.get("hy") and p_.get("comp") and p_["comp"] not in BUILT: BUILT[p_["comp"]] = (p_["hx"], p_["hy"], p_.get("site"))

op = importlib.import_module(sys.argv[1]); OUT = sys.argv[2]; os.makedirs(OUT, exist_ok=True)
N = sys.argv[1].replace("op", "")
D = world.objectives(); R = {s["id"]: s for s in D["sites"]}
P = planner.Plan(op.BOX)
for k_, v_ in getattr(op, "PLAN_KW", {}).items(): setattr(P, k_, v_)     # per-op router settings (none change a rule)
log = []

# ---- towns (hand-made, from the K6 v2 layouts): blocked areas with an entry point at their square
towns = {}
for tid, tl in getattr(op, "TOWNS", {}).items():
    L = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), tl["layout"])))
    pts = [(b["x"], b["y"]) for b in L["buildings"]] + [tuple(p) for s in L["streets"] for p in s["points"]]
    hull = MultiPoint(pts).convex_hull.buffer(10)
    P.add_area(tid, list(hull.exterior.coords), None, own=True)     # roads keep off the whole town outline, except its own road at its port
    houses = [Polygon(TG.footprint(TG.Model(b["model_id"]), TG.origin_from_centre(TG.Model(b["model_id"]), b["x"], b["y"], b["yaw_deg"]), b["yaw_deg"])) for b in L["buildings"]]
    P.own_polys(tid, houses)       # the grader's house footprints: roads keep their band (and 3 m) off the walls
    ex, ey = tl["entry"]; towns[tid] = dict(id=tid, name=tl["name"], hull=hull, entry=(ex, ey), z=tl["entry_z"], ports=tl.get("ports", [(ex, ey, tl["entry_z"], tl.get("out_bearing", 0.0), "road port")]), n_buildings=len(L["buildings"]), houses=houses,
                                            garrison=sum(1 for b in L["buildings"] if b.get("garrison")), layout=tl["layout"], exits=tl.get("exits", {}))
    if tid in R:
        towns[tid]["purpose_map_xy"] = [R[tid]["x"], R[tid]["y"]]; towns[tid]["layout_centre_xy"] = [round(hull.centroid.x, 1), round(hull.centroid.y, 1)]
        towns[tid]["layout_offset_m"] = round(math.dist((R[tid]["x"], R[tid]["y"]), (hull.centroid.x, hull.centroid.y)))

# ---- pads of other ops inside this box (from their plans): blocked for this op's pads and roads; a net may grow from one
EXT = {}
for e in getattr(op, "EXTERNAL_PADS", []):
    c_ = rect(e["x"], e["y"], e["hx"] + 1.5, e["hy"] + 1.5, e["yaw"]); pol_ = Polygon(c_)
    P.add_area(e["id"], [tuple(q) for q in c_], None)
    gx_, gy_ = np.meshgrid(np.arange(int(min(c_[:, 0]) // 5), int(max(c_[:, 0]) // 5) + 2) * 5.0, np.arange(int(min(c_[:, 1]) // 5), int(max(c_[:, 1]) // 5) + 2) * 5.0)
    P.add_buildings(e["id"], [(a, b) for a, b in zip(gx_.ravel(), gy_.ravel()) if pol_.contains(Point(a, b))], r=0.0)
    EXT[e["id"]] = e

# ---- other ops' finished plans (EXTERNAL_PLANS): their pads inside this box are blocked, their roads are fixed ground a net may join
EXT_ROADS = []
for f_ in getattr(op, "EXTERNAL_PLANS", []):
    D_ = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), f_)))
    for e in D_["sites"] + D_["squad_positions"]:
        if op.BOX[0] - 200 < e["x"] < op.BOX[1] + 200 and op.BOX[2] - 200 < e["y"] < op.BOX[3] + 200:
            e2 = dict(id=f"{e['id']} (op {D_['op']})", x=e["x"], y=e["y"], hx=e["hx"], hy=e["hy"], yaw=e["yaw"], z=e["z"])
            c_ = rect(e2["x"], e2["y"], e2["hx"] + 1.5, e2["hy"] + 1.5, e2["yaw"]); pol_ = Polygon(c_)
            P.add_area(e2["id"], [tuple(q) for q in c_], None)
            gx_, gy_ = np.meshgrid(np.arange(int(min(c_[:, 0]) // 5), int(max(c_[:, 0]) // 5) + 2) * 5.0, np.arange(int(min(c_[:, 1]) // 5), int(max(c_[:, 1]) // 5) + 2) * 5.0)
            P.add_buildings(e2["id"], [(a, b) for a, b in zip(gx_.ravel(), gy_.ravel()) if pol_.contains(Point(a, b))], r=0.0)
            EXT[e2["id"]] = e2
    for r_ in D_["roads"]:
        pts_ = np.array(r_["points"])
        if not ((pts_[:, 0] > op.BOX[0]) & (pts_[:, 0] < op.BOX[1]) & (pts_[:, 1] > op.BOX[2]) & (pts_[:, 1] < op.BOX[3])).any(): continue
        r2 = dict(r_, id=f"op{D_['op']}:{r_['id']}", external=True)
        P.commit_road(r2); P.roads.remove(r2); EXT_ROADS.append(r2)

# ---- your built ops 1-2 roads (ground/roads_ops_1_2.json): fixed ground; levels read off the build-4 grid (the file has none)
for r_ in json.load(open(os.path.join(world.PACK, "ground", "roads_ops_1_2.json"))):
    if not r_["kind"] in ("dirt", "main"): continue          # Perys's town streets stay in Perys
    pts_ = np.array(r_["points"], float)
    if not ((pts_[:, 0] > op.BOX[0]) & (pts_[:, 0] < op.BOX[1]) & (pts_[:, 1] > op.BOX[2]) & (pts_[:, 1] < op.BOX[3])).any(): continue
    r2 = dict(id=f"built:{r_['link']}#{len(EXT_ROADS)}", kind=r_["kind"], width_m=10.0 if r_["kind"] == "main" else 7.0, links=[], points=r_["points"],
              points_z=[round(world.z(x, y), 2) for x, y in r_["points"]], external=True, source="roads_ops_1_2.json")
    P.commit_road(r2); P.roads.remove(r2); EXT_ROADS.append(r2)
# other ops' and built roads that touch are one net: group them (12 m)
EXT_GROUP = {}
_par = {r_["id"]: r_["id"] for r_ in EXT_ROADS}
def _f(a):
    while _par[a] != a: a = _par[a]
    return a
from scipy.spatial import cKDTree as _KD
_trees = [(r_["id"], _KD(np.array(r_["points"]))) for r_ in EXT_ROADS]
for i_, (a_, ta_) in enumerate(_trees):
    for b_, tb_ in _trees[i_ + 1:]:
        if ta_.sparse_distance_matrix(tb_, 12.0).nnz: _par[_f(a_)] = _f(b_)
for r_ in EXT_ROADS: EXT_GROUP[r_["id"]] = "existing net " + _f(r_["id"]).split("#")[0]

# ---- sites
def place_sites(only=None, skip=()):
    for sid, name, comp, hx, hy, ev, xy, rad, wmode in op.SITES:
        if (only is not None and sid not in only) or sid in skip or (only is None and sid in getattr(op, "LATE_SITES", ())): continue
        base = sid.split("-N")[0].split("-T")[0]
        x, y = xy if xy else (R[base]["x"], R[base]["y"])
        kw_ = getattr(op, "SITE_KW", {}).get(sid, {})
        # sizes to try: your built pad of the same composition first (MEASURED), then the op file's size (with its stated basis)
        sizes = []
        bk = comp if comp in BUILT else comp.split(" + ")[0] if comp.split(" + ")[0] in BUILT else None
        if bk and (abs(BUILT[bk][0] - hx) > 0.5 or abs(BUILT[bk][1] - hy) > 0.5) and not ev.startswith("REDUCED: the stack"):
            sizes.append((BUILT[bk][0], BUILT[bk][1], f"KNOWN (built): your {BUILT[bk][2]} pad of {bk}, {2 * BUILT[bk][0]:.0f} x {2 * BUILT[bk][1]:.0f} m"))
        sizes.append((hx, hy, ev if not bk or sizes == [] else f"REDUCED: your built pad ({BUILT[bk][2]}, {2 * BUILT[bk][0]:.0f} x {2 * BUILT[bk][1]:.0f} m) holds 4 m nowhere within {rad * 2.4:.0f} m; this {2 * hx:.0f} x {2 * hy:.0f} m pad needs a trimmed composition. Was: {ev}"))
        s = None
        for hx_, hy_, ev_ in sizes:
            s = P.add_site(sid, name, comp, hx_, hy_, x, y, rad, water_ok=wmode, size_note=ev_, step=5.0 if rad <= 200 else 10.0, **kw_)
            if s is None:
                for r2 in (rad * 1.6, rad * 2.4):
                    s = P.add_site(sid, name, comp, hx_, hy_, x, y, r2, water_ok=wmode, cap=3.9, size_note=ev_, **kw_)
                    if s: break
            if s: break
        if s is None:
            log.append(f"{sid}: NO PAD FOUND within {rad * 2.4:.0f} m at {', '.join(f'{2 * a:.0f} x {2 * b:.0f} m' for a, b, _ in sizes)}"); continue
        d_ = R.get(base, {})
        s.update(role=d_.get("role", "squad"), size=d_.get("tier"), stake=d_.get("stake", ""), island=d_.get("island", ""))
        if d_:     # moves are measured from the purpose map's design point (for a split site's second pad: from its main's point)
            s["moved_from_rough_m"] = s.get("moved_m"); s["design_xy"] = [d_["x"], d_["y"]]
            s["moved_m"] = round(math.dist((d_["x"], d_["y"]), (s["x"], s["y"]))); s["rough"] = [d_["x"], d_["y"]] if not xy else list(xy)

trunk_stops = [leg["stop"][1] for leg in getattr(op, "TRUNK", []) if leg["stop"][0] == "site"]
place_sites(only=trunk_stops) if trunk_stops else place_sites()
SITE = {s["id"]: s for s in P.sites}


def entry_point(s, toward, out=2.5, rank=0):
    """the pad edge midpoint (grown by `out`) that faces `toward` (rank 1: the second-best edge)"""
    best = None; allc = []
    a = math.radians(s["yaw"]); ex = np.array([math.cos(a), -math.sin(a)]); ey = np.array([math.sin(a), math.cos(a)])
    c = np.array([s["x"], s["y"]])
    for v, h in ((ex, s["hx"]), (-ex, s["hx"]), (ey, s["hy"]), (-ey, s["hy"])):
        p = c + v * (h + 1.5 + out)
        allc.append((math.dist(p, toward), p, v))
    allc.sort(key=lambda t: t[0])
    return allc[rank][1], allc[rank][2]


# ---- trunk (an AI road through given stops: a fixed point, sites (through-comps enter one edge and leave another), a town entry)
trunk_nodes = []
trunk_breaks = [dict(at=list(g_["at"]), z=round(world.z(*g_["at"]), 2), label=g_["label"]) for g_ in getattr(op, "GAPS", [])]      # known gaps (need your ramps)
def flat_nodes(r, owner):
    zz = np.array(r["points_z"]); gg = np.abs(np.gradient(zz, 4.5))
    fl = [(x, y, z, owner) for k, ((x, y), z) in enumerate(zip(r["points"], r["points_z"])) if k % 3 == 0 and gg[max(0, k - 3):k + 4].max() <= 0.03]
    return fl if len(fl) >= 2 else [(x, y, z, owner) for (x, y), z in zip(r["points"][::4], r["points_z"][::4])]

if getattr(op, "TRUNK", None):
    prev_xy, prev_z, prev_id = None, None, None
    for k, leg in enumerate(op.TRUNK):
        kind_, key = leg["stop"]
        if kind_ == "xyz":
            prev_xy = np.array(key, float); prev_z = round(world.z(*key), 2); prev_id = "trunk start %d" % k; trunk_breaks.append(dict(at=list(key), z=prev_z, label=leg.get("label", ""))); continue
        if kind_ == "site":
            s = SITE[key]; ep, v = entry_point(s, tuple(prev_xy)); a_xy, a_z = ep, s["z"]
        else:
            t = towns[key]; a_xy, a_z = np.array(t["entry"]), t["z"]; v = None
        out = a_xy + 12.0 * v if v is not None else a_xy
        r = None
        for margin in (500, 1000, 1600):
            r = P.route(tuple(prev_xy), tuple(out), grade=leg["grade"], width=leg["width"], za=prev_z, zb=a_z, name=f"trunk-{k}:{prev_id}-{key}", kind=leg["kind"],
                        links=[prev_id, key], margin=margin, post=[tuple(a_xy)] if v is not None else None, own_ids=(prev_id, key))
            if r is None: continue
            ok = r["max_cut_fill_m"] <= 4.0 and r["max_grade_pct"] <= leg["grade"] * 100 + 0.05 and r["clash_points"] == 0 and r["in_water_points"] <= 3
            if ok: break
            log.append(f"trunk leg {k} to {key} (margin {margin}): grade {r['max_grade_pct']} %, cut/fill {r['max_cut_fill_m']} m, pad clash {r['clash_points']} {r['clash_with']}, water {r['in_water_points']}")
            r = None
        if r is None:
            log.append(f"TRUNK LEG {k} to {key}: NO ROUTE"); break
        P.commit_road(r); trunk_nodes += flat_nodes(r, key)
        if kind_ == "site":
            s["entrance_bearing_deg"] = round(math.degrees(math.atan2(v[0], v[1])) % 360); s["entrance_xy"] = [round(float(a_xy[0]), 1), round(float(a_xy[1]), 1)]
            if leg.get("through"):                              # leave by the edge facing the next stop
                nxt = op.TRUNK[k + 1]["stop"]
                tgt = SITE[nxt[1]] if nxt[0] == "site" else dict(x=towns[nxt[1]]["entry"][0], y=towns[nxt[1]]["entry"][1])
                e2, v2 = entry_point(s, (tgt["x"], tgt["y"]))
                if np.allclose(e2, a_xy): e2, v2 = entry_point(s, (tgt["x"], tgt["y"]), rank=1)
                s["exit_xy"] = [round(float(e2[0]), 1), round(float(e2[1]), 1)]; s["exit_bearing_deg"] = round(math.degrees(math.atan2(v2[0], v2[1])) % 360)
                prev_xy, prev_z, prev_id = e2 + 12.0 * v2, s["z"], key
                # stub from the exit edge
                stub = P._road(np.array([e2, e2 + 12.0 * v2]), 0.14, leg["width"], s["z"], s["z"], f"trunk-{k}b:{key}-exit", leg["kind"], [key, key])
                P.commit_road(stub)
            else:
                prev_xy, prev_z, prev_id = a_xy, s["z"], key
        else:
            prev_xy, prev_z, prev_id = a_xy, a_z, key

if trunk_stops:
    place_sites(skip=trunk_stops)
    SITE = {s["id"]: s for s in P.sites}

# ---- road nets
nodes = {}       # net name -> list of (x, y, z, owner)
LATE = tuple(getattr(op, "LATE_SITES", ()))     # sites seated after the roads, beside them, then joined by a short spur
def level_nodes(points, points_z, owner, away=None, half=15.0, tol=0.2, every=3):
    """points of a road where it is level (within tol over +-half metres along it): a road joining there meets it on its own level"""
    X = np.array(points, float); Z = np.array(points_z, float); s_ = np.r_[0, np.cumsum(np.hypot(*np.diff(X, axis=0).T))]; out = []
    for k in range(0, len(X), every):
        m = np.abs(s_ - s_[k]) <= half
        if s_[k] < half or s_[-1] - s_[k] < half: continue
        if np.ptp(Z[m]) <= tol and (away is None or math.dist(X[k], away) > 40.0): out.append((float(X[k, 0]), float(X[k, 1]), float(Z[k]), owner))
    return out


def pad_edge_nodes(e, owner, used=None):
    a_ = math.radians(e["yaw"]); ex_ = np.array([math.cos(a_), -math.sin(a_)]); ey_ = np.array([math.sin(a_), math.cos(a_)])
    out = []
    for v_, h_ in ((ex_, e["hx"]), (-ex_, e["hx"]), (ey_, e["hy"]), (-ey_, e["hy"])):
        q_ = np.array([e["x"], e["y"]]) + v_ * (h_ + 4.0)
        if used is None or math.dist(q_, used) > 5: out.append((float(q_[0]), float(q_[1]), e["z"], owner))
    return out


JMAX = getattr(op, "JUNCTION_MAX", 0.3)      # item 9: a joining road ends on the earlier road's own level (step <= 0.3 m)
HOUSES = [(tid, h) for tid, t in towns.items() for h in t["houses"]]


def house_clear(r):
    """nearest house wall (the grader's footprints) to the road's edge, m"""
    if not HOUSES: return 1e9
    ln = LineString(r["points"]).buffer(r["width_m"] / 2)
    return min(ln.distance(h) for _, h in HOUSES)


for phase in (0, 1):
  if phase == 1:
    if not LATE: break
    place_sites(only=LATE); SITE = {s["id"]: s for s in P.sites}
  for net, order in op.NETS.items():
    if phase == 1: order = [x for x in order if x in LATE]
    else: order = [x for x in order if x not in LATE]
    root = op.ROOT[net]
    if phase == 0:
        if root == "TRUNK":
            nodes[net] = list(trunk_nodes) + [(x, y, z, tid) for tid, t in towns.items() for nm, (x, y, z) in t.get("exits", {}).items()]
        elif root in towns:
            t = towns[root]; nodes[net] = [(t["entry"][0], t["entry"][1], t["z"], root)]
        elif root == "EXTERNAL_ROADS":      # existing roads (other ops', your built ones): their level stretches, and the free edges of the pads on them
            nodes[net] = [n_ for r_ in EXT_ROADS for n_ in level_nodes(r_["points"], r_["points_z"], r_["id"]) if op.BOX[0] < n_[0] < op.BOX[1] and op.BOX[2] < n_[1] < op.BOX[3]]
            nodes[net] += [n_ for eid, e in EXT.items() for n_ in pad_edge_nodes(e, eid)]
        elif root in EXT:     # another op's pad: the net leaves it from its free edges (the edges its own op's road does not use)
            e = EXT[root]; a_ = math.radians(e["yaw"]); ex_ = np.array([math.cos(a_), -math.sin(a_)]); ey_ = np.array([math.sin(a_), math.cos(a_)])
            nodes[net] = [tuple(np.array([e["x"], e["y"]]) + v * (h + 1.5 + 2.5)) + (e["z"], root) for v, h in ((ex_, e["hx"]), (-ex_, e["hx"]), (ey_, e["hy"]), (-ey_, e["hy"]))
                          if math.dist(np.array([e["x"], e["y"]]) + v * (h + 4.0), e.get("used_entrance", (1e9, 1e9))) > 5]
        else:
            s = SITE[root]; s["_root"] = True
            a_ = math.radians(s["yaw"]); ex_ = np.array([math.cos(a_), -math.sin(a_)]); ey_ = np.array([math.sin(a_), math.cos(a_)])
            nodes[net] = [tuple(np.array([s["x"], s["y"]]) + v * (h + 1.5 + 2.5)) + (s["z"], root) for v, h in ((ex_, s["hx"]), (-ex_, s["hx"]), (ey_, s["hy"]), (-ey_, s["hy"]))]
    pending = [x for x in order if (x in SITE or x in towns) and x != root]
    for pass_no in range(3):
      failed = []
      for sid in pending:
        if sid in towns:     # a town joins the net at its road port, leaving along the bearing its op file gives
            t_ = towns[sid]; s = dict(id=sid, x=t_["entry"][0], y=t_["entry"][1], z=t_["z"], _town=t_)
        else: s = SITE[sid]
        cand = sorted(nodes[net], key=lambda n: math.dist((n[0], n[1]), (s["x"], s["y"])))
        picked = []                                    # up to 4 candidates at least 150 m apart (not four points of one road)
        for nd in cand:
            if nd[3] == sid: continue
            if all(math.dist((nd[0], nd[1]), (q[0], q[1])) > 150 for q in picked): picked.append(nd)
            if len(picked) >= 6: break
        own_ = {}                                       # and the nearest point of each other road or pad, so a far net is tried too
        for nd in cand:
            o_ = nd[3]
            if o_ != sid and o_ not in own_: own_[o_] = nd
        picked += [nd for nd in list(own_.values())[:12] if nd not in picked][:6]
        done = False
        tries = [(q, 450, e) for q in picked[:2] for e in (0, 1)] + [(q, 900, e) for q in picked[:3] for e in (0, 1)]
        if pass_no > 0: tries += [(q, 1500, e) for q in picked[:12] for e in (0, 1, 2)]
        if "_town" in s: tries = [(q, m_, e) for m_ in (450, 900, 1500) for q in picked[:4] for e in range(len(s["_town"]["ports"]))]
        for nd, margin, e_rank in tries:
            if "_town" in s:      # a town tries each of its road ports (street ends at the town's edge) in turn
                pts_ = s["_town"]["ports"]
                if e_rank >= len(pts_): continue
                px_, py_, pz_, pb_, pn_ = pts_[e_rank]; s["x"], s["y"], s["z"] = px_, py_, pz_
                b_ = math.radians(pb_); v = np.array([math.sin(b_), math.cos(b_)]); ep = np.array([px_, py_])
            else: ep, v = entry_point(s, (nd[0], nd[1]), rank=e_rank)
            out = np.array(ep) + 12.0 * v
            t_r = time.time()
            r = P.route(tuple(out), (nd[0], nd[1]), grade=0.14, width=7.0, za=s["z"], zb=nd[2], name=f"{sid}-{nd[3]}", kind="dirt", links=[sid, nd[3]], margin=margin, pre=[tuple(ep)], own_ids=(sid, nd[3]))
            if os.environ.get("PLAN_VERBOSE"):
                print(f"  {sid} -> {nd[3]} margin {margin} edge {e_rank}: {'no path' if r is None else (r['max_cut_fill_m'], r['junction_step_max_m'], len(r['points']))} {time.time() - t_r:.0f} s", file=sys.stderr, flush=True)
            if r is None: continue
            if r["max_cut_fill_m"] > 4.0 or r["max_grade_pct"] > 14.05 or r["clash_points"] > 0 or r["in_water_points"] or r["junction_step_max_m"] > JMAX or house_clear(r) < 3.0:
                log.append(f"road {sid} -> {nd[3]}: rejected (grade {r['max_grade_pct']} %, cut/fill {r['max_cut_fill_m']} m, pad clash {r['clash_points']} {r['clash_with']}, junction step {r['junction_step_max_m']} m, water {r['in_water_points']}, house {round(house_clear(r), 1)} m)"); continue
            P.commit_road(r)
            if "_town" in s:      # the port the road reached becomes the town's entry
                t_ = s["_town"]; t_["entry"] = (s["x"], s["y"]); t_["z"] = s["z"]; t_["port_used"] = pn_
            if "_town" not in s:
                s["entrance_bearing_deg"] = round(math.degrees(math.atan2(v[0], v[1])) % 360)
                s["entrance_xy"] = [round(float(ep[0]), 1), round(float(ep[1]), 1)]
            nodes[net] += level_nodes(r["points"], r["points_z"], sid, away=ep)      # its level stretches (not its own landing at its pad)
            if "_town" in s:      # a joined town's other street ends are on the net too (its streets carry traffic)
                nodes[net] += [(px_, py_, pz_, sid) for px_, py_, pz_, pb_, pn_ in s["_town"]["ports"] if math.dist((px_, py_), (s["x"], s["y"])) > 5]
            else:                 # and a joined pad's free edges (level, at the pad's height) are join points
                nodes[net] += pad_edge_nodes(s, sid, used=ep)
            done = True; break
        if not done: failed.append(sid)
      if not failed or len(failed) == len(pending): pending = failed; break
      pending = failed
    for sid in pending: log.append(f"road for {sid}: NO ROUTE found to the {net} net")

# ---- foot links (stairs / paths, not graded ground) for every site the road net does not reach
foot = []
road_pts = [(x, y, z, r["id"]) for r in P.roads for (x, y), z in zip(r["points"], r["points_z"])]


def dry(a, b):
    """True if the straight line a-b stays on land (+0.3 m) all the way"""
    L = math.dist(a, b); n = max(2, int(L / 5))
    return all(P.H[int(round((a[1] + (b[1] - a[1]) * t) / 5)), int(round((a[0] + (b[0] - a[0]) * t) / 5))] > 0.3 for t in np.linspace(0.05, 0.95, n))


def nearest_dry(xy):
    for t in sorted(road_pts, key=lambda t: math.dist((t[0], t[1]), xy))[:4000:7]:
        if dry(xy, (t[0], t[1])): return t
    return None
reached_ids = {x for r in P.roads for x in r["links"]}
for s in P.sites:
    if s["id"] in reached_ids or s.get("water_ok") == "beach" and s["id"] in getattr(op, "BOAT_ONLY", ()): continue
    if s["id"] in reached_ids: continue
    isl = s.get("island", "")
    q = nearest_dry((s["x"], s["y"])) if road_pts and isl in op.NETS else None
    if q is None:      # no road on its island: a foot path to a town on the same island, if one stands there
        tq = [(t["entry"][0], t["entry"][1], t["z"], f"town {t['id']} ({t['name']})") for t in towns.values()
              if R.get(t["id"], {}).get("island") == isl and dry((s["x"], s["y"]), t["entry"])]
        q = min(tq, key=lambda t: math.dist((t[0], t[1]), (s["x"], s["y"]))) if tq else None
    if q is None: continue
    foot.append(dict(site=s["id"], bottom_xyz=[round(s["x"], 1), round(s["y"], 1), s["z"]], top_xyz=[round(q[0], 1), round(q[1], 1), round(q[2], 2)], top_on_road=q[3],
                     straight_m=round(math.dist((q[0], q[1]), (s["x"], s["y"]))), rise_m=round(q[2] - s["z"], 1)))
for t in towns.values():
    if t["id"] in reached_ids: continue          # the road net ends at the town's road port
    q = nearest_dry(t["entry"])
    if q is None: continue
    foot.append(dict(site=t["id"], bottom_xyz=[t["entry"][0], t["entry"][1], t["z"]], top_xyz=[round(q[0], 1), round(q[1], 1), round(q[2], 2)], top_on_road=q[3],
                     straight_m=round(math.dist((q[0], q[1]), t["entry"])), rise_m=round(q[2] - t["z"], 1)))

# ---- entrances for sites the net does not end at (roots, foot-only and sea sites): face the foot link / the road / the sea
for s in P.sites:
    if "entrance_xy" in s: continue
    fl = next((f for f in foot if f["site"] == s["id"]), None)
    if fl: tgt = fl["top_xyz"][:2]; why = "faces its foot link"
    elif road_pts and s["id"] in reached_ids:
        q = min(road_pts, key=lambda t: math.dist((t[0], t[1]), (s["x"], s["y"]))); tgt = (q[0], q[1]); why = "faces the road that serves it"
    else:
        J, I = np.nonzero(P.water[int(s["y"] / 5) - 40:int(s["y"] / 5) + 41, int(s["x"] / 5) - 40:int(s["x"] / 5) + 41])
        k = np.argmin(np.hypot(J - 40, I - 40)) if len(J) else None
        tgt = ((int(s["x"] / 5) - 40 + I[k]) * 5, (int(s["y"] / 5) - 40 + J[k]) * 5) if k is not None else (s["x"], s["y"] + 1); why = "faces the water (a sea / beach work)"
    ep, v = entry_point(s, tgt)
    s["entrance_bearing_deg"] = round(math.degrees(math.atan2(v[0], v[1])) % 360); s["entrance_xy"] = [round(float(ep[0]), 1), round(float(ep[1]), 1)]; s["entrance_note"] = why

# ---- squad positions
for qid, comp, hx, hy, ax, ay, rad, guards in getattr(op, "SQUADS", []):
    s = P.add_site(qid, "squad position", comp, hx, hy, ax, ay, rad, size_note="KNOWN: same composition in pads_op1 / pads_op2")
    if s is None:
        s = P.add_site(qid, "squad position", comp, hx, hy, ax, ay, rad * 1.8, cap=3.9, size_note="KNOWN")
    if s is None: log.append(f"{qid}: NO PAD FOUND"); continue
    near = min([x for x in P.sites if not x["id"].startswith("A")] + [dict(id=t, x=v["entry"][0], y=v["entry"][1]) for t, v in towns.items()],
               key=lambda z_: math.dist((z_["x"], z_["y"]), (s["x"], s["y"])))
    s.update(role="squad position", guards=guards, nearest_site=near["id"], nearest_site_m=round(math.dist((near["x"], near["y"]), (s["x"], s["y"]))))

# ---- shores
shores = P.shores(*op.BOX)

# ---- checks
pads = P.sites
polys = {s["id"]: Polygon(rect(s["x"], s["y"], s["hx"], s["hy"], s["yaw"])) for s in pads}
C = collections.OrderedDict()
worst = []
for i in range(len(pads)):
    for j in range(i + 1, len(pads)):
        a, b = pads[i], pads[j]; d = polys[a["id"]].distance(polys[b["id"]])
        if d < 40: worst.append((round(d, 1), a["id"], b["id"], abs(a["z"] - b["z"]) > 0.01))
worst.sort()
bad1 = [w for w in worst if (w[3] and w[0] < 17.0)]
bad4 = [w for w in worst if w[0] < 12.0]
# road vs pad / road clashes on the grid
road_clash = {r["id"]: (r["clash_points"], r["clash_with"]) for r in P.roads}
C["1 grid: pads at different levels >= 14 m (17 m diagonal; checked at 17 m)"] = dict(status="PASS" if not bad1 else "FAIL", closest=worst[:3], failing=bad1)
C["1 grid: road points vs pad points at another level (5 cm)"] = dict(status="PASS" if all(v[0] == 0 for v in road_clash.values()) else "FAIL",
    total=sum(v[0] for v in road_clash.values()), by_road={k: v for k, v in road_clash.items() if v[0]})
C["1 grid: junction steps (a road joining the net meets the earlier road's points at another level; the earlier road keeps its level)"] = dict(
    status="REPORT", by_road={r["id"]: [r["junction_step_points"], r["junction_step_max_m"]] for r in P.roads if r["junction_step_points"]},
    note="each joining road ends on a 12 m level landing at the junction's level; the step is where the earlier road's band climbs away from it")
ch = max(pads, key=lambda s: s["max_change_m"])
C["2 pad ground change <= 4.0 m"] = dict(status="PASS" if ch["max_change_m"] <= 4.0 else "FAIL", worst=[ch["id"], ch["max_change_m"]],
                                          over_3_5=[[s["id"], s["max_change_m"]] for s in pads if s["max_change_m"] > 3.5])
g = max(P.roads, key=lambda r: r["max_grade_pct"]) if P.roads else None
cf = max(P.roads, key=lambda r: r["max_cut_fill_m"]) if P.roads else None
st = max(P.roads, key=lambda r: r["straight_max_m"]) if P.roads else None
# clearance: pad footprints vs road edges
clr = []
ALLPADS = [(s["id"], polys[s["id"]]) for s in pads] + [(eid, Polygon(rect(e["x"], e["y"], e["hx"], e["hy"], e["yaw"]))) for eid, e in EXT.items()]
for r in P.roads:
    X = np.array(r["points"])
    for pid, pol in ALLPADS:
        if pid in r["links"]:      # the pad a road serves: only the road's own end (its last 25 m) may meet it
            keep = [k for k in range(len(X)) if pol.distance(Point(X[k])) > 25.0 + r["width_m"] / 2]
            if len(keep) < 2: continue
            ln = LineString(X[keep[0]:keep[-1] + 1]).buffer(r["width_m"] / 2)
        else: ln = LineString(X).buffer(r["width_m"] / 2)
        clr.append((round(pol.distance(ln), 1), pid, r["id"]))
clr.sort()
# connectivity: union of links per net
conn = {}
ISL = collections.OrderedDict()      # rule 3 is per island: nets named "<island>: <part>" are one island and must join up
for net, order in op.NETS.items():
    k_ = net.split(":")[0].strip(); ISL.setdefault(k_, dict(roots=[], order=[]))
    ISL[k_]["roots"].append(op.ROOT[net]); ISL[k_]["order"] += order
for net, io in ISL.items():
    order = io["order"]
    par = {}
    def f(a):
        while par.get(a, a) != a: a = par[a]
        return a
    for r in P.roads:
        a, b = [EXT_GROUP.get(x, x) for x in r["links"]]     # other ops' and built roads: their own connected groups
        par.setdefault(a, a); par.setdefault(b, b); par[f(a)] = f(b)
    reached = {x for r in P.roads for x in r["links"]}
    want = [x for x in io["roots"] + order if (x in SITE or x in towns) and x in reached]
    comps = collections.defaultdict(list)
    for x in want: comps[f(x)].append(x)
    conn[net] = dict(pieces=list(comps.values()), not_reached=[x for x in order if x in SITE and x not in reached])
def worst_grade(r, base):
    """steepest grade over any stretch of `base` metres, measured along the points as handed over"""
    X = np.array(r["points"]); Z = np.array(r["points_z"]); s_ = np.r_[0, np.cumsum(np.hypot(*np.diff(X, axis=0).T))]; w = 0.0
    for i in range(len(s_)):
        j = np.searchsorted(s_, s_[i] + base)
        if j < len(s_): w = max(w, abs(Z[j] - Z[i]) / (s_[j] - s_[i]))
    return round(100 * w, 1)
GR = sorted(((worst_grade(r, 10.0), worst_grade(r, 20.0), r["max_grade_pct"], r["id"]) for r in P.roads), reverse=True)
C["3 roads: dirt grade <= 14 %"] = dict(status="PASS" if not GR or max(GR[0][0], max(x[2] for x in GR)) <= 14.05 else "FAIL",
    worst=[GR[0][3], dict(over_10_m=GR[0][0], over_20_m=GR[0][1], point_to_point=GR[0][2])] if GR else None,
    method="measured on the points as handed over: point to point, and over every stretch of 10 m and 20 m along them")
C["3 roads: cut / fill <= 4 m (every grid point the road fixes)"] = dict(status="PASS" if not cf or cf["max_cut_fill_m"] <= 4.0 else "FAIL", worst=[cf["id"], cf["max_cut_fill_m"]] if cf else None)
APPR = {}
for line_ in open(os.path.join(world.PACK, "design", "PURPOSE_MAP.md"), encoding="utf-8"):
    if line_.startswith("| ") and line_.count("|") > 8:
        cells = [c.strip() for c in line_.strip().strip("|").split("|")]
        APPR[cells[0]] = cells[-1]
veh = [x for x in list(SITE) + list(towns) if "vehicles" in APPR.get(x.split("-N")[0].split("-T")[0], "")]
veh_missing = [x for x in veh if x not in {y for r in P.roads for y in r["links"]}]
C["3 roads: one connected net per island"] = dict(status="PASS" if all(len(v["pieces"]) <= 1 for v in conn.values()) and not veh_missing else "FAIL", nets=conn,
    vehicle_sites_not_on_the_net=veh_missing,
    reading="the rule binds sites with a vehicle approach; where the purpose map gives no site one, every site the net reaches is on ONE net per island and the rest are foot / boat / air (their foot links are in the plan)")
C["3 roads: no straight run over 150 m (within 1 m of the chord)"] = dict(status="PASS" if not st or st["straight_max_m"] <= 150 else "FAIL", worst=[st["id"], st["straight_max_m"]] if st else None)
tb = sorted((round(LineString(r["points"]).buffer(r["width_m"] / 2).distance(h), 2), tid, r["id"]) for r in P.roads for tid, h in HOUSES)     # house walls (the grader's footprints), no exemption
C["3 roads: nothing built within 3 m of a road edge"] = dict(status="PASS" if (not clr or clr[0][0] >= 3.0) and (not tb or tb[0][0] >= 3.0) else "FAIL", closest=clr[:3],
    town_houses_closest=tb[:3], town_note="town houses are measured from their walls (your grader's footprints of the K6 layouts) to the road edge, with no exemption at the street ends")
wd = []
for s in pads:
    if s.get("water_ok"): continue
    poly = polys[s["id"]]
    x0, y0, x1, y1 = poly.bounds
    I, J = np.meshgrid(np.arange(int((x0 - 30) / 5), int((x1 + 30) / 5) + 1), np.arange(int((y0 - 30) / 5), int((y1 + 30) / 5) + 1))
    w = P.water[J, I]
    dmin = min([poly.distance(Point(i * 5, j * 5)) for i, j in zip(I[w], J[w])] or [99])
    wd.append((round(dmin, 1), s["id"]))
wd.sort()
C["4 pads: no two within 12 m"] = dict(status="PASS" if not bad4 else "FAIL", closest=worst[:1])
C["4 pads: edge >= 10 m from the +0.3 m line (harbour / beach works exempt)"] = dict(status="PASS" if not wd or wd[0][0] >= 10 else "FAIL", closest=wd[:3],
    exempt=[s["id"] for s in pads if s.get("water_ok")])
mains = [x for x in pads if x.get("role") in ("FINAL", "MAIN") and x["id"] != "3-F-N"] + [dict(id=t, x=v["hull"].centroid.x, y=v["hull"].centroid.y) for t, v in towns.items() if R.get(t, {}).get("role") in ("FINAL", "MAIN")]
md = sorted((round(math.dist((a["x"], a["y"]), (b["x"], b["y"]))), a["id"], b["id"]) for i, a in enumerate(mains) for b in mains[i + 1:] if a["id"].split("-N")[0].split("-T")[0] != b["id"].split("-N")[0].split("-T")[0])
C["5 final and mains >= 400 m apart"] = dict(status="PASS" if not md or md[0][0] >= 400 else "FAIL", closest=md[:3])
C["6 approaches (two per main, designed)"] = dict(status="SEE NOTES", per_main=getattr(op, "APPROACHES", {}))
C["7 no rock walls / rock towers as dressing on fought ground"] = dict(status="PASS (none placed by this plan)")

plan = dict(op=int(N), name=getattr(op, "NAME", ""), frame="map metres, x east, y north, origin SW corner; yaw clockwise from north; hx along the pad's local x",
            sites=[{k: v for k, v in s.items() if not k.startswith("_")} for s in pads if not s["id"].startswith("A")],
            squad_positions=[{k: v for k, v in s.items() if not k.startswith("_")} for s in pads if s["id"].startswith("A")],
            towns=[{k: v for k, v in t.items() if k != "hull"} | {"hull": [list(map(lambda q: round(q, 1), p)) for p in t["hull"].exterior.coords]} for t in towns.values()],
            roads=P.roads, external_roads_joined=sorted({x for r in P.roads for x in r["links"] if x.startswith("op") and ":" in x}), trunk_breaks=trunk_breaks, foot_links=foot, approaches=getattr(op, "APPROACHES", {}), shores=shores, gate=getattr(op, "GATE", None), moves=[dict(id=s["id"], from_xy=list(s.get("design_xy", s["rough"])), to_xy=[s["x"], s["y"]], moved_m=s["moved_m"]) for s in pads if s.get("moved_m", 0) > 0 and not s["id"].startswith("A")],
            log=log)
json.dump(plan, open(os.path.join(OUT, f"op{N}_plan.json"), "w"), indent=1, default=float)
json.dump(C, open(os.path.join(OUT, f"op{N}_checks.json"), "w"), indent=1, default=str)

# ---- plan image
x0, x1, y0, y1 = op.VIEW if hasattr(op, "VIEW") else op.BOX
h, hs = world.hillshade(x0, x1, y0, y1)
X = np.linspace(x0, x0 + 5 * (h.shape[1] - 1), h.shape[1]); Y = np.linspace(y0, y0 + 5 * (h.shape[0] - 1), h.shape[0])
fig, ax = plt.subplots(figsize=(18, 14))
ax.imshow(hs, origin="lower", extent=(X[0], X[-1], Y[0], Y[-1]), cmap="gray", alpha=0.85)
ax.contourf(X, Y, h, levels=[-500, 0.3], colors=["#a9cbe0"], alpha=0.8)
cs = ax.contour(X, Y, h, levels=range(50, 700, 50), colors="#6b5a3a", linewidths=0.35); ax.clabel(cs, fontsize=6, fmt="%d")
for sh in shores: ax.plot([sh["from_xy"][0], sh["to_xy"][0]], [sh["from_xy"][1], sh["to_xy"][1]], color="#00a6d6", lw=4, alpha=0.7, solid_capstyle="round")
for r in EXT_ROADS:
    p = np.array(r["points"]); ax.plot(p[:, 0], p[:, 1], color="#6b6b6b", lw=1.8, ls="--")
for r in P.roads:
    p = np.array(r["points"]); ax.plot(p[:, 0], p[:, 1], color="#b5651d", lw=2.2)
for fl in foot:
    ax.plot([fl["bottom_xyz"][0], fl["top_xyz"][0]], [fl["bottom_xyz"][1], fl["top_xyz"][1]], color="#6a3d9a", lw=1.4, ls="--")
for t in towns.values():
    hp = np.array(t["hull"].exterior.coords); ax.fill(hp[:, 0], hp[:, 1], fc="#f4d06f", ec="#8a6d00", alpha=0.7)
    ax.text(*t["hull"].centroid.coords[0], f"{t['id']} {t['name']}\n(town, {t['n_buildings']} bldgs)", fontsize=8, ha="center", weight="bold")
    if t["id"] in R:     # the purpose map's point for the town, and how far the K6 layout sits from it
        dx_, dy_ = R[t["id"]]["x"], R[t["id"]]["y"]; cx_, cy_ = t["hull"].centroid.coords[0]
        ax.plot([dx_, cx_], [dy_, cy_], color="r", ls=":", lw=1.2); ax.plot(dx_, dy_, "rx", ms=8, mew=2)
        ax.text(dx_, dy_ - 60, f"{t['id']} purpose-map point\n({math.dist((dx_, dy_), (cx_, cy_)):.0f} m from the layout)", fontsize=6.5, color="r", ha="center", va="top")
for e in EXT.values():
    c_ = rect(e["x"], e["y"], e["hx"], e["hy"], e["yaw"]); ax.fill(c_[:, 0], c_[:, 1], fc="none", ec="k", hatch="///", lw=0.8)
    ax.text(e["x"] + e["hx"] + 15, e["y"], e["id"], fontsize=7, va="center")
col = {"FINAL": "#d62728", "MAIN": "#ff7f0e", "SUP": "#1f77b4", "squad position": "#7f7f7f"}
for s in pads:
    c = rect(s["x"], s["y"], s["hx"], s["hy"], s["yaw"])
    ax.fill(c[:, 0], c[:, 1], fc=col.get(s.get("role"), "#2ca02c"), ec="k", lw=0.6, alpha=0.85)
    if "entrance_xy" in s: ax.plot(*s["entrance_xy"], "w^", ms=5, mec="k")
    lab = s["id"] if s["id"].startswith("A") else f"{s['id']} {s['name']}"
    ax.text(s["x"] + s["hx"] + 10, s["y"], lab, fontsize=7.5 if not s["id"].startswith("A") else 6.5, color="k", weight="bold" if s.get("role") in ("FINAL", "MAIN") else None,
            bbox=dict(fc="white", ec="none", alpha=0.6, pad=0.5))
    ax.plot([s.get("design_xy", s["rough"])[0], s["x"]], [s.get("design_xy", s["rough"])[1], s["y"]], color="r", lw=0.6, ls=":")
for tb in trunk_breaks:
    ax.plot(*tb["at"], marker="X", color="#d62728", ms=14, mec="k"); ax.text(tb["at"][0] + 40, tb["at"][1] - 60, "GAP: " + tb["label"].split(";")[-1].strip(), color="#d62728", fontsize=8, weight="bold",
                                                                              bbox=dict(fc="white", ec="#d62728", alpha=0.8))
if getattr(op, "GATE", None):
    (ga, gb) = op.GATE; ax.plot([ga[0], gb[0]], [ga[1], gb[1]], color="#d62728", lw=3, ls="--"); ax.text((ga[0] + gb[0]) / 2 + 20, (ga[1] + gb[1]) / 2, getattr(op, "GATE_LABEL", "sea gate"), color="#d62728", fontsize=8)
ax.plot([x1 - 1100, x1 - 100], [y0 + 120, y0 + 120], "k", lw=4); ax.text(x1 - 600, y0 + 160, "1 km", ha="center")
ax.annotate("N", xy=(x0 + 150, y1 - 150), xytext=(x0 + 150, y1 - 450), arrowprops=dict(arrowstyle="->", lw=2), ha="center", fontsize=12)
from matplotlib.patches import Patch
from matplotlib.lines import Line2D
ax.legend(handles=[Patch(fc=col["FINAL"], label="final"), Patch(fc=col["MAIN"], label="main"), Patch(fc=col["SUP"], label="supporting"),
                   Patch(fc=col["squad position"], label="squad position"), Patch(fc="#f4d06f", label="town (K6 layout)"), Line2D([], [], color="#b5651d", lw=2, label="dirt road (7 m)"), Line2D([], [], color="#6a3d9a", ls="--", label="foot link (stair / path; not graded)"),
                   Line2D([], [], color="#00a6d6", lw=4, label="landing shore (boat)"), Line2D([], [], color="r", ls=":", label="moved from the purpose map point"),
                   Line2D([], [], marker="^", color="w", mec="k", ls="", label="entrance (road end)")], loc=getattr(op, "LEGEND_LOC", "lower left"), fontsize=8)
nfail = sum(1 for v in C.values() if str(v["status"]).startswith("FAIL"))
ax.set_title(f"Op {N}: {getattr(op, 'NAME', '')} ground plan (Kernel, PROPOSED) over the real ground, build 4 | rules failing: {nfail}", fontsize=13)
ax.set_xlim(x0, x1); ax.set_ylim(y0, y1); ax.set_aspect("equal"); ax.set_xlabel("x east (m)"); ax.set_ylabel("y north (m)")
fig.savefig(os.path.join(OUT, f"op{N}_plan.png"), dpi=90, bbox_inches="tight"); plt.close(fig)
print("\n".join(log)); print({k: v["status"] for k, v in C.items()})
