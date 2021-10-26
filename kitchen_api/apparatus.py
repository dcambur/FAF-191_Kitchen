import itertools
import config, menu


class Apparatus():
    apparatus_id = itertools.count()
    def __init__(self, identity = {}):
        self.id = next(self.apparatus_id)
        self.type = identity["type"]
        self.maxsize = identity["quantity"]
        self.foods = []

    def put(self, food):
        if len(self.foods) == self.maxsize:
            return False
        self.foods.append(food)
        return True

    def get(self, food_id, cook_id):
        for food in self.foods:
            if food["food"]["id"] == food_id and food["cook_id"] == cook_id:
                return food
        return None

    def remove(self, food_id, cook_id):
        idx_to_remove = None
        for idx, food in enumerate(self.foods):
            if food["food"]["id"] == food_id and food["cook_id"] == cook_id:
                idx_to_remove = idx
                break
        if idx_to_remove:
            del(self.foods[idx_to_remove])
            return True
        return False