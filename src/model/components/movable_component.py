from src.model.components.component import Component
from src.model.tile import TileType
from enum import Enum


class MovementDirection(Enum):
    LEFT = 1
    RIGHT = 2
    UP = 3
    DOWN = 4

class MovableComponent(Component):

    def __init__(self, dungeon, tile):
        Component.__init__(self, "MovableComponent")
        self.dungeon = dungeon
        self.tile = tile

    def try_move(self, direction):
        new_position_coords = self.tile.coords[:]
        if direction is MovementDirection.LEFT:
            new_position_coords[1] -= 1
        elif direction is MovementDirection.RIGHT:
            new_position_coords[1] += 1
        elif direction is MovementDirection.UP:
            new_position_coords[0] -= 1
        elif direction is MovementDirection.DOWN:
            new_position_coords[0] += 1

        requested_tile = self.dungeon.tiles[new_position_coords[0]][new_position_coords[1]]

        if requested_tile.type is TileType.FLOOR:
            requested_tile.game_objects = self.tile.game_objects
            self.tile.game_objects = []
            self.tile = requested_tile
