"""
MSE v1: sci-fi repulsorlift IFV for Arma 3 (Clone Wars era, 41st legion).

A fresh design, separate from the hover_ifv/ attempts, drawn from the
reference sheet of a heavy Republic-style repulsor tank but original:

    * two tall slab skirts with a chined outer face that run forward past
      the nose as raked prongs, cut on the diagonal;
    * a recessed centre nose with a chevron of two raised armor arms that
      spring from the driver's brow and end in twin lens clusters, a large
      framed sensor between them and a keel plate underneath;
    * a brow block over the driver with one long vision slit;
    * a faceted turret with a 50 mm autocannon, a ball sensor cluster on
      one cheek, a perforated cooling pack on the other, and an 8-cell
      vertical launch system set into the roof behind the gunner;
    * a finned transverse engine drum across the rear deck;
    * a rear ramp between louvered engine boxes.

Bradley-sized: about 7.2 m long over the prongs, 3.6 m wide over the
skirts, 2.55 m to the turret roof. 2 crew + 13 passengers. Detail is spent
on greebles (vents, conduits, dampers, sensors, hatches) rather than
rivets, and on surfaces that are seen rather than the belly.

Pick the legion markings with LIVERY below or on the command line:
41st (green, default), republic (red), 501st (blue), 212th (orange).

Builds the whole model from scratch with bpy/bmesh, no add-ons needed.

Run headless:
    blender --background --python MSE_v1_build.py -- --out MSE_v1.blend [--livery 501st]
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


def bm_spring(mat, coil_r, wire_r, length, turns, per_turn=20, ring=6):
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
DECK = 1.88
DECK_FRONT = 0.60                         # where the deck breaks into the glacis
NOSE_Y, NOSE_Z = 3.15, 0.90
GLACIS_SLOPE = (DECK - NOSE_Z) / (NOSE_Y - DECK_FRONT)
GLACIS_DEG = math.degrees(math.atan(GLACIS_SLOPE))


def glacis_z(y):
    return DECK - (y - DECK_FRONT) * GLACIS_SLOPE


SHOULDER_Z = 1.55
SHOULDER_Y = DECK_FRONT + (DECK - SHOULDER_Z) / GLACIS_SLOPE
REAR_Y = -3.20

# Centre hull between the skirts: flat belly, vertical rear, flat turret deck,
# long glacis down to a recessed nose behind the prong tips.
HULL = sym(
    (1.18, REAR_Y, BELLY), (1.18, 2.85, BELLY),               # belly
    (1.22, REAR_Y, 0.80), (1.22, 3.05, 0.80),                 # sides (behind the skirts)
    (1.22, REAR_Y, SHOULDER_Z), (1.22, SHOULDER_Y, SHOULDER_Z),
    (1.02, REAR_Y, DECK), (1.02, DECK_FRONT, DECK),           # turret deck
    (1.20, NOSE_Y, NOSE_Z),                                   # nose
)

# Slab skirt (right side; mirrored for the left): flat inner face against the
# hull, chined outer face, flat top, and a prong running past the nose that
# is cut on the diagonal (outer edge longest) with a wedge side profile.
SKIRT_TOP, SKIRT_BOT, CHINE_Z = 1.75, 0.40, 1.05
SKIRT = (
    (1.22, -3.25, SKIRT_TOP), (1.66, -3.25, SKIRT_TOP), (1.80, -3.32, CHINE_Z),
    (1.62, -3.12, SKIRT_BOT), (1.26, -3.12, SKIRT_BOT), (1.22, -3.25, CHINE_Z),
    (1.22, 2.25, SKIRT_TOP), (1.66, 2.25, SKIRT_TOP), (1.80, 2.40, CHINE_Z),
    (1.26, 2.70, SKIRT_BOT), (1.62, 2.70, SKIRT_BOT),
    (1.22, 3.55, 1.12), (1.22, 3.55, 0.88),                   # inner tip
    (1.62, 3.82, 1.14), (1.60, 3.80, 0.88), (1.76, 3.92, 1.00),  # outer tip
)
SKIRT_UP_DEG = math.degrees(math.atan2(1.80 - 1.66, SKIRT_TOP - CHINE_Z))
SKIRT_LO_DEG = math.degrees(math.atan2(1.80 - 1.62, CHINE_Z - SKIRT_BOT))


def skirt_up_x(z):
    return 1.66 + (1.80 - 1.66) * (SKIRT_TOP - z) / (SKIRT_TOP - CHINE_Z)


def skirt_lo_x(z):
    return 1.62 + (1.80 - 1.62) * (z - SKIRT_BOT) / (CHINE_Z - SKIRT_BOT)


# Driver's brow block riding on the glacis, narrow, below the turret's sweep.
BROW_TOP = 2.00
BROW = sym(
    (0.50, 0.70, BROW_TOP), (0.50, 1.80, BROW_TOP),
    (0.58, 2.05, glacis_z(2.05) - 0.03), (0.58, 0.70, 1.84),
)


def brow_front_y(z):
    """Y of the brow's raked front face at height z."""
    z0 = glacis_z(2.05) - 0.03
    return 1.80 + (BROW_TOP - z) * (2.05 - 1.80) / (BROW_TOP - z0)


BROW_FRONT_DEG = math.degrees(math.atan2(2.05 - 1.80, BROW_TOP - (glacis_z(2.05) - 0.03)))
DRIVER_X = -0.28

# Raised armor arm (right side; mirrored): springs from the brow side, runs
# forward and out over the glacis with a shadow gap under it, ends ahead of
# the nose in a twin lens cluster.
ARM_Y0, ARM_Y1 = 1.25, 3.30
ARM = (
    (0.42, ARM_Y0, 2.00), (0.70, ARM_Y0, 2.00), (0.42, ARM_Y0, 1.78), (0.70, ARM_Y0, 1.78),
    (0.82, ARM_Y1, 1.27), (1.12, ARM_Y1, 1.27), (0.82, ARM_Y1, 1.02), (1.14, ARM_Y1, 1.02),
)


def arm_t(y):
    return (y - ARM_Y0) / (ARM_Y1 - ARM_Y0)


def arm_top_z(y):
    return 2.00 - arm_t(y) * (2.00 - 1.27)


def arm_bot_z(y):
    return 1.78 - arm_t(y) * (1.78 - 1.02)


def arm_mid_x(y):
    return 0.56 + arm_t(y) * (0.98 - 0.56)


ARM_DEG = math.degrees(math.atan2(2.00 - 1.27, ARM_Y1 - ARM_Y0))
ARM_YAW = math.degrees(math.atan2(0.98 - 0.56, ARM_Y1 - ARM_Y0))
LENS_Z = 1.145
LENS_X = (0.90, 1.05)                     # inner lens is the headlight

# Turret: axis on the deck, aft of centre, faceted with a rear bustle that
# carries the VLS block.
T0 = Vector((0.0, -0.85, DECK))
TROOF = 0.55                              # turret roof, turret-relative
TURRET = sym(
    (1.00, -1.25, 0.02), (1.00, 0.55, 0.02), (0.70, 0.95, 0.04),
    (0.84, -1.22, 0.42), (0.84, 0.45, 0.42), (0.52, 0.82, 0.38),
    (0.72, -1.25, TROOF), (0.72, 0.30, TROOF), (0.40, 0.60, TROOF),
    (0.92, -1.40, 0.24), (0.80, -1.40, 0.44),                 # rear bustle
)
MANTLET = sym((0.30, 0.78, 0.12), (0.30, 0.78, 0.48), (0.25, 1.18, 0.17), (0.25, 1.18, 0.43))
G0 = T0 + Vector((0.0, 0.98, 0.30))      # gun elevation pivot
BARREL_LEN = 3.38
MUZZLE_Y = G0.y + BARREL_LEN

VLS_COLS = (-0.22, 0.22)
VLS_ROWS = (-1.03, -0.81, -0.59, -0.37)
VLS_CELLS = [(cx, cy) for cy in VLS_ROWS for cx in VLS_COLS]
VLS_TOP = 0.68                            # turret-relative
VLS_HINGE = 0.32                          # hatch hinge line, |x|, turret-relative

# Finned transverse engine drum on a cradle across the rear deck.
DRUM = Vector((0.0, -2.95, 2.12))
DRUM_R, DRUM_HALF = 0.36, 1.05
EXHAUST_X, EXHAUST_Z = 0.62, 2.02

