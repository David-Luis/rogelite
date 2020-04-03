from src.model.game_object import GameObject

import pytweening

class Enemy(GameObject):
    def __init__(self, game_objects_factory_cls):
        GameObject.__init__(self, game_objects_factory_cls)

        self.attack_duration = 0.15
        self.attacking = False
        self.current_animation_time = 0.0
        self.attack_direction = 1

    def update(self, delta_time):
        if self.attacking:
            self.graphic_component.local_pos[0] = pytweening.linear(self.current_animation_time / self.attack_duration) * 30 * self.attack_direction
            self.current_animation_time += delta_time
            if self.current_animation_time >= self.attack_duration:
                self.graphic_component.local_pos[0] = 0.0
                self.attacking = False

    def on_component_event(self, event):
        if event["name"] == "attack":
            self.attack(event["game_object"])
        if event["name"] == "move":
            if event["direction"] == "LEFT":
                self.graphic_component.flipped = True
            elif event["direction"] == "RIGHT":
                self.graphic_component.flipped = False

    def attack(self, game_object):
        self.attacking = True
        self.current_animation_time = 0.0
        if game_object.has_component_of_type("GraphicComponent"):
            graphic_component = self.get_components_by_type("GraphicComponent")[0]
            if game_object.tile.coords[1] < self.tile.coords[1]:
                self.attack_direction = -1
                graphic_component.flipped = True
            elif game_object.tile.coords[1] > self.tile.coords[1]:
                self.attack_direction = 1
                graphic_component.flipped = False

    def on_create(self):
        self.graphic_component = self.get_components_by_type("GraphicComponent")[0]