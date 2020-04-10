from src.application_base import ApplicationConfig
from src.editor.editor_application import EditorApplication

if __name__ == '__main__':
    applicationConfig = ApplicationConfig()
    applicationConfig.window_width = 1366
    applicationConfig.window_height = 768
    applicationConfig.window_title = "Roguelite Editor"
    game = EditorApplication(applicationConfig)
    game.initialize()
    game.start_game_loop()
