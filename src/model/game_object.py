from src.model.components.graphic_component import GraphicComponent
from src.model.components.movable_component import MovableComponent
from src.model.components.destructible_component import DestructibleComponent
from src.model.components.attacker_component import AttackerComponent
from src.model.components.enemy_component import EnemyComponent
from src.model.components.enemy_spawner_component import EnemySpawnerComponent

import json


class GameObject:

    def __init__(self, game_objects_factory_cls):
        self._components = {}
        self.mark_as_destruct = False
        self.tile = None
        self.game_objects_factory_cls = game_objects_factory_cls

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

    def mark_as_destroy(self):
        self.mark_as_destruct = True

    def destroy(self):
        for component_type in self._components:
            for component in self._components[component_type]:
                component.on_destroy()

        self.tile.game_objects.remove(self)

    def process_turn(self):
        for component_type in self._components:
            for component in self._components[component_type]:
                component.update()

    def update(self, delta_time):
        pass

    def on_create(self):
        pass

    def on_component_event(self, event):
        pass

    @classmethod
    def from_json(cls, game_object_factory_cls, json_file, tile, dungeon):
        game_object = cls(game_object_factory_cls)

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

            if "enemy" in game_object_info:
                game_object.add_component(EnemyComponent(game_object, game_object_info["enemy"]["behaviour"]))

            if "enemy_spawner" in game_object_info:
                game_object.add_component(EnemySpawnerComponent(game_object, game_object_info["enemy_spawner"]["enemy"]))

        game_object.on_create()

        return game_object

