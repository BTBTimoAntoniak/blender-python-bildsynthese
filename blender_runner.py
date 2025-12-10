import subprocess

blender = (
    "blender"  # z.B. "/usr/bin/blender" oder r"C:\Program Files\Blender\blender.exe"
)
blend_file = "blender-python-bildsynthese/Playground.blend"
script = "blender-python-bildsynthese/playground.py"


def run(
    stack_height_min,
    stack_height_max,
    generated_scenes,
    imgs_per_scene,
    render_method,
    box_types,
):
    args = [
        blender,
        "--background",  # headless
        blend_file,
        "--python",
        script,
        "--",  # alles danach landet in sys.argv im Blender‑Script
    ]

    if stack_height_min is not None:
        args += ["--stack-height-min", str(stack_height_min)]

    if stack_height_max is not None:
        args += ["--stack-height-max", str(stack_height_max)]

    if generated_scenes is not None:
        args += ["--generated-scenes", str(generated_scenes)]

    if imgs_per_scene is not None:
        args += ["--imgs-per-scene", str(imgs_per_scene)]

    if render_method is not None:
        args += ["--render-method", str(render_method)]

    if box_types:
        args += ["--box-types"] + [str(bt) for bt in box_types]

    print(args)

    subprocess.run(args, check=True)
