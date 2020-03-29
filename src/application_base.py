import pygame


class ApplicationConfig():
    def __init__(self):
        self.window_width = 1024
        self.window_height = 768
        self.window_title = 'My new game'


class ApplicationBase():
    def __init__(self, config):
        self.application_config = config
        self.running = True
        self.display_surface = None
        self.main_surface = None
        self.timer = pygame.time.Clock()

    def _init_engine(self):
        self.running = True
        pygame.init()
        pygame.display.set_caption(self.application_config.window_title)

        self.display_surface = pygame.display.set_mode(( self.application_config.window_width,  self.application_config.window_height), pygame.HWSURFACE)
        self.main_surface = pygame.Surface(( self.application_config.window_width,  self.application_config.window_height))

    def _on_event(self, event):
        if event.type == pygame.QUIT:
            self.running = False
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            self.running = False

    def _update(self):
        pass

    def _render(self):
        pass

    def _on_render(self):
        self.display_surface.fill((0, 0, 0))
        self._render()
        pygame.display.flip()

    def _cleanup(self):
        pygame.quit()

    def initialize(self):
        self._init_engine()

    def game_loop(self):
        while self.running:
            self.timer.tick(60)

            for event in pygame.event.get():
                self._on_event(event)

            self._update()
            self._on_render()

        self._cleanup()


