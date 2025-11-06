import psycopg
from psycopg_pool import ConnectionPool
from psycopg.rows import namedtuple_row
from operator import itemgetter
from typing import cast, LiteralString
import logging
import flask
from flask import current_app, g

def _get_maintenance_db() -> psycopg.Connection:
    """Returns a connection to the database matching the name of the Postgres user in the config."""
    host, port, user, password = \
        itemgetter("DATABASE_HOST", "DATABASE_PORT", "DATABASE_USER", "DATABASE_PASSWORD")(current_app.config)
    connString = f"postgresql://{user}:{password}@{host}:{port}/{user}"
    logging.info("Connecing to maintenance DB (%s)", connString)
    return psycopg.connect(connString, autocommit=True)

def get_db():
    """Returns a context manager which gives a connection to the database specified in the config."""
    if 'dbpool' not in g:
        host, name, port, user, password = \
            itemgetter("DATABASE_HOST", "DATABASE_NAME", "DATABASE_PORT", "DATABASE_USER", "DATABASE_PASSWORD")(current_app.config)
        connString = f"postgresql://{user}:{password}@{host}:{port}/{name}"
        logging.info("Connecing to DB (%s)", connString)
        g.dbpool = ConnectionPool(connString, kwargs={'row_factory':namedtuple_row})
    return g.dbpool.connection()

def teardown_db(exception: BaseException | None = None):
    dbpool = g.pop('dbpool', None)
    if dbpool is not None:
        dbpool.close()

def reset_db():
    """Incredibly dangerous. Gets the current maintenance DB connection and deletes everything from the table. Then makes a new blank DB in its place."""
    dbname: str = current_app.config["DATABASE_NAME"]
    logging.warning("Recreating the database %s", dbname)
    with _get_maintenance_db() as db:
        db.execute(cast(LiteralString, f"DROP DATABASE IF EXISTS {dbname} WITH (FORCE)"))
        db.execute(cast(LiteralString, f"CREATE DATABASE {dbname}"))

def init_db():
    """Loads the schema into the connected DB."""
    with get_db() as db:
        with current_app.open_resource('schema.sql') as f:
            q = cast(LiteralString, f.read().decode('utf8')) # type: ignore
            logging.info("Initializing the DB with the schema %s", q)
            db.execute(q)

def seed_db():
    """Seeds the DB with test data"""
    with get_db() as db:
        with current_app.open_resource('seed.sql') as f:
            q = cast(LiteralString, f.read().decode('utf8')) # type: ignore
            logging.info("Seeding the DB with the initial data %s", q)
            db.execute(q)

def init_app(app: flask.Flask):
    app.teardown_appcontext(teardown_db)
