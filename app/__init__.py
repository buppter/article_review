# -*- coding: utf-8 -*-
from flask import Flask
from flask_login import LoginManager
from flask_caching import Cache

from app.models.base import db

_Author_ = 'BUPPT'

login_manager = LoginManager()
cache = Cache()


def create_app():
    app = Flask(__name__)
    app.config.from_object("app.secure")
    app.config.from_object("app.settings")
    register_blueprint(app)

    login_manager.login_view = 'web.login'
    login_manager.login_message = "Please sign in or register"

    login_manager.init_app(app)
    cache.init_app(app)
    db.init_app(app)
    db.create_all(app=app)

    return app


def register_blueprint(app):
    from app.web import web
    app.register_blueprint(web)
