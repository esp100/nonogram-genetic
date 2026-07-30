from flask import Flask
from project.adapters.assembly import Container
import os
import sys

def create_app():
    app = Flask(__name__, instance_relative_config=True)

    container = Container()
    app.container = container
    container.wire(modules=[sys.modules[__name__]])

    from project.blueprints.main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app