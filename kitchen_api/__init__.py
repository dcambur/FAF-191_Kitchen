from flask import Flask
from .views import kitchen


def create_app(config_object):
    app = Flask(__name__)
    app.config.from_object(config_object)

    app.register_blueprint(kitchen)
    return app
