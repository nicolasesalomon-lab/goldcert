from flask import Flask, jsonify, redirect
from flask_smorest import Api
from .config import Config
from .extensions import db, ma, migrate, jwt, cors
from .routes.auth import blp as AuthBP
from .routes.providers import blp as ProvidersBP
from .routes.factories import blp as FactoriesBP
from .routes.audits import blp as AuditsBP
from .routes.products import blp as ProductsBP
from .routes.models_routes import blp as ModelsBP
from .routes.certificates import blp as CertificatesBP
from .routes.attachments import blp as AttachmentsBP
from .routes.alerts import blp as AlertsBP
from .routes.djc import blp as DjcBP

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app); ma.init_app(app); migrate.init_app(app, db, directory="app/migrations"); jwt.init_app(app); cors.init_app(app)
    api = Api(app, spec_kwargs={"title":"GoldCert API v2","version":"2.0.0","openapi_version":"3.1.0"})
    api.register_blueprint(AuthBP, url_prefix="/api/auth")
    api.register_blueprint(ProvidersBP, url_prefix="/api/v2/providers")
    api.register_blueprint(FactoriesBP, url_prefix="/api/v2/factories")
    api.register_blueprint(AuditsBP, url_prefix="/api/v2/audits")
    api.register_blueprint(ProductsBP, url_prefix="/api/v2/products")
    api.register_blueprint(ModelsBP, url_prefix="/api/v2/models")
    api.register_blueprint(CertificatesBP, url_prefix="/api/v2/certificates")
    api.register_blueprint(AttachmentsBP, url_prefix="/api/v2/attachments")
    api.register_blueprint(AlertsBP, url_prefix="/api/v2/alerts")
    api.register_blueprint(DjcBP, url_prefix="/api/v2/djc")
    @app.get("/api/health")
    def health(): return jsonify(status="ok")
    @app.get("/api/docs")
    def docs(): return redirect("/swagger-ui")
    return app
