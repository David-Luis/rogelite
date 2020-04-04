from src.model.components.component import Component


class DeleteInTimeComponent(Component):

    def __init__(self, game_object, definition):
        Component.__init__(self, game_object, "DeleteInTimeComponent")
        self.delete_in_seconds = definition["seconds"]
        self.current_time_seconds = 0.0

    def update(self, delta_time):
        self.current_time_seconds += delta_time
        if self.current_time_seconds >= self.delete_in_seconds:
            self.game_object.mark_as_destroy()


