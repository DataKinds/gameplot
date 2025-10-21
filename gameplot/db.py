import psycopg
from datetime import datetime
from operator import itemgetter

import click
from flask import current_app, g

def get_db():
    if 'db' not in g:
        host, port, dbname, user, password = \
            itemgetter("DATABASE_HOST", "DATABASE_PORT", "DATABASE_NAME", "DATABASE_USER", "DATABASE_PASSWORD")(current_app.config)
        g.db = psycopg.connect(
            f"host={host} port={port} dbname={dbname} user={user} password={password}",
        )
    return g.db

def teardown_db(exception=None):
    db = g.pop('db', None)
    if db is not None:
        db.close()

def init_db():
    db = get_db()
    with current_app.open_resource('schema.sql') as f:
        db.executescript(f.read().decode('utf8'))

@click.command('init-db')
def init_db_command():
    """Clear the existing data and create new tables."""
    init_db()
    click.echo('Initialized the database.')


def init_app(app):
    app.teardown_appcontext(teardown_db)
    app.cli.add_command(init_db_command)