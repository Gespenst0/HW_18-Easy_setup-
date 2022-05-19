from flask import Flask
from flask_restx import Api
from app.config import Config
from app.setup_db import db
from views.directors import directors_ns
from views.genres import genres_ns
from views.movies import movies_ns


def create_app(config):
    application = Flask(__name__)
    application.config.from_object(config)
    application.app_context().push()
    register_extensions(application)
    return application


def register_extensions(app):
    db.init_app(app)
    api = Api(app)
    api.add_namespace(genres_ns)
    api.add_namespace(directors_ns)
    api.add_namespace(movies_ns)


if __name__ == '__main__':
    app_config = Config()
    app = create_app(app_config)
    app.run(debug=True)
