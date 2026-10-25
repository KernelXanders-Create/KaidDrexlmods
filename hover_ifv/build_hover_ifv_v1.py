"""
Hover IFV blockout for Arma 3, v1.

Sci-fi repulsorlift infantry fighting vehicle, Bradley-sized
(about 6.9 m hull, 3.6 m wide, 2.9 m tall), 2 crew + 13 passengers,
50 mm autocannon and an 8-cell vertical launch rocket system on the turret.

Builds the whole model from scratch with bpy/bmesh, no add-ons needed.

Run headless:
    blender --background --python build_hover_ifv_v1.py -- --out hover_ifv_v1.blend
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
         smooth=35):
    """Turn a world-space bmesh into an object whose origin sits at `origin`."""
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


# -------------------------------------------------------------- dimensions

# Hull: belly 0.50 m off the ground, roof at 2.10 m, nose at +Y.
HULL = sym(
    (1.30, -3.10, 0.50), (1.30, 2.70, 0.50),    # belly
    (1.70, -3.35, 0.95), (1.70, 2.90, 0.95),    # lower chine
    (1.55, -3.35, 1.85), (1.55, 1.90, 1.85),    # upper shoulder
    (1.20, -3.25, 2.10), (1.20, 1.50, 2.10),    # roof
    (0.95, 3.45, 1.00), (0.85, 3.40, 0.70),     # nose
)
SPONSON = (
    (1.30, -2.75, 0.38), (1.30, 2.35, 0.38), (1.75, -2.75, 0.42), (1.75, 2.35, 0.42),
    (1.82, -3.05, 0.80), (1.82, 2.70, 0.80), (1.82, -2.95, 1.05), (1.82, 2.55, 1.05),
    (1.35, -3.00, 1.15), (1.35, 2.60, 1.15),
)
GLACIS_DEG = math.degrees(math.atan2(2.10 - 1.00, 3.45 - 1.50))


def glacis_z(y):
    return 2.10 - (y - 1.50) * (2.10 - 1.00) / (3.45 - 1.50)


T0 = Vector((0.0, 0.30, 2.10))           # turret rotation axis on the roof
TURRET = sym(
    (1.00, -1.10, 0.02), (1.00, 0.90, 0.02), (0.55, 1.35, 0.10),
    (0.80, -1.10, 0.62), (0.75, 0.70, 0.62), (0.45, 1.10, 0.48),
)
MANTLET = sym((0.28, 1.05, 0.15), (0.28, 1.05, 0.48),
              (0.22, 1.40, 0.20), (0.22, 1.40, 0.42))
G0 = T0 + Vector((0.0, 1.15, 0.31))      # gun elevation pivot
MUZZLE_Y = T0.y + 4.06

VLS_CELLS = [(sx * 0.27, cy) for cy in (-0.93, -0.71, -0.49, -0.27) for sx in (-1, 1)]
VLS_TOP = 0.80                            # turret-relative

FLOOR = 0.58
PAN = 1.02                                # passenger seat height
CARGO_Y = (-2.80, -2.25, -1.70, -1.15, -0.60, -0.05)
REPULSORS = ([(s * 1.52, y, 0.37, 0.26) for s in (1, -1) for y in (-2.05, 0.15, 1.95)]
             + [(0.0, -1.45, 0.47, 0.42), (0.0, 1.20, 0.47, 0.42)])


def tp(pts):
    """Turret-relative points to world."""
    return [tuple(Vector(p) + T0) for p in pts]


# ------------------------------------------------------------------- build

def build():
    clear_scene()
    scn = bpy.context.scene
    scn.unit_settings.system = 'METRIC'
    scn.unit_settings.scale_length = 1.0

    root = coll("HoverIFV_v1")
    vis = coll("LOD_Resolution_0", root)
    c_hull = coll("Hull", vis)
    c_rep = coll("Repulsors", vis)
    c_tur = coll("Turret", vis)
    c_vls = coll("VLS_Rockets", vis)
    c_int = coll("Interior_Seats", vis)
    c_geo = coll("LOD_Geometry", root)
    c_mem = coll("LOD_Memory", root)
    c_crew = coll("Crew_Positions", root)
    coll("LOD_FireGeometry_TODO", root)
    coll("LOD_ViewGeometry_TODO", root)

    paint = material("hull_paint", (0.58, 0.59, 0.57), rough=0.55)
    panel = material("armor_panel", (0.42, 0.43, 0.42), rough=0.6)
    dark = material("dark_metal", (0.07, 0.075, 0.08), rough=0.4, metal=0.7)
    accent = material("accent", (0.48, 0.14, 0.06), rough=0.5)
    glass = material("glass", (0.02, 0.03, 0.04), rough=0.08, metal=0.4)
    glow = material("repulsor_glow", (0.1, 0.3, 0.5), emit=(0.35, 0.75, 1.0), strength=6.0)
    thrust = material("thruster_glow", (0.1, 0.2, 0.5), emit=(0.45, 0.6, 1.0), strength=8.0)
    lamp = material("headlight", (0.9, 0.9, 0.8), emit=(1.0, 0.92, 0.75), strength=5.0)
    seat_m = material("seat", (0.16, 0.16, 0.14), rough=0.8)

    # ---- hull
    make("hull", bm_hull(HULL), paint, c_hull, groups=["hull"])
    for s, side in ((1, "r"), (-1, "l")):
        make(f"sponson_{side}", bm_hull([(s * x, y, z) for x, y, z in SPONSON]),
             paint, c_hull, groups=["hull"])
        for i, yc in enumerate((-2.2, -0.6, 1.0), 1):
            make(f"armor_plate_{side}{i}",
                 bm_box((0.03, 1.4, 0.55), T(s * 1.64, yc, 1.42) @ Ry(-s * 9.5)),
                 panel, c_hull, groups=["hull"])

    # driver / front-passenger viewports set into the glacis
    nrm = Vector((0, math.sin(R(GLACIS_DEG)), math.cos(R(GLACIS_DEG))))
    for s, side in ((1, "r"), (-1, "l")):
        base = Vector((s * 0.55, 1.95, glacis_z(1.95)))
        make(f"viewport_frame_{side}",
             bm_box((0.60, 0.40, 0.025), T(*(base + nrm * 0.012)) @ Rx(-GLACIS_DEG)),
             dark, c_hull, groups=["hull"])
        make(f"viewport_glass_{side}",
             bm_box((0.50, 0.30, 0.012), T(*(base + nrm * 0.026)) @ Rx(-GLACIS_DEG)),
             glass, c_hull, groups=["hull", "glass"])

        make(f"light_housing_{side}", bm_box((0.28, 0.05, 0.12), T(s * 0.62, 3.425, 0.86)),
             dark, c_hull, groups=["hull"])
        make(f"light_{side}", bm_box((0.22, 0.03, 0.07), T(s * 0.62, 3.445, 0.86)),
             lamp, c_hull, groups=[f"light_{side}"])

        make(f"hatch_cargo_{side}", bm_box((0.60, 0.75, 0.05), T(s * 0.60, -2.35, 2.125)),
             dark, c_hull, origin=(s * 0.90, -2.35, 2.10), groups=[f"hatch_cargo_{side}"])

        make(f"thruster_{side}", bm_cyl(0.18, 0.23, 0.32, 12, T(s * 1.18, -3.44, 1.45) @ Rx(90)),
             dark, c_hull, groups=["hull"])
        make(f"thruster_glow_{side}", bm_cyl(0.19, 0.19, 0.02, 12, T(s * 1.18, -3.605, 1.45) @ Rx(90)),
             thrust, c_hull, groups=["exhaust_glow"])

    vents = bm_box((1.5, 0.45, 0.03), T(0, -1.30, 2.115))
    for i in range(7):
        bm_append(vents, bm_box((1.4, 0.03, 0.03), T(0, -1.30 + (i - 3) * 0.055, 2.14)), 1)
    make("engine_vents", vents, [dark, paint], c_hull, groups=["hull"])

    ramp_pts = sym((0.80, -3.40, 0.55), (0.80, -3.40, 1.90), (0.80, -3.33, 1.90),
                   (0.80, -3.33, 0.95), (0.80, -3.08, 0.55))
    ramp = make("ramp", bm_hull(ramp_pts), paint, c_hull,
                origin=(0, -3.25, 0.55), groups=["ramp"])
    ribs = bm_merge(*[bm_box((1.4, 0.03, 0.05), T(0, -3.415, z)) for z in (1.05, 1.35, 1.65)])
    make("ramp_ribs", ribs, dark, c_hull, origin=(0, -3.25, 0.55), groups=["ramp"], parent=ramp)

    make("turret_ring", bm_cyl(0.90, 0.90, 0.08, 24, T(*T0)), dark, c_hull, groups=["hull"])

    # ---- repulsors
    for i, (x, y, z, r) in enumerate(REPULSORS, 1):
        make(f"repulsor_{i}", bm_cyl(r, r * 0.85, 0.08, 16, T(x, y, z)),
             dark, c_rep, groups=["hull"])
        make(f"repulsor_glow_{i}", bm_cyl(r * 0.8, r * 0.8, 0.02, 16, T(x, y, z - 0.045)),
             glow, c_rep, groups=["repulsor_glow"])

    # ---- turret
    turret = make("turret", bm_hull(tp(TURRET)), paint, c_tur, origin=T0, groups=["turret"])
    make("vls_block", bm_box_mm(T0 + Vector((-0.58, -1.05, 0.55)), T0 + Vector((0.58, -0.15, VLS_TOP))),
         paint, c_tur, origin=T0, groups=["turret"], parent=turret)
    for i, (cx, cy) in enumerate(VLS_CELLS, 1):
        c = T0 + Vector((cx, cy, 0))
        make(f"vls_cell_{i}", bm_box((0.19, 0.19, 0.01), T(c.x, c.y, c.z + VLS_TOP + 0.002)),
             dark, c_tur, origin=T0, groups=["turret"], parent=turret)
        hinge = (math.copysign(0.365, cx) + T0.x, c.y, T0.z + VLS_TOP)
        make(f"vls_hatch_{i}", bm_box((0.19, 0.19, 0.025), T(c.x, c.y, c.z + VLS_TOP + 0.0125)),
             accent, c_tur, origin=hinge, groups=["turret", f"vls_hatch_{i}"], parent=turret)
        rocket = bm_merge(
            (bm_cyl(0.065, 0.065, 0.70, 12, T(c.x, c.y, c.z + 0.28)), 0),
            (bm_cyl(0.065, 0.005, 0.15, 12, T(c.x, c.y, c.z + 0.705)), 1),
        )
        make(f"rocket_{i}", rocket, [paint, accent], c_vls, origin=T0,
             groups=["turret", f"rocket_{i}"], parent=turret)

    gun = make("gun_mantlet", bm_hull(tp(MANTLET)), paint, c_tur, origin=G0,
               groups=["gun"], parent=turret)
    gz = G0.z
    barrel = bm_merge(
        bm_cyl(0.12, 0.12, 1.0, 6, T(0, T0.y + 1.90, gz) @ Rx(-90) @ Rz(30)),
        bm_cyl(0.065, 0.065, 1.8, 12, T(0, T0.y + 2.90, gz) @ Rx(-90)),
        *[bm_cyl(0.085, 0.085, 0.04, 8, T(0, T0.y + y, gz) @ Rx(-90)) for y in (2.75, 3.05, 3.35)],
        bm_cyl(0.10, 0.10, 0.28, 8, T(0, T0.y + 3.92, gz) @ Rx(-90) @ Rz(22.5)),
    )
    make("gun_barrel_50mm", barrel, dark, c_tur, origin=G0, groups=["gun"], parent=gun)

    make("gunner_sight", bm_box((0.24, 0.30, 0.16), T(*(T0 + Vector((-0.48, 0.55, 0.70))))),
         dark, c_tur, origin=T0, groups=["turret"], parent=turret)
    make("gunner_sight_glass", bm_box((0.18, 0.015, 0.09), T(*(T0 + Vector((-0.48, 0.705, 0.70))))),
         glass, c_tur, origin=T0, groups=["turret", "glass"], parent=turret)
    antenna = bm_merge(
        bm_cyl(0.05, 0.04, 0.06, 8, T(*(T0 + Vector((0.66, -0.95, 0.65))))),
        bm_cyl(0.012, 0.006, 1.1, 6, T(*(T0 + Vector((0.66, -0.95, 1.20))))),
    )
    make("antenna", antenna, dark, c_tur, origin=T0, groups=["turret"], parent=turret)

    # ---- interior: 2 crew + 13 passengers
    make("interior_floor", bm_box_mm((-1.25, -3.20, FLOOR - 0.03), (1.25, 2.40, FLOOR)),
         dark, c_int, groups=["interior"])
    seats = [("driver", -0.55, 1.55, 0, PAN, FLOOR),
             ("gunner", 0.0, 0.25, 0, 1.65, 1.15)]
    n = 0
    for s, yaw in ((1, 90), (-1, -90)):
        for y in CARGO_Y:
            n += 1
            seats.append((f"cargo_{n:02d}", s * 1.22, y, yaw, PAN, FLOOR))
    seats.append(("cargo_13", 0.55, 1.55, 0, PAN, FLOOR))

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
    sight = T0 + Vector((-0.48, 0.70, 0.70))
    mem = {
        "osaveze": [tuple(T0), tuple(T0 + Vector((0, 0, 0.7)))],
        "osahlavne": [(-0.2, G0.y, G0.z), (0.2, G0.y, G0.z)],
        "konec hlavne": [(0, G0.y + 0.3, gz)],
        "usti hlavne": [(0, MUZZLE_Y, gz)],
        "gunnerview": [tuple(sight)],
        "driverview": [(-0.55, 1.75, 1.85)],
        "ramp_axis": [(-0.8, -3.25, 0.55), (0.8, -3.25, 0.55)],
        "pos driver": [(-0.6, -4.3, 0.3)],
        "pos gunner": [(0.6, -4.3, 0.3)],
        "pos cargo": [(0.0, -4.3, 0.3)],
        "light_l": [(-0.62, 3.47, 0.86)], "light_l_end": [(-0.62, 4.47, 0.80)],
        "light_r": [(0.62, 3.47, 0.86)], "light_r_end": [(0.62, 4.47, 0.80)],
        "exhaust_l": [(-1.18, -3.62, 1.45)], "exhaust_l_dir": [(-1.18, -4.2, 1.45)],
        "exhaust_r": [(1.18, -3.62, 1.45)], "exhaust_r_dir": [(1.18, -4.2, 1.45)],
    }
    for i, (cx, cy) in enumerate(VLS_CELLS, 1):
        c = T0 + Vector((cx, cy, VLS_TOP))
        mem[f"missile_{i}"] = [tuple(c)]
        mem[f"missile_{i}_dir"] = [tuple(c + Vector((0, 0, 1.0)))]
    for i, (x, y, z, r) in enumerate(REPULSORS, 1):
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
    geo_parts = [
        (HULL, ["hull"]),
        ([(x, y, z) for x, y, z in SPONSON], ["hull"]),
        ([(-x, y, z) for x, y, z in SPONSON], ["hull"]),
        (tp(TURRET) + tp(sym((0.58, -1.05, VLS_TOP), (0.58, -0.15, VLS_TOP))), ["turret"]),
        (tp(MANTLET) + sym((0.12, T0.y + 1.40, gz + 0.12), (0.12, T0.y + 1.40, gz - 0.12),
                           (0.12, MUZZLE_Y, gz + 0.12), (0.12, MUZZLE_Y, gz - 0.12)), ["gun"]),
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
    build()
    bpy.context.view_layer.update()
    report()
    argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
    if "--out" in argv:
        path = argv[argv.index("--out") + 1]
        bpy.ops.wm.save_as_mainfile(filepath=bpy.path.abspath(path))
        print("Saved", path)
