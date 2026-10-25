"""
Preview renders for MSE v2: studio ground, three-point light, Cycles.

    blender --background MSE_v2.blend --python MSE_v2_render_previews.py -- --outdir previews [--views front34,rear34] [--samples 48]

Views: front34, rear34, side, top, front, cab_closeup, turret_closeup,
underside, seating_cutaway. Files are written as MSE_v2_<view>.png.
"""

import math
import os
import sys

import bpy
from mathutils import Vector

argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []


def arg(name, default):
    return argv[argv.index(name) + 1] if name in argv else default


OUTDIR = bpy.path.abspath(arg("--outdir", "previews"))
SAMPLES = int(arg("--samples", "48"))
RES = [int(v) for v in arg("--res", "1600x900").split("x")]
PREFIX = arg("--prefix", "MSE_v2")

VIEWS = {
    # name: (camera location, look-at target, focal length mm)
    "front34": ((7.8, 9.6, 4.4), (0.0, 0.4, 1.2), 50),
    "rear34": ((-7.6, -9.4, 4.6), (0.0, -0.6, 1.3), 50),
    "side": ((13.0, 0.3, 1.9), (0.0, 0.3, 1.35), 50),
    "top": ((0.0, 0.3, 13.0), None, 50),          # straight down, nose to the right
    "front": ((0.0, 13.0, 1.9), (0.0, 0.0, 1.35), 50),
    "cab_closeup": ((2.6, 6.6, 2.9), (0.2, 2.4, 1.45), 45),
    "turret_closeup": ((-3.6, 2.6, 4.2), (0.0, -0.8, 2.25), 45),
    "underside": ((6.5, 6.5, -2.6), (0.0, 0.0, 0.6), 40),
    "seating_cutaway": ((2.8, 5.0, 10.0), (0.0, -0.6, 0.8), 45),
}


def look_at(obj, target):
    d = Vector(target) - obj.location
    obj.rotation_euler = d.to_track_quat('-Z', 'Y').to_euler()


def setup():
    scn = bpy.context.scene
    scn.render.engine = 'CYCLES'
    scn.cycles.device = 'CPU'
    scn.cycles.samples = SAMPLES
    scn.cycles.use_denoising = True
    scn.render.resolution_x, scn.render.resolution_y = RES
    scn.render.film_transparent = False
    scn.view_settings.view_transform = 'AgX'
    scn.view_settings.look = 'AgX - Medium High Contrast'

    world = bpy.data.worlds.new("preview_world")
    world.use_nodes = True
    bg = world.node_tree.nodes["Background"]
    bg.inputs["Color"].default_value = (0.42, 0.46, 0.52, 1)
    bg.inputs["Strength"].default_value = 0.55
    scn.world = world

    # ground: a big plane with a soft grey material
    bpy.ops.mesh.primitive_plane_add(size=80, location=(0, 0, 0))
    ground = bpy.context.active_object
    ground.name = "preview_ground"
    gm = bpy.data.materials.new("preview_ground")
    gm.use_nodes = True
    gm.node_tree.nodes["Principled BSDF"].inputs["Base Color"].default_value = (0.36, 0.35, 0.33, 1)
    gm.node_tree.nodes["Principled BSDF"].inputs["Roughness"].default_value = 0.9
    ground.data.materials.append(gm)

    def sun(name, rot, strength, angle):
        d = bpy.data.lights.new(name, 'SUN')
        d.energy = strength
        d.angle = math.radians(angle)
        o = bpy.data.objects.new(name, d)
        scn.collection.objects.link(o)
        o.rotation_euler = [math.radians(a) for a in rot]
        return o

    sun("key", (42, 8, 140), 3.6, 6)
    sun("fill", (65, 0, -60), 0.9, 25)
    sun("rim", (60, 0, 20), 1.4, 10)

    cam_data = bpy.data.cameras.new("preview_cam")
    cam = bpy.data.objects.new("preview_cam", cam_data)
    scn.collection.objects.link(cam)
    scn.camera = cam
    return cam, ground


def hide_collection(name, hide):
    lc = None

    def walk(l):
        nonlocal lc
        if l.name == name:
            lc = l
        for c in l.children:
            walk(c)
    walk(bpy.context.view_layer.layer_collection)
    if lc:
        lc.exclude = hide


def main():
    os.makedirs(OUTDIR, exist_ok=True)
    cam, ground = setup()
    hide_collection("LOD_Geometry", True)
    hide_collection("LOD_Memory", True)
    hide_collection("Crew_Positions", True)
    wanted = arg("--views", ",".join(VIEWS)).split(",")
    cut_objs = []
    for name in wanted:
        loc, target, lens = VIEWS[name]
        cam.location = loc
        cam.data.lens = lens
        cam.data.clip_end = 200
        if target is None:
            cam.rotation_euler = (0, 0, math.radians(90))
        else:
            look_at(cam, target)
        ground.hide_render = name == "underside"
        cutaway = name == "seating_cutaway"
        if cutaway and not cut_objs:
            # hide everything above the floor except seats, so the seating plan reads from above
            keep = ("seat_", "interior_floor", "repulsor", "wall_upper", "wall_lower", "wall_ram", "wall_top", "hull")
            for o in bpy.data.collections["LOD_Resolution_0"].all_objects:
                if o.type == 'MESH' and not o.name.startswith(keep):
                    cut_objs.append(o)
            hull = bpy.data.objects["hull"]
            cut_objs.append(hull)
            for o in bpy.data.objects:
                if o.name.startswith("hull_rivets"):
                    cut_objs.append(o)
        for o in cut_objs:
            o.hide_render = cutaway
        if cutaway:
            # a low hull tub stand-in so the seats sit in something
            if "cutaway_tub" not in bpy.data.objects:
                bpy.ops.mesh.primitive_cube_add(size=1, location=(0, -0.3, 0.47))
                tub = bpy.context.active_object
                tub.name = "cutaway_tub"
                tub.scale = (2.36, 5.9, 0.10)
                tub.data.materials.append(bpy.data.materials["machinery_gray"])
            bpy.data.objects["cutaway_tub"].hide_render = False
        elif "cutaway_tub" in bpy.data.objects:
            bpy.data.objects["cutaway_tub"].hide_render = True
        bpy.context.scene.render.filepath = os.path.join(OUTDIR, f"{PREFIX}_{name}.png")
        bpy.ops.render.render(write_still=True)
        print("Rendered", name)


main()
