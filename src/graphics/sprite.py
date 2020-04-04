import pygame


class Sprite:
    def __init__(self, file, with_alpha=True):
        if with_alpha:
            self.surface = pygame.image.load(file).convert_alpha()
        else:
            self.surface = pygame.image.load(file).convert()

        self._subtexture_rectangle = None
        self._visible = True

    def get_current_surface(self):
        return self.surface

    def blit(self, display_surface, position, graphic_component=None):
        if self._visible:
            display_surface.blit(self.get_current_surface(), position, area=self._subtexture_rectangle)

    def blit_flipped(self, display_surface, position, graphic_component=None):
        if self._visible:
            display_surface.blit(pygame.transform.flip(self.get_current_surface(), True, False), position)

    def update(self, delta_time):
        pass