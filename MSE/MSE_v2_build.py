"""
MSE v2: sci-fi repulsorlift IFV for Arma 3 (Clone Wars era, 41st legion).

v2 is an outward redesign of v1, rebuilt to follow the reference sheet of a
heavy Republic-style repulsor tank much more closely (and to move away from
the hover_ifv/ look), while staying an original design:

    * thin side armor walls that flare outward toward the top (a V seen from
      the front), bent along a chine, with an open gutter between each wall
      and the hull, and a wedge prow (top edge falls, bottom edge rises);
    * wide, layered armor arms forming a big chevron over a hollow nose, so
      the walls' inner faces and machinery show underneath; twin lens
      clusters at their feet, a porthole sensor at their apex and a keel rib
      below it;
    * a broad driver's brow with a long window on its sloped front and boxed
      lights at its corners;
    * a narrow two-cheek turret with the 50 mm autocannon on a cylindrical
      mount between the cheeks, a ball-and-mast sensor cluster on the left,
      and on the right a box pod that is the 8-cell vertical launch system
      (cells open upward through its roof);
    * horizontal coil-spring dampers on the deck beside the turret;
    * a large segmented transverse engine drum on end brackets;
    * a rear face of tall louvered engine modules around the ramp.

Bradley-sized: about 6.9 m long, 3.6 m wide, 2.75 m to the top of the
turret sensors. 2 crew + 13 passengers. Detail goes into greebles and
visible surfaces; rivets are kept light and the belly stays plain.

Pick the legion markings with LIVERY below or on the command line:
41st (green, default), republic (red), 501st (blue), 212th (orange).

Builds the whole model from scratch with bpy/bmesh, no add-ons needed.

Run headless:
    blender --background --python MSE_v2_build.py -- --out MSE_v2.blend [--livery 501st]
Or open it in Blender's Scripting tab in a NEW, EMPTY file and press Run.
It deletes everything in the current file before building.

Conventions (match the Arma 3 Object Builder add-on):
    1 Blender unit = 1 m, +Y is forward, +Z is up, ground at Z = 0.
    Faces are tris/quads only (P3D does not take n-gons).
    Each object carries a vertex group named for its Arma selection
    (hull, turret, gun, ramp, vls_hatch_N, rocket_N, ...), so joining the
    visual parts into one LOD mesh keeps the selections intact.
    Animated parts have their origin on their pivot.
"""

import math
import random
import sys

import bpy  # before bmesh: the standalone bpy module only exposes bmesh after this
import bmesh
from mathutils import Matrix, Vector

R = math.radians


def T(x, y, z):
    return Matrix.Translation((x, y, z))


def Rx(d):
    return Matrix.Rotation(R(d), 4, 'X')


def Ry(d):
    return Matrix.Rotation(R(d), 4, 'Y')


def Rz(d):
    return Matrix.Rotation(R(d), 4, 'Z')


def S(x, y, z):
    return Matrix.Diagonal((x, y, z, 1.0))


def sym(*pts):
    """Mirror points across X so every shape is left/right symmetric."""
    out = []
    for x, y, z in pts:
        out.append((x, y, z))
        if x != 0:
            out.append((-x, y, z))
    return out


def mirror(pts, s):
    return [(s * x, y, z) for x, y, z in pts]


# ---------------------------------------------------------------- bmesh shapes

def bm_hull(pts):
    """Convex hull of a point cloud: gives the faceted, armored look."""
    bm = bmesh.new()
    for p in pts:
        bm.verts.new(p)
    res = bmesh.ops.convex_hull(bm, input=bm.verts[:])
    loose = list({g for g in res['geom_interior'] + res['geom_unused']
                  if isinstance(g, bmesh.types.BMVert)})
    bmesh.ops.delete(bm, geom=loose, context='VERTS')
    bmesh.ops.dissolve_limit(bm, angle_limit=R(0.5),
                             verts=bm.verts[:], edges=bm.edges[:])
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces[:])
    return bm


def bm_box(size, mat=Matrix()):
    bm = bmesh.new()
    bmesh.ops.create_cube(bm, size=1.0, matrix=mat @ S(*size))
    return bm


def bm_box_mm(lo, hi):
    lo, hi = Vector(lo), Vector(hi)
    return bm_box(hi - lo, T(*((lo + hi) / 2)))


def bm_cyl(r1, r2, depth, segs, mat=Matrix()):
    """Cylinder/cone along local Z; r1 at -Z end, r2 at +Z end."""
    bm = bmesh.new()
    bmesh.ops.create_cone(bm, cap_ends=True, cap_tris=False, segments=segs,
                          radius1=r1, radius2=r2, depth=depth, matrix=mat)
    return bm


def bm_sphere(r, mat=Matrix(), u=16, v=8):
    bm = bmesh.new()
    bmesh.ops.create_uvsphere(bm, u_segments=u, v_segments=v, radius=r, matrix=mat)
    return bm


def bm_append(dst, src, mat_index=0, groups=(), dl=None):
    """Copy src into dst (freeing src), tagging material and vertex groups."""
    vmap = {}
    for v in src.verts:
        nv = dst.verts.new(v.co)
        for g in groups:
            nv[dl][g] = 1.0
        vmap[v] = nv
    for f in src.faces:
        nf = dst.faces.new([vmap[v] for v in f.verts])
        nf.material_index = mat_index if mat_index is not None else f.material_index
    src.free()


def bm_merge(*parts):
    """parts: bmesh or (bmesh, material_index); index None keeps the source's."""
    out = bmesh.new()
    for p in parts:
        bm, idx = p if isinstance(p, tuple) else (p, 0)
        bm_append(out, bm, idx)
    return out


def finish(bm, smooth_angle=35):
    ngons = [f for f in bm.faces if len(f.verts) > 4]
    if ngons:
        bmesh.ops.triangulate(bm, faces=ngons, quad_method='BEAUTY',
                              ngon_method='BEAUTY')
    bm.normal_update()
    for f in bm.faces:
        f.smooth = True
    for e in bm.edges:
        if len(e.link_faces) != 2 or e.calc_face_angle(0) > R(smooth_angle):
            e.smooth = False


# ------------------------------------------------------------ scene plumbing

def clear_scene():
    for ob in list(bpy.data.objects):
        bpy.data.objects.remove(ob, do_unlink=True)
    for c in list(bpy.data.collections):
        bpy.data.collections.remove(c)
    for me in list(bpy.data.meshes):
        bpy.data.meshes.remove(me)
    for m in list(bpy.data.materials):
        bpy.data.materials.remove(m)


def coll(name, parent=None):
    c = bpy.data.collections.new(name)
    (parent.children if parent else bpy.context.scene.collection.children).link(c)
    return c


def layer_coll(name, lc=None):
    lc = lc or bpy.context.view_layer.layer_collection
    if lc.name == name:
        return lc
    for child in lc.children:
        found = layer_coll(name, child)
        if found:
            return found
    return None


def material(name, color, rough=0.5, metal=0.0, emit=None, strength=0.0):
    m = bpy.data.materials.new(name)
    if m.node_tree is None:
        m.use_nodes = True
    bsdf = m.node_tree.nodes.get("Principled BSDF")
    bsdf.inputs["Base Color"].default_value = (*color, 1)
    bsdf.inputs["Roughness"].default_value = rough
    bsdf.inputs["Metallic"].default_value = metal
    if emit:
        bsdf.inputs["Emission Color"].default_value = (*emit, 1)
        bsdf.inputs["Emission Strength"].default_value = strength
    m.diffuse_color = (*(emit or color), 1)
    return m


def make(name, bm, mats, collection, origin=(0, 0, 0), groups=(), parent=None,
         smooth=35, bevel=0.0, bevel_segs=1, panels=None):
    """Turn a world-space bmesh into an object whose origin sits at `origin`.

    `panels` runs the panel-line pass (see panelize); any rivets it makes
    become a child object `<name>_rivets` with the same selections.
    """
    if bevel:
        bevel_edges(bm, bevel, bevel_segs)
    rivets = panelize(bm, **panels) if panels is not None else None
    finish(bm, smooth)
    o = Vector(origin)
    bmesh.ops.translate(bm, verts=bm.verts[:], vec=-o)
    me = bpy.data.meshes.new(name)
    bm.to_mesh(me)
    bm.free()
    for m in (mats if isinstance(mats, (list, tuple)) else [mats]):
        me.materials.append(m)
    ob = bpy.data.objects.new(name, me)
    collection.objects.link(ob)
    ob.location = o
    for g in groups:
        ob.vertex_groups.new(name=g).add(range(len(me.vertices)), 1.0, 'REPLACE')
    if parent:
        ob.parent = parent
        ob.matrix_parent_inverse = T(*parent.location).inverted()
    if rivets is not None and len(rivets.verts):
        make(f"{name}_rivets", rivets, DETAIL["rivet"], collection, origin=origin,
             groups=groups, parent=ob)
    elif rivets is not None:
        rivets.free()
    return ob


# ------------------------------------------------------------------ livery

LIVERY = "41st"
LIVERIES = {
    # legion marking color; the base white and running-gear gray are shared
    "41st": (0.10, 0.17, 0.05),
    "republic": (0.40, 0.02, 0.015),
    "501st": (0.02, 0.06, 0.35),
    "212th": (0.70, 0.20, 0.02),
}


def bevel_edges(bm, width, segs=1, min_angle=25):
    """Chamfer the hard edges for the chunky, animated-series armor look."""
    bm.normal_update()
    edges = [e for e in bm.edges
             if len(e.link_faces) == 2 and e.calc_face_angle(0) > R(min_angle)]
    if edges:
        bmesh.ops.bevel(bm, geom=edges, offset=width, segments=segs, profile=0.5,
                        affect='EDGES', clamp_overlap=True)


# ----------------------------------------------------------- detail helpers

DETAIL = {}                               # materials the detail passes need, set in build()


def orient(p, n):
    """Matrix placing local +Z along normal `n` at point `p`."""
    return T(*p) @ Vector(n).to_track_quat('Z', 'Y').to_matrix().to_4x4()


def add_rivet(bm, mat):
    """Hex bolt head (16 tris, no hidden underside) placed by `mat`."""
    ring = []
    for z, r in ((-0.006, 0.012), (0.007, 0.009)):
        ring.append([bm.verts.new(mat @ Vector((r * math.cos(a), r * math.sin(a), z)))
                     for a in (math.pi * k / 3 for k in range(6))])
    for k in range(6):
        bm.faces.new((ring[0][k], ring[0][(k + 1) % 6], ring[1][(k + 1) % 6], ring[1][k]))
    bm.faces.new(ring[1])


