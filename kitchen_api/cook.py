import threading, itertools, time, requests, json, random
from datetime import datetime
import config, menu


class Cook(threading.Thread):
    cook_id = itertools.count()
    def __init__(self, order_list, food_list, serve_lock, apparatus_lock, identity = {}, apparatuses = [], *args, **kwargs):
        super(Cook, self).__init__(*args, **kwargs)
        self.food_list = food_list
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
            with item["food_lock"]:
                if not item["prepared"]:
                    if self.rank == item["food"]["complexity"] or (self.rank - item["food"]["complexity"] == 1):
                        if not item["food"]["cooking-apparatus"] and not self.i_use_apparatus:
                            preparation_time = item['food']['preparation-time'] * config.TIME_UNIT
                            time.sleep(preparation_time)
                            item["prepared"] = True
                            item["cook_id"] = self.id
                            print(f"New food cooked - cook: {item['cook_id']}, cook's rank {self.rank}, order_id: {item['order_id']}, food_id: {item['food']['id']}, food_complexity: {item['food']['complexity']}, time to cook: {preparation_time} food: {item['food']['name']}")
                            # return to beginnig to check if we have something in apparatuses
                        else:
                            # get apparatus
                            if apparatus := self.__get_apparatus(item["food"]["cooking-apparatus"]):
                                # check if the food is in apparatus being prepared
                                if p_food := apparatus.get(item["food"]["id"], self.id):
                                    # check food state/time
                                    if (preparation_time := (int(datetime.now().timestamp()) - p_food["preparation_time_start"])*config.TIME_UNIT) >= (item['food']['preparation-time']*config.TIME_UNIT):
                                        # food is ready, need to remove it from apparatus and process
                                        apparatus.remove(item['food']['id'], self.id)
                                        self.i_use_apparatus = False
                                        item["prepared"] = True
                                        item["cook_id"] = self.id
                                        print(f"New food cooked - cook: {item['cook_id']}, cook's rank {self.rank}, order_id: {item['order_id']}, food_id: {item['food']['id']}, food_complexity: {item['food']['complexity']}, time to cook: {preparation_time} food: {item['food']['name']}, apparatus: {item['food']['cooking-apparatus']}")
                                else:
                                    # no such food in apparatus, we need to put it there for preparation
                                    # lock apparatus before putting something
                                    if self.apparatus_lock.acquire(blocking=False):
                                        if apparatus.put({"food": item["food"], "cook_id": self.id, "preparation_time_start": int(datetime.now().timestamp())}):
                                            print(f"Food: {item['food']['id']} is in {apparatus.type}, preparation began.")
                                            self.i_use_apparatus = True
                                            self.apparatus_lock.release()
                            else:
                                # no such apparatus, should we skip and remove this food or halt our work?
                                print(f"No such apparatus: {item['food']['cooking-apparatus']}")
                        break
            with self.serve_lock:
                self.__serve_order(item)
        
    def __serve_order(self, food):
        prepared_food = []
        cooking_details = []
        for food_item in self.food_list:
            if food_item["order_id"] == food["order_id"] and food_item["prepared"]:
                prepared_food.append({"food_id": food_item["food"]["id"], "cook_id": food_item["cook_id"]})
        
        if len(prepared_food) > 0:
            for order in self.order_list:
                with order["lock"]:
                    if order["order"]["order_id"] == food["order_id"]:
                        if len(order["order"]["items"]) == len(prepared_food):
                            order["order"]["cooking_details"] = prepared_food
                            requests.post(config.DINING_HALL_URL, data=json.dumps(order["order"]), headers={"Content-Type": "application/json"})
                            print(f"Cook {self.id}, {self.name}, sent order back to dining hall: {order['order']}")
                            self.__remove_foods(food["order_id"])
                            break

    def __remove_foods(self, order_id):
        # get position of foods with right order_id
        orders = []
        for idx, food in enumerate(self.food_list):
            if food["order_id"] == order_id:
                orders.append(idx)
        
        for idx in orders:
            del(self.food_list[idx])
        
        print(f"Foods left in food list: {len(self.food_list)}")
    
    def __get_apparatus(self, apparatus_type):
        for apparatus in self.apparatuses:
            if apparatus.type == apparatus_type:
                return apparatus
        return None