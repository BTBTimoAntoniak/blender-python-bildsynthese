import json
import os
import sys

import bpy

if bpy.data.is_saved:
    proj_dir = os.path.dirname(bpy.data.filepath)  # Ordner der .blend
else:
    # Falls die .blend noch nicht gespeichert ist:
    # versuche den Dateipfad dieses Scripts (wenn als .py von Disk gestartet)
    try:
        proj_dir = os.path.dirname(__file__)
    except NameError:
        proj_dir = os.getcwd()

if proj_dir not in sys.path:
    sys.path.append(proj_dir)

import shutil
from datetime import datetime

import bounding_box
import boxes
import camera
import light
import render
from obj_to_cocojson import AnnotatedImage, CocoJsonBuilder


def generate_foldername():
    now = datetime.now()
    return "run_" + now.strftime("%Y%m%d_%H%M%S")


# Parameter: Anzahl Box-Konfigurationen und Render pro Konfiguration
num_box_configs = 2
num_renders_per_config = 2

box_types = ["Kiste_Blau", "Kiste_Gruen"]

output_root = os.path.join(proj_dir, "outputs")
if not os.path.exists(output_root):
    os.makedirs(output_root)

run_folder = os.path.join(output_root, generate_foldername())
os.makedirs(run_folder)

output = CocoJsonBuilder()
output.set_categories(box_types)

for box_idx in range(num_box_configs):
    # Boxen generieren
    boxes.place_random_boxes(box_types, min=10, max=15)
    box_folder = os.path.join(run_folder, f"boxes_{box_idx:03d}")
    os.makedirs(box_folder)

    for render_idx in range(num_renders_per_config):
        # Kameras und Licht generieren
        camera.delete_cameras()
        light.delete_lights()
        camera.place_random_camera()
        light.place_random_light(height=1000, amount=3, area=1500)

        img_name = f"img_{render_idx:03d}.png"
        bbox_name = f"img_{render_idx:03d}_bboxes.json"
        img_path = os.path.join(box_folder, img_name)
        bbox_path = os.path.join(box_folder, bbox_name)

        # Rendern und speichern
        bpy.context.scene.render.filepath = img_path

        img_w, img_h = render.simple_render(name=img_name)

        ann_img = AnnotatedImage(
            file_name=os.path.join(box_folder, img_name),
            height=img_h,
            width=img_w,
        )

        # Bounding Boxes berechnen und speichern
        scene = bpy.context.scene
        stapel = [o for o in scene.objects if o.type == "MESH"]
        cam = scene.camera

        for kiste in stapel:
            bbox = bounding_box.object_bbox_in_image(scene, cam, kiste)
            ann_img.add_annotation(bbox=bbox, name=kiste.name)

        output.add_annotated_image(ann_img)

output.export_self_to_cocojson(dir=run_folder)
