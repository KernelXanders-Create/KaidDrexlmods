"""Pack v8: pack v7 plus the approaches A4 causeways (HUMAN): 3-M2 W, 3-M4 NW and 6-M1 W, and a cut on the 6-M1 line.
Each causeway fills the line from its first wet stretch to its last (approaches36/causeway36_v1.jsonl) to +0.75 m, 25 m half-width.
The 6-M1 line is first cut so its ground runs at no more than 12 % along the line (cut only, never fill). Level, width and 12 % ASSUMED."""
import sys, json, math, shutil, os, numpy as np
A, B = sys.argv[1:3]
shutil.copytree(A, B, dirs_exist_ok=True)
H = np.load(A + "/ground/height_whole_cm.npz")["height_cm"].astype(float) / 100
log = json.load(open(A + "/ground_requests_applied.json"))
CW = [json.loads(l) for l in open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "approaches36/causeway36_v1.jsonl"))]
for c in CW:
    (x0, y0), (x1, y1) = c["line_from"], c["line_to"]; L = math.dist((x0, y0), (x1, y1)); ux, uy = (x1 - x0) / L, (y1 - y0) / L
    i0, i1 = int(min(x0, x1) / 5) - 8, int(max(x0, x1) / 5) + 9; j0, j1 = int(min(y0, y1) / 5) - 8, int(max(y0, y1) / 5) + 9
    jj, ii = np.mgrid[j0:j1, i0:i1]; X, Y = ii * 5.0, jj * 5.0; t = (X - x0) * ux + (Y - y0) * uy; n = np.abs(-(X - x0) * uy + (Y - y0) * ux)
    h = H[j0:j1, i0:i1]; before = h.copy()
    if c["approach"].startswith("6-M1"):        # cut: lower envelope of the line profile with a 12 % limit, on the whole line inside 25 m
        d = np.arange(0, L + 5, 5.0); zl = np.array([H[int(round((y0 + uy * s) / 5)), int(round((x0 + ux * s) / 5))] for s in d])
        p = np.array([np.min(zl + 0.12 * np.abs(d - s)) for s in d])
        m = (n <= 25) & (t >= 0) & (t <= L); pk = np.interp(t[m], d, p); h[m] = np.minimum(h[m], pk)
        cut = float((before - h).max())
    a, b = c["pieces"][0]["from_m"], c["pieces"][-1]["to_m"]
    m = (n <= 25) & (t >= a) & (t <= b); h[m] = np.maximum(h[m], 0.75)
    H[j0:j1, i0:i1] = h; ch = h - before
    log.append(dict(decision="approaches ops 3-6 A4", kind="causeway fill" + (" and line cut to 12 %" if c["approach"].startswith("6-M1") else ""), site=c["approach"].split(" ")[0],
                    approach=c["approach"], from_m=a, to_m=b, half_width_m=25, level_m=0.75, fill_m3=int(np.clip(ch, 0, None).sum() * 25), max_fill_m=round(float(ch.max()), 2),
                    cut_m3=int(np.clip(-ch, 0, None).sum() * 25), max_cut_m=round(float(-ch.min()), 2), source="HUMAN decision; level, width and 12 % ASSUMED"))
np.savez_compressed(B + "/ground/height_whole_cm.npz", height_cm=np.rint(H * 100).astype(np.int32))
json.dump(log, open(B + "/ground_requests_applied.json", "w"), indent=1); [print(l) for l in log[-3:]]