def panelize(bm, cuts_x=(), cuts_y=(), cuts_z=(), groove=0.012, lift=0.007,
             rivet_step=0.0, rivet_inset=0.035, alt=None, alt_share=0.25, seed=1,
             min_width=0.045, rivets_where=None):
    """Panel-line a hard-surface mesh and return a bmesh of (few) rivets.

    Cuts the faces with axis-aligned planes, insets every face that is wide
    enough to leave a groove around it and raises the panel slightly. `alt`
    recolours some slot-0 panels with that material slot for a patchwork
    plate look. Rivets are off by default; with `rivet_step` set they line
    the panel edges only where `rivets_where(centre, normal)` is true, so a
    part can carry a single bolted row where it shows.
    """
    rnd = random.Random(seed)
    # merge near-flat facets first so panels come out rectangular, not triangular
    bmesh.ops.dissolve_limit(bm, angle_limit=R(4), verts=bm.verts[:], edges=bm.edges[:],
                             delimit={'MATERIAL'})
    for axis, cuts in (((1, 0, 0), cuts_x), ((0, 1, 0), cuts_y), ((0, 0, 1), cuts_z)):
        for c in cuts:
            geom = bm.verts[:] + bm.edges[:] + bm.faces[:]
            bmesh.ops.bisect_plane(bm, geom=geom, plane_co=Vector(axis) * c,
                                   plane_no=Vector(axis), dist=1e-4)
    bm.normal_update()
    faces = [f for f in bm.faces
             if f.normal.z > -0.5 and f.calc_area() / max(f.calc_perimeter(), 1e-6) > min_width]
    bmesh.ops.inset_individual(bm, faces=faces, thickness=groove, depth=0.0,
                               use_even_offset=True)
    bmesh.ops.inset_individual(bm, faces=faces, thickness=0.004, depth=lift,
                               use_even_offset=True)
    bm.normal_update()
    rivets = bmesh.new()
    for f in faces:
        if alt is not None and f.material_index == 0 and rnd.random() < alt_share:
            f.material_index = alt
        if not rivet_step:
            continue
        c = f.calc_center_median()
        n = f.normal.copy()
        if n.z < -0.3 or (rivets_where and not rivets_where(c, n)):
            continue
        vs = [v.co.copy() for v in f.verts]
        for a, b in zip(vs, vs[1:] + vs[:1]):
            d = b - a
            length = d.length
            count = int(length / rivet_step)
            if length < 0.15 or count < 1:
                continue
            d.normalize()
            inward = n.cross(d).normalized()
            if inward.dot(c - (a + b) / 2) < 0:
                inward = -inward
            for k in range(count):
                p = a + d * length * (k + 0.5) / count + inward * rivet_inset + n * 0.003
                add_rivet(rivets, orient(p, n))
    return rivets


def bm_tube(pts, r, segs=12, joints=True):
    """Tube along a polyline with ball joints at the bends (rails, frames, pipes)."""
    out = bmesh.new()
    pts = [Vector(p) for p in pts]
    for a, b in zip(pts, pts[1:]):
        d = b - a
        bm_append(out, bm_cyl(r, r, d.length, segs, orient((a + b) / 2, d)))
    if joints:
        for p in pts[1:-1]:
            bm_append(out, bm_sphere(r * 1.04, T(*p), segs, 6))
    return out


def bm_spring(mat, coil_r, wire_r, length, turns, per_turn=24, ring=6):
    """Helical coil spring along local Z, centred on the origin of `mat`."""
    bm = bmesh.new()
    rings = []
    n = int(turns * per_turn)
    for i in range(n + 1):
        t = i / n
        a = 2 * math.pi * turns * t
        centre = Vector((coil_r * math.cos(a), coil_r * math.sin(a), -length / 2 + length * t))
        tangent = Vector((-coil_r * math.sin(a) * 2 * math.pi * turns,
                          coil_r * math.cos(a) * 2 * math.pi * turns, length)).normalized()
        radial = Vector((math.cos(a), math.sin(a), 0))
        binorm = tangent.cross(radial).normalized()
        rings.append([bm.verts.new(mat @ (centre + (radial * math.cos(b) + binorm * math.sin(b)) * wire_r))
                      for b in (2 * math.pi * j / ring for j in range(ring))])
    for r0, r1 in zip(rings, rings[1:]):
        for j in range(ring):
            bm.faces.new((r0[j], r0[(j + 1) % ring], r1[(j + 1) % ring], r1[j]))
    bm.faces.new(rings[0][::-1])
    bm.faces.new(rings[-1])
    return bm


def louvre(size, mat, slats, slat_depth=0.03):
    """Recessed vent: a frame box (slot 0) with `slats` angled blades (slot 1) on its -Y face."""
    sx, sy, sz = size
    out = bm_merge((bm_box(size, mat), 0))
    for i in range(slats):
        z = -sz / 2 + sz * (i + 0.5) / slats
        bm_append(out, bm_box((sx * 0.88, slat_depth, sz / slats * 0.55),
                              mat @ T(0, -sy / 2 - slat_depth / 2, z) @ Rx(-25)), 1)
    return out


def grille(w, h, bars, mat, depth=0.03, bar=0.014):
    """Flat grille on local XY (Z out): frame and bars (slot 0) over a dark backing (slot 1)."""
    out = bmesh.new()
    t = 0.03
    for sx, sy, x, y in ((w, t, 0, h / 2 - t / 2), (w, t, 0, -h / 2 + t / 2),
                         (t, h - 2 * t, w / 2 - t / 2, 0), (t, h - 2 * t, -w / 2 + t / 2, 0)):
        bm_append(out, bm_box((sx, sy, depth), mat @ T(x, y, depth / 2)), 0)
    bm_append(out, bm_box((w - 2 * t, h - 2 * t, 0.006), mat @ T(0, 0, 0.003)), 1)
    for k in range(bars):
        x = -w / 2 + t + (w - 2 * t) * (k + 0.5) / bars
        bm_append(out, bm_box((bar, h - 2 * t, depth * 0.8), mat @ T(x, 0, depth * 0.4)), 0)
    return out


def greebles(mat, w, h, seed, n=8, hmax=0.05, hmin=0.012):
    """Scatter of small machined blocks, caps and pipe stubs on local XY (Z out).

    Slot 0 is the body colour, slot 1 dark metal. Deterministic per seed.
    """
    rnd = random.Random(seed)
    out = bmesh.new()
    placed = []
    for _ in range(n * 25):
        if len(placed) >= n:
            break
        bw = rnd.uniform(0.05, max(0.06, w * 0.35))
        bh = rnd.uniform(0.04, max(0.05, h * 0.45))
        x = rnd.uniform(-w / 2 + bw / 2, w / 2 - bw / 2)
        y = rnd.uniform(-h / 2 + bh / 2, h / 2 - bh / 2)
        if any(abs(x - px) < (bw + pw) / 2 + 0.015 and abs(y - py) < (bh + ph) / 2 + 0.015
               for px, py, pw, ph in placed):
            continue
        placed.append((x, y, bw, bh))
        d = rnd.uniform(hmin, hmax)
        kind = rnd.random()
        m = mat @ T(x, y, 0)
        if kind < 0.45:
            bm_append(out, bm_box((bw, bh, d), m @ T(0, 0, d / 2)), rnd.choice((0, 0, 1)))
        elif kind < 0.7:
            bm_append(out, bm_box((bw, bh, d), m @ T(0, 0, d / 2)), 0)
            bm_append(out, bm_box((bw * 0.6, bh * 0.5, d * 0.5), m @ T(0, 0, d * 1.25)), 1)
        elif kind < 0.85:
            r = min(bw, bh) / 2
            bm_append(out, bm_cyl(r, r * 0.85, d, 16, m @ T(0, 0, d / 2)), 1)
            bm_append(out, bm_cyl(r * 0.4, r * 0.4, d * 0.4, 10, m @ T(0, 0, d * 1.2)), 0)
        else:
            r = min(bh, 0.05) / 2
            bm_append(out, bm_cyl(r, r, bw, 12, m @ T(0, 0, r) @ Ry(90)), 1)
            for sx in (-1, 1):
                bm_append(out, bm_box((0.02, r * 2.6, r * 2.2), m @ T(sx * bw * 0.35, 0, r)), 0)
    return out


def applique(quad, inside, t=0.045, shrink=0.10, bolts=True, sink=0.008):
    """Bolt-on armor plate lying on the (roughly planar) face spanned by `quad`.

    Returns (plate bmesh, bolt bmesh). `inside` is any point inside the part,
    used to point the plate outward. The plate is sunk `sink` into the face
    so it never floats where the face is not perfectly planar.
    """
    pts = [Vector(p) for p in quad]
    c = sum(pts, Vector()) / len(pts)
    n = (pts[2] - pts[0]).cross(pts[3] - pts[1]).normalized()
    if n.dot(c - Vector(inside)) < 0:
        n = -n
    base = [c + (p - c) * (1 - shrink) - n * sink for p in pts]
    top = [c + (p - c) * (1 - shrink - 0.05) + n * t for p in pts]
    plate = bm_hull([tuple(p) for p in base + top])
    bolts_bm = bmesh.new()
    if bolts:
        for p in top:
            q = c + (p - c) * 0.88
            add_rivet(bolts_bm, orient(q + n * 0.002, n))
    return plate, bolts_bm


def cyl_y(r1, r2, depth, segs, x, y, z, spin=0):
    """Cylinder along +Y; r1 at the rear end, r2 at the front end."""
    return bm_cyl(r1, r2, depth, segs, T(x, y, z) @ Rx(-90) @ Rz(spin))


def cyl_x(r1, r2, depth, segs, x, y, z):
    """Cylinder along +X; r1 at the -X end."""
    return bm_cyl(r1, r2, depth, segs, T(x, y, z) @ Ry(90))


def two_tone(bm, below_z, slot=1):
    """Faces under `below_z` take material `slot` (running-gear gray)."""
    for f in bm.faces:
        if f.calc_center_median().z < below_z:
            f.material_index = slot
    return bm


def on_plane(p, n, up=(0, 0, 1)):
    """Matrix at `p` with local Z along normal `n` and local Y as close to `up` as it gets."""
    n = Vector(n).normalized()
    y = (Vector(up) - n * n.dot(Vector(up)))
    y = y.normalized() if y.length > 1e-6 else Vector((0, 1, 0))
    x = y.cross(n)
    m = Matrix((x, y, n)).transposed().to_4x4()
    return T(*p) @ m


# -------------------------------------------------------------- dimensions

BELLY = 0.45
DECK = 1.80
DECK_FRONT = 0.55                         # where the deck breaks into the glacis
HULL_FRONT_Y, HULL_FRONT_Z = 1.95, 1.30   # top of the recessed hull front face
GLACIS_SLOPE = (DECK - HULL_FRONT_Z) / (HULL_FRONT_Y - DECK_FRONT)
HULL_X = 1.16                             # hull side wall, the inner side of each gutter
REAR_Y = -3.15


def glacis_z(y):
    return DECK - (y - DECK_FRONT) * GLACIS_SLOPE


# Centre hull between the walls: flat belly, vertical sides and rear, flat
# deck, short glacis, then a vertical front face set well back from the prows.
HULL = sym(
    (1.10, REAR_Y, BELLY), (1.10, 1.80, BELLY),
    (HULL_X, REAR_Y, 0.55), (HULL_X, HULL_FRONT_Y, 0.55),
    (HULL_X, REAR_Y, DECK), (HULL_X, DECK_FRONT, DECK),
    (HULL_X, HULL_FRONT_Y, HULL_FRONT_Z),
)

# Side wall (right side; mirrored): a thin plate bent along a chine. Both
# facets lean outward going up, the lower one more, so the pair reads as a V
# from the front. The prow is a wedge: the top edge falls from TOP_BREAK_Y,
# the bottom edge rises from BOT_BREAK_Y, and they meet in a short blunt tip.
WALL_T = 0.14
WALL_BOT, WALL_CHINE, WALL_TOP = 0.40, 1.05, 1.85
WALL_X_BOT, WALL_X_CHINE, WALL_X_TOP = 1.30, 1.60, 1.80
WALL_REAR = -3.15
TIP_Y, TIP_TOP, TIP_BOT = 3.60, 1.05, 0.80
TOP_BREAK_Y, BOT_BREAK_Y = 1.50, 1.20
UP_DEG = math.degrees(math.atan2(WALL_X_TOP - WALL_X_CHINE, WALL_TOP - WALL_CHINE))
LO_DEG = math.degrees(math.atan2(WALL_X_CHINE - WALL_X_BOT, WALL_CHINE - WALL_BOT))
WALL_UP = [(WALL_REAR, WALL_CHINE), (WALL_REAR, WALL_TOP), (TOP_BREAK_Y, WALL_TOP), (TIP_Y, TIP_TOP)]
WALL_LO = [(WALL_REAR + 0.10, WALL_BOT), (WALL_REAR, WALL_CHINE), (TIP_Y, WALL_CHINE), (TIP_Y, TIP_BOT),
           (BOT_BREAK_Y, WALL_BOT)]


