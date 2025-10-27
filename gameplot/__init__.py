import os
from typing import Any

from flask import Flask

from . import db, commands

import logging


def create_app(test_config: Any = None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)

    # load config vars from environment -- like FLASK_DATABASE_HOST becomes config["DATABASE_HOST"]
    app.config.from_prefixed_env()
    match f"{app.config["LOG_LEVEL"]}".lower():
        case "debug":
            logging.basicConfig(level=logging.DEBUG)
        case "warn":
            logging.basicConfig(level=logging.WARN)
        case _:
            logging.basicConfig(level=logging.INFO)


    # if test_config is None:
    #     # load the instance config, if it exists, when not testing
    #     app.config.from_pyfile('config.py', silent=True)
    # else:
    #     # load the test config if passed in
    #     app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    db.init_app(app)
    commands.register_commands(app)

    # a simple page that says hello
    @app.route('/hello')
    def hello() -> str:
        d = db.get_db()
        return f'Hello, World! Got db  asdas object {str(d)}'

    return app