FLOOR = 0.53
PAN = 0.98                                # passenger seat height
CARGO_Y = (-2.75, -2.15, -1.55, -0.95, -0.35, 0.25)
CARGO_X = 0.92
FRONT_Y = 1.45                            # driver and front passenger, under the brow
RAMP_W, RAMP_TOP = 0.66, 1.70
# (x, y, z, size_x, size_y): 3 strips under each skirt, 2 plates under the belly
REPULSORS = ([(s * 1.44, y, 0.37, 0.28, 1.40) for s in (1, -1) for y in (-2.30, -0.60, 1.10)]
             + [(0.0, -1.60, 0.42, 1.50, 1.20), (0.0, 1.00, 0.42, 1.50, 1.20)])


def tp(pts):
    """Turret-relative points to world."""
    return [tuple(Vector(p) + T0) for p in pts]


def on_slope(base, deg, lift):
    """Matrix for a part lying on a surface tilted `deg` nose-down about X."""
    n = Vector((0, math.sin(R(deg)), math.cos(R(deg))))
    return T(*(Vector(base) + n * lift)) @ Rx(-deg)


def drum_x(x, r, depth, segs=64):
    """Cylinder segment of the engine drum, axis along X."""
    return cyl_x(r, r, depth, segs, x, DRUM.y, DRUM.z)


# ------------------------------------------------------------------- build

