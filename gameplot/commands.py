import click
from . import db
import logging
logger = logging.getLogger(__name__)

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    import flask

@click.command('reset-db')
def init_db_command():
    """Clear the existing data and create new tables."""
    db.reset_db()
    db.init_db()
    click.echo('Initialized the database.')

@click.command('seed-db')
def seed_db_command():
    """Seed the database with test data."""
    db.seed_db()
    click.echo('Seeded the database.')

@click.command('worker')
def run_worker():
    """Start polling the database for pending jobs."""
    logger.error("IMPLEMENT ME!")

def register_commands(app: flask.Flask):
    """Register all commands with flask."""
    app.cli.add_command(init_db_command)
    app.cli.add_command(seed_db_command)
    app.cli.add_command(run_worker)