import threading, itertools, time, requests, json, random
from datetime import datetime
import config, menu


class Cook(threading.Thread):
    cook_id = itertools.count()
    def __init__(self, order_list, food_list, food_list_lock, serve_lock, apparatus_lock, identity = {}, apparatuses = [], *args, **kwargs):
        super(Cook, self).__init__(*args, **kwargs)
        self.food_list = food_list
        self.food_list_lock = food_list_lock
        self.order_list = order_list
        self.id = next(self.cook_id)
        self.serve_lock = serve_lock
        self.apparatus_lock = apparatus_lock
        self.name = identity["name"]
        self.catchphrase = identity["catchphrase"]
        self.rank = identity["rank"]
        self.proficiency = identity["proficiency"]
        self.title = identity["title"]
        self.apparatuses = apparatuses
        self.i_use_apparatus = False

    def run(self):
        while True:
            self.cook_food()

    def cook_food(self): 
        for item in self.food_list:
            if item["food_lock"].acquire(blocking=False):
                if not item["prepared"]:
                    if self.rank - item["food"]["complexity"] in range(0, 2):
                        if item["food"]["cooking-apparatus"] == None and not self.i_use_apparatus:
                            preparation_time_start = item['food']['preparation-time'] - item['food']['preparation-time']*0.1
                            preparation_time_end = item['food']['preparation-time'] + item['food']['preparation-time']*0.1
                            preparation_time = round(random.uniform(preparation_time_start, preparation_time_end)*config.TIME_UNIT, 2)
                            time.sleep(preparation_time)
                            item["prepared"] = True
                            item["cook_id"] = self.id
                            print(f"New food cooked - cook: {item['cook_id']}, cook's rank {self.rank}, order_id: {item['order_id']}, food_id: {item['food']['id']}, food_complexity: {item['food']['complexity']}, time to cook: {preparation_time} food: {item['food']['name']}")
                        else:
                            # get apparatus
                            if (apparatus := self.__get_apparatus(item["food"]["cooking-apparatus"])) != None:
                                # check if the food is in apparatus being prepared
                                if p_food := apparatus.get(item["food"]["id"], self.id):
                                    # check food state/time
                                    if (preparation_time := (int(datetime.now().timestamp()) - p_food["preparation_time_start"])*config.TIME_UNIT) >= (item['food']['preparation-time']*config.TIME_UNIT):
                                        # food is ready, need to remove it from apparatus and process
                                        apparatus.remove(item['food']['id'], self.id)
                                        if apparatus.count(self.id) == 0:
                                            self.i_use_apparatus = False
                                        item["prepared"] = True
                                        item["cook_id"] = self.id
                                        print(f"New food cooked - cook: {item['cook_id']}, cook's rank {self.rank}, order_id: {item['order_id']}, food_id: {item['food']['id']}, food_complexity: {item['food']['complexity']}, time to cook: {preparation_time} food: {item['food']['name']}, apparatus: {item['food']['cooking-apparatus']}")
                                else:
                                    # no such food in apparatus, we need to put it there for preparation
                                    # lock apparatus before putting something
                                    if self.apparatus_lock.acquire(blocking=False):
                                        if apparatus.put({"food": item["food"], "cook_id": self.id, "preparation_time_start": int(datetime.now().timestamp())}):
                                            self.i_use_apparatus = True
                                        self.apparatus_lock.release()
                        #if item["food_lock"].locked():
                        #    item["food_lock"].release()
                        #break
                item["food_lock"].release()
            self.__serve_order(item)
        
    def __serve_order(self, food):
        prepared_food = []
        for food_item in self.food_list:
            if food_item["order_id"] == food["order_id"] and food_item["prepared"]:
                prepared_food.append({"food_id": food_item["food"]["id"], "cook_id": food_item["cook_id"]})
        
        if len(prepared_food) > 0:
            with self.serve_lock:
                for order in self.order_list:
                    if order["order"]["order_id"] == food["order_id"] and order["order"]["state"] == 1:
                        if len(order["order"]["items"]) == len(prepared_food):
                            order["order"]["cooking_details"] = prepared_food
                            order["order"]["state"] = 2
                            requests.post(config.DINING_HALL_URL, data=json.dumps(order["order"]), headers={"Content-Type": "application/json"})
                            print(f"Cook {self.id}, {self.name}, sent order back to dining hall: {order['order']}")
                            break

    def __get_apparatus(self, apparatus_type):
        for apparatus in self.apparatuses:
            if apparatus.type == apparatus_type:
                return apparatus
        return None