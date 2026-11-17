"""Turn a sketch planner plan (opN_plan.json + _suddra.json) into the JOB_2 return structure, with gun facing, entrances and reserve areas
measured on the K3 sketch ground. Usage: python3 assemble.py <N> <planner out dir> <sizes csv> <out json>"""
import sys, json, math, csv
import numpy as np
from shapely.geometry import Polygon, LineString, Point
import world
from planner import rect

N = int(sys.argv[1]); D = json.load(open(f"{sys.argv[2]}/op{N}_plan.json")); SX = json.load(open(f"{sys.argv[2]}/op{N}_plan_suddra.json"))
T = {r["composition"]: r for r in csv.DictReader(open(sys.argv[3]))}
R = {s["id"]: s for s in world.objectives()["sites"]}
APP = {3: {"3-F": [297, 243], "3-M1": [253, 188], "3-M2": [273, 235], "3-M3": [220, 256], "3-M4": [315, 72]},
       4: {"4-F": [215, 269], "4-M1": [91, 336], "4-M2": [190, 309], "4-M3": [214, 238], "4-M4": [250, None]}}[N]
APP_TXT = {3: {"3-F": ["W along the pipeline road past 3-M2 (297 deg)", "SW past 3-M4 / 3-02 (243 deg)"], "3-M1": ["WSW past 3-12 (253 deg)", "S from 3-F once it falls (188 deg)"],
               "3-M2": ["W from the start (273 deg)", "SW past 3-05 (235 deg)"], "3-M3": ["SW past 3-M1 (220 deg)", "WSW past 3-07 (256 deg)"], "3-M4": ["NW past 3-05 (315 deg)", "E from 3-02 once it falls (72 deg)"]},
           4: {"4-F": ["SW past 4-04 (215 deg)", "W along the bank from 4-M2 once it falls (269 deg)"], "4-M1": ["E along the north bank from the Plank Road causeway, on the road to 4-M3 (91 deg; decision 46)", "NNW past 4-09 (336 deg)"],
               "4-M2": ["SSW past 4-01 to the south gate (190 deg)", "over the 4-06 causeway to the north gate (309 deg)"], "4-M3": ["SSW past 4-11 from the Rail Bridge (214 deg)", "WSW from the 4-06 causeway (238 deg)"],
               "4-M4": ["WSW past 4-05 (250 deg)", "by player boat through the lock once 4-F falls"]}}[N]
START = {3: (8200, 3600), 4: (2600, 3200)}[N]
FLOOR = {"squad": (49, 69), "two_squad": (116, 165), "platoon": (159, 312)}
pads = {s["id"]: s for s in D["sites"]}
BEARING_OVERRIDE = {"4-M1.3": (330, "HUMAN (decision 45): 6 deg west of the NNW approach, clear of the re-seated checkpoint 4-M1.4")}
polys = {k: Polygon(rect(s["x"], s["y"], s["hx"], s["hy"], s["yaw"])) for k, s in pads.items()}
def brg(a, b): return math.degrees(math.atan2(b[0] - a[0], b[1] - a[1])) % 360
def mean_bearing(bs):
    bs = [b for b in bs if b is not None]; x = sum(math.sin(math.radians(b)) for b in bs); y = sum(math.cos(math.radians(b)) for b in bs); return math.degrees(math.atan2(x, y)) % 360
road_ends = []
for r in D["roads"]:
    for e in (0, -1): road_ends.append((tuple(r["points"][e]), r["points_z"][e], r["id"]))
