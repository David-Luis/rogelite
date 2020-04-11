class UIUtils:

    @classmethod
    def disable_all(cls, ui_element):
        if ui_element:
            try:
                ui_element.was_enabled = ui_element.is_enabled
                ui_element.disable()
            except:
                pass
            try:
                for element in ui_element.elements:
                    cls.disable_all(element)
            except:
                pass

    @classmethod
    def enable_all(cls, ui_element):
        if ui_element:
            try:
                if ui_element.was_enabled:
                    ui_element.enable()
            except:
                pass
            try:
                for element in ui_element.elements:
                    cls.enable_all(element)
            except:
                pass
