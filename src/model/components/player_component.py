from src.model.components.component import Component
from src.game.animations_controller import AnimationsController


class PlayerComponent(Component):

    def __init__(self, game_object, description):
        Component.__init__(self, game_object, "PlayerComponent")
        self.behaviour = description["behaviour"]
        self.player = None
        self.animation_controller = AnimationsController(game_object)
        self.movable_component = self.game_object.get_components_of_type("MovableComponent")[0]

    def update(self, delta_time):
        self.animation_controller.update(delta_time)

    def on_component_event(self, component, event):
        self.animation_controller.on_component_event(event)

    def try_move_direction(self, direction):
        self.movable_component.try_move_direction(direction)

