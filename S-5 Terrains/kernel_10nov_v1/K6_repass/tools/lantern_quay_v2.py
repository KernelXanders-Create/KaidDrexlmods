"""Lantern Quay Hamlet (5-09, op 5) on the real ground: K6 config (PROPOSED).
Ground: a 12-17 % slope falling south-west from the K1 site (84 m) to the top of a
25-40 m sea escarpment; a beach strip 20-40 m wide at its foot. As your review asked,
the quay row moves down to the real shore (the beach strip); a stair climbs the
escarpment; the hamlet above sits on contour terraces (both rows, one level per
segment) joined by the stepped main street (ramp pieces) up to the pocket square."""
import math
import numpy as np
from shapely.geometry import Polygon, LineString, box
from scipy.ndimage import gaussian_filter
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as _plt
PACK = "/tmp/claude-0/-home-user-KaidDrexlmods/68d91108-852d-5f8a-b84e-f7c6d8824e63/scratchpad/handoff_10nov_b/KERNEL_HANDOFF_20261110b"
_X0, _Y0 = 7050, 16300
_H = np.load(PACK + "/towns6/lantern_quay/height_1m.npy"); _HS = gaussian_filter(_H, 5)
SLOPE = Polygon([(7262, 16512), (7330, 16512), (7410, 16512), (7480, 16514), (7530, 16520), (7536, 16560), (7520, 16640),
                 (7450, 16676), (7350, 16676), (7280, 16630), (7250, 16560)])


