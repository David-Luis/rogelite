import pygame

from src.model.dungeon_loader import DungeonLoader
from src.model.game_object import GameObject
from src.model.components.graphic_component import GraphicComponent
from src.model.components.movable_component import MovableComponent, MovementDirection

from src.graphics.game_graphics import GameGraphics

class Game():
    window_width = 1024
    window_height = 768
    x = 10
    y = 10

    def __init__(self):
        self.running = True
        self.display_surface = None
        self.timer = pygame.time.Clock()

    def _init_engine(self):
        pygame.init()
        self.display_surface = pygame.display.set_mode((self.window_width, self.window_height), pygame.HWSURFACE)
        pygame.display.set_caption('Roguelite')
        self.running = True

    def _init_model(self):
        self.dungeon = DungeonLoader.load_from_tsv("data/dungeons/test_dungeon.tsv")

        player_tile = self.dungeon.tiles[3][1]
        self.player = GameObject()
        self.player.add_component(GraphicComponent("player"))
        self.player.add_component(MovableComponent(self.dungeon, player_tile))
        player_tile.game_objects.append(self.player)

    def _init_graphics(self):
        self.game_graphics = GameGraphics()

    def _on_event(self, event):
        if event.type == pygame.QUIT:
            self.running = False
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            self.running = False

        if event.type == pygame.KEYDOWN and event.key == pygame.K_LEFT:
            self.player.get_components_by_type("MovableComponent")[0].try_move(MovementDirection.LEFT)
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_RIGHT:
            self.player.get_components_by_type("MovableComponent")[0].try_move(MovementDirection.RIGHT)
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_UP:
            self.player.get_components_by_type("MovableComponent")[0].try_move(MovementDirection.UP)
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_DOWN:
            self.player.get_components_by_type("MovableComponent")[0].try_move(MovementDirection.DOWN)

    def _on_loop(self):
        pass

    def _on_render(self):
        self.display_surface.fill((0, 0, 0))

        self.game_graphics.draw(self.dungeon, self.display_surface)

        pygame.display.flip()

    def _on_cleanup(self):
        pygame.quit()

    def init(self):
        self._init_engine()
        self._init_model()
        self._init_graphics();

    def game_loop(self):
        while self.running:
            self.timer.tick(60)

            for event in pygame.event.get():
                self._on_event(event)

            self._on_loop()
            self._on_render()

        self._on_cleanup()

# https://stackoverflow.com/questions/14354171/add-scrolling-to-a-platformer-in-pygame
if __name__ == '__main__':
    game = Game()
    game.init()
    game.game_loop()

