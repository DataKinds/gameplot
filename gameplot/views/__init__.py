from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from flask import Flask

def register_blueprints(app: Flask):
    from . import games, toplevel
    app.register_blueprint(games.bp)
    app.register_blueprint(toplevel.bp)