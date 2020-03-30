from src.model.components.graphic_component import GraphicComponent
from src.model.components.movable_component import MovableComponent
from src.model.components.destructible_component import DestructibleComponent
from src.model.components.attacker_component import AttackerComponent

import json

class GameObject:

    def __init__(self):
        self._components = {}

    def add_component(self, component):
        if component.type not in self._components:
            self._components[component.type] = []

        self._components[component.type].append(component)

    def has_component_of_type(self, type):
        return type in self._components

    def get_components_by_type(self, type):
        if type not in self._components:
            return None

        return self._components[type]

    def act_on_other_game_object(self, game_object):
        for component_type in self._components:
            for component in self._components[component_type]:
                component.act_on_game_object(game_object)

    def destruct(self):
        self.tile.game_objects.remove(self)

    @classmethod
    def from_json(cls, json_file, tile, dungeon):
        game_object = GameObject()

        with open(json_file) as json_data:
            game_object_info = json.load(json_data)
            game_object.tile = tile
            game_object.dungeon = dungeon

            if "graphics" in game_object_info:
                game_object.add_component(GraphicComponent(game_object, game_object_info["graphics"]["texture_id"]))

            if "movable" in game_object_info:
                game_object.add_component(MovableComponent(game_object))

            if "destructible" in game_object_info:
                game_object.add_component(DestructibleComponent(game_object, game_object_info["destructible"]["life"]))

            if "attacker" in game_object_info:
                game_object.add_component(AttackerComponent(game_object, game_object_info["attacker"]["strength"]))

        return game_object

