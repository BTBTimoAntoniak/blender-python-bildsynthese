import os
import random

import bpy


def get_object_height(obj):
    return obj.dimensions.z


def place_random_boxes(box_types, min=5, max=100):
    # Project directory and blend file
    project_dir = os.path.dirname(bpy.data.filepath)
    boxes_blend = os.path.join(project_dir, "Kisten.blend")

    # Prepare playground: delete all objects
    bpy.ops.object.select_all(action="SELECT")
    bpy.ops.object.delete(use_global=False)

    # Generate and stack random boxes
    num_stacks = 1
    for stack_idx in range(num_stacks):
        stack_size = random.randint(min, max)
        z_offset = 0.0
        for box_idx in range(stack_size):
            box_type = random.choice(box_types)
            obj_path = os.path.join(boxes_blend, "Object", box_type)
            # print(box_type)
            bpy.ops.wm.append(
                filepath=obj_path,
                directory=os.path.join(boxes_blend, "Object"),
                filename=box_type,
            )
            # The newly added object is now selected
            new_obj = bpy.context.selected_objects[0]
            box_height = get_object_height(new_obj)
            new_obj.location = (stack_idx * 10, 0, z_offset + box_height / 2)
            z_offset += box_height

            # Slightly rotate
            # bpy.ops.transform.rotate(value=random.randint(-10, 10)*0.01, orient_axis="Z")
