from flask import Blueprint, render_template
from gameplot.db import get_db

bp = Blueprint('games', __name__, url_prefix='/games')

@bp.route('/', methods=['GET'])
def index() -> str:
    db = get_db()
    games = db.execute("SELECT * FROM games;").fetchall()
    return render_template("games/index.html", games=games)

@bp.route('/<int:id>', methods=['GET'])
def game(id: int) -> str:
    return f"Gonna grab you game {id}"