from src.graphics.sprite import Sprite

class SpriteAnimated(Sprite):
    def __init__(self, file, with_alpha = True):
        Sprite.__init__(self, file, with_alpha)

    def blit(self, display_surface, position, graphic_component):
        current_frame = graphic_component.get_current_frame()
        x = current_frame["x"]
        y = current_frame["y"]
        width = current_frame["width"]
        height = current_frame["height"]

        self._subtexture_rectangle = (x, y, width, height)
        Sprite.blit(self, display_surface, position)

    def blit_flipped(self, display_surface, position, graphic_component):
        current_frame = graphic_component.get_current_frame()
        x = current_frame["x"]
        y = current_frame["y"]
        width = current_frame["width"]
        height = current_frame["height"]

        self._subtexture_rectangle = (x, y, width, height)
        Sprite.blit_flipped(self, display_surface, position)

