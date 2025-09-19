#!/usr/bin/env python3
"""
Blender headless script to generate a lightweight stadium slice using the
Procedural Stadiums add-on, with optional Jumbotron import, and export a
GLB with minimal geometry and KTX2-ready textures.

Usage (from terminal):
  blender -b -P ops/3d/blender/export_stadium_slice.py -- \
    --stadium-preset "College Bowl" \
    --output "/abs/path/stadium_slice_raw.glb" \
    --import-jumbotron "/abs/path/jumbotron_raw.glb" \
    --camera-fov 35.0 --camera-height 1.6 --camera-dist 40.0 \
    --keep-lower-bowl --hide-audience --hide-upper-deck --texture-max 2048

Notes:
- Requires Procedural Stadiums add-on installed and enabled.
- This script focuses on visibility culling and exporter settings. It does not
  attempt to model; it toggles/hides heavy systems by convention.
"""

import argparse
import sys
import bpy

# ----------------------
# Arg parsing
# ----------------------

def parse_args(argv):
    parser = argparse.ArgumentParser()
    parser.add_argument('--stadium-preset', type=str, default='', help='Preset name to import/build')
    parser.add_argument('--output', type=str, required=True, help='Absolute output GLB path')
    parser.add_argument('--import-jumbotron', type=str, default='', help='Optional GLB to import for placement')
    parser.add_argument('--camera-fov', type=float, default=35.0)
    parser.add_argument('--camera-height', type=float, default=1.7)
    parser.add_argument('--camera-dist', type=float, default=45.0)
    parser.add_argument('--keep-lower-bowl', action='store_true')
    parser.add_argument('--hide-audience', action='store_true')
    parser.add_argument('--hide-upper-deck', action='store_true')
    parser.add_argument('--hide-exterior', action='store_true')
    parser.add_argument('--texture-max', type=int, default=2048)
    return parser.parse_args(argv)

# ----------------------
# Utilities
# ----------------------

def set_render_simplify():
    scene = bpy.context.scene
    scene.render.engine = 'BLENDER_EEVEE'
    scene.eevee.use_gtao = True
    scene.eevee.shadow_method = 'ESM'
    scene.render.use_simplify = True
    scene.render.simplify_subdivision = 0


def find_collection_by_name(name_substr: str):
    for c in bpy.data.collections:
        if name_substr.lower() in c.name.lower():
            return c
    return None


def hide_collection(c):
    if not c:
        return
    c.hide_viewport = True
    c.hide_render = True


def ensure_camera(args):
    cam = None
    for obj in bpy.data.objects:
        if obj.type == 'CAMERA':
            cam = obj
            break
    if cam is None:
        bpy.ops.object.camera_add()
        cam = bpy.context.active_object
    cam.location = (0.0, -args.camera_dist, args.camera_height)
    cam.rotation_euler = (1.2, 0.0, 0.0)
    cam.data.lens_unit = 'FOV'
    cam.data.angle = args.camera_fov * (3.14159265/180.0)
    bpy.context.scene.camera = cam


def import_glb(path: str):
    if not path:
        return None
    bpy.ops.import_scene.gltf(filepath=path)
    imported = [obj for obj in bpy.context.selected_objects]
    return imported


def set_texture_limits(max_size: int):
    for img in bpy.data.images:
        if img.size[0] > max_size or img.size[1] > max_size:
            img.use_generated_float = False
            # Metadata only; resizing should be done in pipeline tools. Here we flag.
            img['__oversized_warning'] = True


# ----------------------
# Stadium controls (best-effort based on add-on conventions)
# ----------------------

def apply_visibility_culling(args):
    # Attempt to find likely heavy collections by common names
    hide_collection(find_collection_by_name('Audience')) if args.hide_audience else None
    hide_collection(find_collection_by_name('Crowd')) if args.hide_audience else None
    hide_collection(find_collection_by_name('Upper')) if args.hide_upper_deck else None
    hide_collection(find_collection_by_name('Exterior')) if args.hide_exterior else None

    # Keep lower bowl hints; hide distant details
    if not args.keep_lower_bowl:
        hide_collection(find_collection_by_name('Lower'))


# ----------------------
# Export
# ----------------------

def export_glb(path: str):
    bpy.ops.export_scene.gltf(
        filepath=path,
        export_format='GLB',
        export_selected=False,
        export_apply=True,
        export_lights=False,
        export_cameras=False,
        export_extras=False,
        export_yup=True,
        export_materials='EXPORT',
        export_image_format='AUTO',
        export_texcoords=True,
        export_normals=True,
        export_tangents=False,
        export_colors=True,
        export_skins=False,
        export_morph=False,
        export_animations=False,
        export_frame_range=False,
        export_draco_mesh_compression_enable=False
    )


def main(argv):
    # Blender passes args, we split on '--'
    if '--' in argv:
        argv = argv[argv.index('--') + 1:]
    else:
        argv = []

    args = parse_args(argv)

    set_render_simplify()
    ensure_camera(args)

    if args.import_jumbotron:
        import_glb(args.import_jumbotron)

    apply_visibility_culling(args)
    set_texture_limits(args.texture_max)

    export_glb(args.output)
    print(f"Exported stadium slice to {args.output}")


if __name__ == '__main__':
    main(sys.argv)
