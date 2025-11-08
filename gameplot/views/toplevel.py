from flask import Blueprint, redirect, render_template

from gameplot.auth import login_required, login_user
from gameplot.db import get_db

bp = Blueprint('toplevel', __name__, url_prefix='/')

@bp.route('/', methods=['GET'])
def index() -> str:
    return "Hello world!! Gameplot v0"

@bp.route('/login', methods=['GET', 'POST'])
def login() -> str:
    return "Login using the form below"

@bp.route('/needsauth', methods=['GET', 'POST'])
@login_required
def needsauth() -> str:
    return "You found my special page >:)"


@bp.route('/logout', methods=['POST'])
def logout():
    return redirect('toplevel.index')
