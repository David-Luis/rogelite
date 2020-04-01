from src.model.components.component import Component
from src.model.tile import TileType
from enum import Enum


class MovementDirection(Enum):
    LEFT = 1
    RIGHT = 2
    UP = 3
    DOWN = 4


class MovableComponent(Component):

    def __init__(self, game_object):
        Component.__init__(self, game_object, "MovableComponent")
        self.dungeon = game_object.dungeon

    def try_move_direction(self, direction):
        new_position_coords = self.game_object.tile.coords[:]
        if direction is MovementDirection.LEFT:
            new_position_coords[1] -= 1
        elif direction is MovementDirection.RIGHT:
            new_position_coords[1] += 1
        elif direction is MovementDirection.UP:
            new_position_coords[0] -= 1
        elif direction is MovementDirection.DOWN:
            new_position_coords[0] += 1

        requested_tile = self.dungeon.tiles[new_position_coords[0]][new_position_coords[1]]
        self._try_move_tile(requested_tile, can_act_on_game_object=True)

    def _try_move_tile(self, requested_tile, can_act_on_game_object):
        if requested_tile.type is TileType.FLOOR:
            if requested_tile.game_objects:
                if can_act_on_game_object:
                    for game_object in requested_tile.game_objects[:]:
                        self.game_object.act_on_other_game_object(game_object)

                    self._try_move_tile(requested_tile, False)
            else:
                requested_tile.game_objects = self.game_object.tile.game_objects
                self.game_object.tile.game_objects = []
                self.game_object.tile = requested_tile
