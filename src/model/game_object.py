from src.model.components.graphic_component import GraphicComponent
from src.model.components.movable_component import MovableComponent

import json

class GameObject:

    def __init__(self):
        self._components = {}

    def add_component(self, component):
        if component.type not in self._components:
            self._components[component.type] = []

        self._components[component.type].append(component)

    def get_components_by_type(self, type):
        if type not in self._components:
            return None

        return self._components[type]

    @classmethod
    def from_json(cls, json_file):
        game_object = GameObject()

        with open(json_file) as json_data:
            game_object_info = json.load(json_data)

            if game_object_info["graphics"]:
                game_object.add_component(GraphicComponent(game_object_info["graphics"]["texture_id"]))

            if game_object_info["movable"]:
                game_object.add_component(MovableComponent())

        return game_object

