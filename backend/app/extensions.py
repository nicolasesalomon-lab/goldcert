from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from flask_marshmallow import Marshmallow
from flask import jsonify
db=SQLAlchemy(); migrate=Migrate(); jwt=JWTManager(); cors=CORS(resources={r"/api/*":{"origins":"*"}}); ma=Marshmallow()
@jwt.invalid_token_loader
def inv(reason): return jsonify(message="Invalid token", reason=reason), 401
@jwt.unauthorized_loader
def miss(reason): return jsonify(message="Missing token", reason=reason), 401
