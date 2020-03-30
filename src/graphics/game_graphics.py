from src.model.tile import TileType

import pygame

class GameGraphics:

    def __init__(self):

        self.show_debug_graphics = True
        self.tile_size = 64

        self.follow_game_object_x = 0
        self.follow_game_object_y = 0
        self.camera_x = 0
        self.camera_y = 0

        self._floor_surface = pygame.image.load("data/textures/tile_floor.png").convert()
        self._wall_surface = pygame.image.load("data/textures/tile_wall.png").convert()

        self.graphic_ids = {"player": pygame.image.load("data/textures/player.png").convert_alpha(),
                            "enemy1": pygame.image.load("data/textures/enemy1.png").convert_alpha()}

        self.debug_font = pygame.font.Font('data/fonts/debug_font.ttf', 26)


    def follow_game_object(self, game_object, window_width, window_height):
        self.follow_game_object_x = (-game_object.get_components_by_type("MovableComponent")[0].tile.coords[1] * self.tile_size) + window_width / 2 - self.tile_size / 2
        self.follow_game_object_y = (-game_object.get_components_by_type("MovableComponent")[0].tile.coords[0] * self.tile_size) + window_height / 2


    def update(self):
        self.camera_x += (self.follow_game_object_x - self.camera_x) * 0.1
        self.camera_y += (self.follow_game_object_y - self.camera_y) * 0.1

    def draw(self, dungeon, display_surface):
        position_y = 0
        for tile_row in dungeon.tiles:
            position_x = 0
            for tile in tile_row:
                dungeon_surface = None

                if tile.type is TileType.FLOOR:
                    dungeon_surface = self._floor_surface
                elif tile.type is TileType.WALL:
                    dungeon_surface = self._wall_surface

                if dungeon_surface:
                    display_surface.blit(dungeon_surface, (position_x * self.tile_size + self.camera_x, position_y * self.tile_size + + self.camera_y))

                for game_object in tile.game_objects:
                    for graphic_component in game_object.get_components_by_type("GraphicComponent"):

                        if graphic_component.graphic_id in self.graphic_ids:
                            display_surface.blit(self.graphic_ids[graphic_component.graphic_id], (position_x * self.tile_size + self.camera_x, position_y * self.tile_size + + self.camera_y))

                position_x += 1

            position_y += 1

    def draw_debug(self, dungeon, display_surface):
        position_y = 0
        for tile_row in dungeon.tiles:
            position_x = 0
            for tile in tile_row:
                for game_object in tile.game_objects:
                    self._draw_debug_for_game_object(display_surface, game_object, position_x, position_y)

                position_x += 1

            position_y += 1

    def _draw_debug_for_game_object(self, display_surface, game_object, position_x, position_y):
        if game_object.has_component_of_type("DestructibleComponent"):
            life = game_object.get_components_by_type("DestructibleComponent")[0].life
            white = (255, 255, 255)
            text = self.debug_font.render("{}".format(life), True, white)
            textRect = text.get_rect()
            textRect.center = (position_x * self.tile_size + self.camera_x + self.tile_size*0.5, position_y * self.tile_size + self.camera_y - self.tile_size * 0.1)
            display_surface.blit(text, textRect)
