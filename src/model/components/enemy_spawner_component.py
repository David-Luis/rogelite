from src.model.components.component import Component


class EnemySpawnerComponent(Component):

    def __init__(self, game_object, definition):
        Component.__init__(self, game_object, "EnemySpawnerComponent")
        self.enemy_def = definition["enemy"]

    def on_destroy(self):
        new_enemy_position_coords1 = self.game_object.tile.coords[:]
        new_enemy_position_coords1[1] += 1

        new_enemy_position_coords2 = self.game_object.tile.coords[:]
        new_enemy_position_coords2[0] -= 1

        new_enemy_position_coords3 = self.game_object.tile.coords[:]
        new_enemy_position_coords3[0] += 1

        self.game_object.on_component_event(self,
            {"name": "create_game_object", "game_object_def": self.enemy_def, "class": "Enemy",
             "coords": new_enemy_position_coords1})

        self.game_object.on_component_event(self,
            {"name": "create_game_object", "game_object_def": self.enemy_def, "class": "Enemy",
             "coords": new_enemy_position_coords2})

        self.game_object.on_component_event(self,
            {"name": "create_game_object", "game_object_def": self.enemy_def, "class": "Enemy",
             "coords": new_enemy_position_coords3})

