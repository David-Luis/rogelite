from application_base import ApplicationBase
from src.model.dungeon_loader import DungeonLoader
from src.model.game_object import GameObject
from src.model.components.movable_component import MovementDirection
from src.graphics.game_graphics import GameGraphics

import pygame

class RogueliteGame(ApplicationBase):
    def __init__(self, config):
        ApplicationBase.__init__(self, config)

    def _add_game_object(self, file_definition, dungeon, row, col):
        game_object_tile = self.dungeon.tiles[row][col]
        game_object = GameObject.from_json(file_definition, game_object_tile, dungeon)
        game_object_tile.game_objects.append(game_object)

        return game_object

    def _init_model(self):
        self.dungeon = DungeonLoader.load_from_tsv("data/dungeons/test_dungeon.tsv")
        self.player = self._add_game_object("data/game/player.json", self.dungeon, 3, 1)

        self._add_game_object("data/game/enemy1.json", self.dungeon, 3, 3)

    def _init_graphics(self):
        self.game_graphics = GameGraphics()
        self.game_graphics.follow_game_object(self.player, self.application_config.window_width,
                                              self.application_config.window_height)

    def _update(self):
        self.game_graphics.update()

    def _render(self):
        self.game_graphics.draw(self.dungeon, self.main_surface)

        if self.game_graphics.show_debug_graphics:
            self.game_graphics.draw_debug(self.dungeon, self.main_surface)

    def _on_event(self, event):
        ApplicationBase._on_event(self, event)

        if event.type == pygame.KEYDOWN and event.key == pygame.K_LEFT:
            self.player.get_components_by_type("MovableComponent")[0].try_move_direction(MovementDirection.LEFT)
            self.game_graphics.follow_game_object(self.player, self.application_config.window_width, self.application_config.window_height)
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_RIGHT:
            self.player.get_components_by_type("MovableComponent")[0].try_move_direction(MovementDirection.RIGHT)
            self.game_graphics.follow_game_object(self.player, self.application_config.window_width, self.application_config.window_height)
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_UP:
            self.player.get_components_by_type("MovableComponent")[0].try_move_direction(MovementDirection.UP)
            self.game_graphics.follow_game_object(self.player, self.application_config.window_width, self.application_config.window_height)
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_DOWN:
            self.player.get_components_by_type("MovableComponent")[0].try_move_direction(MovementDirection.DOWN)
            self.game_graphics.follow_game_object(self.player, self.application_config.window_width, self.application_config.window_height)

    def initialize(self):
        ApplicationBase.initialize(self)
        self._init_model()
        self._init_graphics();


