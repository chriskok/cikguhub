import os
import pickle
from utils import generate_embedding, cosine_similarity

class Metric:
    def __init__(self, name, icon_url, description_beginner, description_intermediate, description_master, definition):
        self.name = name
        self.icon_url = icon_url
        self.description_beginner = description_beginner
        self.description_intermediate = description_intermediate
        self.description_master = description_master
        self.definition = definition

        # generate embedding
        self.embedding = generate_embedding(self.definition)
        
    def to_view(self, val):
        # We want to show different descriptions in different value ranges
        selected_description = ""
        if val <= 33:
            selected_description = self.description_beginner
        elif val <= 66:
            selected_description = self.description_intermediate
        else:
            selected_description = self.description_master

        tooltip = '<p class="tooltip-content-text"><b>Definition:</b><br> {} <br><br><b>Your score means:</b><br>{}</p>'.format(self.definition, selected_description)

        return {
            'name': self.name,
            'tooltip': tooltip,
            'icon_url': self.icon_url,
            'value': val
        }
    
    def relevance(self, embedding):
        return cosine_similarity(self.embedding, embedding)