sites = []; facing_rows = []
for base in sorted({k.split(".")[0] for k in pads}, key=lambda k: (k[2] != "F", k)):
    s0 = R.get(base, {}); mem = []; g = o = 0; unk = False
    for k in sorted([k for k in pads if k.split(".")[0] == base]):
        p = pads[k]; t = T.get(p["comp"]); guns = int(t["static_guns"]) if t else None
        if t: g += int(t["garrison_points"]); o += int(t["objects"])
        elif not p["comp"].startswith("town"): unk = True
        # entrance: the nearest road end to this pad (the planner ends roads 2.5 m off the pad edge, on the edge facing the road)
        ent = None
        if p.get("astride"):     # decision 43: the road runs through this checkpoint's passage
            ent = dict(x=p["x"], y=p["y"], faces_deg="along the road", sill_step_m=0.0, road_end_m=0.0, astride=dict(road=p["astride"]["road"], axis_offset_m="<= 2.0 (MEASURED when seated)", angle_deg=0, passage_axis="local y (ASSUMED)"), on_gate_axis="the road is the passage axis")
        near = None if ent else min(road_ends, key=lambda e: polys[k].exterior.distance(Point(e[0]))) if road_ends else None
        if near and polys[k].exterior.distance(Point(near[0])) < 20:
            q = polys[k].exterior.interpolate(polys[k].exterior.project(Point(near[0])))
            ent = dict(x=round(near[0][0], 1), y=round(near[0][1], 1), faces_deg=round(brg((p["x"], p["y"]), near[0])), sill_step_m=round(abs(p["z"] - near[1]), 2),
                       road_end_m=round(Point(near[0]).distance(q), 1), on_gate_axis="NOT MEASURED (the comp's authored gate position is not known)", road=near[2])
        gl = []
        if guns:
            bs = [x for x in (APP.get(base) or []) if x is not None]
            c0 = (pads[base]["x"], pads[base]["y"])
            if not bs: b = round(brg((p["x"], p["y"]), START)); why = "toward the op start (no designed approach for a supporting site)"
            elif k == base or math.dist(c0, (p["x"], p["y"])) < 1: b = round(bs[0]); why = "the site's first designed approach"
            else:     # a member faces the designed approach on its own side of the site
                own = brg(c0, (p["x"], p["y"])); b = round(min(bs, key=lambda x: abs((x - own + 180) % 360 - 180))); why = "the designed approach on this member's side of the site"
            if k in BEARING_OVERRIDE: b, why = BEARING_OVERRIDE[k]
            mz = p["z"] + 2.0
            prof = [(d, world.z(p["x"] + d * math.sin(math.radians(b)), p["y"] + d * math.cos(math.radians(b)))) for d in range(0, 301, 5)]
            rise = max(z for d, z in prof if d <= 150) - mz
            ln = LineString([(p["x"], p["y"]), (p["x"] + 300 * math.sin(math.radians(b)), p["y"] + 300 * math.cos(math.radians(b)))])
            hit = sorted((Point(p["x"], p["y"]).distance(ln.intersection(pl)), kk) for kk, pl in polys.items() if kk != k and ln.intersects(pl))
            gl.append(dict(guns=guns, bearing=b, approach=why,
                           clear_m=round(hit[0][0]) if hit else 300, rise_150m_m=round(rise, 2), first_comp_hit=hit[0][1] if hit else None, muzzle="pad + 2.0 m (ASSUMED)", source="HUMAN (bearing)" if k in BEARING_OVERRIDE else "AI (bearing)"))
            facing_rows.append([k, p["comp"], guns, b, round(rise, 2), hit[0][1] if hit else None])
        mem.append(dict(comp=p["comp"], part="main" if k == base else "member", x=p["x"], y=p["y"], yaw=p["yaw"],
                        pad=dict(hx=p["hx"], hy=p["hy"], z=p["z"], cut_fill_max_m=p.get("max_change_m", p.get("change_m"))),
                        gps=int(t["garrison_points"]) if t else None, objects=int(t["objects"]) if t else None, size_from="measured_table" if t else "ESTIMATE (not in the size table)",
                        pad_size_from=p.get("size_note", ""), built_for="NOT MEASURED (per comp)", guns=gl, entrance=ent))
    if base == "4-F":     # the CIS Fortress Dam is the crossing itself, not a pad here
        mem.insert(0, dict(comp="CIS Fortress Dam with GPs", part="main", x=10393, y=7230, yaw=0, pad="the dam spans the Drain (see crossings)", gps=None, objects=None,
                           size_from="ESTIMATE (not in the size table)", guns=[], entrance=None)); unk = True
        mem[1]["part"] = "member"
    tier = s0.get("tier"); fl = FLOOR.get(tier, (0, 0))
    floor = "gps" if g >= fl[0] else "objects" if o >= fl[1] else ("NOT MEASURED" if unk else "NO")
    if s0.get("id") in ("3-11", "4-12"): floor = "air-only, exempt"
    if any(m["comp"].startswith("town") for m in mem): floor = "town work: 140 house garrison + the guards' GPs (ASSUMED meets)" if g < fl[0] else floor
    sites.append(dict(id=base, name=s0.get("name"), role=s0.get("role"), grade=tier, stake=s0.get("stake"), approaches=APP_TXT.get(base, []), recon_m="NOT MEASURED (no vegetation on the sketch)",
                      landmass=("south bank" if N == 4 and pads[base]["y"] < 7150 else "north bank") if N == 4 else 1, members=mem, sum_gps=g, sum_objects=o, floor_met=floor,
                      moved_from_design_m=pads[base].get("moved_m"), source="HUMAN (comps, see DECISIONS.md); AI (pad positions by the planner on the sketch)"))
