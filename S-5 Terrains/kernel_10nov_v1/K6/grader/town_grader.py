#!/usr/bin/env python3
"""town_grader.py - the terrain grader for town layouts, as one stand-alone command.

It reproduces, on your own computer, the verdict our grading agent gives a town layout in the return schema:
which buildings our terrain grid can seat as drawn, which it refuses and why, and the check summary.

    python town_grader.py LAYOUT.json --grid5 TOWN_natural_5m.npy X0 Y0 [--fixed FIXED.json] [--out DIR]
    python town_grader.py LAYOUT.json --height HEIGHT_1m.npy X0 Y0 [--height OTHER_1m.npy X0 Y0] [--out DIR]

Needs Python 3.8+, numpy and matplotlib. Reads only the files named on the command line, writes only into --out
(default: grade_<layout name> next to the current directory). No network.

THE GRID (how the 5 m grid is taken from a 1 m height window)
  The map's terrain is a grid of points 5 m apart. Grid point (i, j) stands at map x = 5 i, y = 5 j.
  A 1 m window with south-west corner (X0, Y0) holds the height of map point (x, y) at H[y - Y0, x - X0].
  So the grid height of point (i, j) is exactly  H[5 j - Y0, 5 i - X0]  (every 5th value; no interpolation).
  A 5 m grid file (--grid5, corner X0 Y0 on multiples of 5) holds it directly: G[(5 j - Y0) / 5, (5 i - X0) / 5].
  The 5 m files are our natural ground exactly. The 1 m files are rounded to 1/64 m, and the six town windows are the
  ground as built (with our roads), so a 1 m window gave the same verdicts on all four of your returns but can move a
  cut / fill figure by 1 cm (up to 7 cm where one of our roads runs). Use the 5 m files for the exact numbers.
  The 1 m values between grid points are only a bilinear fill: the game never sees them.
  The grader works on the grid points from 20 cells (100 m) beyond the layout's buildings and street points:
  i from floor(min x / 5) - 20 to floor(max x / 5) + 20, the same for j with y.

THE RULES (in the order the grader applies them)
  1. Streets, in this order: every "main" and "lane" street in file order, then the square, then every "road" and "path".
     A street fixes every grid point of every 5 m cell whose centre lies within half-width + 3.54 m (half a cell diagonal)
     of its centre line. The level of each such point is the street's level (points_z, interpolated along the line)
     at the point's nearest station on the centre line. A point already fixed by an earlier street keeps the earlier
     level; if the two levels differ by more than 1 cm it is a street-street clash (counted, shown on the plan).
  2. The square is one level (level_z_m). It fixes every grid point of every cell its polygon touches. It must not meet
     a street point at another level, must stay within 4.0 m of the natural ground at every point, and must keep the
     31 degree bank (0.6 m per m) against every other fixed point. If it fails, its free points are still fixed.
  3. Buildings, in this order: role landmark, then square and quay, then main, then lane (then anything else);
     by id inside each role. Each building is refused at the first test it fails:
       a. overlap: its footprint box overlaps a building already seated;
       b. street ribbon: its footprint comes closer to a street centre line than half-width + 0.2 m (its own
          street, the one named in "street") or half-width + 1.0 m (any other street: this is the corner clearance);
       c. its pad (see below) meets a grid point already fixed at another level (more than 1 cm off): a street,
          ramp, lane, path, the square or another building's pad;
       d. cut / fill: any of its pad points is more than 4.0 m from the natural ground;
       e. bank: between any of its pad points and any other fixed point up to 6 grid cells (30 m) away in x or y,
          the level difference is more than 0.6 m per metre of distance (a 31 degree bank cannot join them).
          This is the back-to-back gap.
     A building that passes is seated: its pad points are fixed at its pad level.
  4. The pad of a building is its footprint box grown by 1.5 m on every side, except its rear, which grows 0.4 m.
     The rear is the box face that looks most nearly along the line from the nearest point of its own street's centre
     line to the footprint centre. The 0.4 m rear applies only to role main or lane with a street that exists in the
     file; every other building gets 1.5 m all round. Every grid point of every 5 m cell that pad touches (the pad is
     sampled every 0.25 m, corners included) is fixed at pad_z_m.
  5. After all buildings, the ground between fixed points is graded as 31 degree cones; a grid point where the cones
     from two fixed points cannot meet is "infeasible" (counted).

PERYS ONLY: at Perys our own harbour road (as built) and the quay apron (level 2.2 m) are fixed, and we grade in our
town's order: the town streets (M, U, U2, KW, KE), the square, the cross lanes, the quay, the harbour road.
perys_fixed.json holds exactly that; pass --fixed perys_fixed.json with every Perys layout. It is the only file that
changes the order. Without it your second Perys reads 38 of 98 instead of our 39 of 98.
"""
import argparse, collections, json, math, os, sys

import numpy as np

C = 5.0            # grid spacing, m
SLOPE = 0.60       # bank: rise per horizontal metre between fixed points (31 degrees)
CUTCAP = 4.0       # pad cut / fill limit, m
PADM = 1.5         # pad margin, m
REAR_DEFAULT = 0.4  # pad margin on the side facing away from the street (street-row houses)
MARGIN_CELLS = 20
PRI = {"landmark": 0, "square": 1, "quay": 1, "main": 2, "lane": 3}
CLS_ORDER = {"main": 0, "lane": 1, "road": 2, "path": 3}
SIDE2DOOR = {"front": "+z", "back": "-z", "right": "+x", "left": "-x"}
VERSION = "town_grader 1.0 (11 Nov 2026)"

# Model boxes (metres, in the model frame: x = right, z = front, relative to the model origin). The footprint is the
# box; the layout's x, y is the box centre. These are the exact numbers behind catalogue/buildings.json.
MODELS = {
    'IN01': dict(cls='land_3as_FOBBuilding2La', mn=(-7.955, -7.965), mx=(8.827, 7.974), door='right', twin='fob2l', enterable=True, tall=False),
    'IN02': dict(cls='land_3as_FOBBuilding2Lc', mn=(-7.955, -7.965), mx=(8.827, 7.974), door='right', twin='fob2l', enterable=True, tall=False),
    'IN03': dict(cls='land_3as_FOBBuilding2Lb', mn=(-7.955, -7.965), mx=(8.827, 7.974), door='right', twin='fob2l', enterable=True, tall=False),
    'ND01': dict(cls='land_3AS_Naboo_House_Small_1', mn=(-3.231, -3.231), mx=(3.392, 5.745), door='front', twin='naboo_small', enterable=False, tall=False),
    'ND02': dict(cls='land_3AS_Naboo_House_Small_2', mn=(-3.231, -3.231), mx=(3.392, 5.745), door='front', twin='naboo_small', enterable=False, tall=False),
    'ND03': dict(cls='land_3AS_Naboo_House_Small_Double', mn=(-6.396, -3.227), mx=(6.398, 5.295), door='front', twin='ndb', enterable=False, tall=False),
    'ND04': dict(cls='land_3AS_Naboo_House_Small_Corner', mn=(-5.638, -7.105), mx=(4.927, 5.564), door='back', twin='ncr', enterable=False, tall=False),
    'ND05': dict(cls='land_3AS_Naboo_House_Small_Square', mn=(-6.396, -6.166), mx=(6.398, 7.664), door='front', twin='nsq', enterable=False, tall=False),
    'ND06': dict(cls='land_3AS_Naboo_House_Small_Tower', mn=(-3.523, -3.523), mx=(3.523, 6.428), door='front', twin='ntw', enterable=False, tall=True),
    'ND07': dict(cls='land_3AS_Naboo_House_Small_Tower_2', mn=(-3.978, -3.978), mx=(3.978, 6.428), door='front', twin='ntw2', enterable=False, tall=True),
    'SF01': dict(cls='Land_OPTRE_mod_building_white', mn=(-6.714, -7.496), mx=(6.714, 8.98), door='back', twin='optre_mod', enterable=True, tall=False),
    'SF02': dict(cls='Land_JMS_build_Colony_DownShop1', mn=(-5.001, -7.752), mx=(5.001, 5.956), door='back', twin='jds', enterable=False, tall=True),
    'SF03': dict(cls='land_3AS_Imperial_Tower', mn=(-3.0, -3.505), mx=(3.0, 4.267), door='back', twin='imp', enterable=False, tall=False),
    'SF04': dict(cls='Land_Urban_Building_05', mn=(-7.727, -8.781), mx=(7.247, 8.781), door='back', twin='ub5', enterable=False, tall=True),
    'SF05': dict(cls='Land_JMS_build_Colony_block1', mn=(-7.348, -8.518), mx=(7.35, 8.212), door='back', twin='jb1', enterable=False, tall=True),
    'SF06': dict(cls='Land_JMS_build_Colony_blockCafe', mn=(-10.38, -6.497), mx=(10.4, 9.9), door='back', twin='jcf', enterable=True, tall=True),
    'SF07': dict(cls='Land_JMS_build_Colony_Towerblock2', mn=(-14.579, -14.577), mx=(14.576, 14.589), door='back', twin='jt2', enterable=False, tall=True),
    'SF08': dict(cls='Land_OPTRE_mod_building_civ', mn=(-6.714, -7.496), mx=(6.714, 8.98), door='back', twin='optre_mod', enterable=True, tall=False),
    'SF09': dict(cls='Land_Urban_Building_01', mn=(-6.515, -10.24), mx=(7.46, 9.731), door='back', twin='ub1', enterable=True, tall=False),
    'SF10': dict(cls='Land_JMS_build_Colony_block2', mn=(-9.96, -10.064), mx=(9.999, 12.407), door='back', twin='jb2', enterable=False, tall=True),
    'SF11': dict(cls='Land_JMS_build_Colony_DownBlock1', mn=(-10.004, -11.024), mx=(10.006, 10.499), door='back', twin='jdb', enterable=False, tall=True),
    'SF12': dict(cls='Land_JMS_build_Colony_House1', mn=(-7.433, -7.0), mx=(8.984, 8.001), door='back', twin='jms_house', enterable=False, tall=False),
    'SF13': dict(cls='Land_JMS_build_Colony_House2', mn=(-7.433, -7.0), mx=(8.983, 8.001), door='back', twin='jms_house', enterable=False, tall=False),
    'SF14': dict(cls='Land_JMS_build_Colony_Towerblock1', mn=(-14.579, -14.577), mx=(14.576, 14.589), door='back', twin='jt1', enterable=False, tall=True),
    'SF15': dict(cls='Land_OPTRE_mod_building_green', mn=(-6.714, -7.496), mx=(6.714, 8.98), door='back', twin='optre_mod', enterable=True, tall=False),
    'SF16': dict(cls='Land_OPTRE_mod_building_grey', mn=(-6.714, -7.496), mx=(6.714, 8.98), door='back', twin='optre_mod', enterable=True, tall=False),
    'SF17': dict(cls='Land_Urban_Building_02', mn=(-10.514, -11.773), mx=(9.159, 10.354), door='back', twin='ub2', enterable=True, tall=True),
    'SF18': dict(cls='Land_Urban_Building_04', mn=(-7.341, -10.992), mx=(10.133, 11.063), door='back', twin='ub4', enterable=False, tall=True),
    'WH01': dict(cls='Land_i_House_Small_01_b_white_F', mn=(-5.64, -6.157), mx=(5.218, 7.917), door='back', twin='alt_small01', enterable=True, tall=False),
    'WH02': dict(cls='Land_i_House_Big_01_b_whiteblue_F', mn=(-7.015, -8.142), mx=(7.017, 8.1), door='left', twin='alt_big01', enterable=True, tall=False),
    'WH03': dict(cls='Land_i_Stone_HouseSmall_V2_F', mn=(-10.197, -4.769), mx=(10.215, 4.302), door='back', twin='sts', enterable=True, tall=False),
    'WH04': dict(cls='Land_i_House_Small_03_V1_F', mn=(-6.153, -7.354), mx=(6.244, 7.14), door='back', twin='as3', enterable=True, tall=False),
    'WH05': dict(cls='Land_House_C_5_V1_EP1', mn=(-7.135, -6.231), mx=(6.515, 5.917), door='right', twin='tk_c5', enterable=True, tall=False),
    'WH06': dict(cls='Land_House_K_1_EP1', mn=(-6.308, -8.235), mx=(4.674, 3.525), door='back', twin='k1', enterable=True, tall=False),
    'WH07': dict(cls='Land_i_House_Big_01_V1_F', mn=(-7.015, -8.142), mx=(7.017, 8.1), door='left', twin='alt_big01', enterable=True, tall=False),
    'WH08': dict(cls='Land_i_House_Small_01_V1_F', mn=(-5.64, -6.157), mx=(5.218, 7.917), door='back', twin='alt_small01', enterable=True, tall=False),
    'WH09': dict(cls='Land_i_Shop_02_V1_F', mn=(-6.966, -4.753), mx=(8.943, 5.979), door='left', twin='sh2', enterable=True, tall=False),
    'WH10': dict(cls='Land_House_K_6_EP1', mn=(-7.462, -4.712), mx=(7.022, 6.056), door='left', twin='k6', enterable=True, tall=False),
    'WH11': dict(cls='Land_i_House_Small_02_V1_F', mn=(-7.699, -3.794), mx=(6.219, 3.847), door='left', twin='alt_small02', enterable=True, tall=False),
    'WH12': dict(cls='Land_i_Shop_01_V1_F', mn=(-4.688, -8.398), mx=(4.67, 6.957), door='back', twin='ash', enterable=True, tall=False),
    'WH13': dict(cls='Land_House_C_10_EP1', mn=(-5.714, -10.179), mx=(7.036, 10.196), door='back', twin='c10', enterable=False, tall=False),
    'WH14': dict(cls='Land_House_C_5_EP1', mn=(-7.135, -6.231), mx=(6.515, 5.917), door='right', twin='tk_c5', enterable=True, tall=False),
    'WH15': dict(cls='Land_House_C_5_V2_EP1', mn=(-7.135, -6.231), mx=(6.515, 5.917), door='right', twin='tk_c5', enterable=True, tall=False),
    'WH16': dict(cls='Land_House_C_9_EP1', mn=(-6.612, -6.936), mx=(6.453, 7.11), door='back', twin='c9', enterable=False, tall=False),
    'WH17': dict(cls='Land_House_K_2_basehide_EP1', mn=(-6.308, -8.235), mx=(4.674, 3.525), door='back', twin='WH17', enterable=True, tall=False),
    'WH18': dict(cls='Land_House_K_3_EP1', mn=(-8.056, -5.728), mx=(3.702, 7.257), door='back', twin='k3', enterable=True, tall=False),
    'WH19': dict(cls='Land_House_K_5_EP1', mn=(-7.978, -5.252), mx=(6.998, 4.256), door='back', twin='k5', enterable=True, tall=False),
    'WH20': dict(cls='Land_House_K_7_EP1', mn=(-5.962, -6.202), mx=(12.575, 4.282), door='back', twin='k7', enterable=False, tall=False),
    'WH21': dict(cls='Land_House_K_8_EP1', mn=(-5.415, -9.769), mx=(5.885, 8.554), door='front', twin='k8', enterable=True, tall=False),
    'WH22': dict(cls='Land_i_House_Big_02_b_brown_F', mn=(-5.458, -9.666), mx=(5.164, 6.54), door='front', twin='alt_big02', enterable=True, tall=False),
    'WH23': dict(cls='Land_i_House_Big_02_V1_F', mn=(-5.458, -9.666), mx=(5.164, 6.54), door='front', twin='alt_big02', enterable=True, tall=False),
    'WH24': dict(cls='Land_i_House_Small_02_b_pink_F', mn=(-7.699, -3.794), mx=(7.784, 3.847), door='back', twin='alt_small02', enterable=False, tall=False),
}

