import argparse
import sys

from render import RENDER_METHODS

# Beispiel CLI (reines Python):
# python render_pipeline.py --stack-height-min 5 --stack-height-max 12 \
#     --generated-scenes 20 --imgs-per-scene 3 --render-method slow \
#     --box-types cube tall_box short_box
#
# Blender (headless):
# blender --background --python render_pipeline.py -- --stack-height-min 5 \
#     --stack-height-max 12 --render-method slow --box-types cube tall_box


_MISSING = object()


class Config:
    """Konfiguration, deren Standardwerte automatisch durch CLI-Args überschrieben werden können."""

    _CLI_CACHE = None

    def __init__(
        self,
        stack_height_min=_MISSING,
        stack_height_max=_MISSING,
        generated_scenes=_MISSING,
        imgs_per_scene=_MISSING,
        render_method=_MISSING,
        box_types=_MISSING,
        argv=None,
    ):
        args = self._parse_cli_args(argv)

        self.stack_height_min = self._resolve(
            "stack_height_min", stack_height_min, args, 5
        )
        self.stack_height_max = self._resolve(
            "stack_height_max", stack_height_max, args, 10
        )
        if self.stack_height_min > self.stack_height_max:
            raise ValueError("stack_height_min must be <= stack_height_max")

        self.generated_scenes = self._resolve(
            "generated_scenes", generated_scenes, args, 1
        )
        self.imgs_per_scene = self._resolve("imgs_per_scene", imgs_per_scene, args, 1)

        method_value = self._resolve("render_method", render_method, args, "fast")
        self.render_method = self._resolve_render_method(method_value)

        box_value = self._resolve("box_types", box_types, args, None)
        self.box_types = list(box_value) if box_value is not None else []

    @classmethod
    def from_args(cls, argv=None):
        """Erzeugt direkt eine Config-Instanz aus CLI-Argumenten."""
        return cls(argv=argv)

    @classmethod
    def _parse_cli_args(cls, argv=None):
        if argv is None and cls._CLI_CACHE is not None:
            return cls._CLI_CACHE

        parser = argparse.ArgumentParser(add_help=False)
        parser.add_argument("--stack-height-min", type=int)
        parser.add_argument("--stack-height-max", type=int)
        parser.add_argument("--generated-scenes", type=int)
        parser.add_argument("--imgs-per-scene", type=int)
        parser.add_argument(
            "--render-method", type=str, choices=list(RENDER_METHODS.keys())
        )
        parser.add_argument("--box-types", nargs="+")

        normalized = cls._normalize_argv(argv)
        namespace, _ = parser.parse_known_args(normalized)

        if argv is None:
            cls._CLI_CACHE = namespace
        return namespace

    @staticmethod
    def _normalize_argv(argv):
        if argv is None:
            argv = sys.argv[1:]
        else:
            argv = list(argv)

        if "--" in argv:
            argv = argv[argv.index("--") + 1 :]
        return argv

    def _resolve(self, key, explicit, cli_namespace, default):
        if explicit is not _MISSING:
            return explicit
        value = getattr(cli_namespace, key, None)
        if value is not None:
            return value
        return default

    @staticmethod
    def _resolve_render_method(value):
        if callable(value):
            return value
        if not isinstance(value, str):
            raise TypeError(
                f"render_method must be a string key or callable; received {value!r}"
            )
        try:
            return RENDER_METHODS[value]
        except KeyError:
            raise KeyError(
                f"Unknown render method '{value}'. Valid keys: {', '.join(RENDER_METHODS)}"
            )
