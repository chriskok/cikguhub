class Metric:
    def __init__(self, name, description, icon_url):
        self.name = name
        self.description = description
        self.icon_url = icon_url

    def to_view(self, val):
        return {
            'name': self.name,
            'description': self.description,
            'icon_url': self.icon_url,
            'value': val
        }
