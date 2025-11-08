from functools import wraps
from typing import Any, NamedTuple

from flask import Flask, current_app, g, redirect, render_template, request, session
from werkzeug.security import check_password_hash, generate_password_hash

from .db import I, Q, get_db

EXISTENCE_DURATION = '24 hours' # How long does a new or freshly-logged into token last?
SESSION_KEY = 'SULTRY_LIL_THANG'

def _session_token():
    return session.get(SESSION_KEY, [None])[0]

def login_required(route):
    """Decorator for Flask routes which need to be authenticated.
    
    Sets g.current_user on success, and passes the active user as the first argument to the route."""
    @wraps(route)
    def wrapper(*args, **kwargs):
        session_token = _session_token()
        failure = "You gotta log in bud :(", 301
        if session_token is None: return failure
        with get_db() as db:
            cur = db.execute(Q(I.CHECK_TOKEN, session_token, EXISTENCE_DURATION))
            user = cur.fetchone()
        if user is None: return failure
        g.current_user = user
        return route(user, *args, **kwargs)
    return wrapper

def log_user_in(email: str, password: str) -> NamedTuple | None : 
    """Logs a user into a flask session, if the email and password are OK. Returns the user from the DB, and adds the session token to the flask session."""
    with get_db() as db:
        cur = db.execute(Q(I.GET_USER, email))
        user = cur.fetchone()
        if user is None: return None
        if not check_password_hash(user.password.strip(), password): return None
        cur = db.execute(Q(I.NEW_TOKEN, user.id, EXISTENCE_DURATION))
        session_token = cur.fetchone()
    session[SESSION_KEY] = session_token
    return user

def log_out():
    """Logs a user out by deleting their session token."""
    session.pop(SESSION_KEY, None)

def current_user() -> NamedTuple | None:
    """Returns the current authenticated user based on the flask session."""
    session_token = _session_token()
    if session_token is None: 
        return None
    if 'current_user' in g: return g.current_user # request scoped cache
    with get_db() as db:
        cur = db.execute(Q(I.CHECK_TOKEN, session_token, '24 hours'))
        user = cur.fetchone()
    g.current_user = user
    return user


def new_user(email: str, password: str) -> NamedTuple:
    """Generates a new user from an email and a password"""
    with get_db() as db:
        hashed = generate_password_hash(password)
        cur = db.execute(Q(I.NEW_USER, email, hashed))
        return cur.fetchone()
    
def init_app(app: Flask):
    """Registers the auth specific bindings (like current_user) with Flask"""
    def template_processor():
        return dict(current_user=current_user)
    app.context_processor(template_processor)