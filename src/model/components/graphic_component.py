from src.model.components.component import Component

import math
import json


class AnimationInfo:
    def __init__(self):
        self.name = ""
        self.texture_width = 0
        self.texture_height = 0
        self.sub_textures = {}
        self.loop = False
        self.time_per_frame = 0
        self.frames = []
        self.frame_count = 0
        self.current_frame = 0
        self.current_frame_time = 0.0
        self.aabb = None

class GraphicComponent(Component):

    def __init__(self, game_object, definition):
        Component.__init__(self, game_object, "GraphicComponent")
        self.graphic_id = definition["texture_id"]
        self.animated = "is_animated" in definition and definition["is_animated"]
        self.local_pos = [0, 0]
        self.layer = 1
        self.flipped = False
        self.visible = True

        if self.animated:
            self._load_animation_data(definition["animation_data"])

    def _load_animation_data(self, file_path):
        texture_json = file_path + "_tex.json"
        animation_json = file_path + "_ske.json"

        with open(texture_json) as texture_json_data:
            with open(animation_json) as animation_json_data:
                texture_data = json.load(texture_json_data)
                animation_data = json.load(animation_json_data)

                self._animation_info = AnimationInfo()

                #texture_info
                self._animation_info.texture_width = texture_data["width"]
                self._animation_info.texture_height = texture_data["height"]

                for sub_texture in texture_data["SubTexture"]:
                    name = sub_texture["name"]
                    self._animation_info.sub_textures[name] = sub_texture.copy()

                #animation info
                self._animation_info.name = animation_data["name"]
                self._animation_info.loop = animation_data["armature"][0]["animation"][0].get("playTimes", False)
                self._animation_info.aabb = animation_data["armature"][0]["aabb"].copy()
                self._animation_info.time_per_frame = 1.0 / animation_data["armature"][0]["frameRate"]

                for frame in animation_data["armature"][0]["skin"][0]["slot"][0]["display"]:
                    texture_id = frame.get("path", frame["name"])
                    self._animation_info.frames.append(self._animation_info.sub_textures[texture_id])

                self._animation_info.frame_count = len(self._animation_info.frames)

    def update(self, delta_time):
        if self.animated:

            self._animation_info.current_frame_time += delta_time

            if self._animation_info.current_frame_time > self._animation_info.time_per_frame:
                self._animation_info.current_frame += math.floor(self._animation_info.current_frame_time / self._animation_info.time_per_frame)
                self._animation_info.current_frame_time = self._animation_info.current_frame_time % self._animation_info.time_per_frame

                if self._animation_info.current_frame >= self._animation_info.frame_count:
                    if self._animation_info.loop:
                        self._animation_info.current_frame = 0
                    else:
                        self._animation_info.current_frame -= 1

    def get_current_frame(self):
        if self.animated:
            return self._animation_info.frames[self._animation_info.current_frame]

        return None

    def get_size(self):
        return self._animation_info.aabb["width"], self._animation_info.aabb["height"]



