class Entity:
    def __init__(self, id):
        self.id = id
        self.links = {}

    def get_id(self):
        return self.id

    def set_id(self, id):
        self.id = id

    def get_links(self):
        return self.links

    def set_links(self, links):
        self.links = links

    def add_to_links(self, entity, value):
        self.links[entity] = value

    def get_link(self, entity):
        return self.links.get(entity)