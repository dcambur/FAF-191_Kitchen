import queue, itertools
import config, menu


class Apparatus(queue.Queue):
    apparatus_id = itertools.count()
    def __init__(self, a_type="", *args, **kwargs):
        self.id = next(self.apparatus_id)
        self.type = a_type
        super(Apparatus, self).__init__(*args, **kwargs)
