import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager, login_user
from .config import config
from . import commands

db = SQLAlchemy()
login_manager = LoginManager()


def create_app(config_name='default'):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)

    app.config.from_object(config[config_name])

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # register customer command
    commands.init_app(app)

    # plugins
    db.init_app(app)
    migrate = Migrate(app, db)
    login_manager.init_app(app)

    app.secret_key = 'super secret key'

    # blueprint registration
    from .modules.main import main
    app.register_blueprint(main)

    from .api import api
    app.register_blueprint(api)

    from .modules.domain import domain
    app.register_blueprint(domain)

    from .modules.intent import intent
    app.register_blueprint(intent)

    from .modules.action import action
    app.register_blueprint(action)

    from .modules.story import story
    app.register_blueprint(story)

    @app.shell_context_processor
    def make_shell_context():
        from .model import User, Domain, Action
        return dict(app=app, db=db, User=User, Domain=Domain, Action=Action)

    @app.before_request
    def login():
        from .model import User
        user = User.query.get(1)
        if user:
            login_user(user)

    return app
