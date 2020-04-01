import pygame

from src.engine.pygame.pygame_application import PyGameApplication
from src.graphics.game_graphics import GameGraphics
from src.model.components.movable_component import MovementDirection
from src.model.dungeon_loader import DungeonLoader
from src.game.game_objects_factory import GameObjectsFactory
from src.game.player import Player


class RogueliteGame(PyGameApplication):
    def __init__(self, config):
        PyGameApplication.__init__(self, config)
        self._game_objects = []

    def _init_model(self):
        self.dungeon = DungeonLoader.load_from_tsv("data/dungeons/test_dungeon.tsv")
        GameObjectsFactory.init(self._game_objects, self.dungeon)
        self.player = GameObjectsFactory.add_game_object_using_cls(Player, "data/game/player.json", 3, 1)
        GameObjectsFactory.set_player(self.player)

        GameObjectsFactory.add_enemy_game_object("data/game/enemy1.json", 4, 5)
        GameObjectsFactory.add_enemy_game_object("data/game/enemy2.json", 7, 9)

    def _init_graphics(self):
        self.game_graphics = GameGraphics()
        self.game_graphics.follow_game_object(self.player, self.application_config.window_width,
                                              self.application_config.window_height)

    def _update(self):
        PyGameApplication._update(self)

        for game_object in self._game_objects:
            game_object.update(self.delta_time)
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
        self.game_graphics.draw(self.dungeon, self.main_surface)

        if self.game_graphics.show_debug_graphics:
            self.game_graphics.draw_debug(self.dungeon, self.main_surface)

    def _on_event(self, event):
        PyGameApplication._on_event(self, event)

        if event.type == pygame.KEYDOWN and event.key == pygame.K_LEFT:
            self.player.get_components_by_type("MovableComponent")[0].try_move_direction(MovementDirection.LEFT)
            self.game_graphics.follow_game_object(self.player, self.application_config.window_width, self.application_config.window_height)
            self._process_turn()
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_RIGHT:
            self.player.get_components_by_type("MovableComponent")[0].try_move_direction(MovementDirection.RIGHT)
            self.game_graphics.follow_game_object(self.player, self.application_config.window_width, self.application_config.window_height)
            self._process_turn()
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_UP:
            self.player.get_components_by_type("MovableComponent")[0].try_move_direction(MovementDirection.UP)
            self.game_graphics.follow_game_object(self.player, self.application_config.window_width, self.application_config.window_height)
            self._process_turn()
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_DOWN:
            self.player.get_components_by_type("MovableComponent")[0].try_move_direction(MovementDirection.DOWN)
            self.game_graphics.follow_game_object(self.player, self.application_config.window_width, self.application_config.window_height)
            self._process_turn()
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            self._process_turn()

    def initialize(self):
        PyGameApplication.initialize(self)
        self._init_model()
        self._init_graphics();