def contour_street(level, region=SLOPE, spacing=24.0):
    xs = np.arange(_X0, _X0 + _H.shape[1]); ys = np.arange(_Y0, _Y0 + _H.shape[0])
    cs = _plt.contour(xs, ys, _HS, levels=[level]); _plt.close()
    best = None
    for seg in cs.allsegs[0]:
        ls = LineString(seg).intersection(region)
        for p_ in ([ls] if ls.geom_type == "LineString" else list(getattr(ls, "geoms", []))):
            if p_.geom_type == "LineString" and (best is None or p_.length > best.length): best = p_
    n = max(2, int(best.length // spacing))
    pts = [tuple(np.round(best.interpolate(i / n, normalized=True).coords[0], 1)) for i in range(n + 1)]
    if pts[0][0] > pts[-1][0]: pts = pts[::-1]                 # run west to east
    out = [pts[0]]                                            # gentle bends (+-3.5 m) so no run is straight over 80 m
    for i in range(1, len(pts) - 1):
        a, b = np.array(pts[i - 1]), np.array(pts[i + 1]); t = (b - a) / np.linalg.norm(b - a); nn = np.array([-t[1], t[0]])
        out.append(tuple(np.round(np.array(pts[i]) + nn * 3.5 * (1 if i % 2 else -1), 1)))
    return out + [pts[-1]]


def ramp(id_, pts, a, b, name, w=5.0, out_cls=None):
    d = dict(id=id_, cls="lane", w=w, rows="none", name=name, pin_start=a, pin_end=b, ramp=True, landing=9.0, keep_landings=True, pts=pts, smooth=True)
    if out_cls: d["out_cls"] = out_cls
    return d


LEVELS = {"T58": 58, "T66": 66, "T74": 74, "T82": 82, "T90": 90}
QUAY_Z = 2.0
Q_PTS = [(7296, 16396), (7330, 16381), (7366, 16378), (7400, 16359), (7436, 16358), (7470, 16343)]
_ql = LineString(Q_PTS)
from shapely.ops import substring as _sub
_qw = _sub(_ql, 0, 42)
QUAY = Polygon(list(_qw.offset_curve(-4.0).coords) + list(_qw.offset_curve(-16.0).coords)[::-1])
SPINES = [((7250, 16480), (7330, 16690)), ((7345, 16430), (7440, 16680)), ((7440, 16430), (7540, 16620))]

CFG = dict(
    key="lantern_quay_v2", town="Lantern Quay Hamlet", version="K6 v2 (graded with the 11 Nov grader) PROPOSED", seed=4,
    tile=PACK + "/towns6/lantern_quay/height_1m.npy", tile_origin=(_X0, _Y0), ground_label="site tile (as built today)",
    target_n=66, garrison_range=(40, 55), square=True,
    view=((7240, 7560), (16310, 16690)),
    inset=dict(view=((7280, 7490), (16320, 16420)), title="the quay row on the beach strip (quay apron 2.0 m)"),
    title="Lantern Quay Hamlet (op 5, 5-09), K6 PROPOSED: quay row on the real shore, terraces above the escarpment, 5 m grid rule",
    labels={"sea escarpment (25-40 m)": (7250, 16440), "beacon path (to 5-M4)": (7470, 16684), "quay": (7380, 16330)},
    streets=[],
    notes=["PROPOSED by Kernel K6, Lantern Quay Hamlet, under the 5 m grid rule (10 Nov late note).",
           "As your review asked, the quay row moves down to the real shore: the beach strip at the foot of the sea escarpment, about 280 m south-south-west of the K1 site point.",
           "The escarpment (25-40 m) is climbed by a stair (a piece, not a graded street). Above it the hamlet sits on five contour terraces 8 m apart (58, 66, 74, 82 and 90 m), one row each, one level per segment; the terraces stop short of the escarpment so the ground between them and the quay can be graded.",
           "The stepped main street and the side stairs between terraces are stair pieces (listed below with their ends and levels), not graded streets. Boats and air only, so no vehicle road is needed.",
           "Lamps are yours."],
)
for sid, lev in LEVELS.items():
    CFG["streets"].append(dict(id=sid, cls="lane", w=5.0, rows="up", name=f"terrace lane ({lev} m contour)", pts=contour_street(lev), adaptive=True, tol=1.5))
CFG["streets"] += [
    dict(id="Q", cls="lane", w=5.0, rows=-1, name="quay lane (the quay row stands on the beach, doors on the lane)", pts=Q_PTS, adaptive=True, tol=1.5, band=(2.0, 5.0, 8.0)),
]
CFG["pool_main"] = ["WH01", "WH02", "WH03", "WH04", "WH09", "WH11", "WH12", "WH21", "WH23", "WH07", "WH08", "ND03", "ND01", "ND02", "WH24", "WH22", "WH19", "WH18", "SF15", "SF16"]
CFG["pool_lane"] = ["WH01", "WH04", "WH03", "WH11", "WH12", "WH08", "WH24", "ND01", "ND02", "ND03", "ND04", "WH06", "WH17", "WH19", "WH22",
                    "WH23", "WH18", "WH05", "WH02", "WH07", "WH14", "WH15", "WH10", "WH09", "WH21"]
CFG["pool_quay"] = ["SF15", "SF16", "SF13", "WH09", "WH19", "WH03", "WH11", "WH01", "ND03", "WH21", "WH12"]


def _spine_pieces():
    """ramp pieces between neighbouring terraces where each spine line crosses them; the middle spine is the stepped main street"""
    lanes = [k for k in LEVELS]; out = []
    for si, (a, b) in enumerate(SPINES):
        sp = LineString([a, b]); hits = []
        for k in lanes:
            L = LineString([st for st in CFG["streets"] if st["id"] == k][0]["pts"]); x = L.intersection(sp)
            if not x.is_empty: hits.append((k, tuple(np.round(L.interpolate(L.project(x if x.geom_type == "Point" else x.geoms[0])).coords[0], 1))))
        lines = {k: LineString([st for st in CFG["streets"] if st["id"] == k][0]["pts"]) for k, _ in hits}
        for j, ((k0, p0), (k1, p1)) in enumerate(zip(hits[:-1], hits[1:])):
            L1 = lines[k1]; v = L1.project(LineString([p1, p1]).centroid if False else __import__("shapely").geometry.Point(p1))
            cand = [tuple(np.round(L1.interpolate(min(max(v + d, 4), L1.length - 4)).coords[0], 1)) for d in ((0, 0) if si != 1 else (0, 0))]
            p1 = max(cand, key=lambda q: math.dist(q, p0))
            hits[j + 1] = (k1, p1)
            m = ((p0[0] + p1[0]) / 2, (p0[1] + p1[1]) / 2)
            name = "stepped main street, piece" if si == 1 else f"stair lane {si + 1}"
            out.append(ramp(f"S{si + 1}{k0[1:]}", [p0, m, p1], k0, k1, f"{name} ({k0[1:]} to {k1[1:]} m)", w=6.0 if si == 1 else 4.5, out_cls=None))
    return out


_SP = _spine_pieces()
STAIR_NOTES = ["%s: from (%.0f, %.0f) at %s m to (%.0f, %.0f) at %s m" % (d["name"].replace("stepped main street, piece", "stepped main street (stairs)"), d["pts"][0][0], d["pts"][0][1], d["pin_start"][1:],
               d["pts"][-1][0], d["pts"][-1][1], d["pin_end"][1:]) for d in _SP]
CFG["notes"].append("Stairs, not graded streets (a climb of 8 m between terraces 35 m apart is steeper than the 31 degree bank can grade; the hamlet is foot-only): " + "; ".join(STAIR_NOTES))
_t50 = LineString([st for st in CFG["streets"] if st["id"] == "T58"][0]["pts"])
_head = tuple(np.round(_t50.interpolate(_t50.project(LineString(SPINES[1]).intersection(_t50))).coords[0], 1)) if not LineString(SPINES[1]).intersection(_t50).is_empty else _t50.coords[-1]
CFG["notes"].append("The quay stair up the escarpment is not drawn as a street: at 25-100 %% it is steeper than the 31 degree bank, so it cannot be graded ground. "
                    "Build it as stair pieces from the quay lane (about 7400, 16364) to the lowest terrace (about %.0f, %.0f)." % tuple(float(v) for v in list(_head)[:2]))


def build(T):
    from gtown import standard_build
    rows = [("T74", T.cfg["pool_main"], "main", 0.0, 16.6)] + [(k, T.cfg["pool_lane"], "lane", 0.0, 16.6) for k in ("T66", "T82", "T58", "T90")] + \
           [("Q", T.cfg["pool_quay"], "quay", 0.3, 16.6)]
    standard_build(T, "T74", 30.0, 9.0, (7428, 16536), "up", ("SF03", "back"), ["WH09", "WH19", "WH03", "WH11", "ND03", "WH01", "SF15", "SF16"], rows,
                   comps=[("fish market or net stalls on the square (whole comp, your pick)", -9.0, 0.0, (9.5, 9.4))], open_side="south-west, toward the sea")
    T.comps.append(dict(name_or_role="quay: boat slips, fishing boats, net racks (whole comp, your pick)", x=round(float(QUAY.centroid.x), 1), y=round(float(QUAY.centroid.y), 1), yaw_deg=17.0, footprint_m=[34.0, 8.0], pad_z_m=QUAY_Z))