_tw = collections.defaultdict(list)
for _k, _v in MODELS.items():
    _tw[_v["twin"]].append(_k)
TWIN = {k: "+".join(sorted(_tw[v["twin"]])) for k, v in MODELS.items()}


# ---------------------------------------------------------------- geometry
def unit(v):
    v = np.asarray(v, float)
    return v / np.linalg.norm(v)


def axes(yaw):
    a = math.radians(yaw)
    return np.array([math.cos(a), -math.sin(a)]), np.array([math.sin(a), math.cos(a)])


def left(u):
    return np.array([-u[1], u[0]])


def sat_pen(A, B):
    """penetration depth of two convex polygons (> 0 = overlap; < 0 = minus the gap along the best separating axis)"""
    best = 1e9
    sep = 1e9
    for P in (A, B):
        for k in range(len(P)):
            e = P[(k + 1) % len(P)] - P[k]
            nrm = np.array([-e[1], e[0]]) / (np.linalg.norm(e) + 1e-12)
            a, b = A @ nrm, B @ nrm
            o = min(a.max(), b.max()) - max(a.min(), b.min())
            if o <= 0:
                sep = min(sep, o)
            best = min(best, o)
    return best if sep == 1e9 else sep


class Model:
    def __init__(self, mid, door_side=None):
        r = MODELS[mid]
        self.mid = mid
        self.mn = np.array([r["mn"][0], 0.0, r["mn"][1]])
        self.mx = np.array([r["mx"][0], 0.0, r["mx"][1]])
        self.door = SIDE2DOOR[door_side or r["door"]]


def origin_from_centre(m, cx, cy, yaw):
    ex, ez = axes(yaw)
    bx, bz = 0.5 * (m.mn[0] + m.mx[0]), 0.5 * (m.mn[2] + m.mx[2])
    return np.array([cx, cy]) - bx * ex - bz * ez


def footprint(m, O, yaw, grow=0.0):
    ex, ez = axes(yaw)
    x0, x1, z0, z1 = m.mn[0] - grow, m.mx[0] + grow, m.mn[2] - grow, m.mx[2] + grow
    return np.array([O + x * ex + z * ez for x, z in ((x0, z0), (x1, z0), (x1, z1), (x0, z1))])


def pad_poly(m, O, yaw, rear_n=None, rear_m=PADM, other=PADM):
    ex, ez = axes(yaw)
    g = {"+x": other, "-x": other, "+z": other, "-z": other}
    if rear_n is not None:
        cand = {"+x": ex @ rear_n, "-x": -(ex @ rear_n), "+z": ez @ rear_n, "-z": -(ez @ rear_n)}
        g[max(cand, key=cand.get)] = rear_m
    x0, x1, z0, z1 = m.mn[0] - g["-x"], m.mx[0] + g["+x"], m.mn[2] - g["-z"], m.mx[2] + g["+z"]
    return np.array([O + x * ex + z * ez for x, z in ((x0, z0), (x1, z0), (x1, z1), (x0, z1))])


def door_point(m, O, yaw):
    """the middle of the door face, and the outward direction"""
    ex, ez = axes(yaw)
    dvec = {"-z": -ez, "+z": ez, "+x": ex, "-x": -ex}[m.door]
    face = {"-z": m.mn[2], "+z": m.mx[2], "+x": m.mx[0], "-x": m.mn[0]}[m.door]
    lat = {"-z": (m.mn[0] + m.mx[0]) / 2, "+z": (m.mn[0] + m.mx[0]) / 2, "+x": (m.mn[2] + m.mx[2]) / 2, "-x": (m.mn[2] + m.mx[2]) / 2}[m.door]
    dc = O + abs(face) * dvec + lat * (ez if m.door in ("+x", "-x") else ex)
    return dc, dvec


def raster_polys(polys, box, res=0.5):
    x0, y0, x1, y1 = box
    nx, ny = int((x1 - x0) / res), int((y1 - y0) / res)
    Mk = np.zeros((ny, nx), bool)
    for P in polys:
        P = np.asarray(P, float)
        a0, b0 = np.floor((P.min(0) - [x0, y0]) / res).astype(int)
        a1, b1 = np.ceil((P.max(0) - [x0, y0]) / res).astype(int)
        a0, b0 = max(a0, 0), max(b0, 0)
        a1, b1 = min(a1, nx), min(b1, ny)
        if a1 <= a0 or b1 <= b0:
            continue
        X, Y = np.meshgrid(x0 + (np.arange(a0, a1) + 0.5) * res, y0 + (np.arange(b0, b1) + 0.5) * res)
        area = sum(P[k, 0] * P[(k + 1) % len(P), 1] - P[(k + 1) % len(P), 0] * P[k, 1] for k in range(len(P)))
        sg = 1.0 if area > 0 else -1.0
        inside = np.ones(X.shape, bool)
        for k in range(len(P)):
            a, b = P[k], P[(k + 1) % len(P)]
            inside &= sg * ((b[0] - a[0]) * (Y - a[1]) - (b[1] - a[1]) * (X - a[0])) >= 0
        Mk[b0:b1, a0:a1] |= inside
    return Mk


# ---------------------------------------------------------------- the grid
def fill_missing(nat):
    """grid points outside every height window are filled from their nearest known neighbours (for the drawing and
    the bank scan only; a pad that needs them is refused and a street that needs them is reported)"""
    out = nat.copy()
    if not np.isnan(out).any():
        return out
    if np.isnan(out).all():
        raise SystemExit("none of the grader's grid points is inside the height window(s): check the X0 Y0 you gave")
    for _ in range(sum(out.shape)):
        m = np.isnan(out)
        if not m.any():
            break
        acc = np.zeros(out.shape)
        cnt = np.zeros(out.shape)
        for dj, di in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            sh = np.full(out.shape, np.nan)
            src = out[max(0, -dj):out.shape[0] - max(0, dj), max(0, -di):out.shape[1] - max(0, di)]
            sh[max(0, dj):out.shape[0] - max(0, -dj), max(0, di):out.shape[1] - max(0, -di)] = src
            ok = ~np.isnan(sh)
            acc[ok] += sh[ok]
            cnt[ok] += 1
        take = m & (cnt > 0)
        out[take] = acc[take] / cnt[take]
    return out


