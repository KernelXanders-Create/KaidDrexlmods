"""
Hover IFV blockout for Arma 3, v4 (Clone Wars Republic, armored cab).

Repulsorlift infantry fighting vehicle, Bradley-sized (about 7.0 m hull,
3.6 m wide, 2.7 m to the turret roof), 2 crew + 13 passengers, 50 mm
autocannon and an 8-cell vertical launch rocket system on the turret.

v3 restyled it as Clone Wars era Republic armor: a long flat shovel nose,
a long full-width crew cab, the turret moved aft to make room, chunky
bevelled armor, and Republic two-tone livery (white upper hull, gray
running gear) with legion-colored markings.

v4 turns the cab into an armored crew compartment: a steep armored front
under an overhanging brow, narrow hooded vision slots instead of a
windshield, and more frontal armor (layered glacis plates, a nose ram
with slit lights, and add-on armor caps on the repulsor pod tips).

Pick the legion markings with LIVERY below or on the command line:
41st (green, default), republic (red), 501st (blue), 212th (orange).

Builds the whole model from scratch with bpy/bmesh, no add-ons needed.

Run headless:
    blender --background --python build_hover_ifv_v4.py -- --out hover_ifv_v4.blend [--livery 501st]
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
         smooth=35, bevel=0.0):
    """Turn a world-space bmesh into an object whose origin sits at `origin`."""
    if bevel:
        bevel_edges(bm, bevel)
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

# Forward-swept repulsor pod (right side; mirrored for the left).
POD = (
    (1.25, -3.15, 0.40), (1.80, -3.15, 0.45), (1.82, -3.25, 0.85), (1.40, -3.30, 1.05),
    (1.25, 2.55, 0.38), (1.75, 2.55, 0.42), (1.82, 2.35, 1.00), (1.40, 2.35, 1.12),
    (1.45, 3.55, 0.62), (1.30, 3.50, 0.75),
)
POD_TOP_DEG = math.degrees(math.atan2(0.12, 0.42))

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


def cab_wall_x(z):
    return 0.85 + (2.02 - z) * (0.95 - 0.85) / (2.02 - 1.70)


# Frontal armor: nose ram and repulsor pod caps (right side; mirrored for the left).
RAM = sym((1.12, 3.62, 1.04), (1.12, 3.62, 0.60), (1.05, 3.92, 0.98),
          (1.00, 3.92, 0.68), (0.90, 3.80, 0.55))
POD_CAP = (
    (1.23, 2.30, 0.33), (1.80, 2.30, 0.37), (1.85, 2.25, 1.04), (1.38, 2.25, 1.17),
    (1.49, 3.62, 0.58), (1.27, 3.57, 0.79),
)

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

NACELLE_X, NACELLE_Z, NACELLE_R = 1.30, 1.50, 0.36
EXHAUST_Y = -3.83

FLOOR = 0.58
PAN = 1.02                                # passenger seat height
CARGO_Y = (-2.70, -2.10, -1.50, -0.90, -0.30, 0.30)
CARGO_X = 1.18
FRONT_Y = 1.75                            # driver and front passenger, inside the cab
# (x, y, z, size_x, size_y): 3 strips under each pod, 2 plates under the belly
REPULSORS = ([(s * 1.52, y, 0.375, 0.42, 1.30) for s in (1, -1) for y in (-2.20, -0.45, 1.30)]
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

    root = coll("HoverIFV_v4")
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

    # ---- hull, pods, cab (two-tone, chamfered)
    make("hull", two_tone(bm_hull(HULL), 0.97), [paint, gray], c_hull, groups=["hull"], bevel=0.04)
    for s, side in ((1, "r"), (-1, "l")):
        make(f"repulsor_pod_{side}", bm_hull([(s * x, y, z) for x, y, z in POD]),
             gray, c_hull, groups=["hull"], bevel=0.035)
    make("cab", bm_hull(CAB), paint, c_hull, groups=["hull"], bevel=0.035)

    # armored brow overhanging the front, legion stripe along its lip
    make("cab_brow_armor", bm_box((1.72, 0.40, 0.05), on_slope(BROW_MID, BROW_DEG, 0.025) @ T(0, 0.04, 0)),
         panel, c_hull, groups=["hull"], bevel=0.012)
    make("cab_brow_stripe", bm_box((1.72, 0.06, 0.012), on_slope(BROW_MID, BROW_DEG, 0.056) @ T(0, 0.17, 0)),
         accent, c_det, groups=["hull"])

    # vision slots: armored blocks with a narrow glass slit and a hood above
    slot_blocks, slot_glass, hoods = bmesh.new(), bmesh.new(), bmesh.new()
    for x in (-0.62, -0.21, 0.21, 0.62):
        m = on_slope(SLOT_LINE + Vector((x, 0, 0)), FRONT_DEG, 0.0)
        bm_append(slot_blocks, bm_box((0.32, 0.12, 0.04), m @ T(0, 0, 0.02)))
        bm_append(slot_glass, bm_box((0.24, 0.035, 0.01), m @ T(0, 0, 0.043)))
        bm_append(hoods, bm_box((0.36, 0.025, 0.09), m @ T(0, -0.07, 0.045)))
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
    plate = bm_box((1.75, 0.20, 0.06), on_slope(FRONT_PLATE, FRONT_DEG, 0.03))
    for x in (-0.75, -0.45, -0.15, 0.15, 0.45, 0.75):
        bm_append(plate, bm_box((0.04, 0.04, 0.02), on_slope(FRONT_PLATE + Vector((x, 0, 0)), FRONT_DEG, 0.07)), 1)
    make("cab_front_armor", plate, [panel, dark], c_hull, groups=["hull"])
    make("hatch_driver", bm_box((0.55, 0.55, 0.04), T(0, 1.55, 2.04)), panel, c_hull,
         origin=(0, 1.275, 2.02), groups=["hatch_driver"])

    # frontal armor: layered glacis plates, nose ram, pod tip caps
    gbase = (0.0, 3.38, glacis_z(3.38))
    glacis = bm_merge(
        (bm_box((2.00, 0.62, 0.08), on_slope(gbase, GLACIS_DEG, 0.04)), 0),
        (bm_box((1.50, 0.40, 0.06), on_slope(gbase, GLACIS_DEG, 0.11) @ T(0, -0.02, 0)), 0),
        (bm_box((1.50, 0.05, 0.01), on_slope(gbase, GLACIS_DEG, 0.145) @ T(0, 0.12, 0)), 1),
        *[(bm_box((0.04, 0.04, 0.02), on_slope(gbase, GLACIS_DEG, 0.09) @ T(x, 0.26, 0)), 2)
          for x in (-0.90, -0.60, 0.60, 0.90)],
    )
    make("glacis_armor", glacis, [panel, accent, dark], c_hull, groups=["hull"])
    make("nose_ram", bm_hull(RAM), gray, c_hull, groups=["hull"], bevel=0.03)
    for s, side in ((1, "r"), (-1, "l")):
        make(f"pod_armor_cap_{side}", bm_hull([(s * x, y, z) for x, y, z in POD_CAP]),
             panel, c_hull, groups=["hull"], bevel=0.03)

    # ---- side armor, pipes, pod stripes, lights, deck hatches
    for s, side in ((1, "r"), (-1, "l")):
        for i, (y0, y1) in enumerate(((-1.75, -0.80), (-0.70, 0.30), (0.40, 1.40)), 1):
            make(f"armor_plate_{side}{i}",
                 bm_box((0.03, y1 - y0, 0.40), T(s * (side_x(1.38) + 0.016), (y0 + y1) / 2, 1.38) @ Ry(-s * SIDE_DEG)),
                 panel, c_det, groups=["hull"])
        pipes = bm_merge(
            cyl_y(0.035, 0.035, 3.2, 8, s * (side_x(1.66) + 0.04), -0.20, 1.66),
            *[bm_box((0.07, 0.05, 0.12), T(s * (side_x(1.66) + 0.03), y, 1.66)) for y in (-1.6, -0.5, 0.6, 1.3)],
        )
        make(f"side_pipes_{side}", pipes, dark, c_det, groups=["hull"])
        top_z = 1.12 - 0.12 * (1.70 - 1.40) / 0.42
        make(f"pod_stripe_{side}", bm_box((0.10, 3.8, 0.02), T(s * 1.70, -0.10, top_z + 0.012) @ Ry(s * POD_TOP_DEG)),
             accent, c_det, groups=["hull"])

        make(f"light_hood_{side}", bm_box((0.34, 0.09, 0.025), T(s * 0.62, 3.955, 0.905)),
             dark, c_det, groups=["hull"])
        make(f"light_{side}", bm_box((0.26, 0.03, 0.045), T(s * 0.62, 3.925, 0.86)),
             lamp, c_det, groups=[f"light_{side}"])

        make(f"hatch_cargo_{side}", bm_box((0.60, 0.75, 0.05), T(s * 0.60, -2.65, 2.075)),
             panel, c_hull, origin=(s * 0.90, -2.65, 2.05), groups=[f"hatch_cargo_{side}"])

        make(f"deck_box_{side}", bm_merge(
            bm_box((0.14, 0.35, 0.08), T(s * 0.98, -2.95, 2.09)),
            bm_box((0.14, 0.25, 0.10), T(s * 0.98, -2.15, 2.10))),
            gray, c_det, groups=["hull"])

    # ---- rear deck: spine, sensor dish, whip antenna (all outside the turret's sweep)
    spine = bm_merge(
        (bm_box((0.22, 1.00, 0.07), T(0, -2.60, 2.085)), 0),
        (cyl_y(0.025, 0.025, 1.00, 8, 0.06, -2.60, 2.14), 1),
        (cyl_y(0.025, 0.025, 1.00, 8, -0.06, -2.60, 2.14), 1),
    )
    make("deck_spine", spine, [gray, dark], c_det, groups=["hull"])
    dish = bm_merge(
        bm_cyl(0.03, 0.03, 0.30, 8, T(-0.98, -2.55, 2.20)),
        bm_cyl(0.15, 0.03, 0.05, 12, T(-0.98, -2.60, 2.39) @ Rx(60)),
    )
    make("sensor_dish", dish, dark, c_det, groups=["hull"])
    whip = bm_merge(
        bm_cyl(0.045, 0.04, 0.06, 8, T(0.98, -2.55, 2.08)),
        bm_cyl(0.010, 0.005, 1.30, 6, T(0.98, -2.55, 2.76)),
    )
    make("antenna", whip, dark, c_det, groups=["hull"])

    # ---- rear ramp
    ramp_pts = sym((0.80, -3.35, 0.55), (0.80, -3.35, 1.75), (0.80, -3.28, 1.75),
                   (0.80, -3.28, 0.95), (0.80, -3.03, 0.55))
    ramp = make("ramp", bm_hull(ramp_pts), paint, c_hull,
                origin=(0, -3.20, 0.55), groups=["ramp"])
    ribs = bm_merge(*[bm_box((1.4, 0.03, 0.05), T(0, -3.365, z)) for z in (1.00, 1.30, 1.60)])
    make("ramp_ribs", ribs, accent, c_hull, origin=(0, -3.20, 0.55), groups=["ramp"], parent=ramp)

    make("turret_ring", bm_cyl(0.90, 0.90, 0.08, 24, T(*T0)), dark, c_hull, groups=["hull"])

    # ---- engine nacelles
    for s, side in ((1, "r"), (-1, "l")):
        x, z = s * NACELLE_X, NACELLE_Z
        make(f"nacelle_{side}", bm_merge(
            cyl_y(NACELLE_R, NACELLE_R, 1.50, 16, x, -2.85, z),
            cyl_y(NACELLE_R, 0.22, 0.30, 16, x, -1.95, z)),
            gray, c_eng, groups=["hull"])
        bands = bm_merge(
            *[(cyl_y(0.385, 0.385, 0.05, 16, x, y, z), 1 if y == -2.90 else 0) for y in (-2.35, -2.90, -3.45)],
            cyl_y(0.34, 0.30, 0.20, 16, x, -3.70, z),
            *[bm_box((0.56, 0.03, 0.03), T(x, EXHAUST_Y, z) @ Ry(a)) for a in (0, 45, 90, 135)],
        )
        make(f"nacelle_bands_{side}", bands, [dark, accent], c_eng, groups=["hull"])
        make(f"exhaust_glow_{side}", cyl_y(0.27, 0.27, 0.02, 16, x, -3.805, z),
             thrust, c_eng, groups=["exhaust_glow"])

    # ---- repulsor strips
    for i, (x, y, z, sx, sy) in enumerate(REPULSORS, 1):
        make(f"repulsor_{i}", bm_box((sx, sy, 0.08), T(x, y, z)), dark, c_rep, groups=["hull"])
        make(f"repulsor_glow_{i}", bm_box((sx - 0.08, sy - 0.12, 0.015), T(x, y, z - 0.045)),
             glow, c_rep, groups=["repulsor_glow"])

    # ---- turret
    turret = make("turret", bm_hull(tp(TURRET)), paint, c_tur, origin=T0, groups=["turret"], bevel=0.035)

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
        (cyl_y(0.13, 0.13, 0.60, 16, sp.x, sp.y, sp.z), 0),
        (cyl_y(0.15, 0.15, 0.04, 16, sp.x, sp.y + 0.20, sp.z), 1),
        (tbox((0.12, 0.20, 0.10), (-0.97, 0.20, 0.28)), 1)), [gray, accent])
    tur("sensor_pod_lens", cyl_y(0.09, 0.09, 0.02, 16, sp.x, sp.y + 0.305, sp.z), glass,
        groups=["turret", "glass"])
    tur("stowage_box", tbox((0.16, 0.80, 0.26), (1.03, -0.30, 0.25)), gray)

    # ---- 50 mm cannon: stepped blaster-style barrel
    gun = make("gun_mantlet", bm_hull(tp(MANTLET)), paint, c_tur, origin=G0,
               groups=["gun"], parent=turret, bevel=0.02)
    gy, gz = T0.y, G0.z
    barrel = bm_merge(
        cyl_y(0.17, 0.17, 0.88, 4, 0, gy + 1.86, gz, spin=45),          # square shroud
        *[cyl_y(0.035, 0.035, 1.18, 8, x, gy + 2.01, gz - 0.10) for x in (-0.10, 0.10)],
        cyl_y(0.085, 0.085, 0.70, 12, 0, gy + 2.65, gz),
        *[cyl_y(0.105, 0.105, 0.035, 12, 0, gy + y, gz) for y in (2.40, 2.55, 2.70, 2.85)],
        cyl_y(0.065, 0.065, 0.75, 12, 0, gy + 3.375, gz),
        cyl_y(0.10, 0.10, 0.35, 8, 0, gy + 3.925, gz, spin=22.5),
        cyl_y(0.11, 0.11, 0.03, 8, 0, gy + 4.085, gz, spin=22.5),
    )
    make("gun_barrel_50mm", barrel, dark, c_tur, origin=G0, groups=["gun"], parent=gun)

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
        "hatch_driver_axis": [(-0.27, 1.275, 2.02), (0.27, 1.275, 2.02)],
        "pos driver": [(-0.6, -4.4, 0.3)],
        "pos gunner": [(0.6, -4.4, 0.3)],
        "pos cargo": [(0.0, -4.4, 0.3)],
        "light_l": [(-0.62, 3.95, 0.86)], "light_l_end": [(-0.62, 4.95, 0.80)],
        "light_r": [(0.62, 3.95, 0.86)], "light_r_end": [(0.62, 4.95, 0.80)],
        "exhaust_l": [(-NACELLE_X, EXHAUST_Y, NACELLE_Z)], "exhaust_l_dir": [(-NACELLE_X, -4.5, NACELLE_Z)],
        "exhaust_r": [(NACELLE_X, EXHAUST_Y, NACELLE_Z)], "exhaust_r_dir": [(NACELLE_X, -4.5, NACELLE_Z)],
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
    nacelle = [ring_pts(NACELLE_X, y, NACELLE_Z, NACELLE_R) for y in (-1.80, EXHAUST_Y)]
    nacelle = nacelle[0] + nacelle[1]
    geo_parts = [
        (HULL + CAB + RAM, ["hull"]),
        (list(POD) + list(POD_CAP), ["hull"]),
        ([(-x, y, z) for x, y, z in POD + POD_CAP], ["hull"]),
        (nacelle, ["hull"]),
        ([(-x, y, z) for x, y, z in nacelle], ["hull"]),
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