def wall_x(z):
    """Outer face of the right wall at height z."""
    if z <= WALL_CHINE:
        return WALL_X_BOT + (z - WALL_BOT) * (WALL_X_CHINE - WALL_X_BOT) / (WALL_CHINE - WALL_BOT)
    return WALL_X_CHINE + (z - WALL_CHINE) * (WALL_X_TOP - WALL_X_CHINE) / (WALL_TOP - WALL_CHINE)


def wall_in_x(z):
    return wall_x(z) - WALL_T


def wall_top_z(y):
    if y <= TOP_BREAK_Y:
        return WALL_TOP
    return WALL_TOP - (y - TOP_BREAK_Y) * (WALL_TOP - TIP_TOP) / (TIP_Y - TOP_BREAK_Y)


def wall_bot_z(y):
    if y <= BOT_BREAK_Y:
        return WALL_BOT
    return WALL_BOT + (y - BOT_BREAK_Y) * (TIP_BOT - WALL_BOT) / (TIP_Y - BOT_BREAK_Y)


def wall_n(z, s, inner=False):
    """Outward (or inward) normal of the wall facet at height z."""
    a = R(UP_DEG if z > WALL_CHINE else LO_DEG)
    n = Vector((s * math.cos(a), 0, -math.sin(a)))
    return -n if inner else n


def wall_plate(poly, s, grow=0.0):
    """Prism of a wall facet: the (y, z) polygon pushed onto the leaning face."""
    c = Vector((sum(p[0] for p in poly) / len(poly), sum(p[1] for p in poly) / len(poly)))
    pts = []
    for y, z in poly:
        if grow:
            d = Vector((y, z)) - c
            y, z = y + d.x * grow, z + d.y * grow
        pts += [(s * (wall_x(z) + grow * 0.4), y, z), (s * (wall_in_x(z) - grow * 0.4), y, z)]
    return bm_hull(pts)


def on_wall(y, z, s, inner=False):
    """Matrix on a wall face: local Z out of the face, local Y up the facet, local X along the hull."""
    x = wall_in_x(z) if inner else wall_x(z)
    n = wall_n(z, s, inner)
    return on_plane((s * x, y, z), n)


# Driver's brow: broad block on the glacis, long window on its sloped front.
BROW_TOP = 2.00
BROW = sym(
    (0.60, 0.65, BROW_TOP), (0.60, 1.25, BROW_TOP),
    (0.65, 1.45, 1.60), (0.65, 1.52, 1.45), (0.65, 0.65, 1.76),
)
BROW_FRONT_DEG = math.degrees(math.atan2(1.45 - 1.25, BROW_TOP - 1.60))
DRIVER_X = -0.30

# Armor arm (right; mirrored): a wide flat plate springing from under the brow
# front and running forward, outward and down to a lens cluster near the
# wall's prow, cantilevered over the hollow nose.
ARM_Y0, ARM_Y1 = 1.40, 3.25
ARM_IN = (0.28, 1.00)                    # inner edge x, back and front
ARM_OUT = (0.78, 1.46)
ARM_TOP = (1.72, 1.22)
ARM_BOT = (1.45, 0.90)


def arm_t(y):
    return (y - ARM_Y0) / (ARM_Y1 - ARM_Y0)


def lerp2(v, t):
    return v[0] + (v[1] - v[0]) * t


def arm_pt(y, u, w=1.0):
    """Point on the right arm: u across (0 inner .. 1 outer), w down (1 top .. 0 bottom)."""
    t = arm_t(y)
    x = lerp2(ARM_IN, t) + (lerp2(ARM_OUT, t) - lerp2(ARM_IN, t)) * u
    z = lerp2(ARM_BOT, t) + (lerp2(ARM_TOP, t) - lerp2(ARM_BOT, t)) * w
    return (x, y, z)


ARM = [arm_pt(y, u, w) for y in (ARM_Y0, ARM_Y1) for u in (0, 1) for w in (0, 1)]
LENS_X = (1.12, 1.34)                    # inner lens is the headlight
LENS_Z = 1.06

# Turret: plinth on the deck, two cheek blocks with the gun mount between
# them, a rear block, and the VLS pod on the right cheek.
T0 = Vector((0.0, -0.75, DECK))
TB, TT = 0.20, 0.70                      # turret body bottom and roof, turret-relative
REAR_BLOCK = sym((0.70, -1.02, TB), (0.70, -0.02, TB), (0.66, -1.10, TB + 0.24),
                 (0.60, -1.00, TT), (0.60, -0.02, TT))
CHEEK = [(0.24, -0.06, TB), (0.70, -0.06, TB), (0.24, 0.66, TB), (0.70, 0.58, TB),
         (0.24, -0.06, TT), (0.60, -0.06, TT), (0.24, 0.46, TT), (0.56, 0.42, TT),
         (0.24, 0.64, 0.46), (0.66, 0.56, 0.44)]
G0 = T0 + Vector((0.0, 0.40, 0.44))      # gun elevation pivot
BARREL_LEN = 3.42
MUZZLE_Y = G0.y + BARREL_LEN
POD = ((-1.04, -0.70), (-0.62, 0.44), (0.26, 0.88))  # VLS pod box (x, y, z ranges), turret-relative, left side
VLS_TOP = POD[2][1]
VLS_CELLS = [(cx, cy) for cy in (-0.48, -0.22, 0.04, 0.30) for cx in (-0.80, -0.94)]
VLS_CELL = 0.12

# Segmented transverse engine drum on end brackets.
DRUM = Vector((0.0, -2.80, 2.28))
DRUM_CORE, DRUM_R = 0.40, 0.47
DRUM_SEGS = ((0.42, 0.72), (0.78, 1.08))           # |x| ranges of the big segments
DRUM_CAP = (1.12, 1.22)
EXHAUST_X, EXHAUST_Z = 0.57, 2.14

FLOOR = 0.53
PAN = 0.98                                # passenger seat height
FRONT_PAN = 1.10                          # driver and front passenger sit higher, under the brow
CARGO_Y = (-2.70, -2.10, -1.50, -0.90, -0.30, 0.30)
CARGO_X = 0.84
FRONT_Y = 1.05
RAMP_W, RAMP_TOP = 0.58, 1.60
# (x, y, z, size_x, size_y): 3 pads under the belly, 3 strips under each wall foot
REPULSORS = ([(0.0, y, 0.42, 1.70, 1.25) for y in (-2.00, -0.25, 1.30)]
             + [(s * 1.23, y, 0.37, 0.16, 1.10) for s in (1, -1) for y in (-2.30, -0.80, 0.60)])


def tp(pts):
    """Turret-relative points to world."""
    return [tuple(Vector(p) + T0) for p in pts]


def drum_x(x, r, depth, segs=64):
    """Cylinder segment of the engine drum, axis along X."""
    return cyl_x(r, r, depth, segs, x, DRUM.y, DRUM.z)


# ------------------------------------------------------------------- build

