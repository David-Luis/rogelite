class Component:

    def __init__(self, game_object, type):
        self.game_object = game_object
        self.type = type

    def update(self, delta_time):
        pass

    def process_turn(self):
        pass

    def act_on_game_object(self, game_object):
        pass

    def on_destroy(self):
        pass

    def on_component_event(self, component, event):
        pass

