from render import RENDER_METHODS

class Config:
    def __init__(
        self,
        stack_height_min=5,
        stack_height_max=10,
        generated_scenes=1,
        imgs_per_scene=1,
        render_method="fast",
        box_types=[],
    ):
        self.stack_height_min = stack_height_min
        self.stack_height_max = stack_height_max
        self.generated_scenes = generated_scenes
        self.imgs_per_scene = imgs_per_scene
        self.render_method = RENDER_METHODS[render_method]
        self.box_types = box_types
