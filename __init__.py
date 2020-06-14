from flask import Flask
from .models import db
from . import config


def create_app():
    app = Flask(__name__)
    app.secret_key = "Secret Key"
    # app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.db'
    app.config['SQLALCHEMY_DATABASE_URI'] = config.DATABASE_URI

    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.app_context().push()
    db.init_app(app)
    db.create_all()
    return app
