from src.model.tile import TileType

import pygame

class GameGraphics:

    def __init__(self):

        self.camera_x = 0
        self.camera_y = 0

        self._floor_surface = pygame.image.load("data/textures/tile_floor.png").convert()
        self._wall_surface = pygame.image.load("data/textures/tile_wall.png").convert()

        self.graphic_ids = {"player": pygame.image.load("data/textures/player.png").convert_alpha(),
                            "enemy1": pygame.image.load("data/textures/enemy1.png").convert_alpha()}



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
                    display_surface.blit(dungeon_surface, (position_x * 32 + self.camera_x, position_y * 32 + + self.camera_y))

                for game_object in tile.game_objects:
                    for graphic_component in game_object.get_components_by_type("GraphicComponent"):

                        if graphic_component.graphic_id in self.graphic_ids:
                            display_surface.blit(self.graphic_ids[graphic_component.graphic_id], (position_x * 32 + + self.camera_x, position_y * 32 + + self.camera_y))

                position_x += 1

            position_y += 1
