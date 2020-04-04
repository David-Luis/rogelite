from src.graphics.sprite import Sprite
from src.graphics.sprite_animated import SpriteAnimated

import json
import os


class AssetsManager:
    texture_definitions = {}
    animation_definitions = {}
    sprites = {}
    animations = {}

    @classmethod
    def load_textures_definition(cls):
        with open("data/textures.json") as json_data:
            textures_def = json.load(json_data)
            for texture_definition_info in textures_def["textures"]:
                id = os.path.splitext(os.path.basename(texture_definition_info["path"]))[0]
                path = texture_definition_info["path"]

                alpha = True
                if "alpha" in texture_definition_info:
                    alpha = texture_definition_info["alpha"]

                cls.texture_definitions[id] = {"path": path, "alpha": alpha}

    @classmethod
    def load_animation_definition(cls):
        with open("data/animations.json") as json_data:
            animations_def = json.load(json_data)
            for animation_definition_info in animations_def["animations"]:
                id = os.path.splitext(os.path.basename(animation_definition_info["path"]))[0]
                path = animation_definition_info["path"]

                alpha = True
                if "alpha" in animation_definition_info:
                    alpha = animation_definition_info["alpha"]

                cls.animation_definitions[id] = {"path": path, "alpha": alpha}

    @classmethod
    def get_sprite(cls, id):
        if id in cls.sprites:
            return cls.sprites[id]
        elif id in cls.texture_definitions:
            definition = cls.texture_definitions[id]
            cls.sprites[id] = Sprite(definition["path"], definition["alpha"])
            return cls.sprites[id]
        else:
            return None

    @classmethod
    def get_animation(cls, id):
        if id in cls.animations:
            return cls.animations[id]
        elif id in cls.animation_definitions:
            definition = cls.animation_definitions[id]
            cls.animations[id] = SpriteAnimated(definition["path"], definition["alpha"])
            return cls.animations[id]
        else:
            return None




