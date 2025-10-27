from flask import Blueprint, render_template
from gameplot.db import get_db

bp = Blueprint('toplevel', __name__, url_prefix='/')

@bp.route('/', methods=['GET'])
def index() -> str:
    return "Hello world!! Gameplot v0"
