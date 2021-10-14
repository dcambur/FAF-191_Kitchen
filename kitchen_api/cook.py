import threading, queue, itertools, time, requests, json, random
import config


class Cook(threading.Thread):
    cook_id = itertools.count()

    def __init__(self, q, identity = {}, loop_time = 1.0/60, *args, **kwargs):
        super(Cook, self).__init__(*args, **kwargs)
        self.q = q
        self.timeout = loop_time
        self.id = next(self.cook_id)
        self.name = identity["name"]
        self.catchphrase = identity["catchphrase"]
        self.rank = identity["rank"]
        self.proficiency = identity["proficiency"]
        self.title = identity["title"]

    def on_thread(self, function, *args, **kwargs):
        self.q.put((function, args, kwargs))
    
    def run(self):
        print(f"cook stated: {self.id}, id: {self.name}")
        while True:
            try:
                function, args, kwargs = self.q.get(timeout=self.timeout)
                function(*args, **kwargs)
            except queue.Empty:
                self.cook_order()

    def _send_order(self, *args, **kwargs):
        pass

    def send_order(self, *args, **kwargs):
        self.on_thread(self._serve_order, *args, **kwargs)

    def cook_order(self):
        pass
