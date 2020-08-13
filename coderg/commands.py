import click
from flask.cli import with_appcontext

from .extensions import db
from coderg.models import Post, Role, Project, User


@click.command(name='create_tables')
@with_appcontext
def create_tables():
    db.create_all()
