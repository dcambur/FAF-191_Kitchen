import threading, itertools, time, requests, json, random
import config, menu


class Cook(threading.Thread):
    cook_id = itertools.count()

    def __init__(self, food_list, identity = {}, loop_time = 1.0/60, *args, **kwargs):
        super(Cook, self).__init__(*args, **kwargs)
        self.food_list = food_list
        self.timeout = loop_time
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
                    self.food_list[idx]["prepared"] = True

