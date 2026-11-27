"""Ground on an approach side: the line from a site's centre along the approach bearing, and lines 150 m either side.
Usage: PACK_C=<pack> python3 sideground36.py x y bearing length"""
import sys, math, numpy as np
sys.path.insert(0, __import__("os").path.join(__import__("os").path.dirname(__import__("os").path.abspath(__file__)), "../../../job2/tools_sketch"))
import world
x0, y0, b, L = map(float, sys.argv[1:5]); start = float(sys.argv[5]) if len(sys.argv) > 5 else 60.0
ux, uy = math.sin(math.radians(b)), math.cos(math.radians(b)); px, py = -uy, ux
for off in (-150, 0, 150):
    d = np.arange(start, L, 10.0); zs = np.array([world.z(x0 + ux * t + px * off, y0 + uy * t + py * off) for t in d]); g = np.abs(np.diff(zs)) / 10 * 100
    wet = zs <= 0.3; runs = []; i = 0
    while i < len(wet):
        if wet[i]:
            j = i
            while j < len(wet) and wet[j]: j += 1
            runs.append((int(d[i]), int(d[j - 1]) + 10)); i = j
        else: i += 1
    print(f"offset {off:+d} m: z {zs.min():.2f} to {zs.max():.2f}, wet {int(wet.sum() * 10)} m {runs[:5]}, worst 10 m grade {g.max():.1f} %")
