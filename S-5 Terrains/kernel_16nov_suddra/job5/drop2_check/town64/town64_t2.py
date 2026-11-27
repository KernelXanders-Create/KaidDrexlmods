"""T2 (HUMAN): the SSW road is a shore stub from the town point to a K1 boat landing (graded beach -1.5 m to +0.5 m at 1:6, 12 m wide) toward 6-M3.
Profile along 214 deg from the town point: the stub, where the ground drops through +0.5 m and -1.5 m, and the grade of the stub."""
import sys, json, math, numpy as np
PK = sys.argv[1]
H = np.load(PK + "/ground/height_whole_cm.npz")["height_cm"] / 100.0
X0, Y0, b = 13600.0, 11200.0, 214.0; ux, uy = math.sin(math.radians(b)), math.cos(math.radians(b))
z = lambda t: float(H[int(round((Y0 + uy * t) / 5)), int(round((X0 + ux * t) / 5))])
d = np.arange(0, 400, 5.0); zs = np.array([z(t) for t in d])
d = np.arange(0, 400, 1.0); zs = np.array([float(np.interp(0, [0], [0])) for _ in d])
def zi(t):     # bilinear on the 5 m grid
    x, y = (X0 + ux * t) / 5, (Y0 + uy * t) / 5; i, j = int(x), int(y); fx, fy = x - i, y - j
    return float(H[j, i] * (1 - fx) * (1 - fy) + H[j, i + 1] * fx * (1 - fy) + H[j + 1, i] * (1 - fx) * fy + H[j + 1, i + 1] * fx * fy)
zs = np.array([zi(t) for t in d])
t05 = next(t for t, q in zip(d, zs) if t > 100 and q < 0.5); tm15 = next((t for t, q in zip(d, zs) if t > t05 and q <= -1.5), None)
dry = d < t05; g = np.abs(zs[dry][10:] - zs[dry][:-10]) / 10 * 100
xy = lambda t: [round(X0 + ux * t), round(Y0 + uy * t)]
out = dict(stub_from=[X0, Y0], stub_bearing=b, stub_length_m=int(t05), stub_worst_10m_grade_pct=round(float(g.max()), 1), stub_ground_m=[round(float(zs[dry].min()), 2), round(float(zs[dry].max()), 2)],
           landing_top_xy=xy(t05), landing_top_ground_m=0.5,
           ground_reaches_minus_1_5_m_at=None if tm15 is None else dict(from_point_m=int(tm15), xy=xy(tm15), natural_run_m=int(tm15 - t05), natural_slope="1:%.1f" % ((tm15 - t05) / 2.0)),
           k1_graded_run_m=12.0, profile_beyond=[[int(t), round(q, 2)] for t, q in zip(d, zs) if t05 - 10 <= t <= t05 + 60][::5])
print(json.dumps(out))
