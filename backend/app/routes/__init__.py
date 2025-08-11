from flask import Flask
from .certificates import bp as certificates_bp
from .products import bp as products_bp
from .alerts import bp as alerts_bp
from .auth import bp as auth_bp


def register_routes(app: Flask) -> None:
    app.register_blueprint(certificates_bp, url_prefix="/api/certificates")
    app.register_blueprint(products_bp, url_prefix="/api/products")
    app.register_blueprint(alerts_bp, url_prefix="/api/alerts")
    app.register_blueprint(auth_bp, url_prefix="/api/auth")
