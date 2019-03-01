import click
from flask.cli import with_appcontext
from flask_migrate import upgrade


@click.command('init-db')
@with_appcontext
def init_db_command():
    """Clear the existing data and create new tables."""
    upgrade()
    from .model import User, db
    u = User.query.filter_by(email='demos@gammalab.us').first()
    if not u:
        u = User(email='demos@gammalab.us', password='test')
        db.session.add(u)
        db.session.commit()
        click.echo('Add new user(email: demos@gammalab.us password: test)')
    click.echo('Initialized the database.')


def init_app(app):
    app.cli.add_command(init_db_command)
