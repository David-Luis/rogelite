import pytweening

class AnimationsController:

    def __init__(self, game_object):
        self.game_object = game_object

        self.attack_duration = 0.15
        self.attacking = False
        self.current_animation_time = 0.0
        self.attack_direction = [0, 0]
        self.graphic_component = game_object.get_components_of_type("GraphicComponent")[0]

    def update(self, delta_time):
        if self.attacking:
            self.graphic_component.local_pos[0] = pytweening.linear(self.current_animation_time / self.attack_duration) * 30 * self.attack_direction[0]
            self.graphic_component.local_pos[1] = pytweening.linear(self.current_animation_time / self.attack_duration) * 30 * self.attack_direction[1]
            self.current_animation_time += delta_time
            if self.current_animation_time >= self.attack_duration:
                self.graphic_component.local_pos = [0, 0]
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
            graphic_component = self.game_object.get_components_of_type("GraphicComponent")[0]
            if game_object.tile.coords[1] < self.game_object.tile.coords[1]:
                self.attack_direction = [-1, 0]
                graphic_component.flipped = True
            elif game_object.tile.coords[1] > self.game_object.tile.coords[1]:
                self.attack_direction = [1, 0]
                graphic_component.flipped = False
            elif game_object.tile.coords[0] < self.game_object.tile.coords[0]:
                self.attack_direction = [0, -1]
            else:
                self.attack_direction = [0, 1]
