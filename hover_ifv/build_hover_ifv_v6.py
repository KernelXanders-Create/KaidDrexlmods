"""
Hover IFV model for Arma 3, v6 (Clone Wars Republic, high-detail slab-skirt).

Repulsorlift infantry fighting vehicle, Bradley-sized (about 7.0 m hull,
3.6 m wide, 2.7 m to the turret roof), 2 crew + 13 passengers, 50 mm
autocannon and an 8-cell vertical launch rocket system on the turret.

v3 restyled it as Clone Wars era Republic armor: a long flat shovel nose,
a long full-width crew cab, the turret moved aft to make room, chunky
bevelled armor, and Republic two-tone livery (white upper hull, gray
running gear) with legion-colored markings.

v4 turned the cab into an armored crew compartment with hooded vision
slots and added frontal armor.

v5 is a visual redesign inspired by (not copied from) heavy Republic
repulsor tanks: tall slab armor skirts that run past the nose as two
forward prongs around a recessed centre nose, two raised armor arms
over the glacis ending in twin lens clusters, a single long vision slit
for the cab, a banded transverse engine drum across the rear deck, and
ribbed vent boxes.

v6 keeps the v5 layout and spends a much bigger triangle budget (up to
~70k) on surface detail: panel-lined, riveted armor on the hull, skirts,
cab, arms, turret and ramp; a multi-segment engine drum on a cradle; a
ribbed rear door inside a tubular frame with louvered vents and tail
lights; coil-spring dampers on the turret; a finned sensor array; a
slotted muzzle brake; a round driver cupola with periscopes; grab rails,
hinges, handles and underside vents.

Pick the legion markings with LIVERY below or on the command line:
41st (green, default), republic (red), 501st (blue), 212th (orange).

Builds the whole model from scratch with bpy/bmesh, no add-ons needed.

Run headless:
    blender --background --python build_hover_ifv_v6.py -- --out hover_ifv_v6.blend [--livery 501st]
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
        nf.material_index = mat_index
    src.free()


def bm_merge(*parts):
    """parts: bmesh or (bmesh, material_index)."""
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
         smooth=35, bevel=0.0, panels=None):
    """Turn a world-space bmesh into an object whose origin sits at `origin`.

    `panels` runs the panel-line and rivet pass (see panelize); the rivets
    become a child object `<name>_rivets` with the same selections.
    """
    if bevel:
        bevel_edges(bm, bevel)
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
    "41st": (0.045, 0.10, 0.03),
    "republic": (0.40, 0.02, 0.015),
    "501st": (0.02, 0.06, 0.35),
    "212th": (0.70, 0.20, 0.02),
}


def bevel_edges(bm, width, min_angle=25):
    """Chamfer the hard edges for the chunky, animated-series armor look."""
    bm.normal_update()
    edges = [e for e in bm.edges
             if len(e.link_faces) == 2 and e.calc_face_angle(0) > R(min_angle)]
    if edges:
        bmesh.ops.bevel(bm, geom=edges, offset=width, segments=1, profile=0.5,
                        affect='EDGES', clamp_overlap=True)


# ----------------------------------------------------------- detail helpers

DETAIL = {}                               # materials the detail passes need, set in build()


def orient(p, n):
    """Matrix placing local +Z along normal `n` at point `p`."""
    return T(*p) @ Vector(n).to_track_quat('Z', 'Y').to_matrix().to_4x4()


def add_rivet(bm, mat):
    """Hex bolt head (16 tris, no hidden underside) placed by `mat`."""
    ring = []
    for z, r in ((-0.006, 0.011), (0.006, 0.008)):
        ring.append([bm.verts.new(mat @ Vector((r * math.cos(a), r * math.sin(a), z)))
                     for a in (math.pi * k / 3 for k in range(6))])
    for k in range(6):
        bm.faces.new((ring[0][k], ring[0][(k + 1) % 6], ring[1][(k + 1) % 6], ring[1][k]))
    bm.faces.new(ring[1])


def panelize(bm, cuts_x=(), cuts_y=(), cuts_z=(), groove=0.014, lift=0.008,
             rivet_step=0.26, rivet_inset=0.035, alt=None, seed=1, min_width=0.045,
             hidden=None):
    """Panel-line a hard-surface mesh and return a bmesh of rivets.

    Cuts the faces with axis-aligned planes, insets every face that is wide
    enough to leave a groove around it, raises the panel slightly, and lines
    the panel edges with rivets. `alt` recolours about a quarter of the
    slot-0 panels with that material slot for a patchwork plate look.
    Rivets are skipped on downward faces and wherever `hidden(centre, normal)`
    is true, since nobody sees them there and they cost triangles.
    """
    import random
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
             if f.calc_area() / max(f.calc_perimeter(), 1e-6) > min_width]
    bmesh.ops.inset_individual(bm, faces=faces, thickness=groove, depth=0.0,
                               use_even_offset=True)
    bmesh.ops.inset_individual(bm, faces=faces, thickness=0.004, depth=lift,
                               use_even_offset=True)
    bm.normal_update()
    rivets = bmesh.new()
    for f in faces:
        if alt is not None and f.material_index == 0 and rnd.random() < 0.25:
            f.material_index = alt
        if not rivet_step:
            continue
        c = f.calc_center_median()
        n = f.normal.copy()
        if n.z < -0.3 or (hidden and hidden(c, n)):
            continue
        vs = [v.co.copy() for v in f.verts]
        for a, b in zip(vs, vs[1:] + vs[:1]):
            d = b - a
            length = d.length
            count = int(length / rivet_step)
            if length < 0.12 or count < 1:
                continue
            d.normalize()
            inward = n.cross(d).normalized()
            if inward.dot(c - (a + b) / 2) < 0:
                inward = -inward
            for k in range(count):
                p = a + d * length * (k + 0.5) / count + inward * rivet_inset + n * 0.003
                add_rivet(rivets, orient(p, n))
    return rivets


def bm_tube(pts, r, segs=12):
    """Tube along a polyline with ball joints at the bends (rails, frames)."""
    out = bmesh.new()
    pts = [Vector(p) for p in pts]
    for a, b in zip(pts, pts[1:]):
        d = b - a
        bm_append(out, bm_cyl(r, r, d.length, segs, orient((a + b) / 2, d)))
    for p in pts[1:-1]:
        ball = bmesh.new()
        bmesh.ops.create_uvsphere(ball, u_segments=segs, v_segments=6, radius=r * 1.05,
                                  matrix=T(*p))
        bm_append(out, ball)
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
    """Recessed vent: a dark frame box with `slats` angled blades across it."""
    sx, sy, sz = size
    out = bm_merge((bm_box(size, mat), 0))
    for i in range(slats):
        z = -sz / 2 + sz * (i + 0.5) / slats
        bm_append(out, bm_box((sx * 0.9, slat_depth, sz / slats * 0.55),
                              mat @ T(0, -sy / 2 - slat_depth / 2, z) @ Rx(-25)), 1)
    return out


# -------------------------------------------------------------- dimensions

# Hull: belly 0.50 m off the ground, roof at 2.05 m, long flat shovel nose.
HULL = sym(
    (1.25, -3.05, 0.50), (1.25, 2.80, 0.50),    # belly
    (1.62, -3.30, 0.95), (1.62, 3.00, 0.95),    # lower chine
    (1.50, -3.30, 1.75), (1.50, 1.20, 1.75),    # upper shoulder
    (1.10, -3.20, 2.05), (1.10, 0.30, 2.05),    # roof (turret deck)
    (1.05, 3.75, 0.95), (0.95, 3.70, 0.70),     # shovel prow
)
GLACIS_DEG = math.degrees(math.atan2(2.05 - 0.95, 3.75 - 0.30))


def glacis_z(y):
    return 2.05 - (y - 0.30) * (2.05 - 0.95) / (3.75 - 0.30)


def side_x(z):
    """Hull side surface between chine and shoulder."""
    return 1.62 - 0.12 * (z - 0.95) / 0.80


SIDE_DEG = math.degrees(math.atan2(0.12, 0.80))

# Slab armor skirt (right side; mirrored for the left). Faceted outer face with
# a chine, running forward past the nose as a raked prong.
SKIRT = (
    (1.68, -3.30, 1.55), (1.84, -3.35, 0.95), (1.62, -3.20, 0.40),     # rear, outer
    (1.46, -3.30, 1.55), (1.40, -3.20, 0.40),                          # rear, inner
    (1.66, 4.20, 1.50), (1.80, 4.05, 0.95), (1.60, 3.45, 0.40),        # prong, outer
    (1.48, 4.20, 1.50), (1.44, 4.05, 0.95), (1.40, 3.45, 0.40),        # prong, inner
)
SKIRT_PANEL_DEG = math.degrees(math.atan2(1.84 - 1.68, 1.55 - 0.95))
SKIRT_LOWER_DEG = math.degrees(math.atan2(1.84 - 1.62, 0.95 - 0.40))


def skirt_lower_x(z):
    """Lower outer facet of the skirt, between the chine and the bottom edge."""
    return 1.62 + (1.84 - 1.62) * (z - 0.40) / (0.95 - 0.40)


def skirt_x(z):
    """Upper outer facet of the skirt, between its top edge and the chine."""
    return 1.68 + (1.84 - 1.68) * (1.55 - z) / (1.55 - 0.95)

# Armored crew cab riding on the glacis, full width, below the turret's sweep:
# sloped brow, then a steep armored front that carries the vision slots.
CAB = sym(
    (0.85, 0.75, 2.02), (0.85, 2.25, 2.02),     # roof
    (0.89, 2.55, 1.88),                         # brow edge, top of the armored front
    (0.95, 2.80, 1.50),                         # foot of the armored front
    (0.95, 0.75, 1.70), (0.95, 2.55, 1.70),     # flat side wall for the side slots
    (0.98, 0.70, 1.60), (0.98, 3.05, 1.10),     # base, sunk below the glacis
)
BROW_DEG = math.degrees(math.atan2(2.02 - 1.88, 2.55 - 2.25))
FRONT_DEG = math.degrees(math.atan2(1.88 - 1.50, 2.80 - 2.55))
BROW_MID = Vector((0.0, 2.40, 1.95))
SLOT_LINE = Vector((0.0, 2.6125, 1.785))  # a quarter of the way down the armored front
FRONT_PLATE = Vector((0.0, 2.7125, 1.633))
CAB_SIDE_DEG = math.degrees(math.atan2(0.95 - 0.85, 2.02 - 1.70))
CUPOLA = (-0.45, 1.55)                    # over the driver; stays under the gun's sweep


def cab_wall_x(z):
    return 0.85 + (2.02 - z) * (0.95 - 0.85) / (2.02 - 1.70)


# Raised armor arm (right side; mirrored): rides the cab brow, then angles out
# and down over the glacis to a lens cluster ahead of the recessed nose.
ARM = (
    (0.55, 2.30, 2.06), (0.85, 2.30, 2.06), (0.55, 2.30, 1.84), (0.85, 2.30, 1.84),
    (0.95, 3.95, 1.08), (1.25, 3.95, 1.08), (0.95, 3.95, 0.80), (1.25, 3.95, 0.80),
)
LENS_Z = 0.94
LENS_X = (1.03, 1.17)                     # inner lens is the headlight


def arm_bottom_z(y):
    return 1.84 - (y - 2.30) * (1.84 - 0.80) / (3.95 - 2.30)


def arm_inner_x(y):
    return 0.55 + (y - 2.30) * (0.95 - 0.55) / (3.95 - 2.30)

T0 = Vector((0.0, -0.35, 2.05))          # turret rotation axis, moved aft for the cab
TURRET = sym(
    (1.10, -1.15, 0.02), (1.10, 0.65, 0.02), (0.85, 1.05, 0.04), (0.45, 1.40, 0.08),
    (0.80, -1.10, 0.50), (0.80, 0.55, 0.50), (0.60, 0.90, 0.46), (0.35, 1.10, 0.40),
    (1.00, -1.35, 0.20), (0.85, -1.35, 0.45),            # rear bustle
)
MANTLET = sym((0.30, 1.00, 0.10), (0.30, 1.00, 0.44),
              (0.24, 1.42, 0.15), (0.24, 1.42, 0.38))
G0 = T0 + Vector((0.0, 1.15, 0.27))      # gun elevation pivot
MUZZLE_Y = T0.y + 4.10

VLS_CELLS = [(sx * 0.27, cy) for cy in (-0.93, -0.71, -0.49, -0.27) for sx in (-1, 1)]
VLS_TOP = 0.64                            # turret-relative

# Transverse engine drum across the rear deck, exhausts on its rear face.
DRUM = Vector((0.0, -3.15, 2.22))
DRUM_R, DRUM_HALF = 0.40, 1.10
EXHAUST_X, EXHAUST_Z = 0.70, 2.15
EXHAUST_Y = -3.66

FLOOR = 0.58
PAN = 1.02                                # passenger seat height
CARGO_Y = (-2.70, -2.10, -1.50, -0.90, -0.30, 0.30)
CARGO_X = 1.18
FRONT_Y = 1.75                            # driver and front passenger, inside the cab
# (x, y, z, size_x, size_y): 3 strips under each skirt, 2 plates under the belly
REPULSORS = ([(s * 1.51, y, 0.36, 0.22, 1.30) for s in (1, -1) for y in (-2.20, -0.45, 1.30)]
             + [(0.0, -1.45, 0.47, 1.40, 1.10), (0.0, 1.25, 0.47, 1.40, 1.10)])


def tp(pts):
    """Turret-relative points to world."""
    return [tuple(Vector(p) + T0) for p in pts]


def on_slope(base, deg, lift):
    """Matrix for a part lying on a surface tilted `deg` nose-down about X."""
    n = Vector((0, math.sin(R(deg)), math.cos(R(deg))))
    return T(*(Vector(base) + n * lift)) @ Rx(-deg)


def cyl_y(r1, r2, depth, segs, x, y, z, spin=0):
    """Cylinder along +Y; r1 at the rear end, r2 at the front end."""
    return bm_cyl(r1, r2, depth, segs, T(x, y, z) @ Rx(-90) @ Rz(spin))


def ring_pts(x, y, z, r, segs=8):
    return [(x + r * math.cos(a), y, z + r * math.sin(a))
            for a in (2 * math.pi * i / segs for i in range(segs))]


def drum_x(x, r, depth, segs=32):
    """Cylinder segment of the engine drum, axis along X."""
    return bm_cyl(r, r, depth, segs, T(x, DRUM.y, DRUM.z) @ Ry(90))


def two_tone(bm, below_z):
    """Faces under `below_z` take material slot 1 (running-gear gray)."""
    for f in bm.faces:
        f.material_index = 1 if f.calc_center_median().z < below_z else 0
    return bm


# ------------------------------------------------------------------- build

def build(livery=LIVERY):
    clear_scene()
    scn = bpy.context.scene
    scn.unit_settings.system = 'METRIC'
    scn.unit_settings.scale_length = 1.0

    root = coll("HoverIFV_v6")
    vis = coll("LOD_Resolution_0", root)
    c_hull = coll("Hull", vis)
    c_det = coll("Hull_Details", vis)
    c_eng = coll("Engines", vis)
    c_rep = coll("Repulsors", vis)
    c_tur = coll("Turret", vis)
    c_vls = coll("VLS_Rockets", vis)
    c_int = coll("Interior_Seats", vis)
    c_geo = coll("LOD_Geometry", root)
    c_mem = coll("LOD_Memory", root)
    c_crew = coll("Crew_Positions", root)
    coll("LOD_FireGeometry_TODO", root)
    coll("LOD_ViewGeometry_TODO", root)

    paint = material("hull_white", (0.80, 0.80, 0.77), rough=0.5)
    gray = material("hull_gray", (0.11, 0.115, 0.12), rough=0.55)
    panel = material("armor_panel", (0.45, 0.45, 0.44), rough=0.55)
    dark = material("dark_metal", (0.07, 0.075, 0.08), rough=0.4, metal=0.7)
    accent = material(f"legion_{livery}", LIVERIES[livery], rough=0.5)
    glass = material("glass", (0.015, 0.05, 0.05), rough=0.06, metal=0.4)
    glow = material("repulsor_glow", (0.1, 0.3, 0.5), emit=(0.35, 0.75, 1.0), strength=6.0)
    thrust = material("thruster_glow", (0.1, 0.2, 0.5), emit=(0.45, 0.6, 1.0), strength=10.0)
    lamp = material("headlight", (0.9, 0.9, 0.8), emit=(1.0, 0.92, 0.75), strength=5.0)
    seat_m = material("seat", (0.16, 0.16, 0.14), rough=0.8)
    paint_alt = material("hull_white_alt", (0.70, 0.70, 0.67), rough=0.55)
    gray_alt = material("hull_gray_alt", (0.085, 0.09, 0.095), rough=0.6)
    tail = material("taillight", (0.5, 0.02, 0.02), emit=(1.0, 0.08, 0.05), strength=4.0)
    DETAIL["rivet"] = dark

    # ---- hull, skirts, cab (two-tone, chamfered)
    make("hull", two_tone(bm_hull(HULL), 0.97), [paint, gray, paint_alt], c_hull, groups=["hull"],
         bevel=0.04, panels=dict(cuts_x=(-0.55, 0.55), cuts_y=(-2.4, -1.5, -0.6, 0.3, 1.2, 2.1, 3.0),
                                 cuts_z=(1.30,), alt=2, seed=11, rivet_step=0.30,
                                 hidden=lambda c, n: abs(c.x) > 1.25 and c.z < 1.56))
    for s, side in ((1, "r"), (-1, "l")):
        make(f"skirt_{side}", bm_hull([(s * x, y, z) for x, y, z in SKIRT]),
             [gray, gray_alt], c_hull, groups=["hull"], bevel=0.03,
             panels=dict(cuts_y=(-2.25, -1.20, -0.15, 0.90, 1.95, 3.00), cuts_z=(1.25, 0.68),
                         alt=1, seed=3 if s > 0 else 4, rivet_step=0.22,
                         hidden=lambda c, n: n.x * math.copysign(1, c.x) < -0.5 and c.y < 3.0))
    make("cab", bm_hull(CAB), [paint, paint_alt], c_hull, groups=["hull"], bevel=0.035,
         panels=dict(cuts_x=(-0.30, 0.30), cuts_y=(1.25, 1.75), alt=1, seed=5))

    # armored brow overhanging the front, legion stripe along its lip
    make("cab_brow_armor", bm_box((1.72, 0.40, 0.05), on_slope(BROW_MID, BROW_DEG, 0.025) @ T(0, 0.04, 0)),
         panel, c_hull, groups=["hull"], bevel=0.012)
    make("cab_brow_stripe", bm_box((1.72, 0.06, 0.012), on_slope(BROW_MID, BROW_DEG, 0.056) @ T(0, 0.17, 0)),
         accent, c_det, groups=["hull"])

    # vision slit: one long armored block between the arms, hood above it
    slot_blocks, slot_glass, hoods = bmesh.new(), bmesh.new(), bmesh.new()
    m = on_slope(SLOT_LINE, FRONT_DEG, 0.0)
    bm_append(slot_blocks, bm_box((0.96, 0.14, 0.06), m @ T(0, 0, 0.03)))
    bm_append(slot_glass, bm_box((0.86, 0.035, 0.01), m @ T(0, 0, 0.063)))
    bm_append(hoods, bm_box((1.00, 0.025, 0.11), m @ T(0, -0.08, 0.055)))
    for s in (1, -1):
        for y in (1.30, 1.95):
            m = T(s * cab_wall_x(1.86), y, 1.86) @ Ry(-s * CAB_SIDE_DEG)
            bm_append(slot_blocks, bm_box((0.04, 0.32, 0.10), m @ T(s * 0.02, 0, 0)))
            bm_append(slot_glass, bm_box((0.01, 0.24, 0.03), m @ T(s * 0.043, 0, 0)))
            bm_append(hoods, bm_box((0.08, 0.36, 0.025), m @ T(s * 0.04, 0, 0.065)))
    make("cab_slot_blocks", slot_blocks, dark, c_hull, groups=["hull"])
    make("cab_slot_glass", slot_glass, glass, c_hull, groups=["hull", "glass"])
    make("cab_slot_hoods", hoods, panel, c_det, groups=["hull"])

    # add-on armor plate across the cab front, below the slots, with bolt heads
    plate = bm_box((1.00, 0.20, 0.06), on_slope(FRONT_PLATE, FRONT_DEG, 0.03))
    for x in (-0.40, -0.13, 0.13, 0.40):
        bm_append(plate, bm_box((0.04, 0.04, 0.02), on_slope(FRONT_PLATE + Vector((x, 0, 0)), FRONT_DEG, 0.07)), 1)
    make("cab_front_armor", plate, [panel, dark], c_hull, groups=["hull"])
    # driver cupola: armored ring, periscope blocks around the front arc, round lid
    cx, cy = CUPOLA
    ring = bm_merge((bm_cyl(0.30, 0.30, 0.08, 32, T(cx, cy, 2.05)), 0))
    for a in (30, 60, 90, 120, 150):
        m = T(cx, cy, 2.105) @ Rz(a - 90) @ T(0, 0.25, 0)
        bm_append(ring, bm_box((0.10, 0.06, 0.045), m), 0)
        bm_append(ring, bm_box((0.07, 0.01, 0.025), m @ T(0, 0.032, 0)), 1)
    make("cupola", ring, [panel, glass], c_hull, groups=["hull"])
    lid = bm_merge(
        (bm_cyl(0.22, 0.22, 0.035, 32, T(cx, cy, 2.107)), 0),
        (bm_tube([(cx - 0.07, cy + 0.05, 2.125), (cx - 0.07, cy + 0.05, 2.15),
                  (cx + 0.07, cy + 0.05, 2.15), (cx + 0.07, cy + 0.05, 2.125)], 0.01, 8), 1),
        (bm_cyl(0.025, 0.025, 0.30, 12, T(cx, cy - 0.22, 2.10) @ Ry(90)), 1),
    )
    make("hatch_driver", lid, [panel, dark], c_hull, origin=(cx, cy - 0.22, 2.09),
         groups=["hatch_driver"])
    for s in (1, -1):
        x = s * (cab_wall_x(1.94) + 0.05)
        make(f"cab_rail_{'r' if s > 0 else 'l'}",
             bm_tube([(x - s * 0.05, 1.0, 1.90), (x, 1.0, 1.98), (x, 2.15, 1.98), (x - s * 0.05, 2.15, 1.90)],
                     0.016, 10), dark, c_det, groups=["hull"])

    # frontal armor: layered glacis plates between the arms, recessed nose sensor
    gbase = (0.0, 3.38, glacis_z(3.38))
    glacis = bm_merge(
        (bm_box((1.30, 0.62, 0.08), on_slope(gbase, GLACIS_DEG, 0.04)), 0),
        (bm_box((1.00, 0.40, 0.06), on_slope(gbase, GLACIS_DEG, 0.11) @ T(0, -0.02, 0)), 0),
        (bm_box((1.00, 0.05, 0.01), on_slope(gbase, GLACIS_DEG, 0.145) @ T(0, 0.12, 0)), 1),
        *[(bm_box((0.04, 0.04, 0.02), on_slope(gbase, GLACIS_DEG, 0.09) @ T(x, 0.26, 0)), 2)
          for x in (-0.55, -0.35, 0.35, 0.55)],
    )
    make("glacis_armor", glacis, [panel, accent, dark], c_hull, groups=["hull"])
    make("nose_sensor", bm_merge(
        (cyl_y(0.14, 0.14, 0.04, 16, 0, 3.735, 0.83), 0),
        (cyl_y(0.10, 0.10, 0.02, 16, 0, 3.765, 0.83), 1)), [dark, glass], c_det, groups=["hull", "glass"])

    # raised armor arms over the glacis, each ending in a twin lens cluster
    for s, side in ((1, "r"), (-1, "l")):
        make(f"armor_arm_{side}", bm_hull([(s * x, y, z) for x, y, z in ARM]),
             [paint, paint_alt], c_hull, groups=["hull"], bevel=0.025,
             panels=dict(cuts_y=(2.85, 3.40), alt=1, seed=7 if s > 0 else 8, rivet_step=0.18))
        stripe = []
        for y in (2.40, 3.85):
            t = (y - 2.30) / (3.95 - 2.30)
            x, z = 0.70 + 0.40 * t, 2.06 - 0.98 * t
            stripe += [(s * (x + dx), y, z + dz) for dx in (-0.03, 0.03) for dz in (0.004, 0.016)]
        make(f"arm_stripe_{side}", bm_hull(stripe), accent, c_det, groups=["hull"])
        py = 3.15
        make(f"arm_pylon_{side}", bm_box((0.20, 0.20, arm_bottom_z(py) - glacis_z(py) + 0.06),
                                         T(s * (arm_inner_x(py) + 0.15), py, (arm_bottom_z(py) + glacis_z(py)) / 2)),
             dark, c_det, groups=["hull"])
        housing = bm_merge(*[cyl_y(0.075, 0.075, 0.06, 24, s * x, 3.97, LENS_Z) for x in LENS_X])
        make(f"lens_housing_{side}", housing, dark, c_det, groups=["hull"])
        make(f"light_{side}", cyl_y(0.055, 0.055, 0.02, 24, s * LENS_X[0], 4.005, LENS_Z),
             lamp, c_det, groups=[f"light_{side}"])
        make(f"arm_sensor_{side}", cyl_y(0.055, 0.055, 0.02, 24, s * LENS_X[1], 4.005, LENS_Z),
             glass, c_det, groups=["hull", "glass"])

    # ---- side armor, pipes, pod stripes, lights, deck hatches
    for s, side in ((1, "r"), (-1, "l")):
        # access hatches with pull handles on the lower skirt facet
        hatches = bmesh.new()
        for y in (-2.70, -0.65, 1.45):
            m = T(s * (skirt_lower_x(0.70) + 0.02), y, 0.70) @ Ry(s * SKIRT_LOWER_DEG)
            bm_append(hatches, bm_box((0.025, 0.42, 0.24), m), 0)
            bm_append(hatches, bm_tube([m @ Vector((s * 0.012, -0.08, 0.06)), m @ Vector((s * 0.045, -0.08, 0.06)),
                                        m @ Vector((s * 0.045, 0.08, 0.06)), m @ Vector((s * 0.012, 0.08, 0.06))],
                                       0.009, 8), 1)
        make(f"skirt_hatches_{side}", hatches, [panel, dark], c_det, groups=["hull"])
        pipes = bm_merge(
            cyl_y(0.035, 0.035, 3.2, 16, s * (side_x(1.66) + 0.04), -0.20, 1.66),
            *[bm_box((0.07, 0.05, 0.12), T(s * (side_x(1.66) + 0.03), y, 1.66)) for y in (-1.6, -0.5, 0.6, 1.3)],
        )
        make(f"side_pipes_{side}", pipes, dark, c_det, groups=["hull"])
        make(f"skirt_stripe_{side}", bm_box((0.10, 6.4, 0.02), T(s * 1.57, 0.25, 1.568)),
             accent, c_det, groups=["hull"])

        make(f"rear_vent_{side}", louvre((0.45, 0.06, 0.45), T(s * 1.12, -3.33, 1.30), 8),
             [dark, panel], c_det, groups=["hull"])
        make(f"taillight_housing_{side}", bm_box((0.18, 0.04, 0.10), T(s * 1.20, -3.32, 1.64)),
             dark, c_det, groups=["hull"])
        make(f"taillight_{side}", bm_box((0.13, 0.02, 0.05), T(s * 1.20, -3.345, 1.64)),
             tail, c_det, groups=[f"taillight_{side}"])
        make(f"tow_hook_{side}", bm_merge(
            bm_box((0.12, 0.08, 0.10), T(s * 1.05, -3.30, 0.80)),
            bm_tube([(s * 1.01, -3.34, 0.78), (s * 1.01, -3.40, 0.78), (s * 1.09, -3.40, 0.78),
                     (s * 1.09, -3.34, 0.78)], 0.018, 8)), dark, c_det, groups=["hull"])

        hatch = make(f"hatch_cargo_{side}", bm_box((0.60, 0.60, 0.05), T(s * 0.60, -2.30, 2.075)),
                     panel, c_hull, origin=(s * 0.90, -2.30, 2.05), groups=[f"hatch_cargo_{side}"],
                     panels=dict(rivet_step=0.14, lift=0.004))
        make(f"hatch_cargo_{side}_hardware", bm_merge(
            *[bm_cyl(0.022, 0.022, 0.14, 12, T(s * 0.90, y, 2.075) @ Rx(90)) for y in (-2.45, -2.15)],
            bm_tube([(s * 0.40, -2.38, 2.10), (s * 0.40, -2.38, 2.13), (s * 0.40, -2.22, 2.13),
                     (s * 0.40, -2.22, 2.10)], 0.01, 8)),
             dark, c_hull, origin=(s * 0.90, -2.30, 2.05), groups=[f"hatch_cargo_{side}"], parent=hatch)

    # ---- rear deck: ribbed vent boxes and whip antenna (outside the turret's sweep)
    ribbed = bmesh.new()
    for y in (-2.45, -2.10):
        bm_append(ribbed, bm_box((0.16, 0.30, 0.10), T(-0.99, y, 2.10)))
        for dx in (-0.063, -0.045, -0.027, -0.009, 0.009, 0.027, 0.045, 0.063):
            bm_append(ribbed, bm_box((0.012, 0.28, 0.035), T(-0.99 + dx, y, 2.165)), 1)
    make("deck_vents", ribbed, [gray, dark], c_det, groups=["hull"])
    whip = bm_merge(
        bm_cyl(0.045, 0.04, 0.06, 8, T(1.00, -1.95, 2.08)),
        bm_cyl(0.010, 0.005, 1.30, 6, T(1.00, -1.95, 2.76)),
    )
    make("antenna", whip, dark, c_det, groups=["hull"])

    # ---- rear ramp
    ramp_pts = sym((0.80, -3.35, 0.55), (0.80, -3.35, 1.75), (0.80, -3.28, 1.75),
                   (0.80, -3.28, 0.95), (0.80, -3.03, 0.55))
    ramp = make("ramp", bm_hull(ramp_pts), [paint, paint_alt], c_hull,
                origin=(0, -3.20, 0.55), groups=["ramp"],
                panels=dict(cuts_z=(1.05,), alt=1, seed=9, rivet_step=0.2))
    ribs = bmesh.new()
    for x in (-0.56, -0.28, 0.0, 0.28, 0.56):
        bm_append(ribs, bm_hull([(x + dx, y, z) for dx in (-0.05, 0.05) for y, z in
                                 ((-3.36, 1.72), (-3.42, 1.72), (-3.36, 1.12), (-3.38, 1.12))]), 0)
        bm_append(ribs, bm_hull([(x + dx, y, z) for dx in (-0.035, 0.035) for y, z in
                                 ((-3.36, 0.95), (-3.39, 0.95), (-3.36, 0.62), (-3.375, 0.62))]), 0)
    bm_append(ribs, bm_box((1.52, 0.06, 0.06), T(0, -3.39, 1.03)), 1)
    bm_append(ribs, bm_box((1.52, 0.012, 0.02), T(0, -3.424, 1.03)), 2)
    make("ramp_ribs", ribs, [panel, gray, accent], c_hull, origin=(0, -3.20, 0.55), groups=["ramp"],
         parent=ramp)

    # tubular frame around the door, standoffs back to the hull, marker lights
    frame = bm_tube([(-0.88, -3.44, 0.55), (-0.88, -3.44, 1.88), (0.88, -3.44, 1.88),
                     (0.88, -3.44, 0.55)], 0.035, 12)
    for p in ((-0.88, 0.65), (-0.88, 1.80), (0.88, 0.65), (0.88, 1.80), (0.0, 1.88)):
        bm_append(frame, bm_box((0.06, 0.13, 0.06), T(p[0], -3.38, p[1])))
    make("rear_frame", frame, dark, c_det, groups=["hull"])
    for s, side in ((1, "r"), (-1, "l")):
        make(f"frame_light_{side}", bm_merge(
            (bm_box((0.09, 0.06, 0.09), T(s * 0.88, -3.49, 1.25)), 0),
            (cyl_y(0.03, 0.03, 0.01, 16, s * 0.88, -3.525, 1.25), 1)), [dark, lamp], c_det, groups=["hull"])

    make("turret_ring", bm_cyl(0.90, 0.90, 0.08, 24, T(*T0)), dark, c_hull, groups=["hull"])

    # ---- transverse engine drum: banded body, ribbed centre, heavy end caps
    make("engine_drum", drum_x(0, DRUM_R, 2 * DRUM_HALF, 48), paint, c_eng, groups=["hull"])
    sleeves = bm_merge(
        *[(drum_x(s * 0.86, DRUM_R + 0.035, 0.48, 48), 0) for s in (1, -1)],
        *[(drum_x(s * x, DRUM_R + 0.045, 0.03, 48), 1) for s in (1, -1) for x in (0.63, 1.09)],
        *[(drum_x(s * 0.86, DRUM_R + 0.04, 0.02, 48), 1) for s in (1, -1)],
    )
    make("engine_drum_sleeves", sleeves, [paint, gray], c_eng, groups=["hull"])
    bands = bm_merge(
        *[(drum_x(x, DRUM_R + 0.03, 0.025, 48), 0) for x in (-0.30, -0.225, -0.15, -0.075, 0.0, 0.075, 0.15, 0.225, 0.30)],
        *[(drum_x(x, DRUM_R + 0.03, 0.06, 48), 1) for x in (-0.50, 0.50)],
    )
    make("engine_drum_bands", bands, [dark, accent], c_eng, groups=["hull"])
    caps = bmesh.new()
    for s in (1, -1):
        e = s * (DRUM_HALF + 0.06)
        bm_append(caps, drum_x(e, DRUM_R + 0.06, 0.13, 48), 0)
        for r, w, mi in ((0.40, 0.025, 1), (0.31, 0.035, 0), (0.22, 0.025, 1), (0.10, 0.06, 0)):
            bm_append(caps, drum_x(e + s * (0.065 + w / 2), r, w, 48), mi)
        bm_append(caps, drum_x(e + s * 0.13, 0.035, 0.03, 16), 1)
    make("engine_drum_caps", caps, [gray, dark], c_eng, groups=["hull"])
    cradle = bm_merge(
        (bm_box_mm((-1.02, -3.40, 1.92), (1.02, -2.88, 2.10)), 0),
        *[(bm_box((0.10, 0.55, 0.42), T(s * 1.14, DRUM.y, 2.06)), 0) for s in (1, -1)],
        *[(bm_box((0.07, 0.07, 0.40), T(s * 1.14, DRUM.y + dy, 2.10)), 1)
          for s in (1, -1) for dy in (-0.18, 0.18)],
    )
    make("engine_cradle", cradle, [gray, dark], c_eng, groups=["hull"], bevel=0.015)
    for s, side in ((1, "r"), (-1, "l")):
        x = s * EXHAUST_X
        make(f"exhaust_{side}", bm_merge(
            cyl_y(0.17, 0.14, 0.14, 24, x, EXHAUST_Y + 0.08, EXHAUST_Z),
            cyl_y(0.185, 0.185, 0.03, 24, x, EXHAUST_Y + 0.12, EXHAUST_Z),
            *[bm_box((0.24, 0.015, 0.015), T(x, EXHAUST_Y - 0.01, EXHAUST_Z) @ Ry(a)) for a in (0, 60, 120)]),
            dark, c_eng, groups=["hull"])
        make(f"exhaust_glow_{side}", cyl_y(0.12, 0.12, 0.02, 24, x, EXHAUST_Y, EXHAUST_Z),
             thrust, c_eng, groups=["exhaust_glow"])

    # ---- repulsor strips
    for i, (x, y, z, sx, sy) in enumerate(REPULSORS, 1):
        make(f"repulsor_{i}", bm_box((sx, sy, 0.08), T(x, y, z)), dark, c_rep, groups=["hull"])
        make(f"repulsor_glow_{i}", bm_box((sx - 0.08, sy - 0.12, 0.015), T(x, y, z - 0.045)),
             glow, c_rep, groups=["repulsor_glow"])
        n_bars = int(sy / 0.14)
        make(f"repulsor_grille_{i}", bm_merge(
            *[bm_box((sx - 0.04, 0.018, 0.02), T(x, y - sy / 2 + sy * (k + 0.5) / n_bars, z - 0.06))
              for k in range(n_bars)],
            *[bm_box((0.018, sy - 0.06, 0.02), T(x + dx, y, z - 0.062))
              for dx in ((-sx / 4, sx / 4) if sx > 0.5 else (0,))]),
             dark, c_rep, groups=["hull"])
    belly = bmesh.new()
    for x, y in ((-0.55, -0.15), (0.55, -0.15), (-0.55, 2.35), (0.55, 2.35), (0.0, -2.75)):
        bm_append(belly, louvre((0.46, 0.04, 0.34), T(x, y, 0.49) @ Rx(-90), 6), 0)
        bm_append(belly, bm_box((0.50, 0.38, 0.015), T(x, y, 0.495)), 2)
    make("belly_vents", belly, [dark, gray, gray], c_rep, groups=["hull"])

    # ---- turret
    turret = make("turret", bm_hull(tp(TURRET)), [paint, paint_alt], c_tur, origin=T0, groups=["turret"],
                  bevel=0.035, panels=dict(cuts_x=(-0.42, 0.42), cuts_y=tuple(T0.y + v for v in (-0.70, -0.20, 0.30, 0.80)),
                                           cuts_z=(T0.z + 0.26,), alt=1, seed=13, rivet_step=0.20))

    def tur(name, bm, mats, groups=("turret",), origin=T0, collection=c_tur, bevel=0.0):
        return make(name, bm, mats, collection, origin=origin, groups=list(groups), parent=turret,
                    bevel=bevel)

    def tbox(size, rel):
        return bm_box(size, T(*(T0 + Vector(rel))))

    tur("vls_block", bm_box_mm(T0 + Vector((-0.58, -1.05, 0.42)), T0 + Vector((0.58, -0.15, VLS_TOP))),
        gray, bevel=0.02)
    for i, (cx, cy) in enumerate(VLS_CELLS, 1):
        c = T0 + Vector((cx, cy, 0))
        tur(f"vls_cell_{i}", bm_box((0.19, 0.19, 0.01), T(c.x, c.y, c.z + VLS_TOP + 0.002)), dark)
        hinge = (math.copysign(0.365, cx) + T0.x, c.y, T0.z + VLS_TOP)
        tur(f"vls_hatch_{i}", bm_box((0.19, 0.19, 0.025), T(c.x, c.y, c.z + VLS_TOP + 0.0125)),
            accent, groups=["turret", f"vls_hatch_{i}"], origin=hinge)
        rocket = bm_merge(
            (bm_cyl(0.065, 0.065, 0.70, 12, T(c.x, c.y, c.z + VLS_TOP - 0.52)), 0),
            (bm_cyl(0.065, 0.005, 0.15, 12, T(c.x, c.y, c.z + VLS_TOP - 0.095)), 1),
        )
        tur(f"rocket_{i}", rocket, [paint, accent], groups=["turret", f"rocket_{i}"], collection=c_vls)

    tur("turret_stripes", bm_merge(tbox((0.10, 0.60, 0.012), (0.66, 0.20, 0.505)),
                                   tbox((0.10, 0.60, 0.012), (-0.66, 0.20, 0.505))), accent)
    tur("gunner_sight", tbox((0.22, 0.28, 0.16), (-0.30, 0.30, 0.58)), dark)
    tur("gunner_sight_glass", tbox((0.16, 0.015, 0.08), (-0.30, 0.445, 0.58)), glass,
        groups=["turret", "glass"])
    sp = T0 + Vector((-1.06, 0.20, 0.28))
    tur("sensor_pod", bm_merge(
        (cyl_y(0.13, 0.13, 0.60, 32, sp.x, sp.y, sp.z), 0),
        (cyl_y(0.15, 0.15, 0.04, 32, sp.x, sp.y + 0.20, sp.z), 1),
        (cyl_y(0.145, 0.145, 0.03, 32, sp.x, sp.y - 0.12, sp.z), 2),
        (cyl_y(0.13, 0.11, 0.06, 32, sp.x, sp.y - 0.33, sp.z), 0),
        (cyl_y(0.11, 0.11, 0.03, 32, sp.x, sp.y + 0.285, sp.z), 2),
        (tbox((0.12, 0.20, 0.10), (-0.97, 0.20, 0.28)), 1)), [gray, accent, dark])
    tur("sensor_pod_lens", cyl_y(0.09, 0.09, 0.02, 32, sp.x, sp.y + 0.305, sp.z), glass,
        groups=["turret", "glass"])

    # finned sensor array on the turret roof (designator pods, not weapons)
    arr = bm_merge((tbox((0.26, 0.30, 0.08), (-0.56, 0.12, 0.54)), 0),
                   (tbox((0.06, 0.10, 0.12), (-0.56, 0.12, 0.62)), 1))
    for x in (-0.64, -0.48):
        p = T0 + Vector((x, 0.12, 0.70))
        bm_append(arr, cyl_y(0.055, 0.055, 0.40, 16, p.x, p.y, p.z), 0)
        bm_append(arr, cyl_y(0.055, 0.008, 0.12, 16, p.x, p.y + 0.26, p.z), 2)
        bm_append(arr, cyl_y(0.06, 0.06, 0.02, 16, p.x, p.y + 0.08, p.z), 1)
        for a in (0, 120, 240):
            bm_append(arr, bm_box((0.008, 0.12, 0.06), T(p.x, p.y - 0.15, p.z) @ Ry(a) @ T(0, 0, 0.075)), 1)
    tur("sensor_array", arr, [gray, dark, accent])

    # coil-spring recoil dampers on the turret cheeks
    for s, side in ((1, "r"), (-1, "l")):
        p = T0 + Vector((s * 0.99, 0.55, 0.14))
        tur(f"damper_spring_{side}", bm_spring(T(*p) @ Rx(-90), 0.075, 0.016, 0.42, 6), dark)
        tur(f"damper_body_{side}", bm_merge(
            cyl_y(0.025, 0.025, 0.56, 12, p.x, p.y, p.z),
            cyl_y(0.095, 0.095, 0.04, 24, p.x, p.y - 0.25, p.z),
            cyl_y(0.095, 0.095, 0.04, 24, p.x, p.y + 0.25, p.z)), gray)

    # grab handles across the turret bustle
    handles = bmesh.new()
    for x in (-0.55, 0.0, 0.55):
        p = T0 + Vector((x, -1.37, 0.33))
        bm_append(handles, bm_tube([p + Vector((-0.10, 0.02, 0)), p + Vector((-0.10, -0.05, 0)),
                                    p + Vector((0.10, -0.05, 0)), p + Vector((0.10, 0.02, 0))], 0.012, 8))
    tur("bustle_handles", handles, dark)
    tur("stowage_box", bm_merge(
        (tbox((0.16, 0.80, 0.26), (1.03, -0.30, 0.25)), 0),
        *[(tbox((0.02, 0.72, 0.022), (1.115, -0.30, z)), 1) for z in (0.15, 0.18, 0.21, 0.24, 0.27, 0.30, 0.33, 0.36)],
        *[(tbox((0.03, 0.04, 0.24), (1.115, y, 0.25)), 0) for y in (-0.70, 0.10)]),
        [gray, dark])

    # ---- 50 mm cannon: stepped blaster-style barrel
    gun = make("gun_mantlet", bm_hull(tp(MANTLET)), paint, c_tur, origin=G0,
               groups=["gun"], parent=turret, bevel=0.02, panels=dict(rivet_step=0.10, lift=0.005))
    gy, gz = T0.y, G0.z
    barrel = bm_merge(
        (cyl_y(0.17, 0.17, 0.88, 4, 0, gy + 1.86, gz, spin=45), 1),     # square shroud
        *[(bm_box((0.245, 0.02, 0.245), T(0, gy + y, gz)), 0) for y in (1.55, 1.80, 2.05)],
        *[(cyl_y(0.035, 0.035, 1.18, 16, x, gy + 2.01, gz - 0.10), 0) for x in (-0.10, 0.10)],
        *[(cyl_y(0.045, 0.045, 0.04, 16, x, gy + 2.55, gz - 0.10), 0) for x in (-0.10, 0.10)],
        (cyl_y(0.085, 0.085, 0.70, 24, 0, gy + 2.65, gz), 0),
        *[(cyl_y(0.105, 0.105, 0.035, 24, 0, gy + y, gz), 0) for y in (2.40, 2.55, 2.70, 2.85)],
        (cyl_y(0.085, 0.065, 0.06, 24, 0, gy + 3.03, gz), 0),
        (cyl_y(0.065, 0.065, 0.75, 24, 0, gy + 3.375, gz), 0),
        (cyl_y(0.075, 0.075, 0.03, 24, 0, gy + 3.30, gz), 0),
        (bm_box((0.19, 0.35, 0.15), T(0, gy + 3.925, gz)), 1),                 # muzzle brake
        *[(bm_box((0.012, 0.06, 0.11), T(sx * 0.096, gy + y, gz)), 0)
          for sx in (1, -1) for y in (3.82, 3.92, 4.02)],
        (cyl_y(0.11, 0.11, 0.03, 24, 0, gy + 4.085, gz), 1),
        (cyl_y(0.045, 0.045, 0.012, 16, 0, gy + 4.102, gz), 0),
    )
    make("gun_barrel_50mm", barrel, [dark, gray], c_tur, origin=G0, groups=["gun"], parent=gun,
         bevel=0.004)

    # ---- interior: 2 crew + 13 passengers
    make("interior_floor", bm_box_mm((-1.20, -3.15, FLOOR - 0.03), (1.20, 2.60, FLOOR)),
         dark, c_int, groups=["interior"])
    seats = [("driver", -0.45, FRONT_Y, 0, PAN, FLOOR),
             ("gunner", 0.0, T0.y - 0.05, 0, 1.55, 1.10)]
    n = 0
    for s, yaw in ((1, 90), (-1, -90)):
        for y in CARGO_Y:
            n += 1
            seats.append((f"cargo_{n:02d}", s * CARGO_X, y, yaw, PAN, FLOOR))
    seats.append(("cargo_13", 0.45, FRONT_Y, 0, PAN, FLOOR))

    for name, x, y, yaw, pan, floor in seats:
        m = T(x, y, 0) @ Rz(yaw)
        bm = bm_merge(
            (bm_box((0.44, 0.42, 0.06), m @ T(0, 0, pan - 0.03)), 0),
            (bm_box((0.44, 0.06, 0.55), m @ T(0, -0.24, pan + 0.26)), 0),
            (bm_box((0.22, 0.22, pan - 0.06 - floor), m @ T(0, 0, (pan - 0.06 + floor) / 2)), 1),
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

    # ---- Memory LOD: loose vertices, one vertex group per memory point
    sight = T0 + Vector((-0.30, 0.46, 0.58))
    mem = {
        "osaveze": [tuple(T0), tuple(T0 + Vector((0, 0, 0.7)))],
        "osahlavne": [(-0.2, G0.y, G0.z), (0.2, G0.y, G0.z)],
        "konec hlavne": [(0, G0.y + 0.3, gz)],
        "usti hlavne": [(0, MUZZLE_Y, gz)],
        "gunnerview": [tuple(sight)],
        "driverview": [(-0.45, 2.50, 1.78)],
        "ramp_axis": [(-0.8, -3.20, 0.55), (0.8, -3.20, 0.55)],
        "hatch_driver_axis": [(CUPOLA[0] - 0.15, CUPOLA[1] - 0.22, 2.09), (CUPOLA[0] + 0.15, CUPOLA[1] - 0.22, 2.09)],
        "pos driver": [(-0.6, -4.4, 0.3)],
        "pos gunner": [(0.6, -4.4, 0.3)],
        "pos cargo": [(0.0, -4.4, 0.3)],
        "light_l": [(-LENS_X[0], 4.02, LENS_Z)], "light_l_end": [(-LENS_X[0], 5.02, LENS_Z - 0.06)],
        "light_r": [(LENS_X[0], 4.02, LENS_Z)], "light_r_end": [(LENS_X[0], 5.02, LENS_Z - 0.06)],
        "exhaust_l": [(-EXHAUST_X, EXHAUST_Y, EXHAUST_Z)], "exhaust_l_dir": [(-EXHAUST_X, -4.3, EXHAUST_Z)],
        "exhaust_r": [(EXHAUST_X, EXHAUST_Y, EXHAUST_Z)], "exhaust_r_dir": [(EXHAUST_X, -4.3, EXHAUST_Z)],
    }
    for i, (cx, cy) in enumerate(VLS_CELLS, 1):
        c = T0 + Vector((cx, cy, VLS_TOP))
        mem[f"missile_{i}"] = [tuple(c)]
        mem[f"missile_{i}_dir"] = [tuple(c + Vector((0, 0, 1.0)))]
    for i, (x, y, z, sx, sy) in enumerate(REPULSORS, 1):
        mem[f"repulsor_{i}"] = [(x, y, z - 0.06)]

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

    # ---- Geometry LOD: closed convex components, one mesh
    drum = [(x, DRUM.y + DRUM_R * math.cos(a), DRUM.z + DRUM_R * math.sin(a))
            for x in (-DRUM_HALF - 0.11, DRUM_HALF + 0.11)
            for a in (2 * math.pi * i / 8 for i in range(8))]
    geo_parts = [
        (HULL + CAB + [(s * x, y, z) for s in (1, -1) for x, y, z in ARM], ["hull"]),
        (list(SKIRT), ["hull"]),
        ([(-x, y, z) for x, y, z in SKIRT], ["hull"]),
        (drum, ["hull"]),
        (tp(TURRET) + tp(sym((0.58, -1.05, VLS_TOP), (0.58, -0.15, VLS_TOP))), ["turret"]),
        (tp(MANTLET) + sym((0.17, gy + 1.42, gz + 0.17), (0.17, gy + 1.42, gz - 0.17),
                           (0.11, MUZZLE_Y, gz + 0.11), (0.11, MUZZLE_Y, gz - 0.11)), ["gun"]),
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
    total = 0
    for o in bpy.data.collections["LOD_Resolution_0"].all_objects:
        if o.type == 'MESH':
            me = o.evaluated_get(deps).data
            total += sum(len(p.vertices) - 2 for p in me.polygons)
    print(f"LOD_Resolution_0 triangles: {total}")
    lo = Vector((1e9,) * 3)
    hi = -lo
    for o in bpy.data.collections["LOD_Resolution_0"].all_objects:
        if o.type == 'MESH':
            for c in o.bound_box:
                w = o.matrix_world @ Vector(c)
                lo = Vector(map(min, lo, w))
                hi = Vector(map(max, hi, w))
    d = hi - lo
    print(f"Overall size: width {d.x:.2f} m, length {d.y:.2f} m, height {hi.z:.2f} m")


if __name__ == "__main__":
    argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
    build(argv[argv.index("--livery") + 1] if "--livery" in argv else LIVERY)
    bpy.context.view_layer.update()
    report()
    if "--out" in argv:
        path = argv[argv.index("--out") + 1]
        bpy.ops.wm.save_as_mainfile(filepath=bpy.path.abspath(path))
        print("Saved", path)
