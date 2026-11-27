"""Pack v10: pack v9 plus P16 (HUMAN): the 5-12 junction ground request at the 5-03 -> 5-F.3 road join, (2733, 11760), net level +0.66 m.
Cut only: within 40 m of the join, ground is lowered to no more than +0.66 m + 3 % of the distance (+1.86 m at 40 m), so a road arriving
there meets the net level. The 40 m reach and 3 % slope are ASSUMED. Ground is never raised; the +0.3 m water line is not crossed (cut floor +0.66 m)."""
import sys, json, shutil, numpy as np
A, B = sys.argv[1:3]
shutil.copytree(A, B, dirs_exist_ok=True)
H = np.load(A + "/ground/height_whole_cm.npz")["height_cm"].astype(float) / 100
log = json.load(open(A + "/ground_requests_applied.json"))
x0, y0, z0, reach, slope = 2733.0, 11760.0, 0.66, 40.0, 0.03
yy, xx = np.mgrid[0:H.shape[0], 0:H.shape[1]]; d = np.hypot(xx * 5.0 - x0, yy * 5.0 - y0)
m = d <= reach; cap = z0 + slope * d
before = H.copy(); H[m] = np.minimum(H[m], cap[m]); cut = before - H
log.append(dict(decision="ops 5-6 planner P16", kind="junction ground request (cut)", site="5-12 road join on 5-03-5-F.3", x=x0, y=y0, net_level_m=z0,
                reach_m=reach, slope=slope, max_cut_m=round(float(cut.max()), 2), cut_m3=int(cut.sum() * 25), cells_changed=int((cut > 0.005).sum()),
                source="HUMAN decision; reach and slope ASSUMED"))
np.savez_compressed(B + "/ground/height_whole_cm.npz", height_cm=np.rint(H * 100).astype(np.int32))
json.dump(log, open(B + "/ground_requests_applied.json", "w"), indent=1); print(log[-1])