def build(livery=LIVERY):
    clear_scene()
    scn = bpy.context.scene
    scn.unit_settings.system = 'METRIC'
    scn.unit_settings.scale_length = 1.0

    root = coll("MSE_v2")
    vis = coll("LOD_Resolution_0", root)
    c_hull = coll("Hull", vis)
    c_wall = coll("Side_Walls", vis)
    c_front = coll("Front_Armor", vis)
    c_det = coll("Hull_Details", vis)
    c_rear = coll("Rear_Ramp", vis)
    c_eng = coll("Engine_Drum", vis)
    c_rep = coll("Repulsors", vis)
    c_tur = coll("Turret", vis)
    c_gun = coll("Gun", vis)
    c_vls = coll("VLS_Rockets", vis)
    c_int = coll("Interior_Seats", vis)
    c_geo = coll("LOD_Geometry", root)
    c_mem = coll("LOD_Memory", root)
    c_crew = coll("Crew_Positions", root)
    coll("LOD_FireGeometry_TODO", root)
    coll("LOD_ViewGeometry_TODO", root)

    # one light armor gray all over, like the reference; mechanicals darker
    paint = material("armor_gray", (0.62, 0.63, 0.64), rough=0.55)
    paint_alt = material("armor_gray_alt", (0.54, 0.55, 0.565), rough=0.6)
    inner = material("armor_gray_inner", (0.42, 0.43, 0.44), rough=0.6)
    gray = material("machinery_gray", (0.26, 0.27, 0.28), rough=0.55)
    panel = material("panel_gray", (0.48, 0.49, 0.50), rough=0.55)
    dark = material("dark_metal", (0.06, 0.065, 0.07), rough=0.4, metal=0.7)
    steel = material("steel", (0.32, 0.32, 0.33), rough=0.35, metal=0.8)
    accent = material(f"legion_{livery}", LIVERIES[livery], rough=0.5)
    glass = material("glass", (0.02, 0.06, 0.12), rough=0.06, metal=0.4)
    glow = material("repulsor_glow", (0.1, 0.3, 0.5), emit=(0.35, 0.75, 1.0), strength=6.0)
    thrust = material("thruster_glow", (0.1, 0.2, 0.5), emit=(0.45, 0.6, 1.0), strength=10.0)
    lamp = material("headlight", (0.85, 0.9, 1.0), emit=(0.85, 0.92, 1.0), strength=5.0)
    tail = material("taillight", (0.5, 0.02, 0.02), emit=(1.0, 0.08, 0.05), strength=4.0)
    seat_m = material("seat", (0.16, 0.16, 0.14), rough=0.8)
    DETAIL["rivet"] = steel

    sides = ((1, "r"), (-1, "l"))

    # ================================================================ HULL
    make("hull", bm_hull(HULL), [paint, paint_alt], c_hull, groups=["hull"], bevel=0.03, bevel_segs=2,
         panels=dict(cuts_x=(-0.55, 0.0, 0.55), cuts_y=(-2.45, -1.60, -0.30, 0.55, 1.30),
                     cuts_z=(1.10,), alt=1, seed=11))

    # ================================================================ SIDE WALLS
    for s, side in sides:
        make(f"wall_upper_{side}", wall_plate(WALL_UP, s), [paint, paint_alt], c_wall, groups=["hull"],
             bevel=0.018, bevel_segs=2,
             panels=dict(cuts_y=(-2.10, -1.05, 0.0, 1.05, 2.10), cuts_z=(1.47,), alt=1, seed=3 if s > 0 else 4,
                         rivet_step=0.42, rivet_inset=0.04,
                         rivets_where=lambda c, n, s=s: n.x * s > 0.8 and c.z > 1.1))
        make(f"wall_lower_{side}", wall_plate(WALL_LO, s), [paint, paint_alt], c_wall, groups=["hull"],
             bevel=0.018, bevel_segs=2,
             panels=dict(cuts_y=(-2.10, -1.05, 0.0, 1.05, 2.10), cuts_z=(0.72,), alt=1, seed=5 if s > 0 else 6))
        # capping rail along the top edge, and a darker ram cap on the prow
        cap = bmesh.new()
        for y0, y1 in ((WALL_REAR, TOP_BREAK_Y), (TOP_BREAK_Y, TIP_Y - 0.05)):
            pts = []
            for y in (y0, y1):
                z = wall_top_z(y)
                pts += [(s * (wall_in_x(z) - 0.02), y, z - 0.03), (s * (wall_x(z) + 0.02), y, z - 0.03),
                        (s * (wall_in_x(z) - 0.01), y, z + 0.03), (s * (wall_x(z) + 0.01), y, z + 0.03)]
            bm_append(cap, bm_hull(pts))
        make(f"wall_top_rail_{side}", cap, panel, c_wall, groups=["hull"], bevel=0.008)
        tip_up = [(3.05, WALL_CHINE), (3.05, wall_top_z(3.05)), (TIP_Y, TIP_TOP)]
        tip_lo = [(3.05, WALL_CHINE), (TIP_Y, WALL_CHINE), (TIP_Y, TIP_BOT), (3.05, wall_bot_z(3.05))]
        ram = bm_merge((wall_plate(tip_up, s, grow=0.05), 0), (wall_plate(tip_lo, s, grow=0.05), 0))
        make(f"wall_ram_cap_{side}", ram, [gray], c_wall, groups=["hull"], bevel=0.01)

        # outer face: a recessed access hatch, boarding rungs, a vent plate, marker lights
        det = bmesh.new()
        m = on_wall(1.05, 1.62, s)
        bm_append(det, bm_box((0.46, 0.26, 0.012), m @ T(0, 0, 0.006)), 1)
        for x_, y_, w_, h_ in ((0, 0.14, 0.50, 0.03), (0, -0.14, 0.50, 0.03), (0.24, 0, 0.03, 0.28), (-0.24, 0, 0.03, 0.28)):
            bm_append(det, bm_box((w_, h_, 0.025), m @ T(x_, y_, 0.0125)), 0)
        bm_append(det, bm_tube([m @ Vector((-0.07, -0.05, 0.012)), m @ Vector((-0.07, -0.05, 0.04)),
                                m @ Vector((0.07, -0.05, 0.04)), m @ Vector((0.07, -0.05, 0.012))], 0.008, 8), 2)
        m = on_wall(-0.55, 1.25, s)
        bm_append(det, bm_box((0.26, 0.30, 0.02), m @ T(0, 0, 0.01)), 0)
        for k in range(5):
            bm_append(det, bm_box((0.22, 0.02, 0.012), m @ T(0, -0.11 + k * 0.055, 0.026)), 1)
        m = on_wall(-2.60, 1.60, s)                       # second access hatch near the rear
        bm_append(det, bm_box((0.36, 0.24, 0.012), m @ T(0, 0, 0.006)), 1)
        for x_, y_, w_, h_ in ((0, 0.13, 0.40, 0.03), (0, -0.13, 0.40, 0.03), (0.19, 0, 0.03, 0.26), (-0.19, 0, 0.03, 0.26)):
            bm_append(det, bm_box((w_, h_, 0.025), m @ T(x_, y_, 0.0125)), 0)
        m = on_wall(3.30, 1.02, s)
        bm_append(det, bm_box((0.10, 0.05, 0.03), m @ T(0, 0, 0.015)), 1)
        for y, z, w_, h_ in ((2.05, 1.52, 0.30, 0.18), (2.55, 1.38, 0.22, 0.12)):   # small plates on the prow
            m = on_wall(y, z, s)
            bm_append(det, bm_box((w_, h_, 0.025), m @ T(0, 0, 0.0125)), 0)
            for sx in (-1, 1):
                add_rivet(det, m @ T(sx * (w_ / 2 - 0.03), 0, 0.028))
        make(f"wall_details_{side}", det, [panel, dark, steel], c_det, groups=["hull"])
        make(f"wall_marker_{side}", bm_box((0.07, 0.03, 0.012), on_wall(3.30, 1.02, s) @ T(0, 0, 0.034)),
             lamp, c_det, groups=["hull"])
        # inner faces in the open nose: brackets and conduits (seen from the front)
        make(f"wall_inner_greebles_{side}", bm_merge(
            (greebles(on_wall(2.45, 0.80, s, inner=True), 0.80, 0.24, 81 + s, n=7, hmax=0.05), None),
            (greebles(on_wall(2.35, 1.22, s, inner=True), 0.70, 0.22, 91 + s, n=6, hmax=0.05), None)),
             [gray, dark], c_det, groups=["hull"])
        # inner faces along the gutters: bracket plates and boxes (seen from above)
        make(f"wall_gutter_greebles_{side}", bm_merge(
            *[(greebles(on_wall(y, 1.55, s, inner=True), 0.95, 0.30, 140 + k * 3 + s, n=6, hmax=0.04), None)
              for k, y in enumerate((-2.55, -1.40, -0.25, 0.85))]),
             [gray, dark], c_det, groups=["hull"])
        # rear edge: tail light and a small vent
        make(f"taillight_housing_{side}", bm_box((0.16, 0.04, 0.12), T(s * 1.63, WALL_REAR - 0.02, 1.55)),
             dark, c_rear, groups=["hull"])
        make(f"taillight_{side}", bm_box((0.11, 0.02, 0.06), T(s * 1.63, WALL_REAR - 0.045, 1.55)),
             tail, c_rear, groups=[f"taillight_{side}"])

        # ---- gutter between wall and hull: braces, conduits, clamps
        gut = bmesh.new()
        for y in (-2.60, -1.40, -0.20, 0.90):
            x1 = wall_in_x(1.48) + 0.02
            bm_append(gut, bm_box((x1 - HULL_X + 0.02, 0.10, 0.12), T(s * (HULL_X + x1) / 2, y, 1.48)), 0)
            bm_append(gut, bm_box((0.05, 0.16, 0.18), T(s * (HULL_X + 0.025), y, 1.48)), 0)
            for dz in (-0.04, 0.04):
                add_rivet(gut, orient((s * (HULL_X + 0.052), y + 0.05, 1.48 + dz), (s, 0, 0)))
        for x, z, r in ((HULL_X + 0.05, 1.28, 0.035), (HULL_X + 0.04, 1.12, 0.025)):
            bm_append(gut, cyl_y(r, r, 3.95, 16, s * x, -1.10, z), 1)
        for y in (-3.00, -2.00, -0.80, 0.40):
            bm_append(gut, bm_box((0.06, 0.05, 0.24), T(s * (HULL_X + 0.03), y, 1.20)), 2)
        for y in (-2.00, -0.80, 0.35):
            bm_append(gut, greebles(on_plane((s * HULL_X, y, 1.62), (s, 0, 0)), 0.80, 0.18, 120 + int(y * 10) + s,
                                    n=4, hmax=0.04), None)
        make(f"gutter_{side}", gut, [gray, dark, steel], c_det, groups=["hull"])

        # ---- coil-spring dampers on the deck beside the turret (reference's twin springs)
        for i, (y0, y1) in enumerate(((-2.10, -1.55), (-1.45, -0.90))):
            p = (s * 1.00, (y0 + y1) / 2, 1.865)
            ln = y1 - y0
            make(f"deck_damper_{side}_{i + 1}", bm_merge(
                (bm_spring(T(*p) @ Rx(-90), 0.055, 0.012, ln - 0.10, 4), 0),
                (cyl_y(0.02, 0.02, ln, 12, *p), 1),
                *[(cyl_y(0.07, 0.07, 0.04, 24, p[0], p[1] + dy, p[2]), 2) for dy in (-ln / 2, ln / 2)],
                *[(bm_box((0.12, 0.06, 0.07), T(p[0], p[1] + dy, 1.835)), 2) for dy in (-ln / 2, ln / 2)]),
                [dark, steel, gray], c_det, groups=["hull"])

    # ================================================================ BROW
    make("brow", bm_hull(BROW), [paint, paint_alt], c_front, groups=["hull"], bevel=0.03, bevel_segs=2,
         panels=dict(cuts_x=(-0.30, 0.30), cuts_y=(0.95,), alt=1, seed=5))
    zw = 1.82
    m = T(0, 1.25 + (BROW_TOP - zw) * math.tan(R(BROW_FRONT_DEG)), zw) @ Rx(BROW_FRONT_DEG)
    win = bm_merge(
        (bm_box((0.92, 0.06, 0.16), m @ T(0, 0.0, 0)), 0),                 # dark frame
        (bm_box((0.84, 0.02, 0.10), m @ T(0, 0.025, 0)), 1),               # window
        (bm_box((0.98, 0.10, 0.025), m @ T(0, 0.03, 0.095)), 2),           # hood
        *[(bm_box((0.012, 0.03, 0.10), m @ T(x, 0.04, 0)), 0) for x in (-0.21, 0.0, 0.21)],
    )
    make("brow_window", win, [dark, glass, panel], c_front, groups=["hull", "glass"])
    # driver cupola with periscopes, round lid hinged at the rear
    hx, hy = DRIVER_X, 0.98
    ring = bm_merge((bm_cyl(0.20, 0.20, 0.05, 32, T(hx, hy, BROW_TOP + 0.02)), 0))
    for a in (-60, -30, 0, 30, 60):
        mm = T(hx, hy, BROW_TOP + 0.07) @ Rz(a) @ T(0, 0.16, 0)
        bm_append(ring, bm_box((0.08, 0.06, 0.05), mm), 0)
        bm_append(ring, bm_box((0.055, 0.01, 0.025), mm @ T(0, 0.031, 0)), 1)
    make("driver_cupola", ring, [panel, glass], c_front, groups=["hull"])
    lid = bm_merge(
        (bm_cyl(0.14, 0.14, 0.035, 32, T(hx, hy, BROW_TOP + 0.062)), 0),
        (bm_cyl(0.08, 0.08, 0.02, 24, T(hx, hy, BROW_TOP + 0.088)), 0),
        (bm_tube([(hx - 0.05, hy + 0.03, BROW_TOP + 0.09), (hx - 0.05, hy + 0.03, BROW_TOP + 0.12),
                  (hx + 0.05, hy + 0.03, BROW_TOP + 0.12), (hx + 0.05, hy + 0.03, BROW_TOP + 0.09)], 0.01, 8), 1),
        (cyl_x(0.02, 0.02, 0.18, 12, hx, hy - 0.14, BROW_TOP + 0.06), 1),
    )
    make("hatch_driver", lid, [panel, dark], c_front, origin=(hx, hy - 0.14, BROW_TOP + 0.06),
         groups=["hatch_driver"])
    for s in (1, -1):
        make(f"brow_side_greebles_{'r' if s > 0 else 'l'}",
             greebles(on_plane((s * 0.625, 1.0, 1.86), (s, 0, 0.32), up=(0, 0, 1)), 0.50, 0.16, 150 + s, n=4, hmax=0.03),
             [panel, dark], c_front, groups=["hull"])
    make("brow_top_greebles", greebles(T(-DRIVER_X, 0.95, BROW_TOP), 0.40, 0.42, 7, n=6, hmax=0.05),
         [panel, dark], c_front, groups=["hull"])
    # boxed lights at the brow's outer corners (reference's corner lamps)
    corner = bmesh.new()
    lens_c = bmesh.new()
    for x in (-0.90, 0.90):
        z0 = glacis_z(1.05)
        bm_append(corner, bm_box((0.20, 0.20, 0.16), T(x, 1.05, z0 + 0.07)), 0)
        bm_append(corner, bm_box((0.22, 0.06, 0.03), T(x, 1.13, z0 + 0.16)), 1)
        bm_append(corner, cyl_y(0.055, 0.055, 0.04, 24, x, 1.16, z0 + 0.08), 1)
        bm_append(lens_c, cyl_y(0.045, 0.045, 0.01, 24, x, 1.18, z0 + 0.08))
    make("corner_lights", corner, [panel, dark], c_front, groups=["hull"], bevel=0.0)
    make("corner_light_lenses", lens_c, glass, c_front, groups=["hull", "glass"])

    # ================================================================ ARMS
    for s, side in sides:
        make(f"armor_arm_{side}", bm_hull(mirror(ARM, s)), [paint, paint_alt], c_front, groups=["hull"],
             bevel=0.025, bevel_segs=2,
             panels=dict(cuts_y=(1.95, 2.55), alt=1, seed=7 if s > 0 else 8, rivet_step=0.20,
                         rivets_where=lambda c, n: n.z > 0.6))
        # layered plates on top: a raised strip along the inner edge and a legion plate outboard
        strip = []
        for y in (ARM_Y0 + 0.10, ARM_Y1 - 0.08):
            for u in (0.03, 0.30):
                x, _, z = arm_pt(y, u)
                strip += [(s * x, y, z - 0.01), (s * x, y, z + 0.06)]
        make(f"arm_strip_{side}", bm_hull(strip), [panel], c_front, groups=["hull"], bevel=0.012)
        plate, bolts = applique(mirror([arm_pt(1.85, 0.40), arm_pt(2.90, 0.40), arm_pt(2.90, 0.94),
                                        arm_pt(1.85, 0.94)], s), (s * 0.8, 2.3, 1.2), t=0.03, shrink=0.05)
        bm_append(bolts, plate, 1)
        make(f"arm_plate_{side}", bolts, [steel, panel], c_front, groups=["hull"])
        p0, p1, p2 = (Vector(arm_pt(y, u)) for y, u in ((ARM_Y0, 0), (ARM_Y0, 1), (ARM_Y1, 0)))
        an = (p1 - p0).cross(p2 - p0).normalized()
        an = an if an.z > 0 else -an
        an.x *= s
        ag = bmesh.new()
        for y, u, w_, h_, seed in ((1.62, 0.66, 0.24, 0.30, 1), (3.05, 0.66, 0.16, 0.30, 2), (2.38, 0.17, 0.55, 0.10, 3)):
            x, _, z = arm_pt(y, u)
            bm_append(ag, greebles(on_plane((s * x, y, z + 0.005), an, up=(0, 1, 0)), h_, w_, 100 + seed * 7 + s,
                                   n=4, hmax=0.035), None)
        make(f"arm_greebles_{side}", ag, [panel, dark], c_det, groups=["hull"])
        # vents on the outer flank
        x0, y0, z0 = arm_pt(2.40, 1.0, 0.5)
        d = (Vector(arm_pt(2.90, 1.0, 0.5)) - Vector(arm_pt(1.90, 1.0, 0.5))).normalized()
        d.x *= s
        n_ = Vector((s * 1.0, -0.35, 0)).normalized()
        n_ = (n_ - d * n_.dot(d)).normalized()
        up = n_.cross(d) if n_.cross(d).z > 0 else d.cross(n_)
        make(f"arm_vents_{side}", grille(0.50, 0.14, 9, on_plane((s * x0 + s * 0.004, y0, z0), n_, up), depth=0.018),
             [gray, dark], c_det, groups=["hull"])
        # twin lens cluster under the arm's front edge
        cx_ = s * (LENS_X[0] + LENS_X[1]) / 2
        housing = bm_merge(
            (bm_box((0.42, 0.10, 0.20), T(cx_, ARM_Y1 - 0.02, LENS_Z)), 0),
            *[(cyl_y(0.085, 0.085, 0.04, 32, s * x, ARM_Y1 + 0.04, LENS_Z), 0) for x in LENS_X],
            *[(cyl_y(0.075, 0.075, 0.012, 32, s * x, ARM_Y1 + 0.066, LENS_Z), 1) for x in LENS_X],
            (bm_box((0.46, 0.08, 0.03), T(cx_, ARM_Y1 + 0.02, LENS_Z + 0.115)), 1),
        )
        make(f"lens_housing_{side}", housing, [dark, panel], c_front, groups=["hull"])
        make(f"light_{side}", cyl_y(0.062, 0.062, 0.02, 32, s * LENS_X[0], ARM_Y1 + 0.07, LENS_Z),
             lamp, c_front, groups=[f"light_{side}"])
        make(f"arm_sensor_{side}", bm_merge(
            (cyl_y(0.062, 0.062, 0.02, 32, s * LENS_X[1], ARM_Y1 + 0.07, LENS_Z), 0),
            (cyl_y(0.024, 0.024, 0.01, 16, s * LENS_X[1], ARM_Y1 + 0.083, LENS_Z), 1)),
             [glass, lamp], c_front, groups=["hull", "glass"])
        # stiffening ribs under the arm, seen from low in front
        ribs = bmesh.new()
        for y in (2.10, 2.35, 2.60, 2.85, 3.08):
            pts = []
            for u in (0.08, 0.92):
                x, _, z = arm_pt(y, u, 0.0)
                pts += [(s * x, y + dy, z + dz) for dy in (-0.025, 0.025) for dz in (0.01, -0.06)]
            bm_append(ribs, bm_hull(pts))
        make(f"arm_ribs_{side}", ribs, gray, c_det, groups=["hull"])
        # hydraulic ram from the hull front face up to the arm, and a pylon under the arm root
        a = Vector((s * 0.92, HULL_FRONT_Y + 0.02, 0.92))
        b = Vector(arm_pt(2.70, 0.35, 0.0)) * Vector((s, 1, 1)) - Vector((0, 0, 0.01))
        dv = b - a
        make(f"arm_ram_{side}", bm_merge(
            (bm_cyl(0.045, 0.045, dv.length * 0.55, 16, orient(a + dv * 0.275, dv)), 0),
            (bm_cyl(0.026, 0.026, dv.length * 0.5, 12, orient(a + dv * 0.75, dv)), 1),
            (bm_box((0.14, 0.06, 0.14), T(*(a - Vector((0, 0.01, 0))))), 2),
            (bm_box((0.12, 0.12, 0.05), T(*(b + Vector((0, 0, 0.01))))), 2)),
            [dark, steel, gray], c_det, groups=["hull"])

    # ================================================================ NOSE
    sc = Vector((0.0, 1.68, 1.47))                     # porthole sensor at the arms' apex
    make("nose_sensor_mount", bm_hull([(x, y, z) for x in (-0.25, 0.25) for y, z in
                                       ((1.40, 1.72), (1.66, 1.70), (1.66, 1.22), (1.40, 1.24))]),
         panel, c_front, groups=["hull"], bevel=0.04, bevel_segs=2)
    port = bm_merge(
        (cyl_y(0.21, 0.21, 0.05, 48, 0, sc.y, sc.z), 0),
        (cyl_y(0.185, 0.185, 0.03, 48, 0, sc.y + 0.035, sc.z), 1),
        *[(cyl_y(0.016, 0.016, 0.02, 8, 0.198 * math.cos(R(a)), sc.y + 0.03, sc.z + 0.198 * math.sin(R(a))), 1)
          for a in range(0, 360, 30)],
        *[(bm_box((0.08, 0.05, 0.08), T(sx * 0.20, sc.y + 0.005, sc.z + sz * 0.20)), 0)
          for sx in (-1, 1) for sz in (-1, 1)],                                  # rounded-square frame corners
    )
    make("nose_sensor", port, [dark, steel], c_front, groups=["hull"])
    make("nose_sensor_lens", cyl_y(0.17, 0.17, 0.02, 48, 0, sc.y + 0.055, sc.z), glass, c_front,
         groups=["hull", "glass"])
    make("nose_band", bm_merge(
        (bm_box((0.62, 0.10, 0.03), T(0, 1.43, 1.73)), 0),
        *[(bm_box((0.04, 0.105, 0.02), T(x, 1.435, 1.73)), 1) for x in (-0.22, 0.0, 0.22)]),
        [panel, dark], c_front, groups=["hull"])
    keel = bm_hull([(x, y, z) for x in (-0.085, 0.085) for y, z in
                    ((1.70, 1.30), (2.42, 1.10), (2.56, 0.90), (2.46, 0.52), (1.90, 0.50))])
    make("nose_keel", keel, [paint], c_front, groups=["hull"], bevel=0.015,
         panels=dict(cuts_y=(2.15,), seed=19))
    make("nose_keel_detail", bm_merge(
        *[(bm_box((0.18, 0.04, 0.10), T(0, y, z)), 0) for y, z in ((2.20, 0.75), (2.38, 0.95))],
        (bm_box((0.175, 0.30, 0.03), T(0, 2.10, 1.18) @ Rx(-16)), 1),
        (bm_tube([(0.09, 2.30, 0.62), (0.15, 2.30, 0.62), (0.15, 2.40, 0.62), (0.09, 2.40, 0.62)], 0.014, 8), 1),
        (bm_tube([(-0.09, 2.30, 0.62), (-0.15, 2.30, 0.62), (-0.15, 2.40, 0.62), (-0.09, 2.40, 0.62)], 0.014, 8), 1)),
        [gray, dark], c_front, groups=["hull"])
    # hull front face, recessed in the hollow nose: grilles, machinery, tow eyes
    front = bmesh.new()
    fn = Vector((0, 1, 0))
    for x in (-0.55, 0.55):
        bm_append(front, grille(0.44, 0.34, 9, on_plane((x, HULL_FRONT_Y, 0.98), fn), depth=0.03), None)
    for x in (-0.95, 0.95):
        bm_append(front, bm_box((0.14, 0.10, 0.12), T(x, HULL_FRONT_Y + 0.05, 0.64)), 0)
        bm_append(front, bm_tube([(x - 0.045, HULL_FRONT_Y + 0.10, 0.62), (x - 0.045, HULL_FRONT_Y + 0.16, 0.62),
                                  (x + 0.045, HULL_FRONT_Y + 0.16, 0.62), (x + 0.045, HULL_FRONT_Y + 0.10, 0.62)],
                                 0.02, 10), 1)
    bm_append(front, greebles(on_plane((0, HULL_FRONT_Y, 0.70), fn), 0.60, 0.22, 13, n=5, hmax=0.05), None)
    for x in (-0.95, 0.95):                       # machinery boxes in the cavity under each arm
        bm_append(front, bm_box((0.26, 0.18, 0.22), T(x, HULL_FRONT_Y + 0.09, 1.08)), 0)
        bm_append(front, louvre((0.20, 0.03, 0.16), T(x, HULL_FRONT_Y + 0.195, 1.08) @ Rz(180), 4), None)
        bm_append(front, bm_tube([(x * 0.85, HULL_FRONT_Y + 0.02, 0.80), (x * 0.85, HULL_FRONT_Y + 0.12, 0.80),
                                  (x, HULL_FRONT_Y + 0.12, 0.95)], 0.025, 12), 1)
    make("hull_front_details", front, [gray, dark], c_front, groups=["hull"])
    # glacis vents beside the brow
    gl = bmesh.new()
    for x in (-0.95, 0.95):
        p = Vector((x, 0.62, glacis_z(0.62)))
        bm_append(gl, grille(0.30, 0.18, 6, on_plane(p, (0, GLACIS_SLOPE, 1.0), up=(0, 1, 0)), depth=0.02), None)
    make("glacis_vents", gl, [gray, dark], c_det, groups=["hull"])

    # ================================================================ DECK
    make("turret_plinth", bm_merge(
        (bm_cyl(0.86, 0.86, TB, 48, T(*T0) @ T(0, 0, TB / 2)), 0),
        (bm_cyl(0.88, 0.88, 0.03, 48, T(*T0) @ T(0, 0, TB - 0.02)), 1),
        *[(bm_box((0.05, 0.03, 0.10), T(*T0) @ Rz(a) @ T(0, 0.865, 0.09)), 1) for a in range(0, 360, 20)]),
        [gray, dark], c_hull, groups=["hull"])
    deck = bmesh.new()
    for x in (-0.55, 0.55):                       # troop roof hatches behind the turret
        y = -2.05
        bm_append(deck, bm_box((0.48, 0.48, 0.03), T(x, y, DECK + 0.015)), 0)
        bm_append(deck, bm_box((0.40, 0.40, 0.01), T(x, y, DECK + 0.035)), 2)
        bm_append(deck, bm_tube([(x - 0.08, y, DECK + 0.04), (x - 0.08, y, DECK + 0.07),
                                 (x + 0.08, y, DECK + 0.07), (x + 0.08, y, DECK + 0.04)], 0.01, 8), 1)
        for dy in (-0.15, 0.15):
            bm_append(deck, cyl_x(0.02, 0.02, 0.10, 12, x + (0.24 if x > 0 else -0.24), y + dy, DECK + 0.03), 1)
    for x in (-0.62, 0.62):                       # deck grilles ahead of the turret
        bm_append(deck, grille(0.34, 0.30, 7, T(x, 0.30, DECK + 0.002), depth=0.02), None)
    for s in (1, -1):                             # tie-down eyes along the deck edges
        for y in (-0.40, 0.40):
            bm_append(deck, bm_box((0.08, 0.06, 0.02), T(s * 1.08, y, DECK + 0.01)), 1)
            bm_append(deck, bm_tube([(s * 1.08, y - 0.03, DECK + 0.02), (s * 1.08, y - 0.03, DECK + 0.06),
                                     (s * 1.08, y + 0.03, DECK + 0.06), (s * 1.08, y + 0.03, DECK + 0.02)],
                                    0.01, 8), 1)
    make("deck_details", deck, [panel, dark, paint_alt], c_det, groups=["hull"])

    # ================================================================ REAR
    ramp_pts = sym((RAMP_W, REAR_Y, 0.50), (RAMP_W, REAR_Y, RAMP_TOP),
                   (RAMP_W - 0.04, REAR_Y - 0.07, RAMP_TOP - 0.03), (RAMP_W - 0.04, REAR_Y - 0.07, 0.53))
    ramp = make("ramp", bm_hull(ramp_pts), [paint, paint_alt], c_rear,
                origin=(0, REAR_Y, 0.50), groups=["ramp"], bevel=0.01,
                panels=dict(cuts_z=(1.05,), cuts_x=(0.0,), alt=1, seed=9, rivet_step=0.24,
                            rivets_where=lambda c, n: n.y < -0.8))
    rr = REAR_Y - 0.07
    rd = bmesh.new()
    for x in (-0.40, -0.13, 0.13, 0.40):
        bm_append(rd, bm_hull([(x + dx, y, z) for dx in (-0.045, 0.045) for y, z in
                               ((rr, 1.52), (rr - 0.05, 1.48), (rr, 1.14), (rr - 0.04, 1.16))]), 0)
    bm_append(rd, bm_box((1.06, 0.05, 0.08), T(0, rr - 0.025, 1.05)), 1)
    bm_append(rd, grille(0.70, 0.28, 10, on_plane((0, rr, 0.75), (0, -1, 0))), None)
    bm_append(rd, bm_tube([(-0.18, rr, 0.95), (-0.18, rr - 0.06, 0.95), (0.18, rr - 0.06, 0.95),
                           (0.18, rr, 0.95)], 0.014, 8), 1)
    make("ramp_detail", rd, [panel, dark], c_rear, origin=(0, REAR_Y, 0.50), groups=["ramp"], parent=ramp)
    make("ramp_hinge", bm_merge(*[cyl_x(0.04, 0.04, 0.20, 16, x, REAR_Y - 0.02, 0.52) for x in (-0.40, 0.0, 0.40)]),
         steel, c_rear, groups=["hull"])
    make("rear_top_vent", grille(1.10, 0.12, 14, on_plane((0, REAR_Y, 1.70), (0, -1, 0)), depth=0.03),
         [gray, dark], c_rear, groups=["hull"])
    for s, side in sides:
        x = s * 0.88
        # tall louvered engine module, boxed out from the rear face (reference's rear vents)
        make(f"rear_module_{side}", bm_merge(
            (bm_box((0.52, 0.16, 1.14), T(x, REAR_Y - 0.08, 1.16)), 0),
            *[(bm_box((0.56, 0.20, 0.05), T(x, REAR_Y - 0.10, 1.16 + dz)), 0) for dz in (-0.57, 0.57)],
            *[(bm_box((0.05, 0.20, 1.18), T(x + dx, REAR_Y - 0.10, 1.16)), 0) for dx in (-0.27, 0.27)]),
            [gray], c_rear, groups=["hull"], bevel=0.008)
        make(f"rear_louvre_{side}", bm_merge(
            (louvre((0.44, 0.03, 0.50), T(x, REAR_Y - 0.175, 1.44), 7), None),
            (louvre((0.44, 0.03, 0.42), T(x, REAR_Y - 0.175, 0.86), 6), None)),
            [dark, panel], c_rear, groups=["hull"])
        make(f"rear_module_pipe_{side}", bm_merge(
            (bm_tube([(x + s * 0.24, REAR_Y - 0.18, 0.66), (x + s * 0.24, REAR_Y - 0.26, 0.70),
                      (x + s * 0.24, REAR_Y - 0.26, 1.56), (x + s * 0.24, REAR_Y - 0.18, 1.60)], 0.02, 10), 0),
            *[(bm_box((0.06, 0.08, 0.04), T(x + s * 0.24, REAR_Y - 0.22, z)), 1) for z in (0.95, 1.30)]),
            [steel, dark], c_rear, groups=["hull"])
        make(f"tow_hook_{side}", bm_merge(
            bm_box((0.14, 0.08, 0.10), T(x, REAR_Y - 0.04, 0.53)),
            bm_tube([(x - 0.045, REAR_Y - 0.08, 0.52), (x - 0.045, REAR_Y - 0.15, 0.52),
                     (x + 0.045, REAR_Y - 0.15, 0.52), (x + 0.045, REAR_Y - 0.08, 0.52)], 0.02, 10)),
            dark, c_rear, groups=["hull"])

    # ================================================================ ENGINE DRUM
    make("engine_drum_core", drum_x(0, DRUM_CORE, 2 * DRUM_CAP[0]), gray, c_eng, groups=["hull"])
    fins = bmesh.new()
    for k in range(19):
        bm_append(fins, drum_x(-0.36 + k * 0.04, DRUM_CORE + 0.04, 0.014), 0)
    make("engine_drum_fins", fins, dark, c_eng, groups=["hull"])
    segs = bmesh.new()
    for s in (1, -1):
        for x0, x1 in DRUM_SEGS:
            xc, w = s * (x0 + x1) / 2, x1 - x0
            bm_append(segs, drum_x(xc, DRUM_R, w), 0)
            for e in (x0, x1):
                bm_append(segs, drum_x(s * e, DRUM_R + 0.012, 0.03), 1)
        bm_append(segs, drum_x(s * 0.57, DRUM_R + 0.006, 0.08), 2)
    make("engine_drum_segments", segs, [paint, panel, accent], c_eng, groups=["hull"],
         panels=None)
    caps = bmesh.new()
    for s in (1, -1):
        e0, e1 = DRUM_CAP
        bm_append(caps, drum_x(s * (e0 + e1) / 2, DRUM_R, e1 - e0), 0)
        for r, w, mi in ((0.42, 0.02, 1), (0.355, 0.035, 0), (0.26, 0.05, 1), (0.14, 0.07, 0)):
            bm_append(caps, drum_x(s * (e1 + w / 2), r, w), mi)          # stepped face
        bm_append(caps, drum_x(s * (e1 + 0.09), 0.07, 0.04, 24), 1)
        for a in range(0, 360, 30):
            bm_append(caps, cyl_x(0.016, 0.016, 0.02, 8, s * (e1 + 0.025),
                                  DRUM.y + 0.39 * math.cos(R(a)), DRUM.z + 0.39 * math.sin(R(a))), 2)
    make("engine_drum_caps", caps, [paint, gray, steel], c_eng, groups=["hull"])
    for s in (1, -1):
        e1 = DRUM_CAP[1]
        bracket = bm_merge(
            (bm_hull([(s * x, y, z) for x in (e1 + 0.08, e1 + 0.17) for y, z in
                      ((-3.12, 1.72), (-2.48, 1.72), (-2.92, DRUM.z + 0.05), (-2.68, DRUM.z + 0.05))]), 0),
            (bm_box((0.40, 0.66, 0.08), T(s * (HULL_X + 0.10), -2.80, 1.76)), 0),
            (cyl_x(0.11, 0.11, 0.08, 32, s * (e1 + 0.125), DRUM.y, DRUM.z), 1),
            (cyl_x(0.06, 0.06, 0.05, 24, s * (e1 + 0.19), DRUM.y, DRUM.z), 0),
            *[(cyl_x(0.014, 0.014, 0.02, 8, s * (e1 + 0.17), DRUM.y + 0.08 * math.cos(R(a)),
                     DRUM.z + 0.08 * math.sin(R(a))), 2) for a in range(0, 360, 60)],
        )
        make(f"drum_bracket_{'r' if s > 0 else 'l'}", bracket, [gray, dark, steel], c_eng, groups=["hull"],
             bevel=0.01)
    make("engine_cradle", bm_merge(
        (bm_box_mm((-1.05, -3.10, DECK - 0.02), (1.05, -2.50, DECK + 0.04)), 0),
        *[(bm_hull([(x + dx, y, z) for dx in (-0.06, 0.06) for y, z in
                    ((-3.10, DECK), (-2.50, DECK), (-3.02, DECK + 0.12), (-2.58, DECK + 0.12))]), 0)
          for x in (-0.95, -0.25, 0.25, 0.95)]),
        [gray], c_eng, groups=["hull"], bevel=0.01)
    pipes = bmesh.new()
    for s in (1, -1):
        bm_append(pipes, bm_tube([(s * 0.30, -2.40, 2.38), (s * 0.30, -2.25, 2.20),
                                  (s * 0.30, -2.25, DECK + 0.02)], 0.03, 12), 0)
        bm_append(pipes, bm_cyl(0.05, 0.05, 0.03, 16, T(s * 0.30, -2.25, DECK + 0.015)), 1)
    make("engine_pipes", pipes, [steel, dark], c_eng, groups=["hull"])
    for s, side in sides:
        x = s * EXHAUST_X
        ey = DRUM.y - DRUM_R + 0.05
        make(f"exhaust_{side}", bm_merge(
            (cyl_y(0.11, 0.13, 0.18, 32, x, ey - 0.09, EXHAUST_Z), 0),
            (cyl_y(0.15, 0.15, 0.03, 32, x, ey - 0.17, EXHAUST_Z), 0),
            *[(bm_box((0.22, 0.012, 0.012), T(x, ey - 0.185, EXHAUST_Z) @ Ry(a)), 0) for a in (0, 60, 120)]),
            dark, c_eng, groups=["hull"])
        make(f"exhaust_glow_{side}", cyl_y(0.10, 0.10, 0.02, 32, x, ey - 0.17, EXHAUST_Z),
             thrust, c_eng, groups=["exhaust_glow"])

    # ================================================================ REPULSORS
    for i, (x, y, z, sx, sy_) in enumerate(REPULSORS, 1):
        make(f"repulsor_{i}", bm_box((sx, sy_, 0.06), T(x, y, z)), dark, c_rep, groups=["hull"])
        make(f"repulsor_glow_{i}", bm_box((sx - 0.06, sy_ - 0.10, 0.012), T(x, y, z - 0.035)),
             glow, c_rep, groups=["repulsor_glow"])
        n_bars = int(sy_ / 0.16)
        make(f"repulsor_grille_{i}", bm_merge(
            *[bm_box((sx - 0.03, 0.018, 0.016), T(x, y - sy_ / 2 + sy_ * (k + 0.5) / n_bars, z - 0.045))
              for k in range(n_bars)]),
             dark, c_rep, groups=["hull"])

    # ================================================================ TURRET
    turret = make("turret", bm_hull(tp(REAR_BLOCK)), [paint, paint_alt], c_tur, origin=T0, groups=["turret"],
                  bevel=0.03, bevel_segs=2,
                  panels=dict(cuts_x=(-0.25, 0.25), cuts_y=(T0.y - 0.55,), cuts_z=(T0.z + 0.45,), alt=1, seed=13))

    def tur(name, bm, mats, groups=("turret",), origin=T0, collection=c_tur, bevel=0.0, bevel_segs=1,
            panels=None, parent=turret):
        return make(name, bm, mats, collection, origin=origin, groups=list(groups), parent=parent,
                    bevel=bevel, bevel_segs=bevel_segs, panels=panels)

    def tm(x, y, z):
        return T(*(T0 + Vector((x, y, z))))

    for s, side in sides:
        tur(f"turret_cheek_{side}", bm_hull(tp(mirror(CHEEK, s))), [paint, paint_alt], bevel=0.03, bevel_segs=2,
            panels=dict(cuts_y=(T0.y + 0.25,), cuts_z=(T0.z + 0.45,), alt=1, seed=21 + s, rivet_step=0.16,
                        rivets_where=lambda c, n: n.y > 0.5))
    tur("turret_bridge", bm_box((0.50, 0.18, TT - 0.56), tm(0, 0.02, (TT + 0.56) / 2)), panel, bevel=0.01)
    tur("turret_rear_greebles", greebles(on_plane(T0 + Vector((0, -1.10, 0.42)), (0, -1, 0)), 1.10, 0.30, 51,
                                         n=8, hmax=0.04), [gray, dark])
    handles = bmesh.new()
    for x in (-0.40, 0.40):
        p = T0 + Vector((x, -1.10, 0.60))
        bm_append(handles, bm_tube([p + Vector((-0.10, 0.04, 0)), p + Vector((-0.10, -0.04, 0)),
                                    p + Vector((0.10, -0.04, 0)), p + Vector((0.10, 0.04, 0))], 0.012, 8))
    tur("turret_handles", handles, dark)

    # roof: gunner sight on the left cheek, commander's periscope dome, gunner hatch, antennas
    tur("gunner_sight", bm_merge(
        (bm_box((0.22, 0.28, 0.14), tm(-0.44, 0.18, TT + 0.07)), 0),
        (bm_box((0.26, 0.08, 0.03), tm(-0.44, 0.30, TT + 0.155)), 1),
        *[(bm_box((0.02, 0.24, 0.10), tm(-0.44 + dx, 0.18, TT + 0.06)), 1) for dx in (-0.12, 0.12)]),
        [dark, panel])
    tur("gunner_sight_glass", bm_box((0.16, 0.015, 0.06), tm(-0.44, 0.325, TT + 0.08)), glass,
        groups=["turret", "glass"])
    cs = T0 + Vector((0.32, -0.72, TT))
    tur("commander_sight", bm_merge(
        (bm_cyl(0.14, 0.14, 0.05, 32, T(cs.x, cs.y, cs.z + 0.025)), 0),
        (bm_cyl(0.05, 0.05, 0.10, 16, T(cs.x, cs.y, cs.z + 0.10)), 1),
        (bm_sphere(0.11, T(cs.x, cs.y, cs.z + 0.20), 24, 12), 0),
        (bm_box((0.16, 0.06, 0.07), T(cs.x, cs.y + 0.09, cs.z + 0.20)), 1)),
        [panel, dark])
    tur("commander_sight_glass", bm_box((0.12, 0.012, 0.04), T(cs.x, cs.y + 0.122, cs.z + 0.20)), glass,
        groups=["turret", "glass"])
    gh = T0 + Vector((-0.30, -0.58, TT))
    tur("gunner_hatch_ring", bm_cyl(0.20, 0.20, 0.03, 32, T(gh.x, gh.y, gh.z + 0.015)), panel)
    peri = bmesh.new()
    for a in (-40, 0, 40):
        mm = T(gh.x, gh.y, gh.z + 0.04) @ Rz(a) @ T(0, 0.25, 0)
        bm_append(peri, bm_box((0.08, 0.06, 0.07), mm), 0)
        bm_append(peri, bm_box((0.06, 0.01, 0.03), mm @ T(0, 0.031, 0.01)), 1)
    tur("gunner_periscopes", peri, [panel, glass])
    tur("hatch_gunner", bm_merge(
        (bm_cyl(0.165, 0.165, 0.03, 32, T(gh.x, gh.y, gh.z + 0.045)), 0),
        (bm_cyl(0.10, 0.10, 0.015, 24, T(gh.x, gh.y, gh.z + 0.067)), 0),
        (bm_tube([(gh.x - 0.06, gh.y + 0.05, gh.z + 0.06), (gh.x - 0.06, gh.y + 0.05, gh.z + 0.09),
                  (gh.x + 0.06, gh.y + 0.05, gh.z + 0.09), (gh.x + 0.06, gh.y + 0.05, gh.z + 0.06)], 0.01, 8), 1),
        (cyl_y(0.02, 0.02, 0.18, 12, gh.x - 0.165, gh.y, gh.z + 0.045), 1)),
        [panel, dark], groups=["turret", "hatch_gunner"], origin=(gh.x - 0.165, gh.y, gh.z + 0.045))
    for s in (1, -1):
        tur(f"antenna_{'r' if s > 0 else 'l'}", bm_merge(
            (bm_cyl(0.045, 0.04, 0.07, 12, tm(s * 0.50, -0.95, TT + 0.035)), 0),
            (bm_cyl(0.008, 0.004, 1.10 if s > 0 else 0.80, 6,
                    tm(s * 0.50, -0.95, TT + 0.07 + (0.55 if s > 0 else 0.40))), 0)), dark)

    tur("roof_periscope", bm_merge(
        (bm_cyl(0.10, 0.10, 0.04, 24, tm(0, 0.0, TT + 0.02)), 0),
        (bm_sphere(0.08, tm(0, 0.0, TT + 0.06), 24, 12), 1),
        (bm_box((0.10, 0.05, 0.05), tm(0, 0.07, TT + 0.08)), 0)), [gray, panel])
    tur("roof_periscope_glass", bm_box((0.07, 0.01, 0.025), tm(0, 0.097, TT + 0.085)), glass,
        groups=["turret", "glass"])

    # ---- right cheek: ball-and-mast sensor cluster (reference's stacked spheres and rod)
    bs = T0 + Vector((0.70, 0.30, 0.0))
    tur("ball_sensors", bm_merge(
        (bm_box((0.12, 0.22, 0.46), T(bs.x + 0.05, bs.y, bs.z + 0.48)), 0),
        *[(bm_sphere(0.09, T(bs.x + 0.19, bs.y, bs.z + z), 24, 12), 1) for z in (0.40, 0.60)],
        *[(cyl_y(0.035, 0.035, 0.03, 16, bs.x + 0.19, bs.y + 0.08, bs.z + z), 0) for z in (0.40, 0.60)],
        *[(bm_box((0.10, 0.05, 0.05), T(bs.x + 0.11, bs.y, bs.z + z)), 0) for z in (0.40, 0.60)],
        (bm_cyl(0.012, 0.012, 0.62, 8, T(bs.x + 0.33, bs.y - 0.02, bs.z + 0.56)), 0),
        *[(bm_sphere(0.032, T(bs.x + 0.33, bs.y - 0.02, bs.z + z), 16, 8), 1) for z in (0.36, 0.56, 0.76)],
        *[(bm_box((0.12, 0.02, 0.02), T(bs.x + 0.27, bs.y - 0.02, bs.z + z)), 0) for z in (0.36, 0.76)],
        (bm_cyl(0.05, 0.05, 0.12, 16, T(bs.x + 0.19, bs.y - 0.06, bs.z + 0.80)), 1)),
        [dark, panel])
    tur("ball_sensor_lenses", bm_merge(*[cyl_y(0.026, 0.026, 0.01, 16, bs.x + 0.19, bs.y + 0.097, bs.z + z)
                                         for z in (0.40, 0.60)]), glass, groups=["turret", "glass"])
    tur("stowage_r", bm_merge(
        (bm_box((0.12, 0.66, 0.26), tm(0.76, -0.60, 0.38)), 0),
        *[(bm_box((0.02, 0.60, 0.02), tm(0.825, -0.60, z)), 1) for z in (0.31, 0.38, 0.45)],
        *[(bm_box((0.03, 0.04, 0.28), tm(0.825, y, 0.38)), 1) for y in (-0.88, -0.32)]),
        [gray, dark])

    # ---- left cheek: the VLS pod, 8 cells opening upward through its roof
    (px0, px1), (py0, py1), (pz0, pz1) = POD
    tur("vls_pod", bm_hull(tp([(x, y, z) for x in (px0, px1) for y in (py0, py1) for z in (pz0, pz1)])),
        [paint, paint_alt], bevel=0.03, bevel_segs=2,
        panels=dict(cuts_z=(T0.z + 0.55,), alt=1, seed=31))
    front_face = bmesh.new()
    for ix in range(2):
        for iz in range(5):
            bm_append(front_face, cyl_y(0.032, 0.032, 0.02, 12, T0.x - 0.80 - ix * 0.14, T0.y + py1 + 0.005,
                                        T0.z + 0.36 + iz * 0.10), 0)
    bm_append(front_face, bm_box((0.36, 0.03, 0.05), tm((px0 + px1) / 2, py1 + 0.01, pz1 - 0.06)), 1)
    bm_append(front_face, grille(0.70, 0.30, 8, on_plane(T0 + Vector((px0, (py0 + py1) / 2 - 0.10, 0.52)), (-1, 0, 0),
                                                         up=(0, 0, 1)), depth=0.02), None)
    tur("vls_pod_details", front_face, [dark, panel])
    tur("vls_frame", bm_merge(
        *[(bm_box((px1 - px0 - 0.04, 0.025, 0.012), tm((px0 + px1) / 2, y, VLS_TOP + 0.006)), 0)
          for y in (-0.55, -0.35, -0.09, 0.17, 0.37)],
        (bm_box((0.02, py1 - py0 - 0.08, 0.012), tm(-0.87, (py0 + py1) / 2, VLS_TOP + 0.006)), 0)), dark)
    for i, (cx, cy) in enumerate(VLS_CELLS, 1):
        c = T0 + Vector((cx, cy, 0))
        tur(f"vls_cell_{i}", bm_box((VLS_CELL, VLS_CELL, 0.008), T(c.x, c.y, T0.z + VLS_TOP + 0.002)), dark)
        hinge = (c.x, c.y - VLS_CELL / 2, T0.z + VLS_TOP)      # rear edge: the hatch flips up and back
        tur(f"vls_hatch_{i}", bm_merge(
            (bm_box((VLS_CELL, VLS_CELL, 0.02), T(c.x, c.y, T0.z + VLS_TOP + 0.012)), 0),
            (bm_box((0.07, 0.07, 0.008), T(c.x, c.y, T0.z + VLS_TOP + 0.025)), 1),
            (cyl_x(0.01, 0.01, 0.10, 8, *hinge), 1)),
            [accent, gray], groups=["turret", f"vls_hatch_{i}"], origin=hinge)
        rz = T0.z + VLS_TOP
        rocket = bm_merge(
            (bm_cyl(0.048, 0.048, 0.36, 16, T(c.x, c.y, rz - 0.30)), 0),
            (bm_cyl(0.048, 0.005, 0.11, 16, T(c.x, c.y, rz - 0.065)), 1),
            *[(bm_box((0.004, 0.045, 0.06), T(c.x, c.y, rz - 0.45) @ Rz(a) @ T(0, 0.06, 0)), 2)
              for a in (0, 90, 180, 270)],
        )
        tur(f"rocket_{i}", rocket, [paint, accent, dark], groups=["turret", f"rocket_{i}"], collection=c_vls)

    # ---- 50 mm autocannon on a cylindrical mount between the cheeks
    gy, gz = G0.y, G0.z
    gun = make("gun_mount", bm_merge(
        (cyl_y(0.175, 0.175, 0.62, 40, 0, T0.y + 0.42, gz), 0),
        *[(cyl_y(0.185, 0.185, 0.03, 40, 0, T0.y + y, gz), 1) for y in (0.30, 0.55)],
        (cyl_y(0.19, 0.16, 0.05, 40, 0, T0.y + 0.745, gz), 1)),
        [paint, accent], c_gun, origin=G0, groups=["gun"], parent=turret)

    def bar(d0, d1, r1, r2=None, segs=40, x=0.0, z=0.0):
        return cyl_y(r1, r2 if r2 is not None else r1, d1 - d0, segs, x, gy + (d0 + d1) / 2, gz + z)

    barrel = bm_merge(
        (bar(0.36, 0.46, 0.12), 1),                                             # collar
        (bar(0.46, 1.15, 0.085), 0),                                            # recoil sleeve
        *[(bar(d, d + 0.03, 0.105), 1) for d in (0.58, 0.76, 0.94)],             # heat-sink rings
        *[(bar(0.46, 1.00, 0.03, segs=16, x=sx * 0.10, z=-0.05), 1) for sx in (1, -1)],
        (bar(1.15, 1.24, 0.085, 0.060), 0),                                     # step taper
        (bar(1.24, 3.14, 0.055), 0),
        (bar(2.10, 2.15, 0.07), 1),
        (bar(3.14, 3.40, 0.082), 1),                                            # muzzle brake
        (bar(3.40, 3.42, 0.07), 0),
        (bar(3.415, 3.425, 0.04, segs=16), 2),                                  # bore
        *[(bm_cyl(0.017, 0.017, 0.012, 10, T(0, gy + d, gz) @ Ry(a) @ T(0, 0, 0.081)), 2)
          for d in (3.20, 3.27, 3.34) for a in range(0, 360, 45)],               # brake ports
    )
    make("gun_barrel_50mm", barrel, [dark, gray, steel], c_gun, origin=G0, groups=["gun"], parent=gun)
    # square frame on the mount's front face (it elevates with the gun, so it never fouls the cheeks)
    make("gun_mount_frame", bm_merge(
        *[(bm_box((0.04, 0.05, 0.36), tm(sx * 0.16, 0.70, 0.44)), 0) for sx in (1, -1)],
        *[(bm_box((0.36, 0.05, 0.04), tm(0, 0.70, 0.44 + sz * 0.16)), 0) for sz in (1, -1)]),
        dark, c_gun, origin=G0, groups=["gun"], parent=gun)

    # ================================================================ INTERIOR
    make("interior_floor", bm_box_mm((-1.08, -3.10, FLOOR - 0.03), (1.08, 1.85, FLOOR)),
         dark, c_int, groups=["interior"])
    seats = [("driver", DRIVER_X, FRONT_Y, 0, FRONT_PAN, FLOOR),
             ("gunner", 0.0, T0.y - 0.12, 0, 1.40, 1.05)]
    n = 0
    for s, yaw in ((1, 90), (-1, -90)):
        for y in CARGO_Y:
            n += 1
            seats.append((f"cargo_{n:02d}", s * CARGO_X, y, yaw, PAN, FLOOR))
    seats.append(("cargo_13", -DRIVER_X, FRONT_Y, 0, FRONT_PAN, FLOOR))

    for name, x, y, yaw, pan, floor in seats:
        m = T(x, y, 0) @ Rz(yaw)
        bm = bm_merge(
            (bm_box((0.42, 0.40, 0.06), m @ T(0, 0, pan - 0.03)), 0),
            (bm_box((0.42, 0.06, 0.52), m @ T(0, -0.23, pan + 0.25)), 0),
            (bm_box((0.20, 0.20, pan - 0.06 - floor), m @ T(0, 0, (pan - 0.06 + floor) / 2)), 1),
        )
        is_turret = name == "gunner"
        make(f"seat_{name}", bm, [seat_m, dark], c_int, origin=(x, y, pan),
             groups=["turret" if is_turret else "interior"],
             parent=turret if is_turret else None)
        e = bpy.data.objects.new(f"proxy_{name}", None)
        e.empty_display_type = 'ARROWS'
        e.empty_display_size = 0.3
        e.location = (x, y, pan)
        e.rotation_euler = (0, 0, R(yaw))
        c_crew.objects.link(e)

    # ================================================================ MEMORY LOD
    sight = T0 + Vector((-0.44, 0.33, TT + 0.08))
    mem = {
        "osaveze": [tuple(T0), tuple(T0 + Vector((0, 0, 0.7)))],
        "osahlavne": [(-0.2, G0.y, G0.z), (0.2, G0.y, G0.z)],
        "konec hlavne": [(0, G0.y + 0.40, gz)],
        "usti hlavne": [(0, MUZZLE_Y, gz)],
        "gunnerview": [tuple(sight)],
        "commanderview": [tuple(cs + Vector((0, 0.13, 0.20)))],
        "driverview": [(DRIVER_X, 1.30, 1.84)],
        "ramp_axis": [(-RAMP_W, REAR_Y, 0.50), (RAMP_W, REAR_Y, 0.50)],
        "hatch_driver_axis": [(hx - 0.09, hy - 0.14, BROW_TOP + 0.06), (hx + 0.09, hy - 0.14, BROW_TOP + 0.06)],
        "hatch_gunner_axis": [(gh.x - 0.165, gh.y - 0.09, gh.z + 0.045), (gh.x - 0.165, gh.y + 0.09, gh.z + 0.045)],
        "pos driver": [(-0.6, -4.3, 0.3)],
        "pos gunner": [(0.6, -4.3, 0.3)],
        "pos cargo": [(0.0, -4.3, 0.3)],
        "light_l": [(-LENS_X[0], ARM_Y1 + 0.09, LENS_Z)], "light_l_end": [(-LENS_X[0], ARM_Y1 + 1.09, LENS_Z - 0.06)],
        "light_r": [(LENS_X[0], ARM_Y1 + 0.09, LENS_Z)], "light_r_end": [(LENS_X[0], ARM_Y1 + 1.09, LENS_Z - 0.06)],
    }
    ey = DRUM.y - DRUM_R + 0.05 - 0.18
    for s, side in sides:
        mem[f"exhaust_{side}"] = [(s * EXHAUST_X, ey, EXHAUST_Z)]
        mem[f"exhaust_{side}_dir"] = [(s * EXHAUST_X, ey - 1.0, EXHAUST_Z)]
    for i, (cx, cy) in enumerate(VLS_CELLS, 1):
        c = T0 + Vector((cx, cy, VLS_TOP))
        mem[f"missile_{i}"] = [tuple(c)]
        mem[f"missile_{i}_dir"] = [tuple(c + Vector((0, 0, 1.0)))]
        mem[f"vls_hatch_{i}_axis"] = [(c.x + d, c.y - VLS_CELL / 2, c.z) for d in (-0.05, 0.05)]
    for i, (x, y, z, sx, sy_) in enumerate(REPULSORS, 1):
        mem[f"repulsor_{i}"] = [(x, y, z - 0.05)]

    bm = bmesh.new()
    dl = bm.verts.layers.deform.verify()
    for gi, pts in enumerate(mem.values()):
        for p in pts:
            bm.verts.new(p)[dl][gi] = 1.0
    me = bpy.data.meshes.new("LOD_Memory")
    bm.to_mesh(me)
    bm.free()
    ob = bpy.data.objects.new("LOD_Memory", me)
    for name in mem:
        ob.vertex_groups.new(name=name)
    c_mem.objects.link(ob)

    # ================================================================ GEOMETRY LOD
    def wall_pts(poly, s):
        return [(s * x, y, z) for y, z in poly for x in (wall_x(z), wall_in_x(z))]

    drum = [(x, DRUM.y + DRUM_R * math.cos(a), DRUM.z + DRUM_R * math.sin(a))
            for x in (-DRUM_CAP[1] - 0.08, DRUM_CAP[1] + 0.08)
            for a in (2 * math.pi * i / 8 for i in range(8))]
    geo_parts = [
        (HULL + BROW, ["hull"]),
        (wall_pts(WALL_UP, 1), ["hull"]), (wall_pts(WALL_LO, 1), ["hull"]),
        (wall_pts(WALL_UP, -1), ["hull"]), (wall_pts(WALL_LO, -1), ["hull"]),
        (list(ARM), ["hull"]), (mirror(ARM, -1), ["hull"]),
        (drum, ["hull"]),
        (tp(REAR_BLOCK + CHEEK + mirror(CHEEK, -1)
            + [(x, y, z) for x in POD[0] for y in POD[1] for z in POD[2]]), ["turret"]),
        ([(x, y, z) for x in (-0.175, 0.175) for y in (T0.y + 0.11, T0.y + 0.74) for z in (gz - 0.175, gz + 0.175)]
         + sym((0.08, MUZZLE_Y, gz + 0.08), (0.08, MUZZLE_Y, gz - 0.08)), ["gun"]),
    ]
    names = ["hull", "turret", "gun"] + [f"Component{i:02d}" for i in range(1, len(geo_parts) + 1)]
    bm = bmesh.new()
    dl = bm.verts.layers.deform.verify()
    for i, (pts, groups) in enumerate(geo_parts, 1):
        bm_append(bm, bm_hull(pts), 0,
                  [names.index(g) for g in groups + [f"Component{i:02d}"]], dl)
    finish(bm)
    me = bpy.data.meshes.new("LOD_Geometry")
    bm.to_mesh(me)
    bm.free()
    ob = bpy.data.objects.new("LOD_Geometry", me)
    for name in names:
        ob.vertex_groups.new(name=name)
    c_geo.objects.link(ob)
    layer_coll("LOD_Geometry").hide_viewport = True

    unwrap([o for o in vis.all_objects if o.type == 'MESH'])


