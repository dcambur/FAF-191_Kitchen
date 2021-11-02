import threading
import config, menu
from cook import Cook
from apparatus import Apparatus
from flask import Flask, request


app = Flask(__name__)
cooks = []
orders = []
food_list = []
apparatuses = []
serve_lock = threading.Lock()
apparatus_lock = threading.Lock()
food_list_lock = threading.Lock()

@app.route('/order', methods=['POST'])
def processor():
    if request:
        r = request.get_json()
        print(f"New order received: {r}")
        with food_list_lock:
            for item in r["items"]:
                for menu_item in menu.menu:
                    if item == menu_item["id"]:
                        food_lock = threading.Lock()
                        food_list.append({"order_id": r["order_id"], "food": menu_item, "food_lock": food_lock, "prepared": False})
        order_lock = threading.Lock()
        with serve_lock:
            orders.append({"order": r, "lock": order_lock})
        
    return "Ok"


if __name__ == "__main__":
    # start apparatuses
    for apparatus in config.APPARATUSES:
        a = Apparatus(identity=apparatus)
        apparatuses.append(a)

    # start order processor
    processor_thread = threading.Thread(target=lambda: app.run(host='0.0.0.0', port='5000', debug=True, use_reloader=False))
    processor_thread.start()

    # start cooks
    for cook_identity in config.COOKS:
        cook = Cook(orders, food_list, food_list_lock, serve_lock, apparatus_lock, identity=cook_identity, apparatuses=apparatuses)
        cooks.append(cook)
        cook.start()

    for c in cooks:
        c.join()

    processor_thread.join()