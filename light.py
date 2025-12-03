import bpy
import os
import random
import math

def place_random_light(height=1500, amount=1, area=1500):
    project_dir = os.path.dirname(bpy.data.filepath)
    light_blend = os.path.join(project_dir, "Light.blend")

    lights = ["Area"]
    
    light_type = random.choice(lights)
    rotation = math.radians(random.randint(0,180))
    
    for lightNr in range(amount):
        x = random.uniform(- area/2, area/2)
        y = random.uniform(- area/2, area/2)
        z = height
        
        obj_path = os.path.join(light_blend, "Object", light_type)
        bpy.ops.wm.append(
            filepath=obj_path,
            directory=os.path.join(light_blend, "Object"),
            filename=light_type
        )
        
        new_obj = bpy.context.selected_objects[0]
        new_obj.location = (x, y, z)
        bpy.ops.transform.rotate(value=rotation, orient_axis="Z")


def delete_lights():
    bpy.ops.object.select_by_type(type='LIGHT')
    bpy.ops.object.delete()