from src.model.components.component import Component
from src.model.components.movable_component import MovementDirection
from src.game.animations_controller import AnimationsController


class EnemyComponent(Component):

    def __init__(self, game_object, description):
        Component.__init__(self, game_object, "EnemyComponent")
        self.behaviour = description["behaviour"]
        self.player = None
        self.animation_controller = AnimationsController(game_object)
        self.movable_component = self.game_object.get_components_of_type("MovableComponent")[0]

    def update(self, delta_time):
        self.animation_controller.update(delta_time)

    def on_component_event(self, component, event):
        self.animation_controller.on_component_event(event)

    def set_player(self, player_game_object):
        self.player = player_game_object

    def process_turn(self):
        if self.player.tile.coords[0] < self.game_object.tile.coords[0]:
            self.movable_component.try_move_direction(MovementDirection.UP)
        elif self.player.tile.coords[0] > self.game_object.tile.coords[0]:
            self.movable_component.try_move_direction(MovementDirection.DOWN)
        elif self.player.tile.coords[1] < self.game_object.tile.coords[1]:
            self.movable_component.try_move_direction(MovementDirection.LEFT)
        elif self.player.tile.coords[1] > self.game_object.tile.coords[1]:
            self.movable_component.try_move_direction(MovementDirection.RIGHT)

