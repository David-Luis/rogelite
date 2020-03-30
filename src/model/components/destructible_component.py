from src.model.components.component import Component


class DestructibleComponent(Component):

    def __init__(self, game_object, life):
        Component.__init__(self, game_object, "DestructibleComponent")
        self.life = life

    def receive_attack(self, strength):
        self.life -= strength
        if self.life <= 0:
            self.game_object.mark_as_destroy()
