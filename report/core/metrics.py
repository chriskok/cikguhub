class Metric:
    def __init__(self, name, description, icon):
        self.name = name
        self.description = description
        self.icon = icon

    def to_view(self, val):
        return {
            'name': self.name,
            'description': self.description,
            'icon': self.icon,
            'value': val
        }
