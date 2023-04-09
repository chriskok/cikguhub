class Metric:
    def __init__(self, name, icon_url, description_beginner, description_intermediate, description_master, definition):
        self.name = name
        self.icon_url = icon_url
        self.description_beginner = description_beginner
        self.description_intermediate = description_intermediate
        self.description_master = description_master
        self.definition = definition

    def to_view(self, val):
        # We want to show different descriptions in different value ranges
        print("CHECK KEN: to_view ran!")
        selected_description = ""
        if val <= 33:
            selected_description = self.description_beginner
        elif val <= 66:
            selected_description = self.description_intermediate
        else:
            selected_description = self.description_master

        tooltip = "Definition:\n{}\n\nYour score means:\n{}".format(self.definition, selected_description)

        return {
            'name': self.name,
            'tooltip': tooltip,
            'icon_url': self.icon_url,
            'value': val
        }
