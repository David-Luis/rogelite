from src.model.components.component import Component
from src.model.components.movable_component import MovementDirection


class EnemyComponent(Component):

    def __init__(self, game_object, behaviour):
        Component.__init__(self, game_object, "EnemyComponent")
        self.behaviour = behaviour
        self.player = None

    def set_player(self, player_game_object):
        self.player = player_game_object

    def update(self):
        if self.player.tile.coords[0] < self.game_object.tile.coords[0]:
            self.game_object.get_components_by_type("MovableComponent")[0].try_move_direction(MovementDirection.UP)
        elif self.player.tile.coords[0] > self.game_object.tile.coords[0]:
            self.game_object.get_components_by_type("MovableComponent")[0].try_move_direction(MovementDirection.DOWN)
        elif self.player.tile.coords[1] < self.game_object.tile.coords[1]:
            self.game_object.get_components_by_type("MovableComponent")[0].try_move_direction(MovementDirection.LEFT)
        elif self.player.tile.coords[1] > self.game_object.tile.coords[1]:
            self.game_object.get_components_by_type("MovableComponent")[0].try_move_direction(MovementDirection.RIGHT)

