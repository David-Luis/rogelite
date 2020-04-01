from src.model.components.component import Component

class EnemySpawnerComponent(Component):

    def __init__(self, game_object, enemy_def):
        Component.__init__(self, game_object, "EnemySpawnerComponent")
        self.enemy_def = enemy_def

    def on_destroy(self):
        new_enemy_position_coords1 = self.game_object.tile.coords[:]
        new_enemy_position_coords1[1] += 1

        new_enemy_position_coords2 = self.game_object.tile.coords[:]
        new_enemy_position_coords2[0] -= 1

        new_enemy_position_coords3 = self.game_object.tile.coords[:]
        new_enemy_position_coords3[0] += 1

        self.game_object.game_objects_factory_cls.add_enemy_game_object( self.enemy_def, new_enemy_position_coords1[0], new_enemy_position_coords1[1])
        self.game_object.game_objects_factory_cls.add_enemy_game_object(self.enemy_def, new_enemy_position_coords2[0], new_enemy_position_coords2[1])
        self.game_object.game_objects_factory_cls.add_enemy_game_object(self.enemy_def, new_enemy_position_coords3[0], new_enemy_position_coords3[1])

