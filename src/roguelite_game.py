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
        game_object = GameObject.from_json(file_definition)
        game_object_tile = self.dungeon.tiles[row][col]
        game_object_tile.game_objects.append(game_object)

        if game_object.get_components_by_type("MovableComponent"):
            game_object.get_components_by_type("MovableComponent")[0].set_tile(game_object_tile)
            game_object.get_components_by_type("MovableComponent")[0].set_dungeon(dungeon)

        return game_object

    def _init_model(self):
        self.dungeon = DungeonLoader.load_from_tsv("data/dungeons/test_dungeon.tsv")
        self.player = self._add_game_object("data/game/player.json", self.dungeon, 3, 1)

        self._add_game_object("data/game/enemy1.json", self.dungeon, 3, 3)

    def _init_graphics(self):
        self.game_graphics = GameGraphics()

    def _update(self):
        self.game_graphics.camera_x = (-self.player.get_components_by_type("MovableComponent")[0].tile.coords[1] * 32) + self.application_config.window_width / 2
        self.game_graphics.camera_y = (-self.player.get_components_by_type("MovableComponent")[0].tile.coords[0] * 32) + self.application_config.window_height / 2
        pass

    def _render(self):
        self.game_graphics.draw(self.dungeon, self.main_surface)
        #self.display_surface.blit(self.main_surface, (0, 0))

    def _on_event(self, event):
        ApplicationBase._on_event(self, event)

        if event.type == pygame.KEYDOWN and event.key == pygame.K_LEFT:
            self.player.get_components_by_type("MovableComponent")[0].try_move(MovementDirection.LEFT)
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_RIGHT:
            self.player.get_components_by_type("MovableComponent")[0].try_move(MovementDirection.RIGHT)
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_UP:
            self.player.get_components_by_type("MovableComponent")[0].try_move(MovementDirection.UP)
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_DOWN:
            self.player.get_components_by_type("MovableComponent")[0].try_move(MovementDirection.DOWN)

    def initialize(self):
        ApplicationBase.initialize(self)
        self._init_model()
        self._init_graphics();


