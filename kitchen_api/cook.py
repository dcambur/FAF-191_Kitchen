import threading, itertools, time, requests, json, random
import config, menu


class Cook(threading.Thread):
    cook_id = itertools.count()

    def __init__(self, order_list, food_list, identity = {}, *args, **kwargs):
        super(Cook, self).__init__(*args, **kwargs)
        self.food_list = food_list
        self.order_list = order_list
        self.id = next(self.cook_id)
        self.name = identity["name"]
        self.catchphrase = identity["catchphrase"]
        self.rank = identity["rank"]
        self.proficiency = identity["proficiency"]
        self.title = identity["title"]

    def run(self):
        while True:
            self.cook_order()

    def cook_order(self): 
        for idx, item in enumerate(self.food_list):
            time.sleep(random.randint(0, 3) * config.TIME_UNIT)
            with item["food_lock"]:
                if not item["prepared"]:
                    preparation_time_start = item['food']['preparation-time'] - item['food']['preparation-time']*0.1
                    preparation_time_end = item['food']['preparation-time'] + item['food']['preparation-time']*0.1
                    preparation_time = round(random.uniform(preparation_time_start, preparation_time_end)*config.TIME_UNIT, 2)
                    time.sleep(preparation_time)
                    print(f"New food cooked - cook: {self.id}, order_id: {item['order_id']}, food_id: {item['food']['id']}, time to cook: {preparation_time} food: {item['food']['name']}")
                    item["prepared"] = True
                    item["cook_id"] = self.id

            self._serve_order(item)
        
    # FIXME: check locking because of duplicate sendings
    def _serve_order(self, food):
        print(f"In serve test order, food_id: {food['food']}")
        prepared_food = []
        cooking_details = []
        for food_item in self.food_list:
            if food_item["order_id"] == food["order_id"] and food_item["prepared"]:
                prepared_food.append({"food_id": food_item["food"]["id"], "cook_id": food_item["cook_id"]})
        
        print(f"Prepared foods: {prepared_food}")

        if len(prepared_food) > 0:
            for order in self.order_list:
                with order["lock"]:
                    if order["order"]["order_id"] == food["order_id"]:
                        if len(order["order"]["items"]) == len(prepared_food):
                            # prepare and send order back
                            order["order"]["cooking_details"] = prepared_food
                            requests.post(config.DINING_HALL_URL, data=json.dumps(order["order"]), headers={"Content-Type": "application/json"})
                            print(f"Order sent back to dining hall: {order['order']}")
                            
                            # clean up food list and order list
                            self._remove_foods(prepared_food)
                            break

    def _remove_foods(self, foods):
        for food in foods:
            if food in self.food_list:
                print(f"Food removed from list: {food}")
                with food["food_lock"]:
                    self.food_list.remove(food)

