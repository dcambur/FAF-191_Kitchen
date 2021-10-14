import threading, queue
import config
from cook import Cook
from flask import Flask, request


app = Flask(__name__)
cooks = []
cook_pipes = []
orders = []
aparatus = []

@app.route('/order', methods=['POST'])
def processor():
    if request:
        r = request.get_json(force=True)
        print(r)
        
    return "Ok"


if __name__ == "__main__":
    # start order processor
    processor_thread = threading.Thread(target=lambda: app.run(host='0.0.0.0', port='5000', debug=True, use_reloader=False))
    processor_thread.start()

    # start cooks
    for cook_identity in config.COOKS:
        print(cook_identity)
        pipe = queue.Queue()
        cook = Cook(pipe, identity=cook_identity)
        cooks.append(cook)
        cook_pipes.append(pipe)
        cook.start()

    for c in cooks:
        c.join()

    processor_thread.join()