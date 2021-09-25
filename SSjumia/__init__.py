from flask import Flask
from SSjumia.config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager




db=SQLAlchemy()
bcrypt=Bcrypt()
login_manager=LoginManager()
login_manager.login_view='users.login'


def create_app(config_class=Config):
    app=Flask(__name__)
    app.config.from_object(Config)

    bcrypt.init_app(app)
    db.init_app(app)
    login_manager.init_app(app)

    from SSjumia.users.routes import users
    from SSjumia.main.routes import main
    from SSjumia.admin.routes import admin
    from SSjumia.errors.handlers import errors
    app.register_blueprint(users)
    app.register_blueprint(main)
    app.register_blueprint(admin)
    app.register_blueprint(errors)

    return app