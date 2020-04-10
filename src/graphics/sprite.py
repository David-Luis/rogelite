import pygame


class Sprite:
    def __init__(self, file, with_alpha = True):
        if with_alpha:
            self.surface = pygame.image.load(file).convert_alpha()
        else:
            self.surface = pygame.image.load(file).convert()

        self._subtexture_rectangle = None
        self._visible = True

    def get_surface(self):
        return self.surface

    def blit(self, display_surface, position, graphic_component=None):
        if not self._visible:
            return

        if graphic_component and graphic_component.animated:
            current_frame = graphic_component.get_current_frame()
            x = current_frame["x"]
            y = current_frame["y"]
            width = current_frame["width"]
            height = current_frame["height"]

            self._subtexture_rectangle = (x, y, width, height)

        display_surface.blit(self.surface, position, area=self._subtexture_rectangle)

    def blit_flipped(self, display_surface, position, graphic_component=None):
        if not self._visible:
            return

        if graphic_component and graphic_component.animated:
            current_frame = graphic_component.get_current_frame()
            x = current_frame["x"]
            y = current_frame["y"]
            width = current_frame["width"]
            height = current_frame["height"]

            self._subtexture_rectangle = (x, y, width, height)

        display_surface.blit(pygame.transform.flip(self.surface, True, False), position)

