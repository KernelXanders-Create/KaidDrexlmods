"""Build a planner pack on the drop 2 ground (5 m resample) with Kernel's ground requests applied as ASSUMED fills."""
import sys, os, json, math, shutil, numpy as np
from scipy import ndimage as nd
D, SK, OUT, PL = sys.argv[1:5]
h = np.load(D + "/suddra_height_cm.npz", allow_pickle=False)["height_cm"].astype(np.float64) / 100
n = 3201; c = np.arange(n) * 5.0 / 4.0          # 5 m grid points in 4 m cell units
I, J = np.meshgrid(c, c, indexing="ij")
H = nd.map_coordinates(h, [I, J], order=1, mode="nearest")
P3 = json.load(open(PL + "/op3_plan_sketch_v3.json")); P4 = json.load(open(PL + "/op4_plan_sketch_v3.json"))
def mem(P, sid, k): return [s for s in P["sites"] if s["id"] == sid][0]["members"][k]
REQ = [  # (plan, site, member index, level m, note)  levels ASSUMED (the lane's build)
 (P4, "4-M2", 0, 1.0, "f2"), (P4, "4-M2", 1, 1.0, "f2"), (P4, "4-M2", 2, 1.0, "f2"),
 (P4, "4-F", 1, 1.3, "f4"),
 (P4, "4-M1", 1, 0.75, "f5"), (P4, "4-M1", 3, 0.75, "f5"),
 (P3, "3-M2", 2, 0.75, "f6"),
 (P3, "3-10", 0, 0.75, "f7"), (P3, "3-10", 1, 0.75, "f7"), (P3, "3-10", 2, 0.75, "f7"),
 (P4, "4-11", 1, 1.0, "f10"),
 (P4, "4-06", 0, 0.75, "f13"), (P4, "4-06", 1, 0.75, "f13")]
log = []
for P, sid, k, L, note in REQ:
    m = mem(P, sid, k); p = m["pad"]; t = math.radians(m.get("yaw") or 0); marg = 10.0
    X = J * 0 + np.arange(n)[None, :] * 5.0; Y = np.arange(n)[:, None] * 5.0 + X * 0
    x0, y0 = m["x"], m["y"]; r = math.hypot(p["hx"], p["hy"]) + marg + 10
    i0, i1, j0, j1 = int((y0 - r) / 5), int((y0 + r) / 5) + 1, int((x0 - r) / 5), int((x0 + r) / 5) + 1
    yy, xx = np.mgrid[i0:i1, j0:j1] * 5.0
    u = (xx - x0) * math.cos(t) - (yy - y0) * math.sin(t); v = (xx - x0) * math.sin(t) + (yy - y0) * math.cos(t)
    inside = (abs(u) <= p["hx"] + marg) & (abs(v) <= p["hy"] + marg)
    blk = H[i0:i1, j0:j1]; before = blk[inside].min()
    blk[inside] = np.maximum(blk[inside], L); H[i0:i1, j0:j1] = blk
    log.append(dict(site=sid, member=k, comp=m["comp"], x=x0, y=y0, level_m=L, finding=note, lowest_before_m=round(float(before), 2), margin_m=marg))
os.makedirs(OUT + "/ground", exist_ok=True)
np.savez_compressed(OUT + "/ground/height_whole_cm.npz", height_cm=np.rint(H * 100).astype(np.int32))
for d in ("design", "ops_1_2"): shutil.copytree(SK + "/" + d, OUT + "/" + d, dirs_exist_ok=True)
shutil.copy(SK + "/ground/roads_ops_1_2.json", OUT + "/ground/")
json.dump(log, open(OUT + "/ground_requests_applied.json", "w"), indent=1)
print("H", H.shape, round(H.min(), 2), round(H.max(), 2)); [print(l) for l in log]