class Grid:
    def __init__(self, i0, i1, j0, j1, windows):
        self.I0, self.I1, self.J0, self.J1 = i0, i1, j0, j1
        ny, nx = j1 - j0, i1 - i0
        nat = np.full((ny, nx), np.nan)
        for H, X0, Y0, step in windows:          # step 1: a 1 m window (every 5th value); step 5: a 5 m grid file
            rows = (5 * np.arange(j0, j1) - Y0) // step
            cols = (5 * np.arange(i0, i1) - X0) // step
            okr = (rows >= 0) & (rows < H.shape[0])
            okc = (cols >= 0) & (cols < H.shape[1])
            sub = np.full((ny, nx), np.nan)
            if okr.any() and okc.any():
                sub[np.ix_(okr, okc)] = np.asarray(H, np.float64)[np.ix_(rows[okr], cols[okc])]
            take = np.isnan(nat) & ~np.isnan(sub)
            nat[take] = sub[take]
        self.missing = np.isnan(nat)
        self.nat = fill_missing(nat)
        self.fix = np.full((ny, nx), np.nan)
        self.owner = np.full((ny, nx), "", object)
        self.kind = np.full((ny, nx), "", object)
        self.slope = np.full((ny, nx), SLOPE)
        self.X = (i0 + np.arange(nx))[None, :] * C + np.zeros((ny, 1))
        self.Y = (j0 + np.arange(ny))[:, None] * C + np.zeros((1, nx))
        self.H = None
        self.last_bank = None
        self.last_bad = []

    def cells_of_poly(self, P):
        """grid point indices (j, i) of every 5 m cell the convex polygon touches (0.25 m sampling + its corners)"""
        P = np.asarray(P, float)
        x0, y0 = P.min(0)
        x1, y1 = P.max(0)
        xs = np.arange(x0, x1 + 0.25, 0.25)
        ys = np.arange(y0, y1 + 0.25, 0.25)
        X, Y = np.meshgrid(xs, ys)
        pts = np.c_[X.ravel(), Y.ravel()]
        m = np.ones(len(pts), bool)
        area = 0.0
        for k in range(len(P)):
            a, b = P[k], P[(k + 1) % len(P)]
            area += a[0] * b[1] - a[1] * b[0]
        s = 1.0 if area > 0 else -1.0
        for k in range(len(P)):
            a, b = P[k], P[(k + 1) % len(P)]
            m &= s * ((b[0] - a[0]) * (pts[:, 1] - a[1]) - (b[1] - a[1]) * (pts[:, 0] - a[0])) >= -1e-9
        pts = np.vstack([pts[m], P])
        ci = np.floor(pts[:, 0] / C).astype(int) - self.I0
        cj = np.floor(pts[:, 1] / C).astype(int) - self.J0
        out = set()
        for j, i in set(zip(cj.tolist(), ci.tolist())):
            out |= {(j, i), (j, i + 1), (j + 1, i), (j + 1, i + 1)}
        return sorted(out)

    def clash_points(self, V, z, tol=0.01):
        J = np.array([v[0] for v in V])
        I = np.array([v[1] for v in V])
        ny, nx = self.fix.shape
        ok = (J >= 0) & (I >= 0) & (J < ny) & (I < nx)
        J, I = J[ok], I[ok]
        cur = self.fix[J, I]
        bad = ~np.isnan(cur) & (np.abs(cur - z) > tol)
        return [(int(j), int(i), float(c), self.owner[j, i]) for j, i, c in zip(J[bad], I[bad], cur[bad])]

    def feasible(self, V, z, tol=0.01, cutcap=CUTCAP, slope=SLOPE):
        J = np.array([v[0] for v in V])
        I = np.array([v[1] for v in V])
        z = np.broadcast_to(np.asarray(z, float), J.shape).astype(float)
        ny, nx = self.nat.shape
        self.last_bank = None
        if J.min() < 2 or I.min() < 2 or J.max() >= ny - 2 or I.max() >= nx - 2:
            return False, "leaves the window"
        cur = self.fix[J, I]
        bad = ~np.isnan(cur) & (np.abs(cur - z) > tol)
        if bad.any():
            return False, "vertex owned by %s at another level" % self.owner[J[bad][0], I[bad][0]]
        if self.missing[J, I].any():
            return False, "outside the height window(s) given"
        cf = float(np.abs(z - self.nat[J, I]).max())
        if cf > cutcap + 1e-6:
            return False, "cut/fill %.2f > %.1f" % (cf, cutcap)
        F = ~np.isnan(self.fix)
        F[J, I] = False
        F[:max(0, J.min() - 6)] = False      # pairs more than 6 cells apart cannot bind
        F[J.max() + 7:] = False
        F[:, :max(0, I.min() - 6)] = False
        F[:, I.max() + 7:] = False
        fj, fi = np.nonzero(F)
        if len(fj):
            fz = self.fix[fj, fi]
            d = np.hypot((fj[:, None] - J[None, :]) * C, (fi[:, None] - I[None, :]) * C)
            dz = np.abs(fz[:, None] - z[None, :])
            sl = np.maximum(self.slope[fj, fi][:, None], slope)
            viol = dz > sl * d + 1e-6
            if viol.any():
                k = np.argwhere(viol)[0]
                self.last_bank = ((int(fj[k[0]]), int(fi[k[0]])), (int(J[k[1]]), int(I[k[1]])), float(dz[k[0], k[1]]), float(d[k[0], k[1]]))
                return False, "bank too steep vs %s (dz %.2f over %.1f m)" % (self.owner[fj[k[0]], fi[k[0]]], dz[k[0], k[1]], d[k[0], k[1]])
        return True, "cut/fill %.2f" % cf

    def commit(self, V, z, who, kind=""):
        if not len(V):
            return
        J = np.array([v[0] for v in V])
        I = np.array([v[1] for v in V])
        self.fix[J, I] = z
        for j, i in zip(J, I):
            if not self.owner[j, i]:
                self.owner[j, i] = who
                self.kind[j, i] = kind

    def solve(self):
        F = ~np.isnan(self.fix)
        fj, fi = np.nonzero(F)
        fz = self.fix[fj, fi]
        fs = self.slope[fj, fi]
        ny, nx = self.nat.shape
        jj0 = np.arange(ny)[:, None, None]
        ii0 = np.arange(nx)[None, :, None]
        lo = np.full((ny, nx), -1e9)
        hi = np.full((ny, nx), 1e9)
        for c0 in range(0, len(fj), 300):
            jj, ii, zz, ss = fj[c0:c0 + 300], fi[c0:c0 + 300], fz[c0:c0 + 300], fs[c0:c0 + 300]
            d = np.hypot((jj0 - jj[None, None, :]) * C, (ii0 - ii[None, None, :]) * C)
            lo = np.maximum(lo, (zz[None, None, :] - ss[None, None, :] * d).max(-1))
            hi = np.minimum(hi, (zz[None, None, :] + ss[None, None, :] * d).min(-1))
        bad = lo > hi + 1e-6
        self.infeasible = int(bad.sum())
        self.infeasible_where = [(int(j), int(i)) for j, i in np.argwhere(bad)]
        H = np.clip(self.nat, lo, hi)
        H[F] = self.fix[F]
        edge = np.zeros(H.shape, bool)
        edge[[0, -1], :] = True
        edge[:, [0, -1]] = True
        H[edge] = self.nat[edge]
        self.H = H
        return H

    def xy(self, j, i):
        return (self.I0 + i) * C, (self.J0 + j) * C

    def box(self):
        return (self.I0 * C, self.J0 * C, (self.I1 - 1) * C, (self.J1 - 1) * C)


def bil(G, h, x, y):
    fx = np.asarray(x, float) / C - G.I0
    fy = np.asarray(y, float) / C - G.J0
    i = np.clip(np.floor(fx).astype(int), 0, h.shape[1] - 2)
    j = np.clip(np.floor(fy).astype(int), 0, h.shape[0] - 2)
    u, v = fx - i, fy - j
    return h[j, i] * (1 - u) * (1 - v) + h[j, i + 1] * u * (1 - v) + h[j + 1, i] * (1 - u) * v + h[j + 1, i + 1] * u * v


def tri_z(G, h, x, y):
    """the cell surface under both possible triangulations of the 5 m cell -> (z_a, z_b)"""
    fx = np.asarray(x, float) / C - G.I0
    fy = np.asarray(y, float) / C - G.J0
    i = np.clip(np.floor(fx).astype(int), 0, h.shape[1] - 2)
    j = np.clip(np.floor(fy).astype(int), 0, h.shape[0] - 2)
    u, v = fx - i, fy - j
    a, b, c, d = h[j, i], h[j, i + 1], h[j + 1, i], h[j + 1, i + 1]
    za = np.where(u >= v, a + (b - a) * u + (d - b) * v, a + (c - a) * v + (d - c) * u)
    zb = np.where(u + v <= 1, a + (b - a) * u + (c - a) * v, d + (c - d) * (1 - u) + (b - d) * (1 - v))
    return za, zb


# ---------------------------------------------------------------- streets
class Street:
    def __init__(self, sid, title, pts, width, cls, zpts):
        self.name, self.title, self.width, self.cls = sid, title, float(width), cls
        P = np.asarray(pts, float)
        D = [P[0]]
        Z = [zpts[0]]
        for k, (a, b) in enumerate(zip(P[:-1], P[1:])):
            n = max(1, int(math.ceil(np.linalg.norm(b - a) / 1.0)))
            for t in np.linspace(0, 1, n + 1)[1:]:
                D.append(a + (b - a) * t)
                Z.append(zpts[k] + (zpts[k + 1] - zpts[k]) * t)
        self.P = np.array(D)
        self.s = np.r_[0, np.cumsum(np.hypot(*np.diff(self.P, axis=0).T))]
        self.L = float(self.s[-1])
        self.z = np.array(Z)
        xs = np.arange(0, self.L, 0.5)
        self.samples = np.c_[np.interp(xs, self.s, self.P[:, 0]), np.interp(xs, self.s, self.P[:, 1])]
        self.clash = 0
        self.clash_where = []
        self.vertices = 0
        self.cutfill = 0.0
        self.no_height = 0

    def zs(self, s):
        return float(np.interp(s, self.s, self.z))

    def xy(self, s):
        return np.array([np.interp(s, self.s, self.P[:, 0]), np.interp(s, self.s, self.P[:, 1])])

    def grade_at(self, s, half=2.5):
        a, b = max(0.0, s - half), min(self.L, s + half)
        return abs(self.zs(b) - self.zs(a)) / max(b - a, 1e-6)

    def project(self, X, Y):
        A, B = self.P[:-1], self.P[1:]
        AB = B - A
        L2 = (AB ** 2).sum(1)
        pts = np.c_[np.ravel(X), np.ravel(Y)]
        out_s, out_d = np.empty(len(pts)), np.empty(len(pts))
        for c0 in range(0, len(pts), 2000):
            p = pts[c0:c0 + 2000]
            t = np.clip(((p[:, None, :] - A[None]) * AB[None]).sum(-1) / L2[None], 0, 1)
            Q = A[None] + t[..., None] * AB[None]
            d = np.hypot(p[:, None, 0] - Q[..., 0], p[:, None, 1] - Q[..., 1])
            k = d.argmin(1)
            r = np.arange(len(p))
            out_s[c0:c0 + 2000] = self.s[:-1][k] + t[r, k] * np.sqrt(L2[k])
            out_d[c0:c0 + 2000] = d[r, k]
        return out_s, out_d


