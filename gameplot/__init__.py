import logging
import os
from typing import Any


def create_app(test_config: Any = None):
    from flask import Flask

    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)

    # load config vars from environment -- like FLASK_DATABASE_HOST becomes config["DATABASE_HOST"]
    app.config.from_prefixed_env()
    match app.config.get("LOG_LEVEL", "").lower(): # type: ignore
        case "debug":
            logging.basicConfig(level=logging.DEBUG)
        case "warn":
            logging.basicConfig(level=logging.WARN)
        case _:
            logging.basicConfig(level=logging.DEBUG)


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

    from . import commands, db, views, auth
    db.init_app(app)
    commands.register_commands(app)
    views.register_blueprints(app)
    auth.init_app(app)

    # a simple page that says hello
    @app.route('/hello')
    def hello() -> str:
        d = db.get_db()
        return f'Hello, World! Got db  asdas object {str(d)}'

    return app