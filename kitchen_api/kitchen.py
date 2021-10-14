import threading, queue
import config
from cook import Cook
from flask import Flask, request

app = Flask(__name__)

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

    processor_thread.join()