def street_from_json(s):
    if s.get("points_z") is None:
        raise SystemExit("street %s has no points_z: the grader needs the street level at every point" % s.get("id"))
    P = np.asarray([p[:2] for p in s["points"]], float)
    Z = np.asarray(s["points_z"], float)
    if len(Z) != len(P):
        raise SystemExit("street %s: %d points but %d points_z" % (s.get("id"), len(P), len(Z)))
    keep = np.r_[True, np.hypot(*np.diff(P, axis=0).T) > 1e-6]      # a point repeated at a segment join is dropped
    return Street(s["id"], s.get("name", s["id"]), P[keep], s["width_m"], s.get("class", "lane"), Z[keep])


def road_vertices(G, st, half):
    """grid points of every 5 m cell whose centre is within half + 3.54 m of the centre line, each at the street level
    of its own nearest station on the centre line"""
    cx = (G.X[:-1, :-1] + C / 2).ravel()
    cy = (G.Y[:-1, :-1] + C / 2).ravel()
    box = (cx > st.P[:, 0].min() - half - 10) & (cx < st.P[:, 0].max() + half + 10) & (cy > st.P[:, 1].min() - half - 10) & (cy < st.P[:, 1].max() + half + 10)
    idx = np.nonzero(box)[0]
    if not len(idx):
        return [], np.zeros(0), np.zeros(0)
    s, d = st.project(cx[idx], cy[idx])
    nx = G.X.shape[1] - 1
    V = set()
    for k in idx[d <= half + C * math.sqrt(2) / 2 + 1e-6]:
        j, i = divmod(int(k), nx)
        V |= {(j, i), (j, i + 1), (j + 1, i), (j + 1, i + 1)}
    V = sorted(V)
    if not V:
        return V, np.zeros(0), np.zeros(0)
    J = np.array([v[0] for v in V])
    I = np.array([v[1] for v in V])
    sv, _ = st.project(G.X[J, I], G.Y[J, I])
    return V, np.array([st.zs(x) for x in sv]), sv


def seg_poly_dist(st, fp):
    """min distance from the street centre line (0.5 m samples) to the polygon (0 if a sample is inside it)"""
    pts = st.samples
    box = (pts[:, 0] > fp[:, 0].min() - 30) & (pts[:, 0] < fp[:, 0].max() + 30) & (pts[:, 1] > fp[:, 1].min() - 30) & (pts[:, 1] < fp[:, 1].max() + 30)
    pts = pts[box]
    if not len(pts):
        return 1e9
    best = 1e9
    n = len(fp)
    ins = np.ones(len(pts), bool)
    area = sum(fp[k, 0] * fp[(k + 1) % n, 1] - fp[(k + 1) % n, 0] * fp[k, 1] for k in range(n))
    sg = 1.0 if area > 0 else -1.0
    for k in range(n):
        a, b = fp[k], fp[(k + 1) % n]
        ab = b - a
        t = np.clip(((pts - a) @ ab) / (ab @ ab), 0, 1)
        d = np.hypot(*(pts - (a + t[:, None] * ab)).T)
        best = min(best, float(d.min()))
        ins &= sg * (ab[0] * (pts[:, 1] - a[1]) - ab[1] * (pts[:, 0] - a[0])) >= 0
    return 0.0 if ins.any() else best


def straight_runs(st, tol=1.0):
    """the longest stretch of the centre line that stays within tol m of its own chord"""
    P, s = st.P, st.s
    best = (0.0, 0.0, 0.0)
    j = 0
    for i in range(0, len(P) - 1, 2):
        j = min(max(j, i + 1), len(P) - 1)
        while j + 1 < len(P):
            A, B = P[i], P[j + 1]
            d = unit(B - A)
            Q = P[i:j + 2] - A
            dev = np.abs(Q[:, 0] * d[1] - Q[:, 1] * d[0]).max()
            if dev > tol:
                break
            j += 1
        L = s[j] - s[i]
        if L > best[0]:
            best = (float(L), float(s[i]), float(s[j]))
    return dict(longest_m=round(best[0], 1), from_s=round(best[1], 1), to_s=round(best[2], 1))


# ---------------------------------------------------------------- the grading run
class Town:
    pass


def add_street(T, st):
    G = T.G
    V, z, sv = road_vertices(G, st, st.width / 2)
    st.V_all = V
    if not V:
        T.streets.append(st)
        return st
    J = np.array([v[0] for v in V])
    I = np.array([v[1] for v in V])
    cur = G.fix[J, I]
    keep = np.isnan(cur)
    clash = (~keep) & (np.abs(cur - z) > 0.01)
    st.clash = int(clash.sum())
    st.clash_where = [(int(j), int(i), float(z_), float(c_), G.owner[j, i]) for j, i, z_, c_, k in zip(J, I, z, cur, clash) if k]
    Vk = [v for v, k in zip(V, keep) if k]
    G.commit(Vk, z[keep], st.name, "street:" + st.cls)
    for (j, i), s_ in zip(V, sv):
        T.st_station.setdefault((j, i), (st.name, float(s_)))
    st.vertices = len(Vk)
    st.no_height = int(G.missing[J, I].sum())
    st.cutfill = float(np.abs(z - G.nat[J, I]).max())
    T.streets.append(st)
    return st


def add_level_pad(T, key, poly, z, who, kind):
    """a level patch (the square, or a fixed pad from --fixed): feasible -> fix all its points; else fix its free points"""
    G = T.G
    V = G.cells_of_poly(poly)
    J = np.array([v[0] for v in V])
    I = np.array([v[1] for v in V])
    free = np.isnan(G.fix[J, I])
    clash = G.clash_points(V, z)
    ok, why = G.feasible(V, z)
    cf = float(np.abs(z - G.nat[J, I]).max())
    T.pads[key] = dict(who=who, level=z, vertices=len(V), ok=ok, why=why, cutfill_max=round(cf, 2), clash_points=len(clash),
                       clash_owners=dict(collections.Counter(c[3] for c in clash)), bank=G.last_bank)
    T.pad_clash[key] = clash
    G.commit(V if ok else [v for v, f in zip(V, free) if f], z, who, kind)
    return ok, why, cf


def bobj(T, b, rear):
    mid = b["model_id"]
    if mid not in MODELS:
        raise SystemExit("building %s: model_id %s is not in the catalogue" % (b.get("id"), mid))
    if b.get("pad_z_m") is None:
        raise SystemExit("building %s has no pad_z_m: the grader needs the pad level of every building" % b.get("id"))
    m = Model(mid, b.get("door_side"))
    O = origin_from_centre(m, b["x"], b["y"], b["yaw_deg"])
    fp = footprint(m, O, b["yaw_deg"])
    rear_n, rear_m = None, PADM
    SN = T.SN
    if b.get("street") in SN and b.get("role") in ("main", "lane"):
        st = SN[b["street"]]
        c = fp.mean(0)
        s_, _ = st.project(np.array([c[0]]), np.array([c[1]]))
        rear_n, rear_m = unit(c - st.xy(s_[0])), rear
    padp = pad_poly(m, O, b["yaw_deg"], rear_n, rear_m)
    return dict(kid=b["id"], mid=mid, m=m, O=O, yaw=float(b["yaw_deg"]), fp=fp, c=fp.mean(0), padp=padp, V=T.G.cells_of_poly(padp),
                pad=float(b["pad_z_m"]), group=b.get("pad_group", b["id"]), street=b.get("street"), role=b.get("role", ""),
                garrison=bool(b.get("garrison", False)), rear_m=rear_m)


def cause_of(T, w):
    """our grading agent's cause categories (kept word for word, so the counts compare)"""
    if w == "ok":
        return "ok"
    if w.startswith("street ribbon"):
        return "footprint inside a street ribbon (own street needs half + 0.2 m, others half + 1.0 m)"
    if w.startswith("vertex owned by"):
        o = w.split("owned by ")[1].split(" at")[0]
        if o in T.SN:
            return "pad shares 5 m vertices with street ramps or lanes at another level (ramp / lane cells)"
        if o == "SQUARE":
            return "pad shares vertices with the square at another level"
        if o in T.fixed_pads:
            return "pad shares vertices with a fixed pad at another level"
        return "pad shares 5 m vertices with another pad at another level"
    if w.startswith("bank too steep"):
        return "pad within the 31 deg bank of another level (needs more than 0.6 m per m)"
    if w.startswith("cut/fill"):
        return "pad cut / fill over 4.0 m on our grid"
    if w.startswith("overlap"):
        return "footprint overlap"
    return w.split(" (")[0]


def kind_of_check(T, o, w):
    """the clash family, for the per-check table: pad-pad, pad-street, pad-ramp, pad-lane, pad-path, pad-square, ..."""
    if w.startswith("vertex owned by"):
        own = w.split("owned by ")[1].split(" at")[0]
        if own in T.SN:
            st = T.SN[own]
            pts = [c for c in o["clash"] if c[3] == own] or o["clash"]
            ramp = False
            for j, i, z_, _ in pts:
                nm, s_ = T.st_station.get((j, i), (own, None))
                if s_ is not None and nm == own and st.grade_at(s_) > 0.01:
                    ramp = True
            fam = {"main": "street", "lane": "lane", "road": "road", "path": "path"}.get(st.cls, st.cls)
            if own == o["street"]:
                return "pad-own-street-ramp" if ramp else "pad-own-street"
            return "pad-%s-ramp" % fam if ramp else "pad-%s" % fam
        if own == "SQUARE":
            return "pad-square"
        if own in T.fixed_pads:
            return "pad-fixed-pad"
        return "pad-pad"
    if w.startswith("street ribbon"):
        nm = w.split("street ribbon ")[1].split(" (")[0]
        return "ribbon-own-street" if nm == o["street"] else "ribbon-other-street (corner clearance)"
    if w.startswith("bank too steep"):
        own = w.split(" vs ")[1].split(" (")[0]
        return "bank-to-street" if own in T.SN else ("bank-to-square" if own == "SQUARE" else "bank-to-pad (back-to-back gap)")
    if w.startswith("cut/fill"):
        return "cut-fill"
    if w.startswith("overlap"):
        return "overlap"
    return "other"


def plain_reason(T, o, w):
    if w == "ok":
        return "seated"
    if w.startswith("overlap"):
        return "its footprint overlaps %s, which was seated first" % w.split()[1]
    if w.startswith("street ribbon"):
        nm = w.split("street ribbon ")[1].split(" (")[0]
        d, lim = [float(x) for x in w.split("(")[1].rstrip(")").split(" < ")]
        if nm == o["street"]:
            return "too close to its own street %s: %.2f m from the centre line, needs %.2f m (half-width + 0.2 m); move it %.2f m out" % (nm, d, lim, lim - d)
        return "too close to street %s (corner clearance): %.2f m from its centre line, needs %.2f m (half-width + 1.0 m); %.2f m short" % (nm, d, lim, lim - d)
    if w.startswith("vertex owned by"):
        own = w.split("owned by ")[1].split(" at")[0]
        pts = o["clash"]
        lv = sorted({round(c[2], 2) for c in pts})
        lvs = "%.2f m" % lv[0] if len(lv) == 1 else "%.2f-%.2f m" % (lv[0], lv[-1])
        k = kind_of_check(T, o, w)
        what = {"pad-pad": "another building's pad", "pad-square": "the square", "pad-fixed-pad": "a fixed pad"}.get(k, "street %s" % own)
        if own in T.SN:
            what = "the cells of street %s (%s%s)" % (own, T.SN[own].cls, ", a ramp there" if k.endswith("ramp") else ", level there")
        elif k == "pad-pad":
            what = "the pad of %s" % own
        return "its pad meets %s at %s on %d grid point(s); its pad is %.2f m" % (what, lvs, len(pts), o["pad"])
    if w.startswith("bank too steep"):
        own = w.split(" vs ")[1].split(" (")[0]
        dz, d = w.split("dz ")[1].rstrip(")").split(" over ")
        return "too close in height to %s: %s m of level difference over %s, more than a 31 degree bank (0.6 m per m) allows" % (own, dz, d)
    if w.startswith("cut/fill"):
        return "its pad needs %s m of cut or fill on the 5 m grid (limit 4.0 m)" % w.split()[1]
    if w.startswith("leaves the window"):
        return "its pad reaches the edge of the graded window"
    if w.startswith("outside the height"):
        return "its pad lies outside the height window(s) you gave"
    return w


