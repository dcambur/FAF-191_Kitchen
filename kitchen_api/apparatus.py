import itertools
import config, menu


class Apparatus():
    apparatus_id = itertools.count()
    def __init__(self, identity = {}):
        self.id = next(self.apparatus_id)
        self.type = identity["type"]
        self.maxsize = identity["quantity"]
        self.food = []

    def put(self, food):
        if len(self.food) == self.maxsize:
            return False
        self.food.append(food)
        return True

    def get(self, cook_id):
        pass

    def remove(self, food_id):
        pass
        