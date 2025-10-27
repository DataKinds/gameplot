import psycopg
from psycopg import sql
from datetime import datetime
from operator import itemgetter
from typing import cast, LiteralString
import logging
import flask
from flask import current_app, g


def get_db() -> psycopg.Connection:
    if 'db' not in g:
        host, port, dbname, user, password = \
            itemgetter("DATABASE_HOST", "DATABASE_PORT", "DATABASE_NAME", "DATABASE_USER", "DATABASE_PASSWORD")(current_app.config)
        connString = f"host={host} port={port} dbname={dbname} user={user} password={password}"
        logging.info("Connecing to DB (%s)", connString)
        print("AAAAAAAAAAAAAAAAAAA")
        g.db = psycopg.connect(connString)
    return g.db

def teardown_db(exception: BaseException | None = None):
    db = g.pop('db', None)
    if db is not None:
        db.close()

def reset_db():
    """Incredibly dangerous. Gets the current DB connection and deletes everything from the table. Then makes a new blank DB in its place."""
    db = get_db()
    with db.connect(autocommit=True) as conn:
        conn.execute(cast(LiteralString, f"DROP DATABASE IF EXISTS {current_app.config["DATABASE_NAME"]}"))
        conn.execute(cast(LiteralString, f"CREATE DATABASE {current_app.config["DATABASE_NAME"]}"))

def init_db():
    """Loads the schema into the connected DB."""
    db = get_db()
    with current_app.open_resource('schema.sql') as f:
        db.execute(f.read().decode('utf8'))

def seed_db():
    """Seeds the DB with test data"""
    db = get_db()
    with current_app.open_resource('seed.sql') as f:
        db.execute(f.read().decode('utf8'))

def init_app(app: flask.Flask):
    app.teardown_appcontext(teardown_db)
