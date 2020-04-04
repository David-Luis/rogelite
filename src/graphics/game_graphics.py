from src.model.tile import TileType
from src.graphics.sprite import Sprite
from src.graphics.sprite_animated import SpriteAnimated
from src.game.assets_manager import AssetsManager

import pygame


class GameGraphics:

    def __init__(self):

        self.show_debug_graphics = True
        self.tile_size = 64

        self.follow_game_object_x = 0
        self.follow_game_object_y = 0
        self.camera_x = 0
        self.camera_y = 0

        self.debug_font = pygame.font.Font('data/fonts/debug_font.ttf', 26)

        self.layers = [0,1]

    def follow_game_object(self, game_object, window_width, window_height):
        self.follow_game_object_x = (-game_object.tile.coords[1] * self.tile_size) + window_width / 2 - self.tile_size / 2
        self.follow_game_object_y = (-game_object.tile.coords[0] * self.tile_size) + window_height / 2

    def update(self):
        self.camera_x += (self.follow_game_object_x - self.camera_x) * 0.1
        self.camera_y += (self.follow_game_object_y - self.camera_y) * 0.1

    def draw(self, dungeon, display_surface, delta_time):

        for layer in self.layers:
            position_y = 0
            for tile_col in dungeon.tiles:
                position_x = 0
                for tile in tile_col:
                    dungeon_sprite = None

                    if tile.type is TileType.FLOOR and layer == 0:
                        dungeon_sprite = AssetsManager.get_sprite("tile_floor")
                    elif tile.type is TileType.WALL and layer == 1:
                        dungeon_sprite = AssetsManager.get_sprite("tile_wall")

                    if dungeon_sprite:
                        dungeon_sprite.blit(display_surface, (position_x * self.tile_size + self.camera_x, position_y * self.tile_size + + self.camera_y))

                    for game_object in tile.game_objects:
                        for graphic_component in game_object.get_components_of_type("GraphicComponent"):

                            if graphic_component.layer == layer and graphic_component.visible:
                                if graphic_component._animated:
                                    sprite = AssetsManager.get_animation(graphic_component.graphic_id)
                                else:
                                    sprite = AssetsManager.get_sprite(graphic_component.graphic_id)

                                if graphic_component._animated:
                                    height = graphic_component.get_size()[1]
                                else:
                                    height =  sprite.get_current_surface().get_rect().size[1]
                                draw_x = position_x * self.tile_size + self.camera_x + graphic_component.local_pos[0]
                                draw_y = position_y * self.tile_size + + self.camera_y - (height - self.tile_size) + graphic_component.local_pos[1]


                                if graphic_component.flipped:
                                    sprite.blit_flipped(display_surface, (draw_x, draw_y), graphic_component)
                                else:
                                    sprite.blit(display_surface, (draw_x, draw_y), graphic_component)

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
            graphic_component = game_object.get_components_of_type("GraphicComponent")[0]

            life = game_object.get_components_of_type("DestructibleComponent")[0].life
            white = (255, 255, 255)
            text = self.debug_font.render("{}".format(life), True, white)
            textRect = text.get_rect()
            size = AssetsManager.get_sprite(graphic_component.graphic_id).get_current_surface().get_rect().size
            height = size[1]
            draw_x = position_x * self.tile_size + self.camera_x + self.tile_size*0.5
            draw_y = position_y * self.tile_size + self.camera_y + self.tile_size - height - 5
            textRect.center = (draw_x, draw_y)
            display_surface.blit(text, textRect)