# reserves: for every main and the final, a start area 250-400 m out on the side away from its approaches, dry (>= +0.5 m), 50 m clear of pads and roads
roads_ls = [LineString(r["points"]) for r in D["roads"]]
res = []
for base, bs in APP.items():
    if base not in pads: continue
    p = pads[base]; back = (mean_bearing(bs) + 180) % 360; best = None
    for dd in range(250, 401, 25):
        for off in range(0, 181, 15):
            for sg in (1, -1):
                b = (back + sg * off) % 360; q = (p["x"] + dd * math.sin(math.radians(b)), p["y"] + dd * math.cos(math.radians(b)))
                if world.z(*q) < 0.5: continue
                if any(pl.distance(Point(q)) < 50 for pl in polys.values()) or any(l.distance(Point(q)) < 30 for l in roads_ls): continue
                if N == 4 and ((q[1] < 7150) != (p["y"] < 7150)): continue
                best = dict(site=base, x=round(q[0]), y=round(q[1]), z=round(world.z(*q), 2), distance_m=dd, bearing_from_site=round(b), off_rear_deg=off,
                            out_of_sight="NOT MEASURED (no vegetation on the sketch)", same_dry_ground="yes (no water crossed, MEASURED on the sketch)" if N != 4 else "same bank (MEASURED on the sketch)", source="AI"); break
            if best: break
        if best: break
    res.append(best or dict(site=base, status="NO SPOT within 250-400 m on dry ground clear of pads and roads"))
plan = dict(op=N, concept="A", name=D["name"], ground="K3 A sketch (16 m cells resampled to 5 m); a dry run, to be re-run on drop 2",
            start_fob={3: "1-F", 4: "2-F"}[N], start_if_final_held="ship", fob_after={3: "3-F", 4: "4-M1 (fallback 4-F)"}[N],
            sites=sites, roads=[dict(id=r["id"], kind="dirt", width_m=7, links=r["links"], length_m=r.get("length_m"), raised_to_0_5=r.get("raised_to_0_5", False),
                                     points=[[round(x, 1), round(y, 1), round(z, 2)] for (x, y), z in zip(r["points"], r["points_z"])]) for r in D["roads"]],
            crossings=[], ground_requests=dict(pads=[dict(site=k, x=v["x"], y=v["y"], hx=v["hx"], hy=v["hy"], yaw=v["yaw"], z=v["z"]) for k, v in pads.items()], water=[], designed_straights=[]),
            reserves=res, towns=[], garrison_total={3: 770, 4: 885}[N], garrison_note="K3 per-site plan (+30 village for op 4); members added since are not in it (ASSUMED)",
            alive_split_proposal=dict(garrison_cap=700, director=200, zeus=300), checks_planner=json.load(open(f"{sys.argv[2]}/op{N}_checks.json")), checks_suddra=SX)
json.dump(plan, open(sys.argv[4], "w"), indent=1)
print("sites", len(sites), "reserves", sum(1 for r in res if "x" in r), "/", len(res)); print("facing (pad, comp, guns, bearing, rise in 150 m, first comp hit):")
for f in facing_rows: print("  ", f)
