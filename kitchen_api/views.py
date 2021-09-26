from flask import Blueprint

kitchen = Blueprint("kitchen", "__name__")


@kitchen.route("/order")
def kitchen_order_test():
    return {"msg": "test response"}, 200