def grade(LAY, windows, fixed=None, rear=REAR_DEFAULT):
    fixed = fixed or {}
    T = Town()
    T.lay = LAY
    T.streets, T.st_station, T.pads, T.pad_clash = [], {}, {}, {}
    over = {s["id"]: s for s in fixed.get("streets", [])}
    raw_streets = [over.get(s["id"], s) for s in LAY["streets"]] + [s for s in fixed.get("streets", []) if s["id"] not in {x["id"] for x in LAY["streets"]}]
    T.fixed_pads = {p["id"]: p for p in fixed.get("pads", [])}
    xs = [b["x"] for b in LAY["buildings"]] + [p[0] for s in LAY["streets"] for p in s["points"]]
    ys = [b["y"] for b in LAY["buildings"]] + [p[1] for s in LAY["streets"] for p in s["points"]]
    if "window" in fixed:
        i0, i1, j0, j1 = fixed["window"]
    else:
        i0, i1 = int(min(xs) // 5) - MARGIN_CELLS, int(max(xs) // 5) + MARGIN_CELLS + 1
        j0, j1 = int(min(ys) // 5) - MARGIN_CELLS, int(max(ys) // 5) + MARGIN_CELLS + 1
    G = T.G = Grid(i0, i1, j0, j1, windows)
    order = fixed.get("order")
    sts = [street_from_json(s) for s in raw_streets]
    byid = {s.name: s for s in sts}
    sq = LAY.get("square") or {}
    has_sq = bool(sq.get("polygon")) and sq.get("level_z_m") is not None
    if has_sq and not isinstance(sq["level_z_m"], (int, float)):
        raise SystemExit("the square's level_z_m must be one number: a square is one level (a step inside it becomes a bank on the 5 m grid)")
    T.sq = np.array(sq["polygon"], float) if has_sq else None
    T.sqz = float(sq["level_z_m"]) if has_sq else None
    if order is None:        # the default order: main and lane streets in file order, the square, roads and paths, then fixed pads
        first = [s for s in sorted(sts, key=lambda s: CLS_ORDER.get(s.cls, 4)) if s.cls in ("main", "lane")]
        rest = [s for s in sorted(sts, key=lambda s: CLS_ORDER.get(s.cls, 4)) if s.cls not in ("main", "lane")]
        steps = [("street", s.name) for s in first] + [("square", None)] + [("street", s.name) for s in rest] + [("pad", k) for k in T.fixed_pads]
    else:                    # an order from --fixed; streets it does not name go in by the default rule around the square
        named = {x[1] for x in order if x[0] == "street"}
        steps = []
        for kind, key in (tuple(x) for x in order):
            if kind == "street" and key not in byid:
                continue
            if kind == "pad" and key not in T.fixed_pads:
                continue
            if kind == "square":
                steps += [("street", s.name) for s in sorted(sts, key=lambda s: CLS_ORDER.get(s.cls, 4)) if s.cls in ("main", "lane") and s.name not in named]
                steps.append(("square", None))
                steps += [("street", s.name) for s in sorted(sts, key=lambda s: CLS_ORDER.get(s.cls, 4)) if s.cls not in ("main", "lane") and s.name not in named]
            else:
                steps.append((kind, key))
        if ("square", None) not in steps:
            steps += [("street", s.name) for s in sts if s.name not in named]
    for kind, key in steps:
        if kind == "street":
            add_street(T, byid[key])
        elif kind == "square" and has_sq:
            add_level_pad(T, "square", T.sq, T.sqz, "SQUARE", "square")
        elif kind == "pad":
            p = T.fixed_pads[key]
            add_level_pad(T, key, np.array(p["polygon"], float), float(p["level_z_m"]), key, "fixed pad")
    T.SN = {s.name: s for s in T.streets}
    objs = [bobj(T, b, rear) for b in LAY["buildings"]]
    # order-independent measures (before any building is seated)
    own = collections.defaultdict(set)
    for o in objs:
        for v in o["V"]:
            own[v].add((o["group"], o["pad"]))
    pairs, shared = set(), 0
    for v, s in own.items():
        if len({z for g, z in s}) > 1:
            shared += 1
            gs = sorted(s)
            for a in range(len(gs)):
                for b_ in range(a + 1, len(gs)):
                    if abs(gs[a][1] - gs[b_][1]) > 0.01:
                        pairs.add((gs[a][0], gs[b_][0]))
    pad_vs_street = bld_vs_street = 0
    for o in objs:
        Jo = np.array([v[0] for v in o["V"]])
        Io = np.array([v[1] for v in o["V"]])
        ok_ = (Jo >= 0) & (Io >= 0) & (Jo < G.fix.shape[0]) & (Io < G.fix.shape[1])
        cur = G.fix[Jo[ok_], Io[ok_]]
        bad = ~np.isnan(cur) & (np.abs(cur - o["pad"]) > 0.01)
        pad_vs_street += int(bad.sum())
        bld_vs_street += int(bad.any())
        o["cf"] = float(np.abs(o["pad"] - G.nat[Jo[ok_], Io[ok_]]).max())
        o["pre_clash"] = int(bad.sum())
    cfs = np.array([o["cf"] for o in objs])
    # the buildings, one at a time, in our order
    objs.sort(key=lambda o: (PRI.get(o["role"], 3), o["kid"]))
    res = collections.OrderedDict()
    acc = []
    for o in objs:
        why = None
        o["clash"] = G.clash_points(o["V"], o["pad"])
        o["bank"] = None
        o["ribbon"] = []
        for st in T.streets:
            lim = st.width / 2 + (0.2 if st.name == o["street"] else 1.0)
            d = seg_poly_dist(st, o["fp"])
            if d < lim:
                o["ribbon"].append((st.name, round(d, 2), round(lim, 2)))
        for x in acc:
            if abs(x["c"][0] - o["c"][0]) < 45 and abs(x["c"][1] - o["c"][1]) < 45 and sat_pen(o["fp"], x["fp"]) > 0:
                why = "overlap " + x["kid"]
                break
        if why is None:
            for st in T.streets:
                lim = st.width / 2 + (0.2 if st.name == o["street"] else 1.0)
                d = seg_poly_dist(st, o["fp"])
                if d < lim:
                    why = "street ribbon %s (%.2f < %.2f)" % (st.name, d, lim)
                    break
        if why is None:
            ok, w2 = G.feasible(o["V"], o["pad"])
            why = None if ok else w2
            o["bank"] = G.last_bank
        if why is None:
            G.commit(o["V"], o["pad"], o["kid"], "pad")
            acc.append(o)
            res[o["kid"]] = "ok"
        else:
            res[o["kid"]] = why
        o["why"] = res[o["kid"]]
    T.objs, T.acc, T.res = objs, acc, res
    G.solve()
    T.counts = dict(
        town=LAY.get("town"), version=LAY.get("version"), buildings=len(objs),
        pad_rule="v5: footprint + 1.5 m street side / ends, + %.1f m rear (front rows); 1.5 m all round otherwise" % rear,
        window_vertices=dict(i0=i0, i1=i1, j0=j0, j1=j1),
        grid_clash=dict(pad_group_pairs_sharing_a_vertex_at_different_levels=len(pairs), shared_vertices=shared, pairs=sorted(pairs)[:60],
                        buildings_whose_pad_meets_street_cells_at_another_level=bld_vs_street, such_vertices=pad_vs_street,
                        street_vertices_held_by_an_earlier_street_at_another_level={s.name: s.clash for s in T.streets}),
        pad_cutfill=dict(median=round(float(np.median(cfs)), 2), max=round(float(cfs.max()), 2), n_over_2_5=int((cfs > 2.5).sum()),
                         n_over_4=int((cfs > 4.0).sum()),
                         over_4=[[o["kid"], round(o["cf"], 2)] for o in objs if o["cf"] > 4.0],
                         square=(dict(level=T.sqz, cutfill_max=T.pads["square"]["cutfill_max"], feasible=T.pads["square"]["ok"], why=T.pads["square"]["why"])
                                 if "square" in T.pads else None)),
        grader_as_drawn=dict(accepted=sum(1 for w in res.values() if w == "ok"), refused=sum(1 for w in res.values() if w != "ok"),
                             causes=dict(collections.Counter(cause_of(T, w) for w in res.values() if w != "ok")),
                             accepted_by_role=dict(collections.Counter(o["role"] for o in acc)), rows=res),
        ground=dict(infeasible_vertices=G.infeasible))
    return T


# ---------------------------------------------------------------- checks on the seated town
def bank_scan(T, streets, max_r=25.0, dz_lim=1.5):
    """every 2 m on both edges of a street: walk straight out up to 25 m; the edge faces a bank if the walk meets a graded
    face (edited > 0.3 m, slope > 20 deg) more than 1.5 m high before it reaches a building, another street or the square"""
    G = T.G
    H = G.H
    res = 0.5
    box = G.box()
    occ = raster_polys([footprint(b["m"], b["O"], b["yaw"], 0.3) for b in T.acc], box, res)
    rib = []
    for o in T.streets:
        for a_, b_ in zip(o.P[:-1:2], o.P[2::2]):
            u = unit(b_ - a_)
            nn = left(u) * (o.width / 2)
            rib.append(np.array([a_ - nn - 0.3 * u, b_ - nn + 0.3 * u, b_ + nn + 0.3 * u, a_ + nn - 0.3 * u]))
    stop = raster_polys(rib + ([T.sq] if T.sq is not None else []), box, res)
    gy, gx = np.gradient(H, C)
    slope = np.degrees(np.arctan(np.hypot(gx, gy)))
    out = []
    rr = np.arange(0.3, max_r, 0.5)
    for st in streets:
        half = st.width / 2
        for s in np.arange(1.0, st.L - 1.0, 2.0):
            k_ = min(max(int(np.searchsorted(st.s, s)), 1), len(st.s) - 1)
            p, u = st.xy(s), unit(st.P[k_] - st.P[k_ - 1])
            for side in (1, -1):
                n = left(u) * side
                Q = p[None, :] + (half + rr)[:, None] * n[None, :]
                ix = np.clip(((Q[:, 0] - box[0]) / res).astype(int), 0, occ.shape[1] - 1)
                iy = np.clip(((Q[:, 1] - box[1]) / res).astype(int), 0, occ.shape[0] - 1)
                blk = occ[iy, ix] | stop[iy, ix]
                g = bil(G, H, Q[:, 0], Q[:, 1])
                steep = (np.abs(g - bil(G, G.nat, Q[:, 0], Q[:, 1])) > 0.3) & (bil(G, slope, Q[:, 0], Q[:, 1]) > 20.0)
                kb = int(np.argmax(blk)) if blk.any() else len(rr)
                hit, k = None, 0
                while k < kb:
                    if steep[k]:
                        k2 = k
                        while k2 + 1 < kb and steep[k2 + 1]:
                            k2 += 1
                        hgt = float(g[min(k2 + 1, len(g) - 1)] - g[max(k - 1, 0)])
                        if abs(hgt) > dz_lim:
                            hit = (k, hgt)
                            break
                        k = k2 + 1
                    else:
                        k += 1
                if hit:
                    out.append(dict(street=st.name, s=round(float(s), 1), side=side, r=round(float(rr[hit[0]]), 1), dz=round(hit[1], 2),
                                    xy=[round(float(p[0]), 1), round(float(p[1]), 1)]))
    return out


def runs_of(scan, gapmax=4.5):
    runs = []
    for k in sorted(scan, key=lambda q: (q["street"], q["side"], q["s"])):
        if runs and runs[-1]["street"] == k["street"] and runs[-1]["side"] == k["side"] and k["s"] - runs[-1]["s1"] <= gapmax:
            runs[-1]["s1"] = k["s"]
            runs[-1]["n"] += 1
            runs[-1]["dz"] = max(runs[-1]["dz"], abs(k["dz"]))
        else:
            runs.append(dict(street=k["street"], side=k["side"], s0=k["s"], s1=k["s"], n=1, dz=abs(k["dz"]), xy=k["xy"]))
    return runs


def checks(T):
    G, H, LAY = T.G, T.G.H, T.lay
    out = collections.OrderedDict()
    seated = T.acc
    n_all, n_seat = len(T.objs), len(seated)
    row = lambda name, rule, result, status: out.__setitem__(name, dict(rule=rule, result=result, status=status))
    row("buildings seated", "every building must be seated as drawn", "%d of %d" % (n_seat, n_all), "PASS" if n_seat == n_all else "FAIL")
    fam = collections.Counter(kind_of_check(T, o, o["why"]) for o in T.objs if o["why"] != "ok")
    row("refusals by kind", "first failed test per refused building", dict(fam) if fam else "none", "PASS" if not fam else "FAIL")
    gc = T.counts["grid_clash"]
    row("pad-pad clash", "two pads at different levels may not share a grid point (all buildings, order-free)",
        "%d pairs of pad groups, %d shared points" % (gc["pad_group_pairs_sharing_a_vertex_at_different_levels"], gc["shared_vertices"]),
        "PASS" if gc["pad_group_pairs_sharing_a_vertex_at_different_levels"] == 0 else "FAIL")
    row("pad-street / ramp / lane clash", "no pad point may sit on a street, lane, path or square point at another level (all buildings, order-free)",
        "%d buildings, %d grid points" % (gc["buildings_whose_pad_meets_street_cells_at_another_level"], gc["such_vertices"]),
        "PASS" if gc["such_vertices"] == 0 else "FAIL")
    sc = {k: v for k, v in gc["street_vertices_held_by_an_earlier_street_at_another_level"].items() if v}
    row("street-street clash", "grid points two streets both claim at different levels; the earlier street keeps its level there, so the later one gets a step. "
        "A few at a junction where a ramp meets a level street are normal; dozens mean two streets run over each other at different levels (report)",
        sc if sc else "none", "REPORT")
    if "square" in T.pads:
        p = T.pads["square"]
        row("square", "one level; every point within 4.0 m of natural ground; no street point at another level; 31 deg bank to everything else",
            "level %.2f m, cut/fill max %.2f m, %d points meet streets at another level %s; %s" % (p["level"], p["cutfill_max"], p["clash_points"],
                                                                                             p["clash_owners"] or "", "ok" if p["ok"] else p["why"]),
            "PASS" if p["ok"] and p["clash_points"] == 0 else "FAIL")
    for k, p in T.pads.items():
        if k != "square":
            row("fixed pad " + k, "a fixed level patch of ours (from --fixed)", "level %.2f m, cut/fill %.2f m, %s" % (p["level"], p["cutfill_max"], "ok" if p["ok"] else p["why"]),
                "PASS" if p["ok"] else "FAIL")
    pc = T.counts["pad_cutfill"]
    row("pad cut / fill (true grid)", "every pad point within 4.0 m of the natural ground; aim for 2.5 m (all buildings as drawn)",
        "median %.2f m, max %.2f m, %d over 2.5 m, %d over 4.0 m %s" % (pc["median"], pc["max"], pc["n_over_2_5"], pc["n_over_4"], pc["over_4"] or ""),
        "PASS" if pc["n_over_4"] == 0 else "FAIL")
    row("ground solvable", "31 deg cones between all fixed points must meet (seated set)", "%d infeasible grid points" % G.infeasible,
        "PASS" if G.infeasible == 0 else "FAIL")
    # door threshold and wall below ground (seated)
    thr, wbg, dvs = [], [], []
    for b in seated:
        m = b["m"]
        dc, dvec = door_point(m, b["O"], b["yaw"])
        outp = dc + 1.0 * dvec
        surf = float(np.mean(tri_z(G, H, outp[0], outp[1])))
        thr.append((b["kid"], round(b["pad"] - surf, 3)))
        ring = footprint(m, b["O"], b["yaw"], 0.25)
        rp = np.vstack([ring[k] + (ring[(k + 1) % 4] - ring[k]) * t for k in range(4) for t in np.linspace(0, 1, 9)[:-1]])
        ra, rb = tri_z(G, H, rp[:, 0], rp[:, 1])
        wbg.append((b["kid"], round(max(0.0, float(np.max(np.r_[ra, rb]) - b["pad"])), 3)))
        if b["street"] in T.SN:
            st = T.SN[b["street"]]
            s_, d_ = st.project(np.array([dc[0]]), np.array([dc[1]]))
            dvs.append((b["kid"], b["street"], round(b["pad"] - st.zs(s_[0]), 3), round(float(d_[0]), 1)))
    tf = [x for x in thr if abs(x[1]) > 0.05]
    row("door threshold vs ground 1 m out", "pad (= floor = threshold) within 5 cm of the graded surface 1 m out of the door (seated)",
        "max %.3f m; %d fail %s" % (max([abs(x[1]) for x in thr] or [0]), len(tf), tf[:12] or ""), "PASS" if not tf else "FAIL")
    df = [x for x in dvs if abs(x[2]) > 0.05 and x[3] <= 12.0]
    row("door threshold vs street surface", "pad within 5 cm of its street's level at the door's station, for doors within 12 m of the centre line (seated)",
        "%d checked, %d fail %s; %d doors more than 12 m from their street (listed in result.json)" % (len(dvs), len(df), df[:12] or "", sum(1 for x in dvs if x[3] > 12.0)),
        "PASS" if not df else "FAIL")
    wf = [x for x in wbg if x[1] > 0.3]
    row("wall below ground", "highest ground 0.25 m outside the walls minus the floor <= 0.3 m (seated)",
        "max %.2f m; %d fail %s" % (max([x[1] for x in wbg] or [0]), len(wf), wf[:12] or ""), "PASS" if not wf else "FAIL")
    # overlaps and ribbons over the whole drawn layout (design checks) and among the seated
    ov_all, gap_min = [], 1e9
    for a in range(len(T.objs)):
        for b_ in range(a + 1, len(T.objs)):
            A_, B_ = T.objs[a], T.objs[b_]
            if abs(A_["c"][0] - B_["c"][0]) > 45 or abs(A_["c"][1] - B_["c"][1]) > 45:
                continue
            pen = sat_pen(A_["fp"], B_["fp"])
            if pen > 0:
                ov_all.append((A_["kid"], B_["kid"], round(float(pen), 3)))
            else:
                gap_min = min(gap_min, -pen)
    row("overlaps", "no two footprint boxes overlap (whole layout as drawn)", "%d pairs %s; closest gap %.3f m" % (len(ov_all), ov_all[:12] or "", gap_min if gap_min < 1e9 else 0),
        "PASS" if not ov_all else "FAIL")
    own_r = [(o["kid"],) + r for o in T.objs for r in o["ribbon"] if r[0] == o["street"]]
    oth_r = [(o["kid"],) + r for o in T.objs for r in o["ribbon"] if r[0] != o["street"]]
    row("in a street ribbon (own street)", "footprint >= half-width + 0.2 m from its own street's centre line (whole layout)",
        "%d buildings %s" % (len({x[0] for x in own_r}), own_r[:12] or ""), "PASS" if not own_r else "FAIL")
    row("corner clearance (other streets)", "footprint >= half-width + 1.0 m from every other street's centre line (whole layout)",
        "%d buildings %s" % (len({x[0] for x in oth_r}), oth_r[:12] or ""), "PASS" if not oth_r else "FAIL")
    bk = [o for o in T.objs if o["why"].startswith("bank too steep")]
    row("back-to-back gap (31 deg bank)", "pads at different levels need at least |dz| / 0.6 m between their grid points (first failure per building)",
        "%d buildings refused %s" % (len(bk), [(o["kid"], o["why"].split(" vs ")[1]) for o in bk][:12] or ""), "PASS" if not bk else "FAIL")
    main_lane = [s for s in T.streets if s.cls in ("main", "lane")]
    scan = bank_scan(T, main_lane)
    runs = runs_of(scan)
    row("banks facing streets", "a graded bank over 1.5 m seen from a main street or lane edge, before any building (seated set; report)",
        "%d runs, %d stations (by street: %s)" % (len(runs), len(scan), dict(collections.Counter(r["street"] for r in runs))), "REPORT")
    sr = {s.name: straight_runs(s) for s in T.streets}
    srf = {k: v["longest_m"] for k, v in sr.items() if v["longest_m"] > 80.0 and T.SN[k].cls in ("main", "lane")}
    row("straight runs", "no main street or lane straight for more than 80 m (within 1.0 m of its chord)",
        "longest main street or lane: %s; roads and paths (report): %s%s" % (
            ("%s %.1f m" % max(((k, v["longest_m"]) for k, v in sr.items() if T.SN[k].cls in ("main", "lane")), key=lambda kv: kv[1])) if main_lane else "none",
            ", ".join("%s %.1f m" % (k, v["longest_m"]) for k, v in sr.items() if T.SN[k].cls not in ("main", "lane")) or "none",
            "; over 80 m: %s" % srf if srf else ""),
        "PASS" if not srf else "FAIL")
    gr = {s.name: round(float(np.max(np.abs(np.diff(s.z)) / np.maximum(np.diff(s.s), 1e-6)) * 100), 1) for s in T.streets}
    row("street grades", "main streets under 5 % (8 % average, 12 % on a short drop), lanes under 19 %, paths are stairs (report)", gr, "REPORT")
    for label, objs_ in (("drawn", T.objs), ("seated", seated)):
        n = len(objs_)
        if not n:
            continue
        cm = collections.Counter(o["mid"] for o in objs_)
        ct = collections.Counter(TWIN[o["mid"]] for o in objs_)
        fm = [(k, v, round(100.0 * v / n, 1)) for k, v in cm.items() if v > 0.15 * n + 1e-9]
        ft = [(k, v, round(100.0 * v / n, 1)) for k, v in ct.items() if v > 0.12 * n + 1e-9 and "+" in k]
        top = cm.most_common(1)[0]
        tt = max(ct.items(), key=lambda kv: kv[1])
        row("model / twin share (%s)" % label, "any one model <= 15 %, any one twin group (colour variants of one house) <= 12 %" +
            (" (the check is on the town as drawn; the seated share is a report)" if label == "seated" else ""),
            "largest model %s %d = %.1f %%, largest twin group %s %d = %.1f %%%s" % (top[0], top[1], 100.0 * top[1] / n, tt[0], tt[1], 100.0 * tt[1] / n,
                                                                                 ("; over: %s" % (fm + ft)) if fm or ft else ""),
            ("PASS" if not (fm or ft) else "FAIL") if label == "drawn" else "REPORT")
    lamps = LAY.get("lamps") or []
    if lamps:
        lf = []
        for k, l in enumerate(lamps):
            p = np.array([l["x"], l["y"]], float)
            for st in T.streets:
                s_, d_ = st.project(np.array([p[0]]), np.array([p[1]]))
                if d_[0] < st.width / 2 + 0.5 and st.name != l.get("street"):
                    lf.append((l.get("id", "L%03d" % k), st.name, round(float(d_[0] - st.width / 2), 2)))
            sq_ = np.array([[p[0] - 0.3, p[1] - 0.3], [p[0] + 0.3, p[1] - 0.3], [p[0] + 0.3, p[1] + 0.3], [p[0] - 0.3, p[1] + 0.3]])
            za, zb = tri_z(G, H, sq_[:, 0], sq_[:, 1])
            if float(np.ptp(np.r_[za, zb])) > 0.07:
                lf.append((l.get("id", "L%03d" % k), "ground under the base varies %.2f m" % float(np.ptp(np.r_[za, zb]))))
        row("lamps", "every lamp at least 0.5 m clear of every other street's carriageway; ground under its base flat within 7 cm",
            "%d lamps, %d problems %s" % (len(lamps), len(lf), lf[:12] or ""), "PASS" if not lf else "FAIL")
    else:
        row("lamps", "lamp positions, if given", "none given (we place lamps ourselves)", "n/a")
    comps = [c for c in (LAY.get("comps") or []) if c.get("footprint_m") and c.get("x") is not None]
    if comps:
        cf_ = []
        for c in comps:
            w, d = c["footprint_m"][:2]
            ex, ez = axes(float(c.get("yaw_deg", 0.0)))
            P0 = np.array([c["x"], c["y"]], float)
            R = np.array([P0 + sx * w / 2 * ex + sz * d / 2 * ez for sx, sz in ((-1, -1), (1, -1), (1, 1), (-1, 1))])
            lvl = c.get("pad_z_m", c.get("z_m", c.get("level_z_m")))
            if lvl is None and T.sq is not None and sat_pen(R, T.sq) > 0:
                lvl = T.sqz
            name_ = c.get("name_or_role", c.get("name", "comp"))
            if lvl is None:
                cf_.append(dict(comp=name_, level=None, why="no level given (pad_z_m)", overlaps=[], in_carriageway=[], ok=False))
                continue
            V = G.cells_of_poly(R)
            ok, why = G.feasible(V, float(lvl))
            hits = [b["kid"] for b in seated if sat_pen(R, b["fp"]) > 0]
            car = [st.name for st in T.streets if seg_poly_dist(st, R) < st.width / 2]
            cf_.append(dict(comp=name_, level=round(float(lvl), 2), why=("its pad would seat: " if ok else "its pad would NOT seat: ") + why,
                            overlaps=hits, in_carriageway=car, ok=ok and not hits and not car))
        row("comp seat and height", "a whole comp needs its own level pad (every grid point of its rectangle at its pad_z_m, the same tests as a building pad, "
            "after the buildings), clear of seated buildings and of every carriageway",
            [(x["comp"], "level %s: %s%s%s" % (x["level"], x["why"], ", overlaps %s" % x["overlaps"] if x["overlaps"] else "",
                                               ", in %s" % x["in_carriageway"] if x["in_carriageway"] else "")) for x in cf_],
            "PASS" if all(x["ok"] for x in cf_) else "FAIL")
    else:
        row("comp seat and height", "whole comps with a footprint, if given", "none given with a footprint (roles only)", "n/a")
    nh = {s.name: s.no_height for s in T.streets if s.no_height}
    if nh or G.missing.any():
        row("height data coverage", "every grid point the grader uses should come from your height window(s)",
            "%d of %d grid points outside them%s" % (int(G.missing.sum()), G.missing.size, "; street points without heights: %s" % nh if nh else ""),
            "FAIL" if nh else "REPORT")
    T.extra = dict(thresholds=thr, door_vs_street=dvs, wall_below_ground=wbg, bank_runs=runs, bank_stations=scan, straight_runs=sr, grades=gr,
                   overlaps=ov_all, ribbons_own=own_r, ribbons_other=oth_r)
    return out


# ---------------------------------------------------------------- outputs
def building_rows(T):
    order = {b["id"]: k for k, b in enumerate(T.lay["buildings"])}
    rows = []
    for o in sorted(T.objs, key=lambda o: order[o["kid"]]):
        w = o["why"]
        rows.append(dict(id=o["kid"], model=o["mid"], street=o["street"] or "", role=o["role"], pad_group=o["group"], pad_z=round(o["pad"], 2),
                         seated="yes" if w == "ok" else "no", kind="" if w == "ok" else kind_of_check(T, o, w),
                         reason=plain_reason(T, o, w), grader_message=w, cutfill_m=round(o["cf"], 2),
                         clash_points=len(o["clash"]), grade_order=[x["kid"] for x in T.objs].index(o["kid"]) + 1))
    return rows


def write_atomic(path, text, binary=False):
    tmp = path + ".tmp"
    with open(tmp, "wb" if binary else "w", **({} if binary else dict(encoding="utf-8", newline="\n"))) as f:
        f.write(text)
    os.replace(tmp, path)


def jdefault(o):
    if isinstance(o, (np.integer,)):
        return int(o)
    if isinstance(o, (np.floating,)):
        return float(o)
    if isinstance(o, np.ndarray):
        return o.tolist()
    if isinstance(o, (set, tuple)):
        return list(o)
    return str(o)


def plot(T, path, title):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from matplotlib.patches import Polygon, Rectangle
    from matplotlib.lines import Line2D
    G = T.G
    pts = np.vstack([o["fp"] for o in T.objs] + [s.P for s in T.streets] + ([T.sq] if T.sq is not None else []))
    x0, y0 = pts.min(0) - 25
    x1, y1 = pts.max(0) + 25
    w_m, h_m = x1 - x0, y1 - y0
    scale = 16.0 / max(w_m, h_m)
    fig, ax = plt.subplots(figsize=(max(6.0, w_m * scale) + 0.5, max(6.0, h_m * scale) + 1.6), dpi=110)
    ax.set_facecolor("#f4f1ea")
    X = G.X[0]
    Y = G.Y[:, 0]
    lv = np.arange(math.floor(np.nanmin(G.nat) / 2) * 2, math.ceil(np.nanmax(G.nat) / 2) * 2 + 2, 2.0)
    ax.contour(X, Y, G.nat, levels=lv, colors="#c9bfa8", linewidths=0.4, zorder=1)
    ax.contour(X, Y, G.nat, levels=lv[(lv % 10) == 0], colors="#9d8f72", linewidths=0.8, zorder=1)
    for s in T.streets:
        rib = []
        for a_, b_ in zip(s.P[:-1], s.P[1:]):
            u = unit(b_ - a_)
            nn = left(u) * (s.width / 2)
            rib.append(np.array([a_ - nn, b_ - nn, b_ + nn, a_ + nn]))
        col = {"main": "#a8a8a8", "lane": "#c4c4c4", "road": "#b9b0a0", "path": "#d8c9a8"}.get(s.cls, "#c4c4c4")
        for q in rib:
            ax.add_patch(Polygon(q, closed=True, fc=col, ec=col, lw=0.4, zorder=2))
        ax.plot(s.P[:, 0], s.P[:, 1], color="#6b6b6b", lw=0.4, zorder=3)
        k = len(s.P) // 2
        ax.text(s.P[k, 0], s.P[k, 1], s.name, fontsize=6, color="#333333", ha="center", va="center", zorder=9,
                bbox=dict(fc="white", ec="none", alpha=0.6, pad=0.5))
    if T.sq is not None:
        ax.add_patch(Polygon(T.sq, closed=True, fc="#cfe0f2", ec="#3b6fb0", lw=1.0, zorder=3))
    for k, p in T.fixed_pads.items():
        ax.add_patch(Polygon(np.array(p["polygon"], float), closed=True, fc="#dde8f5", ec="#3b6fb0", lw=0.8, ls="--", zorder=3))

    def cell(j, i, fc, alpha, z=6):
        xx, yy = G.xy(j, i)
        ax.add_patch(Rectangle((xx, yy), C, C, fc=fc, ec="none", alpha=alpha, zorder=z))

    for o in T.objs:
        if o["why"] == "ok":
            continue
        padcells = set()
        Vs = set(o["V"])
        for (j, i) in Vs:
            if (j + 1, i) in Vs and (j, i + 1) in Vs and (j + 1, i + 1) in Vs:
                padcells.add((j, i))
        for j, i, _, _ in o["clash"]:
            for cj, ci in ((j - 1, i - 1), (j - 1, i), (j, i - 1), (j, i)):
                if (cj, ci) in padcells:
                    cell(cj, ci, "#e0301e", 0.35)
        for j, i, _, _ in o["clash"]:
            xx, yy = G.xy(j, i)
            ax.plot(xx, yy, marker="x", color="#b00000", ms=3.5, mew=0.9, zorder=8)
        if o["why"].startswith("bank too steep") and o["bank"]:
            (j1, i1), (j2, i2) = o["bank"][0], o["bank"][1]
            a, b = G.xy(j1, i1), G.xy(j2, i2)
            ax.plot([a[0], b[0]], [a[1], b[1]], color="#c000c0", lw=1.6, zorder=8)
    for s in T.streets:
        for j, i, _, _, _ in s.clash_where:
            xx, yy = G.xy(j, i)
            ax.plot(xx, yy, marker="o", color="#ff8c00", ms=2.6, mec="#a05000", mew=0.4, zorder=7)
    for key, cl in T.pad_clash.items():
        for j, i, _, _ in cl:
            xx, yy = G.xy(j, i)
            ax.plot(xx, yy, marker="s", color="#2050d0", ms=3.0, zorder=7)
    for j, i in G.infeasible_where:
        xx, yy = G.xy(j, i)
        if x0 <= xx <= x1 and y0 <= yy <= y1:
            ax.plot(xx, yy, marker=".", color="black", ms=2.0, zorder=7)
    for o in T.objs:
        ok = o["why"] == "ok"
        if ok:
            ax.add_patch(Polygon(o["fp"], closed=True, fc="#5aa55a", ec="#1f5f1f", lw=0.6, alpha=0.9, zorder=5))
        else:
            rib = o["why"].startswith("street ribbon") or o["why"].startswith("overlap")
            ax.add_patch(Polygon(o["fp"], closed=True, fc="white", ec="#c00000", lw=1.0, ls="--" if rib else "-", alpha=0.95, zorder=5))
        dc, dvec = door_point(o["m"], o["O"], o["yaw"])
        ax.plot([dc[0], dc[0] + 2.0 * dvec[0]], [dc[1], dc[1] + 2.0 * dvec[1]], color="#1f5f1f" if ok else "#c00000", lw=0.8, zorder=6)
        ax.text(o["c"][0], o["c"][1], o["kid"].replace("B0", "").replace("B", ""), fontsize=4.5, ha="center", va="center",
                color="white" if ok else "#900000", zorder=9)
    ax.set_xlim(x0, x1)
    ax.set_ylim(y0, y1)
    ax.set_aspect("equal")
    ax.grid(False)
    ax.tick_params(labelsize=7)
    ax.set_xlabel("map x (m, east)", fontsize=8)
    ax.set_ylabel("map y (m, north)", fontsize=8)
    sx = x0 + 10
    ax.plot([sx, sx + 50], [y0 + 8, y0 + 8], color="black", lw=2.5, zorder=10)
    ax.text(sx + 25, y0 + 11, "50 m", ha="center", fontsize=7, zorder=10)
    a_ = T.counts["grader_as_drawn"]
    ax.set_title("%s\nseated %d of %d as drawn; %d infeasible grid points" % (title, a_["accepted"], T.counts["buildings"], T.G.infeasible), fontsize=10)
    leg = [Polygon([[0, 0]], fc="#5aa55a", ec="#1f5f1f", label="seated building (tick = door)"),
           Polygon([[0, 0]], fc="white", ec="#c00000", label="refused: pad meets fixed ground / bank / cut-fill"),
           Polygon([[0, 0]], fc="white", ec="#c00000", ls="--", label="refused: street ribbon or overlap"),
           Rectangle((0, 0), 1, 1, fc="#e0301e", alpha=0.35, label="clashing 5 m pad cell"),
           Line2D([], [], marker="x", color="#b00000", ls="none", label="grid point already fixed at another level"),
           Line2D([], [], color="#c000c0", lw=1.6, label="bank too steep (31 deg) between these points"),
           Line2D([], [], marker="o", color="#ff8c00", ls="none", label="street point held by an earlier street at another level"),
           Line2D([], [], marker="s", color="#2050d0", ls="none", label="square / fixed pad point at another street's level"),
           Line2D([], [], marker=".", color="black", ls="none", label="infeasible ground point (cones cannot meet)")]
    ax.legend(handles=leg, loc="upper center", bbox_to_anchor=(0.5, -0.06), ncol=3, fontsize=6.5, frameon=False)
    fig.tight_layout()
    tmp = path + ".tmp.png"
    fig.savefig(tmp, dpi=110)
    plt.close(fig)
    os.replace(tmp, path)


def write_outputs(T, ck, outdir, name, args_echo):
    os.makedirs(outdir, exist_ok=True)
    rows = building_rows(T)
    a_ = T.counts["grader_as_drawn"]
    # csv
    cols = ["id", "model", "street", "role", "pad_group", "pad_z", "seated", "kind", "reason", "cutfill_m", "clash_points", "grade_order"]
    lines = [",".join(cols)]
    for r in rows:
        lines.append(",".join('"%s"' % str(r[c]).replace('"', "'") if isinstance(r[c], str) else str(r[c]) for c in cols))
    write_atomic(os.path.join(outdir, "buildings.csv"), "\n".join(lines) + "\n")
    # json
    res = dict(grader=VERSION, layout=name, command=args_echo, counts=T.counts, checks=ck, buildings=rows,
               streets={s.name: dict(cls=s.cls, width_m=s.width, length_m=round(s.L, 1), grid_points_fixed=s.vertices,
                                     points_held_by_earlier_street_at_another_level=s.clash, cutfill_max_m=round(s.cutfill, 2),
                                     clash_points=[[round(G_[0], 1), round(G_[1], 1), round(z_, 2), round(c_, 2), w_] for (j, i, z_, c_, w_) in s.clash_where
                                                   for G_ in [T.G.xy(j, i)]]) for s in T.streets},
               pads=T.pads, extra=T.extra)
    write_atomic(os.path.join(outdir, "result.json"), json.dumps(res, indent=1, default=jdefault))
    # markdown report
    md = ["# Grade: %s" % (T.lay.get("town") or name), "",
          "%s. Layout `%s`. Version string in the layout: %s." % (VERSION, name, T.lay.get("version", "-")), "",
          "**Seated as drawn: %d of %d.** Refused: %d." % (a_["accepted"], T.counts["buildings"], a_["refused"]), "",
          "Refusal causes (our grading agent's categories): " + ("; ".join("%s %d" % (k, v) for k, v in a_["causes"].items()) or "none") + ".", "",
          "Seated by role: " + (", ".join("%s %d" % (k, v) for k, v in a_["accepted_by_role"].items()) or "none") + ".", "",
          "## Checks", "", "| Check | Rule | Result | Status |", "|---|---|---|---|"]
    for k, v in ck.items():
        md.append("| %s | %s | %s | %s |" % (k, v["rule"], str(v["result"]).replace("|", "/"), v["status"]))
    md += ["", "## Buildings (in your file's order; grade_order = the order the grader seats them)", "",
           "| id | model | street | role | pad z | seated | why |", "|---|---|---|---|---|---|---|"]
    for r in rows:
        md.append("| %s | %s | %s | %s | %.2f | %s | %s |" % (r["id"], r["model"], r["street"], r["role"], r["pad_z"], r["seated"], r["reason"]))
    md += ["", "## Streets", "", "| street | class | width | grid points fixed | points already held by an earlier street at another level | max grade % |",
           "|---|---|---|---|---|---|"]
    for s in T.streets:
        md.append("| %s | %s | %.1f | %d | %d | %s |" % (s.name, s.cls, s.width, s.vertices, s.clash, T.extra["grades"][s.name]))
    md += ["", "Files: `plan.png` (every clashing cell drawn), `buildings.csv`, `result.json` (everything, with the grid points)."]
    write_atomic(os.path.join(outdir, "report.md"), "\n".join(md) + "\n")
    plot(T, os.path.join(outdir, "plan.png"), T.lay.get("town") or name)
    return rows


def main(argv=None):
    ap = argparse.ArgumentParser(description="Grade a town layout on the 5 m terrain grid (stand-alone copy of our grader).")
    ap.add_argument("layout", help="the town layout json (return schema)")
    ap.add_argument("--height", nargs=3, action="append", metavar=("NPY", "X0", "Y0"), default=[],
                    help="a 1 m height window and its south-west corner in map metres; repeat for a second window")
    ap.add_argument("--grid5", nargs=3, action="append", metavar=("NPY", "X0", "Y0"), default=[],
                    help="a 5 m grid file (heights_5m/) and its south-west corner in map metres: the exact grid, used before any --height")
    ap.add_argument("--fixed", help="optional json of fixed features of ours at this site (streets that replace yours by id, level pads, order)")
    ap.add_argument("--out", help="output folder (default grade_<layout name>)")
    ap.add_argument("--expect", help="a result.json from grader/expected/: after grading, say whether this run matches it building by building")
    ap.add_argument("--rear", type=float, default=REAR_DEFAULT, help="pad margin on the side away from the street for street-row houses (default 0.4)")
    a = ap.parse_args(argv)
    LAY = json.load(open(a.layout, encoding="utf-8"))
    wins = []
    if not a.height and not a.grid5:
        raise SystemExit("give at least one --grid5 or --height file")
    for step, lst in ((5, a.grid5), (1, a.height)):
        for p, x0, y0 in lst:
            H = np.load(p, allow_pickle=False)
            if H.ndim != 2:
                raise SystemExit("%s is not a 2-D height array" % p)
            X0, Y0 = int(round(float(x0))), int(round(float(y0)))
            if step == 5 and (X0 % 5 or Y0 % 5):
                raise SystemExit("--grid5 %s: the corner must be a multiple of 5 m" % p)
            wins.append((H, X0, Y0, step))
    fixed = json.load(open(a.fixed, encoding="utf-8")) if a.fixed else None
    name = os.path.splitext(os.path.basename(a.layout))[0]
    outdir = a.out or ("grade_" + name)
    T = grade(LAY, wins, fixed, a.rear)
    ck = checks(T)
    echo = "town_grader.py %s %s%s%s" % (os.path.basename(a.layout), " ".join(["--grid5 %s %s %s" % (os.path.basename(p), x, y) for p, x, y in a.grid5] +
                                                                              ["--height %s %s %s" % (os.path.basename(p), x, y) for p, x, y in a.height]),
                                       " --fixed %s" % os.path.basename(a.fixed) if a.fixed else "", " --rear %s" % a.rear if a.rear != REAR_DEFAULT else "")
    write_outputs(T, ck, outdir, name, echo)
    a_ = T.counts["grader_as_drawn"]
    print("%s: seated %d of %d as drawn" % (T.lay.get("town") or name, a_["accepted"], T.counts["buildings"]))
    for k, v in a_["causes"].items():
        print("   %3d  %s" % (v, k))
    fails = [k for k, v in ck.items() if v["status"] == "FAIL"]
    print("checks failed: %s" % (", ".join(fails) if fails else "none"))
    print("infeasible grid points: %d" % T.G.infeasible)
    print("wrote %s" % outdir)
    if a.expect:
        E = json.load(open(a.expect, encoding="utf-8"))["counts"]
        ea, ma = E["grader_as_drawn"], a_
        import re
        num = lambda w: re.sub(r"[0-9]+[.][0-9]+", "#", w)
        keys = sorted(set(ea["rows"]) | set(ma["rows"]))
        dif = [k for k in keys if num(str(ea["rows"].get(k))) != num(str(ma["rows"].get(k)))]
        dnum = [k for k in keys if k not in dif and ea["rows"].get(k) != ma["rows"].get(k)]
        same = (not dif and ea["accepted"] == ma["accepted"]
                and E["grid_clash"]["street_vertices_held_by_an_earlier_street_at_another_level"] == T.counts["grid_clash"]["street_vertices_held_by_an_earlier_street_at_another_level"])
        print("EXPECTED: seated %d, this run %d; buildings with a different verdict: %d %s" % (ea["accepted"], ma["accepted"], len(dif), dif[:10]))
        if dnum:
            print("   same verdicts, but %d message(s) differ in a measured number (a 1 m file is rounded): %s" % (len(dnum), dnum[:10]))
        if E["ground"] != T.counts["ground"]:
            print("   infeasible grid points: expected %s, this run %s" % (E["ground"]["infeasible_vertices"], T.counts["ground"]["infeasible_vertices"]))
        print("MATCH" if same else "NO MATCH: check your height file and its corner, and that you used --fixed where the sheet says so")
        if not same:
            return 2
    return 0 if not fails else 1


if __name__ == "__main__":
    sys.exit(main())
