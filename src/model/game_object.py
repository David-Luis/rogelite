class GameObject:

    def __init__(self):
        self._components = {}

    def add_component(self, component):
        if component.type not in self._components:
            self._components[component.type] = []

        self._components[component.type].append(component)

    def get_components_by_type(self, type):
        if type not in self._components:
            return None

        return self._components[type]

