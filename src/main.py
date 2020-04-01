from src.application_base import ApplicationConfig
from src.game.roguelite_game import RogueliteGame

if __name__ == '__main__':
    applicationConfig = ApplicationConfig()
    applicationConfig.window_width = 1366
    applicationConfig.window_height = 768
    applicationConfig.window_title = "Roguelite"
    game = RogueliteGame(applicationConfig)
    game.initialize()
    game.game_loop()
