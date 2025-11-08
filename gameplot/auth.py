from functools import wraps

from flask import current_app, session

from .db import get_db


def login_required(route):
    @wraps(route)
    def wrapper(*args, **kwargs):
        current_app.session.
        with get_db() as db:
            q = Q(I.CHECK_TOKEN)
        return f(*args, **kwargs)
    return wrapper