def unwrap(objs):
    """Basic Smart UV Project so the texture artists have a starting point."""
    vl = bpy.context.view_layer
    for o in vl.objects:
        o.select_set(False)
    for o in objs:
        o.select_set(True)
    vl.objects.active = objs[0]
    try:
        bpy.ops.object.mode_set(mode='EDIT')
        bpy.ops.mesh.select_all(action='SELECT')
        bpy.ops.uv.smart_project(angle_limit=R(66), island_margin=0.02)
    except RuntimeError as err:
        print("UV unwrap skipped:", err)
    finally:
        bpy.ops.object.mode_set(mode='OBJECT')
        for o in objs:
            o.select_set(False)


def report():
    deps = bpy.context.evaluated_depsgraph_get()
    total, rivets = 0, 0
    per = {}
    for o in bpy.data.collections["LOD_Resolution_0"].all_objects:
        if o.type == 'MESH':
            me = o.evaluated_get(deps).data
            n = sum(len(p.vertices) - 2 for p in me.polygons)
            total += n
            if o.name.endswith("_rivets"):
                rivets += n
            c = o.users_collection[0].name
            per[c] = per.get(c, 0) + n
    print(f"LOD_Resolution_0 triangles: {total} (rivets {rivets})")
    for c, n in sorted(per.items(), key=lambda kv: -kv[1]):
        print(f"    {c:16s} {n}")
    lo = Vector((1e9,) * 3)
    hi = -lo
    for o in bpy.data.collections["LOD_Resolution_0"].all_objects:
        if o.type == 'MESH' and not o.name.startswith("antenna"):
            for c in o.bound_box:
                w = o.matrix_world @ Vector(c)
                lo = Vector(map(min, lo, w))
                hi = Vector(map(max, hi, w))
    d = hi - lo
    print(f"Overall size (no antennas): width {d.x:.2f} m, length {d.y:.2f} m, "
          f"height {hi.z:.2f} m, lowest point {lo.z:.2f} m")


if __name__ == "__main__":
    argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
    build(argv[argv.index("--livery") + 1] if "--livery" in argv else LIVERY)
    bpy.context.view_layer.update()
    report()
    if "--out" in argv:
        path = argv[argv.index("--out") + 1]
        bpy.ops.wm.save_as_mainfile(filepath=bpy.path.abspath(path))
        print("Saved", path)
