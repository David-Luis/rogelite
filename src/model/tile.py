from enum import Enum


class TileType(Enum):
    FLOOR = 1
    WALL = 2


class Tile:
    def __init__(self, tile_type, coords):
        self.type = tile_type
        self.game_objects = []
        self.coords = coords

    def __str__(self):
        if self.type is TileType.FLOOR:
            return "F"
        else:
            return "W"

    def __repr__(self):
        return self.__str__()
