"""House fit check for the 6-M4 town and the 5-13 hamlet: how many house plots fit on the town's dry ground round its guard pads and streets.
A plot is a square of side P (20 m: a house of about 14 m, the middle of the WH house sizes in the K6 grader, plus 3 m all round; 25 m: also room for lanes; both ASSUMED),
on a grid tried at every 5 m offset. A plot counts when it is all dry (>= +0.5 m, village form rule), 5 m clear of the +0.3 m line (ASSUMED),
3 m clear of a 7 m road or street edge (the planner rule), and 5 m clear of a guard pad (ASSUMED). The town's ground is its dry rise within R of its point.
Usage: housefit.py <pack> <op 6 plan> <op 5 plan> <out>"""
import sys, json, math, numpy as np
from scipy import ndimage as nd
PK, P6, P5, OUT = sys.argv[1:5]
H = np.load(PK + "/ground/height_whole_cm.npz")["height_cm"] / 100.0; C = 5.0
G6 = json.load(open("town64/town64_guards_v1.json")); G5 = json.load(open("hamlet513/guards513_v1.json"))
def line(x0, y0, b, L): return np.array([[x0 + d * math.sin(math.radians(b)), y0 + d * math.cos(math.radians(b))] for d in np.arange(0, L + 0.1, 2.0)])
def rect_d(X, Y, o):
    t = math.radians(o["yaw"]); dx, dy = X - o["x"], Y - o["y"]; u = dx * math.cos(t) - dy * math.sin(t); v = dx * math.sin(t) + dy * math.cos(t)
    return np.hypot(np.maximum(abs(u) - o["hx"], 0), np.maximum(abs(v) - o["hy"], 0))
TOWNS = {
 "6-M4": dict(pt=(13600.0, 11200.0), R=400.0, want=80, pads=[G6["FOB"], G6["SSW gun"], G6["N gun"]],
              roads=[line(13600, 11200, 214, 194)] + [np.array(r["points"], float) for r in json.load(open(P6))["roads"]]),
 "5-13": dict(pt=(1840.0, 9705.0), R=200.0, want=30, pads=[m for m in G5["members"]],
              roads=[line(1840, 9705, b, G5["stubs"][k]["length_m"]) for k, b in (("NNE gate", 31), ("SE gate", 123))] + [np.array(r["points"], float) for r in json.load(open(P5))["roads"]]),
}
out = {}
for tid, T in TOWNS.items():
    x0, y0 = T["pt"]; R = T["R"] + 40
    i0, i1, j0, j1 = int((y0 - R) / C), int((y0 + R) / C) + 1, int((x0 - R) / C), int((x0 + R) / C) + 1
    sub = H[i0:i1, j0:j1]; yy, xx = np.mgrid[i0:i1, j0:j1] * C
    lab, _ = nd.label(sub >= 0.5); k = lab[int(round(y0 / C)) - i0, int(round(x0 / C)) - j0]
    rise = (lab == k) & (np.hypot(xx - x0, yy - y0) <= T["R"])
    wet = sub <= 0.3; dwet = nd.distance_transform_edt(~wet) * C
    ok = rise & (dwet >= 5.0)
    for o in T["pads"]: ok &= rect_d(xx, yy, o) >= 5.0
    from scipy.spatial import cKDTree
    RP = np.vstack([r for r in T["roads"] if len(r)]); near = cKDTree(RP).query(np.c_[xx.ravel(), yy.ravel()])[0].reshape(xx.shape)
    ok &= near >= 3.5 + 3.0
    res = dict(rise_ha=round(float(rise.sum()) * C * C / 1e4, 1), usable_ha=round(float(ok.sum()) * C * C / 1e4, 1), want=T["want"], plots={})
    for P in (20.0, 25.0):
        n = int(P / C); best = 0
        for oi in range(n):
            for oj in range(n):
                cnt = 0
                for a in range(oi, ok.shape[0] - n, n):
                    for b in range(oj, ok.shape[1] - n, n):
                        if ok[a:a + n + 1, b:b + n + 1].all(): cnt += 1
                best = max(best, cnt)
        res["plots"][f"{int(P)} m"] = best
    out[tid] = res; print(tid, res)
json.dump(out, open(OUT, "w"), indent=1)
