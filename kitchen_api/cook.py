import threading, itertools, time, requests, json, random
import config, menu


class Cook(threading.Thread):
    cook_id = itertools.count()

    def __init__(self, orders, identity = {}, loop_time = 1.0/60, *args, **kwargs):
        super(Cook, self).__init__(*args, **kwargs)
        self.orders = orders
        self.timeout = loop_time
        self.id = next(self.cook_id)
        self.name = identity["name"]
        self.catchphrase = identity["catchphrase"]
        self.rank = identity["rank"]
        self.proficiency = identity["proficiency"]
        self.title = identity["title"]

    def run(self):
        while True:
            for order in self.orders:
                with order["lock"]:
                    print(f"cook: {self.id}, order: {order['order']}")
            self.cook_order()

    def cook_order(self):
        pass
