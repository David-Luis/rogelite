from src.model.game_object import GameObject
from src.model.tile import TileType
from src.game.enemy import Enemy

class GameObjectsFactory():

    @classmethod
    def init(cls, game_objects, dungeon):
        cls._game_objects = game_objects
        cls._dungeon = dungeon

    @classmethod
    def set_player(cls, player):
        cls._player = player

    @classmethod
    def add_game_object_using_cls(cls, game_object_cls, file_definition, row, col):
        game_object_tile = cls._dungeon.tiles[row][col]

        game_object = None
        if game_object_tile.type == TileType.FLOOR:
            game_object = game_object_cls.from_json(cls, file_definition, game_object_tile, cls._dungeon)
            game_object_tile.game_objects.append(game_object)
            cls._game_objects.append(game_object)

        return game_object

    @classmethod
    def add_game_object(cls, file_definition, row, col):
        return cls.add_game_object_using_cls(GameObject, file_definition, row, col)

    @classmethod
    def add_enemy_game_object(cls, file_definition, row, col):
        enemy_game_object = cls.add_game_object_using_cls(Enemy, file_definition, row, col)

        if enemy_game_object:
            enemy_game_object.get_components_by_type("EnemyComponent")[0].set_player(cls._player)

