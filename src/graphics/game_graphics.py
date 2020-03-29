from src.model.tile import TileType

import pygame

class GameGraphics:

    def __init__(self):
        self._floor_surface = pygame.image.load("data/textures/tile_floor.png").convert()
        self._wall_surface = pygame.image.load("data/textures/tile_wall.png").convert()

        self.graphic_ids = {"player": pygame.image.load("data/textures/player.png").convert_alpha(),
                            "enemy1": pygame.image.load("data/textures/enemy1.png").convert_alpha()}



    def draw(self, dungeon, display_surface):
        position_y = 0
        for tile_row in dungeon.tiles:
            position_x = 0
            for tile in tile_row:
                if tile.type is TileType.FLOOR:
                    display_surface.blit(self._floor_surface, (position_x * 32, position_y * 32))
                elif tile.type is TileType.WALL:
                    display_surface.blit(self._wall_surface, (position_x * 32, position_y * 32))

                for game_object in tile.game_objects:
                    for graphic_component in game_object.get_components_by_type("GraphicComponent"):

                        if graphic_component.graphic_id in self.graphic_ids:
                            display_surface.blit(self.graphic_ids[graphic_component.graphic_id], (position_x * 32, position_y * 32))

                position_x += 1

            position_y += 1