def build(livery=LIVERY):
    clear_scene()
    scn = bpy.context.scene
    scn.unit_settings.system = 'METRIC'
    scn.unit_settings.scale_length = 1.0

    root = coll("MSE_v1")
    vis = coll("LOD_Resolution_0", root)
    c_hull = coll("Hull", vis)
    c_skirt = coll("Skirts", vis)
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

    paint = material("hull_white", (0.80, 0.80, 0.77), rough=0.5)
    paint_alt = material("hull_white_alt", (0.69, 0.69, 0.66), rough=0.55)
    gray = material("hull_gray", (0.30, 0.31, 0.32), rough=0.55)
    gray_alt = material("hull_gray_alt", (0.24, 0.25, 0.26), rough=0.6)
    panel = material("armor_panel", (0.50, 0.50, 0.49), rough=0.55)
    dark = material("dark_metal", (0.07, 0.075, 0.08), rough=0.4, metal=0.7)
    steel = material("steel", (0.30, 0.30, 0.31), rough=0.35, metal=0.8)
    accent = material(f"legion_{livery}", LIVERIES[livery], rough=0.5)
    glass = material("glass", (0.015, 0.05, 0.06), rough=0.06, metal=0.4)
    glow = material("repulsor_glow", (0.1, 0.3, 0.5), emit=(0.35, 0.75, 1.0), strength=6.0)
    thrust = material("thruster_glow", (0.1, 0.2, 0.5), emit=(0.45, 0.6, 1.0), strength=10.0)
    lamp = material("headlight", (0.9, 0.9, 0.8), emit=(1.0, 0.92, 0.75), strength=5.0)
    tail = material("taillight", (0.5, 0.02, 0.02), emit=(1.0, 0.08, 0.05), strength=4.0)
    seat_m = material("seat", (0.16, 0.16, 0.14), rough=0.8)
    DETAIL["rivet"] = steel

    sides = ((1, "r"), (-1, "l"))

    # ================================================================ HULL
    make("hull", two_tone(bm_hull(HULL), 1.0), [paint, gray, paint_alt, gray_alt], c_hull,
         groups=["hull"], bevel=0.035, bevel_segs=2,
         panels=dict(cuts_x=(-0.45, 0.45), cuts_y=(-2.45, -1.65, -0.05, 0.75, 1.55, 2.35),
                     cuts_z=(1.20,), alt=2, seed=11))

    # ---- slab skirts: two plate rows, a bolted row along the upper facet only
    for s, side in sides:
        make(f"skirt_{side}", two_tone(bm_hull(mirror(SKIRT, s)), CHINE_Z - 0.02),
             [paint, gray, paint_alt], c_skirt, groups=["hull"], bevel=0.03, bevel_segs=2,
             panels=dict(cuts_y=(-2.20, -1.15, -0.10, 0.95, 2.00, 3.00), cuts_z=(1.42, 0.72),
                         alt=2, seed=3 if s > 0 else 4, rivet_step=0.34,
                         rivets_where=lambda c, n, s=s: n.x * s > 0.6 and c.z > 1.45 and c.y < 2.2))
        # dark ram cap on the prong tip
        tip = ((1.215, 3.55, 1.12), (1.215, 3.55, 0.88), (1.62, 3.82, 1.14), (1.60, 3.80, 0.88),
               (1.76, 3.92, 1.00))
        make(f"prong_cap_{side}", bm_hull(mirror([(x, y + dy, z) for x, y, z in tip for dy in (0.02, -0.14)], s)),
             gray_alt, c_skirt, groups=["hull"], bevel=0.01)

    # ================================================================ BROW
    make("brow", bm_hull(BROW), [paint, paint_alt], c_front, groups=["hull"], bevel=0.03, bevel_segs=2,
         panels=dict(cuts_x=(-0.18, 0.18), cuts_y=(1.25,), alt=1, seed=5))
    # vision slit: armored block, glass, hood and lower lip
    zs = 1.83
    m = T(0, brow_front_y(zs), zs) @ Rx(BROW_FRONT_DEG)     # local +Y out of the raked face
    slit = bm_merge(
        (bm_box((0.86, 0.08, 0.11), m @ T(0, 0.02, 0)), 0),
        (bm_box((0.78, 0.02, 0.035), m @ T(0, 0.055, 0)), 1),
        (bm_box((0.94, 0.16, 0.025), m @ T(0, 0.07, 0.07)), 2),        # hood
        (bm_box((0.90, 0.10, 0.02), m @ T(0, 0.05, -0.065)), 2),       # lip
        *[(bm_box((0.012, 0.03, 0.04), m @ T(x, 0.07, 0)), 0) for x in (-0.20, 0.0, 0.20)],
    )
    make("brow_slit", slit, [dark, glass, panel], c_front, groups=["hull", "glass"])
    # driver hatch (round, hinged at the rear) and a periscope ring
    hx, hy = DRIVER_X, 1.30
    ring = bm_merge((bm_cyl(0.21, 0.21, 0.05, 32, T(hx, hy, BROW_TOP + 0.02)), 0))
    for a in (-60, -30, 0, 30, 60):
        mm = T(hx, hy, BROW_TOP + 0.07) @ Rz(a) @ T(0, 0.17, 0)
        bm_append(ring, bm_box((0.08, 0.06, 0.05), mm), 0)
        bm_append(ring, bm_box((0.055, 0.01, 0.025), mm @ T(0, 0.031, 0)), 1)
    make("driver_cupola", ring, [panel, glass], c_front, groups=["hull"])
    lid = bm_merge(
        (bm_cyl(0.15, 0.15, 0.035, 32, T(hx, hy, BROW_TOP + 0.062)), 0),
        (bm_cyl(0.09, 0.09, 0.02, 24, T(hx, hy, BROW_TOP + 0.088)), 0),
        (bm_tube([(hx - 0.05, hy + 0.04, BROW_TOP + 0.09), (hx - 0.05, hy + 0.04, BROW_TOP + 0.12),
                  (hx + 0.05, hy + 0.04, BROW_TOP + 0.12), (hx + 0.05, hy + 0.04, BROW_TOP + 0.09)],
                 0.01, 8), 1),
        (cyl_x(0.022, 0.022, 0.20, 12, hx, hy - 0.15, BROW_TOP + 0.06), 1),
    )
    make("hatch_driver", lid, [panel, dark], c_front, origin=(hx, hy - 0.15, BROW_TOP + 0.06),
         groups=["hatch_driver"])
    spots = bmesh.new()
    lenses = bmesh.new()
    for x in (-0.40, 0.40):
        y0 = brow_front_y(BROW_TOP) + 0.02
        bm_append(spots, bm_box((0.10, 0.08, 0.05), T(x, y0 - 0.03, BROW_TOP + 0.02)), 0)
        bm_append(spots, cyl_y(0.04, 0.045, 0.07, 24, x, y0 + 0.03, BROW_TOP + 0.05), 1)
        bm_append(lenses, cyl_y(0.034, 0.034, 0.01, 24, x, y0 + 0.068, BROW_TOP + 0.05))
    make("brow_spotlights", spots, [dark, gray], c_front, groups=["hull"])
    make("brow_spotlight_lenses", lenses, lamp, c_front, groups=["hull"])
    # passenger-side sensor block and brow side vision blocks
    make("brow_sensor", bm_merge(
        (bm_box((0.22, 0.26, 0.10), T(-DRIVER_X, 1.30, BROW_TOP + 0.05)), 0),
        (bm_box((0.16, 0.01, 0.05), T(-DRIVER_X, 1.435, BROW_TOP + 0.06)), 1),
        (bm_cyl(0.04, 0.04, 0.10, 12, T(-DRIVER_X + 0.06, 1.22, BROW_TOP + 0.15)), 2),
        (bm_cyl(0.05, 0.05, 0.02, 12, T(-DRIVER_X + 0.06, 1.22, BROW_TOP + 0.21)), 2)),
        [panel, glass, dark], c_front, groups=["hull"])

    # ================================================================ ARMS
    for s, side in sides:
        make(f"armor_arm_{side}", bm_hull(mirror(ARM, s)), [paint, paint_alt], c_front,
             groups=["hull"], bevel=0.03, bevel_segs=2,
             panels=dict(cuts_y=(1.95, 2.65), alt=1, seed=7 if s > 0 else 8, rivet_step=0.16,
                         rivets_where=lambda c, n: n.z > 0.5))
        # legion stripe along the arm top
        stripe = []
        for y in (1.85, 3.20):
            x, z = arm_mid_x(y), arm_top_z(y)
            stripe += [(s * (x + dx), y, z + dz) for dx in (-0.035, 0.035) for dz in (0.006, 0.018)]
        make(f"arm_stripe_{side}", bm_hull(stripe), accent, c_det, groups=["hull"])
        # pylons and hydraulic rams in the shadow gap under the arm
        under = bmesh.new()
        for y in (1.75, 2.75):
            x = s * arm_mid_x(y)
            top, bot = arm_bot_z(y), glacis_z(y)
            bm_append(under, bm_box((0.16, 0.14, top - bot + 0.04), T(x, y, (top + bot) / 2)), 0)
        a = Vector((s * arm_mid_x(2.45), 2.45, glacis_z(2.45) + 0.02))
        b = Vector((s * arm_mid_x(2.15), 2.15, arm_bot_z(2.15) - 0.01))
        d = b - a
        bm_append(under, bm_cyl(0.035, 0.035, d.length * 0.55, 12, orient(a + d * 0.275, d)), 1)
        bm_append(under, bm_cyl(0.02, 0.02, d.length * 0.5, 10, orient(a + d * 0.75, d)), 2)
        make(f"arm_pylons_{side}", under, [dark, gray, steel], c_det, groups=["hull"])
        # vent strips along the arm's outer flank, following its slope
        d = Vector((0.44 * s, ARM_Y1 - ARM_Y0, -0.73)).normalized()
        n_ = Vector((2.05 * s, -0.44, 0)).normalized()
        n_ = (n_ - d * n_.dot(d)).normalized()
        up = n_.cross(d) if n_.cross(d).z > 0 else d.cross(n_)
        flank = bmesh.new()
        for y in (1.95, 2.70):
            t_ = arm_t(y)
            p = Vector((s * (0.70 + 0.44 * t_ + 0.004), y, (arm_top_z(y) + arm_bot_z(y)) / 2 + 0.005))
            bm_append(flank, grille(0.42, 0.11, 8, on_plane(p, n_, up), depth=0.018), None)
        make(f"arm_vents_{side}", flank, [gray, dark], c_det, groups=["hull"])
        # twin lens cluster on the arm end
        hm = T(s * 0.975, ARM_Y1 + 0.015, LENS_Z)
        housing = bm_merge(
            (bm_box((0.34, 0.05, 0.22), hm), 0),
            *[(cyl_y(0.072, 0.072, 0.05, 32, s * x, ARM_Y1 + 0.05, LENS_Z), 0) for x in LENS_X],
            (bm_box((0.36, 0.10, 0.025), hm @ T(0, 0.04, 0.12)), 1),                    # visor
            *[(bm_box((0.025, 0.10, 0.20), hm @ T(sx * 0.17, 0.04, 0)), 1) for sx in (-1, 1)],
        )
        for x in LENS_X:
            bm_append(housing, cyl_y(0.064, 0.064, 0.012, 32, s * x, ARM_Y1 + 0.081, LENS_Z), 1)
        make(f"lens_housing_{side}", housing, [dark, panel], c_front, groups=["hull"])
        make(f"light_{side}", cyl_y(0.055, 0.055, 0.02, 32, s * LENS_X[0], ARM_Y1 + 0.08, LENS_Z),
             lamp, c_front, groups=[f"light_{side}"])
        make(f"arm_sensor_{side}", bm_merge(
            (cyl_y(0.055, 0.055, 0.02, 32, s * LENS_X[1], ARM_Y1 + 0.08, LENS_Z), 0),
            (cyl_y(0.02, 0.02, 0.01, 16, s * LENS_X[1], ARM_Y1 + 0.093, LENS_Z), 1)),
             [glass, lamp], c_front, groups=["hull", "glass"])

    # ================================================================ NOSE
    sy = 2.62
    sz = glacis_z(sy)
    mount = bm_hull([(x * k, y, z) for x in (-0.25, 0.25) for y, z, k in
                     ((sy - 0.30, sz + 0.12, 0.70), (sy - 0.26, sz + 0.36, 0.70), (sy - 0.05, sz + 0.44, 0.92),
                      (sy + 0.16, sz + 0.42, 1.0), (sy + 0.18, sz - 0.12, 1.0), (sy - 0.30, sz - 0.05, 0.70))])
    make("nose_sensor_mount", mount, [panel, paint_alt], c_front, groups=["hull"], bevel=0.025, bevel_segs=2,
         panels=dict(cuts_y=(sy - 0.04,), alt=1, alt_share=0.5, seed=17))
    flank = bmesh.new()
    for x in (-1, 1):
        n_ = Vector((x, 0.0, 0.0))
        bm_append(flank, grille(0.22, 0.12, 5, on_plane((x * 0.252, sy + 0.02, sz + 0.20), n_), depth=0.02), None)
    bm_append(flank, greebles(on_plane((0, sy + 0.02, sz + 0.43), (0, 0, 1), up=(0, 1, 0)), 0.30, 0.22, 71,
                              n=4, hmax=0.035), None)
    make("nose_sensor_greebles", flank, [gray, dark], c_det, groups=["hull"])
    lc = Vector((0, sy + 0.18, sz + 0.14))
    lens = bm_merge(
        (cyl_y(0.19, 0.19, 0.06, 40, 0, lc.y, lc.z), 0),
        (cyl_y(0.17, 0.17, 0.04, 40, 0, lc.y + 0.04, lc.z), 1),
        (cyl_y(0.12, 0.12, 0.02, 32, 0, lc.y + 0.06, lc.z), 2),
        *[(cyl_y(0.018, 0.018, 0.03, 8, 0.17 * math.cos(R(a)), lc.y + 0.04, lc.z + 0.17 * math.sin(R(a))), 0)
          for a in range(0, 360, 45)],
        # square bracket frame around the lens, like the reference's boxed sensor
        *[(bm_box((0.46, 0.06, 0.04), T(0, lc.y + 0.01, lc.z + dz)), 3) for dz in (-0.21, 0.21)],
        *[(bm_box((0.04, 0.06, 0.38), T(dx, lc.y + 0.01, lc.z)), 3) for dx in (-0.21, 0.21)],
    )
    make("nose_sensor", lens, [dark, steel, glass, panel], c_front, groups=["hull", "glass"])
    keel = bm_hull([(x, y, z) for x in (-0.09, 0.09) for y, z in
                    ((2.95, 0.98), (3.42, 0.90), (3.50, 0.70), (3.30, 0.52), (2.90, 0.50))])
    make("nose_keel", keel, gray_alt, c_front, groups=["hull"], bevel=0.02)
    make("nose_keel_detail", bm_merge(
        (bm_box((0.20, 0.06, 0.06), T(0, 3.40, 0.62)), 0),
        *[(bm_box((0.205, 0.03, 0.016), T(0, y, 0.984 - (y - 2.95) * 0.08 / 0.47)), 1)
          for y in (3.10, 3.17, 3.24, 3.31)],
        (bm_tube([(0.10, 3.44, 0.62), (0.16, 3.44, 0.62), (0.16, 3.52, 0.62), (0.10, 3.52, 0.62)], 0.016, 8), 0),
        (bm_tube([(-0.10, 3.44, 0.62), (-0.16, 3.44, 0.62), (-0.16, 3.52, 0.62), (-0.10, 3.52, 0.62)], 0.016, 8), 0)),
        [dark, steel], c_front, groups=["hull"])
    # nose face: grilles flanking the keel, tow eyes at the corners
    noseface = bmesh.new()
    nface_n = Vector((0, 0.45, -0.30)).normalized()  # lower nose slopes back under to the belly
    for x in (-0.55, 0.55):
        p = Vector((x, 3.00, 0.68))
        bm_append(noseface, grille(0.50, 0.24, 9, on_plane(p, nface_n)), None)
    for x in (-0.98, 0.98):
        bm_append(noseface, bm_box((0.14, 0.12, 0.10), T(x, 3.04, 0.62)), 0)
        bm_append(noseface, bm_tube([(x - 0.04, 3.09, 0.60), (x - 0.04, 3.15, 0.60),
                                     (x + 0.04, 3.15, 0.60), (x + 0.04, 3.09, 0.60)], 0.018, 8), 1)
    make("nose_grilles", noseface, [gray, dark], c_front, groups=["hull"])

    # glacis vent boxes outboard of the arms
    gl = bmesh.new()
    for s in (1, -1):
        for y in (1.20, 2.00):
            base = Vector((s * 1.00, y, glacis_z(y)))
            mm = on_slope(base, GLACIS_DEG, 0.0)
            bm_append(gl, bm_box((0.30, 0.42, 0.05), mm @ T(0, 0, 0.025)), 0)
            bm_append(gl, grille(0.26, 0.36, 7, mm @ T(0, 0, 0.05)), None)
    make("glacis_vents", gl, [gray, dark], c_det, groups=["hull"])

    # ================================================================ HULL SIDES
    for s, side in sides:
        # conduit run in the groove between skirt and hull shoulder
        gx = s * 1.165
        conduit = bm_merge(
            (cyl_y(0.034, 0.034, 3.90, 16, gx, -1.10, 1.66), 0),
            (cyl_y(0.022, 0.022, 3.90, 12, s * 1.095, -1.10, 1.775), 1),
        )
        for y in (-2.85, -2.05, -1.05, 0.15, 0.75):
            bm_append(conduit, bm_box((0.22, 0.05, 0.05), T(s * 1.13, y, 1.72) @ Ry(s * 58.8)), 2)
        # elbows dropping into the hull at both ends
        for y0, y1 in ((-3.05, -3.15), (0.85, 1.05)):
            bm_append(conduit, bm_tube([(gx, y0, 1.66), (gx, y1, 1.66), (gx, y1, 1.55)], 0.034, 16), 0)
        make(f"side_conduit_{side}", conduit, [dark, steel, gray], c_det, groups=["hull"])
        # coil-spring dampers between skirt and hull, like a hover suspension
        for i, y in enumerate((-2.45, -1.55, 0.35)):
            p = (s * 1.24, y, 1.80)
            make(f"damper_{side}_{i + 1}", bm_merge(
                (bm_spring(T(*p) @ Rx(-90), 0.065, 0.014, 0.36, 5), 0),
                (cyl_y(0.022, 0.022, 0.50, 12, *p), 1),
                *[(cyl_y(0.085, 0.085, 0.035, 24, p[0], p[1] + dy, p[2]), 2) for dy in (-0.21, 0.21)],
                *[(bm_box((0.10, 0.06, 0.12), T(p[0], p[1] + dy, p[2] - 0.07)), 2) for dy in (-0.25, 0.25)]),
                [dark, steel, gray], c_det, groups=["hull"])

        # skirt: access hatches with pull handles on the lower facet
        hatches = bmesh.new()
        for y in (-2.65, -0.55, 1.55):
            zz = 0.72
            mm = T(s * (skirt_lo_x(zz) + 0.012), y, zz) @ Ry(s * SKIRT_LO_DEG)
            bm_append(hatches, bm_box((0.024, 0.46, 0.26), mm), 0)
            for dy in (-0.20, 0.20):
                bm_append(hatches, bm_box((0.03, 0.03, 0.08), mm @ T(s * 0.012, dy, 0.07)), 1)
            bm_append(hatches, bm_tube([mm @ Vector((s * 0.012, -0.08, -0.06)), mm @ Vector((s * 0.045, -0.08, -0.06)),
                                        mm @ Vector((s * 0.045, 0.08, -0.06)), mm @ Vector((s * 0.012, 0.08, -0.06))],
                                       0.009, 8), 1)
        make(f"skirt_hatches_{side}", hatches, [panel, dark], c_det, groups=["hull"])
        # chine stripe, step plates and grab rail on the upper facet
        run = bm_box((0.05, 5.45, 0.07), T(s * 1.80, -0.375, CHINE_Z))
        bm_append(run, bm_hull([(s * (x + dx), y, z + dz) for x, y, z in ((1.80, 2.40, CHINE_Z), (1.765, 3.80, 1.003))
                                for dx in (-0.025, 0.025) for dz in (-0.035, 0.035)]))
        make(f"skirt_stripe_{side}", run, accent, c_det, groups=["hull"])
        steps = bmesh.new()
        for y in (-2.95, 1.95):
            zz = 1.25
            mm = T(s * (skirt_up_x(zz) + 0.01), y, zz) @ Ry(-s * SKIRT_UP_DEG)
            bm_append(steps, bm_box((0.05, 0.30, 0.04), mm @ T(s * 0.02, 0, 0)), 0)
            for k in range(4):
                bm_append(steps, bm_box((0.052, 0.012, 0.042), mm @ T(s * 0.022, -0.105 + k * 0.07, 0.002)), 1)
        for y in (-1.95, -1.40):
            zz = 1.32
            # louvre slats face its local -Y; turn that out of the facet
            mm = T(s * (skirt_up_x(zz) + 0.005), y, zz) @ Ry(-s * SKIRT_UP_DEG) @ Rz(s * 90)
            bm_append(steps, louvre((0.34, 0.05, 0.20), mm, 5), None)
        for y in (-3.05, 2.10):
            ex = s * 1.52
            bm_append(steps, bm_box((0.10, 0.08, 0.03), T(ex, y, SKIRT_TOP + 0.015)), 0)
            bm_append(steps, bm_tube([(ex, y - 0.035, SKIRT_TOP + 0.03), (ex, y - 0.035, SKIRT_TOP + 0.075),
                                      (ex, y + 0.035, SKIRT_TOP + 0.075), (ex, y + 0.035, SKIRT_TOP + 0.03)],
                                     0.012, 8), 1)
        rail_x = s * (skirt_up_x(1.62) + 0.04)
        bm_append(steps, bm_tube([(rail_x - s * 0.04, -2.30, 1.62), (rail_x, -2.30, 1.66),
                                  (rail_x, -0.80, 1.66), (rail_x - s * 0.04, -0.80, 1.62)], 0.015, 10), 1)
        make(f"skirt_steps_{side}", steps, [gray, dark], c_det, groups=["hull"])
        # skirt-top greebles ahead of the dampers, and a marker light on each prong
        make(f"skirt_top_greebles_{side}", greebles(T(s * 1.45, 1.55, SKIRT_TOP), 0.30, 1.0, 21 + s, n=6, hmax=0.04),
             [gray, dark], c_det, groups=["hull"])
        # layered ram plate on the prong's upper facet
        def prong_pt(y, u):
            ty = (y - 2.25) / (3.82 - 2.25)
            cy_ = (y - 2.40) / (3.92 - 2.40)
            top = Vector((1.66 - 0.04 * ty, y, SKIRT_TOP - (SKIRT_TOP - 1.14) * ty))
            chn = Vector((1.80 - 0.04 * cy_, y, CHINE_Z - 0.05 * cy_))
            return tuple(top.lerp(chn, u))
        plate, bolts = applique(mirror([prong_pt(2.55, 0.10), prong_pt(3.45, 0.10),
                                        prong_pt(3.45, 0.90), prong_pt(2.55, 0.90)], s),
                                (s * 1.45, 3.0, 1.0), t=0.04, shrink=0.04)
        bm_append(bolts, plate, 1)
        make(f"prong_plate_{side}", bolts, [steel, panel], c_skirt, groups=["hull"])
        # bolted armor band along the upper facet, between the louvres and the prong plate
        band, bolts = applique(mirror([(skirt_up_x(1.56), -0.45, 1.56), (skirt_up_x(1.56), 2.15, 1.56),
                                       (skirt_up_x(1.40), 2.15, 1.40), (skirt_up_x(1.40), -0.45, 1.40)], s),
                               (s * 1.45, 0.8, 1.2), t=0.035, shrink=0.0)
        for y in (0.05, 0.70, 1.35):
            add_rivet(bolts, orient((s * (skirt_up_x(1.48) + 0.036), y, 1.48), (s * 0.98, 0, 0.196)))
        bm_append(bolts, band, 1)
        make(f"skirt_band_{side}", bolts, [steel, panel], c_skirt, groups=["hull"])
        # recessed access hatches on the skirt top, clear of the dampers
        top_h = bmesh.new()
        for y, ln in ((-2.00, 0.30), (-0.60, 0.56)):
            cx_ = s * 1.48
            bm_append(top_h, bm_box((0.24, ln, 0.006), T(cx_, y, SKIRT_TOP + 0.003)), 1)
            for dx, dy, w_, l_ in ((0, ln / 2, 0.28, 0.03), (0, -ln / 2, 0.28, 0.03),
                                   (0.13, 0, 0.03, ln), (-0.13, 0, 0.03, ln)):
                bm_append(top_h, bm_box((w_, l_, 0.02), T(cx_ + dx, y + dy, SKIRT_TOP + 0.01)), 0)
            bm_append(top_h, bm_tube([(cx_ - 0.05, y, SKIRT_TOP + 0.006), (cx_ - 0.05, y, SKIRT_TOP + 0.03),
                                      (cx_ + 0.05, y, SKIRT_TOP + 0.03), (cx_ + 0.05, y, SKIRT_TOP + 0.006)],
                                     0.008, 8), 2)
        make(f"skirt_top_hatches_{side}", top_h, [panel, dark, steel], c_det, groups=["hull"])
        make(f"prong_recess_greebles_{side}",
             greebles(on_plane((s * 1.215, 3.28, 0.84), (-s, 0, 0)), 0.40, 0.20, 61 + s, n=6, hmax=0.045),
             [gray, dark], c_det, groups=["hull"])
        make(f"prong_marker_{side}", bm_merge(
            (bm_box((0.05, 0.12, 0.07), T(s * 1.73, 3.70, 1.10) @ Rz(-s * 35)), 0),
            (bm_box((0.012, 0.08, 0.04), T(s * 1.755, 3.71, 1.10) @ Rz(-s * 35)), 1)),
            [dark, lamp], c_det, groups=["hull"])

    # ================================================================ DECK
    make("turret_ring", bm_merge(
        (bm_cyl(0.92, 0.92, 0.05, 48, T(*T0) @ T(0, 0, 0.01)), 0),
        *[(bm_box((0.05, 0.03, 0.02), T(*T0) @ Rz(a) @ T(0, 0.92, 0.015)), 1) for a in range(0, 360, 15)]),
        [dark, steel], c_hull, groups=["hull"])
    # forward deck between turret and brow: flush hatches and vents (inside the turret sweep)
    fd = bmesh.new()
    for x in (-0.70, 0.70):
        bm_append(fd, grille(0.30, 0.34, 6, T(x, 0.38, DECK + 0.002), depth=0.012), None)
    make("forward_deck_vents", fd, [gray, dark], c_det, groups=["hull"])

    # ================================================================ REAR
    ramp_pts = sym((RAMP_W, REAR_Y, 0.50), (RAMP_W, REAR_Y, RAMP_TOP),
                   (RAMP_W - 0.04, REAR_Y - 0.07, RAMP_TOP - 0.03), (RAMP_W - 0.04, REAR_Y - 0.07, 0.53))
    ramp = make("ramp", bm_hull(ramp_pts), [paint, paint_alt], c_rear,
                origin=(0, REAR_Y, 0.50), groups=["ramp"], bevel=0.01,
                panels=dict(cuts_z=(1.10,), cuts_x=(0.0,), alt=1, seed=9, rivet_step=0.22,
                            rivets_where=lambda c, n: n.y < -0.8))
    rr = REAR_Y - 0.07
    ribs = bmesh.new()
    for x in (-0.45, -0.15, 0.15, 0.45):
        bm_append(ribs, bm_hull([(x + dx, y, z) for dx in (-0.045, 0.045) for y, z in
                                 ((rr, 1.62), (rr - 0.05, 1.58), (rr, 1.20), (rr - 0.04, 1.22))]), 0)
    bm_append(ribs, bm_box((1.20, 0.05, 0.08), T(0, rr - 0.025, 1.10)), 1)
    bm_append(ribs, bm_box((1.20, 0.012, 0.025), T(0, rr - 0.052, 1.10)), 2)
    bm_append(ribs, grille(0.80, 0.30, 10, on_plane((0, rr, 0.78), (0, -1, 0))), None)
    bm_append(ribs, bm_tube([(-0.20, rr, 0.98), (-0.20, rr - 0.06, 0.98), (0.20, rr - 0.06, 0.98),
                             (0.20, rr, 0.98)], 0.014, 8), 1)
    bm_append(ribs, bm_cyl(0.06, 0.06, 0.04, 16, T(0.40, rr - 0.02, 0.98) @ Rx(90)), 1)
    bm_append(ribs, bm_box((0.18, 0.03, 0.06), T(0, rr - 0.015, 1.47)), 1)            # vision block
    bm_append(ribs, bm_box((0.13, 0.01, 0.025), T(0, rr - 0.032, 1.47)), 3)
    make("ramp_detail", ribs, [panel, dark, accent, glass], c_rear, origin=(0, REAR_Y, 0.50), groups=["ramp"],
         parent=ramp)
    make("ramp_hinge", bm_merge(*[cyl_x(0.04, 0.04, 0.22, 16, x, REAR_Y - 0.02, 0.52) for x in (-0.45, 0.0, 0.45)]),
         steel, c_rear, groups=["hull"])

    for s, side in sides:
        x = s * 0.95
        make(f"rear_louvre_{side}", louvre((0.40, 0.06, 0.56), T(x, REAR_Y - 0.03, 1.12), 8),
             [dark, gray], c_rear, groups=["hull"])
        make(f"rear_louvre_frame_{side}", bm_merge(
            *[(bm_box((0.46, 0.08, 0.04), T(x, REAR_Y - 0.04, 1.12 + dz)), 0) for dz in (-0.30, 0.30)],
            *[(bm_box((0.04, 0.08, 0.64), T(x + dx, REAR_Y - 0.04, 1.12)), 0) for dx in (-0.21, 0.21)]),
            gray, c_rear, groups=["hull"])
        make(f"taillight_housing_{side}", bm_box((0.22, 0.05, 0.10), T(x, REAR_Y - 0.025, 1.56)),
             dark, c_rear, groups=["hull"])
        make(f"taillight_{side}", bm_merge(*[bm_box((0.06, 0.02, 0.05), T(x + dx, REAR_Y - 0.055, 1.56))
                                            for dx in (-0.07, 0.0, 0.07)]),
             tail, c_rear, groups=[f"taillight_{side}"])
        make(f"tow_hook_{side}", bm_merge(
            bm_box((0.14, 0.08, 0.12), T(x, REAR_Y - 0.04, 0.68)),
            bm_tube([(x - 0.045, REAR_Y - 0.08, 0.66), (x - 0.045, REAR_Y - 0.15, 0.66),
                     (x + 0.045, REAR_Y - 0.15, 0.66), (x + 0.045, REAR_Y - 0.08, 0.66)], 0.02, 10)),
            dark, c_rear, groups=["hull"])
        # rear face greebles between louvre and skirt
        make(f"rear_greebles_{side}", greebles(on_plane((s * 1.02, REAR_Y, 0.62), (0, -1, 0)), 0.30, 0.18, 41 + s,
                                               n=4, hmax=0.04), [gray, dark], c_rear, groups=["hull"])
        # skirt rear face: a vent and a light
        make(f"skirt_rear_{side}", bm_merge(
            (louvre((0.24, 0.05, 0.36), T(s * 1.46, -3.27, 1.38), 6), None),
            (bm_box((0.10, 0.03, 0.06), T(s * 1.46, -3.20, 0.88)), 0)),
            [dark, gray], c_rear, groups=["hull"])

    # ================================================================ ENGINE DRUM
    make("engine_drum", drum_x(0, DRUM_R, 2 * DRUM_HALF), paint, c_eng, groups=["hull"])
    fins = bmesh.new()
    for k in range(21):
        bm_append(fins, drum_x(-0.32 + k * 0.032, DRUM_R + 0.055, 0.014), 0)
    for x in (-0.36, 0.36):
        bm_append(fins, drum_x(x, DRUM_R + 0.07, 0.04), 1)
    make("engine_drum_fins", fins, [dark, gray], c_eng, groups=["hull"])
    sleeves = bm_merge(
        *[(drum_x(s * 0.72, DRUM_R + 0.03, 0.56), 0) for s in (1, -1)],
        *[(drum_x(s * x, DRUM_R + 0.045, 0.03), 1) for s in (1, -1) for x in (0.46, 0.98)],
        *[(drum_x(s * 0.72, DRUM_R + 0.04, 0.07), 2) for s in (1, -1)],
    )
    make("engine_drum_sleeves", sleeves, [paint, gray, accent], c_eng, groups=["hull"],
         panels=None)
    caps = bmesh.new()
    for s in (1, -1):
        e = s * (DRUM_HALF + 0.07)
        bm_append(caps, drum_x(e, DRUM_R + 0.08, 0.14), 0)
        for r, w, mi in ((0.40, 0.025, 1), (0.32, 0.04, 0), (0.24, 0.025, 1), (0.13, 0.07, 0)):
            bm_append(caps, drum_x(e + s * (0.07 + w / 2), r, w), mi)
        bm_append(caps, drum_x(e + s * 0.14, 0.045, 0.04, 16), 1)
        for a in range(0, 360, 30):
            bm_append(caps, cyl_x(0.018, 0.018, 0.02, 8, e + s * 0.075,
                                  DRUM.y + 0.36 * math.cos(R(a)), DRUM.z + 0.36 * math.sin(R(a))), 2)
    make("engine_drum_caps", caps, [gray, dark, steel], c_eng, groups=["hull"])
    cradle = bm_merge(
        (bm_box_mm((-1.00, -3.22, DECK - 0.02), (1.00, -2.68, DECK + 0.06)), 0),
        *[(bm_hull([(x + dx, y, z) for dx in (-0.06, 0.06) for y, z in
                    ((-3.22, DECK), (-2.68, DECK), (-3.18, DECK + 0.16), (-2.72, DECK + 0.16))]), 0)
          for x in (-0.86, -0.45, 0.45, 0.86)],
        *[(bm_box((0.04, 0.04, 0.10), T(x, y, DECK + 0.10)), 1)
          for x in (-0.95, 0.95) for y in (-3.18, -2.72)],
    )
    make("engine_cradle", cradle, [gray, dark], c_eng, groups=["hull"], bevel=0.012)
    for s in (1, -1):
        hub = DRUM_HALF + 0.07 + 0.14 + 0.04
        bracket = bm_merge(
            (bm_hull([(s * x, y, z) for x in (hub, hub + 0.07) for y, z in
                      ((-3.20, SKIRT_TOP), (-2.70, SKIRT_TOP), (-3.03, DRUM.z + 0.06), (-2.87, DRUM.z + 0.06))]), 0),
            (cyl_x(0.10, 0.10, 0.08, 32, s * (hub + 0.035), DRUM.y, DRUM.z), 1),
            (cyl_x(0.06, 0.06, 0.04, 24, s * (hub + 0.09), DRUM.y, DRUM.z), 0),
            *[(cyl_x(0.014, 0.014, 0.02, 8, s * (hub + 0.08), DRUM.y + 0.075 * math.cos(R(a)),
                     DRUM.z + 0.075 * math.sin(R(a))), 2) for a in range(0, 360, 60)],
            (bm_box((0.30, 0.56, 0.04), T(s * (hub + 0.12), -2.95, SKIRT_TOP + 0.02)), 0),
        )
        make(f"drum_bracket_{'r' if s > 0 else 'l'}", bracket, [gray, dark, steel], c_eng, groups=["hull"],
             bevel=0.008)

    # coolant pipes from the drum down into the deck
    pipes = bmesh.new()
    for s in (1, -1):
        bm_append(pipes, bm_tube([(s * 0.20, -2.68, 2.30), (s * 0.20, -2.56, 2.20),
                                  (s * 0.20, -2.56, DECK + 0.02)], 0.03, 12), 0)
        bm_append(pipes, bm_cyl(0.05, 0.05, 0.03, 16, T(s * 0.20, -2.56, DECK + 0.015)), 1)
    for s in (1, -1):
        bm_append(pipes, bm_tube([(s * 1.10, -2.74, 1.86), (s * 1.10, -2.52, 1.90),
                                  (s * 1.17, -2.30, 1.78), (s * 1.17, -2.15, 1.68)], 0.028, 12), 1)
        bm_append(pipes, bm_tube([(s * 1.04, -2.74, 1.90), (s * 1.04, -2.50, 1.95),
                                  (s * 1.10, -2.30, 1.86), (s * 1.10, -2.15, 1.78)], 0.02, 10), 0)
        bm_append(pipes, bm_box((0.16, 0.08, 0.10), T(s * 1.12, -2.15, 1.72) @ Ry(s * 58.8)), 1)
    make("engine_pipes", pipes, [steel, dark], c_eng, groups=["hull"])
    for s, side in sides:
        x = s * EXHAUST_X
        ey = DRUM.y - DRUM_R + 0.06
        make(f"exhaust_{side}", bm_merge(
            (cyl_y(0.13, 0.15, 0.20, 32, x, ey - 0.10, EXHAUST_Z), 0),
            (cyl_y(0.17, 0.17, 0.035, 32, x, ey - 0.19, EXHAUST_Z), 0),
            (cyl_y(0.16, 0.16, 0.03, 32, x, ey - 0.02, EXHAUST_Z), 0),
            *[(bm_box((0.26, 0.012, 0.012), T(x, ey - 0.205, EXHAUST_Z) @ Ry(a)), 0) for a in (0, 60, 120)]),
            dark, c_eng, groups=["hull"])
        make(f"exhaust_glow_{side}", cyl_y(0.12, 0.12, 0.02, 32, x, ey - 0.19, EXHAUST_Z),
             thrust, c_eng, groups=["exhaust_glow"])

    # ================================================================ REPULSORS
    for i, (x, y, z, sx, sy_) in enumerate(REPULSORS, 1):
        make(f"repulsor_{i}", bm_box((sx, sy_, 0.07), T(x, y, z)), dark, c_rep, groups=["hull"])
        make(f"repulsor_glow_{i}", bm_box((sx - 0.08, sy_ - 0.12, 0.012), T(x, y, z - 0.04)),
             glow, c_rep, groups=["repulsor_glow"])
        n_bars = int(sy_ / 0.16)
        make(f"repulsor_grille_{i}", bm_merge(
            *[bm_box((sx - 0.04, 0.018, 0.018), T(x, y - sy_ / 2 + sy_ * (k + 0.5) / n_bars, z - 0.052))
              for k in range(n_bars)]),
             dark, c_rep, groups=["hull"])

    # ================================================================ TURRET
    turret = make("turret", bm_hull(tp(TURRET)), [paint, paint_alt], c_tur, origin=T0, groups=["turret"],
                  bevel=0.035, bevel_segs=2,
                  panels=dict(cuts_x=(-0.42, 0.42), cuts_y=tuple(T0.y + v for v in (-0.75, -0.15, 0.40)),
                              cuts_z=(T0.z + 0.24,), alt=1, seed=13, rivet_step=0.18,
                              rivets_where=lambda c, n: n.y > 0.45))

    def tur(name, bm, mats, groups=("turret",), origin=T0, collection=c_tur, bevel=0.0, parent=turret):
        return make(name, bm, mats, collection, origin=origin, groups=list(groups), parent=parent,
                    bevel=bevel)

    def tm(x, y, z):
        return T(*(T0 + Vector((x, y, z))))

    # roof: legion stripes, gunner sight, commander's sight head, gunner hatch
    tur("turret_stripes", bm_merge(*[bm_box((0.08, 0.95, 0.012), tm(sx * 0.62, -0.30, TROOF + 0.006))
                                     for sx in (1, -1)]), accent)
    tur("gunner_sight", bm_merge(
        (bm_box((0.24, 0.30, 0.16), tm(-0.30, 0.30, TROOF + 0.08)), 0),
        (bm_box((0.28, 0.10, 0.03), tm(-0.30, 0.42, TROOF + 0.175)), 0),
        *[(bm_box((0.02, 0.26, 0.12), tm(-0.30 + dx, 0.30, TROOF + 0.07)), 1) for dx in (-0.13, 0.13)]),
        [dark, gray])
    tur("gunner_sight_glass", bm_box((0.18, 0.015, 0.07), tm(-0.30, 0.455, TROOF + 0.09)), glass,
        groups=["turret", "glass"])
    cs = T0 + Vector((0.40, 0.25, TROOF))
    tur("commander_sight", bm_merge(
        (bm_cyl(0.13, 0.13, 0.05, 32, T(cs.x, cs.y, cs.z + 0.025)), 0),
        (bm_cyl(0.05, 0.05, 0.12, 16, T(cs.x, cs.y, cs.z + 0.11)), 1),
        (bm_box((0.20, 0.18, 0.13), T(cs.x, cs.y, cs.z + 0.23)), 0),
        (bm_box((0.22, 0.04, 0.03), T(cs.x, cs.y + 0.08, cs.z + 0.31)), 1),
        *[(cyl_x(0.03, 0.03, 0.05, 12, cs.x + dx, cs.y + 0.03, cs.z + 0.23), 1) for dx in (-0.125, 0.125)]),
        [gray, dark])
    tur("commander_sight_glass", bm_merge(
        *[cyl_y(0.035, 0.035, 0.02, 16, cs.x + dx, cs.y + 0.095, cs.z + 0.23) for dx in (-0.05, 0.05)]),
        glass, groups=["turret", "glass"])
    gh = T0 + Vector((0.04, -0.04, TROOF))
    tur("gunner_hatch_ring", bm_cyl(0.20, 0.20, 0.03, 32, T(gh.x, gh.y, gh.z + 0.015)), panel)
    peri = bmesh.new()
    for a in (-50, -15, 20, 55):
        mm = T(gh.x, gh.y, gh.z + 0.04) @ Rz(a) @ T(0, 0.25, 0)
        bm_append(peri, bm_box((0.08, 0.06, 0.07), mm), 0)
        bm_append(peri, bm_box((0.06, 0.01, 0.03), mm @ T(0, 0.031, 0.01)), 1)
    tur("gunner_periscopes", peri, [panel, glass])
    tur("hatch_gunner", bm_merge(
        (bm_cyl(0.165, 0.165, 0.03, 32, T(gh.x, gh.y, gh.z + 0.045)), 0),
        (bm_cyl(0.10, 0.10, 0.015, 24, T(gh.x, gh.y, gh.z + 0.067)), 0),
        (bm_tube([(gh.x - 0.06, gh.y + 0.05, gh.z + 0.06), (gh.x - 0.06, gh.y + 0.05, gh.z + 0.09),
                  (gh.x + 0.06, gh.y + 0.05, gh.z + 0.09), (gh.x + 0.06, gh.y + 0.05, gh.z + 0.06)], 0.01, 8), 1),
        (cyl_y(0.02, 0.02, 0.18, 12, gh.x + 0.165, gh.y, gh.z + 0.045), 1)),
        [panel, dark], groups=["turret", "hatch_gunner"], origin=(gh.x + 0.165, gh.y, gh.z + 0.045))

    # ---- VLS: armored block in the roof, 8 hinged hatches, rockets standing in the cells
    tur("vls_block", bm_hull(tp(sym((0.50, -1.18, 0.40), (0.50, -0.25, 0.40), (0.46, -1.15, VLS_TOP),
                                    (0.46, -0.28, VLS_TOP)))), [gray], bevel=0.015)
    tur("vls_frame", bm_merge(
        *[(bm_box((0.86, 0.025, 0.012), tm(0, y, VLS_TOP + 0.006)), 0)
          for y in (-1.14, -0.92, -0.70, -0.48, -0.26)],
        (bm_box((0.025, 0.90, 0.012), tm(0, -0.70, VLS_TOP + 0.006)), 0),
        *[(bm_box((0.04, 0.85, 0.05), tm(sx * 0.48, -0.70, VLS_TOP - 0.02)), 1) for sx in (1, -1)]),
        [dark, accent])
    for i, (cx, cy) in enumerate(VLS_CELLS, 1):
        c = T0 + Vector((cx, cy, 0))
        tur(f"vls_cell_{i}", bm_box((0.19, 0.19, 0.008), T(c.x, c.y, T0.z + VLS_TOP + 0.002)), dark)
        hinge = (math.copysign(VLS_HINGE, cx) + T0.x, c.y, T0.z + VLS_TOP)
        tur(f"vls_hatch_{i}", bm_merge(
            (bm_box((0.19, 0.19, 0.022), T(c.x, c.y, T0.z + VLS_TOP + 0.013)), 0),
            (bm_box((0.12, 0.12, 0.008), T(c.x, c.y, T0.z + VLS_TOP + 0.027)), 1),
            (cyl_y(0.012, 0.012, 0.16, 8, *hinge), 1)),
            [panel, gray], groups=["turret", f"vls_hatch_{i}"], origin=hinge)
        rz = T0.z + VLS_TOP
        rocket = bm_merge(
            (bm_cyl(0.065, 0.065, 0.48, 16, T(c.x, c.y, rz - 0.40)), 0),
            (bm_cyl(0.065, 0.006, 0.14, 16, T(c.x, c.y, rz - 0.09)), 1),
            *[(bm_box((0.004, 0.06, 0.08), T(c.x, c.y, rz - 0.60) @ Rz(a) @ T(0, 0.08, 0)), 2)
              for a in (0, 90, 180, 270)],
        )
        tur(f"rocket_{i}", rocket, [paint, accent, dark], groups=["turret", f"rocket_{i}"], collection=c_vls)

    # bolt-on armor on the front cheeks
    cheek = bmesh.new()
    cheek_bolts = bmesh.new()
    for s in (1, -1):
        plate, bolts = applique(tp(mirror([(1.00, 0.55, 0.04), (0.70, 0.95, 0.06), (0.52, 0.82, 0.37),
                                           (0.84, 0.45, 0.40)], s)), T0 + Vector((0, 0, 0.25)),
                                t=0.05, shrink=0.12)
        bm_append(cheek, plate)
        bm_append(cheek_bolts, bolts)
    bm_append(cheek_bolts, cheek, 1)
    tur("turret_cheek_armor", cheek_bolts, [steel, panel])
    tur("roof_dome", bm_merge(
        (bm_cyl(0.10, 0.10, 0.04, 24, tm(0.05, 0.40, TROOF + 0.02)), 0),
        (bm_sphere(0.085, tm(0.05, 0.40, TROOF + 0.05), 24, 12), 1)), [gray, panel])

    # ---- left cheek: ball sensor cluster on a bracket (reference's stacked spheres)
    bs = T0 + Vector((-0.95, 0.30, 0.28))
    tur("ball_sensors", bm_merge(
        (bm_box((0.10, 0.20, 0.42), T(bs.x + 0.03, bs.y, bs.z)), 0),
        *[(bm_sphere(0.075, T(bs.x - 0.08, bs.y + 0.02, bs.z + dz), 24, 12), 1) for dz in (-0.14, 0.0, 0.14)],
        *[(cyl_y(0.03, 0.03, 0.03, 16, bs.x - 0.08, bs.y + 0.09, bs.z + dz), 2) for dz in (-0.14, 0.0, 0.14)],
        *[(bm_box((0.06, 0.03, 0.03), T(bs.x - 0.02, bs.y + 0.02, bs.z + dz)), 0) for dz in (-0.14, 0.0, 0.14)]),
        [dark, panel, dark])
    tur("ball_sensor_lenses", bm_merge(*[cyl_y(0.022, 0.022, 0.01, 16, bs.x - 0.08, bs.y + 0.107, bs.z + dz)
                                         for dz in (-0.14, 0.0, 0.14)]), glass, groups=["turret", "glass"])
    # ---- right cheek: perforated cooling pack (reference's gridded box)
    cp = T0 + Vector((0.98, 0.20, 0.27))
    pack = bm_merge((bm_box((0.16, 0.46, 0.30), T(cp.x, cp.y, cp.z)), 0),
                    (bm_box((0.17, 0.50, 0.03), T(cp.x, cp.y, cp.z + 0.165)), 0))
    for iy in range(6):
        for iz in range(4):
            bm_append(pack, cyl_x(0.024, 0.024, 0.01, 8, cp.x + 0.082, cp.y - 0.175 + iy * 0.07,
                                  cp.z - 0.095 + iz * 0.065), 1)
    tur("cooling_pack", pack, [gray, dark], bevel=0.0)
    # ---- turret sides and rear: stowage bins, grab rails, antennas, rear greebles
    for s in (1, -1):
        tur(f"stowage_{'r' if s > 0 else 'l'}", bm_merge(
            (bm_box((0.14, 0.62, 0.24), tm(s * 0.97, -0.78, 0.22)), 0),
            *[(bm_box((0.02, 0.56, 0.02), tm(s * 1.045, -0.78, z)), 1) for z in (0.15, 0.22, 0.29)],
            *[(bm_box((0.03, 0.04, 0.26), tm(s * 1.045, y, 0.22)), 1) for y in (-1.05, -0.51)]),
            [gray, dark], bevel=0.0)
        tur(f"antenna_{'r' if s > 0 else 'l'}", bm_merge(
            (bm_cyl(0.045, 0.04, 0.07, 12, tm(s * 0.62, -1.15, TROOF + 0.035)), 0),
            (bm_cyl(0.008, 0.004, 1.10 if s > 0 else 0.80, 6, tm(s * 0.62, -1.15, TROOF + 0.07 + (0.55 if s > 0 else 0.40))), 0)),
            dark)
    for s in (1, -1):
        p = T0 + Vector((s * 0.935, -1.27, 0.22))
        # louvre slats face its local -Y; turn that outboard
        tur(f"bustle_gills_{'r' if s > 0 else 'l'}", louvre((0.14, 0.04, 0.24), T(*p) @ Rz(s * 90), 5),
            [dark, gray])
    tur("bustle_greebles", greebles(on_plane(T0 + Vector((0, -1.405, 0.24)), (0, -1, 0)), 1.40, 0.22, 51,
                                    n=8, hmax=0.04), [gray, dark])
    handles = bmesh.new()
    for x in (-0.45, 0.45):
        p = T0 + Vector((x, -1.41, 0.40))
        bm_append(handles, bm_tube([p + Vector((-0.10, 0.02, 0)), p + Vector((-0.10, -0.05, 0)),
                                    p + Vector((0.10, -0.05, 0)), p + Vector((0.10, 0.02, 0))], 0.012, 8))
    tur("bustle_handles", handles, dark)
    tur("turret_front_greebles", bm_merge(
        *[(cyl_y(0.035, 0.035, 0.06, 16, sx * 0.45, T0.y + 0.95, T0.z + 0.12), 1) for sx in (1, -1)],
        *[(bm_box((0.12, 0.05, 0.06), tm(sx * 0.48, 0.86, 0.30)), 0) for sx in (1, -1)]),
        [gray, dark])

    # ---- 50 mm autocannon
    gun = make("gun_mantlet", bm_hull(tp(MANTLET)), paint, c_gun, origin=G0,
               groups=["gun"], parent=turret, bevel=0.02,
               panels=dict(rivet_step=0.11, lift=0.005, rivets_where=lambda c, n: n.y > 0.5))
    gy, gz = G0.y, G0.z
    rf = G0 + Vector((0.18, 0.02, 0.21))
    make("gun_rangefinder", bm_merge(
        (bm_box((0.13, 0.30, 0.10), T(*rf)), 0),
        (cyl_y(0.035, 0.035, 0.04, 16, rf.x, rf.y + 0.16, rf.z), 1),
        (bm_box((0.15, 0.04, 0.02), T(rf.x, rf.y + 0.14, rf.z + 0.06)), 0),
        *[(bm_box((0.03, 0.06, 0.05), T(rf.x, rf.y + dy, rf.z - 0.07)), 1) for dy in (-0.09, 0.09)]),
        [gray, dark], c_gun, origin=G0, groups=["gun"], parent=gun)
    make("gun_rangefinder_glass", cyl_y(0.026, 0.026, 0.01, 16, rf.x, rf.y + 0.185, rf.z), glass,
         c_gun, origin=G0, groups=["gun", "glass"], parent=gun)

    def bar(d0, d1, r1, r2=None, segs=40, x=0.0, z=0.0):
        return cyl_y(r1, r2 if r2 is not None else r1, d1 - d0, segs, x, gy + (d0 + d1) / 2, gz + z)

    barrel = bm_merge(
        (bar(0.18, 0.30, 0.17, 0.17, 32), 1),                                   # collar on the mantlet
        (bar(0.30, 1.30, 0.11), 0),                                             # recoil sleeve
        *[(bar(d, d + 0.03, 0.13), 1) for d in (0.45, 0.62, 0.79, 0.96, 1.13)],  # heat-sink rings
        *[(bar(0.30, 1.05, 0.038, segs=16, x=sx * 0.125, z=-0.06), 1) for sx in (1, -1)],
        *[(bar(1.02, 1.08, 0.05, segs=16, x=sx * 0.125, z=-0.06), 0) for sx in (1, -1)],
        *[(bm_cyl(0.016, 0.016, 0.012, 10, T(0, gy + d, gz) @ Ry(a) @ T(0, 0, 0.107)), 2)
          for d in (0.535, 0.705, 0.875, 1.045) for a in range(-150, 180, 60)],     # sleeve cooling ports
        (bar(1.30, 1.40, 0.11, 0.075), 0),                                      # step taper
        (bar(1.40, 3.06, 0.065), 0),
        (bar(2.10, 2.16, 0.082), 1),
        (bar(2.60, 2.64, 0.075), 1),
        (bar(3.06, 3.36, 0.10), 1),                                             # muzzle brake
        (bar(3.36, 3.38, 0.085), 0),
        (bar(3.375, 3.385, 0.045, segs=16), 2),                                 # bore
        *[(bm_box((0.03, 0.05, 0.06), T(sx * 0.093, gy + d, gz)), 2) for sx in (1, -1) for d in (3.12, 3.21, 3.30)],
        *[(bm_box((0.06, 0.05, 0.03), T(0, gy + d, gz + 0.093)), 2) for d in (3.16, 3.26)],
    )
    make("gun_barrel_50mm", barrel, [dark, gray, steel], c_gun, origin=G0, groups=["gun"], parent=gun)

    # ================================================================ INTERIOR
    make("interior_floor", bm_box_mm((-1.14, -3.15, FLOOR - 0.03), (1.14, 2.40, FLOOR)),
         dark, c_int, groups=["interior"])
    seats = [("driver", DRIVER_X, FRONT_Y, 0, PAN, FLOOR),
             ("gunner", 0.0, T0.y - 0.15, 0, 1.45, 1.05)]
    n = 0
    for s, yaw in ((1, 90), (-1, -90)):
        for y in CARGO_Y:
            n += 1
            seats.append((f"cargo_{n:02d}", s * CARGO_X, y, yaw, PAN, FLOOR))
    seats.append(("cargo_13", -DRIVER_X, FRONT_Y, 0, PAN, FLOOR))

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
    sight = T0 + Vector((-0.30, 0.47, TROOF + 0.09))
    mem = {
        "osaveze": [tuple(T0), tuple(T0 + Vector((0, 0, 0.7)))],
        "osahlavne": [(-0.2, G0.y, G0.z), (0.2, G0.y, G0.z)],
        "konec hlavne": [(0, G0.y + 0.30, gz)],
        "usti hlavne": [(0, MUZZLE_Y, gz)],
        "gunnerview": [tuple(sight)],
        "commanderview": [tuple(cs + Vector((0, 0.10, 0.23)))],
        "driverview": [(DRIVER_X, brow_front_y(1.83) - 0.05, 1.83)],
        "ramp_axis": [(-RAMP_W, REAR_Y, 0.50), (RAMP_W, REAR_Y, 0.50)],
        "hatch_driver_axis": [(hx - 0.10, hy - 0.15, BROW_TOP + 0.06), (hx + 0.10, hy - 0.15, BROW_TOP + 0.06)],
        "hatch_gunner_axis": [(gh.x + 0.165, gh.y - 0.09, gh.z + 0.045), (gh.x + 0.165, gh.y + 0.09, gh.z + 0.045)],
        "pos driver": [(-0.6, -4.4, 0.3)],
        "pos gunner": [(0.6, -4.4, 0.3)],
        "pos cargo": [(0.0, -4.4, 0.3)],
        "light_l": [(-LENS_X[0], ARM_Y1 + 0.10, LENS_Z)], "light_l_end": [(-LENS_X[0], ARM_Y1 + 1.10, LENS_Z - 0.06)],
        "light_r": [(LENS_X[0], ARM_Y1 + 0.10, LENS_Z)], "light_r_end": [(LENS_X[0], ARM_Y1 + 1.10, LENS_Z - 0.06)],
    }
    ey = DRUM.y - DRUM_R + 0.06 - 0.20
    for s, side in sides:
        mem[f"exhaust_{side}"] = [(s * EXHAUST_X, ey, EXHAUST_Z)]
        mem[f"exhaust_{side}_dir"] = [(s * EXHAUST_X, ey - 1.0, EXHAUST_Z)]
    for i, (cx, cy) in enumerate(VLS_CELLS, 1):
        c = T0 + Vector((cx, cy, VLS_TOP))
        mem[f"missile_{i}"] = [tuple(c)]
        mem[f"missile_{i}_dir"] = [tuple(c + Vector((0, 0, 1.0)))]
        mem[f"vls_hatch_{i}_axis"] = [(T0.x + math.copysign(VLS_HINGE, cx), T0.y + cy + d, T0.z + VLS_TOP)
                                      for d in (-0.08, 0.08)]
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
    drum = [(x, DRUM.y + (DRUM_R + 0.08) * math.cos(a), DRUM.z + (DRUM_R + 0.08) * math.sin(a))
            for x in (-DRUM_HALF - 0.14, DRUM_HALF + 0.14)
            for a in (2 * math.pi * i / 8 for i in range(8))]
    geo_parts = [
        (HULL + BROW, ["hull"]),
        (list(SKIRT), ["hull"]),
        (mirror(SKIRT, -1), ["hull"]),
        (list(ARM), ["hull"]),
        (mirror(ARM, -1), ["hull"]),
        (drum, ["hull"]),
        (tp(TURRET) + tp(sym((0.50, -1.18, VLS_TOP), (0.50, -0.25, VLS_TOP))), ["turret"]),
        (tp(MANTLET) + sym((0.17, gy + 0.18, gz + 0.17), (0.17, gy + 0.18, gz - 0.17),
                           (0.10, MUZZLE_Y, gz + 0.10), (0.10, MUZZLE_Y, gz - 0.10)), ["gun"]),
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
