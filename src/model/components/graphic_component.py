from src.model.components.component import Component


class GraphicComponent(Component):

    def __init__(self, game_object, graphic_id):
        Component.__init__(self, game_object, "GraphicComponent")
        self.graphic_id = graphic_id
        self.local_pos = [0,0]
        self.layer = 1



