import json

from sprite_groups import sprite_groups


class Entity():
    def __init__(self):
        self._id = id(self)
        self.components = {}

    def add(self, c, a):
        if c not in self.components.keys():
            self.components[c] = c(**a)
        else:
            raise Exception("cannot add duplicate components: %s to the same entity %s" % (c, self))


class EM():
    entities = {}
    components = {}
    ce_mapping = {}

    @classmethod
    def create(cls, components=None, arguments=None):
        e = Entity()
        EM.entities[e._id] = e

        if components:
            for i, c in enumerate(components):
                if arguments:
                    e.add(c, arguments[i])
                else:
                    e.add(c, {})
                cls.map_components(e, c)
        return e

    @classmethod
    def register_component(cls, c):
        if c.__name__ not in EM.components.keys():
            EM.components[c.__name__] = c
        else:
            raise Exception("components %s already registered" % c.__name__)

    @classmethod
    def map_components(cls, e, c):
        if c not in EM.ce_mapping.keys():
            EM.ce_mapping[c] = []
        EM.ce_mapping[c].append(e._id)

    @classmethod
    def entities_of_component(cls, *components):
        result = []

        for c in components:
            entities = EM.ce_mapping.get(c, [])
            for e_id in entities:
                if all(c in list(EM.entities[e_id].components.keys()) for c in components):
                    if e_id not in result:
                        result.append(EM.entities[e_id])

        return result


    @classmethod
    def ids_of_component(cls, *components):
        result = []

        for c in components:
            entities = EM.ce_mapping.get(c, [])
            for e_id in entities:
                if all(c in list(EM.entities[e_id].components.keys()) for c in components):
                    if e_id not in result:
                        result.append(e_id)

        return result

    @classmethod
    def destroy(cls, e_id):
        if e_id in EM.entities.keys():
            del EM.entities[e_id]
            for key in EM.ce_mapping.keys():
                if e_id in EM.ce_mapping[key]:
                    EM.ce_mapping[key].remove(e_id)
        else:
            raise Exception("cant destroy e: %s - doesnt exist" % _id)

    @classmethod
    def add(cls, e):
        if not isinstance(e, Entity):
            raise Exception("e: %s - is not an instance of Entity" % e)

        EM.entities[e._id] = e

    @classmethod
    def alive(cls, e_id):
        return e_id in EM.entities.keys()

    @classmethod
    def flush(cls):
        EM.entities = {}


def register_components(components):
    for c in components:
        EM.register_component(c)

def init_groups(groups_json):
    with open(groups_json) as f:
        groups_data = json.load(f)

    for g in groups_data["groups"]:
        sprite_groups.create(g)

def load_entities(entities_json):
    with open(entities_json) as f:
        data = json.load(f) 

    for e, d in data.items():
        components = []
        arguments = []
        for c in d["components"].keys():
            components.append(EM.components[c])
            arguments.append(d["components"][c])
        EM.create(components, arguments)
