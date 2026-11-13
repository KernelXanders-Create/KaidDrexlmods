"""The whole map (11 Nov C pack): 5 m grid, row = y / 5 (row 0 south), col = x / 5 (col 0 west), metres."""
import os, json, math
import numpy as np
PACK = os.environ.get("PACK_C", "/tmp/claude-0/-home-user-KaidDrexlmods/68d91108-852d-5f8a-b84e-f7c6d8824e63/scratchpad/handoff_11nov_c")
_H = None


def H():
    global _H
    if _H is None:
        _H = np.load(os.path.join(PACK, "ground", "height_whole_cm.npz"))["height_cm"].astype(np.float64) / 100.0
    return _H


def z(x, y):
    """bilinear height at map (x, y) between grid points (the game's own interpolation is triangle-based; this is for routing only)"""
    h = H(); c, r = x / 5.0, y / 5.0; c0, r0 = int(math.floor(c)), int(math.floor(r)); fc, fr = c - c0, r - r0
    a, b, d, e = h[r0, c0], h[r0, c0 + 1], h[r0 + 1, c0], h[r0 + 1, c0 + 1]
    return float(a * (1 - fc) * (1 - fr) + b * fc * (1 - fr) + d * (1 - fc) * fr + e * fc * fr)


def objectives():
    return json.load(open(os.path.join(PACK, "design", "objectives_v2.json")))


def hillshade(x0, x1, y0, y1, az=315, alt=45):
    h = H()[int(y0 // 5):int(y1 // 5) + 1, int(x0 // 5):int(x1 // 5) + 1]
    gy, gx = np.gradient(h, 5.0)
    slope = np.pi / 2 - np.arctan(np.hypot(gx, gy)); aspect = np.arctan2(-gx, gy)
    a, al = np.radians(az), np.radians(alt)
    hs = np.sin(al) * np.sin(slope) + np.cos(al) * np.cos(slope) * np.cos(a - aspect)
    return h, np.clip(hs, 0, 1)
