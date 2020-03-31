from src.engine.pygame.pygame_application import PyGameApplication

class EditorApplication(PyGameApplication):
    def __init__(self, config):
        PyGameApplication.__init__(self, config)
        self._game_objects = []
