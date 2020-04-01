from src.model.game_object import GameObject

import pytweening

class Player(GameObject):
    def __init__(self, game_objects_factory_cls):
        GameObject.__init__(self, game_objects_factory_cls)
        self.attack_duration = 0.15
        self.attacking = False
        self.current_animation_time = 0.0

    def update(self, delta_time):
        if self.attacking:
            self.graphic_component.local_pos[0] = pytweening.linear(self.current_animation_time / self.attack_duration) * 30
            self.current_animation_time += delta_time
            if self.current_animation_time >= self.attack_duration:
                self.graphic_component.local_pos[0] = 0.0
                self.attacking = False

    def on_component_event(self, event):
        if event["name"] == "attack":
            self.attack()

    def attack(self):
        self.attacking = True
        self.current_animation_time = 0.0

    def on_create(self):
        self.graphic_component = self.get_components_by_type("GraphicComponent")[0]