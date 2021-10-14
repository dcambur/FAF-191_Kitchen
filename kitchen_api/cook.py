import threading, queue, itertools, time, requests, json, random
import config

class Cook(threading.Thread):
    cook_id = itertools.count()

    def __init__(self, q, name = "", loop_time = 1.0/60, *args, **kwargs):
        self.q = q
        self.timeout = loop_time
        self.id = next(self.waiter_id)
        super().__init__(*args, **kwargs)

    def run(self):
        pass