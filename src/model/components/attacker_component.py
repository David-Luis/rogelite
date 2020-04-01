from src.model.components.component import Component

class AttackerComponent(Component):

    def __init__(self, game_object, strength):
        Component.__init__(self, game_object, "AttackerComponent")
        self.strength = strength

    def act_on_game_object(self, game_object):
        if game_object.has_component_of_type("DestructibleComponent"):
            for destructible_component in game_object.get_components_by_type("DestructibleComponent"):
                destructible_component.receive_attack(self.strength)
                self.game_object.on_component_event({"name": "attack"})
