"""Approaches vs planned roads, ops 3-6 (drop 2 plans). For each designed approach of a main or final:
does a planned road leave the site (any member) on that side? Bearing = from the site centre toward where the approach comes from."""
import json, math, os, re
H = os.path.dirname(os.path.abspath(__file__)); R = os.path.join(H, "../../..")
PLANS = {3: ["job2/drop2_check/rerun_ops34_v4/op3/op33_plan.json"],
         4: ["job2/drop2_check/rerun_ops34_v5/op4_north/op43_plan.json", "job2/drop2_check/rerun_ops34_v5/op4_south/op43_plan.json"],
         5: ["job5/drop2_check/planner_ops56_v4/op5_main/op5_plan.json"],
         6: ["job5/drop2_check/planner_ops56_v3/op6/op6_plan.json"]}
OUT_M = 150.0      # ASSUMED: the road's heading is read where it is 150 m out from the site centre
TOL = 45.0         # ASSUMED: a road "on that side" leaves within 45 deg of the approach bearing
# reviewed approaches for ops 5-6 (ops5_6_approaches_v2.md, HUMAN); ops 3-4 from the plans (JOB_2 decisions 16-25, call 6C), 4-M1 per JOB_2 decision 46
V2 = {"5-F": [("SSE up the esker road via 5-M1", 166), ("N down the esker from 5-M2 once it falls", 14)],
      "5-M1": [("E past 5-05 Kettle North Trench", 81), ("SW past 5-09 West Fuel Dump", 225)],
      "5-M2": [("NNE past 5-08 Stake Causeway Checkpoint", 39), ("E past 5-04 Walker Park", 97)],
      "5-M3": [("ESE from 5-M2 once it falls", 117), ("S past 5-02 West Esker AA", 196)],
      "5-M4": [("SW past 5-05", 219), ("WSW from 5-M1 once it falls", 252)],
      "6-F": [("SW over the rim past 6-M1", 225), ("E from 6-M4 Cauldron Apron Town", 86)],
      "6-M1": [("WSW from the start", 243), ("W past 6-04 Gas Holder", 277)],
      "6-M2": [("S past 6-01 Rim Spoil Galleries", 179), ("ENE past 6-02 Spoil Heap Snipers", 78)],
      "6-M3": [("WNW past 6-01", 288), ("SE past 6-10 Crater Lip Pillboxes", 122)],
      "6-M4": [("SSW from 6-M3 once it falls", 214), ("N past 6-06 NE Esker Fort", 0)]}
def brg(a, b): return math.degrees(math.atan2(b[0] - a[0], b[1] - a[1])) % 360
def dif(a, b): return abs((a - b + 180) % 360 - 180)
SK = {s["id"]: tuple(s["xy"]) for s in json.load(open(os.path.join(R, "job5/ops5_8_sketch.json")))["sites"]}
rows = []
for op, files in PLANS.items():
    sites, roads, appr = {}, [], {}
    for f in files:
        D = json.load(open(os.path.join(R, f)))
        for s in D["sites"]: sites.setdefault(s["id"], s)
        roads += [r for r in D["roads"] if r["id"] not in {q["id"] for q in roads}]
        for k, v in D["approaches"].items(): appr.setdefault(k.split(" ")[0], (k, v))
    for sid, (full, ways) in appr.items():
        if op in (5, 6): ways = V2[sid]
        else:
            ways = [(w.rsplit(" (", 1)[0], float(m.group(1)) if (m := re.search(r"\((\d+) deg", w)) else None) for w in ways]
            if sid == "4-M1": ways = [("E along the north bank from the causeway (J2-46)", 91.0), ways[1]]
        if sid not in sites:      # a site with no pad (a town): its sketch point, 30 m reach (ASSUMED)
            x_, y_ = SK[sid]; sites[sid] = dict(id=sid, x=x_, y=y_, hx=15.0 / 1.414, hy=15.0 / 1.414)
        s0 = sites.get(sid); mem = [x for x in sites if x == sid or x.startswith(sid + ".")]
        heads = []          # (road, heading) for each way a road leaves the site
        for r in roads:
            pts = r["points"]
            for m in mem:
                s = sites[m]; reach = math.hypot(s["hx"], s["hy"]) + 15.0
                near = [i for i, p in enumerate(pts) if math.dist(p, (s["x"], s["y"])) <= reach]
                if not near and m not in r["links"]: continue
                if not near: near = [0 if math.dist(pts[0], (s["x"], s["y"])) < math.dist(pts[-1], (s["x"], s["y"])) else len(pts) - 1]
                for seq in (pts[max(near):], pts[:min(near) + 1][::-1]):
                    seqs = [seq]
                    if len(seq) and all(math.dist(p, (s0["x"], s0["y"])) < OUT_M for p in seq):     # a short spur: follow the road it joins, both ways
                        e = seq[-1]
                        for r2 in roads:
                            if r2 is r: continue
                            j = min(range(len(r2["points"])), key=lambda i: math.dist(r2["points"][i], e))
                            if math.dist(r2["points"][j], e) <= 15.0: seqs += [seq + r2["points"][j:], seq + r2["points"][:j + 1][::-1]]
                    for sq in seqs:
                        q = next((p for p in sq if math.dist(p, (s0["x"], s0["y"])) >= OUT_M), None)
                        if q is not None: heads.append((r["id"], round(brg((s0["x"], s0["y"]), q))))
        heads = sorted(set(heads))
        for way, b in ways:
            if b is None:
                rows.append(dict(op=op, site=full, way=way, bearing=None, result="not a land way (no bearing)", roads=heads)); continue
            best = min(heads, key=lambda h: dif(h[1], b)) if heads else None
            res = "no road at the site" if not heads else ("road on that side" if dif(best[1], b) <= TOL else "no road on that side")
            rows.append(dict(op=op, site=full, way=way, bearing=b, result=res,
                             closest_road=best[0] if best else None, closest_heading=best[1] if best else None,
                             off_deg=round(dif(best[1], b)) if best else None, roads=heads))
json.dump(rows, open(os.path.join(H, "approaches36_v1.json"), "w"), indent=1)
for r in rows: print(r["op"], r["site"].split(" ")[0], f'{r["bearing"]}', r["result"], r.get("closest_road"), r.get("closest_heading"), r.get("off_deg"), "| all:", [h[1] for h in r["roads"]])
