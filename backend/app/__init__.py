from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from .config import Config

# extensions

db = SQLAlchemy()
ma = Marshmallow()
jwt = JWTManager()


def create_app() -> Flask:
    """Application factory."""
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    ma.init_app(app)
    jwt.init_app(app)
    CORS(app)

    from .routes import register_routes
    register_routes(app)

    with app.app_context():
        db.create_all()

    return app
