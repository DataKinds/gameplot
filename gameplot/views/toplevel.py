from flask import (Blueprint, Response, flash, redirect, render_template,
                   request, url_for)

from gameplot.auth import log_out, log_user_in, login_required, new_user
from gameplot.db import get_db

bp = Blueprint('toplevel', __name__, url_prefix='/')

@bp.route('/', methods=['GET'])
def index() -> str:
    return render_template("toplevel/index.html")


@bp.route('/newuser', methods=['GET', 'POST'])
def newuser():
    match request.method:
        case 'GET':
            return render_template("toplevel/newuser.html")
        case 'POST':
            user = new_user(request.form['email'], request.form['password'])
            flash("Now you must log in.")
            return redirect(url_for('toplevel.login'))

@bp.route('/login', methods=['GET', 'POST'])
def login():
    match request.method:
        case 'GET':
            return render_template("toplevel/login.html")
        case 'POST':
            user = log_user_in(request.form['email'], request.form['password'])
            if user is None:
                flash("Failed to log in.")
                return redirect(url_for('toplevel.login'))
            flash(f"You're logged in! Hi, {user.email}")
            return redirect(url_for('toplevel.index'))
        case _: pass

@bp.route('/needsauth', methods=['GET', 'POST'])
@login_required
def needsauth(user) -> str:
    return "You found my special page >:)"


@bp.route('/logout', methods=['GET'])
def logout():
    log_out()
    flash("You've been logged out!")
    return redirect(url_for('toplevel.index'))
