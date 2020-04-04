from src.model.components.component import Component


class DestructibleComponent(Component):

    def __init__(self, game_object, descriptor):
        Component.__init__(self, game_object, "DestructibleComponent")
        self.life = descriptor["life"]

        self.create_when_destroy = None
        if "create_when_destroy" in descriptor:
            self.create_when_destroy = descriptor["create_when_destroy"]

    def receive_attack(self, strength):
        self.life -= strength
        if self.life <= 0:
            self.game_object.mark_as_destroy()

    def on_destroy(self):
        if self.create_when_destroy:
            self.game_object.on_component_event(self,
                {"name": "create_game_object", "game_object_def": self.create_when_destroy,
                 "coords": self.game_object.tile.coords})
