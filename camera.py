import math
import random

import bpy
from mathutils import Vector


def place_random_camera(radius=500, hoehe=180):
    bpy.ops.object.select_all(action="SELECT")

    objs = [o for o in bpy.context.selected_objects if o.type in {"MESH"}]
    if not objs:
        raise RuntimeError("Keine Objekte ausgewählt.")

    center = Vector((0, 0, 0))
    for o in objs:
        center += (
            o.matrix_world.translation
        )  # echte Weltposition, auch bei Parenting korrekt
    center /= len(objs)

    bpy.context.scene.cursor.location = center
    # print("Cursor gesetzt auf:", center)

    different_cameras = 1

    for c in range(0, different_cameras):
        winkel_grad = random.randint(0, 360)

        # Grad zu Radiant
        phi = math.radians(winkel_grad)

        # Berechne Position auf dem Kreis (XZ-Ebene, um Ursprung)
        x = radius * math.cos(phi)
        y = radius * math.sin(phi)
        z = hoehe

        # Kamera erstellen
        bpy.ops.object.camera_add(location=(x, y, z))
        cam = bpy.context.active_object

        # Kamera zum Objekt ausrichten ("track to" - schauen auf (0,0,0))
        ziel = center
        richtung = ziel - cam.location
        rot_quat = richtung.to_track_quat("-Z", "Y")
        cam.rotation_euler = rot_quat.to_euler()

        # Als Szenenkamera setzen
        s = bpy.context.scene
        if cam.name not in s.collection.objects:
            s.collection.objects.link(cam)
        cam.hide_render = False
        s.camera = cam


def delete_cameras():
    bpy.ops.object.select_by_type(type="CAMERA")
    bpy.ops.object.delete()
