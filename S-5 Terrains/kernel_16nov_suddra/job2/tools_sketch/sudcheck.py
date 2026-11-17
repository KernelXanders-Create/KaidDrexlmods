"""Suddra rules the Thirra planner does not hold, run on a finished plan (sketch dry run).
- AI roads and site pads at +0.5 m or higher (rule 37): road points below +0.5 m are raised to +0.5 m (fill), then re-measured.
- grades, measured on the points: dirt <= 14 %, point to point and over every 10 m and 20 m stretch.
- bend radius >= 12 m: the circle through each point and the points 5 m either side.
- cut / fill <= 4 m at every road point after the raise.
Usage: python3 sudcheck.py <plan.json>  (writes <plan>_suddra.json beside it, and the raised plan as <plan> itself)"""
import sys, json, math
import numpy as np
import world

p = sys.argv[1]; D = json.load(open(p))
out = dict(raised_roads=[], grade=[], bend=[], cut_fill=[], pads_below=[])
for s in D["sites"]:
    if s["z"] < 0.5 - 1e-6: out["pads_below"].append([s["id"], s["z"]])
for r in D["roads"]:
    X = np.array(r["points"], float); Z = np.array(r["points_z"], float)
    low = Z < 0.5
    if low.any():
        out["raised_roads"].append(dict(id=r["id"], points=int(low.sum()), lowest_before=round(float(Z.min()), 3)))
        Z = np.maximum(Z, 0.5); r["points_z"] = [round(float(z), 3) for z in Z]; r["raised_to_0_5"] = True
    s_ = np.r_[0, np.cumsum(np.hypot(*np.diff(X, axis=0).T))]
    p2p = max(abs(Z[i + 1] - Z[i]) / max(s_[i + 1] - s_[i], 1e-6) for i in range(len(Z) - 1)) * 100
    def win(L):
        g = 0.0
        for i in range(len(Z)):
            j = np.searchsorted(s_, s_[i] + L)
            if j < len(Z): g = max(g, abs(Z[j] - Z[i]) / (s_[j] - s_[i]) * 100)
        return g
    out["grade"].append([r["id"], round(p2p, 2), round(win(10.0), 2), round(win(20.0), 2)])
    rad = 1e9; jrad = 1e9
    for i in range(len(X)):
        a = np.searchsorted(s_, s_[i] - 5.0, side="right") - 1; b = np.searchsorted(s_, s_[i] + 5.0)
        if a < 0 or b >= len(X) or a == i or b == i: continue
        A, B, C = X[a], X[i], X[b]
        ab, bc, ca = math.dist(A, B), math.dist(B, C), math.dist(C, A)
        cross = abs((B[0] - A[0]) * (C[1] - A[1]) - (B[1] - A[1]) * (C[0] - A[0]))
        if cross > 1e-6:
            rr = ab * bc * ca / (2 * cross)
            if s_[i] < 12.0 or s_[-1] - s_[i] < 12.0: jrad = min(jrad, rr)     # the turn off (onto) the net at a junction or a pad edge: reported apart
            else: rad = min(rad, rr)
    out["bend"].append([r["id"], round(rad, 1) if rad < 1e8 else None]); out.setdefault("junction_turns", []).append([r["id"], round(jrad, 1) if jrad < 1e8 else None])
    nat = np.array([world.z(x, y) for x, y in X]); out["cut_fill"].append([r["id"], round(float(np.abs(Z - nat).max()), 2)])
S = dict(rule_37_pads_below_0_5=out["pads_below"], rule_37_roads_raised=out["raised_roads"],
         grade_dirt_14=dict(status="PASS" if max(max(g[1:]) for g in out["grade"]) <= 14.0 else "FAIL", worst=max(out["grade"], key=lambda g: max(g[1:]))),
         bend_radius_12=dict(status="PASS" if all(b[1] is None or b[1] >= 12.0 for b in out["bend"]) else "FAIL", tightest=min((b for b in out["bend"] if b[1]), key=lambda b: b[1], default=None),
                             under_12=[b for b in out["bend"] if b[1] is not None and b[1] < 12.0]),
         junction_turns_under_12=[b for b in out["junction_turns"] if b[1] is not None and b[1] < 12.0],
         cut_fill_4=dict(status="PASS" if max(c[1] for c in out["cut_fill"]) <= 4.0 else "FAIL", worst=max(out["cut_fill"], key=lambda c: c[1])),
         method="measured on the plan's road points (5 m apart or closer) after raising any point under +0.5 m to +0.5 m; bend radius from the circle through each point and the points 5 m before and after it; turns within 12 m of a road end (where it leaves the net or a pad edge) are listed apart as junction turns, NOT as passes")
json.dump(D, open(p, "w"), indent=1); json.dump(S, open(p.replace(".json", "_suddra.json"), "w"), indent=1)
print(json.dumps({k: (v if not isinstance(v, dict) else {kk: vv for kk, vv in v.items() if kk != "under_12"}) for k, v in S.items() if k != "method"})[:1500])
print("bends under 12 m:", len(S["bend_radius_12"]["under_12"]))
