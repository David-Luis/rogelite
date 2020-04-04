from src.model.components.component import Component


class AttackerComponent(Component):

    def __init__(self, game_object, description):
        Component.__init__(self, game_object, "AttackerComponent")
        self.strength = description["strength"]
        self.can_attack_types = description["can_attack_types"]

    def act_on_game_object(self, game_object):
        if game_object.has_component_of_type("DestructibleComponent") and game_object.type in self.can_attack_types:
            for destructible_component in game_object.get_components_of_type("DestructibleComponent"):
                destructible_component.receive_attack(self.strength)
                self.game_object.on_component_event(self, {"name": "attack", "game_object": game_object})
