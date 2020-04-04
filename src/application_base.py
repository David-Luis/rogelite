class ApplicationConfig:
    def __init__(self):
        self.window_width = 1024
        self.window_height = 768
        self.window_title = 'Game'


class ApplicationBase:
    def __init__(self, config):
        self.application_config = config

    def initialize(self):
        pass

    def game_loop(self):
        pass


