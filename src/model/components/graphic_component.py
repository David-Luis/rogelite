from src.model.components.component import Component


class GraphicComponent(Component):

    def __init__(self, graphic_id):
        Component.__init__(self, "GraphicComponent")
        self.graphic_id = graphic_id



