import pygame

from src.engine.pygame.pygame_application import PyGameApplication
from src.graphics.game_graphics import GameGraphics
from src.model.components.movable_component import MovementDirection
from src.model.dungeon_loader import DungeonLoader
from src.model.game_object import GameObject
from src.model.tile import TileType
from src.game.assets_manager import AssetsManager


class RogueliteGame(PyGameApplication):
    def __init__(self, config):
        PyGameApplication.__init__(self, config)
        self._game_objects = []
        self.dungeon = None

    def _init_model(self):
        self.dungeon = DungeonLoader.load_from_tsv("data/dungeons/test_dungeon.tsv")
        self.player = self.add_game_object("data/game/player.json", self.dungeon.tiles[3][1]).get_components_of_type("PlayerComponent")[0]

        self.add_enemy_game_object("data/game/enemy1.json", self.dungeon.tiles[4][5])
        self.add_enemy_game_object("data/game/enemy2.json", self.dungeon.tiles[7][9])

    def _init_graphics(self):
        self.game_graphics = GameGraphics()
        self.game_graphics.follow_game_object(self.player.game_object, self.application_config.window_width,
                                              self.application_config.window_height)

    def add_game_object(self, file_definition, tile):
        game_object = None
        if tile.type == TileType.FLOOR:
            game_object = GameObject.from_json(self, file_definition, tile)
            tile.game_objects.append(game_object)
            self._game_objects.append(game_object)

        return game_object

    def add_enemy_game_object(self, file_definition, tile):
        enemy_game_object = self.add_game_object(file_definition, tile)
        if enemy_game_object:
            enemy_game_object.get_components_of_type("EnemyComponent")[0].set_player(self.player.game_object)

        return enemy_game_object

    def _update(self):
        PyGameApplication._update(self)

        game_objects_to_destroy = []
        for game_object in self._game_objects[:]:
            if not game_object.mark_as_destruct:
                game_object.update(self.delta_time)
            else:
                game_objects_to_destroy.append(game_object)

        for game_object_to_destroy in game_objects_to_destroy:
            game_object_to_destroy.destroy()
            self._game_objects.remove(game_object_to_destroy)

        self.game_graphics.update()

    def _process_turn(self):
        game_objects_to_destroy = []
        for game_object in self._game_objects[:]:
            if not game_object.mark_as_destruct:
                game_object.process_turn()
            else:
                game_objects_to_destroy.append(game_object)

        for game_object_to_destroy in game_objects_to_destroy:
            game_object_to_destroy.destroy()
            self._game_objects.remove(game_object_to_destroy)


    def _render(self):

        if self.dungeon:
            self.game_graphics.draw(self.dungeon, self.main_surface, self.delta_time)

            if self.game_graphics.show_debug_graphics:
                self.game_graphics.draw_debug(self.dungeon, self.main_surface)

    def on_component_event(self, component, event):
        if event["name"] == "create_game_object":
            coords = event["coords"]
            object_class = event.get("class", "None")
            if object_class == "Enemy":
                self.add_enemy_game_object(event["game_object_def"], self.dungeon.tiles[coords[0]][coords[1]])
            else:
                self.add_game_object(event["game_object_def"], self.dungeon.tiles[coords[0]][coords[1]])

    def _on_event(self, event):
        PyGameApplication._on_event(self, event)

        if event.type == pygame.KEYDOWN and (event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT or
                                             event.key == pygame.K_UP or event.key == pygame.K_DOWN or
                                             event.key == pygame.K_SPACE):

            if event.key == pygame.K_LEFT:
                self.player.try_move_direction(MovementDirection.LEFT)
            elif event.key == pygame.K_RIGHT:
                self.player.try_move_direction(MovementDirection.RIGHT)
            elif event.key == pygame.K_UP:
                self.player.try_move_direction(MovementDirection.UP)
            elif event.key == pygame.K_DOWN:
                self.player.try_move_direction(MovementDirection.DOWN)

            self.game_graphics.follow_game_object(self.player.game_object, self.application_config.window_width,
                                                  self.application_config.window_height)
            self._process_turn()

    def initialize(self):
        PyGameApplication.initialize(self)

        AssetsManager.load_textures_definition()
        AssetsManager.load_animation_definition()

        self._init_model()
        self._init_graphics()


