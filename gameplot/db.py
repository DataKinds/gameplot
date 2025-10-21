import psycopg
from datetime import datetime
from operator import itemgetter

from flask import current_app, g


def get_db():
    if 'db' not in g:
        host, port, dbname, user, password = \
            itemgetter("DATABASE_HOST", "DATABASE_PORT", "DATABASE_NAME", "DATABASE_USER", "DATABASE_PASSWORD")(current_app.config)
        g.db = psycopg.connect(
            f"host={host} port={port} dbname={dbname} user={user} password={password}",
        )

    return g.db


def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()