import bpy
from mathutils import Vector
from bpy_extras.object_utils import world_to_camera_view

def object_bbox_in_image(scene, cam_obj, obj, top_left_origin=True):
    depsgraph = bpy.context.evaluated_depsgraph_get()
    eval_obj = obj.evaluated_get(depsgraph)  
    # Punktequelle wählen: Mesh (präzise) oder bound_box (schnell)
    verts_world = []
    if eval_obj.type == 'MESH':
        me = eval_obj.to_mesh()
        mw = eval_obj.matrix_world
        verts_world = [mw @ v.co for v in me.vertices]
        eval_obj.to_mesh_clear()
    else:
        mw = eval_obj.matrix_world
        verts_world = [mw @ Vector(c) for c in eval_obj.bound_box]

    if not verts_world:
        return None

    # Projektion in NDC [0..1]
    coords_ndc = [world_to_camera_view(scene, cam_obj, v) for v in verts_world]
    # nur Punkte vor der Kamera verwenden
    coords_ndc = [c for c in coords_ndc if c.z > 0]

    if not coords_ndc:
        return None  # komplett hinter der Kamera

    xs = [c.x for c in coords_ndc]
    ys = [c.y for c in coords_ndc]

    min_x, max_x = min(xs), max(xs)
    min_y, max_y = min(ys), max(ys)

    # in Pixel umrechnen
    render = scene.render
    res_x = render.resolution_x * render.resolution_percentage / 100.0
    res_y = render.resolution_y * render.resolution_percentage / 100.0

    # clamp auf Bildbereich
    min_px = max(0.0, min_x * res_x)
    max_px = min(res_x, max_x * res_x)
    min_py = max(0.0, min_y * res_y)
    max_py = min(res_y, max_y * res_y)

    if max_px <= min_px or max_py <= min_py:
        return None  # liegt komplett außerhalb

    # Koordinatensystem wählen
    if top_left_origin:
        # y invertieren (Blender: y=0 unten -> ML: y=0 oben)
        y_top = res_y - max_py
        x = int(round(min_px))
        y = int(round(y_top))
        w = int(round(max_px - min_px))
        h = int(round(max_py - min_py))
    else:
        # Blender-Style: Ursprung unten links
        x = int(round(min_px))
        y = int(round(min_py))
        w = int(round(max_px - min_px))
        h = int(round(max_py - min_py))

    return (x, y, w, h);