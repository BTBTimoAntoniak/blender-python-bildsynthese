import bpy


def simple_render(name="img_0001"):
    s = bpy.context.scene
    s.render.engine = "BLENDER_EEVEE"
    s.render.image_settings.file_format = "PNG"
    s.render.resolution_x = 1280
    s.render.resolution_y = 720
    s.render.resolution_percentage = 100
    s.eevee.taa_samples = 16
    bpy.ops.render.render(write_still=True)
    return s.render.resolution_x, s.render.resolution_y


RENDER_METHODS = {"fast": simple_render}
