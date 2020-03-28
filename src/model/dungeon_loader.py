from src.model.dungeon import Dungeon
from src.model.tile import TileType, Tile

import csv


class DungeonLoader:

    @classmethod
    def load_from_tsv(cls, path):
        dungeon = Dungeon()

        with open(path) as file:
            tsv_reader = csv.reader(file, delimiter="\t")
            current_row = 0
            for line in tsv_reader:
                current_col = 0
                current_tiles = []
                for tile_info in line:
                    current_tiles.append(cls._get_tile(tile_info, [current_row, current_col]))
                    current_col += 1

                #print(current_tile_row)
                dungeon.tiles.append(current_tiles)
                current_row += 1

        return dungeon

    @classmethod
    def _get_tile(cls, tile, coords):
        tile_type = TileType.FLOOR
        if not tile:
            tile_type = TileType.WALL

        return Tile(tile_type, coords)


