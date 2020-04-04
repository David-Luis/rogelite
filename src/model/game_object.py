from src.model.components.graphic_component import GraphicComponent
from src.model.components.movable_component import MovableComponent
from src.model.components.destructible_component import DestructibleComponent
from src.model.components.attacker_component import AttackerComponent
from src.model.components.enemy_component import EnemyComponent
from src.model.components.enemy_spawner_component import EnemySpawnerComponent
from src.model.components.delete_in_time_component import DeleteInTimeComponent
from src.model.components.player_component import PlayerComponent

import json


class GameObject:

    def __init__(self, game):
        self._components = {}
        self.mark_as_destruct = False
        self.tile = None
        self.game = game

    def add_component(self, component):
        if component.type not in self._components:
            self._components[component.type] = []

        self._components[component.type].append(component)

    def has_component_of_type(self, type):
        return type in self._components

    def get_components_of_type(self, type):
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

        if self in self.tile.game_objects:
            self.tile.game_objects.remove(self)
        else:
            print(self)

    def process_turn(self):
        for component_type in self._components:
            for component in self._components[component_type]:
                component.process_turn()

    def update(self, delta_time):
        for component_type in self._components:
            for component in self._components[component_type]:
                component.update(delta_time)

    def on_create(self):
        pass

    def on_component_event(self, component, event):
        self.game.on_component_event(component, event)
        for component_type in self._components:
            for component in self._components[component_type]:
                component.on_component_event(component, event)

    @classmethod
    def from_json(cls, game, json_file, tile):
        game_object = GameObject(game)

        with open(json_file) as json_data:
            game_object_info = json.load(json_data)
            game_object.tile = tile
            game_object.dungeon = game.dungeon
            game_object.type = game_object_info["type"]

            if "graphics" in game_object_info:
                game_object.add_component(GraphicComponent(game_object, game_object_info["graphics"]))

            if "movable" in game_object_info:
                game_object.add_component(MovableComponent(game_object))

            if "destructible" in game_object_info:
                game_object.add_component(DestructibleComponent(game_object, game_object_info["destructible"]))

            if "attacker" in game_object_info:
                game_object.add_component(AttackerComponent(game_object, game_object_info["attacker"]))

            if "enemy_spawner" in game_object_info:
                game_object.add_component(EnemySpawnerComponent(game_object, game_object_info["enemy_spawner"]))

            if "delete_in_time" in game_object_info:
                game_object.add_component(DeleteInTimeComponent(game_object, game_object_info["delete_in_time"]))

            if "enemy" in game_object_info:
                game_object.add_component(EnemyComponent(game_object, game_object_info["enemy"]))

            if "player" in game_object_info:
                game_object.add_component(PlayerComponent(game_object, game_object_info["player"]))

        game_object.on_create()

        return game_object

