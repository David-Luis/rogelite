class Component:

    def __init__(self, game_object, type):
        self.game_object = game_object
        self.type = type

    def update(self):
        pass

    def act_on_game_object(self, game_object):
        pass

    def on_destroy(self):
        pass

