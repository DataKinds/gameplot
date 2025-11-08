from functools import wraps

from flask import current_app, redirect, render_template, session, g
from werkzeug.security import check_password_hash, generate_password_hash

from .db import get_db, Q, I

EXISTENCE_DURATION = '24 hours' # How long does a new or freshly-logged into token last?
SESSION_KEY = 'SULTRY_LIL_THANG'

def login_required(route):
    """Decorator for Flask routes which need to be authenticated.
    
    Sets g.user on success, and passes the active user as the first argument to the route."""
    @wraps(route)
    def wrapper(*args, **kwargs):
        session_token = session.get(SESSION_KEY)
        failure = "You gotta log in bud :(", 301
        if session_token is None: return failure
        with get_db() as db:
            cur = db.execute(Q(I.CHECK_TOKEN, session_token, EXISTENCE_DURATION))
            user = cur.fetchone()
        if user is None: return failure
        g['user'] = user
        return route(user, *args, **kwargs)
    return wrapper

def login_user(email: str, password: str) -> str | None: 
    """Logs a user into a flask session, if the email and password are OK. Returns the login session token and adds it to the flask session."""
    with get_db() as db:
        cur = db.execute(Q(I.GET_USER, email))
        user = cur.fetchone()
        if user is None: return None
        if not check_password_hash(user.password, password): return None
        cur = db.execute(Q(I.NEW_TOKEN, email, EXISTENCE_DURATION))
        session_token = cur.fetchone()
    session[SESSION_KEY] = session_token
    return session_token

